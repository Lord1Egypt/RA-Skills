#!/bin/bash
# wechat_send_image.sh - Send an image/file to a WeChat contact via UI automation (macOS)
# Usage: wechat_send_image.sh <contact_name> <image_path>
# Example: wechat_send_image.sh "File Transfer" "/path/to/screenshot.png"

set -euo pipefail

CONTACT="${1:-}"
IMAGE_PATH="${2:-}"

if [ -z "$CONTACT" ] || [ -z "$IMAGE_PATH" ]; then
  echo "Usage: wechat_send_image.sh <contact_name> <image_path>"
  echo "Example: wechat_send_image.sh \"Family\" \"/tmp/screen.png\""
  exit 1
fi

if [ ! -f "$IMAGE_PATH" ]; then
  echo "Error: file not found: $IMAGE_PATH"
  exit 1
fi

# Resolve to an absolute POSIX path (WeChat paste-as-file is sensitive to weird relative paths)
ABS_PATH="$(cd "$(dirname "$IMAGE_PATH")" && pwd)/$(basename "$IMAGE_PATH")"

# Get WeChat window position and an approximate input field click coordinate
read CLICK_X CLICK_Y <<< "$(osascript -e '
tell application "System Events"
    tell process "WeChat"
        set winPos to position of window 1
        set winSize to size of window 1
        set clickX to (item 1 of winPos) + round ((item 1 of winSize) * 0.65)
        set clickY to (item 2 of winPos) + (item 2 of winSize) - 50
        return (clickX as text) & " " & (clickY as text)
    end tell
end tell' 2>&1)"

echo "[1/4] Activate WeChat and search contact: $CONTACT"

# Step 1: Activate WeChat and open the chat by searching contact
osascript -e "
tell application \"WeChat\" to activate
delay 0.5

-- Open search, clear any previous query, then paste the contact name.
set the clipboard to \"$CONTACT\"

tell application \"System Events\"
    tell process \"WeChat\"
        keystroke \"f\" using command down
        delay 0.5
        keystroke \"a\" using command down
        delay 0.1
        key code 51
        delay 0.2
        keystroke \"v\" using command down
        delay 1.2
        key code 36
        delay 0.5
        key code 53
        delay 0.3
    end tell
end tell"

echo "[2/4] Click message input field (${CLICK_X}, ${CLICK_Y})"

# Step 2: Click message input field
osascript -l JavaScript -e "
ObjC.import('Cocoa');
var point = $.CGPointMake(${CLICK_X}, ${CLICK_Y});
var mouseDown = $.CGEventCreateMouseEvent(null, $.kCGEventLeftMouseDown, point, 0);
$.CGEventPost($.kCGHIDEventTap, mouseDown);
var mouseUp = $.CGEventCreateMouseEvent(null, $.kCGEventLeftMouseUp, point, 0);
$.CGEventPost($.kCGHIDEventTap, mouseUp);
'clicked';
"

sleep 0.3

echo "[3/4] Paste image/file from clipboard"

# Step 3: Put a file reference on the clipboard and paste it (WeChat will attach/upload it)
osascript -e "
set the clipboard to (POSIX file \"$ABS_PATH\")

tell application \"System Events\"
    tell process \"WeChat\"
        keystroke \"v\" using command down
    end tell
end tell"

# Give WeChat time to load the image preview / finish attaching.
sleep 1.2

echo "[4/4] Send (Enter)"

osascript -e '
tell application "System Events"
    tell process "WeChat"
        key code 36
    end tell
end tell'

echo "✅ Image/file sent to $CONTACT: $ABS_PATH"
