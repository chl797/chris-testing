import requests
import datetime
from openai import OpenAI

# --- YOUR API KEYS ---
NEWSAPI_KEY = ""
OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)

NEWS_QUERY = "finance OR Federal Reserve OR inflation OR stock market"
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

# --- Step 1: Fetch Financial News ---
def fetch_financial_news():
    url = f"https://newsapi.org/v2/everything?q={NEWS_QUERY}&from={TODAY}&language=en&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [
        {"title": a["title"], "url": a["url"], "content": a.get("description", "")}
        for a in articles[:10]
    ]

# --- Step 2: Summarize with GPT ---
def summarize_articles(articles):
    content_text = "".join(f"- {a['title']}: {a['content']}\n" for a in articles)
    prompt = f"""
You are a financial news assistant. Summarize the following U.S. finance news headlines into a clear daily digest, grouped by themes like Federal Reserve, Stock Market, Inflation, Jobs, or Regulation. Keep it concise and professional.

{content_text}

Output format:
# U.S. Finance Daily Digest – {TODAY}
<Summary grouped by theme>
"""  # <-- Make sure this triple quote is here!
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a financial journalist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

# --- Step 3: Generate and Save Digest ---
def generate_digest():
    print("Fetching news...")
    articles = fetch_financial_news()
    print("Summarizing news...")
    digest = summarize_articles(articles)
    print("\n--- DAILY DIGEST ---\n")
    print(digest)
    with open(f"daily_digest_{TODAY}.md", "w") as f:
        f.write(digest)
    return digest

if __name__ == "__main__":
    generate_digest()
