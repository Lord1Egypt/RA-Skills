#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ------------------------
# Local data files. Do not publish generated data/*.json files.
# ------------------------
DATA_DIR = Path("data")
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"
DATA_DIR.mkdir(exist_ok=True)

OPENALEX_BASE = "https://api.openalex.org"
OPENALEX_MAILTO = os.getenv("OPENALEX_MAILTO", "openclaw@example.com")
DEFAULT_LOOKBACK_DAYS = 1
DEFAULT_RESULT_LIMIT = 10

# ------------------------
# Defaults: journals/conferences + research topics
# ------------------------
DEFAULT_JOURNALS = [
    "IEEE Transactions on Medical Imaging",
    "IEEE Transactions on Image Processing",
    "IEEE Transactions on Biomedical Engineering",
    "IEEE Transactions on Neural Systems and Rehabilitation Engineering",
    "NeuroImage",
    "Human Brain Mapping",
    "Medical Image Analysis",
    "Brain Connectivity",
    "Alzheimer's & Dementia",
    "Frontiers in Aging Neuroscience",
]

DEFAULT_TOPICS = [
    "Alzheimer disease",
    "mild cognitive impairment",
    "MCI",
    "dynamic functional connectivity",
    "dynamic functional brain network",
    "brain network",
    "resting-state fMRI",
    "rs-fMRI",
    "graph neural network",
    "graph convolution",
    "graph attention",
    "neurodegenerative disease classification",
]

JOURNAL_ALIASES = {
    "ieee tmi": "IEEE Transactions on Medical Imaging",
    "tmi": "IEEE Transactions on Medical Imaging",
    "ieee tip": "IEEE Transactions on Image Processing",
    "tip": "IEEE Transactions on Image Processing",
    "ieee tbme": "IEEE Transactions on Biomedical Engineering",
    "tbme": "IEEE Transactions on Biomedical Engineering",
    "ieee tnsre": "IEEE Transactions on Neural Systems and Rehabilitation Engineering",
    "tnsre": "IEEE Transactions on Neural Systems and Rehabilitation Engineering",
}

# ------------------------
# JSON helpers
# ------------------------
def load_json(file_path, default=None):
    if default is None:
        default = []
    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def split_csv(value, default):
    if not value:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def today_utc():
    return dt.datetime.now(dt.timezone.utc).date()


def iso_date_days_ago(days):
    return (today_utc() - dt.timedelta(days=max(days, 0))).isoformat()


def abstract_from_inverted_index(index):
    if not index:
        return ""
    positions = []
    for word, locs in index.items():
        for pos in locs:
            positions.append((pos, word))
    positions.sort()
    return " ".join(word for _, word in positions)


def normalize_text(text):
    return (text or "").lower().replace("’", "'")


def normalize_journal(name):
    raw = (name or "").strip()
    return JOURNAL_ALIASES.get(raw.lower(), raw)


def openalex_get(path, params=None, attempts=3):
    params = dict(params or {})
    if OPENALEX_MAILTO:
        params.setdefault("mailto", OPENALEX_MAILTO)
    url = f"{OPENALEX_BASE}{path}?{urllib.parse.urlencode(params)}"

    last_error = None
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": "openclaw-research-paper-push/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            if "unknown url type: https" in str(exc).lower():
                break
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)

    # Some embedded Windows Python builds lack SSL support. Fall back to curl
    # when available so the skill can still query OpenAlex over HTTPS.
    try:
        result = subprocess.run(
            ["curl", "-L", "-sS", "--max-time", "30", "-A", "openclaw-research-paper-push/1.0", url],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        last_error = result.stderr.strip() or f"curl exited with {result.returncode}"
    except Exception as exc:
        last_error = exc

    print(f"OpenAlex 请求失败：{last_error}", file=sys.stderr)
    return None


def work_to_paper(work):
    source = ((work.get("primary_location") or {}).get("source") or {})
    authors = []
    for item in (work.get("authorships") or [])[:6]:
        author_name = (item.get("author") or {}).get("display_name")
        if author_name:
            authors.append(author_name)

    abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
    doi = work.get("doi") or ""
    return {
        "id": work.get("id") or "",
        "title": work.get("title") or "Untitled",
        "abstract": abstract,
        "publication_date": work.get("publication_date") or "",
        "year": work.get("publication_year") or "",
        "venue": source.get("display_name") or "",
        "authors": authors,
        "doi": doi,
        "url": doi or work.get("id") or "",
        "cited_by_count": work.get("cited_by_count") or 0,
    }


def build_queries(topics):
    english_topics = [t for t in topics if t and not any("\u4e00" <= ch <= "\u9fff" for ch in t)]
    if not english_topics:
        english_topics = DEFAULT_TOPICS

    disease_terms = [t for t in english_topics if any(k in t.lower() for k in ["alzheimer", "mci", "mild cognitive", "parkinson", "dementia", "neurodegenerative"])]
    method_terms = [t for t in english_topics if any(k in t.lower() for k in ["dynamic", "connectivity", "brain network", "fmri", "graph", "gnn", "classification"])]

    queries = []
    if disease_terms and method_terms:
        for disease in disease_terms[:4]:
            for method in method_terms[:5]:
                queries.append(f"{disease} {method}")
    queries.append(" ".join(english_topics[:8]))
    queries.append("dynamic functional connectivity Alzheimer graph neural network rs-fMRI")

    deduped = []
    seen = set()
    for q in queries:
        q = " ".join(q.split())
        key = q.lower()
        if q and key not in seen:
            deduped.append(q)
            seen.add(key)
    return deduped[:12]


def paper_matches_journals(paper, journals):
    if not journals:
        return True
    venue = normalize_text(paper.get("venue"))
    if not venue:
        return True  # Keep preprints/conference metadata if topic relevance is strong.
    for journal in journals:
        normalized = normalize_journal(journal)
        j = normalize_text(normalized)
        if j and (j in venue or venue in j):
            return True
    return False


def score_relevance(paper, topics):
    text = normalize_text(" ".join([paper.get("title", ""), paper.get("abstract", ""), paper.get("venue", "")]))
    score = 0
    matched = []
    for topic in topics:
        topic_norm = normalize_text(topic)
        if not topic_norm:
            continue
        if topic_norm in text:
            score += 2 if topic_norm in normalize_text(paper.get("title", "")) else 1
            matched.append(topic)

    # Reward common synonym groups for the default neuroimaging use case.
    groups = [
        ["alzheimer", "mci", "mild cognitive impairment", "dementia", "neurodegenerative"],
        ["dynamic functional", "functional connectivity", "brain network", "connectivity"],
        ["fmri", "rs-fmri", "resting-state"],
        ["graph neural", "gnn", "graph convolution", "graph attention"],
    ]
    for group in groups:
        if any(term in text for term in group):
            score += 1

    return score, matched


# ------------------------
# CLI actions
# ------------------------
def add_subscription(args):
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    existing_ids = [int(s.get("id", 0)) for s in subscriptions if str(s.get("id", "")).isdigit()]
    sub_id = str(max(existing_ids, default=0) + 1)
    subscription = {
        "id": sub_id,
        "to": args.to,
        "journals": split_csv(args.journals, DEFAULT_JOURNALS),
        "topics": split_csv(args.topics, DEFAULT_TOPICS),
        "time": args.time,
        "timezone": args.timezone or "Asia/Shanghai",
        "lookback_days": args.days or DEFAULT_LOOKBACK_DAYS,
        "last_checked": None,
    }
    subscriptions.append(subscription)
    save_json(SUBSCRIPTIONS_FILE, subscriptions)
    print(f"✅ 已创建订阅：{subscription}")
    create_cron_job(subscription)


def list_subscriptions(args):
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    subs = [s for s in subscriptions if not args.to or s.get("to") == args.to]
    if not subs:
        print("📋 当前没有订阅。")
        return
    print("📋 当前订阅列表：")
    for sub in subs:
        print(json.dumps(sub, ensure_ascii=False, indent=2))


def update_subscription(args):
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    for sub in subscriptions:
        if sub.get("id") == args.id:
            if args.time:
                sub["time"] = args.time
            if args.timezone:
                sub["timezone"] = args.timezone
            if args.journals:
                sub["journals"] = split_csv(args.journals, DEFAULT_JOURNALS)
            if args.topics:
                sub["topics"] = split_csv(args.topics, DEFAULT_TOPICS)
            if args.days:
                sub["lookback_days"] = args.days
            save_json(SUBSCRIPTIONS_FILE, subscriptions)
            print(f"✅ 已更新订阅：{sub}")
            if args.time or args.timezone:
                create_cron_job(sub)
            return
    print("⚠️ 未找到指定订阅ID。")


def remove_subscription(args):
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    new_subs = [sub for sub in subscriptions if sub.get("id") != args.id]
    save_json(SUBSCRIPTIONS_FILE, new_subs)
    print(f"✅ 已取消订阅ID：{args.id}")
    remove_cron_job(args.id)


def test_subscription(args):
    subscription = {
        "journals": split_csv(args.journals, DEFAULT_JOURNALS),
        "topics": split_csv(args.topics, DEFAULT_TOPICS),
        "time": args.time,
        "timezone": args.timezone or "Asia/Shanghai",
        "lookback_days": args.days or DEFAULT_LOOKBACK_DAYS,
    }
    papers = fetch_new_papers(subscription, since=args.since, limit=args.limit)
    relevant = filter_relevant_papers(papers, subscription["topics"], subscription["journals"])
    summaries = summarize_papers(relevant[: args.limit])
    print("📤 测试推送内容：")
    if not summaries:
        print("暂无匹配的新论文。")
    for s in summaries:
        print(s)


# ------------------------
# Scheduling
# ------------------------
def create_cron_job(subscription):
    if not subscription.get("time"):
        print("⚠️ 未提供推送时间，跳过 cron 创建。")
        return
    cmd = [
        "openclaw", "cron", "add",
        "--name", f"paper_push_{subscription['id']}",
        "--time", subscription["time"],
        "--timezone", subscription.get("timezone") or "Asia/Shanghai",
        "--script", f"python scripts/manage_papers.py run --id {subscription['id']}",
    ]
    subprocess.run(cmd)
    print(f"⏰ Cron 任务已创建：{subscription['time']} ({subscription.get('timezone') or 'Asia/Shanghai'})")


def remove_cron_job(sub_id):
    cmd = ["openclaw", "cron", "remove", "--name", f"paper_push_{sub_id}"]
    subprocess.run(cmd)
    print(f"🗑 Cron 任务已删除：{sub_id}")


def run_subscription(args):
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    sub = next((s for s in subscriptions if s.get("id") == args.id), None)
    if not sub:
        print("⚠️ 未找到订阅")
        return

    since = args.since or sub.get("last_checked")
    papers = fetch_new_papers(sub, since=since, limit=args.limit)
    relevant = filter_relevant_papers(papers, sub.get("topics") or DEFAULT_TOPICS, sub.get("journals") or [])
    summaries = summarize_papers(relevant[: args.limit])
    push_to_user(summaries, sub)

    sub["last_checked"] = today_utc().isoformat()
    save_json(SUBSCRIPTIONS_FILE, subscriptions)


# ------------------------
# OpenAlex paper fetching and processing
# ------------------------
def fetch_new_papers(sub, since=None, limit=DEFAULT_RESULT_LIMIT):
    """Fetch recent works from OpenAlex according to subscription topics."""
    topics = sub.get("topics") or DEFAULT_TOPICS
    journals = [normalize_journal(j) for j in (sub.get("journals") or [])]
    lookback_days = int(sub.get("lookback_days") or DEFAULT_LOOKBACK_DAYS)
    from_date = since or iso_date_days_ago(lookback_days)

    works = []
    seen = set()
    for query in build_queries(topics):
        params = {
            "search": query,
            "filter": f"from_publication_date:{from_date}",
            "sort": "publication_date:desc",
            "per-page": str(max(limit * 3, 25)),
        }
        data = openalex_get("/works", params)
        if not data:
            continue
        for work in data.get("results", []):
            paper = work_to_paper(work)
            key = paper.get("doi") or paper.get("id") or paper.get("title", "").lower()
            if not key or key in seen:
                continue
            seen.add(key)
            works.append(paper)
        if len(works) >= limit * 5:
            break

    # Also search specific journal names with topic terms when a user provided a narrow source list.
    for journal in journals[:8]:
        query = f"{journal} {' '.join(topics[:4])}"
        params = {
            "search": query,
            "filter": f"from_publication_date:{from_date}",
            "sort": "publication_date:desc",
            "per-page": str(max(limit, 10)),
        }
        data = openalex_get("/works", params)
        if not data:
            continue
        for work in data.get("results", []):
            paper = work_to_paper(work)
            key = paper.get("doi") or paper.get("id") or paper.get("title", "").lower()
            if not key or key in seen:
                continue
            seen.add(key)
            works.append(paper)

    return works


def filter_relevant_papers(papers, topics, journals=None):
    relevant = []
    for paper in papers:
        score, matched = score_relevance(paper, topics)
        if score <= 0:
            continue
        if journals and not paper_matches_journals(paper, journals) and score < 3:
            continue
        paper = dict(paper)
        paper["relevance_score"] = score
        paper["matched_topics"] = matched[:6]
        relevant.append(paper)

    relevant.sort(key=lambda p: (p.get("publication_date", ""), p.get("relevance_score", 0), p.get("cited_by_count", 0)), reverse=True)
    return relevant


def summarize_papers(papers):
    summaries = []
    for idx, p in enumerate(papers, start=1):
        authors = ", ".join(p.get("authors") or []) or "作者信息暂无"
        matched = "、".join(p.get("matched_topics") or []) or "主题关键词"
        abstract = p.get("abstract") or "OpenAlex 暂无摘要。"
        if len(abstract) > 260:
            abstract = abstract[:260].rstrip() + "..."
        direct = "直接相关" if p.get("relevance_score", 0) >= 4 else "相邻相关"
        summary = (
            f"{idx}. {p.get('title')}\n"
            f"作者/年份/来源：{authors}；{p.get('year') or '年份未知'}；{p.get('venue') or '来源未知'}\n"
            f"日期：{p.get('publication_date') or '未知'}；引用：{p.get('cited_by_count', 0)}\n"
            f"匹配：{matched}；相关性：{direct}\n"
            f"要点：{abstract}\n"
            f"链接：{p.get('url') or p.get('id') or '暂无'}\n"
        )
        summaries.append(summary)
    return summaries


def push_to_user(summaries, sub):
    print("📤 论文订阅更新：")
    if not summaries:
        print("今天暂未发现匹配订阅主题的新论文。")
        return
    for s in summaries:
        print(s)


# ------------------------
# Main
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="Manage scheduled OpenAlex paper subscriptions")
    parser.add_argument("action", choices=["add", "list", "update", "remove", "test", "run"])
    parser.add_argument("--id", help="Subscription ID")
    parser.add_argument("--to", help="Recipient/channel ID; stored only in local data")
    parser.add_argument("--journals", help="Comma-separated journals/conferences")
    parser.add_argument("--topics", help="Comma-separated research keywords")
    parser.add_argument("--time", help="Daily push time, e.g. 09:00")
    parser.add_argument("--timezone", help="Timezone, e.g. Asia/Shanghai")
    parser.add_argument("--days", type=int, help="Lookback days for new papers")
    parser.add_argument("--since", help="Override from-publication-date, YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=DEFAULT_RESULT_LIMIT, help="Maximum papers to summarize")
    args = parser.parse_args()

    if args.action == "add":
        add_subscription(args)
    elif args.action == "list":
        list_subscriptions(args)
    elif args.action == "update":
        update_subscription(args)
    elif args.action == "remove":
        remove_subscription(args)
    elif args.action == "test":
        test_subscription(args)
    elif args.action == "run":
        if not args.id:
            print("run 需要 --id", file=sys.stderr)
            raise SystemExit(2)
        run_subscription(args)


if __name__ == "__main__":
    main()
