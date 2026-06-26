#!/usr/bin/osascript

-- 微信自动化脚本 - 发送消息/图片给联系人
-- 用法: osascript wechat_automation_script.applescript [用户名] [消息内容] [图片路径]
-- 如果不传参数,则从剪切板获取用户名和消息内容
-- 参数说明:
--   $1: 用户名 (可选,不传则从剪切板获取)
--   $2: 消息内容 (可选,可与图片二选一或同时使用)
--   $3: 图片路径或 URL (可选,本地 POSIX 路径或 http(s) 图片地址)

property tempImageDir : ""

on run argv
    -- 获取用户名参数
    set userName to ""
    if (count of argv) >= 1 then
        set userName to item 1 of argv
    end if

    -- 获取消息内容参数
    set messageText to ""
    if (count of argv) >= 2 then
        set messageText to item 2 of argv
    end if

    -- 获取图片路径参数
    set imagePath to ""
    if (count of argv) >= 3 then
        set imagePath to item 3 of argv
    end if

    if imagePath is not "" then
        set imagePath to my resolveImagePath(imagePath)
    end if

    if messageText is "" and imagePath is "" then
        error "消息内容和图片路径不能同时为空"
    end if

  -- 拉起微信（隐藏/最小化时 activate 可能无效，再 open -a WeChat 一次）
    my ensureWeChatVisible()

    delay 0.5

    -- 使用快捷键 Cmd+F 打开搜索框
    tell application "System Events"
        tell process "WeChat"
            keystroke "f" using {command down}
        end tell
    end tell

    delay 1

    -- 输入用户名（使用剪切板粘贴方式）
    if userName is not "" then
        -- 如果提供了用户名参数,先存入剪切板
        set the clipboard to userName
    end if
    -- 直接使用 Cmd+V 粘贴用户名（无论是否提供参数,都使用粘贴方式）
    tell application "System Events"
        tell process "WeChat"
            keystroke "v" using {command down}
        end tell
    end tell

    delay 1

    -- 按回车选择第一个联系人
    tell application "System Events"
        tell process "WeChat"
            keystroke return
        end tell
    end tell

    delay 0.5

    -- 关键：点击微信窗口右下角区域，确保焦点移动到聊天输入框
    my focusChatInput()

    delay 0.5

    -- 发送文本消息（若有）
    if messageText is not "" then
        set the clipboard to messageText
        my pasteInWeChat()
        my sendInWeChat()
    end if

    -- 发送图片（若有）
    if imagePath is not "" then
        my setClipboardFromImageFile(imagePath)
        my pasteInWeChat()
        my sendInWeChat()
    end if

    delay 0.5

    -- 隐藏微信窗口（使用 Cmd+H）
    tell application "System Events"
        tell process "WeChat"
            keystroke "h" using {command down}
        end tell
    end tell

    my cleanupTempImage()
    return "微信消息发送完成"
end run

-- 微信是否已有可交互主窗口（非隐藏、非最小化）
on weChatIsReady()
    tell application "System Events"
        if not (exists process "WeChat") then return false
        tell process "WeChat"
            if (count of windows) is 0 then return false
            try
                if value of attribute "AXMinimized" of window 1 is true then return false
            end try
            return true
        end tell
    end tell
end weChatIsReady

-- 从隐藏/最小化恢复微信主窗口
on ensureWeChatVisible()
    tell application "WeChat" to activate
    delay 0.3

    if not my weChatIsReady() then
        do shell script "open -a WeChat"
        delay 0.6
    end if

    if not my weChatIsReady() then
        error "无法恢复微信主窗口（请确认微信已登录，且终端已授予辅助功能权限）"
    end if
end ensureWeChatVisible

on focusChatInput()
    if not my weChatIsReady() then
        my ensureWeChatVisible()
    end if

    try
        tell application "System Events"
            tell process "WeChat"
                set windowPosition to position of window 1
                set windowSize to size of window 1
                set xCoord to (item 1 of windowPosition) + (item 1 of windowSize) - 25
                set yCoord to (item 2 of windowPosition) + (item 2 of windowSize) - 10
            end tell
        end tell
        my clickAtScreenPosition(xCoord, yCoord)
    on error errWin number numWin
        log "[wechat-automation] 获取微信主窗口坐标失败，已跳过右下角点击 (" & numWin & "): " & errWin
    end try
end focusChatInput

on pasteInWeChat()
    tell application "System Events"
        tell process "WeChat"
            keystroke "v" using {command down}
        end tell
    end tell
    delay 1
end pasteInWeChat

on sendInWeChat()
    tell application "System Events"
        tell process "WeChat"
            keystroke return
        end tell
    end tell
    delay 0.5
    tell application "System Events"
        tell process "WeChat"
            keystroke return
        end tell
    end tell
    delay 0.5
end sendInWeChat

on isHttpUrl(s)
    return s starts with "http://" or s starts with "https://"
end isHttpUrl

on resolveImagePath(imageInput)
    if my isHttpUrl(imageInput) then
        return my downloadImageFromUrl(imageInput)
    end if
    set localPath to my expandPosixPath(imageInput)
    if not my fileExists(localPath) then
        error "图片文件不存在: " & localPath
    end if
    return localPath
end resolveImagePath

on getUrlImageExtension(imageUrl)
    try
        set ext to do shell script "echo " & quoted form of imageUrl & " | sed -E 's/[?#].*//' | sed -E 's/.*\\.([a-zA-Z0-9]+)$/\\1/' | tr '[:upper:]' '[:lower:]'"
        if ext is in {"png", "jpg", "jpeg", "gif", "webp", "tif", "tiff", "bmp"} then return ext
    end try
    return "jpg"
end getUrlImageExtension

on downloadImageFromUrl(imageUrl)
    set tempImageDir to do shell script "mktemp -d /tmp/wechat-img.XXXXXX"
    set ext to my getUrlImageExtension(imageUrl)
    set destPath to tempImageDir & "/image." & ext
    try
        do shell script "curl -fsSL -L --max-time 30 -o " & quoted form of destPath & " " & quoted form of imageUrl
        do shell script "test -s " & quoted form of destPath
    on error
        my cleanupTempImage()
        error "图片下载失败: " & imageUrl
    end try
    if ext is "webp" then
        set jpegPath to tempImageDir & "/image.jpg"
        do shell script "sips -s format jpeg " & quoted form of destPath & " --out " & quoted form of jpegPath & " >/dev/null 2>&1"
        return jpegPath
    end if
    return destPath
end downloadImageFromUrl

on cleanupTempImage()
    if tempImageDir is not "" then
        try
            do shell script "rm -rf " & quoted form of tempImageDir
        end try
        set tempImageDir to ""
    end if
end cleanupTempImage

on expandPosixPath(posixPath)
    if posixPath starts with "~" then
        return do shell script "echo " & quoted form of posixPath
    end if
    return posixPath
end expandPosixPath

on fileExists(posixPath)
    try
        return (do shell script "test -f " & quoted form of posixPath & " && echo yes") is "yes"
    on error
        return false
    end try
end fileExists

on getPathExtension(posixPath)
    set ext to do shell script "basename " & quoted form of posixPath & " | sed 's/.*\\.//'" & " | tr '[:upper:]' '[:lower:]'"
    return ext
end getPathExtension

on setClipboardFromImageFile(posixPath)
    set imgFile to POSIX file posixPath
    set ext to my getPathExtension(posixPath)
    if ext is "png" then
        set the clipboard to (read imgFile as «class PNGf»)
    else if ext is in {"jpg", "jpeg"} then
        set the clipboard to (read imgFile as «class JPEG»)
    else if ext is "gif" then
        set the clipboard to (read imgFile as GIFf)
    else if ext is in {"tif", "tiff"} then
        set the clipboard to (read imgFile as TIFF)
    else
        try
            set the clipboard to (read imgFile as «class PNGf»)
        on error
            set the clipboard to (read imgFile as «class JPEG»)
        end try
    end if
end setClipboardFromImageFile

-- 使用 PATH 中的 cliclick（命令名，非全路径）；失败则跳过，假定输入框已聚焦
on clickAtScreenPosition(x, y)
    set px to x as integer
    set py to y as integer
    try
        do shell script "cliclick c:" & px & "," & py
        log "[wechat-automation] cliclick 点击成功，坐标 (" & px & "," & py & ")"
    on error errMsg number errNum
        log "[wechat-automation] cliclick 点击失败 (" & errNum & "): " & errMsg & "，坐标 (" & px & "," & py & ")"
    end try
end clickAtScreenPosition
