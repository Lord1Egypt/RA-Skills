---
name: reply-wechat-message
slug: wechat-butler
displayName: 微信管家 / WeChat Butler
description: "微信AI助手 — 主动发消息 + 自动回复 / WeChat AI assistant — send messages & auto-reply"
agent_created: true
---

# 微信管家 / WeChat Butler

微信AI助手 — 主动发消息给联系人 + 收到消息后AI自动回复。
WeChat AI assistant — proactively send messages, and auto-reply when messages come in.

**自包含技能包** — 所有依赖脚本（启动微信、发送消息）已打包在内，无需额外安装。
**Self-contained skill** — all dependency scripts (launch WeChat, send messages) are bundled. No extra installation needed.

---

## 功能一：AI 主动发消息 / Feature 1: Send Message

直接发送一条消息给指定联系人（不读取聊天上下文，即时发送）。
Send a message directly to a contact (no context reading, instant send).

### 触发格式 / Trigger Format

**中文 / Chinese:**
```
给 [联系人] 发消息：[内容]
发消息给 [联系人]：[内容]
帮 [联系人] 发消息：[内容]
```

**English:**
```
send [contact] [message]
msg [contact] [message]
message [contact] [message]
```

### 示例 / Examples

**中文 / Chinese:**
- `给 小明 发消息：中午一起去吃饭吗？`
- `发消息给 小红：记得带文件`
- `帮 小张 发消息：生日快乐！`

**English:**
- `send Kitty: Want to grab lunch?`
- `msg Peter: Don't forget the documents`
- `message Tom: Happy birthday!`

### AI 执行步骤 / Execution Steps

```
第1步 / Step 1:
  AI 提取联系人和消息内容
  AI extracts contact name and message content

第2步 / Step 2:
  python scripts/send_wechat.py <联系人/contact> <内容/message>
  → 打开微信 → 搜索联系人 → 打开聊天 → 发送消息
  → Open WeChat → search contact → open chat → send message

第3步 / Step 3:
  返回发送结果给用户
  Report send result to user
```

---

## 功能二：AI 自动回复 / Feature 2: AI Auto-Reply

读取聊天上下文，AI 分析后自动回复。
Reads the chat context, AI analyzes it, then auto-replies.

### 触发格式 / Trigger Format

```
使用技能:reply-wechat-message 给：[联系人] 回复
```

### 示例 / Examples
- `使用技能:reply-wechat-message 给：小明 回复` (Xiao Ming / Kitty)
- `使用技能:reply-wechat-message 给：小红 回复` (Xiao Hong / Peter)

### 简化触发 / Short Forms
- 回复 小明 / reply Kitty
- 回 小红 / reply Peter

---

## AI 工作流程（自动回复）/ AI Workflow (Auto-Reply)

```
第1步 / Step 1:
  python scripts/reply_wechat.py 小明 / python scripts/reply_wechat.py Kitty
  → 读取整个聊天区域，区分左右两侧
  → Read entire chat area, split left/right
  → 输出结构化对话 / Output structured conversation:
    ★上下文开始★ / ★Context Start★
    [对方/Them] xxx
    [我/Me] xxx
    [对方/Them] xxx
    ★上下文结束★ / ★Context End★

第2步 / Step 2:
  AI分析全部上下文，理解对话脉络，生成合适的回复
  AI analyzes full context, understands the conversation flow, generates a suitable reply

  ⚠️ 重要规则 / Important Rule:
  OCR识别出的聊天内容即为真实上下文，模型不得质疑、猜测或怀疑识别结果的准确性。
  The OCR-recognized text IS the real context. The model must NOT question, guess,
  or doubt the accuracy of the recognition. Reply based on the recognized content directly.

第3步 / Step 3:
  echo "AI生成的回复 / AI-generated reply" | python scripts/reply_wechat.py 小明
  → 或 / Or: echo "AI-generated reply" | python scripts/reply_wechat.py Kitty
  → 读取上下文 + 自动发送回复（一步完成，stdin管道无引号问题）
  → Read context + send reply in one step (stdin piping avoids quote issues)
```

---

## 脚本 / Scripts

`scripts\send_wechat.py` — 发送脚本：搜索联系人 + 发送消息 / Send script: search contact + send message
`scripts\reply_wechat.py` — 主脚本：读取上下文 + 发送回复 / Main script: read context + send reply
`scripts\open_wechat.py` — 启动脚本：唤醒微信窗口 / Launch script: bring WeChat to foreground

### send_wechat.py 用法 / Usage
```bash
# 发送消息 / Send message (command line arg)
python scripts/send_wechat.py <小明/Kitty> <消息/message>

# 发送消息（stdin管道，无引号问题）/ Send message (stdin pipe, no quote issues)
echo "消息/message" | python scripts/send_wechat.py <小明/Kitty>
```

### reply_wechat.py 用法 / Usage
```bash
# 只读取上下文（AI分析用）/ Read context only (for AI analysis)
python scripts/reply_wechat.py <小明/Kitty>

# 读取上下文 + 发送回复（一步到位）/ Read context + send reply (one step)
echo "回复内容/reply text" | python scripts/reply_wechat.py <小明/Kitty>
```

### 输出格式 / Output Format
```
★上下文开始★ / ★Context Start★
[对方/Them] 你吃饭了吗 / Have you eaten?
[我/Me] 吃过了，你呢 / Yes, and you?
[对方/Them] 我也吃了 / Me too
★上下文结束★ / ★Context End★
```

---

## 消息区分逻辑 / Message Detection Logic

- **左侧（白底黑字）/ Left side (white bg, black text)** = 对方发的消息 / Messages from the other party → 标注 `[对方/Them]`
- **右侧（绿底黑字）/ Right side (green bg, black text)** = 自己发的消息 / Messages from yourself → 标注 `[我/Me]`
- 截图聊天区从中线切开，左右分别OCR，避免颜色误判
  Screenshot is split at the center line; left and right are OCR'd separately to avoid color misidentification

---

## 依赖 / Dependencies

- Python 3.10+
- OCR.space API（免费版，无需注册 / Free tier, no registration required）
- Python packages: pyautogui, pygetwindow, pyperclip, requests, Pillow, numpy

---

## 脚本清单 / Script Inventory

| 文件 / File | 功能 / Function |
|---|---|
| `send_wechat.py` | 搜索联系人 + 发送消息 / Search contact & send message |
| `reply_wechat.py` | 读取上下文 + 发送回复 / Read context & send reply |
| `open_wechat.py` | 启动微信 / Launch WeChat |
