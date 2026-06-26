#!/bin/bash
# Work Notification Summary
# Usage: WORK_LOOKBACK_MINUTES=180 ./work-summary.sh
# Part of: https://github.com/gift-is-coding/macos-notification-reader

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIF_SCRIPT="$SCRIPT_DIR/read_notifications.py"
TODAY=$(date +%Y-%m-%d)
TS=$(date +%Y%m%d-%H%M%S)
LOOKBACK_MINUTES="${WORK_LOOKBACK_MINUTES:-180}"

# Default output to OpenClaw memory directory
if [ -z "$OUTPUT_DIR" ]; then
    if [ -d "$HOME/.openclaw/workspace/memory" ]; then
        OUTPUT_DIR="$HOME/.openclaw/workspace/memory/$TODAY/computer_io/notification"
    else
        OUTPUT_DIR="./output/$TODAY/computer_io/notification"
    fi
fi

mkdir -p "$OUTPUT_DIR"

TMP_RAW="/tmp/work_notif_raw_$TS.txt"
OUT_MD="$OUTPUT_DIR/work-summary-$TS.md"

python3 "$NOTIF_SCRIPT" --minutes "$LOOKBACK_MINUTES" --output "$TMP_RAW" 2>/dev/null

python3 - "$TMP_RAW" "$OUT_MD" "$LOOKBACK_MINUTES" << 'PYEOF'
import re
import sys
from collections import defaultdict
from pathlib import Path

raw_file = Path(sys.argv[1])
out_file = Path(sys.argv[2])
lookback = sys.argv[3]

work_apps = {
    'Teams': 'teams',
    'Outlook': 'outlook',
    'WeChat': 'wechat',
    'xinwechat': 'wechat',
}

action_kw = [
    '待办', 'todo', 'action item', 'follow up', 'follow-up', '请', '截止', 'deadline',
    'review', '审批', 'approve', '确认', '提醒', '会议', 'meeting', 'sync', 'blocker',
    'request', 'need', 'required', 'urgent', 'important',
]

lines = []
if raw_file.exists():
    txt = raw_file.read_text(encoding='utf-8', errors='ignore')
    for ln in txt.splitlines():
        if '|' in ln and not ln.startswith('==='):
            lines.append(ln)

by_app = defaultdict(list)
all_work = []
for ln in lines:
    parts = [x.strip() for x in ln.split('|', 2)]
    if len(parts) < 3:
        continue
    t, app, msg = parts
    app_norm = app.lower()

    selected = None
    for k, v in work_apps.items():
        if k.lower() in app_norm:
            selected = v
            break

    # WeChat: only keep work-related notifications
    if selected == 'wechat':
        if not re.search(r'project|meeting|review|approval|budget|team|review|urgent', msg, re.I):
            continue

    if selected:
        by_app[selected].append((t, msg))
        all_work.append((t, selected, msg))

# Deduplicate
seen = set()
uniq = []
for t, a, m in all_work:
    key = (a, m)
    if key in seen:
        continue
    seen.add(key)
    uniq.append((t, a, m))

# Extract action items
pending = []
for t, a, m in uniq:
    mm = m.lower()
    if any(k in mm for k in action_kw):
        pending.append((t, a, m))

out = []
out.append('# Work Notification Summary / 工作通知摘要')
out.append(f'- Time Range: 过去 {lookback} 分钟 / Last {lookback} minutes')
out.append(f'- Total Work Notifications: {len(uniq)} 条 / items')
out.append('')
out.append('## 渠道分布 / Channel Distribution')
out.append(f"- Teams: {len(by_app.get('teams', []))}")
out.append(f"- Outlook: {len(by_app.get('outlook', []))}")
out.append(f"- WeChat (工作相关 / Work-related): {len(by_app.get('wechat', []))}")
out.append('')
out.append('## 待处理事项 / Action Items (自动提取 / Auto-extracted)')
if pending:
    for t, a, m in pending[:20]:
        out.append(f"- [{t}] ({a}) {m[:180]}")
else:
    out.append('- 暂未识别到明确待处理项 / No clear action items identified')

out.append('')
out.append('## 最近工作通知 / Recent Work Notifications (去重后 / Deduplicated)')
if uniq:
    for t, a, m in uniq[:30]:
        out.append(f"- [{t}] ({a}) {m[:180]}")
else:
    out.append('- 无 / None')

out_file.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(str(out_file))
PYEOF

rm -f "$TMP_RAW"
echo "Saved: $OUT_MD"
