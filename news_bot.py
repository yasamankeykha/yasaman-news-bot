
import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

RSS_FEEDS = [
    "https://www.mehrnews.com/rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
]

def get_news():
    news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            title = entry.get("title", "")
            link = entry.get("link", "")

            if title and link:
                news.append(f"• {title}\n{link}")

    return news[:10]

def send_news():
    news = get_news()

    if not news:
        message = "امروز خبری دریافت نشد."
    else:
        message = "📰 اخبار مهم امروز\n\n" + "\n\n".join(news)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": message},
        timeout=30
    )
    response.raise_for_status()

if __name__ == "__main__":
    send_news()

