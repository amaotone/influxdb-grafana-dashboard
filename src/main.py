import asyncio
import os
import time

import requests_async as requests
from influxdb_client import InfluxDBClient

INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
NAME = "price-checker"


async def get_bitflyer(symbol):
    url = "https://api.bitflyer.com/v1/ticker"
    resp = await requests.get(url, params={"product_code": symbol})
    data = resp.json()
    print(data, flush=True)
    writer.write(
        bucket=INFLUXDB_BUCKET,
        org=INFLUXDB_ORG,
        record={
            "measurement": NAME,
            "tags": {"exchange": "bitflyer", "symbol": symbol},
            "fields": {
                "price": float(data["ltp"]),
                "best_bid": float(data["best_bid"]),
                "best_ask": float(data["best_ask"]),
                "best_bid_size": float(data["best_bid_size"]),
                "best_ask_size": float(data["best_ask_size"]),
                "total_bid_depth": float(data["total_bid_depth"]),
                "total_ask_depth": float(data["total_ask_depth"]),
            },
        },
    )


async def get_binance(symbol):
    url = "https://api.binance.com/api/v3/trades"
    resp = await requests.get(url, params={"symbol": symbol, "limit": 1})
    data = resp.json()[0]
    print(data, flush=True)
    writer.write(
        bucket=INFLUXDB_BUCKET,
        org=INFLUXDB_ORG,
        record={
            "measurement": NAME,
            "tags": {"exchange": "binance", "symbol": symbol},
            "fields": {"price": float(data["price"])},
        },
    )


async def main():
    await asyncio.gather(
        get_bitflyer("FX_BTC_JPY"),
        get_bitflyer("BTC_JPY"),
        get_binance("BTCUSDT"),
    )


if __name__ == "__main__":
    client = InfluxDBClient(
        url="http://influx:8086", token=INFLUXDB_TOKEN, org=INFLUXDB_ORG
    )
    writer = client.write_api()
    while True:
        asyncio.run(main())
        time.sleep(10)
