# InfluxDB + Grafana Demo

## Overview

InfluxDB と Grafana を利用して BitFlyer と Binance でのビットコイン価格を可視化するデモです。

## Usage

必要なもの

- docker
- docker-compose
- python 3.8
- poetry

やること

1. `.env.example` を参考に `.env` を作成する
2. poetry install
3. poetry run inv setup
4. docker-compose up
5. http://localhost:3000 にアクセス
