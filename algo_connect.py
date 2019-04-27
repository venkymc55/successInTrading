import logging
import json
import os, sys, time
import signal
from kiteconnect import KiteConnect
from datetime import datetime
from common_utils.data_mining import data_frame
from flask import Flask, request, jsonify
import schedule
from os import getenv
from threading import Thread
from common_utils import constant as const

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=const.API_KEY)

sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))))
app = Flask(__name__)

stop_run = const.STOP_RUN
last_buy_order = const.last_buy_order
last_sell_order = const.last_sell_order


@app.route('/trading', methods=['POST'])
def extreme():
    data = json.loads(request.get_data(as_text=True))
    response = main(data)
    return jsonify(response), 200


@app.route('/running', methods=['POST'])
def running():
    response = json.loads(request.get_data(as_text=True))
    return jsonify(response)


def main(data):
    requestToken = data['trading']['request_token']
    access = {}
    try:
        access = kite.generate_session(request_token=requestToken, api_secret=const.API_SECRET)
        access_token = kite.set_access_token(access['access_token'])
    except Exception as TokenError:
        logging.info("Error {}".format(TokenError))
    return access


def get_historical_data():
    try:
        data = kite.historical_data(54426119, from_date=const.from_date, to_date=const.to_date, interval=const.interval)
        # data = kite.historical_data(54334983, from_date="2019-03-02", to_date="2019-03-19", interval="5minute")
        # logging.info("Data fetched successfully")
        data_manger = data_frame(data, 10, 4, 10)
        return data_manger
    except Exception as DataFetchError:
        logging.info("info {}".format(DataFetchError))


def over_strategy(data_manager):
    ltp = last_ltp()
    ltp_price = ltp['MCX:CRUDEOILM19MAYFUT']['last_price']
    global last_buy_order
    # time = convertTimeToIndex(data_manager['time'])
    if data_manager['MA4'].iloc[-1] > data_manager['close'].iloc[-1] and (last_buy_order[0]['transaction_type'] == "SELL"):

        last_buy_order = place_order(kite.TRANSACTION_TYPE_BUY)
        logging.info("Place an Buy order {}".format(datetime.now()))

    # if moving average is lesser than last tick and there is a position
    elif (last_buy_order[0]['trigger_price'] + 54 >= ltp_price and (last_buy_order[0]['transaction_type'] == "BUY")) \
            or (ltp_price < data_manager['open'].iloc[-1] and (last_buy_order[0]['transaction_type'] == "BUY")):

        last_exit_order = exit_order(last_buy_order[0]['order_id'])
        last_buy_order[0]['transaction_type'] = "SELL"
        logging.info("Exit BUY order")
    else:
        logging.info("Wait your time is coming")

    return last_buy_order


def under_strategy(data_manager):
    ltp = last_ltp()
    ltp_price = ltp['MCX:CRUDEOILM19MAYFUT']['last_price']
    global last_sell_order
    # time = convertTimeToIndex(data_manger['time'])
    if data_manager['MA4'].iloc[-1] < data_manager['close'].iloc[-1] and (last_sell_order[0]['transaction_type'] == "BUY"):

        last_sell_order = place_order(kite.TRANSACTION_TYPE_SELL)
        logging.info("Place an Sell order {}".format(datetime.now()))

    elif (last_sell_order[0]['trigger_price'] - 54 >= ltp_price and (last_sell_order[0]['transaction_type'] == "BUY")) \
            or (ltp_price > data_manager['close'].iloc[-1] and (last_buy_order[0]['transaction_type'] == "BUY")):

        last_exit_order = exit_order(last_sell_order[0]['order_id'])
        last_sell_order[0]['transaction_type'] = "BUY"
        logging.info("Exit SELL order".format(datetime.now()))
    else:
        logging.info("Wait order is still on")

    return last_sell_order


def place_order(transaction_type):
    order_data = get_historical_data()
    if transaction_type == kite.TRANSACTION_TYPE_BUY:
        trigger_price = int(order_data['close'].iloc[-1]) - 30
    else:
        trigger_price = int(order_data['close'].iloc[-1]) + 30
    order_id = kite.place_order(tradingsymbol='CRUDEOILM19MAYFUT', exchange='MCX', quantity=1,
                                trigger_price=trigger_price,
                                transaction_type=transaction_type,
                                variety=kite.VARIETY_CO, order_type="MARKET", product="MIS", validity=kite.VALIDITY_DAY)
    order_history = kite.order_history(order_id)
    order_json = json.dumps(order_history, indent=4, sort_keys=True, default=str)
    order_object = json.loads(order_json)
    return order_object


def exit_order(order_id):
    order_exit = kite.exit_order(variety=kite.VARIETY_CO, order_id=order_id, parent_order_id=None)
    return order_exit


def last_ltp():
    order_ltp = kite.ltp('MCX:CRUDEOILM19MAYFUT')
    return order_ltp


def start():
    records = get_historical_data()
    over_strategy(records)
    under_strategy(records)


def run_schedule():
    if const.start_time < datetime.now().timestamp() < const.stop_time:
        schedule.every().minute.do(start)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # logging.info (app.url_map)
    logging.info('root dir : {}'.format(os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))))
    logging.info(os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))))
    logging.info("PYTHON PATH : {}".format(getenv("PYTHONPATH")))
    logging.info("Environment: {}".format(getenv('python_env', 'local')))
    logging.info("SYSTEM PATH : {}".format(sys.path))
    th = Thread(target=run_schedule)
    th.start()
    port = int(os.getenv("VCAP_APP_PORT") or 5000)
    app.run(host=const.IP, port=port, debug=False, use_reloader=False)
