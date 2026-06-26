---
name: subagent-bridge
description: "Bridge communication between subagents via sessions_send — pipeline, debate, broadcast, and aggregate patterns."
metadata:
  openclaw:
    emoji: "🌉"
allowed-tools:
  - sessions_list
  - sessions_send
  - sessions_history
  - session_status
license: MIT
---

# Subagent Bridge 🌉 — 子会话传话

Let different subagents (child sessions) chat with each other under the same
OpenClaw agent. Tell your main session what to do in plain language — no
complex commands needed.

让同一个 OpenClaw 下的不同子会话（subagent）之间互相传话。
你在聊天框里像跟人说话一样发号施令就行。

---

## 🏷️ First: Give Them Names / 先说最重要的：起名字

**Every subagent that you want to bridge needs a memorable name when spawned.**
**每个要长期用、要互相传话的子会话，spawn 时就给它起个容易记住的名字。**

```
You → Main:  spawn a search expert, call it 搜搜 (Soso)
  Main → You: 搜搜 (agent:main:subagent:xxx) is ready!

You → Main:  spawn an analysis expert, call it 想想 (Xiangxiang)
  Main → You: 想想 (agent:main:subagent:yyy) is ready!
```

The main session remembers the name ↔ session-key mapping. Later you just
refer to them by name.

主会话会记住这个映射关系。后面传话你直接叫名字就行。

---

## 🗣️ How to Use / 怎么用

Say these to your main session naturally. 对主会话说人话就行。

| What you want | Say this | 你可以说 |
|--------------|----------|---------|
| Talk to one subagent | `ask 搜搜：xxx` `tell 想想：xxx` `send message to 搜搜：xxx` | `问 搜搜：xxx` `传话给 想想：xxx` `告诉 搜搜：xxx` |
| Pipe one's output to another | `let 搜搜 pass its result to 想想` | `让 搜搜 查完结果给 想想` |
| Two subagents debate | `let 搜搜 and 想想 debate about xxx` | `让 搜搜 和 想想 讨论一下 xxx` |
| Broadcast to many | `ask 搜搜, 想想, coder: xxx` | `问 搜搜、想想、编程小子：xxx` |
| Gather then summarize | `let 搜搜, 想想 each work on this, then send results to 汇总大师` | `让 搜搜、想想 各做各的，结果给 汇总大师` |

---

## ⚙️ How the Main Session Does It / 主会话内部做的工作

### Step 1: Find the subagent / 找人

```text
sessions_list(kinds: ["subagent"])
```

Match by friendly name → get sessionKey.

### Step 2: Send the message / 传话

```text
sessions_send(sessionKey="agent:main:subagent:<uuid>", message="...", timeoutSeconds=N)
```

- `timeoutSeconds: 0` — fire-and-forget, no reply expected
- `timeoutSeconds: >0` — wait for reply. Search tasks: 60-90s, analysis: 30-60s

### Step 3: Multi-turn dialogue (A ↔ B debate / 多轮讨论)

Both sides can reply. Send `REPLY_SKIP` to end your turn early.
Max rounds: 5 (configurable up to 20 via `session.agentToAgent.maxPingPongTurns`).

---

## 📐 Bridge Patterns / 四种传话模式

### 📊 Pipeline（流水线）

```
User → Main spawns 搜搜 → 搜搜's result sent to 想想 → 想想 analyzes and returns
```

### 💬 Debate（辩论）

```
Main: "搜搜, do analysis → pass result to 想想"
Main: "想想, critique 搜搜's result → pass critique back"
Loop until consensus or max rounds.
```

### 📢 Broadcast（广播）

```
Main sends the same message to 搜搜, 想想, coder simultaneously.
Aggregate all replies.
```

### 🤝 Aggregate（汇总）

```
搜搜, 想想, coder each work independently.
Main collects results → sends them all to 汇总大师 for a summary.
```

---

## ⚠️ Limits / 限制

- `sessions_send` cannot target thread-scoped chat sessions.
- Cross-agent bridging needs `tools.agentToAgent.enabled: true` in config.
- Subagents are ephemeral — bridge them while they're alive.
- `sessions_send` 不能发到 thread 类型的聊天会话。
- 跨不同 agentId 的传话需要配置 `tools.agentToAgent.enabled: true`。
- 子会话用完就过期，要传话趁它活着的时候。
