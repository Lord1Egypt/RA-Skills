---
name: wechat-qwen-reply
description: WeChat chat reader + auto-reply (Qwen-VL vision + AHK send). Supports fast/slow capture, group nickname labels, file/red-packet cards, and filtering system messages on Windows.
---

# WeChat Qwen Reply

## 快速开始

### 1) 读聊天文本（默认快模式）
```
python scripts/qwen_vl_read.py "群名或联系人"
```

### 2) 稳模式（全屏截图+裁剪）
```
python scripts/qwen_vl_read.py "群名或联系人" --slow
```

### 3) 调试输出最近截图
```
python scripts/qwen_vl_read.py "群名或联系人" --debug
```

## 关键说明
- 依赖 AHK v2、微信 PC、Python 3.12
- DashScope API Key 存在：`C:\Users\chenxun\.nanobot\workspace\.secrets\dashscope_api_key.txt`
- 默认快模式：直接截聊天区域（更快）；若坐标不准可改用 `--slow`
- 截图坐标（已校准）：左上 (386,68)，右下 (1891,842)

## 脚本说明
- `scripts/qwen_vl_read.py`：读取聊天文本（Qwen-VL）
- `scripts/wechat_capture_fast.ps1`：快模式截图
- `scripts/wechat_capture_crop.ps1`：稳模式截图
- `scripts/wechat_send_chat.ahk`：发送消息（剪贴板粘贴，避免标点错乱）

## 输出
- 最近一次识别文本：`C:\Users\chenxun\.nanobot\workspace\qwen_chat_last.txt`
- 最近一次裁剪图：`C:\Users\chenxun\.nanobot\workspace\qwen_last_crop.png`

## 提示词逻辑（已内置）
- 顺序：从上到下（旧→新）
- 识别：绿色气泡=我，白色气泡=对方；颜色不清晰则参考左右位置
- 群聊：尽量标注具体昵称
- 文件/红包卡片：标注发送方并写明【文件卡片】/【红包卡片】
- 系统提示：不输出
