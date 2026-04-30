from kafka import KafkaProducer
import yfinance as yf
import json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

STOCKS = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT']

print("Stock producer started...")

while True:
    try:
        message = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "stocks": {}}

        for symbol in STOCKS:
            ticker = yf.Ticker(symbol)
            data = ticker.fast_info
            message["stocks"][symbol] = {
                "price": round(data.last_price, 2),
                "change": round(((data.last_price - data.previous_close) / data.previous_close) * 100, 2)
            }
            print(f"{symbol}: ${data.last_price:.2f}")

        producer.send('stock-topic', message)
        print(f"Sent stock data at {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(60)
