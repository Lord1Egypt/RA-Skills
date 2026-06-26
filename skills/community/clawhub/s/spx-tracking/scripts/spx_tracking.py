#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import requests


API_URL = "https://spx.com.my/shipment/order/open/order/get_order_info"
DEFAULT_TIMEOUT = 15
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://spx.com.my/",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/146.0.0.0 Safari/537.36"
    ),
}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class TrackingEvent:
    time: int
    code: str
    title: str
    summary: str
    buyer_description: str
    seller_description: str
    milestone_code: str
    milestone_name: str
    reason_code: str
    reason_desc: str
    epod: str
    display_flag: str
    display_flag_v2: str
    delivery_on_hold_times: str
    current_location_name: str
    current_location_type: str
    current_lng: str
    current_lat: str
    current_location_address: str
    next_location_name: str
    next_location_type: str
    next_lng: str
    next_lat: str
    next_location_address: str

    @property
    def display_time(self) -> str:
        return format_timestamp(self.time)


@dataclass
class EventGroup:
    representative: TrackingEvent
    latest_time: int
    earliest_time: int
    count: int

    @property
    def latest_display_time(self) -> str:
        return format_timestamp(self.latest_time)

    @property
    def earliest_display_time(self) -> str:
        return format_timestamp(self.earliest_time)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def format_timestamp(value: int) -> str:
    if not value:
        return ""
    dt = datetime.fromtimestamp(value, tz=timezone.utc).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def repair_text(value: Any) -> Any:
    if isinstance(value, str):
        return repair_mojibake(value)
    if isinstance(value, list):
        return [repair_text(item) for item in value]
    if isinstance(value, dict):
        return {key: repair_text(item) for key, item in value.items()}
    return value


def repair_mojibake(text: str) -> str:
    for source, target in (("latin1", "utf-8"), ("gbk", "utf-8")):
        try:
            candidate = text.encode(source).decode(target)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if better_text(candidate, text):
            return candidate
    return text


def better_text(candidate: str, original: str) -> bool:
    if candidate.count("\ufffd") > original.count("\ufffd"):
        return False
    return cjk_count(candidate) > cjk_count(original)


def cjk_count(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def as_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def non_empty_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value not in ("", None, [], {})}


def has_coordinates(event: TrackingEvent) -> bool:
    return bool(event.current_lng and event.current_lat)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

def fetch_tracking(tracking_number: str, cookie: str | None, timeout: int) -> dict[str, Any]:
    headers = HEADERS.copy()
    headers["referer"] = f"https://spx.com.my/track?{tracking_number}"
    if cookie:
        headers["cookie"] = cookie

    response = requests.get(
        API_URL,
        params={"spx_tn": tracking_number},
        headers=headers,
        timeout=timeout,
    )
    response.raise_for_status()

    payload = repair_text(response.json())
    if payload.get("retcode") != 0:
        message = payload.get("message") or "unknown API error"
        detail = payload.get("detail") or ""
        raise RuntimeError(f"{message} {detail}".strip())
    return payload


# ---------------------------------------------------------------------------
# Event parsing
# ---------------------------------------------------------------------------

def build_events(payload: dict[str, Any]) -> list[TrackingEvent]:
    records = payload["data"]["sls_tracking_info"].get("records", [])
    events = [build_event(item) for item in records]
    events.sort(key=lambda item: item.time)
    return events


def build_event(item: dict[str, Any]) -> TrackingEvent:
    current_location = item.get("current_location") or {}
    next_location = item.get("next_location") or {}
    return TrackingEvent(
        time=as_int(item.get("actual_time")),
        code=as_text(item.get("tracking_code")),
        title=pick_title(item),
        summary=pick_summary(item),
        buyer_description=as_text(item.get("buyer_description")),
        seller_description=as_text(item.get("seller_description")),
        milestone_code=as_text(item.get("milestone_code")),
        milestone_name=as_text(item.get("milestone_name")),
        reason_code=as_text(item.get("reason_code")),
        reason_desc=as_text(item.get("reason_desc")),
        epod=as_text(item.get("epod")),
        display_flag=as_text(item.get("display_flag")),
        display_flag_v2=as_text(item.get("display_flag_v2")),
        delivery_on_hold_times=as_text(item.get("delivery_on_hold_times")),
        current_location_name=as_text(current_location.get("location_name")),
        current_location_type=as_text(current_location.get("location_type_name")),
        current_lng=as_text(current_location.get("lng")),
        current_lat=as_text(current_location.get("lat")),
        current_location_address=as_text(current_location.get("full_address")),
        next_location_name=as_text(next_location.get("location_name")),
        next_location_type=as_text(next_location.get("location_type_name")),
        next_lng=as_text(next_location.get("lng")),
        next_lat=as_text(next_location.get("lat")),
        next_location_address=as_text(next_location.get("full_address")),
    )


def pick_title(item: dict[str, Any]) -> str:
    for field in ("tracking_name", "milestone_name"):
        value = as_text(item.get(field))
        if value:
            return value
    return "Unknown"


def pick_summary(item: dict[str, Any]) -> str:
    for field in ("buyer_description", "description", "seller_description"):
        value = as_text(item.get(field))
        if value:
            return value
    return as_text(item.get("milestone_name"))


# ---------------------------------------------------------------------------
# Event grouping
# ---------------------------------------------------------------------------

def compress_events(events: list[TrackingEvent]) -> list[EventGroup]:
    if not events:
        return []

    groups: list[EventGroup] = []
    for event in events:
        if groups and same_event(groups[-1].representative, event):
            groups[-1].count += 1
            groups[-1].latest_time = max(groups[-1].latest_time, event.time)
            groups[-1].earliest_time = min(groups[-1].earliest_time, event.time)
            continue
        groups.append(
            EventGroup(
                representative=event,
                latest_time=event.time,
                earliest_time=event.time,
                count=1,
            )
        )
    return groups


def same_event(left: TrackingEvent, right: TrackingEvent) -> bool:
    return (
        left.code == right.code
        and left.title == right.title
        and left.summary == right.summary
        and left.milestone_code == right.milestone_code
        and left.reason_code == right.reason_code
        and left.reason_desc == right.reason_desc
        and left.current_location_name == right.current_location_name
        and left.next_location_name == right.next_location_name
    )


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def resolve_status(payload: dict[str, Any], events: list[TrackingEvent]) -> str:
    order_info = payload["data"].get("order_info", {})
    status = (
        as_text(order_info.get("tracking_code_subgroup_name"))
        or as_text(order_info.get("tracking_code_group_name"))
    )
    if status:
        return status
    if events:
        return events[-1].title
    return ""


def resolve_display_tracking_number(payload: dict[str, Any], requested_tracking_number: str) -> str:
    order_info = payload["data"].get("order_info", {})
    parcel_info = payload["data"].get("parcel_info", {})
    return (
        as_text(parcel_info.get("customer_tracking_no"))
        or as_text(order_info.get("spx_tn"))
        or requested_tracking_number
    )


def format_duration(seconds: int) -> str:
    if seconds <= 0:
        return ""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs and not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def build_stays(events: list[TrackingEvent]) -> list[tuple[TrackingEvent, TrackingEvent, int]]:
    return [
        (previous, current, current.time - previous.time)
        for previous, current in zip(events, events[1:])
    ]


def best_bottleneck(stays: list[tuple[TrackingEvent, TrackingEvent, int]]) -> tuple[TrackingEvent, TrackingEvent, int] | None:
    if not stays:
        return None
    return max(stays, key=lambda item: item[2])


def serialize_event(event: TrackingEvent) -> dict[str, Any]:
    return non_empty_dict(
        {
            "time_unix": event.time,
            "time": event.display_time,
            "tracking_code": event.code,
            "title": event.title,
            "summary": event.summary,
            "buyer_description": event.buyer_description,
            "seller_description": event.seller_description,
            "milestone_code": event.milestone_code,
            "milestone_name": event.milestone_name,
            "reason_code": event.reason_code,
            "reason_desc": event.reason_desc,
            "epod": event.epod,
            "display_flag": event.display_flag,
            "display_flag_v2": event.display_flag_v2,
            "delivery_on_hold_times": event.delivery_on_hold_times,
            "current_location_name": event.current_location_name,
            "current_location_type": event.current_location_type,
            "current_lng": event.current_lng,
            "current_lat": event.current_lat,
            "current_full_address": event.current_location_address,
            "next_location_name": event.next_location_name,
            "next_location_type": event.next_location_type,
            "next_lng": event.next_lng,
            "next_lat": event.next_lat,
            "next_full_address": event.next_location_address,
        }
    )


def serialize_group(group: EventGroup) -> dict[str, Any]:
    event = group.representative
    return non_empty_dict(
        {
            "title": event.title,
            "time_start_unix": group.earliest_time,
            "time_start": group.earliest_display_time,
            "time_end_unix": group.latest_time if group.count > 1 else None,
            "time_end": group.latest_display_time if group.count > 1 else "",
            "repeat_count": group.count,
            "tracking_code": event.code,
            "summary": event.summary,
            "buyer_description": event.buyer_description,
            "seller_description": event.seller_description,
            "milestone_code": event.milestone_code,
            "milestone_name": event.milestone_name,
            "reason_code": event.reason_code,
            "reason_desc": event.reason_desc,
            "epod": event.epod,
            "display_flag": event.display_flag,
            "display_flag_v2": event.display_flag_v2,
            "delivery_on_hold_times": event.delivery_on_hold_times,
            "current_location_name": event.current_location_name,
            "current_location_type": event.current_location_type,
            "current_lng": event.current_lng,
            "current_lat": event.current_lat,
            "current_full_address": event.current_location_address,
            "next_location_name": event.next_location_name,
            "next_location_type": event.next_location_type,
            "next_lng": event.next_lng,
            "next_lat": event.next_lat,
            "next_full_address": event.next_location_address,
        }
    )


def build_report(payload: dict[str, Any], requested_tracking_number: str) -> dict[str, Any]:
    data = payload.get("data", {})
    order_info = data.get("order_info", {})
    parcel_info = data.get("parcel_info", {})
    sls_tracking_info = data.get("sls_tracking_info", {})
    fulfillment_info = data.get("fulfillment_info", {})
    edd_info = data.get("edd_info", {})
    events = build_events(payload)
    groups = compress_events(events)
    geo_events = [event for event in events if has_coordinates(event)]
    stays = build_stays(events)
    bottleneck = best_bottleneck(stays)

    # Derive retcode for top-level convenience
    retcode = payload.get("retcode")

    return {
        # Top-level retcode so Agent can inspect it without relying on exit code
        "retcode": retcode,
        "response": non_empty_dict(
            {
                "message": as_text(payload.get("message")),
                "detail": as_text(payload.get("detail")),
            }
        ),
        "shipment": non_empty_dict(
            {
                "requested_tracking_number": requested_tracking_number,
                "customer_tracking_no": as_text(parcel_info.get("customer_tracking_no")),
                "tracking_number": resolve_display_tracking_number(payload, requested_tracking_number),
                "status": resolve_status(payload, events),
                "sls_tn": as_text(sls_tracking_info.get("sls_tn")) or as_text(order_info.get("sls_tn")),
                "spx_tn": as_text(order_info.get("spx_tn")),
                "client_order_id": as_text(sls_tracking_info.get("client_order_id")),
                "order_id": as_text(order_info.get("order_id")),
                "tracking_code_group_name": as_text(order_info.get("tracking_code_group_name")),
                "tracking_code_subgroup_name": as_text(order_info.get("tracking_code_subgroup_name")),
                "receiver_name": as_text(sls_tracking_info.get("receiver_name")),
                "receiver_type_name": as_text(sls_tracking_info.get("receiver_type_name")),
                "is_instant_order": data.get("is_instant_order"),
                "is_shopee_market_order": data.get("is_shopee_market_order"),
                "deliver_type": fulfillment_info.get("deliver_type"),
                "edd_min_unix": as_int(edd_info.get("edd_min")),
                "edd_min": format_timestamp(as_int(edd_info.get("edd_min"))),
                "edd_max_unix": as_int(edd_info.get("edd_max")),
                "edd_max": format_timestamp(as_int(edd_info.get("edd_max"))),
                "raw_events": len(events),
                "grouped_events": len(groups),
                "geo_events": len(geo_events),
                "first_event_time_unix": events[0].time if events else 0,
                "first_event_time": events[0].display_time if events else "",
                "last_event_time_unix": events[-1].time if events else 0,
                "last_event_time": events[-1].display_time if events else "",
            }
        ),
        "timeline": {
            "grouped_events": [serialize_group(group) for group in groups],
            "raw_events": [serialize_event(event) for event in events],
        },
        "geo_route": {
            "points": [serialize_event(event) for event in geo_events],
        },
        "stay_analysis": {
            "segments": [
                non_empty_dict(
                    {
                        "from_title": previous.title,
                        "to_title": current.title,
                        "from_tracking_code": previous.code,
                        "to_tracking_code": current.code,
                        "from_time_unix": previous.time,
                        "from_time": previous.display_time,
                        "to_time_unix": current.time,
                        "to_time": current.display_time,
                        "duration_seconds": delta,
                        "duration": format_duration(delta),
                    }
                )
                for previous, current, delta in stays
            ],
        },
        "bottleneck": non_empty_dict(
            {
                "from_title": bottleneck[0].title if bottleneck else "",
                "to_title": bottleneck[1].title if bottleneck else "",
                "from_tracking_code": bottleneck[0].code if bottleneck else "",
                "to_tracking_code": bottleneck[1].code if bottleneck else "",
                "from_time_unix": bottleneck[0].time if bottleneck else 0,
                "from_time": bottleneck[0].display_time if bottleneck else "",
                "to_time_unix": bottleneck[1].time if bottleneck else 0,
                "to_time": bottleneck[1].display_time if bottleneck else "",
                "duration_seconds": bottleneck[2] if bottleneck else 0,
                "duration": format_duration(bottleneck[2]) if bottleneck else "",
            }
        ),
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def render_summary(report: dict[str, Any]) -> str:
    """One-line status summary — best for quick Agent replies."""
    shipment = report.get("shipment", {})
    status = shipment.get("status", "Unknown")
    tracking_number = shipment.get("tracking_number", "")
    last_time = shipment.get("last_event_time", "")
    edd_min = shipment.get("edd_min", "")
    edd_max = shipment.get("edd_max", "")

    parts = [f"[{tracking_number}]"]
    if status:
        parts.append(f"状态: {status}")
    if last_time:
        parts.append(f"最后更新: {last_time}")
    if edd_min and edd_max:
        parts.append(f"预计送达: {edd_min} ~ {edd_max}")
    return " | ".join(parts)


def render_text_report(report: dict[str, Any], summary_only: bool = False) -> str:
    """Human-readable text report. Optionally suppress full timeline."""
    lines: list[str] = []

    shipment = report.get("shipment", {})
    timeline = report.get("timeline", {})
    geo_route = report.get("geo_route", {})
    stay_analysis = report.get("stay_analysis", {})
    bottleneck = report.get("bottleneck", {})

    # ── Status block ────────────────────────────────────────────────────────
    lines.append("━━ SPX 快递追踪 ━━")
    status = shipment.get("status", "")
    if status:
        lines.append(f"  状态: {status}")
    tracking_number = shipment.get("tracking_number", "")
    if tracking_number:
        lines.append(f"  单号: {tracking_number}")
    receiver = shipment.get("receiver_name", "")
    if receiver:
        lines.append(f"  收件人: {receiver}")
    edd_min = shipment.get("edd_min", "")
    edd_max = shipment.get("edd_max", "")
    if edd_min and edd_max:
        lines.append(f"  预计送达: {edd_min} ~ {edd_max}")
    first_time = shipment.get("first_event_time", "")
    last_time = shipment.get("last_event_time", "")
    if first_time:
        lines.append(f"  首次更新: {first_time}")
    if last_time:
        lines.append(f"  最后更新: {last_time}")

    if summary_only:
        return "\n".join(lines)

    # ── Timeline ─────────────────────────────────────────────────────────────
    grouped = timeline.get("grouped_events", [])
    if grouped:
        lines.append("")
        lines.append("━━ 物流时间线 ━━")
        for idx, item in enumerate(grouped, start=1):
            title = item.get("title", "Unknown")
            time_str = item.get("time_start", "")
            summary = item.get("summary", "")
            location = item.get("current_location_name", "")
            repeat = item.get("repeat_count", 1)
            repeat_note = f" (×{repeat})" if repeat > 1 else ""
            line = f"  {idx:02d}. {time_str}  {title}{repeat_note}"
            if location:
                line += f" @ {location}"
            lines.append(line)
            if summary:
                lines.append(f"      {summary}")

    # ── Delay analysis ───────────────────────────────────────────────────────
    if bottleneck and bottleneck.get("from_title"):
        lines.append("")
        lines.append("━━ 最大延迟 ━━")
        lines.append(f"  {bottleneck['from_title']} → {bottleneck['to_title']}")
        lines.append(f"  持续时间: {bottleneck['duration']} ({bottleneck['duration_seconds']}s)")

    # ── Geo route ────────────────────────────────────────────────────────────
    geo_points = geo_route.get("points", [])
    if geo_points:
        lines.append("")
        lines.append("━━ 地理位置 ━━")
        for idx, item in enumerate(geo_points, start=1):
            title = item.get("title", "Unknown")
            time_str = item.get("time", "")
            address = item.get("current_full_address", "")
            lines.append(f"  {idx:02d}. {time_str}  {title}")
            if address:
                lines.append(f"      {address}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query SPX Express tracking events",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("tracking_number", help="SPX tracking number, e.g. CNMY000XXXXXX")
    parser.add_argument("--cookie", help="Optional browser cookie for authenticated requests")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Request timeout in seconds (default: 15)")
    parser.add_argument(
        "--format",
        choices=("json", "text", "summary"),
        default="json",
        help="json: full structured data (default); text: human-readable; summary: one-line status",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = fetch_tracking(args.tracking_number, args.cookie, args.timeout)
        report = build_report(payload, args.tracking_number)

        if args.format == "summary":
            print(render_summary(report))
        elif args.format == "text":
            # --format text is always the full readable report (see SKILL.md for usage patterns)
            print(render_text_report(report))
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))

    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1
    except (KeyError, RuntimeError, ValueError) as exc:
        print(f"Parse failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
