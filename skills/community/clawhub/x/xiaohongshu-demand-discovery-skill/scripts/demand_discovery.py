"""
Xiaohongshu Demand Discovery Collector.

This module is intentionally read-only: it uses search and note detail pages to
collect public notes/comments, then writes cleaned JSONL files for downstream
analysis.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9 fallback
    ZoneInfo = None

from .client import CaptchaError, DEFAULT_COOKIE_PATH, XiaohongshuClient
from .feed import FeedDetailAction
from .login import LoginAction
from .search import SearchAction


DEFAULT_KEYWORDS = [
    "求推荐",
    "避雷",
    "平替",
    "真实测评",
    "后悔买",
    "踩坑",
    "好用吗",
    "怎么选",
    "值不值得买",
    "学生党",
    "新手必备",
    "替代品",
    "不好用",
    "怎么解决",
]

DEFAULT_SOURCE_TYPE = "demand_discovery"
PLATFORM = "xiaohongshu"
BASE_DIR = Path(__file__).resolve().parent.parent

PUBLISH_TIME_PATHS = [
    ("time",),
    ("lastUpdateTime",),
    ("createTime",),
    ("publishTime",),
    ("note", "time"),
    ("note", "lastUpdateTime"),
    ("note", "createTime"),
    ("note", "publishTime"),
    ("noteCard", "time"),
    ("noteCard", "lastUpdateTime"),
    ("noteCard", "createTime"),
    ("noteCard", "publishTime"),
]

POST_FIELD_PATHS = {
    "post_title": [
        ("title",),
        ("displayTitle",),
        ("note", "title"),
        ("note", "displayTitle"),
        ("noteCard", "displayTitle"),
        ("noteCard", "title"),
    ],
    "post_content": [
        ("desc",),
        ("content",),
        ("note", "desc"),
        ("note", "content"),
        ("noteCard", "desc"),
        ("noteCard", "content"),
    ],
    "post_type": [
        ("type",),
        ("note", "type"),
        ("noteCard", "type"),
    ],
}

INTERACT_PATHS = [
    ("interactInfo",),
    ("note", "interactInfo"),
    ("noteCard", "interactInfo"),
]

ADVERTISEMENT_PATTERNS = [
    r"加\s*(微信|v信|vx|v|微)",
    r"(微信|v信|vx)\s*[:：]?\s*[a-zA-Z0-9_-]{5,}",
    r"私信.*(链接|优惠|领取|返利|代理|合作)",
    r"(代购|招商|代理|刷单|兼职|返利|领券|优惠券|内部券)",
    r"(http|https)://",
    r"复制.*打开",
]

SHORT_NOISE = {
    ".",
    "..",
    "...",
    "。",
    "。。",
    "蹲",
    "蹲蹲",
    "dd",
    "cy",
    "mark",
    "m",
    "1",
    "+1",
    "好",
    "嗯",
    "啊",
}


@dataclass
class FilterStats:
    filtered_empty_comments: int = 0
    filtered_duplicate_comments: int = 0
    filtered_short_comments: int = 0
    filtered_ad_comments: int = 0


@dataclass
class KeywordStats:
    search_results: int = 0
    notes_seen: int = 0
    notes_saved: int = 0
    comments_raw: int = 0
    comments_saved: int = 0
    publish_time_unknown: int = 0
    errors: List[Dict[str, str]] = field(default_factory=list)


def get_timezone(name: str):
    if ZoneInfo is not None:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    if name == "Asia/Shanghai":
        return timezone(timedelta(hours=8), name="Asia/Shanghai")
    return timezone.utc


def now_in_timezone(tz_name: str) -> datetime:
    return datetime.now(get_timezone(tz_name))


def default_output_dir(tz_name: str) -> Path:
    timestamp = now_in_timezone(tz_name).strftime("%Y%m%d_%H%M%S")
    return BASE_DIR / "data" / "demand_discovery" / timestamp


def load_keywords(raw_keywords: Optional[str] = None, keywords_file: Optional[str] = None) -> List[str]:
    keywords: List[str] = []
    if raw_keywords:
        keywords.extend(part.strip() for part in raw_keywords.split(",") if part.strip())

    if keywords_file:
        with open(keywords_file, "r", encoding="utf-8") as f:
            keywords.extend(line.strip() for line in f if line.strip() and not line.strip().startswith("#"))

    if not keywords:
        keywords = list(DEFAULT_KEYWORDS)

    deduped: List[str] = []
    seen = set()
    for keyword in keywords:
        if keyword not in seen:
            deduped.append(keyword)
            seen.add(keyword)
    return deduped


def json_dump_line(fp, row: Dict[str, Any]):
    fp.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def get_by_path(data: Any, path: Tuple[str, ...]) -> Any:
    current = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def first_value(data: Dict[str, Any], paths: Iterable[Tuple[str, ...]]) -> Any:
    for path in paths:
        value = get_by_path(data, path)
        if value not in (None, ""):
            return value
    return None


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        for key in ("text", "content", "value", "desc"):
            if key in value:
                return stringify(value.get(key))
    return str(value).strip()


def parse_count(value: Any) -> int:
    text = stringify(value).replace(",", "")
    if not text:
        return 0
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
    if not match:
        return 0
    number = float(match.group(1))
    if "万" in text:
        number *= 10000
    elif "千" in text:
        number *= 1000
    return int(number)


def stable_author_hash(raw_author: Any) -> str:
    raw = stringify(raw_author)
    if not raw:
        raw = "unknown"
    return hashlib.sha256(("xiaohongshu:" + raw).encode("utf-8")).hexdigest()


def extract_author_seed(item: Dict[str, Any]) -> str:
    candidates = [
        ("userId",),
        ("user_id",),
        ("authorId",),
        ("user", "userId"),
        ("user", "id"),
        ("userInfo", "userId"),
        ("userInfo", "id"),
        ("author", "userId"),
        ("author", "id"),
        ("user", "nickname"),
        ("user", "nickName"),
        ("userInfo", "nickname"),
        ("userInfo", "nickName"),
        ("author", "nickname"),
        ("author", "name"),
        ("user", "link"),
        ("userInfo", "link"),
    ]
    return stringify(first_value(item, candidates))


def clean_comment_text(text: Any) -> str:
    value = stringify(text)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def is_ad_comment(text: str) -> bool:
    lower = text.lower()
    return any(re.search(pattern, lower, flags=re.IGNORECASE) for pattern in ADVERTISEMENT_PATTERNS)


def is_short_noise(text: str) -> bool:
    normalized = text.strip().lower()
    if normalized in SHORT_NOISE:
        return True
    if len(normalized) <= 1:
        return True
    if len(normalized) <= 2 and not re.search(r"[\u4e00-\u9fff]", normalized):
        return True
    return False


def normalize_for_dedupe(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def parse_publish_time(value: Any, tz_name: str, now: Optional[datetime] = None) -> Tuple[Optional[datetime], str]:
    tz = get_timezone(tz_name)
    current = now.astimezone(tz) if now else datetime.now(tz)

    if value in (None, ""):
        return None, "publish_time_unknown"

    if isinstance(value, (int, float)):
        timestamp = float(value)
        if timestamp > 100000000000:
            timestamp = timestamp / 1000
        if timestamp > 1000000000:
            return datetime.fromtimestamp(timestamp, tz), "known"

    text = stringify(value)
    if not text:
        return None, "publish_time_unknown"

    if re.fullmatch(r"\d{10,13}", text):
        timestamp = float(text)
        if timestamp > 100000000000:
            timestamp = timestamp / 1000
        return datetime.fromtimestamp(timestamp, tz), "known"

    relative_patterns = [
        (r"(\d+)\s*分钟前", "minutes"),
        (r"(\d+)\s*小时前", "hours"),
        (r"(\d+)\s*天前", "days"),
    ]
    for pattern, unit in relative_patterns:
        match = re.search(pattern, text)
        if match:
            amount = int(match.group(1))
            return current - timedelta(**{unit: amount}), "known"

    if "刚刚" in text:
        return current, "known"
    if "昨天" in text:
        return current - timedelta(days=1), "known"
    if "前天" in text:
        return current - timedelta(days=2), "known"

    cleaned = text.replace("年", "-").replace("月", "-").replace("日", " ")
    cleaned = cleaned.replace("/", "-").strip()
    full_year_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    current_year_formats = [
        "%m-%d %H:%M",
        "%m-%d",
    ]
    for fmt in full_year_formats:
        try:
            parsed = datetime.strptime(cleaned, fmt)
            return parsed.replace(tzinfo=tz), "known"
        except ValueError:
            continue
    for fmt in current_year_formats:
        try:
            parsed = datetime.strptime(f"{current.year}-{cleaned}", f"%Y-{fmt}")
            return parsed.replace(tzinfo=tz), "known"
        except ValueError:
            continue

    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        return parsed.astimezone(tz), "known"
    except ValueError:
        return None, "publish_time_unknown"


def extract_publish_time(detail: Dict[str, Any], tz_name: str) -> Tuple[str, str, Optional[datetime]]:
    raw_value = first_value(detail, PUBLISH_TIME_PATHS)
    parsed, status = parse_publish_time(raw_value, tz_name)
    if not parsed:
        return "", status, None
    return parsed.isoformat(), status, parsed


def extract_interact_info(detail: Dict[str, Any]) -> Dict[str, Any]:
    for path in INTERACT_PATHS:
        value = get_by_path(detail, path)
        if isinstance(value, dict):
            return value
    return {}


def extract_post_data(detail: Optional[Dict[str, Any]], search_item: Dict[str, Any]) -> Dict[str, Any]:
    detail = detail or {}
    interact = extract_interact_info(detail)
    return {
        "post_title": stringify(first_value(detail, POST_FIELD_PATHS["post_title"]) or search_item.get("title")),
        "post_content": stringify(first_value(detail, POST_FIELD_PATHS["post_content"])),
        "post_type": stringify(first_value(detail, POST_FIELD_PATHS["post_type"]) or search_item.get("type")),
        "liked_count": parse_count(interact.get("likedCount") or interact.get("liked_count") or search_item.get("liked_count")),
        "collected_count": parse_count(
            interact.get("collectedCount") or interact.get("collected_count") or search_item.get("collected_count")
        ),
        "comment_count": parse_count(interact.get("commentCount") or interact.get("comment_count") or search_item.get("comment_count")),
    }


def comment_text_from_item(item: Dict[str, Any]) -> str:
    return clean_comment_text(
        first_value(
            item,
            [
                ("content",),
                ("text",),
                ("comment",),
                ("commentContent",),
                ("content", "text"),
                ("content", "value"),
            ],
        )
    )


def is_comment_like_item(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    if comment_text_from_item(item):
        keys = set(item.keys())
        comment_markers = {
            "commentId",
            "comment_id",
            "likeCount",
            "likedCount",
            "subComments",
            "userInfo",
            "user",
            "author",
        }
        return bool(keys & comment_markers)
    return False


def flatten_comment_candidates(value: Any) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    if isinstance(value, list):
        if value and all(is_comment_like_item(item) for item in value if isinstance(item, dict)):
            for item in value:
                if isinstance(item, dict):
                    found.append(item)
                    for nested_key in ("subComments", "sub_comments", "replies", "replyComments"):
                        found.extend(flatten_comment_candidates(item.get(nested_key)))
            return found
        for item in value:
            found.extend(flatten_comment_candidates(item))
    elif isinstance(value, dict):
        if is_comment_like_item(value):
            found.append(value)
        for item in value.values():
            found.extend(flatten_comment_candidates(item))
    return found


def extract_comments(detail: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not detail:
        return []
    candidates = flatten_comment_candidates(detail)
    deduped: List[Dict[str, Any]] = []
    seen_ids = set()
    for item in candidates:
        comment_id = stringify(first_value(item, [("id",), ("commentId",), ("comment_id",)]))
        key = comment_id or normalize_for_dedupe(comment_text_from_item(item))
        if key and key not in seen_ids:
            deduped.append(item)
            seen_ids.add(key)
    return deduped


def clean_comments(raw_comments: List[Dict[str, Any]], max_comments: int, stats: FilterStats) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    seen_text = set()
    for item in raw_comments:
        text = comment_text_from_item(item)
        if not text:
            stats.filtered_empty_comments += 1
            continue
        dedupe_key = normalize_for_dedupe(text)
        if dedupe_key in seen_text:
            stats.filtered_duplicate_comments += 1
            continue
        if is_short_noise(text):
            stats.filtered_short_comments += 1
            continue
        if is_ad_comment(text):
            stats.filtered_ad_comments += 1
            continue

        seen_text.add(dedupe_key)
        cleaned.append(item)
        if max_comments > 0 and len(cleaned) >= max_comments:
            break
    return cleaned


def make_source_url(feed_id: str, xsec_token: str, xsec_source: str = "pc_search") -> str:
    token = quote(xsec_token or "")
    return f"https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={token}&xsec_source={xsec_source}"


def comment_id_from_item(item: Dict[str, Any], index: int) -> str:
    value = first_value(item, [("id",), ("commentId",), ("comment_id",)])
    return stringify(value) or f"comment_{index + 1}"


def comment_like_count(item: Dict[str, Any]) -> int:
    value = first_value(item, [("likeCount",), ("likedCount",), ("like_count",), ("interactInfo", "likedCount")])
    return parse_count(value)


class DemandDiscoveryCollector:
    def __init__(
        self,
        *,
        keywords: List[str],
        days: int = 3,
        search_publish_time: str = "一周内",
        sort_by: str = "最多评论",
        note_type: str = "不限",
        posts_per_keyword: int = 3,
        search_limit: int = 8,
        max_comments: int = 20,
        output_dir: Optional[str] = None,
        timezone_name: str = "Asia/Shanghai",
        headless: bool = True,
        cookie_path: str = DEFAULT_COOKIE_PATH,
    ):
        self.keywords = keywords
        self.days = days
        self.search_publish_time = search_publish_time
        self.sort_by = sort_by
        self.note_type = note_type
        self.posts_per_keyword = posts_per_keyword
        self.search_limit = search_limit
        self.max_comments = max_comments
        self.timezone_name = timezone_name
        self.headless = headless
        self.cookie_path = cookie_path
        self.output_dir = Path(output_dir) if output_dir else default_output_dir(timezone_name)
        self.filter_stats = FilterStats()
        self.keyword_stats: Dict[str, KeywordStats] = {keyword: KeywordStats() for keyword in keywords}
        self.errors: List[Dict[str, str]] = []
        self.publish_time_unknown_count = 0

    def run(self) -> Dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        started_at = now_in_timezone(self.timezone_name)
        collected_at = started_at.isoformat()

        notes_path = self.output_dir / "notes_clean.jsonl"
        comments_path = self.output_dir / "comments_clean.jsonl"

        client = XiaohongshuClient(headless=self.headless, cookie_path=self.cookie_path)
        try:
            client.start()
            is_logged_in, username = LoginAction(client).check_login_status(navigate=True)
            if not is_logged_in:
                error = {
                    "type": "LoginRequired",
                    "message": "Not logged in or cookie expired. Run qrcode/login manually, then retry.",
                }
                self.errors.append(error)
                summary = self._build_summary(started_at, now_in_timezone(self.timezone_name))
                self._write_summary_and_report(summary, notes_path, comments_path)
                return {"status": "error", "output_dir": str(self.output_dir), "summary": summary}

            print(f"Login check passed: {username or 'logged in'}", file=sys.stderr)
            search_action = SearchAction(client)
            feed_action = FeedDetailAction(client)

            with open(notes_path, "w", encoding="utf-8") as notes_fp, open(comments_path, "w", encoding="utf-8") as comments_fp:
                for keyword in self.keywords:
                    self._collect_keyword(keyword, search_action, feed_action, notes_fp, comments_fp, collected_at)

            summary = self._build_summary(started_at, now_in_timezone(self.timezone_name))
            self._write_summary_and_report(summary, notes_path, comments_path)
            return {"status": "success", "output_dir": str(self.output_dir), "summary": summary}
        except CaptchaError as exc:
            self.errors.append({"type": "CaptchaError", "message": str(exc), "captcha_url": exc.captcha_url})
            summary = self._build_summary(started_at, now_in_timezone(self.timezone_name))
            self._write_summary_and_report(summary, notes_path, comments_path)
            raise
        finally:
            client.close()

    def _collect_keyword(self, keyword, search_action, feed_action, notes_fp, comments_fp, collected_at):
        stats = self.keyword_stats[keyword]
        try:
            results = search_action.search(
                keyword=keyword,
                sort_by=self.sort_by,
                note_type=self.note_type,
                publish_time=self.search_publish_time,
                limit=self.search_limit,
            )
            stats.search_results = len(results)
        except Exception as exc:
            self._record_keyword_error(keyword, "SearchError", exc)
            return

        saved_for_keyword = 0
        cutoff = now_in_timezone(self.timezone_name) - timedelta(days=self.days)

        for item in results:
            if saved_for_keyword >= self.posts_per_keyword:
                break

            feed_id = stringify(item.get("id") or item.get("feed_id"))
            xsec_token = stringify(item.get("xsec_token") or item.get("xsecToken"))
            if not feed_id:
                self._record_keyword_error(keyword, "MissingFeedId", "Search result did not include id/feed_id")
                continue

            stats.notes_seen += 1
            source_url = make_source_url(feed_id, xsec_token, "pc_search")

            try:
                detail = feed_action.get_feed_detail(
                    feed_id=feed_id,
                    xsec_token=xsec_token,
                    load_comments=True,
                    max_comments=self.max_comments,
                    xsec_source="pc_search",
                )
                if not detail:
                    raise RuntimeError("No detail returned")
            except Exception as exc:
                self._record_note_error(keyword, feed_id, source_url, item, notes_fp, collected_at, exc)
                continue

            publish_time, publish_time_status, parsed_publish_time = extract_publish_time(detail, self.timezone_name)
            if publish_time_status == "publish_time_unknown":
                stats.publish_time_unknown += 1
                self.publish_time_unknown_count += 1

            post_data = extract_post_data(detail, item)
            raw_comments = extract_comments(detail)
            stats.comments_raw += len(raw_comments)

            if parsed_publish_time and parsed_publish_time < cutoff:
                json_dump_line(
                    notes_fp,
                    self._note_row(
                        keyword,
                        feed_id,
                        source_url,
                        post_data,
                        publish_time,
                        publish_time_status,
                        raw_comment_count=len(raw_comments),
                        valid_comment_count=0,
                        collected_at=collected_at,
                        status="skipped_old",
                        error="outside_recent_days_window",
                    ),
                )
                continue

            cleaned_comments = clean_comments(raw_comments, self.max_comments, self.filter_stats)
            stats.comments_saved += len(cleaned_comments)
            stats.notes_saved += 1
            saved_for_keyword += 1

            json_dump_line(
                notes_fp,
                self._note_row(
                    keyword,
                    feed_id,
                    source_url,
                    post_data,
                    publish_time,
                    publish_time_status,
                    raw_comment_count=len(raw_comments),
                    valid_comment_count=len(cleaned_comments),
                    collected_at=collected_at,
                    status="collected",
                    error="",
                ),
            )

            for index, comment in enumerate(cleaned_comments):
                json_dump_line(
                    comments_fp,
                    self._comment_row(
                        keyword,
                        feed_id,
                        source_url,
                        post_data,
                        publish_time,
                        publish_time_status,
                        comment,
                        index,
                        collected_at,
                    ),
                )

    def _record_keyword_error(self, keyword: str, error_type: str, exc: Any):
        error = {"keyword": keyword, "type": error_type, "message": str(exc)}
        self.keyword_stats[keyword].errors.append(error)
        self.errors.append(error)

    def _record_note_error(self, keyword, feed_id, source_url, search_item, notes_fp, collected_at, exc):
        self._record_keyword_error(keyword, "FeedDetailError", f"{feed_id}: {exc}")
        post_data = extract_post_data(None, search_item)
        json_dump_line(
            notes_fp,
            self._note_row(
                keyword,
                feed_id,
                source_url,
                post_data,
                "",
                "publish_time_unknown",
                raw_comment_count=0,
                valid_comment_count=0,
                collected_at=collected_at,
                status="error",
                error=str(exc),
            ),
        )

    def _note_row(
        self,
        keyword,
        feed_id,
        source_url,
        post_data,
        publish_time,
        publish_time_status,
        raw_comment_count,
        valid_comment_count,
        collected_at,
        status,
        error,
    ) -> Dict[str, Any]:
        return {
            "platform": PLATFORM,
            "source_type": DEFAULT_SOURCE_TYPE,
            "keyword": keyword,
            "source_url": source_url,
            "post_id": feed_id,
            "post_title": post_data["post_title"],
            "post_content": post_data["post_content"],
            "post_type": post_data["post_type"],
            "publish_time": publish_time,
            "publish_time_status": publish_time_status,
            "liked_count": post_data["liked_count"],
            "collected_count": post_data["collected_count"],
            "comment_count": post_data["comment_count"],
            "valid_comment_count": valid_comment_count,
            "raw_comment_count": raw_comment_count,
            "collected_at": collected_at,
            "status": status,
            "error": error,
        }

    def _comment_row(
        self,
        keyword,
        feed_id,
        source_url,
        post_data,
        publish_time,
        publish_time_status,
        comment,
        index,
        collected_at,
    ) -> Dict[str, Any]:
        return {
            "platform": PLATFORM,
            "source_type": DEFAULT_SOURCE_TYPE,
            "keyword": keyword,
            "source_url": source_url,
            "post_id": feed_id,
            "post_title": post_data["post_title"],
            "post_content": post_data["post_content"],
            "post_type": post_data["post_type"],
            "publish_time": publish_time,
            "publish_time_status": publish_time_status,
            "liked_count": post_data["liked_count"],
            "collected_count": post_data["collected_count"],
            "comment_count": post_data["comment_count"],
            "comment_id": comment_id_from_item(comment, index),
            "comment_text": comment_text_from_item(comment),
            "comment_like_count": comment_like_count(comment),
            "author_hash": stable_author_hash(extract_author_seed(comment)),
            "collected_at": collected_at,
        }

    def _build_summary(self, started_at: datetime, finished_at: datetime) -> Dict[str, Any]:
        total_search_results = sum(item.search_results for item in self.keyword_stats.values())
        total_notes_seen = sum(item.notes_seen for item in self.keyword_stats.values())
        total_notes_saved = sum(item.notes_saved for item in self.keyword_stats.values())
        total_comments_raw = sum(item.comments_raw for item in self.keyword_stats.values())
        total_comments_saved = sum(item.comments_saved for item in self.keyword_stats.values())
        return {
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "timezone": self.timezone_name,
            "keywords": self.keywords,
            "total_keywords": len(self.keywords),
            "total_search_results": total_search_results,
            "total_notes_seen": total_notes_seen,
            "total_notes_saved": total_notes_saved,
            "total_comments_raw": total_comments_raw,
            "total_comments_saved": total_comments_saved,
            "filtered_empty_comments": self.filter_stats.filtered_empty_comments,
            "filtered_duplicate_comments": self.filter_stats.filtered_duplicate_comments,
            "filtered_short_comments": self.filter_stats.filtered_short_comments,
            "filtered_ad_comments": self.filter_stats.filtered_ad_comments,
            "publish_time_unknown_count": self.publish_time_unknown_count,
            "errors": self.errors,
            "per_keyword": {
                keyword: {
                    "search_results": stats.search_results,
                    "notes_seen": stats.notes_seen,
                    "notes_saved": stats.notes_saved,
                    "comments_raw": stats.comments_raw,
                    "comments_saved": stats.comments_saved,
                    "publish_time_unknown": stats.publish_time_unknown,
                    "errors": stats.errors,
                }
                for keyword, stats in self.keyword_stats.items()
            },
            "params": {
                "days": self.days,
                "search_publish_time": self.search_publish_time,
                "sort_by": self.sort_by,
                "note_type": self.note_type,
                "posts_per_keyword": self.posts_per_keyword,
                "search_limit": self.search_limit,
                "max_comments": self.max_comments,
                "xsec_source": "pc_search",
            },
        }

    def _write_summary_and_report(self, summary: Dict[str, Any], notes_path: Path, comments_path: Path):
        summary_path = self.output_dir / "collection_summary.json"
        report_path = self.output_dir / "collector_report.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(build_report(summary, self.output_dir, notes_path, comments_path))


def build_report(summary: Dict[str, Any], output_dir: Path, notes_path: Path, comments_path: Path) -> str:
    lines = [
        "# Xiaohongshu Demand Discovery Collector Report",
        "",
        "## Collection Parameters",
        f"- Started at: {summary.get('started_at')}",
        f"- Finished at: {summary.get('finished_at')}",
        f"- Timezone: {summary.get('timezone')}",
        f"- Keywords: {', '.join(summary.get('keywords', []))}",
    ]
    for key, value in summary.get("params", {}).items():
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Totals",
            f"- Search results: {summary.get('total_search_results', 0)}",
            f"- Notes seen: {summary.get('total_notes_seen', 0)}",
            f"- Notes saved: {summary.get('total_notes_saved', 0)}",
            f"- Raw comments: {summary.get('total_comments_raw', 0)}",
            f"- Saved comments: {summary.get('total_comments_saved', 0)}",
            f"- Publish time unknown: {summary.get('publish_time_unknown_count', 0)}",
            "",
            "## Per Keyword",
        ]
    )

    for keyword, stats in summary.get("per_keyword", {}).items():
        lines.append(
            f"- {keyword}: {stats.get('notes_saved', 0)} notes, "
            f"{stats.get('comments_saved', 0)} comments, "
            f"{stats.get('search_results', 0)} search results"
        )

    lines.extend(["", "## Cleaning Filters"])
    for key in [
        "filtered_empty_comments",
        "filtered_duplicate_comments",
        "filtered_short_comments",
        "filtered_ad_comments",
    ]:
        lines.append(f"- {key}: {summary.get(key, 0)}")

    lines.extend(["", "## Errors And Safety"])
    errors = summary.get("errors", [])
    if errors:
        for error in errors:
            lines.append(f"- {error.get('type', 'Error')}: {error.get('message', '')}")
    else:
        lines.append("- No login, captcha, or collection errors were recorded.")

    lines.extend(
        [
            "",
            "## Output Files",
            f"- Output directory: {output_dir}",
            f"- Notes JSONL: {notes_path}",
            f"- Comments JSONL: {comments_path}",
            f"- Summary JSON: {output_dir / 'collection_summary.json'}",
            f"- Report: {output_dir / 'collector_report.md'}",
            "",
            "## Next Steps",
            "- Spot-check a few notes with publish_time_unknown to see whether Xiaohongshu changed its detail fields.",
            "- Review filtered comments before using the dataset for demand analysis.",
            "- Keep batch sizes conservative if captcha or login errors appear.",
        ]
    )
    return "\n".join(lines) + "\n"


def collect_demand_discovery(
    *,
    keywords: Optional[str] = None,
    keywords_file: Optional[str] = None,
    days: int = 3,
    search_publish_time: str = "一周内",
    sort_by: str = "最多评论",
    note_type: str = "不限",
    posts_per_keyword: int = 3,
    search_limit: int = 8,
    max_comments: int = 20,
    output_dir: Optional[str] = None,
    timezone_name: str = "Asia/Shanghai",
    headless: bool = True,
    cookie_path: str = DEFAULT_COOKIE_PATH,
) -> Dict[str, Any]:
    keyword_list = load_keywords(keywords, keywords_file)
    collector = DemandDiscoveryCollector(
        keywords=keyword_list,
        days=days,
        search_publish_time=search_publish_time,
        sort_by=sort_by,
        note_type=note_type,
        posts_per_keyword=posts_per_keyword,
        search_limit=search_limit,
        max_comments=max_comments,
        output_dir=output_dir,
        timezone_name=timezone_name,
        headless=headless,
        cookie_path=cookie_path,
    )
    return collector.run()
