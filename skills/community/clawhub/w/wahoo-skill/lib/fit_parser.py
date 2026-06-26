"""FIT file parser using `fitparse`.

Extracts a session-level summary plus per-second records (power, cadence,
HR, GPS). Lazy-imports fitparse so the module is loadable without the
dependency installed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator


def _semicircles_to_deg(value: int | None) -> float | None:
    if value is None:
        return None
    return value * (180.0 / 2**31)


def _ensure_fitparse():
    try:
        import fitparse  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "fitparse not installed. Run: pip install --user 'fitparse>=1.2,<2'"
        ) from e
    return fitparse


def parse(path: str | Path) -> dict[str, Any]:
    fitparse = _ensure_fitparse()
    fit = fitparse.FitFile(str(path))

    session = _first_session(fit)
    records = list(_iter_records(fit))
    lap_data = list(_iter_laps(fit))

    # Session-level power zone distribution
    tz_s = session.get("time_in_power_zone") if session else None
    sz = [float(x) for x in tz_s[:6]] if isinstance(tz_s, tuple) and len(tz_s) >= 6 else [None] * 6

    summary = {
        "fit_path": str(path),
        "start_time": _iso(session.get("start_time")) if session else None,
        "total_elapsed_time_s": _f(session, "total_elapsed_time"),
        "total_timer_time_s": _f(session, "total_timer_time"),
        "total_distance_m": _f(session, "total_distance"),
        "total_ascent_m": _f(session, "total_ascent"),
        "total_descent_m": _f(session, "total_descent"),
        "avg_speed_ms": _f(session, "avg_speed"),
        "max_speed_ms": _f(session, "max_speed"),
        "avg_power_w": _f(session, "avg_power"),
        "max_power_w": _f(session, "max_power"),
        "normalized_power_w": _f(session, "normalized_power"),
        "threshold_power_w": _f(session, "threshold_power"),
        "training_stress_score": _f(session, "training_stress_score"),
        "intensity_factor": _f(session, "intensity_factor"),
        "avg_heart_rate": _f(session, "avg_heart_rate"),
        "max_heart_rate": _f(session, "max_heart_rate"),
        "avg_cadence": _f(session, "avg_cadence"),
        "max_cadence": _f(session, "max_cadence"),
        "total_calories": _f(session, "total_calories"),
        "num_laps": _f(session, "num_laps"),
        "avg_altitude_m": _f(session, "enhanced_avg_altitude") or _f(session, "avg_altitude"),
        "max_altitude_m": _f(session, "enhanced_max_altitude") or _f(session, "max_altitude"),
        "min_altitude_m": _f(session, "enhanced_min_altitude") or _f(session, "min_altitude"),
        "avg_grade": _f(session, "avg_grade"),
        "max_pos_grade": _f(session, "max_pos_grade"),
        "max_neg_grade": _f(session, "max_neg_grade"),
        "avg_temperature": _f(session, "avg_temperature"),
        "max_temperature": _f(session, "max_temperature"),
        "left_right_balance": _f(session, "left_right_balance"),
        "session_time_in_zone1": sz[0],
        "session_time_in_zone2": sz[1],
        "session_time_in_zone3": sz[2],
        "session_time_in_zone4": sz[3],
        "session_time_in_zone5": sz[4],
        "session_time_in_zone6": sz[5],
        "sport": session.get("sport") if session else None,
        "sub_sport": session.get("sub_sport") if session else None,
        "record_count": len(records),
    }
    return {
        "summary": summary,
        "records": records,
        "laps": lap_data,
        "devices": list(_iter_devices(fit)),
        "zones": list(_iter_zones(fit)),
    }


def _first_session(fit) -> dict | None:
    for msg in fit.get_messages("session"):
        return {f.name: f.value for f in msg.fields}
    return None


def _iter_records(fit) -> Iterator[dict]:
    for msg in fit.get_messages("record"):
        d: dict[str, Any] = {}
        for f in msg.fields:
            v = f.value
            if f.name in ("position_lat", "position_long"):
                v = _semicircles_to_deg(v) if isinstance(v, int) else v
            elif f.name == "timestamp":
                v = _iso(v)
            d[f.name] = v
        yield d


def _iter_laps(fit) -> Iterator[dict]:
    for msg in fit.get_messages("lap"):
        d: dict[str, Any] = {}
        tz = None
        for f in msg.fields:
            if f.name == "time_in_power_zone":
                v = f.value
                if isinstance(v, tuple) and len(v) == 6:
                    tz = [float(x) for x in v]
                elif isinstance(v, int):
                    tz = [float(v)] + [0.0] * 5
                continue
            v = f.value
            if f.name == "timestamp":
                d["end_time"] = _iso(v)
            elif f.name == "start_time":
                d["start_time"] = _iso(v)
            elif f.name == "lap_trigger":
                d[f.name] = str(v) if v is not None else None
            else:
                d[f.name] = _f_safe(v)
        for i, key in enumerate(
            ["time_in_zone1", "time_in_zone2", "time_in_zone3",
             "time_in_zone4", "time_in_zone5", "time_in_zone6"]
        ):
            d[key] = tz[i] if tz else None
        yield d


def _iter_devices(fit) -> Iterator[dict]:
    for msg in fit.get_messages("device_info"):
        d: dict[str, Any] = {}
        for f in msg.fields:
            if f.name == "timestamp":
                d["timestamp"] = _iso(f.value)
            else:
                d[f.name] = f.value
        yield d


def _iter_zones(fit) -> Iterator[dict]:
    for zone_type, msg_name, value_field in (
        ("hr", "hr_zone", "high_bpm"),
        ("power", "power_zone", "high_value"),
    ):
        for msg in fit.get_messages(msg_name):
            d = {f.name: f.value for f in msg.fields}
            yield {
                "zone_type": zone_type,
                "zone_number": d.get("message_index"),
                "high_value": _f_safe(d.get(value_field)),
            }


def _f(session: dict | None, key: str) -> float | None:
    if not session:
        return None
    v = session.get(key)
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _f_safe(v) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _iso(dt) -> str | None:
    if dt is None:
        return None
    try:
        return dt.isoformat()
    except AttributeError:
        return str(dt)


if __name__ == "__main__":
    import argparse
    import json
    import sys

    p = argparse.ArgumentParser(description="Parse a FIT file")
    p.add_argument("fit", help="Path to .fit file")
    p.add_argument(
        "--summary-only", action="store_true", help="Skip per-second records"
    )
    args = p.parse_args()

    out = parse(args.fit)
    if args.summary_only:
        out = {"summary": out["summary"]}
    json.dump(out, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")
