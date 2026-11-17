"""Bounded YouTube discovery, public discussions, and explicit transcripts.

Only ``collect`` reads credentials. Data API modes never invoke Apify. A complete
status means the requested API enumeration finished, not that all YouTube content
or every moderated/deleted comment was available. Raw pages are saved by Session
before normalization; replays use Session's request cache and stable evidence IDs.

Reference contracts (verified 2026-09-15):
https://developers.google.com/youtube/v3/docs/commentThreads
https://developers.google.com/youtube/v3/docs/comments/list
https://developers.google.com/youtube/v3/docs/playlistItems
https://developers.google.com/youtube/v3/docs/search/list
https://apify.com/starvibe/youtube-video-transcript/input-schema
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse

from voice2need.records import in_window, iso_time, make_record
from voice2need.runtime import SourceError, require_env


API_BASE = "https://www.googleapis.com/youtube/v3"
TRANSCRIPT_ACTOR = "starvibe/youtube-video-transcript"
_VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")
_MODES = {
    "search": "search", "discovery": "search",
    "channel": "channels", "channels": "channels", "uploads": "channels",
    "videos": "videos", "deep": "videos", "comments": "videos",
    "transcript": "transcript",
}


def _positive(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise SourceError("invalid-input", f"{name} must be a positive integer")
    return value


def _strings(value, name):
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
        raise SourceError("invalid-input", f"{name} must be an array of nonempty strings")
    return list(dict.fromkeys(v.strip() for v in value))


def _video_id(value):
    if _VIDEO_ID.fullmatch(value):
        return value
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    parts = parsed.path.strip("/").split("/")
    candidate = None
    if parsed.scheme not in {"https", "http"}:
        raise SourceError("invalid-input", "Expected a YouTube video ID or URL")
    if host in {"youtu.be", "www.youtu.be"} and len(parts) == 1:
        candidate = parts[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
        elif len(parts) == 2 and parts[0] in {"shorts", "embed", "live"}:
            candidate = parts[1]
    if not isinstance(candidate, str) or not _VIDEO_ID.fullmatch(candidate):
        raise SourceError("invalid-input", "Expected a YouTube video ID or URL")
    return candidate


def _url(video_id, comment_id=None, timestamp=None):
    params = {"v": video_id}
    if comment_id is not None:
        params["lc"] = comment_id
    if timestamp is not None:
        params["t"] = str(math.floor(timestamp)) + "s"
    return "https://www.youtube.com/watch?" + urlencode(params)


def _mapping(value, label):
    if not isinstance(value, dict):
        raise SourceError("schema-drift", f"YouTube {label} must be an object")
    return value


def _identifier(value, label):
    if not isinstance(value, str) or not value:
        raise SourceError("schema-drift", f"YouTube {label} is missing")
    return value


def _count(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
    if isinstance(value, str) and value.isdecimal():
        return int(value)
    return None


def _raw(response, locator):
    return dict(response.raw, locator=locator)


class _Collector:
    def __init__(self, ctx, job, mode):
        self.ctx, self.job, self.mode = ctx, job, mode
        self.max_pages = _positive(job.get("max_pages", 100), "max_pages")
        self.key = None
        self.ids = set()
        self.coverage = {
            "job_id": job.get("id"), "platform": "youtube", "mode": mode,
            "status": "no-results", "counts": {}, "gaps": [],
            "endpoint_requests": {}, "video_ids": [], "discussions": {},
            "enumeration_complete": False, "population_complete": False,
            "scope": "API-visible content for this explicit job at collection time",
            "window": {"start": job.get("start"), "end": job.get("end")},
            "limitations": [
                "Search ranking and API visibility do not establish population completeness.",
                "Deleted, private, moderated, and otherwise inaccessible content is unavailable.",
            ],
        }

    def gap(self, reason, **details):
        item = {"reason": reason, **details}
        if item not in self.coverage["gaps"]:
            self.coverage["gaps"].append(item)

    def save(self, records):
        if records:
            self.ctx.add_records(records)
        for record in records:
            eid = record["evidence_id"]
            if eid not in self.ids:
                self.ids.add(eid)
                counts = self.coverage["counts"]
                counts[record["kind"]] = counts.get(record["kind"], 0) + 1
        self.ctx.checkpoint(self.job.get("id", "youtube"), {"coverage": self.coverage})

    def metadata(self, published_at, **extra):
        within = in_window(published_at, self.job.get("start"), self.job.get("end"))
        return {"in_window": within, "context_only": not within, **extra}

    def request(self, endpoint, params):
        if self.key is None:
            self.key = require_env("YOUTUBE_API_KEY")
        counts = self.coverage["endpoint_requests"]
        counts[endpoint] = counts.get(endpoint, 0) + 1
        # Search uses its own 1-unit Search Queries bucket as of 2026-09-14.
        # This records logical calls; cached replays consume no Session budget.
        try:
            return self.ctx.request("GET", API_BASE + "/" + endpoint,
                                    params={**params, "key": self.key}, units=1)
        except SourceError as exc:
            reason = getattr(exc, "reason", None)
            if reason in {"quotaExceeded", "dailyLimitExceeded", "dailyLimitExceededUnreg"}:
                raise SourceError("budget-exhausted", "YouTube API quota was exhausted",
                                  exc.http_status, reason=reason, raw=exc.raw) from None
            if reason in {"rateLimitExceeded", "userRateLimitExceeded"}:
                raise SourceError("rate-limited", "YouTube API rate limit was reached",
                                  exc.http_status, reason=reason, raw=exc.raw) from None
            raise

    def pages(self, endpoint, params, *, scope):
        token = None
        seen = set()
        for page_number in range(self.max_pages):
            response = self.request(endpoint, {**params, **({"pageToken": token} if token else {})})
            data = _mapping(response.data, endpoint + " response")
            items = data.get("items")
            if not isinstance(items, list):
                raise SourceError("schema-drift", f"YouTube {endpoint} response lacks items array")
            yield response
            next_token = data.get("nextPageToken")
            if next_token is None:
                return
            if not isinstance(next_token, str) or not next_token or next_token in seen:
                self.gap("pagination-invalid-token", endpoint=endpoint, scope=scope,
                         raw=response.raw)
                return
            seen.add(next_token)
            token = next_token
            if page_number + 1 == self.max_pages:
                self.gap("page-limit", endpoint=endpoint, scope=scope,
                         next_page_token=next_token, raw=response.raw)

    def video_record(self, video_id, snippet, raw, *, details=None, discovery=None):
        published = snippet.get("publishedAt")
        return make_record(
            "youtube", "video:" + video_id, "video", snippet.get("description", ""),
            snippet.get("channelId"), published, _url(video_id), "video:" + video_id,
            title=snippet.get("title", ""), raw=[raw],
            metadata=self.metadata(
                published, video_id=video_id, channel_title=snippet.get("channelTitle"),
                discovery=discovery, details=details or {},
                metadata_completeness="discovery-snippet" if discovery else "video-details",
                text_role="creator-description", transcript_status="not-requested",
            ),
        )

    def add_candidate(self, video_id, snippet, raw, *, discovery):
        _identifier(video_id, "video ID")
        published = snippet.get("publishedAt")
        if iso_time(published) is None:
            self.gap("video-published-at-unavailable", video_id=video_id, raw=raw)
        if in_window(published, self.job.get("start"), self.job.get("end")):
            self.save([self.video_record(video_id, snippet, raw, discovery=discovery)])
            if video_id not in self.coverage["video_ids"]:
                self.coverage["video_ids"].append(video_id)

    def search(self):
        query = self.job.get("query")
        if not isinstance(query, str) or not query.strip():
            raise SourceError("invalid-input", "YouTube search requires query")
        params = {"part": "snippet", "type": "video", "q": query,
                  "maxResults": 50, "order": self.job.get("order", "relevance")}
        for source, dest in (("start", "publishedAfter"), ("end", "publishedBefore"),
                             ("language", "relevanceLanguage"), ("region_code", "regionCode")):
            if self.job.get(source):
                params[dest] = iso_time(self.job[source]) if source in {"start", "end"} else self.job[source]
        for response in self.pages("search", params, scope="search"):
            for index, item in enumerate(response.data["items"]):
                item = _mapping(item, "search item")
                ids = _mapping(item.get("id"), "search identity")
                snippet = _mapping(item.get("snippet"), "search snippet")
                self.add_candidate(ids.get("videoId"), snippet,
                                   _raw(response, f"$.data.items[{index}]"), discovery="search")

    def channels(self):
        channels = _strings(self.job.get("channel_ids"), "channel_ids")
        handles = _strings(self.job.get("handles"), "handles")
        if not channels and not handles:
            raise SourceError("invalid-input", "YouTube channels requires channel_ids or handles")
        selectors = [{"id": channel} for channel in channels]
        selectors.extend({"forHandle": handle} for handle in handles)
        seen = set()
        for selector in selectors:
            response = self.request("channels", {"part": "snippet,contentDetails", **selector})
            data = _mapping(response.data, "channels response")
            items = data.get("items")
            if not isinstance(items, list):
                raise SourceError("schema-drift", "YouTube channels response lacks items array")
            if not items:
                self.gap("channel-unavailable", selector=selector, raw=response.raw)
            for index, channel in enumerate(items):
                channel = _mapping(channel, "channel")
                channel_id = _identifier(channel.get("id"), "channel ID")
                if channel_id in seen:
                    continue
                seen.add(channel_id)
                details = _mapping(channel.get("contentDetails"), "channel contentDetails")
                related = _mapping(details.get("relatedPlaylists"), "relatedPlaylists")
                uploads = related.get("uploads")
                if not isinstance(uploads, str) or not uploads:
                    self.gap("uploads-playlist-unavailable", channel_id=channel_id,
                             raw=_raw(response, f"$.data.items[{index}]"))
                    continue
                params = {"part": "snippet,contentDetails", "playlistId": uploads, "maxResults": 50}
                for page in self.pages("playlistItems", params, scope=channel_id):
                    for item_index, item in enumerate(page.data["items"]):
                        item = _mapping(item, "playlist item")
                        snippet = dict(_mapping(item.get("snippet"), "playlist snippet"))
                        content = _mapping(item.get("contentDetails"), "playlist contentDetails")
                        video_id = _identifier(content.get("videoId"), "playlist video ID")
                        # Playlist snippet.publishedAt is insertion time, not video publication.
                        snippet["publishedAt"] = content.get("videoPublishedAt")
                        snippet["channelId"] = snippet.get("videoOwnerChannelId") or channel_id
                        self.add_candidate(video_id, snippet,
                                           _raw(page, f"$.data.items[{item_index}]"),
                                           discovery="channel-uploads")

    def comment_record(self, item, video_id, thread_id, parent, raw, total_replies=None):
        item = _mapping(item, "comment")
        comment_id = _identifier(item.get("id"), "comment ID")
        snippet = _mapping(item.get("snippet"), "comment snippet")
        if snippet.get("videoId", video_id) != video_id:
            raise SourceError("schema-drift", "YouTube comment videoId does not match requested video")
        if parent is not None and snippet.get("parentId") != parent:
            raise SourceError("schema-drift", "YouTube reply parentId does not match requested comment")
        author = snippet.get("authorChannelId")
        author_id = author.get("value") if isinstance(author, dict) else None
        text = snippet.get("textOriginal", snippet.get("textDisplay", ""))
        if not isinstance(text, str):
            raise SourceError("schema-drift", "YouTube comment text must be a string")
        published = snippet.get("publishedAt")
        return make_record(
            "youtube", "comment:" + comment_id, "reply" if parent else "comment", text,
            author_id, published, _url(video_id, comment_id), "video:" + video_id,
            parent_id="comment:" + parent if parent else "video:" + video_id, raw=[raw],
            metadata=self.metadata(published, video_id=video_id, thread_id=thread_id,
                                   comment_id=comment_id, author_name=snippet.get("authorDisplayName"),
                                   updated_at=iso_time(snippet.get("updatedAt")),
                                   like_count=_count(snippet.get("likeCount")),
                                   total_reply_count=total_replies, text_role="viewer-comment"),
        )

    def replies(self, video_id, thread_id, top_id, expected, seen):
        params = {"part": "snippet", "parentId": top_id, "maxResults": 100, "textFormat": "plainText"}
        for response in self.pages("comments", params, scope=top_id):
            page = []
            for index, item in enumerate(response.data["items"]):
                record = self.comment_record(item, video_id, thread_id, top_id,
                                             _raw(response, f"$.data.items[{index}]"))
                page.append(record)
                seen.add(record["native_id"])
            self.save(page)
        if len(seen) != expected:
            self.gap("reply-count-mismatch", video_id=video_id, parent_id="comment:" + top_id,
                     expected=expected, observed=len(seen))

    def discussion(self, video_id, expected_comments=None):
        before = len(self.coverage["gaps"])
        comment_ids = set()
        top_ids = set()
        params = {"part": "snippet,replies", "videoId": video_id, "maxResults": 100,
                  "order": "time", "textFormat": "plainText"}
        try:
            for response in self.pages("commentThreads", params, scope=video_id):
                pending = []
                page = []
                for index, thread in enumerate(response.data["items"]):
                    thread = _mapping(thread, "comment thread")
                    thread_id = _identifier(thread.get("id"), "thread ID")
                    snippet = _mapping(thread.get("snippet"), "thread snippet")
                    if snippet.get("videoId") != video_id:
                        raise SourceError("schema-drift", "YouTube thread videoId does not match requested video")
                    total = _count(snippet.get("totalReplyCount"))
                    if total is None:
                        raise SourceError("schema-drift", "YouTube thread lacks totalReplyCount")
                    top = self.comment_record(snippet.get("topLevelComment"), video_id, thread_id, None,
                                              _raw(response, f"$.data.items[{index}].snippet.topLevelComment"), total)
                    page.append(top)
                    comment_ids.add(top["native_id"])
                    top_id = top["metadata"]["comment_id"]
                    replies = _mapping(thread.get("replies", {}), "embedded replies").get("comments", [])
                    if not isinstance(replies, list):
                        raise SourceError("schema-drift", "YouTube embedded replies must be an array")
                    seen_replies = set()
                    for reply_index, reply in enumerate(replies):
                        record = self.comment_record(
                            reply, video_id, thread_id, top_id,
                            _raw(response, f"$.data.items[{index}].replies.comments[{reply_index}]"))
                        page.append(record)
                        seen_replies.add(record["native_id"])
                    comment_ids.update(seen_replies)
                    if top_id not in top_ids:
                        pending.append((thread_id, top_id, total, seen_replies))
                    top_ids.add(top_id)
                # Preserve the entire returned thread page before any reply request can fail.
                self.save(page)
                for thread_id, top_id, total, seen_replies in pending:
                    if len(seen_replies) < total:
                        try:
                            self.replies(video_id, thread_id, top_id, total, seen_replies)
                        finally:
                            comment_ids.update(seen_replies)
                    elif len(seen_replies) != total:
                        self.gap("reply-count-mismatch", video_id=video_id,
                                 parent_id="comment:" + top_id, expected=total, observed=len(seen_replies))
                    comment_ids.update(seen_replies)
        except SourceError as exc:
            reason = getattr(exc, "reason", None)
            if reason == "commentsDisabled":
                self.gap("comments-disabled", video_id=video_id, raw=getattr(exc, "raw", None))
            elif exc.status in {"forbidden", "provider-failed"}:
                self.gap(exc.status, video_id=video_id, provider_reason=reason,
                         raw=getattr(exc, "raw", None))
            else:
                raise
        if expected_comments is not None and len(comment_ids) != expected_comments:
            self.gap("comment-count-mismatch", video_id=video_id,
                     expected=expected_comments, observed=len(comment_ids))
        self.coverage["discussions"][video_id] = {
            "status": "complete" if before == len(self.coverage["gaps"]) else "partial",
            "top_level_comments": len(top_ids), "comments_and_replies": len(comment_ids),
            "expected_comments_at_metadata_fetch": expected_comments,
        }

    def videos(self, ids):
        self.coverage["video_ids"] = ids
        available = []
        for offset in range(0, len(ids), 50):
            batch = ids[offset:offset + 50]
            response = self.request("videos", {"part": "snippet,statistics,contentDetails,status",
                                                "id": ",".join(batch)})
            data = _mapping(response.data, "videos response")
            if not isinstance(data.get("items"), list):
                raise SourceError("schema-drift", "YouTube videos response lacks items array")
            found = set()
            for index, item in enumerate(data["items"]):
                item = _mapping(item, "video")
                video_id = _identifier(item.get("id"), "video ID")
                if video_id not in batch:
                    raise SourceError("schema-drift", "YouTube returned an unrequested video")
                found.add(video_id)
                snippet = _mapping(item.get("snippet"), "video snippet")
                statistics = _mapping(item.get("statistics", {}), "video statistics")
                details = {"statistics": statistics, "content_details": item.get("contentDetails", {}),
                           "status": item.get("status", {})}
                self.save([self.video_record(video_id, snippet,
                                            _raw(response, f"$.data.items[{index}]"), details=details)])
                available.append((video_id, _count(statistics.get("commentCount"))))
            for missing in sorted(set(batch) - found):
                self.gap("video-unavailable", video_id=missing, raw=response.raw)
        for video_id, count in available:
            self.discussion(video_id, count)

    def transcripts(self, ids):
        # This provider lane is entered only by an explicit transcript job.
        from voice2need.adapters.apify import run_actor

        self.coverage["video_ids"] = ids
        self.coverage["actor"] = TRANSCRIPT_ACTOR
        self.coverage["actor_runs"] = []
        for video_id in ids:
            payload = {"youtube_url": _url(video_id)}
            if self.job.get("language"):
                payload["language"] = self.job["language"]
            nonempty = set()

            def consume(items, refs):
                if len(items) != len(refs):
                    raise SourceError("schema-drift", "Transcript item provenance does not match dataset")
                for item, ref in zip(items, refs):
                    item = _mapping(item, "transcript result")
                    actual_id = item.get("video_id")
                    if actual_id != video_id:
                        if item.get("status") == "error" or item.get("error"):
                            self.gap("transcript-provider-error", video_id=video_id, raw=ref)
                            continue
                        raise SourceError("schema-drift", "Transcript returned a missing or unrequested video ID")
                    if item.get("status") == "error" or item.get("error"):
                        self.gap("transcript-provider-error", video_id=video_id, raw=ref)
                        continue
                    segments = item.get("transcript")
                    if not isinstance(segments, list):
                        self.gap("transcript-schema-drift", video_id=video_id, raw=ref)
                        continue
                    if not segments:
                        self.gap("transcript-zero-segments", video_id=video_id, raw=ref)
                    records = []
                    for index, segment in enumerate(segments):
                        segment_ref = dict(ref, locator=ref["locator"] + f".transcript[{index}]")
                        if not isinstance(segment, dict) or not isinstance(segment.get("text"), str):
                            self.gap("transcript-invalid-segment", video_id=video_id, raw=segment_ref)
                            continue
                        text, start, end = segment["text"], segment.get("start"), segment.get("end")
                        if (isinstance(start, bool) or not isinstance(start, (int, float))
                                or not math.isfinite(start) or start < 0
                                or isinstance(end, bool) or not isinstance(end, (int, float))
                                or not math.isfinite(end) or end < start):
                            self.gap("transcript-invalid-timestamp", video_id=video_id, raw=segment_ref)
                            continue
                        if not text.strip():
                            self.gap("transcript-empty-segment", video_id=video_id, raw=segment_ref)
                        language = item.get("selected_language") or item.get("language") or ""
                        identity = json.dumps([video_id, language, float(start), float(end), text],
                                              ensure_ascii=False, separators=(",", ":"))
                        digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
                        published = item.get("published_at")
                        records.append(make_record(
                            "youtube", f"transcript:{video_id}:{digest}", "transcript", text,
                            item.get("channel_id"), published, _url(video_id, timestamp=start),
                            "video:" + video_id, parent_id="video:" + video_id,
                            title=item.get("title", ""), raw=[segment_ref],
                            metadata=self.metadata(
                                published, video_id=video_id, start_seconds=start, end_seconds=end,
                                language=language, is_auto_generated=item.get("is_auto_generated"),
                                available_languages=item.get("available_languages"),
                                text_role="creator-transcript", provider="apify", actor=TRANSCRIPT_ACTOR,
                            ),
                        ))
                        if text.strip():
                            nonempty.add(digest)
                    self.save(records)

            items, raw_ref, info = run_actor(
                self.ctx, TRANSCRIPT_ACTOR, payload,
                max_charge_usd=self.job.get("max_charge_usd", 1),
                max_polls=self.job.get("max_polls", 30),
                poll_seconds=self.job.get("poll_seconds", 2),
                max_dataset_pages=self.max_pages, on_page=consume,
            )
            self.coverage["actor_runs"].append({"video_id": video_id, **info})
            if info.get("status") not in {"complete", "no-results"}:
                self.gap("transcript-actor-partial", video_id=video_id,
                         actor_status=info.get("actor_status"), gaps=info.get("gaps", []))
            if not items or not nonempty:
                self.gap("transcript-zero-segments", video_id=video_id, raw=raw_ref)
            if info.get("remote_run_may_continue") or info.get("status") in {"timeout", "provider-failed"}:
                # A running or failed Actor is not permission to start more paid
                # transcript runs. Keep its state available for explicit review.
                self.gap("timeout" if info.get("remote_run_may_continue") else info["status"],
                         video_id=video_id, actor_status=info.get("actor_status"), raw=raw_ref)
                break

    def finish(self):
        gaps = self.coverage["gaps"]
        self.coverage["counts"]["records"] = len(self.ids)
        if not self.coverage.get("error_status"):
            self.coverage["status"] = "partial" if gaps else ("complete" if self.ids else "no-results")
        self.coverage["enumeration_complete"] = not gaps
        calls = self.coverage["endpoint_requests"]
        self.coverage["quota_estimate"] = {
            "search_query_units": calls.get("search", 0),
            "data_api_units": sum(value for key, value in calls.items() if key != "search"),
            "basis": "Logical endpoint calls; cached replays use no new quota. Account limits are separate.",
        }
        self.ctx.checkpoint(self.job.get("id", "youtube"), {"coverage": self.coverage})
        return self.coverage


def collect(ctx, job):
    """Collect a configured, bounded job without implicit discovery or providers.

    Modes: search/discovery, channels/channel/uploads, videos/deep/comments, and
    transcript. ``video_ids`` or YouTube ``urls`` are required for deep/transcript;
    search never implicitly deep-fetches candidates. Deep modes retain discussion
    context outside [start,end), flagged through metadata.context_only.
    """
    mode = _MODES.get(job.get("mode", "search"))
    if mode is None:
        raise SourceError("invalid-input", "Unsupported YouTube mode")
    for name in ("start", "end"):
        if job.get(name) is not None and iso_time(job[name]) is None:
            raise SourceError("invalid-input", f"YouTube {name} must be a valid timestamp")
    if (job.get("start") is not None and job.get("end") is not None
            and datetime.fromisoformat(iso_time(job["start"]).replace("Z", "+00:00"))
            >= datetime.fromisoformat(iso_time(job["end"]).replace("Z", "+00:00"))):
        raise SourceError("invalid-input", "YouTube window start must be earlier than end")
    collector = _Collector(ctx, job, mode)
    ids = []
    if mode in {"videos", "transcript"}:
        supplied = _strings(job.get("video_ids"), "video_ids") + _strings(job.get("urls"), "urls")
        ids = list(dict.fromkeys(_video_id(value) for value in supplied))
        if not ids:
            raise SourceError("invalid-input", "YouTube deep/transcript jobs require video_ids or urls")
    try:
        if mode == "search":
            collector.search()
        elif mode == "channels":
            collector.channels()
        elif mode == "videos":
            collector.videos(ids)
        else:
            collector.transcripts(ids)
    except SourceError as exc:
        collector.coverage["error_status"] = exc.status
        collector.coverage["status"] = "partial" if collector.ids else exc.status
        collector.gap(exc.status, provider_reason=getattr(exc, "reason", None),
                      raw=getattr(exc, "raw", None))
    return collector.finish()
