#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

API_URL = "https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true"
DEFAULT_API_KEY = None
BEIJING_TZ = timezone(timedelta(hours=8))


def beijing_now() -> datetime:
    return datetime.now(BEIJING_TZ)


def fmt_ts(ts_ms):
    if not ts_ms:
        return None
    return datetime.fromtimestamp(int(ts_ms) / 1000, tz=BEIJING_TZ).strftime("%H:%M")


def round_info(now: datetime):
    day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if now < day_start:
        return {
            "current": 0,
            "total": 4,
            "status": "not_open",
            "label": "未开放",
            "countdown": "尚未开市",
        }

    delta_seconds = int((now - day_start).total_seconds())
    idx = (delta_seconds // (4 * 3600)) + 1
    if idx > 4:
        return {
            "current": 4,
            "total": 4,
            "status": "closed",
            "label": "第4轮结束后",
            "countdown": "今日已收市",
        }

    round_end = day_start + timedelta(hours=idx * 4)
    remaining = round_end - now
    hours, rem = divmod(int(remaining.total_seconds()), 3600)
    minutes, _ = divmod(rem, 60)
    countdown = f"{hours}小时{minutes}分钟" if hours > 0 else f"{minutes}分钟"
    return {
        "current": idx,
        "total": 4,
        "status": "open",
        "label": f"第{idx}轮",
        "countdown": countdown,
    }


def pick_activity(payload: dict):
    activities = payload.get("merchantActivities") or []
    return activities[0] if activities else {}


def extract_active_items(activity: dict, now_ms: int):
    items = (activity.get("get_props") or []) + (activity.get("get_pets") or [])
    active = []
    for item in items:
        start = item.get("start_time")
        end = item.get("end_time")
        if start and end:
            if not (int(start) <= now_ms < int(end)):
                continue
            time_label = f"{fmt_ts(start)} - {fmt_ts(end)}"
        else:
            time_label = "全天供应"

        active.append(
            {
                "name": item.get("name") or "未知",
                "kind": "pet" if item in (activity.get("get_pets") or []) else "prop",
                "image": item.get("icon_url") or "",
                "start_time": int(start) if start else None,
                "end_time": int(end) if end else None,
                "time_label": time_label,
            }
        )
    return active


def fetch(api_key: str):
    resp = requests.get(API_URL, headers={"X-API-Key": api_key}, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code") != 0:
        raise RuntimeError(payload.get("message") or "API returned non-zero code")
    return payload.get("data") or {}


def build_result(raw: dict):
    now = beijing_now()
    now_ms = int(now.timestamp() * 1000)
    activity = pick_activity(raw)
    items = extract_active_items(activity, now_ms)
    result = {
        "source": API_URL,
        "merchant_name": activity.get("name") or "远行商人",
        "subtitle": activity.get("start_date") or "每日 08:00 / 12:00 / 16:00 / 20:00 刷新",
        "fetched_at": now.isoformat(),
        "round": round_info(now),
        "item_count": len(items),
        "items": items,
    }
    return result


def print_text(result: dict):
    print(f"{result['merchant_name']}库存")
    print(f"时间: {result['fetched_at']}")
    print(f"轮次: {result['round']['label']} / {result['round']['countdown']}")
    print(f"数量: {result['item_count']}")
    if not result["items"]:
        print("当前没有处于本轮有效期内的商品。")
        return
    print("")
    for idx, item in enumerate(result["items"], start=1):
        print(f"{idx}. {item['name']} ({item['time_label']})")


def main():
    parser = argparse.ArgumentParser(description="Fetch current Roco merchant inventory")
    parser.add_argument("--api-key", default=os.environ.get("ROCOM_API_KEY") or DEFAULT_API_KEY)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    if not args.api_key:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "缺少 API key。请设置 ROCOM_API_KEY 或使用 --api-key，并从 https://github.com/Entropy-Increase-Team/ 获取可用 key。",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        raw = fetch(args.api_key)
        result = build_result(raw)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        if args.pretty:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
