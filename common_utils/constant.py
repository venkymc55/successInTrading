import os
import configparser
import datetime as delta
from datetime import datetime

parser = configparser.RawConfigParser()
parser.read(os.path.join(os.getcwd(), 'common_utils', 'config.cfg'))

IP = parser.get('network', 'IP_ADDR')
API_KEY = parser.get('security', 'API_KEY')
API_SECRET = parser.get('security', 'API_SECRET')
STOP_RUN = parser.get('running', 'STOP_RUN')

from_date = str(datetime.date(datetime.now() - delta.timedelta(days=3))) + " 21:00:00"
to_date = str(datetime.date(datetime.now())) + " 23:00:00"
interval = "5minute"

time_stamp_9am = str(datetime.date(datetime.now())) + " 09:05:00"
dt_obj = datetime.strptime(time_stamp_9am, '%Y-%m-%d %H:%M:%S')
start_time = dt_obj.timestamp()

time_stamp_11pm = str(datetime.date(datetime.now())) + " 22:55:00"
dt_obj = datetime.strptime(time_stamp_11pm, '%Y-%m-%d %H:%M:%S')
stop_time = dt_obj.timestamp()

null = 0
last_buy_order = [{
    "average_price": 0,
    "cancelled_quantity": 0,
    "disclosed_quantity": 0,
    "exchange": "MCX",
    "exchange_order_id": null,
    "exchange_timestamp": null,
    "exchange_update_timestamp": null,
    "filled_quantity": 0,
    "guid": "10871X9j11LeE4UuRR",
    "instrument_token": 54426119,
    "market_protection": 0,
    "order_id": "190325001179793",
    "order_timestamp": "2019-03-25 11:40:04",
    "order_type": "MARKET",
    "parent_order_id": null,
    "pending_quantity": 1,
    "placed_by": "ZQ5720",
    "price": 0,
    "product": "CO",
    "quantity": 1,
    "status": "PUT ORDER REQ RECEIVED",
    "status_message": null,
    "tag": null,
    "tradingsymbol": "CRUDEOILM19APRFUT",
    "transaction_type": "SELL",
    "trigger_price": 4107,
    "validity": "DAY",
    "variety": "co"
}]
last_sell_order = [{
    "average_price": 0,
    "cancelled_quantity": 0,
    "disclosed_quantity": 0,
    "exchange": "MCX",
    "exchange_order_id": null,
    "exchange_timestamp": null,
    "exchange_update_timestamp": null,
    "filled_quantity": 0,
    "guid": "10871X9j11LeE4UuRR",
    "instrument_token": 54426119,
    "market_protection": 0,
    "order_id": "190325001179793",
    "order_timestamp": "2019-03-25 11:40:04",
    "order_type": "MARKET",
    "parent_order_id": null,
    "pending_quantity": 1,
    "placed_by": "ZQ5720",
    "price": 0,
    "product": "CO",
    "quantity": 1,
    "status": "PUT ORDER REQ RECEIVED",
    "status_message": null,
    "tag": null,
    "tradingsymbol": "CRUDEOILM19APRFUT",
    "transaction_type": "BUY",
    "trigger_price": 4107,
    "validity": "DAY",
    "variety": "co"
}]