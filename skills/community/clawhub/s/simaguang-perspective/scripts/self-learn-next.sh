#!/usr/bin/env bash
# self-learn-next.sh - Print the next unlearned event from the historical event bank.

set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT/references/历史事件库.md" "$ROOT/references/自我学习日志.md" <<'PY'
import sys

def table_rows(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if cols and cols[0] in ("事件", "序号", "---"):
            continue
        if len(cols) >= 4:
            rows.append(cols)
    return rows

events = [row[0] for row in table_rows(sys.argv[1])]
learned = [row[1] for row in table_rows(sys.argv[2]) if row[1] not in ("-", "")]
next_events = [e for e in events if e not in learned]

if next_events:
    print(next_events[0])
else:
    print("ALL_LEARNED")
PY
