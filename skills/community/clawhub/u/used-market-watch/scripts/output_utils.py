from __future__ import annotations

from typing import Any

from models import MARKET_LABELS
from price_utils import format_price_kr


EVENT_LABELS = {
    "new_listing": "신규 매물",
    "price_drop": "가격하락",
}


def render_search_text(payload: dict[str, Any]) -> str:
    intent = payload.get("intent") or {}
    items = payload.get("items") or []
    lines = [f"중고 매물 브리핑: {intent.get('keyword') or intent.get('raw_query')}"]
    filters = []
    if intent.get("markets"):
        filters.append("마켓=" + ", ".join(MARKET_LABELS.get(m, m) for m in intent["markets"]))
    if intent.get("location"):
        filters.append(f"지역={intent['location']}")
    if intent.get("min_price"):
        filters.append(f"최소={format_price_kr(intent['min_price'])}")
    if intent.get("max_price"):
        filters.append(f"최대={format_price_kr(intent['max_price'])}")
    if intent.get("exclude_terms"):
        filters.append("제외=" + ", ".join(intent["exclude_terms"]))
    if filters:
        lines.append("- " + " / ".join(filters))
    summary = payload.get("summary") or {}
    lines.append(f"- 총 {summary.get('total', 0)}건, 표시 {len(items)}건")
    for market, row in (summary.get("by_market") or {}).items():
        lines.append(f"- {MARKET_LABELS.get(market, market)}: {row.get('count', 0)}건, 최저 {format_price_kr(row.get('min_price'))}, 최고 {format_price_kr(row.get('max_price'))}")
    if not items:
        lines.append("- 조건에 맞는 매물이 없습니다.")
        return "\n".join(lines)
    for idx, item in enumerate(items, start=1):
        label = MARKET_LABELS.get(item.get("market"), item.get("market"))
        price = item.get("price_text") or format_price_kr(item.get("price_numeric"))
        extra = []
        if item.get("location"):
            extra.append(item["location"])
        if item.get("seller"):
            extra.append(f"판매자 {item['seller']}")
        suffix = f" ({' / '.join(extra)})" if extra else ""
        lines.append(f"{idx}. [{label}] {item.get('title')} - {price}{suffix}")
        if item.get("link"):
            lines.append(f"   - {item['link']}")
    return "\n".join(lines)


def render_watch_preview(payload: dict[str, Any]) -> str:
    lines = [f"중고 매물 watch 점검: {payload.get('alert_count', 0)}건 알림"]
    summary = payload.get("summary") or {}
    if summary.get("event_counts"):
        counts = ", ".join(f"{EVENT_LABELS.get(k, k)}={v}" for k, v in summary["event_counts"].items())
        lines.append(f"- 이벤트 요약: {counts}")
    for row in payload.get("alerts") or []:
        rule = row.get("rule") or {}
        schedule = ((rule.get("schedule") or {}).get("label") or "수동")
        mode_label = "브리핑" if rule.get("delivery_mode") == "briefing" else "알림"
        lines.append(f"- {rule.get('name')}: {row.get('matched_count', 0)}건 / {mode_label} / {schedule}")
        for match in (row.get("matched") or [])[:5]:
            badges = [EVENT_LABELS.get(match.get("event_type"), match.get("event_type"))]
            if match.get("previous_price_text"):
                badges.append(f"이전 {match['previous_price_text']}")
            lines.append(f"  · [{MARKET_LABELS.get(match.get('market'), match.get('market'))}] {match.get('title')} / {match.get('price_text')} ({', '.join([b for b in badges if b])})")
            if match.get("link"):
                lines.append(f"    - {match['link']}")
    return "\n".join(lines)


def render_watch_plan(payload: dict[str, Any]) -> str:
    rule = payload.get("rule") or {}
    intent = payload.get("intent") or {}
    modes = []
    if rule.get("notify_on_new"):
        modes.append("신규")
    if rule.get("notify_on_price_drop"):
        modes.append("가격하락")
    delivery_mode = "브리핑" if rule.get("delivery_mode") == "briefing" else "알림"
    schedule = rule.get("schedule") or {}
    plan_hints = rule.get("plan_hints") or payload.get("plan_hints") or {}
    lines = [f"watch 규칙 해석: {rule.get('name')}"]
    lines.append(f"- 쿼리: {rule.get('query')}")
    lines.append(f"- 동작: {delivery_mode}")
    lines.append(f"- 알림 조건: {', '.join(modes) if modes else '없음'}")
    lines.append(f"- 상태: {'활성' if rule.get('enabled', True) else '비활성'}")
    lines.append(f"- limit: {rule.get('limit')}")
    lines.append(f"- 실행 주기: {schedule.get('label') or '수동'}")
    if plan_hints.get("recommended_command"):
        lines.append(f"- 권장 실행: {plan_hints['recommended_command']}")
    if plan_hints.get("cron_example"):
        lines.append(f"- cron 예시: {plan_hints['cron_example']}")
    elif schedule.get("cron"):
        lines.append(f"- cron: {schedule['cron']}")
    if intent.get("markets"):
        lines.append("- 마켓: " + ", ".join(MARKET_LABELS.get(m, m) for m in intent["markets"]))
    if intent.get("location"):
        lines.append(f"- 지역: {intent['location']}")
    if intent.get("min_price"):
        lines.append(f"- 최소가: {format_price_kr(intent['min_price'])}")
    if intent.get("max_price"):
        lines.append(f"- 최대가: {format_price_kr(intent['max_price'])}")
    if intent.get("exclude_terms"):
        lines.append("- 제외어: " + ", ".join(intent["exclude_terms"]))
    return "\n".join(lines)


def render_watch_list(state: dict[str, Any]) -> str:
    rules = state.get("rules") or []
    if not rules:
        return "등록된 watch rule이 없습니다."
    event_counts: dict[str, int] = {}
    for event in state.get("events") or []:
        event_counts[event.get("rule_id")] = event_counts.get(event.get("rule_id"), 0) + 1
    lines = [f"등록된 watch rule {len(rules)}개"]
    for rule in rules:
        modes = []
        if rule.get("notify_on_new"):
            modes.append("신규")
        if rule.get("notify_on_price_drop"):
            modes.append("가격하락")
        schedule_label = ((rule.get("schedule") or {}).get("label") or "수동")
        delivery_mode = "브리핑" if rule.get("delivery_mode") == "briefing" else "알림"
        lines.append(f"- {rule['name']} ({rule['id']})")
        lines.append(f"  · 상태: {'활성' if rule.get('enabled', True) else '비활성'} / 동작: {delivery_mode} / 주기: {schedule_label}")
        lines.append(f"  · 알림 조건: {', '.join(modes) if modes else '없음'}")
        lines.append(f"  · 쿼리: {rule['query']}")
        if rule.get("min_price"):
            lines.append(f"  · 최소가: {rule['min_price']:,}원")
        if rule.get("max_price"):
            lines.append(f"  · 최대가: {rule['max_price']:,}원")
        if (rule.get("plan_hints") or {}).get("cron_example"):
            lines.append(f"  · cron 예시: {rule['plan_hints']['cron_example']}")
        lines.append(f"  · 누적 이벤트: {event_counts.get(rule['id'], 0)}건")
    return "\n".join(lines)


def render_watch_events(payload: dict[str, Any]) -> str:
    events = payload.get("events") or []
    if not events:
        return "최근 watch 이벤트가 없습니다."
    lines = [f"최근 watch 이벤트 {len(events)}건"]
    for event in events:
        badges = [EVENT_LABELS.get(event.get("event_type"), event.get("event_type"))]
        if event.get("previous_price_text"):
            badges.append(f"이전 {event['previous_price_text']}")
        lines.append(
            f"- {event.get('rule_name')} / [{MARKET_LABELS.get(event.get('market'), event.get('market'))}] {event.get('title')} / {event.get('price_text')} ({', '.join([b for b in badges if b])})"
        )
        if event.get("link"):
            lines.append(f"  · {event['link']}")
    return "\n".join(lines)


def render_integration_plan(payload: dict[str, Any]) -> str:
    plan = payload.get("parsed_plan") or {}
    rule = {k: v for k, v in plan.items() if k != "intent"}
    schedule = rule.get("schedule") or {}
    execution = payload.get("execution") or {}
    cron_payload = execution.get("cron_payload") or {}
    lines = [f"자동화 연동 계획: {rule.get('name')}"]
    lines.append(f"- 요청: {payload.get('request')}")
    lines.append(f"- 확인 문구: {payload.get('user_confirmation')}")
    lines.append(f"- 저장 명령: {((payload.get('persist') or {}).get('command'))}")
    if execution.get("recommended_command"):
        lines.append(f"- 실행 명령: {execution['recommended_command']}")
    lines.append(f"- 주기: {schedule.get('label') or '수동'}")
    if cron_payload.get("expr"):
        lines.append(f"- cron 제안: {cron_payload['expr']}")
    system_event = execution.get("system_event") or {}
    if system_event:
        lines.append(f"- systemEvent 힌트: {system_event.get('type')} / rule={system_event.get('rule_name')} / mode={system_event.get('delivery_mode')}")
    lines.append(f"- 운영 요약: {payload.get('operator_summary')}")
    return "\n".join(lines)
