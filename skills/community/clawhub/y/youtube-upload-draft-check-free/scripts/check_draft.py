#!/usr/bin/env python3
"""Create a transparent checklist from an offline, visible-page fixture."""
import json
import sys
from pathlib import Path

FIELDS = ("title", "description", "thumbnail", "audience", "visibility", "captions")

def inspect(document):
    if not document.get("owner_confirmed"):
        return {"ok": False, "stop_reason": "所有权未确认：请由账号持有人确认目标账号。"}
    if not document.get("logged_in"):
        return {"ok": False, "stop_reason": "未处于已登录状态：不尝试绕过登录或安全验证。"}
    if not document.get("draft_selected"):
        return {"ok": False, "stop_reason": "稿件选择不明确：请指定唯一草稿或发布目标。"}
    rows = []
    for field in FIELDS:
        entry = document.get("visible_fields", {}).get(field)
        # A missing record, or one without the visible label/path that supports it,
        # is not evidence that a Studio field is empty. Keep its source null rather
        # than inventing a page source, and make the limitation explicit.
        if not entry or not entry.get("source"):
            rows.append({"field": field, "value": None, "status": "无法核验", "source": None})
        elif not entry.get("value"):
            rows.append({"field": field, "value": "未显示", "status": "缺失", "source": entry["source"]})
        else:
            rows.append({"field": field, "value": entry["value"], "status": "已核对", "source": entry["source"]})
    return {"ok": True, "mode": "offline-fixture", "rows": rows, "missing": [r["field"] for r in rows if r["status"] == "缺失"]}

def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: check_draft.py <离线页面资料.json>")
    with Path(sys.argv[1]).open(encoding="utf-8") as handle:
        print(json.dumps(inspect(json.load(handle)), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
