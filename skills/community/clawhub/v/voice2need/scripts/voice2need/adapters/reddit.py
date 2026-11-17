"""Reddit discovery and thread extraction, without implicit provider fallback.

Input/output schema checked 2026-09-15:
https://apify.com/fatihtahta/reddit-scraper-search-fast/input-schema
https://apify.com/fatihtahta/reddit-scraper-search-fast/output-schema
"""

import re
from collections import Counter
from urllib.parse import urlsplit, urlunsplit

from voice2need.records import in_window, make_record
from voice2need.runtime import SourceError
from .apify import positive_int, run_actor

ACTOR = "fatihtahta/reddit-scraper-search-fast"
INPUT_KEYS = {"queries", "sort", "timeframe", "subredditName", "subredditKeywords",
              "subredditSort", "subredditTimeframe", "urls", "scrapeComments", "maxComments",
              "dateFrom", "dateTo", "commentDateFrom", "commentDateTo", "forceSortNewForTimeFilteredRuns",
              "includeNsfw", "strictSearch", "strictTokenFilter", "maxPosts", "maximize_coverage",
              "sentiment_analysis", "content_analysis"}


def _url(value):
    value = str(value or "")
    if value.startswith("/"):
        value = "https://www.reddit.com" + value
    parts = urlsplit(value)
    if parts.scheme not in {"https", "http"} or parts.hostname not in {"reddit.com", "www.reddit.com", "old.reddit.com"} or parts.username or parts.password:
        return None
    return urlunsplit(("https", "www.reddit.com", parts.path, "", ""))


def actor_input(job):
    """Build only documented fields; accidental expansion/delivery is forbidden."""
    mode = job.get("mode", "discovery")
    if mode not in {"discovery", "threads"}:
        raise SourceError("invalid-input", "Reddit mode must be discovery or threads")
    value = job.get("actor_input", {})
    if not isinstance(value, dict) or set(value) - INPUT_KEYS:
        raise SourceError("invalid-input", "Reddit actor_input contains unsupported fields")
    value = {key: val for key, val in value.items() if val not in (None, "", [])}
    if job.get("subreddit"):
        if not isinstance(job["subreddit"], str):
            raise SourceError("invalid-input", "subreddit must be a string")
        value["subredditName"] = job["subreddit"].removeprefix("r/")
    if value.get("subredditName") and (not isinstance(value["subredditName"], str) or not re.fullmatch(r"[A-Za-z0-9_]{2,30}", value["subredditName"])):
        raise SourceError("invalid-input", "Invalid subreddit name")
    if job.get("query"):
        value["subredditKeywords" if value.get("subredditName") else "queries"] = [job["query"]]
    if job.get("urls"):
        value["urls"] = job["urls"]
    for field in ("queries", "subredditKeywords", "urls"):
        if field in value and (not isinstance(value[field], list) or not value[field] or any(not isinstance(v, str) or not v.strip() for v in value[field])):
            raise SourceError("invalid-input", f"{field} must be a nonempty string array")
    if value.get("subredditName") and value.get("queries"):
        value["subredditKeywords"] = list(dict.fromkeys(value.get("subredditKeywords", []) + value.pop("queries")))
    for field in ("sort", "subredditSort"):
        if field in value and value[field] not in {"relevance", "hot", "top", "new", "comments"}:
            raise SourceError("invalid-input", f"Unsupported {field}")
    for field in ("timeframe", "subredditTimeframe"):
        if field in value and value[field] not in {"all", "year", "month", "week", "day", "hour"}:
            raise SourceError("invalid-input", f"Unsupported {field}")
    for field in ("scrapeComments", "forceSortNewForTimeFilteredRuns", "includeNsfw", "strictSearch", "strictTokenFilter", "maximize_coverage", "sentiment_analysis", "content_analysis"):
        if field in value and not isinstance(value[field], bool):
            raise SourceError("invalid-input", f"{field} must be a boolean")
    if mode == "threads":
        if not value.get("urls"):
            raise SourceError("invalid-input", "Reddit threads requires urls")
        if any(not _url(url) or not re.search(r"/r/[^/]+/comments/[a-z0-9]+(?:/|$)", _url(url)) for url in value["urls"]):
            raise SourceError("invalid-input", "threads only accepts exact Reddit discussion URLs")
        value["urls"] = [_url(url) for url in value["urls"]]
        value.pop("queries", None)
        value.pop("subredditKeywords", None)
        value.pop("subredditName", None)
    elif value.get("urls"):
        raise SourceError("invalid-input", "Use threads mode for direct discussion URLs")
    elif not value.get("subredditName") and not job.get("allow_broad_search", False):
        raise SourceError("invalid-input", "Reddit discovery requires subreddit or explicit allow_broad_search")
    if not any(value.get(key) for key in ("queries", "subredditName", "urls")):
        raise SourceError("invalid-input", "Reddit requires a search or URL target")
    if value.get("maximize_coverage") or value.get("sentiment_analysis") or value.get("content_analysis"):
        raise SourceError("invalid-input", "Automatic scope expansion and provider analysis are not supported")
    value.update(maximize_coverage=False, sentiment_analysis=False, content_analysis=False)
    value["scrapeComments"] = mode == "threads"
    value["maxPosts"] = positive_int(job.get("max_posts", value.get("maxPosts", 100 if mode == "discovery" else 1)), "max_posts", 10000)
    value["maxComments"] = positive_int(job.get("max_comments", value.get("maxComments", 5000)), "max_comments", 50000)
    if job.get("start"):
        value["dateFrom" if mode == "discovery" else "commentDateFrom"] = job["start"]
    if job.get("end"):
        value["dateTo" if mode == "discovery" else "commentDateTo"] = job["end"]
    return value


def _fullname(value, prefix):
    value = str(value or "")
    if re.fullmatch(r"t[13]_[a-z0-9]+", value):
        return value
    return prefix + value if re.fullmatch(r"[a-z0-9]+", value) else None


def _record(item, raw, job):
    kind = item.get("kind")
    if kind not in {"post", "comment"}:
        raise SourceError("schema-drift", "Reddit record kind is missing or unknown")
    native_id = _fullname(item.get("id"), "t3_" if kind == "post" else "t1_")
    if not native_id or not native_id.startswith("t3_" if kind == "post" else "t1_"):
        raise SourceError("schema-drift", "Reddit record lacks a correctly typed ID")
    url = _url(item.get("permalink") or item.get("url") or item.get("canonical_url"))
    if not url:
        raise SourceError("schema-drift", "Reddit record lacks a valid permalink")
    post_id = native_id if kind == "post" else _fullname(item.get("postId") or item.get("link_id"), "t3_")
    if not post_id or not post_id.startswith("t3_"):
        raise SourceError("schema-drift", "Reddit comment lacks a parent post ID")
    parent = item.get("parentId") or item.get("parent_id")
    parent = parent if isinstance(parent, str) and re.fullmatch(r"t[13]_[a-z0-9]+", parent) else None
    published = item.get("created_utc") or item.get("createdAt")
    context_only = not in_window(published, job.get("start"), job.get("end"))
    author = item.get("author")
    if isinstance(author, str) and author.strip().lower() in {"[deleted]", "[removed]", ""}:
        author = None
    return make_record("reddit", native_id, kind, item.get("body") or item.get("selftext") or "",
                       author, published, url, post_id, parent_id=parent,
                       title=item.get("title") or "", raw=[raw],
                       metadata={"job_id": job["id"], "subreddit": item.get("subreddit"),
                                 "context_only": context_only, "in_window": not context_only,
                                 "window": {"start": job.get("start"), "end": job.get("end")},
                                 "num_comments": item.get("num_comments"),
                                 "score": item.get("score"), "depth": item.get("depth"),
                                 "deleted_or_removed": (item.get("body") or "") in {"[deleted]", "[removed]"}})


def collect(ctx, job):
    value = actor_input(job)
    seen = {}

    def save_page(items, refs):
        records = [_record(item, raw, job) for item, raw in zip(items, refs)]
        ctx.add_records(records)
        seen.update((record["native_id"], record) for record in records)

    _, _, info = run_actor(ctx, ACTOR, value, max_charge_usd=job.get("max_charge_usd", 1),
                          max_polls=job.get("max_polls", 30), poll_seconds=job.get("poll_seconds", 2),
                          max_dataset_pages=job.get("max_pages", 100), max_items=job.get("max_items", 10000),
                          page_size=job.get("page_size", 1000), on_page=save_page)
    gaps = list(info["gaps"])
    comments = Counter(row["conversation_id"] for row in seen.values() if row["kind"] == "comment")
    missing = sorted({row["parent_id"] for row in seen.values() if row["parent_id"] and row["parent_id"] not in seen})
    unknown_parents = [row["native_id"] for row in seen.values() if row["kind"] == "comment" and not row["parent_id"]]
    if missing or unknown_parents:
        gaps.append({"reason": "missing-parent-context", "ids": missing, "records_without_parent_id": unknown_parents})
    if job.get("mode", "discovery") == "threads":
        # Window restrictions, deleted messages and Actor limits make platform-wide
        # comment completeness unverifiable, even when displayed counts agree.
        gaps.append({"reason": "comment-completeness-unverified", "max_comments_per_post": value["maxComments"]})
        for row in seen.values():
            expected = row["metadata"].get("num_comments")
            if row["kind"] == "post" and isinstance(expected, int) and comments[row["native_id"]] < expected:
                gaps.append({"reason": "comment-count-gap", "post_id": row["native_id"],
                             "displayed": expected, "returned": comments[row["native_id"]]})
    if job.get("mode", "discovery") == "discovery" and sum(row["kind"] == "post" for row in seen.values()) >= value["maxPosts"]:
        gaps.append({"reason": "discovery-post-cap"})
    primary = [row for row in seen.values() if not row["metadata"]["context_only"]]
    status = info["status"]
    if status in {"complete", "no-results"}:
        status = "partial" if gaps else ("complete" if primary else "no-results")
    result = {"job_id": job["id"], "platform": "reddit", "status": status,
              "counts": {"records": len(seen), "in_window": len(primary), "posts": sum(row["kind"] == "post" for row in seen.values()),
                         "comments": sum(comments.values())}, "gaps": gaps,
              "scope": "requested-sources-and-provider-returned-records", "actor": {key: val for key, val in info.items() if key != "item_raw_refs"}}
    ctx.checkpoint(job["id"], {"coverage": result})
    return result
