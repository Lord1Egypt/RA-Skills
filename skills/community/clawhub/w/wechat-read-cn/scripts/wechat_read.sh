#!/bin/bash
# wechat_read.sh — Read chat history from a WeChat contact/group via macOS desktop client
# v2.2: 滚动方式升级
#
# 主要改进:
#   - 修复验证逻辑：不再依赖搜索框内容，改为检查实际聊天区
#   - 改进焦点管理：Enter 前确保在第一项，Enter 后立即验证
#   - 改进截图时序：扩大截图范围排除搜索框，多次验证滚到底
#   - v2.2: scroll_to_bottom 改用 End 键（key code 119）
#   - v2.2: 上下翻页改用 PgUp（key code 116）/ PgDown（key code 121）

set -euo pipefail

CONTACT="${1:?Usage: wechat_read.sh <contact> [--pages N] | --enter | --capture <x>,<y> [--pages N]}"
SEARCH_SCREENSHOT="/tmp/wechat_read_search.png"
SCREENSHOT_TITLE="/tmp/wechat_read_verify_title.png"
SCREENSHOT_VERIFY="/tmp/wechat_read_verify_chat.png"
PAGE_PREFIX="/tmp/wechat_read_p"
VERIFY_SIMILARITY_THRESHOLD=60

# ── Tunable parameters ──────────────────────────────────────────────
CHAT_X=370
CHAT_Y=90
CHAT_W=830
CHAT_H=620

# PgUp/PgDown 模式下每次翻页重复按键次数（1 次 PgUp = 1 屏，可调）
SCROLL_STEPS=1
SCROLL_DELAY=0.05
POST_SCROLL_WAIT=0.6

FOCUS_X=750
FOCUS_Y=400
# ─────────────────────────────────────────────────────────────────────

log() { echo "[wechat-read] $*"; }
fail() { echo "[wechat-read] FAIL: $*" >&2; exit 1; }

command -v cliclick >/dev/null || fail "cliclick not found. Install: brew install cliclick"

clip_write() {
    local text="$1"
    printf '%s' "$text" > /tmp/wechat_read_clip.txt
    osascript -e 'set the clipboard to (read POSIX file "/tmp/wechat_read_clip.txt" as "utf8")'
}

activate_and_resize() {
    log "Activating WeChat..."
    osascript -e 'tell application "WeChat" to activate' || fail "Cannot activate WeChat"
    sleep 1

    log "Setting window geometry..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            set position of window 1 to {50, 50}
            set size of window 1 to {1200, 800}
        end tell
    end tell' || fail "Cannot resize window"
    sleep 0.5
}

# ══════════════════════════════════════════════════════════════════════
# 新增: OCR 函数（使用 Swift Vision）
# ══════════════════════════════════════════════════════════════════════
ocr_swift() {
    local screenshot="$1"
    
    swift - "$screenshot" 2>/dev/null <<'SWIFT'
import Foundation
import Vision
import AppKit

let path = CommandLine.arguments[1]
guard let image = NSImage(contentsOfFile: path),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en"]

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])

let text = (request.results ?? [])
    .compactMap { $0.topCandidates(1).first?.string }
    .joined(separator: "\n")
print(text)
SWIFT
}

# ══════════════════════════════════════════════════════════════════════
# 新增: verify_chat_content — 检查聊天内容是否有效
# ══════════════════════════════════════════════════════════════════════
verify_chat_content() {
    local contact="$1"
    local screenshot="$2"

    log "  检查聊天内容..."

    # OCR 聊天区
    local chat_text
    chat_text=$(ocr_swift "$screenshot") || chat_text=""

    log "  [DEBUG] 聊天内容长度: ${#chat_text}"

    # 检查 1: 是否为空
    if [ -z "$chat_text" ]; then
        log "  ❌ 聊天区为空"
        return 1
    fi

    # 检查 2: 是否是"对方还不是你的朋友"
    if [[ "$chat_text" == *"对方还不是你的朋友"* ]]; then
        log "  ❌ 对方不是好友"
        return 1
    fi

    # 检查 3: 是否是搜索结果页面
    if [[ "$chat_text" == *"网络查找"* ]] || [[ "$chat_text" == *"查找微信号"* ]]; then
        log "  ❌ 仍在搜索页面"
        return 1
    fi

    # 检查 4: 是否有时间戳（正常聊天会有）
    if [[ "$chat_text" =~ ([0-9]{1,2}):([0-9]{2}) ]]; then
        log "  ✅ 检测到时间戳，聊天区有效"
        return 0
    fi

    log "  ⚠️ 无法确认，但继续前进"
    return 0
}

# ══════════════════════════════════════════════════════════════════════
# 新增: confirm_open — Enter 后确认打开的是正确的聊天
# ══════════════════════════════════════════════════════════════════════
confirm_open() {
    local contact="$1"

    log "  确认打开的是 '$contact' 的聊天..."

    # 先关闭搜索框
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
        end tell
    end tell' 2>/dev/null || true
    sleep 0.3

    # 截图聊天区
    screencapture -x -R "370,50,830,250" "$SCREENSHOT_VERIFY" || fail "Cannot capture verify screenshot"
    
    # 快速 OCR 检查
    if ! verify_chat_content "$contact" "$SCREENSHOT_VERIFY"; then
        log "  ❌ 聊天区检查失败，可能打开了错误的人或搜索页面"
        return 1
    fi

    log "  ✅ 确认成功"
    return 0
}

# ──────────────────────────────────────
# 改进: fast_locate — 确保焦点在第一项再 Enter
# ──────────────────────────────────────
fast_locate() {
    local contact="$1"

    log "【步骤 1】快速定位: $contact"

    activate_and_resize

    log "Opening search (Cmd+F)..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
            delay 0.3
            keystroke "f" using command down
        end tell
    end tell' || fail "Cannot trigger search"
    sleep 0.8

    log "Pasting contact name..."
    clip_write "$contact"
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "a" using command down
            delay 0.2
            keystroke "v" using command down
        end tell
    end tell' || fail "Cannot paste contact name"
    sleep 1

    log "确保焦点在第一项，然后按 Enter..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 126
            delay 0.1
            key code 36
        end tell
    end tell' || fail "Cannot press Enter"
    sleep 1.5
}

# ──────────────────────────────────────
# 改进: verify_contact_v2.1 — 三层验证
# ──────────────────────────────────────
verify_contact() {
    local contact="$1"

    log "【步骤 2】验证联系人..."

    # 第一层：确认打开成功
    if ! confirm_open "$contact"; then
        log "❌ 第一层验证失败：无法打开聊天"
        return 1
    fi

    # 第二层：检查标题栏（现在搜索框已关闭）
    screencapture -x -R "370,50,830,100" "$SCREENSHOT_VERIFY"
    local title_text
    title_text=$(ocr_swift "$SCREENSHOT_VERIFY") || title_text=""

    log "  标题栏 OCR: '$title_text'"

    # 简单检查：标题应该包含联系人名字
    if [[ "$title_text" == *"$contact"* ]]; then
        log "✅ 精确匹配: 标题包含 '$contact'"
        return 0
    fi

    # 相似度检查
    local match_chars=0
    local total_chars=${#contact}
    local i
    for (( i=0; i<total_chars; i++ )); do
        local ch="${contact:$i:1}"
        if [[ "$title_text" == *"$ch"* ]]; then
            (( match_chars++ )) || true
        fi
    done

    local similarity=0
    if (( total_chars > 0 )); then
        similarity=$(( match_chars * 100 / total_chars ))
    fi

    log "  相似度: ${similarity}%"

    if (( similarity >= VERIFY_SIMILARITY_THRESHOLD )); then
        log "✅ 相似度匹配通过"
        return 0
    fi

    log "❌ 验证失败"
    return 1
}

# ──────────────────────────────────────
# 改进: scroll_to_bottom — 使用 End 键直达底部
# ──────────────────────────────────────
scroll_to_bottom() {
    log "滚到底部..."

    # 确保焦点在聊天区
    cliclick c:"$FOCUS_X","$FOCUS_Y" || true
    sleep 0.3

    # End 键（key code 119）直接跳到最底部
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 119
        end tell
    end tell' 2>/dev/null || true

    sleep 0.5
}

# ──────────────────────────────────────
# precise_locate_fallback
# ──────────────────────────────────────
precise_locate_fallback() {
    local contact="$1"

    log "【步骤 3】精确定位降级 (Agent 模式)..."

    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
            delay 0.3
            key code 53
        end tell
    end tell'
    sleep 0.5

    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "f" using command down
        end tell
    end tell' || fail "Cannot re-trigger search"
    sleep 0.8

    clip_write "$contact"
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "a" using command down
            delay 0.2
            keystroke "v" using command down
        end tell
    end tell' || fail "Cannot re-paste contact name"
    sleep 1.5

    screencapture -x -R "50,50,500,600" "$SEARCH_SCREENSHOT" || fail "Cannot capture dropdown screenshot"
    log "Dropdown screenshot: $SEARCH_SCREENSHOT"

    log "FALLBACK: 需要 Agent 识别联系人坐标"
    log "请分析截图 $SEARCH_SCREENSHOT，找到 '$contact' 的行坐标，然后执行:"
    log "  bash scripts/wechat_read.sh \"$contact\" --capture <x>,<y> [--pages N]"
}

do_search() {
    activate_and_resize

    log "Opening search..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
            delay 0.3
            keystroke "f" using command down
        end tell
    end tell' || fail "Cannot trigger search"
    sleep 0.8

    log "Searching for contact: $CONTACT"
    clip_write "$CONTACT"
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "a" using command down
            delay 0.2
            keystroke "v" using command down
        end tell
    end tell' || fail "Cannot paste contact name"
    sleep 1.5

    log "Capturing search dropdown..."
    screencapture -x -R "50,50,500,600" "$SEARCH_SCREENSHOT" || fail "Cannot capture screenshot"
    log "Screenshot saved: $SEARCH_SCREENSHOT"
}

capture_page() {
    local page_num="$1"
    local outfile="${PAGE_PREFIX}${page_num}.png"
    screencapture -x -R "${CHAT_X},${CHAT_Y},${CHAT_W},${CHAT_H}" "$outfile" \
        || fail "Cannot capture page $page_num"
    echo "$outfile"
}

scroll_up_once() {
    # PgUp（key code 116）向上翻一页
    local repeat_block=""
    repeat_block="tell application \"System Events\"
        tell process \"WeChat\"
            repeat ${SCROLL_STEPS} times
                key code 116
                delay ${SCROLL_DELAY}
            end repeat
        end tell
    end tell"
    osascript -e "$repeat_block" || fail "Scroll failed"
    sleep "$POST_SCROLL_WAIT"
}

scroll_down_once() {
    # PgDown（key code 121）向下翻一页
    local repeat_block=""
    repeat_block="tell application \"System Events\"
        tell process \"WeChat\"
            repeat ${SCROLL_STEPS} times
                key code 121
                delay ${SCROLL_DELAY}
            end repeat
        end tell
    end tell"
    osascript -e "$repeat_block" || fail "Scroll failed"
    sleep "$POST_SCROLL_WAIT"
}

file_checksum() {
    md5 -q "$1" 2>/dev/null || md5sum "$1" | cut -d' ' -f1
}

do_capture_pages() {
    local max_pages="$1"

    # Step 1: 滚到底
    scroll_to_bottom
    sleep 0.5

    # Step 2: 再次聚焦
    cliclick c:"$FOCUS_X","$FOCUS_Y" || true
    sleep 0.2

    # Step 3: 截图第 1 页（最新）
    log "Capturing page 1 / $max_pages (latest messages)..."
    local outfile
    outfile=$(capture_page 1)
    local prev_checksum
    prev_checksum=$(file_checksum "$outfile")
    log "  Saved: $outfile"

    # Step 4: 向上翻页
    local page=2
    while [ "$page" -le "$max_pages" ]; do
        log "Scrolling up (page $page / $max_pages)..."
        scroll_up_once

        log "Capturing page $page..."
        outfile=$(capture_page "$page")

        local cur_checksum
        cur_checksum=$(file_checksum "$outfile")
        if [ "$cur_checksum" = "$prev_checksum" ]; then
            log "[REACHED_TOP] Page $page is identical to page $((page - 1)). Chat top reached."
            rm -f "$outfile"
            page=$((page - 1))
            break
        fi
        prev_checksum="$cur_checksum"
        log "  Saved: $outfile"
        page=$((page + 1))
    done

    local total=$((page))
    if [ "$page" -gt "$max_pages" ]; then
        total=$max_pages
    fi

    echo ""
    log "Capture complete. $total page(s) saved."
    log "Files: ${PAGE_PREFIX}1.png through ${PAGE_PREFIX}${total}.png"
    log ""
    log "Page order: p1 = newest (bottom of chat), p${total} = oldest (top of chat)"
    log ""
    log "Next: Agent reads all page screenshots, performs OCR, deduplicates"
    log "overlapping content between adjacent pages, and assembles the"
    log "conversation in chronological order (reverse page order)."
}

do_capture() {
    local coords="$1"
    local max_pages="$2"
    local x="${coords%,*}"
    local y="${coords#*,}"

    log "Clicking contact at ($x, $y)..."
    cliclick c:"$x","$y" || fail "cliclick failed"
    sleep 1.5

    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
        end tell
    end tell'
    sleep 0.5

    do_capture_pages "$max_pages"
}

# ══════════════════════════════════════════════════════════════════════
# v2.1 auto mode — fast-locate + confirm + verify + capture
# ══════════════════════════════════════════════════════════════════════
do_auto() {
    local contact="$1"
    local max_pages="$2"

    log "=== wechat-read v2.2 自动模式 ==="

    # Step 1: Fast locate
    fast_locate "$contact"

    # Step 2: Verify and branch
    if verify_contact "$contact"; then
        log "【步骤 2】✅ 验证通过，开始截图"
        do_capture_pages "$max_pages"
    else
        log "【步骤 2】❌ 验证失败，降级到 Agent 模式"
        precise_locate_fallback "$contact"
        exit 2
    fi
}

# ── Parse arguments ──────────────────────────────────────────────────
MODE=""
CLICK_COORDS=""
MAX_PAGES=3
NEXT_PAGE=1

shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --enter)
            MODE="enter"; shift ;;
        --capture)
            MODE="capture"; CLICK_COORDS="$2"; shift 2 ;;
        --pages)
            MAX_PAGES="$2"; shift 2 ;;
        --next-page)
            MODE="next-page"; NEXT_PAGE="$2"; shift 2 ;;
        *)
            fail "Unknown argument: $1" ;;
    esac
done

[[ -z "$MODE" ]] && MODE="auto"

if [[ "$MODE" == "capture" || "$MODE" == "auto" ]]; then
    rm -f /tmp/wechat_read_p*.png /tmp/wechat_read_search.png 2>/dev/null || true
fi

case "$MODE" in
    auto)
        do_auto "$CONTACT" "$MAX_PAGES"
        ;;
    enter)
        do_search
        log "Phase 1 complete. Analyze $SEARCH_SCREENSHOT, find target row, then run:"
        log "  wechat_read.sh \"$CONTACT\" --capture <x>,<y> [--pages N]"
        ;;
    capture)
        [[ -z "$CLICK_COORDS" ]] && fail "Coordinates required for --capture"
        do_capture "$CLICK_COORDS" "$MAX_PAGES"
        ;;
    next-page)
        log "【继续翻页】向上滚动，截取第 $NEXT_PAGE 页..."
        scroll_up_once
        outfile=$(capture_page "$NEXT_PAGE")
        cur_checksum=$(file_checksum "$outfile")
        prev_file="/tmp/wechat_read_p$((NEXT_PAGE - 1)).png"
        if [[ -f "$prev_file" ]]; then
            prev_checksum=$(file_checksum "$prev_file")
            if [[ "$cur_checksum" == "$prev_checksum" ]]; then
                log "[REACHED_TOP] 已到达聊天顶部，无更多消息"
                rm -f "$outfile"
                exit 3
            fi
        fi
        log "截图保存: $outfile"
        log "请 Agent 分析此截图，若找到对方（左侧白色）气泡即停止；否则继续执行:"
        log "  wechat_read.sh \"$CONTACT\" --next-page $((NEXT_PAGE + 1))"
        ;;
esac
