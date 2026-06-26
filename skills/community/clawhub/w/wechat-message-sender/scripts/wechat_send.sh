#!/bin/bash
# wechat_send.sh - 通过 AppleScript + JXA 操控微信发送消息
# 用法: wechat_send.sh <联系人名称> <消息内容>
# 示例: wechat_send.sh "Ryan" "你好！"

set -e

CONTACT="$1"
MESSAGE="$2"

if [ -z "$CONTACT" ] || [ -z "$MESSAGE" ]; then
    echo "用法: wechat_send.sh <联系人名称> <消息内容>"
    echo "示例: wechat_send.sh \"Ryan\" \"你好！\""
    exit 1
fi

# 获取微信窗口位置和输入框点击坐标
read CLICK_X CLICK_Y <<< $(osascript -e '
tell application "System Events"
    tell process "WeChat"
        set winPos to position of window 1
        set winSize to size of window 1
        set clickX to (item 1 of winPos) + round ((item 1 of winSize) * 0.65)
        set clickY to (item 2 of winPos) + (item 2 of winSize) - 50
        return (clickX as text) & " " & (clickY as text)
    end tell
end tell' 2>&1)

echo "[1/4] 激活微信并搜索联系人: $CONTACT"

# 步骤1: 激活微信并搜索联系人
osascript -e "
tell application \"WeChat\" to activate
delay 0.5

-- Open search, clear any previous query, then paste the contact name.
-- If we don't clear the search box, the old query can stick and the first result
-- (often the last-contact) gets selected repeatedly.
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

echo "[2/4] 点击输入框 ($CLICK_X, $CLICK_Y)"

# 步骤2: 用 JXA 点击输入框
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

echo "[3/4] 粘贴消息内容"

# 步骤3: 设置剪贴板并粘贴
osascript -e "
set the clipboard to \"$MESSAGE\"
tell application \"System Events\"
    tell process \"WeChat\"
        keystroke \"v\" using command down
        delay 0.3
    end tell
end tell"

sleep 0.3

echo "[4/4] 发送消息"

# 步骤4: 回车发送
osascript -e '
tell application "System Events"
    tell process "WeChat"
        key code 36
    end tell
end tell'

echo "✅ 消息已发送给 $CONTACT: $MESSAGE"
