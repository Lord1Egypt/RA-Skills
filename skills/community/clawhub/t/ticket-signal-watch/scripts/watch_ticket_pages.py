#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
ANTI_BOT_PATTERNS = [
    "_____tmd_____",
    "x5secdata",
    "captcha",
    "sessionStorage.x5referer",
]
SIGNAL_ORDER = {"low": 0, "medium": 1, "high": 2}


@dataclass
class Target:
    name: str
    platform: str
    url: str
    require_all: list[str]
    match_any: list[str]
    signal_high: list[str]
    signal_medium: list[str]
    note: str | None = None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def html_to_text(html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_url(url: str, user_agent: str, timeout_seconds: int) -> dict[str, Any]:
    req = Request(
        url,
        headers={
            "User-Agent": user_agent or DEFAULT_USER_AGENT,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    started_at = time.time()
    try:
        with urlopen(req, timeout=timeout_seconds) as resp:
            body = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            html = body.decode(charset, errors="replace")
            return {
                "ok": True,
                "status": getattr(resp, "status", 200),
                "html": html,
                "elapsed_ms": round((time.time() - started_at) * 1000),
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "error": f"HTTP {exc.code}",
            "html": body,
            "elapsed_ms": round((time.time() - started_at) * 1000),
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": None,
            "error": f"URL error: {exc.reason}",
            "html": "",
            "elapsed_ms": round((time.time() - started_at) * 1000),
        }


def normalize_keywords(values: list[str] | None) -> list[str]:
    return [value.strip() for value in (values or []) if value and value.strip()]


def match_keywords(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for keyword in keywords:
        if keyword.lower() in lowered:
            hits.append(keyword)
    return hits


def is_valid_target(raw: dict[str, Any]) -> bool:
    return bool(raw.get("name") and raw.get("platform") and raw.get("url"))


def detect_signal_level(target: Target, positive_hits: list[str]) -> str:
    if any(keyword in positive_hits for keyword in target.signal_high):
        return "high"
    if any(keyword in positive_hits for keyword in target.signal_medium):
        return "medium"
    if positive_hits:
        return "low"
    return "low"


def contains_anti_bot_markers(html: str, text: str) -> bool:
    lowered = f"{html}\n{text}".lower()
    return any(pattern.lower() in lowered for pattern in ANTI_BOT_PATTERNS)


def load_targets(config: dict[str, Any]) -> list[Target]:
    targets: list[Target] = []
    for raw in config.get("targets", []):
        if not is_valid_target(raw):
            continue
        signal_keywords = raw.get("signal_keywords") or {}
        targets.append(
            Target(
                name=raw["name"],
                platform=raw["platform"],
                url=raw["url"],
                require_all=normalize_keywords(raw.get("require_all")),
                match_any=normalize_keywords(raw.get("match_any")),
                signal_high=normalize_keywords(signal_keywords.get("high")),
                signal_medium=normalize_keywords(signal_keywords.get("medium")),
                note=raw.get("note"),
            )
        )
    return targets


def analyze_target(
    target: Target,
    state: dict[str, Any],
    user_agent: str,
    timeout_seconds: int,
    preview_chars: int,
) -> dict[str, Any]:
    fetch = fetch_url(target.url, user_agent=user_agent, timeout_seconds=timeout_seconds)
    html = fetch.get("html", "")
    text = html_to_text(html)
    digest = sha256_text(text)
    require_hits = match_keywords(text, target.require_all)
    positive_hits = match_keywords(text, target.match_any)
    signal_level = detect_signal_level(target, positive_hits)
    anti_bot = contains_anti_bot_markers(html, text)
    prev = state.get(target.url, {})
    prev_hits = set(prev.get("positive_hits", []))
    prev_level = prev.get("signal_level", "low")
    new_hits = [hit for hit in positive_hits if hit not in prev_hits]
    prev_status = prev.get("status")
    status_changed = prev_status != fetch.get("status")
    digest_changed = prev.get("digest") != digest
    require_ready = len(require_hits) == len(target.require_all)
    level_upgraded = SIGNAL_ORDER.get(signal_level, 0) > SIGNAL_ORDER.get(prev_level, 0)

    alert_reasons: list[str] = []
    if anti_bot:
        alert_reasons.append("检测到疑似平台风控/挑战页")
    if new_hits and require_ready:
        alert_reasons.append(f"新增信号词: {', '.join(new_hits)}")
    if level_upgraded and positive_hits and require_ready:
        alert_reasons.append(f"信号等级提升: {prev_level} -> {signal_level}")
    if status_changed and prev_status is not None:
        alert_reasons.append(f"HTTP 状态变化: {prev_status} -> {fetch.get('status')}")
    if digest_changed and positive_hits and require_ready and not new_hits and not level_upgraded:
        alert_reasons.append("页面内容变化，且仍命中关键票务词")

    result = {
        "name": target.name,
        "platform": target.platform,
        "url": target.url,
        "host": urlparse(target.url).netloc,
        "status": fetch.get("status"),
        "ok": fetch.get("ok"),
        "elapsed_ms": fetch.get("elapsed_ms"),
        "require_hits": require_hits,
        "positive_hits": positive_hits,
        "signal_hits": positive_hits,
        "signal_level": signal_level,
        "anti_bot_detected": anti_bot,
        "note": target.note,
        "text_preview": text[:preview_chars],
        "changed": digest_changed,
        "alert_reasons": alert_reasons,
        "error": fetch.get("error"),
    }

    state[target.url] = {
        "name": target.name,
        "platform": target.platform,
        "status": fetch.get("status"),
        "digest": digest,
        "positive_hits": positive_hits,
        "signal_level": signal_level,
        "checked_at": int(time.time()),
    }

    return result


def build_summary(results: list[dict[str, Any]]) -> str:
    alerts = [item for item in results if item["alert_reasons"]]
    if not alerts:
        return "No new ticket alerts."

    lines = ["New ticket signals detected:"]
    for item in alerts:
        lines.append(
            f"- {item['name']} | {item['platform']} | {item['signal_level']} | "
            f"{'; '.join(item['alert_reasons'])} | {item['url']}"
        )
    lines.append("Action: verify on the official app or detail page.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch ticket pages for sale signals.")
    parser.add_argument("--config", required=True, help="Path to targets JSON")
    parser.add_argument("--state", required=True, help="Path to state JSON")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    config_path = Path(args.config)
    state_path = Path(args.state)
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return 2

    config = load_json(config_path)
    state = load_json(state_path) if state_path.exists() else {}
    targets = load_targets(config)
    user_agent = config.get("user_agent") or DEFAULT_USER_AGENT
    timeout_seconds = int(config.get("timeout_seconds") or 12)
    preview_chars = int(config.get("preview_chars") or 280)

    results = [
        analyze_target(
            target=target,
            state=state,
            user_agent=user_agent,
            timeout_seconds=timeout_seconds,
            preview_chars=preview_chars,
        )
        for target in targets
    ]
    save_json(state_path, state)

    payload = {
        "checked_at": int(time.time()),
        "alerts": [item for item in results if item["alert_reasons"]],
        "results": results,
        "summary": build_summary(results),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
