#!/bin/bash
# Extension Host 재시작 스크립트

# 방법 1: VSCode CLI 명령어 (권장)
if command -v code &> /dev/null; then
    echo "VSCode CLI로 Extension Host 재시작 중..."
    code --command "workbench.action.restartExtensionHost" 2>/dev/null && exit 0
fi

# 방법 2: Cursor CLI
if command -v cursor &> /dev/null; then
    echo "Cursor CLI로 Extension Host 재시작 중..."
    cursor --command "workbench.action.restartExtensionHost" 2>/dev/null && exit 0
fi

# 방법 3: AppleScript (macOS fallback)
if [ "$(uname)" = "Darwin" ]; then
    echo "AppleScript로 Extension Host 재시작 시도 중..."
    osascript -e '
    tell application "System Events"
        keystroke "p" using {command down, shift down}
        delay 0.3
        keystroke "Developer: Restart Extension Host"
        delay 0.2
        key code 36
    end tell
    ' 2>/dev/null && exit 0
fi

echo "Extension Host 재시작을 위해 수동으로 실행하세요:"
echo "  Cmd+Shift+P > 'Developer: Restart Extension Host'"
exit 1
