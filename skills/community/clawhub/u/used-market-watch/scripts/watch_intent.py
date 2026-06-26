from __future__ import annotations

import re
from typing import Any

from query_parser import parse_search_intent


SCRIPT_PATH = "skills/used-market-watch/scripts/used_market_watch.py"


def _derive_name(text: str, keyword: str) -> str:
    quoted = re.search(r'"([^"]{2,40})"', text)
    if quoted:
        return quoted.group(1).strip()
    clean_keyword = " ".join(str(keyword or "").split())
    clean_keyword = re.sub(r"\b\d+시간마다\b|\b\d+분마다\b", " ", clean_keyword)
    clean_keyword = re.sub(r"매일\s*(?:아침|저녁|밤|오전|오후)?\s*\d{1,2}시(?:\s*\d{1,2}분)?(?:에)?", " ", clean_keyword)
    clean_keyword = re.sub(r"(신규\s*매물만|신규만|새매물만|새매물|매물만|감시해줘|브리핑해줘|알려줘|체크해줘|감시|브리핑|알림|요약)", " ", clean_keyword)
    clean_keyword = " ".join(clean_keyword.split())[:32].strip()
    return f"{clean_keyword or '중고 매물'} 감시"


def _detect_notifications(text: str) -> tuple[bool, bool]:
    normalized = text.replace(" ", "")
    has_new = any(token in normalized for token in ("신규만", "새매물만", "신규", "새매물", "새로올라오면", "새로올라온"))
    has_drop = any(token in normalized for token in ("가격하락만", "가격내려가면", "가격떨어지면", "가격하락", "내려가면", "떨어지면"))
    if "신규만" in normalized or "새매물만" in normalized:
        return True, False
    if "가격하락만" in normalized:
        return False, True
    if has_new or has_drop:
        return has_new, has_drop
    return True, True


def _detect_limit(text: str, default_limit: int) -> int:
    m = re.search(r"(\d+)\s*(?:개|건)\s*(?:만|까지|정도)?", text)
    if m:
        return max(1, int(m.group(1)))
    return default_limit


def _detect_delivery_mode(text: str) -> str:
    normalized = text.replace(" ", "")
    if any(token in normalized for token in ("브리핑", "요약", "정리해줘", "정리", "리포트", "보고")):
        return "briefing"
    return "alert"


def _parse_hour_minute(text: str) -> tuple[int, int] | None:
    m = re.search(r"(?:(오전|오후|아침|저녁|밤)\s*)?(\d{1,2})\s*(?:시|:)\s*(?:(\d{1,2})\s*분?)?", text)
    if not m:
        return None
    meridiem, hour_raw, minute_raw = m.groups()
    hour = int(hour_raw)
    minute = int(minute_raw or 0)
    if meridiem in ("오후", "저녁", "밤") and hour < 12:
        hour += 12
    if meridiem in ("오전", "아침") and hour == 12:
        hour = 0
    hour = max(0, min(hour, 23))
    minute = max(0, min(minute, 59))
    return hour, minute


def _detect_schedule(text: str) -> dict[str, Any]:
    normalized = text.replace(" ", "")
    every_minutes = re.search(r"(\d+)분마다", normalized)
    if every_minutes:
        minutes = max(1, int(every_minutes.group(1)))
        return {
            "kind": "interval",
            "every_minutes": minutes,
            "label": f"{minutes}분마다",
            "cron": f"*/{minutes} * * * *" if minutes < 60 and 60 % minutes == 0 else None,
        }
    every_hours = re.search(r"(\d+)시간마다", normalized)
    if every_hours:
        hours = max(1, int(every_hours.group(1)))
        return {
            "kind": "interval",
            "every_hours": hours,
            "label": f"{hours}시간마다",
            "cron": f"0 */{hours} * * *" if hours < 24 and 24 % hours == 0 else None,
        }
    if any(token in normalized for token in ("매일", "매일아침", "매일저녁", "매일밤", "아침", "저녁", "밤")):
        parsed = _parse_hour_minute(text)
        if parsed:
            hour, minute = parsed
            return {
                "kind": "daily",
                "hour": hour,
                "minute": minute,
                "label": f"매일 {hour:02d}:{minute:02d}",
                "cron": f"{minute} {hour} * * *",
            }
    return {"kind": "manual", "label": "수동 또는 상위 스케줄러 연결 필요", "cron": None}


def _detect_action(text: str, delivery_mode: str) -> str:
    normalized = text.replace(" ", "")
    if delivery_mode == "briefing" or any(token in normalized for token in ("브리핑", "요약", "정리")):
        return "brief"
    if any(token in normalized for token in ("감시", "모니터링", "알려줘", "체크")):
        return "watch"
    return "watch"


def _build_plan_hints(name: str, delivery_mode: str, schedule: dict[str, Any]) -> dict[str, Any]:
    command = f'python {SCRIPT_PATH} watch-check "{name}" --json'
    if delivery_mode == "alert":
        command = f'python {SCRIPT_PATH} watch-check "{name}" --alerts-only --json'
    persist_command = f'python {SCRIPT_PATH} watch-upsert {{request_json}}'
    return {
        "recommended_command": command,
        "persist_command_template": persist_command,
        "cron": schedule.get("cron"),
        "cron_example": f'{schedule["cron"]} {command}' if schedule.get("cron") else None,
    }


def parse_watch_request(text: str, *, default_limit: int = 12) -> dict[str, Any]:
    intent = parse_search_intent(text, limit=_detect_limit(text, default_limit))
    notify_on_new, notify_on_price_drop = _detect_notifications(text)
    name = _derive_name(text, intent.keyword)
    delivery_mode = _detect_delivery_mode(text)
    schedule = _detect_schedule(text)
    action = _detect_action(text, delivery_mode)
    plan_hints = _build_plan_hints(name, delivery_mode, schedule)
    return {
        "name": name,
        "query": intent.raw_query,
        "limit": intent.limit,
        "min_price": intent.min_price,
        "max_price": intent.max_price,
        "notify_on_new": notify_on_new,
        "notify_on_price_drop": notify_on_price_drop,
        "enabled": "비활성" not in text and "끄기" not in text,
        "delivery_mode": delivery_mode,
        "action": action,
        "schedule": schedule,
        "plan_hints": plan_hints,
        "intent": intent.to_dict(),
    }


def build_integration_bundle(text: str, *, default_limit: int = 12) -> dict[str, Any]:
    plan = parse_watch_request(text, default_limit=default_limit)
    rule = {k: v for k, v in plan.items() if k != "intent"}
    delivery_label = "브리핑" if rule.get("delivery_mode") == "briefing" else "알림"
    notification_bits = []
    if rule.get("notify_on_new"):
        notification_bits.append("신규")
    if rule.get("notify_on_price_drop"):
        notification_bits.append("가격하락")
    schedule = rule.get("schedule") or {}
    recommended_command = (rule.get("plan_hints") or {}).get("recommended_command")
    persist_command = f'python {SCRIPT_PATH} watch-upsert {text!r}'
    cron_payload = None
    if schedule.get("cron"):
        cron_payload = {
            "expr": schedule["cron"],
            "command": recommended_command,
            "description": f'{rule["name"]} / {schedule.get("label") or schedule["cron"]}',
        }
    system_event = {
        "type": "used-market-watch-check",
        "schedule_label": schedule.get("label"),
        "rule_name": rule["name"],
        "delivery_mode": rule.get("delivery_mode"),
        "command": recommended_command,
    }
    operator_summary = (
        f'"{rule["name"]}" 규칙으로 {plan["intent"].get("keyword") or rule.get("query")} 를 '
        f'{schedule.get("label") or "수동"} 기준 {delivery_label} 형태로 운영합니다. '
        f'알림 조건은 {", ".join(notification_bits) if notification_bits else "없음"}입니다.'
    )
    user_confirmation = (
        f'{rule["name"]}: {schedule.get("label") or "수동 실행"} / {delivery_label} / '
        f'{", ".join(notification_bits) if notification_bits else "조건 없음"}으로 설정하면 됩니다.'
    )
    return {
        "kind": "used-market-integration-plan",
        "request": text,
        "parsed_plan": plan,
        "persist": {
            "command": persist_command,
            "rule_name": rule["name"],
        },
        "execution": {
            "recommended_command": recommended_command,
            "cron_payload": cron_payload,
            "system_event": system_event,
        },
        "operator_summary": operator_summary,
        "user_confirmation": user_confirmation,
    }
