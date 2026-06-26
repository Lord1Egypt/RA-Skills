#!/usr/bin/env python3
"""Wellness digest builder.

This script merges multiple normalized daily JSON documents (from Tier 1 source
skills and/or Tier 2 bridge payloads) into one combined daily wellness document,
then renders a short digest.

Design goals:
- Source-agnostic: input docs already normalized by their source skills.
- Safe defaults: missing fields are fine.
- Channel-safe rendering (no tables).

Usage examples:

  # Merge a few daily docs you produced earlier
  python3 scripts/wellness_digest.py --date today \
    --in /tmp/whoop_today.json --in /tmp/strava_today.json --in /tmp/withings_today.json \
    --out /tmp/wellness_today.json --render markdown --channel discord

  # Include the newest Tier-2 bridge inbox payload for the day (if present)
  python3 scripts/wellness_digest.py --date today --use-bridge \
    --out /tmp/wellness_today.json --render markdown

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


DEFAULT_BRIDGE_DIR = os.path.expanduser("~/.config/openclaw/wellness/bridge")


def _tzinfo(tz_name: str):
    if ZoneInfo is None:
        return None
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return None


def resolve_date(s: str, tz_name: str) -> str:
    s = s.strip().lower()
    tz = _tzinfo(tz_name)
    now = datetime.now(tz) if tz else datetime.now()
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    datetime.strptime(s, "%Y-%m-%d")
    return s


def load_json(path: str) -> Dict[str, Any]:
    return json.load(open(path, "r", encoding="utf-8"))


def deep_merge(base: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    """Merge incoming into base (dicts recursively, arrays concatenated)."""
    for k, v in incoming.items():
        if k not in base:
            base[k] = v
            continue
        if isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
            continue
        if isinstance(base[k], list) and isinstance(v, list):
            base[k] = base[k] + v
            continue
        # Prefer non-null values
        if base[k] is None and v is not None:
            base[k] = v
        # Otherwise keep base
    return base


def newest_bridge_payload_for_date(date_yyyy_mm_dd: str, bridge_dir: str) -> Optional[str]:
    day_dir = Path(bridge_dir) / "inbox" / date_yyyy_mm_dd
    if not day_dir.exists() or not day_dir.is_dir():
        return None
    files = sorted([p for p in day_dir.glob("*.json") if p.is_file()], key=lambda p: p.stat().st_mtime)
    return str(files[-1]) if files else None


def style(channel: str, markdown: bool) -> Dict[str, str]:
    c = (channel or "generic").lower()
    if not markdown or c == "telegram":
        return {"md": "0", "bL": "", "bR": "", "bullet": "-"}
    if c in ("slack", "whatsapp"):
        return {"md": "1", "bL": "*", "bR": "*", "bullet": "-"}
    return {"md": "1", "bL": "**", "bR": "**", "bullet": "-"}


def render_digest(doc: Dict[str, Any], fmt: str, channel: str) -> str:
    md = fmt == "markdown"
    st = style(channel, md)

    def b(s: str) -> str:
        return f"{st['bL']}{s}{st['bR']}" if st["md"] == "1" and st["bL"] else s

    date = doc.get("date") or "(unknown date)"
    sleep = doc.get("sleep") or {}
    rec = doc.get("recovery") or {}
    act = doc.get("activity") or {}
    body = doc.get("body") or {}
    vit = doc.get("vitals") or {}
    tr = doc.get("training") or {}
    workouts = tr.get("workouts") if isinstance(tr, dict) else None
    if not isinstance(workouts, list):
        workouts = []

    lines = [b(f"Wellness — {date}")]

    if sleep.get("duration_minutes") is not None:
        score = sleep.get("score")
        if score is not None:
            lines.append(f"{st['bullet']} Sleep: {sleep.get('duration_minutes')} min (score {score})")
        else:
            lines.append(f"{st['bullet']} Sleep: {sleep.get('duration_minutes')} min")

    if rec.get("score") is not None:
        bits = [f"Recovery: {rec.get('score')}"]
        if rec.get("hrv_ms") is not None:
            bits.append(f"HRV {rec.get('hrv_ms')} ms")
        if rec.get("resting_hr_bpm") is not None:
            bits.append(f"RHR {rec.get('resting_hr_bpm')} bpm")
        lines.append(f"{st['bullet']} " + " | ".join(bits))

    if act.get("steps") is not None:
        bits = [f"Steps {act.get('steps')}"]
        if act.get("distance_km") is not None:
            bits.append(f"{act.get('distance_km')} km")
        if act.get("active_calories_kcal") is not None:
            bits.append(f"{act.get('active_calories_kcal')} kcal")
        lines.append(f"{st['bullet']} Activity: " + " | ".join(bits))

    if workouts:
        lines.append(f"{st['bullet']} Workouts: {len(workouts)}")

    if body.get("weight_kg") is not None:
        lines.append(f"{st['bullet']} Weight: {body.get('weight_kg')} kg")

    if vit.get("bp_systolic") is not None or vit.get("bp_diastolic") is not None:
        lines.append(f"{st['bullet']} BP: {vit.get('bp_systolic','—')}/{vit.get('bp_diastolic','—')}")

    if len(lines) == 1:
        lines.append(f"{st['bullet']} No data sources provided")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--tz", default=os.environ.get("WELLNESS_TZ", "Asia/Shanghai"))
    ap.add_argument("--in", dest="inputs", action="append", default=[], help="Path to a normalized daily JSON file")
    ap.add_argument("--use-bridge", action="store_true", help="Also include newest Tier2 bridge payload for the day")
    ap.add_argument("--bridge-dir", default=os.environ.get("WELLNESS_BRIDGE_DIR", DEFAULT_BRIDGE_DIR))
    ap.add_argument("--out", default=None, help="Write merged wellness JSON to this path")
    ap.add_argument("--render", choices=["none", "text", "markdown"], default="markdown")
    ap.add_argument("--channel", default="generic")
    args = ap.parse_args()

    day = resolve_date(args.date, args.tz)

    docs: List[Dict[str, Any]] = []
    for p in args.inputs:
        docs.append(load_json(p))

    if args.use_bridge:
        bp = newest_bridge_payload_for_date(day, args.bridge_dir)
        if bp:
            d = load_json(bp)
            # If payload isn't already in wellness-like schema, still merge conservatively.
            docs.append(d)

    merged: Dict[str, Any] = {
        "date": day,
        "timezone": args.tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sources_present": [],
    }

    for d in docs:
        sp = d.get("sources_present")
        if isinstance(sp, list):
            merged.setdefault("sources_present", [])
            merged["sources_present"] = sorted(set(list(merged.get("sources_present") or []) + [str(x) for x in sp]))
        deep_merge(merged, d)

    # If Tier2 payload used `source`, keep it in sources_present.
    src = merged.get("source")
    if isinstance(src, str):
        merged["sources_present"] = sorted(set(list(merged.get("sources_present") or []) + [src]))

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        json.dump(merged, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
        open(args.out, "a", encoding="utf-8").write("\n")

    if args.render != "none":
        print(render_digest(merged, args.render, args.channel), end="")


if __name__ == "__main__":
    main()
