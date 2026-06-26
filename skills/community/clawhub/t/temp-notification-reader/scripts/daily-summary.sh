#!/bin/bash
# Daily Notification Summary
# Run daily to write daily notification summary to memory
# Part of: https://github.com/gift-is-coding/macos-notification-reader

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIF_SCRIPT="$SCRIPT_DIR/read_notifications.py"
TODAY=$(date +%Y-%m-%d)

# Default to OpenClaw memory directory
if [ -z "$MEMORY_DIR" ]; then
    if [ -d "$HOME/.openclaw/workspace/memory" ]; then
        MEMORY_DIR="$HOME/.openclaw/workspace/memory"
    else
        MEMORY_DIR="./output"
    fi
fi

OUTPUT_FILE="/tmp/notif_summary_$TODAY.txt"

mkdir -p "$MEMORY_DIR"

# Read today's notifications (last 24 hours)
python3 $NOTIF_SCRIPT --hours 24 > "$OUTPUT_FILE" 2>/dev/null

if [ ! -s "$OUTPUT_FILE" ]; then
    echo "No notifications recorded today."
    exit 0
fi

# Count notifications by app
python3 << EOF
import re
from collections import Counter

with open("$OUTPUT_FILE", 'r') as f:
    content = f.read()

# Parse notifications
apps = []
messages = []
for line in content.strip().split('\n'):
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            app = parts[1].strip().split('[')[0].strip()
            msg = parts[2].strip()
            apps.append(app)
            messages.append(msg)

if not apps:
    print("No valid notifications")
    exit(0)

# Count
app_count = Counter(apps)

# Write to daily memory
memory_file = "$MEMORY_DIR/$TODAY.md"

existing = ""
try:
    with open(memory_file, 'r') as f:
        existing = f.read()
except:
    pass

# Chinese + English
if "## 今日通知 / Today's Notifications" in existing:
    import re
    pattern = r"## 今日通知 / Today's Notifications[\s\S]*?(?=\n## |\Z)"
    new_section = f"""## 今日通知 / Today's Notifications

- 条数 / Count: {len(apps)}
- 应用分布 / Apps: {', '.join([f'{k}({v})' for k,v in app_count.most_common(10)])}"""
    existing = re.sub(pattern, new_section, existing)
else:
    new_section = f"""

## 今日通知 / Today's Notifications

- 条数 / Count: {len(apps)}
- 应用分布 / Apps: {', '.join([f'{k}({v})' for k,v in app_count.most_common(10)])}

### 重要通知 / Important

"""
    # Take top 5 non-system notifications
    important = [m for m in messages if len(m) > 10][:5]
    new_section += '\n'.join([f"- {m[:100]}" for m in important])
    existing += f"\n{new_section}"

with open(memory_file, 'w') as f:
    f.write(existing)

print(f"Updated: {memory_file}")
print(f"Today's notifications: {len(apps)} items")
EOF

rm -f "$OUTPUT_FILE"
