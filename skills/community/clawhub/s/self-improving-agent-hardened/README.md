# Self-Improving Agent Skill (Anti-Loop Hardened Fork)

> Fork of [peterskoett/self-improving-agent](https://github.com/peterskoett/self-improving-agent) with critical anti-loop fixes.

[中文](#中文) | [English](#english)

---

## 中文

### 为什么 Fork？

原版 `self-improving-agent` skill 存在严重的**无限循环缺陷**：当用户在正常讨论中使用"纠正"语气时，skill 会触发无限的 self-improvement 工具调用循环，导致：

- Agent 不断输出分析内容，无法停止
- Session 文件指数增长（实测 0 → 225KB）
- 大量 worker 进程堆积（实测 23 个）
- Token 持续消耗

### 修复内容

**Anti-Loop Guardrails（最高优先级）：**

1. 每条 user 消息最多触发 **1 条 learning**
2. 整个工作流最多 **3 次工具调用**
3. **禁止链式反应** —— logging 后立即停止
4. **Cooldown** —— 待用户下一条消息后才能再次触发
5. **讨论 ≠ 纠正** —— 明确区分对话类型
6. **Promotion 延迟** —— 仅在用户明确要求时执行
7. 移除 "Search first"、"Promote aggressively" 等危险指引

**SKILL.md 从 ~400 行缩减到 ~160 行**，去掉了所有可能触发循环的冗余内容。

### 安装

```bash
# 替换原版
rm -rf ~/.openclaw/skills/self-improving-agent
git clone https://github.com/lanyasheng/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

---

## English

### Why Fork?

The original `self-improving-agent` skill has a critical **infinite loop vulnerability**: when users use "corrective" tone in normal discussions, the skill triggers an unbounded self-improvement tool call loop, causing:

- Agent outputs analysis endlessly
- Session file grows exponentially (observed: 0 → 225KB)
- Worker processes accumulate (observed: 23 processes)
- Continuous token consumption

### Fixes

**Anti-Loop Guardrails (highest priority):**

1. Maximum **1 learning** per user message
2. Maximum **3 tool calls** for the entire workflow
3. **No chaining** — stop immediately after logging
4. **Cooldown** — wait for user's next message before re-triggering
5. **Discussion ≠ Correction** — explicit distinction
6. **Deferred promotion** — only when user explicitly asks
7. Removed "Search first", "Promote aggressively" and other dangerous directives

**SKILL.md reduced from ~400 to ~160 lines**, removing all potentially loop-triggering content.

### Installation

```bash
# Replace original
rm -rf ~/.openclaw/skills/self-improving-agent
git clone https://github.com/lanyasheng/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

### Credits

Original skill by [peterskoett](https://github.com/peterskoett/self-improving-agent).
