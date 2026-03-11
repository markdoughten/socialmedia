import feedparser

def get_topics():
    topics = [
        {
            "name": "KDnuggets",
            "category": "data_science",
            "rss": "https://feeds.feedburner.com/kdnuggets-data-mining-analytics",
            "keywords": ["analytics", "machine learning", "data science", "ai"]
        },
        {
            "name": "NVIDIA News",
            "category": "ai_infrastructure",
            "rss": "https://nvidianews.nvidia.com/releases.xml",
            "keywords": ["ai", "gpu", "infrastructure", "data center"]
        },
        {
            "name": "Supply Chain 24/7",
            "category": "supply_chain",
            "rss": "https://www.supplychain247.com/rss",
            "keywords": ["logistics", "supply chain", "inventory", "operations"]
        }
    ]
    return topics

def check_blocked_words(entry):
    
    text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    blocked_words = ["sponsored", "advertisement", "partner", "paid post", "promotion"]

    return any(word in text for word in blocked_words)

def fetch_articles(limit_per_feed=5):
    
    articles = []

    for topic in get_topics():
        feed = feedparser.parse(topic["rss"])
        articles_per_feed = []

        for entry in feed.entries:

            # Skip blocked content
            if check_blocked_words(entry):
                continue

            articles_per_feed.append({
                "source": topic["name"],
                "category": topic["category"],
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
            })

            if len(articles_per_feed) >= limit_per_feed:
                articles.extend(articles_per_feed)
                break

    return articles