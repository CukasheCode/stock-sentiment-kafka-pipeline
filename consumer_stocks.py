from kafka import KafkaConsumer
import json, sqlite3, threading

conn = sqlite3.connect('stocks_data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        symbol TEXT,
        price REAL,
        change_pct REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS news_sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        symbol TEXT,
        score REAL,
        mood TEXT,
        articles_analyzed INTEGER
    )
''')
conn.commit()

def consume_stocks():
    consumer = KafkaConsumer(
        'stock-topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print("Stock consumer started...")
    for message in consumer:
        data = message.value
        for symbol, info in data["stocks"].items():
            cursor.execute('''
                INSERT INTO stock_prices (timestamp, symbol, price, change_pct)
                VALUES (?, ?, ?, ?)
            ''', (data["timestamp"], symbol, info["price"], info["change"]))
            conn.commit()
            print(f"Saved stock: {symbol} ${info['price']}")

def consume_news():
    consumer = KafkaConsumer(
        'news-topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print("News sentiment consumer started...")
    for message in consumer:
        data = message.value
        for symbol, info in data["sentiments"].items():
            cursor.execute('''
                INSERT INTO news_sentiment (timestamp, symbol, score, mood, articles_analyzed)
                VALUES (?, ?, ?, ?, ?)
            ''', (data["timestamp"], symbol, info["score"], info["mood"], info["articles_analyzed"]))
            conn.commit()
            print(f"Saved sentiment: {symbol} {info['mood']}")

t1 = threading.Thread(target=consume_stocks)
t2 = threading.Thread(target=consume_news)
t1.start()
t2.start()
t1.join()
t2.join()
