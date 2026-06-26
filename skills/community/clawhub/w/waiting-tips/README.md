# openclaw-waiting-tips

> 75 bilingual tips — learn while OpenClaw thinks!
>
> OpenClaw 思考时显示 75 条中英双语 tips，等待变学习！

```
💡 给 AI 足够的上下文，回答质量翻倍 | Give AI enough context — quality doubles
```

Every time you chat with OpenClaw on Telegram, Feishu, WhatsApp, Discord, or any platform, a random tip shows while the AI is thinking. Non-intrusive, bilingual, useful.

在 Telegram、飞书、WhatsApp、Discord 等任何平台和 OpenClaw 聊天时，AI 思考期间随机显示一条 tip。不打断、双语、实用。

## Install | 安装

### Method 1: ClawHub (recommended)

```bash
clawhub install waiting-tips
```

### Method 2: Local install

```bash
git clone https://github.com/dongsheng123132/openclaw-waiting-tips.git
openclaw plugins install -l ./openclaw-waiting-tips
```

### Method 3: Manual

Copy the `openclaw-waiting-tips/` folder to `~/.openclaw/skills/waiting-tips/`

```bash
cp -r openclaw-waiting-tips ~/.openclaw/skills/waiting-tips
```

**Done.** Tips will show up next time you chat with OpenClaw.

**搞定。** 下次和 OpenClaw 聊天就能看到 tips。

## How It Works | 原理

```
You send a message on Telegram/Feishu/WhatsApp
         │
         ▼
   OpenClaw receives it
         │
    ┌────▼────┐
    │ waiting  │──▶  💡 Random tip sent immediately
    │ _tip     │     (< 100ms, while AI thinks)
    └────┬────┘
         │
    ┌────▼────┐
    │ AI      │  ← 3~10 seconds processing
    │ thinks  │
    └────┬────┘
         │
    ┌────▼────┐
    │ Full    │──▶  AI response sent
    │ response│
    └─────────┘
```

The plugin registers a `waiting_tip` tool. OpenClaw can call it before processing complex requests, or when users ask for tips directly.

## Usage | 使用

### Automatic (built into OpenClaw flow)

Just chat normally — tips appear automatically during wait times.

### Manual (ask for tips)

```
You: 来个 tip
Bot: 💡 Chain of Thought: 让 AI 一步步思考 | Chain of Thought: make AI think step by step

You: show me 3 tips
Bot: 💡 AI 的输出质量 = 你的输入质量 | AI output quality = your input quality
     💡 用 AI 写正则表达式比自己写快10倍 | AI writes regex 10x faster than you
     💡 好的提问是一种超能力 | Asking good questions is a superpower
```

## Display Styles | 显示风格

| Style | Example |
|-------|---------|
| `emoji` (default) | 💡 中文 tip \| English tip |
| `card` | Bordered card with header |
| `zh-only` | 💡 只显示中文 |
| `en-only` | 💡 English only |

## 75 Tips in 5 Categories | 75 条 Tips，5 大分类

| Category 分类 | Count | Content 内容 |
|------|------|------|
| **AI Interaction** | 15 | Context, multi-turn, verification, constraints |
| **Prompt Engineering** | 15 | CoT, ReAct, few-shot, meta-prompting |
| **OpenClaw** | 15 | Commands, features, best practices |
| **Productivity** | 15 | Code review, regex, templates, reports |
| **Wisdom** | 15 | AI philosophy, learning mindset |

## Add Your Own Tips | 添加 Tips

```bash
# 1. Add a line to any tips/*.txt file
echo "你的新 tip | Your new tip" >> tips/productivity.txt

# 2. Verify
node test.js

# 3. Open a PR
```

New category? Create `tips/coding.txt` — auto-loaded.

## Works On All Platforms | 全平台支持

Telegram · Feishu/Lark · WhatsApp · Discord · Slack · Signal · iMessage · and any other platform OpenClaw supports.

## License

MIT
