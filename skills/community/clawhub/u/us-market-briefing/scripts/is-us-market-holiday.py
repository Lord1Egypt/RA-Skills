#!/usr/bin/env python3
import json
import sys
from datetime import date, datetime
from typing import Optional

HOLIDAYS = {
    "2026-01-01": {"status": "closed", "label": "New Year's Day"},
    "2026-01-19": {"status": "closed", "label": "Martin Luther King, Jr. Day"},
    "2026-02-16": {"status": "closed", "label": "Presidents' Day"},
    "2026-04-03": {"status": "closed", "label": "Good Friday"},
    "2026-05-25": {"status": "closed", "label": "Memorial Day"},
    "2026-06-19": {"status": "closed", "label": "Juneteenth"},
    "2026-07-03": {"status": "closed", "label": "Independence Day (Observed)"},
    "2026-09-07": {"status": "closed", "label": "Labor Day"},
    "2026-11-26": {"status": "closed", "label": "Thanksgiving Day"},
    "2026-12-24": {"status": "early-close", "label": "Christmas Eve"},
    "2026-12-25": {"status": "closed", "label": "Christmas Day"},
}

def parse_input(arg: Optional[str]) -> date:
    if not arg:
        return date.today()
    return datetime.strptime(arg, "%Y-%m-%d").date()


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    d = parse_input(arg)
    key = d.isoformat()
    info = HOLIDAYS.get(key)
    if info:
        payload = {"date": key, **info}
    else:
        payload = {"date": key, "status": "open", "label": None}
    print(json.dumps(payload))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
