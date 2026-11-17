#!/usr/bin/env python3
"""search_anim.py - category-driven GitHub skill search for video-skill-router.

Usage:
    python search_anim.py --category commercial --query "product demo"
    python search_anim.py --category education --query "math animation"
    python search_anim.py --query "lottie web animation"          # auto channel from words
    python search_anim.py --category general --query "..." --json out.json

Category channels (see references/categories.md):
    commercial: motion-design / lottie / remotion / advertising + promo/ad/product templates
    education:  manim / manimgl / data-visualization + math/education templates
    general:    video-editing / ffmpeg / subtitle + editing/video templates

Proxy auto-detection (direct first; injected random ports are usually dead).
Standard library only.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

TOPIC_MAP = {
    "math": ["manim", "manimgl", "3blue1brown"],
    "data": ["data-visualization", "d3", "animation"],
    "motion": ["motion-graphics", "motion-design"],
    "lottie": ["lottie", "lottiefiles"],
    "2d": ["animation2d", "spine", "dragonbones"],
    "3d": ["blender", "blender-scripts", "threejs"],
    "subtitle": ["subtitle-animation", "text-animation"],
    "video": ["ffmpeg", "remotion", "editly"],
    "generic": ["animation", "animation-templates"],
}

CATEGORY_CHANNELS = {
    "commercial": {
        "topics": ["motion-design", "motion-graphics", "lottie", "lottiefiles", "remotion", "advertising"],
        "queries": ["promo video skill", "ad video generator", "product demo animation"],
    },
    "education": {
        "topics": ["manim", "manimgl", "3blue1brown", "data-visualization"],
        "queries": ["manim animation skill", "math animation agent", "data visualization animation"],
    },
    "general": {
        "topics": ["video-editing", "ffmpeg", "subtitle", "video"],
        "queries": ["video editing skill", "ffmpeg automation", "subtitle generator"],
    },
}

PROXY_CANDIDATES = [
    None,
    "http://127.0.0.1:7897",
    os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"),
]


def build_opener():
    last_err = None
    for proxy in PROXY_CANDIDATES:
        if proxy is None:
            handler = urllib.request.ProxyHandler({})
        else:
            handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        opener = urllib.request.build_opener(handler)
        try:
            opener.open("https://api.github.com/rate_limit", timeout=8).read()
            return opener, proxy
        except Exception as exc:  # noqa: BLE001
            last_err = exc
    raise SystemExit("network error: all proxy channels failed: %s" % last_err)


def github_search(opener, query, limit):
    url = (
        "https://api.github.com/search/repositories?q="
        + urllib.parse.quote(query)
        + "&sort=stars&order=desc&per_page=%d" % limit
    )
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with opener.open(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    results = []
    for item in payload.get("items", []):
        results.append(
            {
                "name": item.get("full_name"),
                "url": item.get("html_url"),
                "clone_url": item.get("clone_url"),
                "description": (item.get("description") or "")[:300],
                "stars": item.get("stargazers_count", 0),
                "topics": item.get("topics", []),
                "updated_at": item.get("updated_at", ""),
                "source": "github",
            }
        )
    return results


def expand_topics(query):
    q = query.lower()
    seen = set()
    topics = []
    for key, vals in TOPIC_MAP.items():
        if key in q or any(v.split("-")[0] in q for v in vals):
            for v in vals:
                if v not in seen:
                    seen.add(v)
                    topics.append(v)
    words = [w for w in q.replace("-", " ").split() if len(w) > 2]
    if not topics:
        topics = list(dict.fromkeys(TOPIC_MAP["generic"] + words))
    return topics, words


def run_queries(opener, queries, limit, seen):
    """Run a list of repo-search queries, merge into seen dict."""
    for query in queries:
        try:
            for r in github_search(opener, query, limit):
                seen[r["name"]] = r
        except Exception as exc:  # noqa: BLE001
            print("warn: query '%s' failed: %s" % (query, exc), file=sys.stderr)
            if "rate limit" in str(exc).lower():
                print("rate limited, stopping further queries", file=sys.stderr)
                return False
        time.sleep(2.0)  # GitHub search rate limit: 10 req/min unauthenticated
    return True


def main():
    parser = argparse.ArgumentParser(description="Category-driven GitHub skill search")
    parser.add_argument("--query", required=True, help="user need, any language")
    parser.add_argument("--category", choices=["commercial", "education", "general"],
                        help="video category; picks the channel matrix from categories.md")
    parser.add_argument("--limit", type=int, default=15)
    parser.add_argument("--json", dest="json_out", help="write results to JSON file")
    args = parser.parse_args()

    opener, proxy = build_opener()
    seen = {}
    queries_run = []

    if args.category:
        channel = CATEGORY_CHANNELS[args.category]
        # 1) text queries with "skill" bias to surface skill packs
        queries_run.extend(channel["queries"])
        if not run_queries(opener, channel["queries"], args.limit, seen):
            queries_run = channel["queries"]
        else:
            # 2) topic queries (max 3 to respect rate limit)
            topic_queries = ["topic:%s" % t for t in channel["topics"][:3]]
            queries_run.extend(topic_queries)
            run_queries(opener, topic_queries, args.limit, seen)
        print("channel: category=%s proxy=%s queries=%d hits=%d"
              % (args.category, proxy or "direct", len(queries_run), len(seen)))
    else:
        topics, words = expand_topics(args.query)
        queries = ["topic:%s" % t for t in topics[:4]]
        if words:
            queries.append(" ".join(words[:3]))
        queries_run = queries
        run_queries(opener, queries, args.limit, seen)
        print("channel: auto proxy=%s topics=%s queries=%d hits=%d"
              % (proxy or "direct", topics[:4], len(queries_run), len(seen)))

    results = sorted(seen.values(), key=lambda r: -r["stars"])[: args.limit]
    if args.category:
        for r in results:
            r["category"] = args.category
    for i, r in enumerate(results, 1):
        print("%2d. [%s*] %s\n    %s" % (i, r["stars"], r["name"], r["url"]))
        if r["description"]:
            print("    %s" % r["description"][:120])
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=2)
        print("written: %s" % args.json_out)


if __name__ == "__main__":
    main()


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
