---
name: wx-send
description: 发送微信消息给指定联系人。支持两种模式：(1) 有消息内容：直接发送指定消息；(2) 无消息内容：OCR 截图识别聊天窗口内容并自动回复。当用户需要自动发送微信消息、自动回复微信聊天时触发此技能。
---

# WX-Send

发送微信消息给指定联系人。

## 功能概述

通过 AppleScript 模拟键盘操作，自动完成微信消息发送。

## 技术栈

- **AppleScript** - macOS 自动化脚本语言
- **System Events** - macOS 系统事件处理
- **osascript** - 命令行执行 AppleScript 工具
- **pyautogui** - Python 版本的鼠标键盘控制（可选）

## 工作原理

通过模拟键盘快捷键控制微信客户端 UI：

| 步骤 | 操作 | 工具/命令 |
|------|------|-----------|
| 1 | 激活微信应用 | `tell application "WeChat"` |
| 2 | 复制联系人到剪贴板 | AppleScript `set the clipboard to` |
| 3 | 打开搜索框 | `keystroke "f" using command down` |
| 4 | 粘贴联系人名称 | `keystroke "v" using command down` |
| 5 | 按回车键 | `keystroke return` |
| 6 | 按下箭头选择搜索结果 | `keystroke (ASCII character 31)` |
| 7 | 按上箭头取消选择 | `keystroke (ASCII character 30)` |
| 8 | 再次回车进入聊天 | `keystroke return` |
| 9 | 复制消息到剪贴板 | AppleScript `set the clipboard to` |
| 10 | 粘贴消息 | `keystroke "v" using command down` |
| 11 | 发送消息 | `keystroke return` |

## 完整脚本 (wx_send.applescript)

```applescript
on run argv
    set contactName to item 1 of argv
    set messageText to ""
    
    if (count of argv) > 1 then
        set messageText to item 2 of argv
    end if
    
    tell application "WeChat"
        activate
        delay 0.5
    end tell
    
    set the clipboard to contactName
    
    tell application "System Events"
        tell process "WeChat"
            -- 打开搜索框 (Cmd+F)
            keystroke "f" using command down
            delay 1
            -- 粘贴联系人名称
            keystroke "v" using command down
            delay 2
            -- 回车
            keystroke return
            delay 1
            -- 按一次下箭头
            keystroke (ASCII character 31)
            delay 0.5
            -- 按一次上箭头
            keystroke (ASCII character 30)
            delay 0.5
            -- 再次回车进入聊天
            keystroke return
            delay 2
        end tell
    end tell
    
    if messageText is not "" then
        set the clipboard to messageText
        
        tell application "System Events"
            tell process "WeChat"
                delay 1
                -- 粘贴消息
                keystroke "v" using command down
                delay 0.5
                -- 发送
                keystroke return
            end tell
        end tell
        return "Sent: " & messageText
    else
        return "Ready"
    end if
end run
```

## 使用方法

### 发送消息（推荐）

```bash
# 方法1：复制 wx_send.applescript.txt 内容手动创建 .applescript 文件
# 然后执行：
osascript scripts/wx_send.applescript "联系人名称" "消息内容"

# 方法2：使用 Python 版本
python3 scripts/wx_send.py "联系人名称" "消息内容"
```

### AppleScript 文件创建方法

1. 打开文本编辑器（如 TextEdit）
2. 复制 `scripts/wx_send.applescript.txt` 的内容
3. 保存为 `wx_send.applescript`（无后缀）
4. 赋予执行权限：`chmod +x wx_send.applescript`

### 示例

```bash
# 给"怪兽"发送消息"你好"
python3 scripts/wx_send.py "怪兽" "你好"
```

## 依赖要求

### macOS 权限

首次使用需要授权辅助功能权限：
1. 打开 **系统偏好设置** → **安全性与隐私** → **隐私** → **辅助功能**
2. 添加 `osascript` 或终端应用

### Python 依赖（可选）

```bash
pip3 install pyautogui
```

## 注意事项

- 联系人名称需与微信备注名完全一致
- 微信必须处于未登录状态或已解锁状态
- 需要保持屏幕常亮，避免自动锁定
- 中文消息推荐使用 AppleScript 版本发送

## 进阶：OCR 自动回复

如需 OCR 截图识别自动回复，可使用 `wx_ocr_reply.py`（需要配置 OpenAI API）。
