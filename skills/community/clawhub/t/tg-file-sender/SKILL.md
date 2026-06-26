---
name: tg-file-sender
description: >
  Send local files directly to Telegram chat. Supports documents, photos, and other media types.
  Use when user says: "send this file to me", "send to telegram", "把文件发给我", "通过tg发送",
  or any request to deliver a workspace file via Telegram. Handles file path resolution,
  size validation, and secure token management.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
      env:
        - TG_BOT_TOKEN
    primaryEnv: "TG_BOT_TOKEN"
    emoji: "📤"
    homepage: https://clawhub.ai/BusTes01/tg-file-sender
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
---

# 📤 Telegram File Sender

Send local files directly to a Telegram chat using the Bot API. The bot token is read from environment variable `TG_BOT_TOKEN` — never hardcoded or logged.

## Prerequisites

- `TG_BOT_TOKEN` environment variable must be set
- `curl` must be available
- The target chat must have started a conversation with the bot

## Usage

### Step 1: Resolve File Path

Accept a file path from the user. Resolve it relative to the workspace:

```bash
FILE_PATH="<workspace>/<user-provided-path>"
```

**Security rules:**
- Resolve to absolute path using `realpath`
- Reject if path does not start with the workspace root
- Reject if file does not exist
- Reject if file is a symlink (avoid directory traversal)
- Reject if file size > 50 MB (Telegram document limit)

### Step 2: Detect File Type

Use the file extension to determine the appropriate Telegram method:

| Extension | Method | Caption support |
|-----------|--------|-----------------|
| `.jpg` `.jpeg` `.png` `.gif` `.webp` | `sendPhoto` | ✅ Yes |
| `.mp4` `.mov` `.avi` `.webm` | `sendVideo` | ✅ Yes |
| `.mp3` `.ogg` `.wav` `.flac` | `sendAudio` | ✅ Yes |
| Others (`.xlsx`, `.pdf`, `.md`, `.zip`, etc.) | `sendDocument` | ✅ Yes |

### Step 3: Send via Bot API

```bash
BOT_TOKEN="$TG_BOT_TOKEN"
CHAT_ID="<target chat ID>"
FILE_PATH="<resolved absolute path>"
CAPTION="<optional description>"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="$CHAT_ID" \
  -F document=@"$FILE_PATH" \
  -F caption="$CAPTION"
```

For photos:

```bash
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto" \
  -F chat_id="$CHAT_ID" \
  -F photo=@"$FILE_PATH" \
  -F caption="$CAPTION"
```

### Step 4: Handle Response

Parse the JSON response:
- If `ok: true` → confirm delivery: "✅ 文件已发送"
- If `ok: false` → report the `description` field to the user

## Privacy & Security Guidelines

1. **Token protection:** Never log, echo, or display the bot token value. Use `$TG_BOT_TOKEN` only in the API call URL.
2. **Path traversal prevention:** Always resolve with `realpath` and verify the result starts with the workspace root.
3. **No content logging:** Do not log file contents or read file contents for any purpose beyond sending.
4. **Size limit:** Enforce 50 MB maximum (Telegram Bot API limit for documents).
5. **User confirmation:** For files > 10 MB, warn the user about size before sending.
6. **Chat ID:** Use the `chat_id` from the session context. Never prompt the user for a chat ID.
7. **Ephemeral files:** If the file is in `/tmp/`, clean up after sending.

## Behavior Rules

- If `TG_BOT_TOKEN` is unset → tell the user: "请先设置 TG_BOT_TOKEN 环境变量"
- If the file doesn't exist → "文件不存在，请检查路径"
- If the file is outside workspace → "路径不在工作目录范围内，已拒绝"
- If the file exceeds 50 MB → "文件超过 50MB，Telegram 不支持发送"
- If the API returns an error → show the error description to the user

---

# 📤 Telegram 文件发送器

通过 Telegram Bot API 将本地文件直接发送到聊天窗口。Bot Token 从环境变量 `TG_BOT_TOKEN` 读取，绝不硬编码或写入日志。

## 前提条件

- 需设置 `TG_BOT_TOKEN` 环境变量
- 需安装 `curl`
- 目标聊天对象需已与 bot 有过对话

## 使用方法

### 第一步：解析文件路径

接收用户提供的路径，相对于工作目录解析：

```bash
FILE_PATH="<workspace>/<用户提供的路径>"
```

**安全检查：**
- 用 `realpath` 解析为绝对路径
- 拒绝不在工作目录范围内的路径
- 拒绝不存在的文件
- 拒绝符号链接（防止目录穿越）
- 拒绝大于 50MB 的文件

### 第二步：识别文件类型

根据扩展名选择发送方式：

| 扩展名 | 方法 | 支持标题 |
|--------|------|---------|
| `.jpg` `.jpeg` `.png` `.gif` `.webp` | `sendPhoto` | ✅ 是 |
| `.mp4` `.mov` `.avi` `.webm` | `sendVideo` | ✅ 是 |
| `.mp3` `.ogg` `.wav` `.flac` | `sendAudio` | ✅ 是 |
| 其他（`.xlsx` `.pdf` `.md` `.zip` 等） | `sendDocument` | ✅ 是 |

### 第三步：通过 Bot API 发送

```bash
BOT_TOKEN="$TG_BOT_TOKEN"
CHAT_ID="<目标聊天ID>"
FILE_PATH="<解析后的绝对路径>"
CAPTION="<可选描述>"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="$CHAT_ID" \
  -F document=@"$FILE_PATH" \
  -F caption="$CAPTION"
```

### 第四步：处理响应

解析 JSON 响应：
- `ok: true` → 确认发送："✅ 文件已发送"
- `ok: false` → 向用户展示 `description` 字段中的错误信息

## 隐私与安全规范

1. **Token 保护：** 绝不打印、记录或显示 bot token。仅在 API 调用 URL 中使用 `$TG_BOT_TOKEN`
2. **路径穿越防护：** 始终用 `realpath` 解析，验证结果以工作目录开头
3. **不记录内容：** 不读取或记录文件内容
4. **大小限制：** 上限 50MB
5. **大文件提醒：** 大于 10MB 时提醒用户
6. **Chat ID：** 从会话上下文获取，不向用户询问
7. **临时文件：** /tmp 下的文件发送后清理

## 行为规则

- `TG_BOT_TOKEN` 未设置 → "请先设置 TG_BOT_TOKEN 环境变量"
- 文件不存在 → "文件不存在，请检查路径"
- 路径不在工作目录内 → "路径不在工作目录范围内，已拒绝"
- 文件超过 50MB → "文件超过 50MB，Telegram 不支持发送"
- API 返回错误 → 将错误描述展示给用户
