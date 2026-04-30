# Real-time Stock + News Sentiment Pipeline

## What this project does
A live data engineering pipeline that streams real stock prices for Apple, Tesla, 
Google, Amazon and Microsoft from Yahoo Finance, analyzes real news headlines 
sentiment using NLP, streams everything through Apache Kafka on AWS EC2, stores 
in SQLite and displays on a live Streamlit dashboard.

## Pipeline Architecture

## Tech Stack
| Tool | Purpose |
|---|---|
| Apache Kafka | Real-time message streaming |
| Python | Producers, consumer, dashboard |
| AWS EC2 | Cloud server (Ubuntu t2.micro free tier) |
| SQLite | Data storage |
| Yahoo Finance API | Free real-time stock prices |
| NewsAPI | Real news headlines |
| TextBlob | NLP sentiment analysis |
| Streamlit | Live web dashboard |

## Features
- Live stock prices updating every 60 seconds
- Real news sentiment — BULLISH / BEARISH / NEUTRAL per stock
- Two Kafka topics running simultaneously
- Threading — one consumer handles two topics at once
- Dark themed professional dashboard
- Complete ETL pipeline

## How to run
1. Start ZooKeeper and Kafka broker
2. Create topics: stock-topic and news-topic
3. Run producer_stock.py
4. Run producer_news.py
5. Run consumer_stocks.py
6. Run dashboard_stocks.py with Streamlit
