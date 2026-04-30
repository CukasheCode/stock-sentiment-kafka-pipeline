import streamlit as st
import sqlite3, pandas as pd, time

st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border: 1px solid #2d3250;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 4px 0;
    }
    .metric-label { color: #8b92a5; font-size: 12px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { color: #ffffff; font-size: 28px; font-weight: 700; }
    .bullish { color: #00d4aa; font-size: 14px; font-weight: 600; }
    .bearish { color: #ff4b6e; font-size: 14px; font-weight: 600; }
    .neutral { color: #ffa500; font-size: 14px; font-weight: 600; }
    .up { color: #00d4aa; font-size: 13px; }
    .down { color: #ff4b6e; font-size: 13px; }
    .section-title { color: #ffffff; font-size: 18px; font-weight: 600; margin: 20px 0 10px 0; padding-bottom: 8px; border-bottom: 1px solid #2d3250; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Live Stock + News Sentiment Dashboard")
st.markdown('<p style="color:#8b92a5;font-size:14px;margin-top:-16px">Real-time stocks from Yahoo Finance + News sentiment via Kafka → SQLite</p>', unsafe_allow_html=True)

placeholder = st.empty()

STOCKS = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT']

while True:
    conn = sqlite3.connect('stocks_data.db')
    prices_df = pd.read_sql("SELECT * FROM stock_prices ORDER BY id DESC LIMIT 500", conn)
    sentiment_df = pd.read_sql("SELECT * FROM news_sentiment ORDER BY id DESC LIMIT 100", conn)
    conn.close()

    with placeholder.container():
        if prices_df.empty:
            st.warning("Waiting for data...")
        else:
            st.markdown('<div class="section-title">Live Stock Prices + News Sentiment</div>', unsafe_allow_html=True)
            cols = st.columns(5)

            for i, symbol in enumerate(STOCKS):
                stock_data = prices_df[prices_df['symbol'] == symbol]
                sentiment_data = sentiment_df[sentiment_df['symbol'] == symbol]

                if not stock_data.empty:
                    price = stock_data['price'].iloc[0]
                    change = stock_data['change_pct'].iloc[0]
                    mood = sentiment_data['mood'].iloc[0] if not sentiment_data.empty else "N/A"

                    change_class = "up" if change > 0 else "down"
                    arrow = "▲" if change > 0 else "▼"
                    mood_class = mood.lower() if mood in ["BULLISH", "BEARISH", "NEUTRAL"] else "neutral"

                    with cols[i]:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{symbol}</div>
                            <div class="metric-value">${price:,.2f}</div>
                            <div class="{change_class}">{arrow} {change:+.2f}%</div>
                            <div class="{mood_class}">News: {mood}</div>
                        </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-title">Price History</div>', unsafe_allow_html=True)
            if not prices_df.empty:
                pivot_df = prices_df.pivot_table(
                    index='timestamp', columns='symbol', values='price'
                ).ffill().iloc[::-1]
                st.line_chart(pivot_df)

            st.markdown('<div class="section-title">News Sentiment Scores</div>', unsafe_allow_html=True)
            if not sentiment_df.empty:
                latest_sentiment = sentiment_df.groupby('symbol').first()['score']
                st.bar_chart(latest_sentiment)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="section-title">Stock Data</div>', unsafe_allow_html=True)
                st.dataframe(prices_df.head(20), use_container_width=True)
            with col2:
                st.markdown('<div class="section-title">News Sentiment Data</div>', unsafe_allow_html=True)
                st.dataframe(sentiment_df.head(20), use_container_width=True)

    time.sleep(60)
