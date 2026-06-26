#!/bin/bash
# wechat_send.sh — Send a message to a WeChat contact/group via macOS desktop client
# v2.0: Four-layer progressive verification architecture
#
# Usage:
#   Auto mode (v2.0):  wechat_send.sh <contact> <message>
#   Phase 1 (v1.0):    wechat_send.sh <contact> --search-only
#   Phase 2 (v1.0):    wechat_send.sh <contact> <message> --send-only <x>,<y>
#
# Exit codes:
#   0 — success (message sent)
#   1 — fatal error
#   2 — fallback: Agent must read screenshot and call --send-only
#
# Requires: macOS Accessibility permission, cliclick (brew install cliclick)

set -euo pipefail

CONTACT="${1:?Usage: wechat_send.sh <contact> <message> [--search-only | --send-only x,y]}"
SCREENSHOT_DROPDOWN="/tmp/wechat_search_dropdown.png"
SCREENSHOT_TITLE="/tmp/wechat_verify_title.png"
VERIFY_SIMILARITY_THRESHOLD=60

log() { echo "[wechat-send] $*"; }
fail() { echo "[wechat-send] FAIL: $*" >&2; exit 1; }

command -v cliclick >/dev/null || fail "cliclick not found. Install: brew install cliclick"

clip_write() {
    # Write text to clipboard via temp file (safe for CJK + multiline)
    local text="$1"
    printf '%s' "$text" > /tmp/wechat_send_clip.txt
    osascript -e 'set the clipboard to (read POSIX file "/tmp/wechat_send_clip.txt" as "utf8")'
}

# ──────────────────────────────────────
# Step 1: fast_locate — Cmd+F → paste → Enter (optimistic)
# ──────────────────────────────────────
fast_locate() {
    local contact="$1"

    log "【步骤 1】快速定位: $contact"

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
# Step 2: verify_contact — Lightweight title-bar OCR check
# ──────────────────────────────────────
verify_contact() {
    local contact="$1"

    log "【步骤 2】验证联系人..."

    # 2.1 Capture title bar region
    screencapture -x -R "50,50,1200,150" "$SCREENSHOT_TITLE" || fail "Cannot capture title screenshot"
    log "Title screenshot: $SCREENSHOT_TITLE"

    # 2.2 OCR via macOS Vision framework (Swift — no third-party deps)
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

    # 2.3 Decision logic

    # Exclusion FIRST: detected search/network page (wrong destination)
    # Only reject if we see explicit search-result indicators, NOT just "搜索" in the UI
    if [[ "$title_text" == *"网络查找"* ]] || \
       [[ "$title_text" == *"查找微信号"* ]] || \
       [[ "$title_text" == *"搜索网络结果"* ]]; then
        log "❌ 检测到搜索结果页面，联系人未找到"
        return 1
    fi

    # Exact match: title contains contact name (only after exclusion passes)
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
# Step 4: precise_locate_fallback — Degrade to v1.0 Agent-assisted mode
# ──────────────────────────────────────
precise_locate_fallback() {
    local contact="$1"

    log "【步骤 4】精确定位降级 (Agent 模式)..."

    # 4.1 ESC twice to dismiss any overlay / wrong page
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 53
            delay 0.3
            key code 53
        end tell
    end tell'
    sleep 0.5

    # 4.2 Re-open search
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "f" using command down
        end tell
    end tell' || fail "Cannot re-trigger search"
    sleep 0.8

    # 4.3 Re-paste contact name
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

    # 4.4 Capture search dropdown
    screencapture -x -R "50,50,500,600" "$SCREENSHOT_DROPDOWN" || fail "Cannot capture dropdown screenshot"
    log "Dropdown screenshot: $SCREENSHOT_DROPDOWN"

    # 4.5 Report — Agent takes over from here
    log "FALLBACK: 需要 Agent 识别联系人坐标"
    log "请分析截图 $SCREENSHOT_DROPDOWN，找到 '$contact' 的行坐标，然后执行:"
    log "  bash scripts/wechat_send.sh \"$contact\" \"<消息>\" --send-only <x>,<y>"
}

# ──────────────────────────────────────
# Step 5: send_message — Paste and send
# ──────────────────────────────────────
send_message() {
    local message="$1"

    log "【步骤 5】发送消息..."

    log "Clicking input box..."
    cliclick c:700,650
    sleep 0.3

    log "Pasting message..."
    clip_write "$message"
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            keystroke "v" using command down
        end tell
    end tell' || fail "Cannot paste message"
    sleep 0.5

    log "Pressing Enter to send..."
    osascript -e '
    tell application "System Events"
        tell process "WeChat"
            key code 36
        end tell
    end tell' || fail "Cannot send"
    sleep 0.5

    log "✅ 消息发送完成"
}

# ══════════════════════════════════════
# v1.0 backward-compat functions
# ══════════════════════════════════════
do_search() {
    log "v1.0 Phase 1: search-only"

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
    screencapture -x -R "50,50,500,600" "$SCREENSHOT_DROPDOWN" || fail "Cannot capture screenshot"
    log "Screenshot saved: $SCREENSHOT_DROPDOWN"
}

do_click_and_send() {
    local coords="$1"
    local message="$2"
    local x="${coords%,*}"
    local y="${coords#*,}"

    log "v1.0 Phase 2: click and send"
    log "Clicking contact at ($x, $y) via cliclick..."
    cliclick c:"$x","$y" || fail "cliclick failed"
    sleep 1.5

    send_message "$message"
}

# ══════════════════════════════════════
# v2.0 auto mode — four-layer progressive flow
# ══════════════════════════════════════
do_auto() {
    local contact="$1"
    local message="$2"

    log "=== wechat-send v2.0 自动模式 ==="

    # Step 1: Fast locate
    fast_locate "$contact"

    # Step 2 + 3: Verify and branch
    if verify_contact "$contact"; then
        # ✅ Verified — proceed to step 5
        log "【步骤 3】✅ 验证通过，跳到步骤 5"
        send_message "$message"
    else
        # ❌ Failed — degrade to step 4 (Agent-assisted)
        log "【步骤 3】❌ 验证失败，降级到步骤 4"
        precise_locate_fallback "$contact"
        # Agent must call --send-only with correct coords afterwards
        exit 2
    fi
}

# ══════════════════════════════════════
# Argument parsing & dispatch
# ══════════════════════════════════════
MODE="auto"
MESSAGE=""
CLICK_COORDS=""

shift # skip CONTACT

while [[ $# -gt 0 ]]; do
    case "$1" in
        --search-only)
            MODE="search-only"; shift ;;
        --send-only)
            MODE="send-only"; CLICK_COORDS="$2"; shift 2 ;;
        *)
            [[ -z "$MESSAGE" ]] && MESSAGE="$1"; shift ;;
    esac
done

case "$MODE" in
    auto)
        [[ -z "$MESSAGE" ]] && fail "Usage: wechat_send.sh <contact> <message>"
        do_auto "$CONTACT" "$MESSAGE"
        ;;
    search-only)
        do_search
        log "Phase 1 complete. Analyze $SCREENSHOT_DROPDOWN, find target row, then run:"
        log "  wechat_send.sh \"$CONTACT\" \"<message>\" --send-only <x>,<y>"
        ;;
    send-only)
        [[ -z "$MESSAGE" ]] && fail "Message required for --send-only"
        [[ -z "$CLICK_COORDS" ]] && fail "Coordinates required for --send-only"
        do_click_and_send "$CLICK_COORDS" "$MESSAGE"
        ;;
esac
