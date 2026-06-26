#!/usr/bin/env python3
"""
parse_schedule.py — Parse staff shift schedules from various formats into structured JSON

Usage:
    python3 parse_schedule.py --input schedule.csv [--format csv|text|excel]
                               [--output schedule.json] [--validate]

Output: Structured schedule JSON (see schedule-formats.md)
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# ─── CSV/Excel Parser ─────────────────────────────────────────────────────────

COLUMN_ALIASES = {
    "date": ["date", "日期", "班次日期"],
    "staff_id": ["staff_id", "工号", "员工编号", "id"],
    "staff_name": ["staff_name", "姓名", "员工姓名", "name", "名字"],
    "start_time": ["start_time", "上班时间", "开始时间", "start", "上班"],
    "end_time": ["end_time", "下班时间", "结束时间", "end", "下班"],
    "location": ["location", "岗位", "位置", "工位"],
    "role": ["role", "角色", "职位", "岗位名称"],
    "on_call": ["on_call", "值班", "备班"],
    "manager_on_duty": ["manager_on_duty", "值班店长", "当班主管"],
}

def normalize_col(name: str) -> str:
    name_strip = name.strip()
    for standard, aliases in COLUMN_ALIASES.items():
        if name_strip in aliases or name_strip.lower() in [a.lower() for a in aliases]:
            return standard
    return name_strip.lower().replace(" ", "_")


def parse_csv_excel(filepath: str) -> list:
    if not HAS_PANDAS:
        raise ImportError("pandas required: pip install pandas openpyxl")
    ext = Path(filepath).suffix.lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath, dtype=str)
    else:
        df = pd.read_csv(filepath, dtype=str)
    df.columns = [normalize_col(c) for c in df.columns]

    shifts = []
    for i, row in df.iterrows():
        shift = {
            "shift_id": f"s{i+1:04d}",
            "date": str(row.get("date", "")).strip(),
            "staff_id": str(row.get("staff_id", f"staff_{i+1}")).strip(),
            "staff_name": str(row.get("staff_name", "")).strip(),
            "start_time": str(row.get("start_time", "")).strip(),
            "end_time": str(row.get("end_time", "")).strip(),
            "location": str(row.get("location", "")).strip() or "门店",
            "role": str(row.get("role", "")).strip() or "员工",
            "on_call": str(row.get("on_call", "")).strip().lower() in ("true", "是", "1", "yes"),
            "manager_on_duty": str(row.get("manager_on_duty", "")).strip().lower() in ("true", "是", "1", "yes"),
        }
        # Skip empty rows
        if not shift["date"] or not shift["staff_name"]:
            continue
        shifts.append(shift)
    return shifts


# ─── Text Parser ──────────────────────────────────────────────────────────────

def parse_text_schedule(text: str) -> list:
    """Parse informal Chinese text schedule."""
    shifts = []
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    current_date = None
    shift_id = 1

    # Date patterns
    date_patterns = [
        r"(\d{4})[年/\-](\d{1,2})[月/\-](\d{1,2})",  # 2024年7月15日 / 2024/7/15
        r"(\d{1,2})[月/](\d{1,2})[日号]?",             # 7月15日
    ]

    # Shift time patterns
    time_pattern = re.compile(r"(\d{1,2}:\d{2})[–\-~到至](\d{1,2}:\d{2})")
    name_pattern = re.compile(r"[：:]\s*(.+)")

    for line in lines:
        # Try to detect date
        for pat in date_patterns:
            m = re.search(pat, line)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    current_date = f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
                elif len(groups) == 2:
                    year = datetime.now().year
                    current_date = f"{year}-{int(groups[0]):02d}-{int(groups[1]):02d}"
                break

        if not current_date:
            continue

        # Try to detect time range in line
        time_match = time_pattern.search(line)
        if not time_match:
            continue

        start_time, end_time = time_match.groups()

        # Extract names (after ：or :)
        name_match = name_pattern.search(line)
        if not name_match:
            continue

        names_str = name_match.group(1)
        # Strip leading time-like artifacts (e.g. "00-19:00）：" prefix)
        names_str = re.sub(r"^[\d:：\-–~）\)）\s]+", "", names_str).strip()
        # Split by common delimiters
        names = [n.strip() for n in re.split(r"[,，、 ]+", names_str) if n.strip()]

        # Detect if this line mentions manager
        is_manager = any(kw in line for kw in ["店长", "经理", "主管"])

        for name in names:
            # Skip annotation words
            if any(kw in name for kw in ["早班", "晚班", "全天", "班", "值班"]):
                continue
            shifts.append({
                "shift_id": f"s{shift_id:04d}",
                "date": current_date,
                "staff_id": re.sub(r"[^\w]", "_", name).lower(),
                "staff_name": name,
                "start_time": start_time,
                "end_time": end_time,
                "location": "门店",
                "role": "店长" if is_manager else "员工",
                "on_call": False,
                "manager_on_duty": is_manager,
            })
            shift_id += 1

    return shifts


# ─── Validation ───────────────────────────────────────────────────────────────

def validate_schedule(shifts: list) -> list:
    """Return list of validation warnings."""
    warnings = []

    # Check for overlapping shifts per staff per day
    from collections import defaultdict
    by_staff_day = defaultdict(list)
    for s in shifts:
        key = (s["staff_id"], s["date"])
        by_staff_day[key].append(s)

    for (staff_id, date), staff_shifts in by_staff_day.items():
        if len(staff_shifts) > 1:
            # Simple overlap check
            for i, a in enumerate(staff_shifts):
                for b in staff_shifts[i+1:]:
                    if a["start_time"] < b["end_time"] and b["start_time"] < a["end_time"]:
                        warnings.append(
                            f"⚠️ 排班冲突：{staff_shifts[0]['staff_name']} 在 {date} 有时间重叠"
                        )

    # Check for manager coverage
    by_date = defaultdict(list)
    for s in shifts:
        by_date[s["date"]].append(s)

    for date, day_shifts in by_date.items():
        has_manager = any(s.get("manager_on_duty") for s in day_shifts)
        if not has_manager:
            warnings.append(f"⚠️ {date} 没有指定值班店长")

    # Check minimum staff per day
    for date, day_shifts in by_date.items():
        if len(day_shifts) < 2:
            warnings.append(f"⚠️ {date} 在班人数不足（仅{len(day_shifts)}人）")

    return warnings


# ─── Build final schedule object ──────────────────────────────────────────────

def build_schedule(shifts: list, source_file: str) -> dict:
    if not shifts:
        return {"shifts": [], "period": {}, "manager_on_duty": {}, "meta": {"source": source_file}}

    dates = sorted(set(s["date"] for s in shifts))
    manager_map = {}
    for s in shifts:
        if s.get("manager_on_duty") and s["date"] not in manager_map:
            manager_map[s["date"]] = {
                "staff_id": s["staff_id"],
                "name": s["staff_name"],
            }

    return {
        "schedule_id": f"schedule_{dates[0]}",
        "period": {"start": dates[0], "end": dates[-1]},
        "shifts": shifts,
        "manager_on_duty": manager_map,
        "meta": {
            "source": source_file,
            "total_shifts": len(shifts),
            "total_staff": len(set(s["staff_id"] for s in shifts)),
            "days_covered": len(dates),
        }
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Parse staff schedule into structured JSON")
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", default="auto", choices=["auto", "csv", "excel", "text"])
    parser.add_argument("--output", default=None)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format
    if fmt == "auto":
        ext = input_path.suffix.lower()
        fmt = "excel" if ext in (".xlsx", ".xls") else "csv" if ext == ".csv" else "text"

    if fmt in ("csv", "excel"):
        shifts = parse_csv_excel(str(input_path))
    else:
        raw = input_path.read_text(encoding="utf-8")
        shifts = parse_text_schedule(raw)

    schedule = build_schedule(shifts, input_path.name)

    if args.validate:
        warnings = validate_schedule(shifts)
        schedule["validation_warnings"] = warnings
        if warnings:
            for w in warnings:
                print(w, file=sys.stderr)

    output_json = json.dumps(schedule, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"✅ Parsed {len(shifts)} shifts → {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
