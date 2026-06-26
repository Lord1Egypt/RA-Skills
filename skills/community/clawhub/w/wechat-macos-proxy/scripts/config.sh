#!/bin/bash
# WeChat macOS Proxy 配置文件

# 自动回复模式: auto(全自动) | semi(半自动/建议模式) | manual(仅通知)
MODE="semi"

# 置信度阈值（0-1），超过此值自动发送（auto 模式下有效）
AUTO_REPLY_THRESHOLD=0.85

# 检查间隔（秒）
CHECK_INTERVAL=5

# 微信窗口检测超时（秒）
WECHAT_TIMEOUT=10

# 临时文件目录
TEMP_DIR="/tmp/wechat_proxy"
mkdir -p "$TEMP_DIR"

# 日志文件
LOG_FILE="$TEMP_DIR/wechat_proxy.log"

# 微信 App 名称（英文）
WECHAT_APP_NAME="WeChat"

# 微信窗口标题关键词
WECHAT_WINDOW_KEYWORD="WeChat"

# 坐标配置（根据屏幕分辨率调整，默认适配 14/16 寸 MacBook）
# 聊天列表区域（左侧面板）
CHAT_LIST_X=150
CHAT_LIST_Y_START=150
CHAT_LIST_ITEM_HEIGHT=65

# 输入框区域
INPUT_BOX_Y_OFFSET=60

# 发送按钮位置（相对于输入框）
SEND_BUTTON_OFFSET_X=350
SEND_BUTTON_OFFSET_Y=0

# 最大聊天历史数量（用于检测新消息）
MAX_CHAT_HISTORY=20

# 颜色检测配置（用于红点检测）
RED_DOT_COLOR_THRESHOLD="0.8"

# 写入日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 peekaboo 是否安装
check_peekaboo() {
    if ! command -v peekaboo &> /dev/null; then
        echo "错误: peekaboo 未安装"
        echo "请运行: brew install steipete/tap/peekaboo"
        exit 1
    fi
}

# 检查微信是否运行
check_wechat_running() {
    # 使用进程检测（更可靠）
    if ! pgrep -x "WeChat" > /dev/null; then
        log "微信未运行，尝试启动..."
        open -a WeChat
        sleep 3
        
        # 再次检查
        if ! pgrep -x "WeChat" > /dev/null; then
            log "错误: 无法启动微信"
            return 1
        fi
    fi
    log "✓ 微信正在运行"
    return 0
}

# 获取微信窗口 ID（备用方案，不依赖权限）
get_wechat_window_id() {
    # 由于权限限制，直接使用 frontmost 方式
    echo "frontmost"
}

# 截图并保存（使用 screencapture 作为备选）
screenshot() {
    local output_path="${1:-$TEMP_DIR/screenshot.png}"
    # 先尝试 peekaboo
    if peekaboo image --mode screen --path "$output_path" 2>/dev/null; then
        echo "$output_path"
        return 0
    fi
    # 备选：使用系统 screencapture
    if screencapture -x "$output_path" 2>/dev/null; then
        echo "$output_path"
        return 0
    fi
    echo ""
    return 1
}

# 激活微信窗口（使用 AppleScript，不依赖 peekaboo 窗口权限）
focus_wechat() {
    log "激活微信..."
    osascript -e 'tell application "WeChat" to activate' 2>/dev/null || \
    osascript -e 'tell application "微信" to activate' 2>/dev/null || \
    open -a WeChat
    sleep 1
}

# 导出函数和变量
export TEMP_DIR LOG_FILE WECHAT_APP_NAME
export MODE AUTO_REPLY_THRESHOLD CHECK_INTERVAL
export CHAT_LIST_X CHAT_LIST_Y_START CHAT_LIST_ITEM_HEIGHT
