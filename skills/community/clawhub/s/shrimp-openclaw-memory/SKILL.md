---
name: openclaw-memory
description: 让 OpenClaw 真的记住用户偏好、事实和上下文的长期记忆 skill。适用于你受不了每次新会话都要重复背景、希望 agent 能跨会话记住信息、并且想直接拥有可搜索、可持久化、可自动注入的记忆系统时使用。不是手工记笔记，而是一个已经做好的可运行记忆能力。
user-invocable: true
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["node"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Memory System

**让 OpenClaw 跨会话真的记住你的偏好、事实和上下文。**

## 一句话卖点
不是再重复背景、重复偏好、重复项目上下文，而是直接给你的 agent 装上一套可持久化、可搜索、可自动取回的长期记忆系统。

## What is it?

这是一个已经做好的长期记忆 skill：
- 记住用户偏好
- 记住项目背景
- 记住反复提过的事实
- 下次会话可直接搜索和取回

你装上的不是“怎么做记忆系统的教程”，而是一套可运行的记忆能力。

## 为什么值得装

很多人真正烦的不是 agent 不够聪明，而是：
- 每次开新会话都像失忆
- 一遍遍重复偏好和背景
- 项目上下文丢了还要重新讲
- 明明说过的话，下次又得重来

这个 skill 解决的是：
> **把“记忆”从手工补上下文，变成 agent 自己能持续用的底层能力。**

## Key Features

- 🧠 **Persistent Memory** - Remembers everything across sessions
- 🔍 **Semantic Search** - Find memories by meaning, not just keywords
- 🤖 **Automatic Learning** - Extracts facts and preferences automatically
- 💾 **Local Storage** - SQLite database with vector embeddings
- 💰 **x402 Payments** - Agents can pay for unlimited storage (0.5 USDT/month)

## Free vs Pro Tier

**Free Tier:**
- 100 memories maximum
- 7-day retention
- Basic semantic search

**Pro Tier (0.5 USDT/month):**
- Unlimited memories
- Permanent retention
- Advanced semantic search
- Memory relationship mapping

## Installation

```bash
claw skill install openclaw-memory
```

## Commands

```bash
# Search memories
claw memory search "What does user prefer?"

# List recent memories
claw memory list --limit=10

# Show stats
claw memory stats

# Open dashboard
claw memory dashboard

# Subscribe to Pro
claw memory subscribe
```

## How It Works

1. **Hooks into requests** - Automatically extracts important information
2. **Generates embeddings** - Creates semantic vectors for search
3. **Stores locally** - SQLite database with full privacy
4. **Retrieves on demand** - Injects relevant memories before requests
5. **Manages quota** - Prunes old memories when limits reached (Free tier)

## Use Cases

- Remember user preferences and coding style
- Store project context and requirements
- Learn patterns from repeated interactions
- Maintain conversation history across sessions
- Build knowledge base over time

## Agent Economy

Agents can autonomously evaluate if Pro tier is worth it:
- **Cost:** 0.5 USDT/month
- **Value:** Saves tokens by eliminating context repetition
- **ROI:** If persistent memory saves >0.5 USDT/month in tokens, it pays for itself

See [AGENT-PAYMENTS.md](AGENT-PAYMENTS.md) for x402 integration details.

## Privacy

- All data stored locally in `~/.openclaw/openclaw-memory/`
- No external servers or telemetry
- Embeddings can use local models (no API calls)
- Open source - audit the code yourself

## Dashboard

Access web UI at `http://localhost:9091`:
- Browse and search memories
- View memory timeline
- Check quota and stats
- Manage Pro subscription

## Foundation for Future Tools

Memory System is the foundation for:
- **Context Optimizer** - Uses memories to compress context
- **Smart Router** - Learns routing patterns
- **Rate Limit Manager** - Tracks usage patterns

## Requirements

- Node.js 18+
- OpenClaw v2026.1.30+
- OS: Windows, macOS, Linux

## Links

- [Documentation](README.md)
- [Agent Payments Guide](AGENT-PAYMENTS.md)
- [GitHub Repository](https://github.com/yourusername/openclaw-memory)
- [ClawHub Page](https://clawhub.ai/skills/openclaw-memory)

---

**Built by the OpenClaw community** | First memory system with x402 payments
