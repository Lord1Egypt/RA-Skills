#!/bin/bash
# Screen Activity Tracker v3
# Screenshot → VL analysis → log to SiYuan OR local markdown

# ========== Environment ==========
export PATH="$HOME/.npm-global/bin:$PATH"

# ========== Config ==========
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCRIPT_DIR/../config.json"
MLX_URL=""
BACKEND="local"
OUTPUT_DIR="$HOME/screen-activity"
KEEP_DAYS=7
ANALYSIS_MODE="simple"
ANALYSIS_PROMPT=""
IDLE_DETECTION=true
APP_BLACKLIST=()

# Load config
if [ -f "$CONFIG" ]; then
    MLX_URL=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('mlx_url',''))" 2>/dev/null)
    BACKEND=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('backend','local'))" 2>/dev/null)
    OUTPUT_DIR=$(python3 -c "import json,os; c=json.load(open('$CONFIG')); print(os.path.expanduser(c.get('local',{}).get('output_dir','~/screen-activity')))" 2>/dev/null)
    KEEP_DAYS=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('local',{}).get('keep_days',7))" 2>/dev/null)
    ANALYSIS_MODE=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('analysis_mode','simple'))" 2>/dev/null)
    ANALYSIS_PROMPT=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(c.get('analysis_prompt',''))" 2>/dev/null)
    IDLE_DETECTION=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(str(c.get('idle_detection',True)).lower())" 2>/dev/null)
    # Read blacklist as space-separated string
    BLACKLIST_STR=$(python3 -c "import json; c=json.load(open('$CONFIG')); print(','.join(c.get('app_blacklist',[])))" 2>/dev/null)
    IFS=',' read -ra APP_BLACKLIST <<< "$BLACKLIST_STR"
fi

# ========== Idle Detection ==========
if [ "$IDLE_DETECTION" = "true" ]; then
    # Get idle time (seconds) via macOS system uptime -u
    IDLE_SEC=$(python3 -c "
import subprocess, re
try:
    out = subprocess.check_output(['ioreg', '-c', 'IOHIDSystem', '-d', '4'], text=True, timeout=5)
    m = re.search(r'\"HIDIdleTime\" = (\d+)', out)
    if m:
        print(int(m.group(1)) // 1000000000)
    else:
        print(0)
except:
    print(0)
" 2>/dev/null)
    if [ -n "$IDLE_SEC" ] && [ "$IDLE_SEC" -gt 300 ] 2>/dev/null; then
        # Idle > 5 minutes, skip
        echo "SKIP: idle for ${IDLE_SEC}s, skipping screenshot"
        exit 0
    fi
fi

# ========== App Blacklist Check ==========
# FRONT_APP=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null || echo "未知")
# for keyword in "${APP_BLACKLIST[@]}"; do
#     if echo "$FRONT_APP" | grep -qi "$keyword"; then
#         echo "SKIP: app '$FRONT_APP' matches blacklist keyword '$keyword'"
#         # Log text-only entry
#         DATE=$(date "+%Y-%m-%d")
#         TIME=$(date "+%H:%M")
#         if [ "$BACKEND" = "siyuan" ]; then
#             python3 "$SCRIPT_DIR/siyuan-logger.py" "NONE" "$DATE" "$TIME" "$FRONT_APP 正在使用中（黑名单跳过截图）" 2>/dev/null
#         else
#             echo "- **$TIME** $FRONT_APP 正在使用中（黑名单跳过截图）" >> "$OUTPUT_DIR/$DATE.md"
#         fi
#         exit 0
#     fi
# done

# ========== Screenshot ==========
mkdir -p "$OUTPUT_DIR/screenshots"
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
TIME=$(date "+%H:%M")
DATE=$(date "+%Y-%m-%d")
SS_DIR="$OUTPUT_DIR/screenshots/$DATE"
mkdir -p "$SS_DIR"
SCREENSHOT="$SS_DIR/$TIMESTAMP.png"

peekaboo image --mode screen --path "$SCREENSHOT" --format png 2>/dev/null || true

# ========== Analysis ==========
if [ -f "$SCREENSHOT" ]; then
    # Build prompt based on analysis mode
    case "$ANALYSIS_MODE" in
        simple)
            PROMPT='中文描述这张屏幕截图中用户正在做什么大概100字左右总结，格式: [应用名] 识别图片中在处理的任务。输出描述。'
            ;;
        category)
            PROMPT='判断用户当前状态，从以下分类选一个：工作 / 娱乐 / 学习 / 休息，格式：[分类] 简短描述。只输出结果。'
            ;;
        productivity)
            PROMPT='评估当前活动的生产力得分(1-10分)，格式：[得分] 简短描述。只输出结果。'
            ;;
        custom)
            PROMPT="$ANALYSIS_PROMPT"
            ;;
        *)
            PROMPT='中文描述这张屏幕截图中用户正在做什么大概100字左右总结，格式: [应用名] 识别图片中在处理的任务。输出描述。'
            ;;
    esac

    SUMMARY=$(python3 -c "
import json, base64, urllib.request, sys

try:
    with open('$SCREENSHOT', 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {
        'model': 'Qwen3.5-2B-MLX-4bit',
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}},
                {'type': 'text', 'text': '''$PROMPT'''}
            ]
        }],
        'max_tokens': 80,
        'temperature': 0.3
    }

    req = urllib.request.Request(
        '$MLX_URL/chat/completions',
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer placeholder'},
        method='POST'
    )
    resp = urllib.request.urlopen(req, timeout=60)
    data = json.loads(resp.read())
    content = data['choices'][0]['message']['content'].strip()
    print(content.split('\n')[0][:120])
except Exception as e:
    print('')
" 2>/dev/null)

    # AI fallback
    if [ -z "$SUMMARY" ]; then
        SUMMARY="$FRONT_APP 正在使用中"
    fi

    # ========== Log ==========
    if [ "$BACKEND" = "siyuan" ]; then
        python3 "$SCRIPT_DIR/siyuan-logger.py" "$SCREENSHOT" "$DATE" "$TIME" "$SUMMARY" 2>/dev/null
    else
        # Local backend: append to markdown + embed screenshot
        mkdir -p "$OUTPUT_DIR"
        MD_FILE="$OUTPUT_DIR/$DATE.md"
        # Create file with header if first entry today
        if [ ! -f "$MD_FILE" ]; then
            echo "# $DATE 操作记录" > "$MD_FILE"
            echo "" >> "$MD_FILE"
        fi
        REL_PATH="screenshots/$DATE/$TIMESTAMP.png"
        echo "- **$TIME** $SUMMARY ![截图]($REL_PATH)" >> "$MD_FILE"
    fi
else
    # No screenshot, text-only
    DATE=$(date "+%Y-%m-%d")
    TIME=$(date "+%H:%M")
    SUMMARY="$FRONT_APP 正在使用中"
    if [ "$BACKEND" = "siyuan" ]; then
        python3 "$SCRIPT_DIR/siyuan-logger.py" "NONE" "$DATE" "$TIME" "$SUMMARY" 2>/dev/null
    else
        mkdir -p "$OUTPUT_DIR"
        MD_FILE="$OUTPUT_DIR/$DATE.md"
        [ ! -f "$MD_FILE" ] && echo "# $DATE 操作记录" > "$MD_FILE" && echo "" >> "$MD_FILE"
        echo "- **$TIME** $SUMMARY" >> "$MD_FILE"
    fi
fi

# ========== Cleanup old screenshots ==========
if [ "$KEEP_DAYS" -gt 0 ] 2>/dev/null; then
    find "$OUTPUT_DIR/screenshots" -type d -mtime +$KEEP_DAYS -exec rm -rf {} + 2>/dev/null || true
    # Also clean up empty date md files if using local backend
fi
