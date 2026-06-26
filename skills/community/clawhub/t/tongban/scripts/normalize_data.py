#!/usr/bin/env python3
"""Normalize raw Shanghai service item data into JSONL records."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

BASE = "https://zwdt.sh.gov.cn"


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def iter_items(raw: dict) -> list[dict[str, str]]:
    rows = []
    seen = set()
    for bundle in raw.get("records", []):
        department = bundle["department"]
        role = bundle["role"]
        for page in bundle.get("pages", []):
            item_list = page.get("itemList") or {}
            for group_name, items in item_list.items():
                for item in items or []:
                    item_id = clean(item.get("stId"))
                    key = (department["code"], role, item_id)
                    if not item_id or key in seen:
                        continue
                    seen.add(key)
                    st_net = clean(item.get("stNet"))
                    record = {
                        "department_code": department["code"],
                        "department_name": department["name"],
                        "department_short_name": department["short_name"],
                        "role": role,
                        "item_name": clean(item.get("stItemName")) or clean(group_name),
                        "subitem_name": clean(item.get("stSubitemName")) or clean(item.get("stItemName")) or clean(group_name),
                        "item_type": clean(item.get("stItemType")),
                        "st_net": st_net,
                        "online_available": "true" if st_net == "是" else "false",
                        "item_id": item_id,
                        "item_code": clean(item.get("stItemCode")),
                        "source_url": f"{BASE}/govPortals/{'naturalPerson' if role == '个人' else 'legalPerson'}/department",
                        "guide_url": f"{BASE}/govPortals/bsfw/check/{item_id}",
                        "detail_status": "unavailable",
                    }
                    rows.append(record)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = iter_items(raw)
    rows.sort(key=lambda r: (r["department_code"], r["role"], r["item_name"], r["subitem_name"], r["item_id"]))
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} records to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
