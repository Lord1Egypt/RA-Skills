#!/usr/bin/env python3
"""Seats.aero watcher runner with SQLite state + idempotent alerts."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from seats_client import SeatsClient, SeatsClientError  # type: ignore
    from store import (  # type: ignore
        AlertEvent,
        AvailabilityRecord,
        JsonStore,
        SqliteStore,
        Store,
        WatcherConfig,
        _clean_list,
        _default_state_db,
        _iso_now,
        _normalize_fixed_date,
        _pick,
        _to_int,
    )
else:
    from .seats_client import SeatsClient, SeatsClientError
    from .store import (
        AlertEvent,
        AvailabilityRecord,
        JsonStore,
        SqliteStore,
        Store,
        WatcherConfig,
        _clean_list,
        _default_state_db,
        _iso_now,
        _normalize_fixed_date,
        _pick,
        _to_int,
    )


def _date_only(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value)
    if "T" in text:
        return text.split("T", 1)[0]
    if " " in text:
        return text.split(" ", 1)[0]
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return text


def _load_json_or_yaml(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore

            loaded = yaml.safe_load(raw)
            data = loaded if isinstance(loaded, dict) else {}
        except Exception as exc:
            raise RuntimeError(
                "Config must be JSON (valid YAML subset) unless PyYAML is installed."
            ) from exc
    if not isinstance(data, dict):
        raise RuntimeError("Config root must be an object/map.")
    return data


def load_watchers(config_path: Path) -> list[WatcherConfig]:
    data = _load_json_or_yaml(config_path)
    defaults = data.get("defaults", {})
    if not isinstance(defaults, dict):
        defaults = {}
    raw_watchers = data.get("watchers", [])
    if not isinstance(raw_watchers, list):
        raise RuntimeError("`watchers` must be a list.")

    out: list[WatcherConfig] = []
    for item in raw_watchers:
        if not isinstance(item, dict):
            continue
        watcher = {**defaults, **item}
        watcher_id = str(_pick(watcher, "id") or "").strip()
        if not watcher_id:
            continue
        out.append(
            WatcherConfig(
                id=watcher_id,
                enabled=bool(watcher.get("enabled", True)),
                origin=str(_pick(watcher, "origin") or "").upper(),
                destination=str(_pick(watcher, "destination") or "").upper(),
                program=str(_pick(watcher, "program") or "").strip() or None,
                airlines=[code.upper() for code in _clean_list(watcher.get("airlines"))],
                cabins=[c.lower() for c in _clean_list(watcher.get("cabins")) or ["business"]],
                seats_required=max(1, _to_int(_pick(watcher, "seats_required")) or 1),
                window_days=max(1, _to_int(_pick(watcher, "window_days")) or 365),
                fixed_start_date=_normalize_fixed_date(
                    _pick(watcher, "fixed_start_date", "start_date", "date_from")
                ),
                fixed_end_date=_normalize_fixed_date(
                    _pick(watcher, "fixed_end_date", "end_date", "date_to")
                ),
                alert_new_only=bool(watcher.get("alert_new_only", True)),
                enhanced_alert_on_seat_increase=bool(watcher.get("enhanced_alert_on_seat_increase", False)),
                notify_channel=str(_pick(watcher, "notify_channel") or "telegram"),
                notify_target=str(_pick(watcher, "notify_target") or "").strip() or None,
                fetch_retries=max(0, _to_int(_pick(watcher, "fetch_retries")) or 0),
                fetch_retry_delay_seconds=max(
                    0, _to_int(_pick(watcher, "fetch_retry_delay_seconds")) or 2
                ),
            )
        )
    return out


def select_watchers(watchers: list[WatcherConfig], watcher_id: str | None) -> list[WatcherConfig]:
    selected = [w for w in watchers if w.enabled]
    if watcher_id:
        selected = [w for w in selected if w.id == watcher_id]
    return selected


def _extract_segments(raw: dict[str, Any]) -> dict[str, Any]:
    segments = _pick(raw, "AvailabilitySegments", "availabilitySegments", "segments", "Segments")
    if isinstance(segments, list) and segments and isinstance(segments[0], dict):
        return segments[0]
    return {}


def _build_route(origin: str | None, destination: str | None) -> str:
    left = (origin or "").upper().strip()
    right = (destination or "").upper().strip()
    return f"{left}->{right}" if left and right else "UNKNOWN"


def normalize_records(
    raw_items: list[dict[str, Any]],
    watcher: WatcherConfig,
    observed_at: str,
) -> list[AvailabilityRecord]:
    window_start_iso, window_end_iso = _watcher_date_window(watcher)
    window_start = dt.date.fromisoformat(window_start_iso)
    window_end = dt.date.fromisoformat(window_end_iso)

    normalized: list[AvailabilityRecord] = []
    for raw in raw_items:
        seg = _extract_segments(raw)
        # 只保留直飞航班：双重检查确保无转机
        # 检查1：航段数量必须为1
        full_segments = _pick(raw, "AvailabilitySegments", "availabilitySegments", "segments", "Segments", 
                            "flightSegments", "FlightSegments", "itinerarySegments", "ItinerarySegments")
        if isinstance(full_segments, list) and len(full_segments) > 1:
            continue
        # 检查2：转机次数必须为0
        stops = _to_int(_pick(raw, "stops", "Stops", "numberOfStops", "NumberOfStops", 
                            "stop_count", "StopCount", "connection_count", "ConnectionCount"))
        if stops is not None and stops > 0:
            continue
        # 检查3：总时长过滤（跨太平洋直飞一般10-12小时，超过14小时基本都是转机或者长时间经停）
        total_duration = None
        # 尝试获取总时长（分钟或秒）
        duration_min = _to_int(_pick(raw, "duration", "Duration", "totalDuration", "TotalDuration", 
                                    "flightTime", "FlightTime", "totalTime", "TotalTime"))
        if duration_min is not None:
            # 判断单位：如果数值>1000大概率是秒，转成分钟
            if duration_min > 1000:
                duration_min = duration_min // 60
            total_duration = duration_min
        # 也尝试获取小时格式的时长
        duration_hours = _pick(raw, "durationHours", "DurationHours", "totalHours", "TotalHours")
        if duration_hours is not None and total_duration is None:
            try:
                total_duration = int(float(duration_hours) * 60)
            except (TypeError, ValueError):
                pass
        # 过滤超过14小时的航班（840分钟）
        if total_duration is not None and total_duration > 840:
            continue
        origin = str(
            _pick(raw, "origin", "Origin", "originAirport", "OriginAirport")
            or _pick(seg, "origin", "Origin", "originAirport", "OriginAirport")
            or watcher.origin
        ).upper()
        destination = str(
            _pick(raw, "destination", "Destination", "destinationAirport", "DestinationAirport")
            or _pick(seg, "destination", "Destination", "destinationAirport", "DestinationAirport")
            or watcher.destination
        ).upper()
        date = _date_only(
            _pick(raw, "date", "Date", "departureDate", "DepartureDate")
            or _pick(seg, "date", "Date", "departureDate", "DepartureDate")
        )
        if not date:
            continue
        try:
            parsed_date = dt.date.fromisoformat(date)
        except ValueError:
            continue
        if parsed_date < window_start or parsed_date > window_end:
            continue
        date = parsed_date.isoformat()

        cabin = str(
            _pick(raw, "cabin", "Cabin")
            or _pick(seg, "cabin", "Cabin")
            or (watcher.cabins[0] if watcher.cabins else "business")
        ).lower()
        if watcher.cabins and cabin not in watcher.cabins:
            continue

        flight_no = str(
            _pick(raw, "flightNo", "flightNumber", "FlightNumber", "flight")
            or _pick(seg, "flightNo", "flightNumber", "FlightNumber", "flight")
            or _pick(raw, "id", "_id", "ID")
            or "UNKNOWN"
        ).upper()
        carrier = str(
            _pick(raw, "airline", "Airline", "carrier", "Carrier")
            or _pick(seg, "airline", "Airline", "carrier", "Carrier")
            or ""
        ).upper()
        if watcher.airlines and carrier and carrier not in watcher.airlines:
            continue

        # 舱位代码映射：Y=经济舱, W=超级经济舱, J=商务舱, F=头等舱
        cabin_code_map = {
            "economy": "Y",
            "premium_economy": "W",
            "business": "J",
            "first": "F"
        }
        cabin_code = cabin_code_map.get(cabin, "J")
        
        # 优先取对应舱位的余票，兼容旧字段
        seats = (
            _to_int(_pick(raw, f"{cabin_code}RemainingSeats", f"{cabin_code}RemainingSeatsRaw"))
            or _to_int(_pick(raw, "seats", "Seats", "seatCount", "availableSeats"))
            or _to_int(_pick(seg, "seats", "Seats", "seatCount", "availableSeats"))
            or 1
        )
        if seats < watcher.seats_required:
            continue

        program = str(
            _pick(raw, "source", "Source", "program", "Program") or watcher.program or "unknown"
        ).lower()
        
        # 取对应舱位的里程成本
        miles = _to_int(_pick(raw, f"{cabin_code}MileageCost", f"{cabin_code}MileageCostRaw", 
                              f"{cabin_code}DirectMileageCost", f"{cabin_code}DirectMileageCostRaw"))
        miles = str(miles) if miles else None
        
        # 取对应舱位的税费，API返回的是美分，转成美元
        taxes = _to_int(_pick(raw, f"{cabin_code}TotalTaxes", f"{cabin_code}TotalTaxesRaw",
                              f"{cabin_code}DirectTotalTaxes", f"{cabin_code}DirectTotalTaxesRaw"))
        if taxes is not None:
            taxes = f"${taxes / 100:.2f}"
        else:
            taxes = None
            
        route = _build_route(origin, destination)

        key = "|".join(
            [
                watcher.id,
                date,
                route,
                cabin,
                flight_no,
                program,
            ]
        )
        payload_hash = hashlib.sha256(
            json.dumps(
                {
                    "key": key,
                    "seats": seats,
                    "miles": miles,
                    "taxes": taxes,
                    "raw": raw,
                },
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

        normalized.append(
            AvailabilityRecord(
                watcher_id=watcher.id,
                key=key,
                date=date,
                route=route,
                cabin=cabin,
                flight_no=flight_no,
                program=program,
                seats=seats,
                miles=miles,
                taxes=taxes,
                source_seen_at=observed_at,
                payload_hash=payload_hash,
                raw=raw,
            )
        )

    # Deduplicate by key, keep the highest seat count.
    deduped: dict[str, AvailabilityRecord] = {}
    for record in normalized:
        existing = deduped.get(record.key)
        if existing is None or record.seats > existing.seats:
            deduped[record.key] = record
    return list(deduped.values())


def process_watcher_records(
    watcher: WatcherConfig,
    records: list[AvailabilityRecord],
    store: Store,
    observed_at: str,
) -> tuple[list[AlertEvent], int]:
    states = store.load_watcher_states(watcher.id)
    alerts: list[AlertEvent] = []
    seen_keys: set[str] = set()

    for rec in records:
        seen_keys.add(rec.key)
        prev = states.get(rec.key)
        prev_state = str(prev.get("availability_state")) if prev else "none"
        prev_seats = _to_int(prev.get("seats")) if prev else None
        should_alert = False
        alert_type = "new"

        if prev_state != "available":
            should_alert = True
            alert_type = "new"
        elif not watcher.alert_new_only:
            should_alert = True
            alert_type = "repeat"
        elif watcher.enhanced_alert_on_seat_increase and prev_seats is not None and rec.seats > prev_seats:
            should_alert = True
            alert_type = "seat_increase"

        if should_alert:
            alerts.append(
                AlertEvent(
                    watcher_id=watcher.id,
                    key=rec.key,
                    alert_type=alert_type,
                    record=rec,
                    previous_seats=prev_seats,
                )
            )
        store.upsert_available(rec, observed_at=observed_at, alerted=should_alert)

    downgraded = store.mark_unseen_as_none(watcher.id, seen_keys, observed_at)
    return alerts, downgraded


def build_alert_message(event: AlertEvent) -> str:
    rec = event.record
    # 把舱位翻译成易懂的中文
    cabin_trans = {
        "economy": "经济舱",
        "premium_economy": "超级经济舱",
        "business": "商务舱（可躺平😎）",
        "first": "头等舱"
    }
    cabin_display = cabin_trans.get(rec.cabin.lower(), rec.cabin)
    
    lines = [
        "🎉 发现可用里程票啦！",
        f"🔍 监控任务: {rec.watcher_id}",
        f"✈️ 航线: {rec.route}",
        f"📅 日期: {rec.date}",
        f"🛏️ 舱位: {cabin_display}",
        f"🏷️ 航司: {rec.program}",
        f"🎫 余票: {rec.seats} 张",
        f"💸 所需里程: {rec.miles or '暂未查到'}",
        f"💳 额外税费: {rec.taxes or '暂未查到'}",
        f"⏰ 抓取时间: {rec.source_seen_at}",
        "⚠️ 小提示：Seats.aero抓取偶尔会有延迟/误报，建议先去官网手动确认有票再转点/下单哦~",
    ]
    if event.alert_type == "seat_increase" and event.previous_seats is not None:
        lines.insert(1, f"🔥 加票提醒：之前只有 {event.previous_seats} 张，现在涨到 {rec.seats} 张啦！")
    return "\n".join(lines)


def _alert_event_payload(event: AlertEvent, watcher: WatcherConfig) -> dict[str, Any]:
    return {
        "watcher_id": event.watcher_id,
        "key": event.key,
        "alert_type": event.alert_type,
        "notify_channel": watcher.notify_channel,
        "notify_target": watcher.notify_target,
        "message": build_alert_message(event),
        "record": {
            "date": event.record.date,
            "route": event.record.route,
            "cabin": event.record.cabin,
            "flight_no": event.record.flight_no,
            "program": event.record.program,
            "seats": event.record.seats,
            "miles": event.record.miles,
            "taxes": event.record.taxes,
            "source_seen_at": event.record.source_seen_at,
        },
    }


def _date_window(days: int) -> tuple[str, str]:
    today = dt.date.today()
    end = today + dt.timedelta(days=max(1, days))
    return today.isoformat(), end.isoformat()


def _watcher_date_window(watcher: WatcherConfig) -> tuple[str, str]:
    fixed_start = watcher.fixed_start_date
    fixed_end = watcher.fixed_end_date
    if fixed_start or fixed_end:
        start = fixed_start or fixed_end
        end = fixed_end or fixed_start
        if start is None or end is None:
            raise RuntimeError(f"Watcher `{watcher.id}` has invalid fixed date range.")
        s = dt.date.fromisoformat(start)
        e = dt.date.fromisoformat(end)
        if e < s:
            raise RuntimeError(
                f"Watcher `{watcher.id}` has fixed_end_date earlier than fixed_start_date."
            )
        return s.isoformat(), e.isoformat()
    return _date_window(watcher.window_days)


def _default_config_path() -> str:
    skill_root = Path(__file__).resolve().parent.parent
    return str(skill_root / "config" / "watchers.yaml")


def _resolve_watchers(
    *,
    store: Store,
    watchers_source: str,
    config_path: Path,
    watcher_id: str | None,
) -> tuple[list[WatcherConfig], str]:
    if watchers_source == "db":
        watchers = store.list_watchers(include_disabled=False)
        return select_watchers(watchers, watcher_id), "db"
    if watchers_source == "config":
        if not config_path.exists():
            raise RuntimeError(f"Config file not found: {config_path}")
        watchers = load_watchers(config_path)
        return select_watchers(watchers, watcher_id), "config"

    # auto mode: prefer DB, fallback to config
    db_watchers = store.list_watchers(include_disabled=False)
    if db_watchers:
        return select_watchers(db_watchers, watcher_id), "db"
    if not config_path.exists():
        return [], "db"
    cfg_watchers = load_watchers(config_path)
    return select_watchers(cfg_watchers, watcher_id), "config"


def fetch_records_for_watcher(client: SeatsClient, watcher: WatcherConfig) -> list[dict[str, Any]]:
    start_date, end_date = _watcher_date_window(watcher)
    merged: list[dict[str, Any]] = []
    for cabin in watcher.cabins:
        records = client.cached_search(
            origin=watcher.origin,
            destination=watcher.destination,
            cabin=cabin,
            start_date=start_date,
            end_date=end_date,
            program=watcher.program,
            airlines=watcher.airlines or None,
        )
        merged.extend(records)
    return merged


def fetch_with_retry(client: SeatsClient, watcher: WatcherConfig) -> list[dict[str, Any]]:
    attempts = watcher.fetch_retries + 1
    last_exc: Exception | None = None
    for idx in range(attempts):
        try:
            data = fetch_records_for_watcher(client, watcher)
            if data or idx == attempts - 1:
                return data
        except SeatsClientError as exc:
            last_exc = exc
            if idx == attempts - 1:
                raise
        time.sleep(max(0, watcher.fetch_retry_delay_seconds))
    if last_exc:
        raise last_exc
    return []


def _all_watchers_rate_limited(summary: dict[str, Any]) -> bool:
    """Check if ALL watchers failed due to rate limiting."""
    watchers = summary.get("watchers", [])
    if not watchers:
        return False

    rate_limit_keywords = ["429", "rate limit", "ratelimit", "too many requests"]

    for w in watchers:
        errors = w.get("errors", [])
        if not errors:
            return False  # At least one watcher succeeded
        has_rate_limit = any(
            kw.lower() in " ".join(errors).lower()
            for kw in rate_limit_keywords
        )
        if not has_rate_limit:
            return False  # At least one watcher failed for a different reason

    return True


def run_with_global_retry(
    *,
    watchers: list[WatcherConfig],
    client: SeatsClient,
    store: Store,
    now_iso: str | None = None,
    global_retry_cooldown: int = 120,
    global_retry_max: int = 1,
) -> dict[str, Any]:
    """Run watchers with global rate-limit retry.

    If ALL watchers hit rate limit, wait cooldown seconds and retry.
    """
    summary = run_once(
        watchers=watchers,
        client=client,
        store=store,
        now_iso=now_iso,
    )

    retry_count = 0
    while retry_count < global_retry_max and _all_watchers_rate_limited(summary):
        retry_count += 1
        print(
            json.dumps(
                {
                    "level": "WARN",
                    "message": f"All watchers hit rate limit. Waiting {global_retry_cooldown}s before global retry {retry_count}/{global_retry_max}...",
                }
            ),
            file=sys.stderr,
        )
        time.sleep(global_retry_cooldown)
        summary = run_once(
            watchers=watchers,
            client=client,
            store=store,
            now_iso=now_iso,
        )

    summary["global_retry_count"] = retry_count
    return summary


def run_once(
    *,
    watchers: list[WatcherConfig],
    client: SeatsClient,
    store: Store,
    now_iso: str | None = None,
) -> dict[str, Any]:
    observed_at = now_iso or _iso_now()
    summary: dict[str, Any] = {
        "checked_watchers": 0,
        "alerts": 0,
        "downgraded_to_none": 0,
        "alert_events": [],
        "watchers": [],
    }

    for watcher in watchers:
        summary["checked_watchers"] += 1
        watcher_item: dict[str, Any] = {
            "id": watcher.id,
            "records": 0,
            "alerts": 0,
            "alert_events": [],
            "errors": [],
        }
        try:
            raw_items = fetch_with_retry(client, watcher)
            watcher_item["records_raw"] = len(raw_items)
            records = normalize_records(raw_items, watcher, observed_at=observed_at)
            watcher_item["records"] = len(records)
            alerts, downgraded = process_watcher_records(
                watcher=watcher,
                records=records,
                store=store,
                observed_at=observed_at,
            )
            watcher_item["alerts"] = len(alerts)
            watcher_item["downgraded_to_none"] = downgraded
            summary["alerts"] += len(alerts)
            summary["downgraded_to_none"] += downgraded

            for event in alerts:
                payload = _alert_event_payload(event, watcher)
                watcher_item["alert_events"].append(payload)
                summary["alert_events"].append(payload)
        except Exception as exc:  # pylint: disable=broad-except
            watcher_item["errors"].append(str(exc))

        summary["watchers"].append(watcher_item)

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Seats.aero watchers and return UNCONFIRMED alert events.")
    parser.add_argument("--config", default=_default_config_path(), help="Path to watchers config (JSON or YAML).")
    parser.add_argument("--watcher", help="Run one watcher id only.")
    parser.add_argument(
        "--watchers-source",
        choices=["auto", "db", "config"],
        default="auto",
        help="Load watchers from db/config. auto means db first, then config fallback.",
    )
    parser.add_argument(
        "--watchers-import",
        action="store_true",
        help="Import watchers from --config into DB and exit.",
    )
    parser.add_argument(
        "--replace-watchers",
        action="store_true",
        help="When used with --watchers-import, replace all existing DB watchers.",
    )
    parser.add_argument(
        "--watchers-list",
        action="store_true",
        help="List watchers from DB and exit.",
    )
    parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include disabled watchers for --watchers-list.",
    )
    parser.add_argument(
        "--state-backend",
        choices=["sqlite", "json"],
        default="sqlite",
        help="Storage backend: sqlite or json",
    )
    parser.add_argument(
        "--state-db",
        default=_default_state_db(),
        help="Path to SQLite state DB (used when --state-backend=sqlite)",
    )
    parser.add_argument(
        "--state-json",
        default=None,
        help="Path to JSON state file (used when --state-backend=json)",
    )
    parser.add_argument(
        "--now-iso",
        help="Override observed timestamp (for tests).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).resolve()

    if args.state_backend == "json":
        if not args.state_json:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": "--state-json is required when --state-backend=json",
                    },
                    ensure_ascii=False,
                )
            )
            return 1
        store: Store = JsonStore(Path(args.state_json).resolve())
    else:
        store = SqliteStore(Path(args.state_db).resolve())

    try:
        if args.watchers_import:
            watchers_from_config = load_watchers(config_path)
            import_summary = store.upsert_watchers(watchers_from_config, replace=bool(args.replace_watchers))
            print(
                json.dumps(
                    {
                        "success": True,
                        "data": {
                            "config_path": str(config_path),
                            "imported_watchers": import_summary,
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if args.watchers_list:
            watchers = store.list_watchers(include_disabled=bool(args.include_disabled))
            print(
                json.dumps(
                    {
                        "success": True,
                        "data": {
                            "count": len(watchers),
                            "watchers": [asdict(item) for item in watchers],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        watchers, watcher_source = _resolve_watchers(
            store=store,
            watchers_source=str(args.watchers_source),
            config_path=config_path,
            watcher_id=args.watcher,
        )
        if not watchers:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": "No enabled watchers selected.",
                        "watchers_source": watcher_source,
                    },
                    ensure_ascii=False,
                )
            )
            return 1

        api_key = os.environ.get("SEATS_AERO_API_KEY", "").strip()
        if not api_key:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": "Missing SEATS_AERO_API_KEY.",
                    },
                    ensure_ascii=False,
                )
            )
            return 1

        client = SeatsClient(api_key=api_key)

        summary = run_with_global_retry(
            watchers=watchers,
            client=client,
            store=store,
            now_iso=args.now_iso,
        )
        summary["watchers_source"] = watcher_source
        print(json.dumps({"success": True, "data": summary}, ensure_ascii=False, indent=2))
        return 0
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
