#!/usr/bin/env python3
import argparse
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_TIMEOUT = 20
DEFAULT_USER_AGENT = "Mozilla/5.0"
DEFAULT_API_BASE = "https://api.zsxq.com"
DEFAULT_API_RETRIES = 3
DEFAULT_API_RETRY_DELAY = 1.0
MAX_COUNT = 30
ELLIPSIS_RE = re.compile(r"(\.\.\.|……|\u2026)$")


class SessionError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def load_json(path: Path):
    if not path.exists():
        raise SessionError("TOKEN_MISSING", f"session token file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SessionError("TOKEN_INVALID", f"failed to parse token file: {e}")


def load_generic_json(path: Path, default: Any = None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_token_file(path: Path):
    data = load_json(path)
    if not isinstance(data, dict):
        raise SessionError("TOKEN_INVALID", "token file must be a JSON object")
    kind = data.get("kind")
    cookie_name = data.get("cookie_name")
    cookie_value = data.get("cookie_value")
    if kind != "cookie":
        raise SessionError("TOKEN_INVALID", "only cookie-based token files are supported in MVP")
    if not cookie_name or not cookie_value:
        raise SessionError("TOKEN_INVALID", "cookie_name and cookie_value are required")
    return {
        "kind": kind,
        "cookie_name": str(cookie_name),
        "cookie_value": str(cookie_value),
        "domain": str(data.get("domain", ".zsxq.com")),
        "user_agent": str(data.get("user_agent", DEFAULT_USER_AGENT)),
        "captured_at": data.get("captured_at"),
        "source": data.get("source"),
    }


def build_request(url: str, token_info: dict):
    headers = {
        "Cookie": f"{token_info['cookie_name']}={token_info['cookie_value']}",
        "User-Agent": token_info.get("user_agent") or DEFAULT_USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://wx.zsxq.com/",
        "Origin": "https://wx.zsxq.com",
    }
    return urllib.request.Request(url, headers=headers, method="GET")


def fetch_url(url: str, token_info: dict, timeout: int):
    request = build_request(url, token_info)
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            status_code = getattr(response, "status", 200)
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            return status_code, content_type, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        if e.code == 401:
            raise SessionError("TOKEN_EXPIRED", f"unauthorized: {body[:300]}")
        if e.code == 403:
            raise SessionError("ACCESS_DENIED", f"forbidden: {body[:300]}")
        raise SessionError("QUERY_FAILED", f"http {e.code}: {body[:300]}")
    except urllib.error.URLError as e:
        raise SessionError("QUERY_FAILED", f"network error: {e}")


def parse_json_response(body: str):
    try:
        return json.loads(body)
    except Exception as e:
        raise SessionError("QUERY_FAILED", f"response is not valid JSON: {e}")


def classify_api_error(code: Any, info: Any) -> str:
    text = str(info or "")
    if code in (401, 4010, 4011) or any(token_hint in text for token_hint in ("未登录", "登录已失效", "登录失效", "请先登录")):
        return "TOKEN_EXPIRED"
    if code in (403, 4030, 4031, 1005) or any(access_hint in text for access_hint in ("不是星球成员", "无权限", "没有权限", "已退出")):
        return "ACCESS_DENIED"
    return "QUERY_FAILED"


def extract_resp_data(payload: dict):
    if not isinstance(payload, dict):
        raise SessionError("QUERY_FAILED", "response payload must be a JSON object")
    if payload.get("succeeded") is True:
        return payload.get("resp_data")
    code = payload.get("code")
    info = payload.get("info") or payload.get("error") or "unknown error"
    status = classify_api_error(code, info)
    if status == "TOKEN_EXPIRED":
        raise SessionError("TOKEN_EXPIRED", f"api unauthorized: {info}")
    if status == "ACCESS_DENIED":
        raise SessionError("ACCESS_DENIED", f"api forbidden: {info}")
    raise SessionError("QUERY_FAILED", f"api error code={code}: {info}")


def should_retry_transient_error(error: SessionError) -> bool:
    if error.status != "QUERY_FAILED":
        return False
    message = str(error.message or "")
    transient_markers = (
        "code=1059",
        "内部错误",
        "EOF occurred in violation of protocol",
        "SSL:",
        "tlsv",
        "Connection reset by peer",
    )
    return any(marker in message for marker in transient_markers)


def api_get(path: str, token_info: dict, timeout: int, api_base: str, retries: int = DEFAULT_API_RETRIES, retry_delay: float = DEFAULT_API_RETRY_DELAY):
    url = urllib.parse.urljoin(api_base.rstrip("/") + "/", path.lstrip("/"))
    last_error: Optional[SessionError] = None
    attempts = max(1, retries)
    for attempt in range(attempts):
        try:
            status_code, content_type, body = fetch_url(url, token_info, timeout)
            if "json" not in content_type.lower() and not body.strip().startswith("{"):
                raise SessionError("QUERY_FAILED", f"unexpected content type {content_type!r}")
            payload = parse_json_response(body)
            resp_data = extract_resp_data(payload)
            return url, resp_data
        except SessionError as e:
            last_error = e
            if attempt + 1 >= attempts or not should_retry_transient_error(e):
                raise
            time.sleep(max(0.0, retry_delay) * (attempt + 1))
    if last_error is not None:
        raise last_error
    raise SessionError("QUERY_FAILED", "unknown api_get failure")


def summarize_probe(status_code: int, content_type: str, body: str):
    trimmed = body[:800]
    return {
        "status": "ok",
        "http_status": status_code,
        "content_type": content_type,
        "body_preview": trimmed,
    }


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def coerce_int(value: Any) -> int:
    if value in (None, "", False):
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value).strip().replace(",", "")
    if not text:
        return 0
    match = re.search(r"-?\d+", text)
    if not match:
        return 0
    try:
        return int(match.group(0))
    except Exception:
        return 0


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, "", 0, "0", "false", "False", "no", "No"):
        return False
    return bool(value)


def get_block(topic: dict, key: str) -> dict:
    block = topic.get(key)
    return block if isinstance(block, dict) else {}


def first_text(*values: Any) -> str:
    for value in values:
        if not value:
            continue
        text = clean_text(value)
        if text:
            return text
    return ""


def extract_named_texts(block: dict, keys: List[str]) -> List[str]:
    texts: List[str] = []
    for key in keys:
        value = block.get(key)
        if not value:
            continue
        if isinstance(value, str):
            text = clean_text(value)
            if text:
                texts.append(text)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    text = clean_text(item)
                    if text:
                        texts.append(text)
                elif isinstance(item, dict):
                    for nested_key in ("text", "content", "description", "title"):
                        nested_val = item.get(nested_key)
                        nested_text = clean_text(nested_val)
                        if nested_text:
                            texts.append(nested_text)
                            break
    return texts


def topic_blocks(topic: dict) -> List[dict]:
    return [block for block in (get_block(topic, "question"), get_block(topic, "talk"), get_block(topic, "solution"), get_block(topic, "task")) if block]


def topic_full_text(topic: dict) -> Tuple[str, bool]:
    full_texts: List[str] = []
    preview_texts: List[str] = []
    for block in topic_blocks(topic):
        full_texts.extend(extract_named_texts(block, ["text", "content", "description", "answer", "summary"]))
        preview_texts.extend(extract_named_texts(block, ["text_preview", "preview"]))
    if full_texts:
        return "\n\n".join(full_texts), False
    if preview_texts:
        return "\n\n".join(preview_texts), True
    title = first_text(topic.get("title"))
    return title, not bool(title)


def topic_preview_text(topic: dict, full_text: str) -> str:
    previews: List[str] = []
    for block in topic_blocks(topic):
        previews.extend(extract_named_texts(block, ["text_preview", "preview", "summary"]))
    if previews:
        return "\n\n".join(previews)
    return clean_text(full_text)[:280]


def topic_text(topic: dict) -> str:
    full_text, _ = topic_full_text(topic)
    return clean_text(full_text)


def topic_author(topic: dict) -> str:
    q = topic.get("question")
    if isinstance(q, dict):
        owner = q.get("owner")
        if isinstance(owner, dict) and owner.get("name"):
            return str(owner.get("name"))
    for block in topic_blocks(topic):
        owner = block.get("owner")
        if isinstance(owner, dict) and owner.get("name"):
            return str(owner.get("name"))
    owner = topic.get("owner")
    if isinstance(owner, dict):
        return str(owner.get("name") or "")
    return ""


def extract_flag(topic: dict, keys: List[str]) -> bool:
    for key in keys:
        if truthy(topic.get(key)):
            return True
    for block in topic_blocks(topic):
        for key in keys:
            if truthy(block.get(key)):
                return True
    return False


def detect_has_images(topic: dict) -> bool:
    image_keys = ("images", "image_list", "pictures", "files")
    for key in image_keys:
        value = topic.get(key)
        if isinstance(value, list) and value:
            return True
    for block in topic_blocks(topic):
        for key in image_keys:
            value = block.get(key)
            if isinstance(value, list) and value:
                return True
    return False


def detect_has_links(topic: dict, text: str) -> bool:
    if re.search(r"https?://", text):
        return True
    url_keys = ("url", "article_url", "source_url", "link_url")
    for key in url_keys:
        value = topic.get(key)
        if isinstance(value, str) and value:
            return True
    for block in topic_blocks(topic):
        for key in url_keys:
            value = block.get(key)
            if isinstance(value, str) and value:
                return True
    return False


def classify_topic(topic: dict) -> str:
    text = topic_text(topic)
    if isinstance(topic.get("question"), dict) or topic.get("type") in ("q&a", "question"):
        return "qa"
    if isinstance(topic.get("task"), dict):
        return "event"
    if isinstance(topic.get("solution"), dict):
        return "resource"
    if any(word in text for word in ("框架", "策略", "模型", "回测", "数据集", "研报", "分析", "逻辑", "规章", "变化")):
        return "analysis"
    if isinstance(topic.get("talk"), dict):
        return "chat"
    return "other"


def infer_signals(text: str) -> List[str]:
    mapping = [
        ("original-analysis", ["框架", "策略", "模型", "回测", "分析", "研判", "逻辑", "观察", "规章", "变化"]),
        ("tool-release", ["工具", "模板", "代码", "脚本", "数据集", "开源", "书单", "推荐"]),
        ("deadline", ["截止", "今晚", "本周", "直播", "招募", "报名", "更新", "开播"]),
    ]
    signals = []
    for signal, keywords in mapping:
        if any(word in text for word in keywords):
            signals.append(signal)
    return signals


def decide_priority(text: str, guessed_type: str) -> Tuple[str, str, str]:
    low_words = ["早安", "打卡", "签到", "闲聊", "路过", "分享一下"]
    if any(word in text for word in low_words):
        return "low", "skip", "偏日常交流，当前点击优先级较低"

    signals = infer_signals(text)
    if guessed_type in ("analysis", "resource") or "original-analysis" in signals or "tool-release" in signals:
        return "high", "open-now", "包含方法、框架或资源线索，值得优先点开"
    if guessed_type in ("event", "qa") or "deadline" in signals:
        return "medium", "read-later", "可能涉及答疑、活动或时间信息，建议补看"
    return "medium", "read-later", "先保留在摘要中，必要时再展开原文"


def engagement_hint(topic: dict) -> dict:
    comments = coerce_int(topic.get("comments_count"))
    likes = coerce_int(topic.get("likes_count"))
    return {"likes": likes, "comments": comments}


def detect_is_truncated(text: str, preview: str, preview_only: bool) -> bool:
    if preview_only:
        return True
    if ELLIPSIS_RE.search(clean_text(preview)):
        return True
    if any(marker in clean_text(text) for marker in ("查看详情", "展开全文", "下略")):
        return True
    return False


def detect_source_confidence(preview_only: bool, detail_chars: int, is_truncated: bool) -> str:
    if not preview_only and detail_chars >= 400 and not is_truncated:
        return "high"
    if detail_chars >= 120:
        return "medium"
    return "low"


def build_detail_excerpt(text: str) -> str:
    return clean_text(text)[:1200]


def normalize_topic(topic: dict, group_name: str) -> dict:
    full_text, preview_only = topic_full_text(topic)
    full_text = clean_text(full_text)
    preview = clean_text(topic_preview_text(topic, full_text))
    text = full_text or preview
    excerpt = build_detail_excerpt(text)
    topic_id = topic.get("topic_id")
    guessed_type = classify_topic(topic)
    signals = infer_signals(text)
    priority, suggested_action, why_it_matters = decide_priority(text, guessed_type)
    is_truncated = detect_is_truncated(text, preview, preview_only)
    detail_chars = len(excerpt)
    source_confidence = detect_source_confidence(preview_only, detail_chars, is_truncated)
    title = first_text(topic.get("title"), preview.splitlines()[0] if preview else "", text.splitlines()[0] if text else "") or "（无标题）"
    is_question = isinstance(topic.get("question"), dict) or "？" in text or "?" in text
    is_answer = isinstance(topic.get("solution"), dict)
    is_elite = extract_flag(topic, ["is_elite", "elite", "is_digest", "digest"])
    is_pinned = extract_flag(topic, ["is_pinned", "pinned", "sticky", "top", "is_top"])

    return {
        "item_id": str(topic_id) if topic_id is not None else None,
        "circle_name": group_name or (topic.get("group") or {}).get("name") or "未分类星球",
        "author": topic_author(topic),
        "published_at": topic.get("create_time"),
        "title_or_hook": title[:160],
        "content_preview": (preview or excerpt)[:280],
        "detail_excerpt": excerpt,
        "detail_truncated": is_truncated,
        "detail_chars": detail_chars,
        "content_type": guessed_type,
        "guessed_type": guessed_type,
        "engagement_hint": engagement_hint(topic),
        "signals": signals,
        "priority": priority,
        "why_it_matters": why_it_matters,
        "suggested_action": suggested_action,
        "url": f"https://wx.zsxq.com/topic/{topic_id}" if topic_id is not None else "",
        "raw_topic_id": topic_id,
        "source_mode": "token",
        "source_confidence": source_confidence,
        "is_truncated": is_truncated,
        "is_question": is_question,
        "is_answer": is_answer,
        "is_elite": is_elite,
        "is_pinned": is_pinned,
        "has_images": detect_has_images(topic),
        "has_links": detect_has_links(topic, text),
    }


def normalize_group(group: dict) -> dict:
    return {
        "group_id": group.get("group_id"),
        "name": group.get("name"),
        "description": group.get("description"),
    }


def list_groups(token_info: dict, timeout: int, api_base: str):
    url, data = api_get("/v2/groups", token_info, timeout, api_base)
    groups = data.get("groups", []) if isinstance(data, dict) else []
    normalized = [normalize_group(group) for group in groups if isinstance(group, dict)]
    if not normalized:
        raise SessionError("EMPTY_RESULT", "group list is empty or unavailable")
    return {
        "status": "ok",
        "access_mode": "token",
        "kind": "groups",
        "url": url,
        "count": len(normalized),
        "groups": normalized,
    }


def group_topics(group_id: str, scope: str, count: int, token_info: dict, timeout: int, api_base: str):
    count = min(max(count, 1), MAX_COUNT)
    group_url, group_data = api_get(f"/v2/groups/{group_id}", token_info, timeout, api_base)
    group = group_data.get("group", {}) if isinstance(group_data, dict) else {}
    group_name = group.get("name") or str(group_id)
    topics_url, topics_data = api_get(
        f"/v2/groups/{group_id}/topics?scope={urllib.parse.quote(scope)}&count={count}",
        token_info,
        timeout,
        api_base,
    )
    topics = topics_data.get("topics", []) if isinstance(topics_data, dict) else []
    items = [normalize_topic(topic, group_name) for topic in topics if isinstance(topic, dict)]
    if not items:
        raise SessionError("EMPTY_RESULT", f"no topics returned for group {group_id}")
    return {
        "status": "ok",
        "access_mode": "token",
        "kind": "group_topics",
        "group": {
            "group_id": group.get("group_id", group_id),
            "name": group_name,
            "description": group.get("description"),
            "info_url": group_url,
        },
        "topics_url": topics_url,
        "count": len(items),
        "items": items,
    }


def load_group_targets(group_ids: List[str], groups_file: str, exclude_group_ids: List[str]) -> List[Tuple[str, str]]:
    exclude_set = {str(group_id) for group_id in exclude_group_ids}
    inactive_statuses = {"expired", "disabled", "archived", "ignore", "ignored", "removed"}
    targets: List[Tuple[str, str]] = []
    for group_id in group_ids:
        group_id = str(group_id)
        if group_id in exclude_set:
            continue
        targets.append((group_id, group_id))
    if groups_file:
        data = load_generic_json(Path(groups_file), default=[])
        if not isinstance(data, list):
            raise SessionError("QUERY_FAILED", "groups file must be a JSON array")
        for item in data:
            if isinstance(item, dict):
                group_id = item.get("group_id")
                if not group_id:
                    continue
                group_id = str(group_id)
                status = str(item.get("status") or "").strip().lower()
                enabled = item.get("enabled", True)
                if group_id in exclude_set or enabled is False or status in inactive_statuses:
                    continue
                targets.append((group_id, str(item.get("name") or group_id)))
            elif item:
                group_id = str(item)
                if group_id in exclude_set:
                    continue
                targets.append((group_id, group_id))
    deduped = []
    seen = set()
    for group_id, label in targets:
        if group_id in seen:
            continue
        seen.add(group_id)
        deduped.append((group_id, label))
    return deduped


def multi_group_topics(group_ids: List[str], groups_file: str, exclude_group_ids: List[str], scope: str, count: int, token_info: dict, timeout: int, api_base: str):
    targets = load_group_targets(group_ids, groups_file, exclude_group_ids)
    if not targets:
        raise SessionError("QUERY_FAILED", "provide at least one active target via --group-id or --groups-file")
    groups = []
    items = []
    skipped_groups = []
    for group_id, label in targets:
        try:
            result = group_topics(group_id, scope, count, token_info, timeout, api_base)
            groups.append(result["group"])
            items.extend(result["items"])
        except SessionError as e:
            if e.status == "TOKEN_EXPIRED":
                raise
            skipped_groups.append(
                {
                    "group_id": group_id,
                    "name": label,
                    "status": e.status,
                    "message": e.message,
                }
            )
            continue
    if not items:
        if skipped_groups:
            first = skipped_groups[0]
            raise SessionError(first["status"], f"no accessible topics returned; first failure: {first['message']}")
        raise SessionError("EMPTY_RESULT", "no topics returned for requested groups")
    return {
        "status": "PARTIAL_CAPTURE" if skipped_groups else "ok",
        "access_mode": "token",
        "kind": "multi_group_topics",
        "count": len(items),
        "group_count": len(groups),
        "groups": groups,
        "items": items,
        "skipped_count": len(skipped_groups),
        "skipped_groups": skipped_groups,
        "excluded_group_ids": sorted({str(group_id) for group_id in exclude_group_ids}),
    }


def write_output(path: str, data: Dict[str, Any]):
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="MVP ZSXQ session-token collector")
    parser.add_argument("--token-file", required=True, help="Path to state/session.token.json")
    parser.add_argument("--mode", choices=["probe", "groups", "group-topics", "multi-group-topics"], default="probe")
    parser.add_argument("--url", help="Target URL to probe with cookie auth (probe mode)")
    parser.add_argument("--group-id", action="append", default=[], help="Group id for topic collection; repeatable")
    parser.add_argument("--exclude-group-id", action="append", default=[], help="Group id to explicitly skip; repeatable")
    parser.add_argument("--groups-file", help="JSON array of group ids or {group_id,name,enabled,status} objects")
    parser.add_argument("--scope", default="all")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--output", help="Optional path to save result JSON")
    args = parser.parse_args()

    try:
        token_info = load_token_file(Path(args.token_file))
        if args.mode == "probe":
            if not args.url:
                raise SessionError("QUERY_FAILED", "--url is required in probe mode")
            status_code, content_type, body = fetch_url(args.url, token_info, args.timeout)
            result = summarize_probe(status_code, content_type, body)
            result["access_mode"] = "token"
            result["url"] = args.url
            result["token_source"] = token_info.get("source")
        elif args.mode == "groups":
            result = list_groups(token_info, args.timeout, args.api_base)
        elif args.mode == "group-topics":
            if not args.group_id:
                raise SessionError("QUERY_FAILED", "--group-id is required in group-topics mode")
            result = group_topics(args.group_id[0], args.scope, args.count, token_info, args.timeout, args.api_base)
        else:
            result = multi_group_topics(
                args.group_id,
                args.groups_file,
                args.exclude_group_id,
                args.scope,
                args.count,
                token_info,
                args.timeout,
                args.api_base,
            )

        result["token_source"] = token_info.get("source")
        if args.output:
            write_output(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SessionError as e:
        print(
            json.dumps(
                {
                    "status": e.status,
                    "message": e.message,
                    "access_mode": "token",
                    "mode": args.mode,
                    "url": args.url,
                    "group_id": args.group_id,
                    "groups_file": args.groups_file,
                    "exclude_group_id": args.exclude_group_id,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(2)


if __name__ == "__main__":
    main()
