#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class BrowserError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def load_json(path: Path):
    if not path.exists():
        raise BrowserError("BROWSER_UNAVAILABLE", f"browser capture file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise BrowserError("QUERY_FAILED", f"failed to parse browser capture: {e}")


def normalize_capture_items(data: Any) -> List[dict]:
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    if not isinstance(data, list):
        raise BrowserError("QUERY_FAILED", "browser capture must be a list or an object with an 'items' array")
    return [item for item in data if isinstance(item, dict)]


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def first_non_empty(item: dict, keys: List[str]) -> str:
    for key in keys:
        value = item.get(key)
        if value:
            text = clean_text(value)
            if text:
                return text
    return ""


def coerce_int(value: Any) -> int:
    if value in (None, "", False):
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value).strip()
    if not text:
        return 0
    text = text.replace(",", "")
    match = re.search(r"-?\d+", text)
    if not match:
        return 0
    try:
        return int(match.group(0))
    except Exception:
        return 0


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, "", 0, "0", "false", "False", "no", "No"):
        return False
    return bool(value)


def title_of(item: dict, text: str) -> str:
    title = first_non_empty(item, ["title_or_hook", "title", "hook"])
    if title:
        return title[:160]
    if text:
        first_line = text.splitlines()[0].strip()
        if first_line:
            return first_line[:160]
    return "（无标题）"


def text_of(item: dict) -> str:
    return first_non_empty(
        item,
        [
            "detail_excerpt",
            "raw_text",
            "content_preview",
            "text",
            "preview",
            "description",
            "summary",
            "title_or_hook",
            "title",
        ],
    )


def preview_of(item: dict, text: str) -> str:
    preview = first_non_empty(item, ["content_preview", "preview", "summary"])
    if preview:
        return preview[:280]
    return text[:280]


def excerpt_of(item: dict, text: str) -> str:
    excerpt = first_non_empty(item, ["detail_excerpt", "raw_text", "text", "content_preview", "preview", "summary"])
    return excerpt[:1200]


def parse_engagement(item: dict) -> Dict[str, int]:
    hint = item.get("engagement_hint") if isinstance(item.get("engagement_hint"), dict) else {}
    return {
        "likes": coerce_int(item.get("likes", hint.get("likes"))),
        "comments": coerce_int(item.get("comments", hint.get("comments"))),
    }


def detect_has_images(item: dict, text: str) -> bool:
    if as_bool(item.get("has_images")):
        return True
    if coerce_int(item.get("image_count")) > 0:
        return True
    images = item.get("images")
    if isinstance(images, list) and len(images) > 0:
        return True
    return "[图片]" in text or "图片" in text and "http" in text


def detect_has_links(item: dict, text: str) -> bool:
    if as_bool(item.get("has_links")):
        return True
    if item.get("url"):
        return True
    links = item.get("links")
    if isinstance(links, list) and len(links) > 0:
        return True
    return bool(re.search(r"https?://", text))


ELLIPSIS_RE = re.compile(r"(\.\.\.|……|\u2026)$")


def detect_is_truncated(item: dict, preview: str, excerpt: str) -> bool:
    explicit = item.get("is_truncated")
    if explicit is not None:
        return as_bool(explicit)
    detail_truncated = item.get("detail_truncated")
    if detail_truncated is not None:
        return as_bool(detail_truncated)
    hint_text = " ".join(
        clean_text(item.get(key))
        for key in ("raw_text", "detail_excerpt", "content_preview")
        if item.get(key)
    )
    if any(marker in hint_text for marker in ("查看详情", "展开全文", "全文", "下略")):
        return True
    if preview and excerpt and len(excerpt) > len(preview) + 40:
        return True
    if ELLIPSIS_RE.search(preview) or ELLIPSIS_RE.search(excerpt):
        return True
    return False


def infer_signals(text: str) -> List[str]:
    mapping = [
        ("original-analysis", ["框架", "策略", "模型", "回测", "分析", "研判", "逻辑", "观察", "高质量发展", "规章", "变化"]),
        ("tool-release", ["工具", "模板", "代码", "脚本", "数据集", "开源", "推荐", "书单", "教程"]),
        ("deadline", ["截止", "今晚", "本周", "直播", "招募", "报名", "更新", "开播"]),
    ]
    signals = []
    for signal, keywords in mapping:
        if any(word in text for word in keywords):
            signals.append(signal)
    return signals


def classify_item(item: dict, text: str) -> str:
    given = item.get("guessed_type") or item.get("content_type")
    if given:
        return str(given)
    if as_bool(item.get("is_question")) or item.get("question") or "？" in text or "?" in text:
        return "qa"
    if any(word in text for word in ("直播", "截止", "报名", "活动", "通知", "开播")):
        return "event"
    if any(word in text for word in ("工具", "模板", "代码", "脚本", "数据集", "开源", "书单", "推荐", "教程")):
        return "resource"
    if any(word in text for word in ("框架", "策略", "模型", "回测", "分析", "研判", "规章", "逻辑", "观察", "高质量发展", "变化", "规划")):
        return "analysis"
    if text:
        return "chat"
    return "other"


def decide_priority(text: str, guessed_type: str) -> List[str]:
    low_words = ["早安", "打卡", "签到", "闲聊", "路过", "分享一下"]
    if any(word in text for word in low_words):
        return ["low", "skip", "偏日常交流，当前点击优先级较低"]

    signals = infer_signals(text)
    if guessed_type in ("analysis", "resource") or "original-analysis" in signals or "tool-release" in signals:
        return ["high", "open-now", "包含方法、框架或资源线索，值得优先点开"]
    if guessed_type in ("event", "qa") or "deadline" in signals:
        return ["medium", "read-later", "可能涉及答疑、活动或时间信息，建议补看"]
    return ["medium", "read-later", "先保留在摘要中，必要时再展开原文"]


def detect_source_confidence(excerpt: str, is_truncated: bool) -> str:
    length = len(excerpt)
    if length >= 400 and not is_truncated:
        return "high"
    if length >= 120:
        return "medium"
    return "low"


def normalize_item(item: dict, default_circle: str) -> dict:
    text = text_of(item)
    excerpt = excerpt_of(item, text)
    preview = preview_of(item, text)
    title = title_of(item, text)
    guessed_type = classify_item(item, text)
    signals = infer_signals(text)
    engagement = parse_engagement(item)
    is_truncated = detect_is_truncated(item, preview, excerpt)
    source_confidence = first_non_empty(item, ["source_confidence"]).lower() or detect_source_confidence(excerpt, is_truncated)
    priority, suggested_action, why_it_matters = decide_priority(text, guessed_type)

    published_at = first_non_empty(item, ["published_at", "create_time", "time"])
    if not published_at:
        published_at = None

    return {
        "item_id": str(item.get("item_id") or item.get("topic_id") or item.get("id") or "") or None,
        "circle_name": first_non_empty(item, ["circle_name", "group_name", "planet"]) or default_circle,
        "author": first_non_empty(item, ["author", "owner"]),
        "published_at": published_at,
        "title_or_hook": title,
        "content_preview": preview,
        "detail_excerpt": excerpt,
        "detail_truncated": is_truncated,
        "detail_chars": len(excerpt),
        "content_type": guessed_type,
        "guessed_type": guessed_type,
        "engagement_hint": engagement,
        "signals": signals,
        "priority": priority,
        "why_it_matters": why_it_matters,
        "suggested_action": suggested_action,
        "url": first_non_empty(item, ["url", "source_url"]),
        "capture_mode": "browser",
        "source_mode": "browser",
        "source_confidence": source_confidence,
        "is_truncated": is_truncated,
        "is_question": as_bool(item.get("is_question")),
        "is_answer": as_bool(item.get("is_answer")),
        "is_elite": as_bool(item.get("is_elite")),
        "is_pinned": as_bool(item.get("is_pinned")),
        "has_images": detect_has_images(item, text),
        "has_links": detect_has_links(item, text),
        "topic_cluster": first_non_empty(item, ["topic_cluster"]),
    }


def write_output(path: str, data: Dict[str, Any]):
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Normalize a browser-captured ZSXQ feed JSON into digest items")
    parser.add_argument("input", help="Path to raw browser capture JSON")
    parser.add_argument("--default-circle", default="未分类星球")
    parser.add_argument("--output", help="Optional path to save normalized JSON")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.input))
        raw_items = normalize_capture_items(data)
        items = [normalize_item(item, args.default_circle) for item in raw_items]
        if not items:
            raise BrowserError("EMPTY_RESULT", "browser capture contains no usable items")
        result = {
            "status": "ok",
            "access_mode": "browser",
            "kind": "browser_capture",
            "count": len(items),
            "items": items,
        }
        if args.output:
            write_output(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except BrowserError as e:
        print(
            json.dumps(
                {
                    "status": e.status,
                    "message": e.message,
                    "access_mode": "browser",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(2)


if __name__ == "__main__":
    main()
