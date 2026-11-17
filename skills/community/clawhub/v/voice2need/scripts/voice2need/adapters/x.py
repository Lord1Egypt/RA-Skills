"""Official X search/lookup with bounded pagination and explicit context gaps.

https://docs.x.com/x-api/posts/search/integrate/paginate
https://docs.x.com/x-api/posts/lookup/introduction (checked 2026-09-15).
"""

import hashlib
import json
import re

from voice2need.records import in_window, iso_time, make_record
from voice2need.runtime import SourceError, require_env
from .apify import positive_int

API = "https://api.x.com/2/tweets"
FIELDS = "id,text,created_at,author_id,conversation_id,referenced_tweets,public_metrics,lang,note_tweet"


def _ids(values):
    if not isinstance(values, list) or not values or any(not re.fullmatch(r"[0-9]+", str(value)) for value in values):
        raise SourceError("invalid-input", "tweet_ids must be a nonempty array of numeric IDs")
    return list(dict.fromkeys(str(value) for value in values))


def _parse(response, job, *, context=False, lookup=False):
    payload = response.data
    if not isinstance(payload, dict):
        raise SourceError("schema-drift", "X response must be an object")
    meta = payload.get("meta") or {}
    if not isinstance(meta, dict):
        raise SourceError("schema-drift", "X response metadata must be an object")
    if "data" not in payload and not (payload.get("errors") or meta.get("result_count") == 0):
        raise SourceError("schema-drift", "X response lacks data, errors or an empty-result marker")
    data = payload.get("data", [])
    if not isinstance(data, list):
        raise SourceError("schema-drift", "X data must be an array")
    if payload.get("errors") and not data and not lookup:
        raise SourceError("provider-failed", "X search returned provider errors without data")
    records = []
    for index, item in enumerate(data):
        if not isinstance(item, dict) or not re.fullmatch(r"[0-9]+", str(item.get("id", ""))) or not isinstance(item.get("text"), str):
            raise SourceError("schema-drift", "X post lacks a valid ID/text")
        if not iso_time(item.get("created_at")) or not item.get("conversation_id"):
            raise SourceError("schema-drift", "X requested created_at/conversation_id fields were not returned")
        refs = item.get("referenced_tweets", item.get("referenced_posts", []))
        if not isinstance(refs, list) or any(not isinstance(ref, dict) or ref.get("type") not in {"replied_to", "quoted", "retweeted"} or not re.fullmatch(r"[0-9]+", str(ref.get("id", ""))) for ref in refs):
            raise SourceError("schema-drift", "X references have an unknown type or ID")
        refs = [{"id": str(ref["id"]), "type": ref["type"]} for ref in refs]
        types = {ref["type"] for ref in refs}
        parent_id = next((ref["id"] for ref in refs if ref["type"] == "replied_to"), None)
        kind = "reply" if parent_id else "quote" if "quoted" in types else "retweet" if "retweeted" in types else "post"
        # X's quickstart documents tweet.fields; generated reference pages also
        # show note_post. Accept both returned names without a network fallback.
        note_field = "note_tweet" if isinstance(item.get("note_tweet"), dict) else "note_post"
        note = item.get(note_field)
        text = note.get("text") if isinstance(note, dict) and isinstance(note.get("text"), str) else item["text"]
        native_id = str(item["id"])
        outside = not in_window(item.get("created_at"), job.get("start"), job.get("end"))
        # Keep out-of-window objects for discussion context; never count them as
        # target-window occurrences or turn their absence into a research result.
        metadata = {"job_id": job["id"], "context_only": context or outside, "context_depth": 0,
                    "in_window": not outside, "window": {"start": job.get("start"), "end": job.get("end")},
                    "referenced_tweets": refs, "reference_types": sorted(types),
                    "public_metrics": item.get("public_metrics", {}), "language": item.get("lang"),
                    "text_source": note_field if isinstance(note, dict) and isinstance(note.get("text"), str) else "text",
                    "retweet_occurrence_only": "retweeted" in types}
        records.append(make_record("x", native_id, kind, text, item.get("author_id"), item.get("created_at"),
                                   f"https://x.com/i/web/status/{native_id}", str(item.get("conversation_id") or native_id),
                                   parent_id=parent_id, raw=[dict(response.raw, locator=f"$.data.data[{index}]")], metadata=metadata))
    return records, payload.get("meta") or {}, bool(payload.get("errors"))


def collect(ctx, job):
    mode = job.get("mode", "search_recent")
    aliases = {"search": "search_recent", "recent": "search_recent", "all": "search_all"}
    mode = aliases.get(mode, mode)
    if mode not in {"search_recent", "search_all", "lookup"}:
        raise SourceError("invalid-input", "X mode must be search_recent, search_all or lookup")
    max_pages = positive_int(job.get("max_pages", 100), "max_pages", 10000)
    size = positive_int(job.get("page_size", 100), "page_size", 500 if mode == "search_all" else 100)
    if mode != "lookup" and size < 10:
        raise SourceError("invalid-input", "X search page_size must be at least 10")
    if mode != "lookup" and (not isinstance(job.get("query"), str) or not job["query"].strip()):
        raise SourceError("invalid-input", "X search requires query")
    requested = _ids(job.get("tweet_ids")) if mode == "lookup" else []
    depth_limit = positive_int(job.get("context_depth", 1), "context_depth", 10)
    lookup_limit = positive_int(job.get("max_context_requests", 10), "max_context_requests", 1000)
    context_cap = positive_int(job.get("max_context_ids", 1000), "max_context_ids", 100000)
    fingerprint = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()
    saved = ctx.get_checkpoint(job["id"]) or {}
    if saved and saved.get("fingerprint") != fingerprint:
        raise SourceError("invalid-input", "X job changed; use a new job ID/run for changed scope")
    if saved.get("done"):
        return saved["coverage"]
    headers = {"Authorization": "Bearer " + require_env("X_BEARER_TOKEN")}
    known_ids = set(saved.get("record_ids", []))
    known = {row["native_id"]: row for row in ctx.records() if row["platform"] == "x" and row["native_id"] in known_ids}
    gaps = list(saved.get("gaps", []))
    pages, token = saved.get("pages", 0), saved.get("next_token")
    tokens_seen = set(saved.get("tokens_seen", []))
    search_done = saved.get("search_done", False)
    looked_up = set(saved.get("looked_up", []))
    context_requests = saved.get("context_requests", 0)

    def checkpoint(**extra):
        state = {"fingerprint": fingerprint, "record_ids": sorted(known), "pages": pages,
                 "next_token": token, "search_done": search_done, "gaps": gaps,
                 "tokens_seen": sorted(tokens_seen),
                 "looked_up": sorted(looked_up), "context_requests": context_requests}
        state.update(extra)
        ctx.checkpoint(job["id"], state)

    def add(response, context=False, lookup=False, depths=None):
        records, meta, errors = _parse(response, job, context=context, lookup=lookup)
        for row in records:
            if depths:
                row["metadata"]["context_depth"] = depths.get(row["native_id"], depth_limit)
            old = known.get(row["native_id"])
            if old and not old["metadata"].get("context_only"):
                row["metadata"]["context_only"] = False
                row["metadata"]["context_depth"] = 0
        ctx.add_records(records)
        known.update((row["native_id"], row) for row in records)
        if errors:
            gaps.append({"reason": "provider-partial-errors", "raw": response.raw})
        return records, meta

    while not search_done and pages < max_pages:
        params = {"tweet.fields": FIELDS}
        if mode == "lookup":
            batch = requested[pages * 100:(pages + 1) * 100]
            if not batch:
                search_done = True
                break
            params["ids"] = ",".join(batch)
            url, units = API, len(batch)
        else:
            params.update(query=job["query"], max_results=size, sort_order=job.get("sort_order", "recency"))
            for key, field in (("start", "start_time"), ("end", "end_time")):
                if job.get(key):
                    params[field] = job[key]
            if token:
                params["next_token"] = token
            url, units = f"{API}/search/{'all' if mode == 'search_all' else 'recent'}", size
        response = ctx.request("GET", url, params=params, headers=headers, units=units)
        records, meta = add(response, lookup=mode == "lookup")
        pages += 1
        if mode == "lookup":
            missing = sorted(set(batch) - {row["native_id"] for row in records})
            if missing:
                gaps.append({"reason": "lookup-unavailable", "ids": missing})
            search_done = pages * 100 >= len(requested)
        else:
            next_token = meta.get("next_token")
            if next_token and (not isinstance(next_token, str) or next_token in tokens_seen):
                raise SourceError("schema-drift", "X pagination token is invalid or did not advance")
            if next_token:
                tokens_seen.add(next_token)
            token = next_token
            search_done = not token
        checkpoint()
    if not search_done:
        gaps.append({"reason": "search-page-cap", "next_token": token})

    # Bounded breadth-first hydration: each native ID is looked up at most once.
    # Context references retain types; text from quotes is never concatenated.
    while True:
        missing_depths = {}
        for row in known.values():
            depth = row["metadata"].get("context_depth", 0) + 1
            for ref in row["metadata"].get("referenced_tweets", []):
                if depth <= depth_limit and ref["id"] not in known and ref["id"] not in looked_up:
                    missing_depths[ref["id"]] = min(depth, missing_depths.get(ref["id"], depth))
        missing = sorted(missing_depths)
        if not job.get("hydrate_context", True) or not missing:
            break
        remaining = max(0, context_cap - len(looked_up))
        if not remaining or context_requests >= lookup_limit:
            break
        missing = missing[:remaining]
        for offset in range(0, len(missing), 100):
            if context_requests >= lookup_limit:
                break
            batch = missing[offset:offset + 100]
            response = ctx.request("GET", API, params={"ids": ",".join(batch), "tweet.fields": FIELDS},
                                   headers=headers, units=len(batch))
            add(response, context=True, lookup=True, depths=missing_depths)
            looked_up.update(batch)
            context_requests += 1
            checkpoint()
    missing = sorted({ref["id"] for row in known.values() for ref in row["metadata"].get("referenced_tweets", []) if ref["id"] not in known})
    if missing:
        gaps.append({"reason": "missing-reference-context", "ids": missing,
                     "hydration_enabled": bool(job.get("hydrate_context", True)), "looked_up": len(looked_up)})
    # Persist context status for analysis even after parents arrived on later pages.
    for row in known.values():
        row["metadata"]["missing_context_ids"] = [ref["id"] for ref in row["metadata"].get("referenced_tweets", []) if ref["id"] not in known]
        row["metadata"]["context_status"] = "missing" if row["metadata"]["missing_context_ids"] else "available"
    ctx.add_records(list(known.values()))
    primary = [row for row in known.values() if not row["metadata"].get("context_only")]
    coverage = {"job_id": job["id"], "platform": "x", "status": "partial" if gaps else ("complete" if primary else "no-results"),
                "counts": {"records": len(known), "primary": len(primary), "context": len(known) - len(primary),
                           "search_pages": pages, "context_requests": context_requests},
                "gaps": gaps, "scope": "requested-query-results-and-bounded-reference-context",
                "requested_window": {"start": job.get("start"), "end": job.get("end")},
                "unit_accounting": "conservative-requested-post-resources; not a cash invoice"}
    checkpoint(done=True, coverage=coverage)
    return coverage
