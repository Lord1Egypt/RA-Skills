#!/bin/bash
# Screen Activity Tracker (Lite)
# Capture screenshot → analyze with VL model → log to local markdown
set +e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$SKILL_DIR/config.json"
LOG_DIR="$HOME/screen-activity"
mkdir -p "$LOG_DIR"

# Load config, use defaults if missing
MLX_URL=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('mlx_url','http://192.168.1.198:18000/v1'))" 2>/dev/null || echo "http://192.168.1.198:18000/v1")
KEEP_DAYS=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('keep_days',7))" 2>/dev/null || echo "7")

NOW=$(date "+%Y-%m-%d %H:%M:%S")
DATE_STR=$(date "+%Y-%m-%d")
TIME_STR=$(date "+%H:%M")

SCREENSHOT_DIR="$LOG_DIR/screenshots/$DATE_STR"
mkdir -p "$SCREENSHOT_DIR"

TS=$(date "+%Y%m%d_%H%M%S")
SCREENSHOT="$SCREENSHOT_DIR/${TS}.png"

# Step 1: Capture screenshot
export PATH="$HOME/.npm-global/bin:$PATH"
if command -v peekaboo &>/dev/null; then
    peekaboo image --mode screen --path "$SCREENSHOT" --format png 2>/dev/null
else
    echo "[$(date '+%H:%M')] peekaboo not found, skipping screenshot"
    python3 "$SKILL_DIR/scripts/activity-logger.py" "NONE" "$DATE_STR" "$TIME_STR" "🛑 peekaboo 未安装，无法截图"
    exit 0
fi

if [ ! -f "$SCREENSHOT" ]; then
    echo "[$(date '+%H:%M')] Screenshot failed, logging text-only"
    APP_NAME=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null || echo "未知")
    python3 "$SKILL_DIR/scripts/activity-logger.py" "NONE" "$DATE_STR" "$TIME_STR" "🛑 截图失败 ($APP_NAME)"
    exit 0
fi

# Step 2: Analyze with VL model
DESCRIPTION=$(python3 -c "
import json, base64, urllib.request, sys

with open('$SCREENSHOT', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

prompt = '用一句简短中文描述这张屏幕截图，格式：[应用名] 简短描述用户在做什么。只输出描述，不要额外解释。'

payload = {
    'model': 'Qwen3.5-9B-MLX-4bit',
    'messages': [{
        'role': 'user',
        'content': [
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}},
            {'type': 'text', 'text': prompt}
        ]
    }],
    'max_tokens': 80,
    'temperature': 0.3
}

try:
    req = urllib.request.Request(
        '$MLX_URL/chat/completions',
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer placeholder'},
        method='POST'
    )
    resp = urllib.request.urlopen(req, timeout=60)
    data = json.loads(resp.read())
    content = data['choices'][0]['message']['content'].strip()
    print(content)
except Exception as e:
    print(f'分析失败: {str(e)[:80]}')
" 2>&1)

# Step 3: Log to local markdown
python3 "$SKILL_DIR/scripts/activity-logger.py" "$SCREENSHOT" "$DATE_STR" "$TIME_STR" "$DESCRIPTION"

# Step 4: Cleanup old screenshots
if [ "$KEEP_DAYS" -gt 0 ] 2>/dev/null; then
    find "$LOG_DIR/screenshots" -maxdepth 1 -type d -mtime +"$KEEP_DAYS" -exec rm -rf {} \; 2>/dev/null
fi
