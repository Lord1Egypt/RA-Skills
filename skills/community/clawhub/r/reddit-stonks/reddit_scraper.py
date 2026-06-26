import re
import time
from collections import Counter
from datetime import datetime, timedelta

import requests

SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "pennystocks",
    "StockMarket",
    "thetagang",
    "dividends",
]

COMMON_FALSE_TICKERS = {
    "A", "I", "DD", "CEO", "CFO", "CTA", "ETF", "AI", "IPO", "YOLO",
    "IT", "EV", "FDA", "USA", "USD", "GDP", "CPI", "FOMC", "EPS",
    "IMO", "FYI", "TLDR", "PSA", "EDIT", "LMAO", "ROFL", "FUD",
    "HODL", "ATH", "BTFD", "DTF", "ELI5", "FOMO", "GAINS", "LOSS",
    "OTM", "ITM", "PM", "AH", "EOD", "ETF", "REIT", "SPAC", "BOGO",
    "GOAT", "OG", "OP", "TOS", "NYSE", "NASDAQ", "SEC", "FINRA",
    "IRA", "ROTH", "DTCC", "NSCC", "OCC", "CBOE", "CME", "ICE",
    "IS", "BE", "ARE", "AM", "PM", "OR", "ON", "IN", "AT", "TO",
    "FOR", "BY", "MY", "SO", "DO", "GO", "NO", "WE", "HE", "ME",
    "ALL", "ANY", "BIG", "NEW", "OLD", "LOW", "HIGH", "TOP",
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
    "SEP", "OCT", "NOV", "DEC", "MON", "TUE", "WED", "THU",
    "FRI", "SAT", "SUN", "RH", "TD", "IB", "TDA", "IRS",
}

USER_AGENT = "RedditStonks/1.0 (analysis bot)"


def _is_likely_ticker(word: str) -> bool:
    return (
        2 <= len(word) <= 5
        and word.isalpha()
        and word.isupper()
        and word not in COMMON_FALSE_TICKERS
    )


def extract_tickers(text: str) -> list[str]:
    tickers: list[str] = []

    dollar_matches = re.findall(r"\$([A-Z]{1,5})\b", text)
    tickers.extend(dollar_matches)

    words = re.findall(r"\b[A-Z]{2,5}\b", text)
    for w in words:
        if w in dollar_matches:
            continue
        if _is_likely_ticker(w):
            tickers.append(w)

    return tickers


def _parse_utc(ts: float) -> datetime:
    return datetime.utcfromtimestamp(ts)


def scrape_subreddit(subreddit: str, limit: int = 50) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": USER_AGENT}
    params: dict = {"limit": limit, "t": "week"}

    posts: list[dict] = []
    after: str | None = None
    fetched = 0

    while fetched < limit:
        if after:
            params["after"] = after
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"  [!] r/{subreddit} returned HTTP {resp.status_code}")
            break

        data = resp.json()
        children = data.get("data", {}).get("children", [])
        if not children:
            break

        for child in children:
            post_data = child["data"]
            created = _parse_utc(post_data["created_utc"])
            posts.append({
                "subreddit": subreddit,
                "title": post_data.get("title", ""),
                "selftext": post_data.get("selftext", ""),
                "score": post_data.get("score", 0),
                "num_comments": post_data.get("num_comments", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "created": created.isoformat(),
                "url": f"https://reddit.com{post_data.get('permalink', '')}",
            })
            fetched += 1
            if fetched >= limit:
                break

        after = data.get("data", {}).get("after")
        if not after:
            break
        time.sleep(1.0)

    return posts


def scrape_all(limit_per_sub: int = 50) -> dict:
    print(f"\nScraping {len(SUBREDDITS)} subreddits "
          f"(~{limit_per_sub} posts each)...\n")

    all_posts: list[dict] = []
    ticker_counter: Counter = Counter()
    ticker_posts: dict[str, list[dict]] = {}

    for sub in SUBREDDITS:
        print(f"  r/{sub} ...", end=" ", flush=True)
        posts = scrape_subreddit(sub, limit=limit_per_sub)
        print(f"{len(posts)} posts")

        for post in posts:
            all_posts.append(post)
            full_text = f"{post['title']} {post['selftext']}"
            tickers = extract_tickers(full_text)
            for t in set(tickers):
                ticker_counter[t] += 1
                if t not in ticker_posts:
                    ticker_posts[t] = []
                ticker_posts[t].append(post)

        time.sleep(2.0)

    print(f"\nTotal posts scraped: {len(all_posts)}")
    print(f"Unique tickers found: {len(ticker_counter)}")

    ranked = ticker_counter.most_common(30)
    print("\nTop mentioned tickers:")
    for ticker, count in ranked[:15]:
        print(f"  ${ticker}: {count} mentions")

    return {
        "posts": all_posts,
        "ticker_counts": dict(ranked),
        "ticker_posts": ticker_posts,
    }
