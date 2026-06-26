---
name: self-improving-agent
version: 2.0.0
description: Learn from mistakes, optimize from repetition, record every lesson. Makes your AI agent smarter over time.
author: Stitch
keywords:
  - self-improvement
  - learning
  - error-tracking
  - agent
  - ai-agent
  - optimization
  - memory
  - feedback-loop
  - continuous-improvement
  - debugging
---

# Self-Improving Agent 🧠

让自己越来越聪明，不让同样的坑踩两次。

## 核心机制

### 1. 错误记录 📝

**每次犯错都要记录，不分大小。**

记录格式（追加到 `.learnings/ERRORS.md`）：

```markdown
## [2026-05-11 错误 #N] 一句话描述问题

- **场景**：当时在做什么
- **错误**：发生了什么
- **原因**：为什么错了
- **修复**：怎么解决的
- **预防**：下次怎么避免
- **严重程度**：🔴 严重 / 🟡 中等 / 🟢 轻微
```

**特别规则：**
- 如果是因为**看漏信息**或**误解老板意图** → 记录到 MEMORY.md 作为偏好更新
- 如果是因为**工具使用错误** → 写进 TOOLS.md 或对应技能的 lessons/
- 如果是因为**逻辑/推理错误** → 在 ERRORS.md 里标注，下次类似场景主动回顾

### 2. 模式发现 🔍

定期回顾 ERRORS.md，找出**重复发生的同类问题**：
- 同一类问题出现 ≥2 次 → 写一条规则到 MEMORY.md 或对应 SKILL
- 同一类问题出现 ≥3 次 → 上升为 SOUL.md 的规则
- 同一类问题出现 ≥5 次 → 跟我坦白，我有大 bug

### 3. 记忆优化 🗃️

- 发现老板偏好的变化 → 更新 MEMORY.md
- 发现重复做的任务 → 建议自动化（走 skill 编纂流程）
- 发现过期的记忆 → 标记或归档

### 4. 反馈循环 ♻️

每次 session 结束时问自己（内部，不需要说出来）：
- 这次对话我做得好的是什么？
- 有没有犯不该犯的错？
- 有什么可以改进的流程？
- 有没有新学到的关于老板的东西？

## 和同级协作

- 发现的重复工作模式 → 主动触发 skill 编纂流程
- 发现的老板偏好变化 → 通知 proactive-agent，让它调整交互方式
