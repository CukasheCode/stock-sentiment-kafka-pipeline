from kafka import KafkaProducer
from newsapi import NewsApiClient
from textblob import TextBlob
import json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

newsapi = NewsApiClient(api_key='9fd1df343901413a8855777d70db3668')

STOCKS = ['Apple', 'Tesla', 'Google', 'Amazon', 'Microsoft']
SYMBOLS = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT']

print("News sentiment producer started...")

while True:
    try:
        sentiments = {}

        for stock, symbol in zip(STOCKS, SYMBOLS):
            headlines = newsapi.get_everything(
                q=stock,
                language='en',
                sort_by='publishedAt',
                page_size=10
            )

            scores = []
            for article in headlines['articles']:
                analysis = TextBlob(article['title'])
                scores.append(analysis.sentiment.polarity)

            avg_score = round(sum(scores) / len(scores), 3) if scores else 0

            if avg_score > 0.1:
                mood = "BULLISH"
            elif avg_score < -0.1:
                mood = "BEARISH"
            else:
                mood = "NEUTRAL"

            sentiments[symbol] = {
                "score": avg_score,
                "mood": mood,
                "articles_analyzed": len(scores)
            }
            print(f"{symbol}: {mood} ({avg_score})")

        message = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "sentiments": sentiments
        }

        producer.send('news-topic', message)
        print(f"Sent sentiment data at {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(300)
