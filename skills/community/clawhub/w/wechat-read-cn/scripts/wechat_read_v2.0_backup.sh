#!/bin/bash
# wechat_read.sh — Read chat history from a WeChat contact/group via macOS desktop client
# v2.0: Auto mode with fast-locate + verify; fallback to Agent-assisted mode
#
# Usage:
#   Auto mode (v2.0):  wechat_read.sh <contact> [--pages N]
#   Phase 1 (v1.0):    wechat_read.sh <contact> --enter
#   Phase 2 (v1.0):    wechat_read.sh <contact> --capture <x>,<y> [--pages N]
#   Next page:         wechat_read.sh <contact> --next-page <N>
#
# Exit codes:
#   0 — success (capture complete)
#   1 — fatal error
#   2 — fallback: Agent must read screenshot and call --capture
#   3 — reached top (--next-page identical to previous)
#
# Requires: macOS Accessibility + Screen Recording permission, cliclick

set -euo pipefail

CONTACT="${1:?Usage: wechat_read.sh <contact> [--pages N] | --enter | --capture <x>,<y> [--pages N]}"
SEARCH_SCREENSHOT="/tmp/wechat_read_search.png"
SCREENSHOT_TITLE="/tmp/wechat_read_verify_title.png"
PAGE_PREFIX="/tmp/wechat_read_p"
VERIFY_SIMILARITY_THRESHOLD=60

# ── Tunable parameters ──────────────────────────────────────────────
# Chat content area: x, y, width, height (screen-absolute)
# Based on window at {50,50} size {1200,800}
# Excludes sidebar (~320px), title bar (~40px), input box (~160px)
CHAT_X=370
CHAT_Y=90
CHAT_W=830
CHAT_H=620

# Scroll tuning
SCROLL_STEPS=8           # arrow-up keystrokes per page
SCROLL_DELAY=0.04        # seconds between keystrokes
POST_SCROLL_WAIT=0.6     # seconds to wait after scroll before capture

# Focus click position (center of chat content area)
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

# ──────────────────────────────────────
# fast_locate — Cmd+F → paste → Enter (optimistic)
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

    log "Pressing Enter (optimistic select)..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 36
        end tell
    end tell' || fail "Cannot press Enter"
    sleep 1
}

# ──────────────────────────────────────
# verify_contact — Lightweight title-bar OCR check
# ──────────────────────────────────────
verify_contact() {
    local contact="$1"

    log "【步骤 2】验证联系人..."

    # Capture title bar region
    screencapture -x -R "50,50,1200,150" "$SCREENSHOT_TITLE" || fail "Cannot capture title screenshot"
    log "Title screenshot: $SCREENSHOT_TITLE"

    # OCR via macOS Vision framework (Swift — no third-party deps)
    local title_text
    title_text=$(swift - "$SCREENSHOT_TITLE" 2>/dev/null <<'SWIFT'
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
    .joined(separator: " ")
print(text)
SWIFT
    ) || title_text=""

    log "OCR result: '$title_text'"

    # Exclusion FIRST: detected search/network page (wrong destination)
    if [[ "$title_text" == *"网络查找"* ]] || \
       [[ "$title_text" == *"查找微信号"* ]] || \
       [[ "$title_text" == *"搜索网络结果"* ]]; then
        log "❌ 检测到搜索结果页面，联系人未找到"
        return 1
    fi

    # Exact match: title contains contact name
    if [[ "$title_text" == *"$contact"* ]]; then
        log "✅ 精确匹配: 标题包含 '$contact'"
        return 0
    fi

    # Similarity check (character overlap ratio)
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

    log "相似度: ${similarity}% (阈值: ${VERIFY_SIMILARITY_THRESHOLD}%)"

    if (( similarity >= VERIFY_SIMILARITY_THRESHOLD )); then
        log "✅ 相似度匹配通过"
        return 0
    fi

    log "❌ 验证失败"
    return 1
}

# ──────────────────────────────────────
# precise_locate_fallback — Degrade to v1.0 Agent-assisted mode
# ──────────────────────────────────────
precise_locate_fallback() {
    local contact="$1"

    log "【步骤 3】精确定位降级 (Agent 模式)..."

    # ESC twice to dismiss any overlay / wrong page
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
            delay 0.3
            key code 53
        end tell
    end tell'
    sleep 0.5

    # Re-open search
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "f" using command down
        end tell
    end tell' || fail "Cannot re-trigger search"
    sleep 0.8

    # Re-paste contact name
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

    # Capture search dropdown
    screencapture -x -R "50,50,500,600" "$SEARCH_SCREENSHOT" || fail "Cannot capture dropdown screenshot"
    log "Dropdown screenshot: $SEARCH_SCREENSHOT"

    # Report — Agent takes over from here
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
    # Generate the AppleScript to press arrow-up SCROLL_STEPS times
    local repeat_block=""
    repeat_block="tell application \"System Events\"
        tell process \"WeChat\"
            repeat ${SCROLL_STEPS} times
                key code 126
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

    # Scroll to bottom first to ensure we capture the latest messages
    log "Scrolling to bottom (Cmd+Down)..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 125 using command down
        end tell
    end tell' 2>/dev/null
    sleep 0.5

    # Click chat content area to ensure it has focus for scrolling
    log "Focusing chat content area..."
    cliclick c:"$FOCUS_X","$FOCUS_Y" || true
    sleep 0.3

    # Capture first page (current view = most recent messages)
    log "Capturing page 1 / $max_pages (latest messages)..."
    local outfile
    outfile=$(capture_page 1)
    local prev_checksum
    prev_checksum=$(file_checksum "$outfile")
    log "  Saved: $outfile"

    # Scroll up and capture additional pages
    local page=2
    while [ "$page" -le "$max_pages" ]; do
        log "Scrolling up..."
        scroll_up_once

        log "Capturing page $page / $max_pages..."
        outfile=$(capture_page "$page")

        # Check if page changed (scroll-stop detection)
        local cur_checksum
        cur_checksum=$(file_checksum "$outfile")
        if [ "$cur_checksum" = "$prev_checksum" ]; then
            log "[REACHED_TOP] Page $page is identical to page $((page - 1)). Chat top reached."
            rm -f "$outfile"  # Remove duplicate
            page=$((page - 1))
            break
        fi
        prev_checksum="$cur_checksum"
        log "  Saved: $outfile"
        page=$((page + 1))
    done

    local total=$((page - 1))
    [ "$page" -le "$max_pages" ] && total=$page  # adjust if reached top

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

    # Close search overlay by pressing Escape
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
        end tell
    end tell'
    sleep 0.5

    do_capture_pages "$max_pages"
}

# ══════════════════════════════════════
# v2.0 auto mode — fast-locate + verify + capture
# ══════════════════════════════════════
do_auto() {
    local contact="$1"
    local max_pages="$2"

    log "=== wechat-read v2.0 自动模式 ==="

    # Step 1: Fast locate
    fast_locate "$contact"

    # Step 2 + 3: Verify and branch
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
NEXT_PAGE=1  # for --next-page mode

shift  # skip CONTACT

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

# ── Clean up old captures (only on first capture) ───────────────────
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
        # 继续向上翻一页，截图后由 Agent 判断是否已找到对方回复
        # 用法：wechat_read.sh <contact> --next-page <N>
        # 效果：向上滚动一次，截图保存为 /tmp/wechat_read_p<N>.png
        log "【继续翻页】向上滚动，截取第 $NEXT_PAGE 页..."
        scroll_up_once
        outfile=$(capture_page "$NEXT_PAGE")
        cur_checksum=$(file_checksum "$outfile")
        # 检查是否已到顶（与上一页相同）
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
