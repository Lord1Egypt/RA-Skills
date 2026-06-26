# OpenClaw Self-Check

[![Stars](https://img.shields.io/github/stars/Eita19/openclaw-skills?style=flat)](https://github.com/Eita19/openclaw-skills)
[![Based on](https://img.shields.io/badge/based-Y7%20Framework-FF6B6B?style=flat)](https://github.com/Y7-ai)
[![Version](https://img.shields.io/badge/version-7.2.0-FF6B6B?style=flat)](self-check/SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 🤖 **Multi-dimensional critical thinking for AI agents** — based on Y7 framework + Three Provinces Six Ministries

**Think before you act. Check before you deliver.**

---

## What is Self-Check?

Before any task delivery, run through a checklist:

```
任务对吗？✅❌
有更好的方向吗？💡
执行路径通吗？🔧
```

**Four Questions:**
1. Is this task right?
2. Is there a better direction?
3. What risks might be ignored?
4. Should I raise a challenge?

---

## Framework

### Simple Task (3 questions)
```
任务对吗？✅❌
有更好的方向吗？💡
执行路径通吗？🔧
不寻常的主张？⚠️ 需不寻常证据
```

### Complex Task (+ execution path)
```
视角：[批判/创造/风险/收益]
执行步骤
有没有工具/权限/资源限制？
```

---

## Task Decompose

| Layer | How |
|-------|-----|
| Leaf | Execute directly |
| Parallel | Spawn sub-agents |
| Merge | Sequential orchestration |

---

## Quality Control

### Three Gates
- **Pre-Check** → Don't execute
- **Mid-Check** → Don't advance
- **Post-Check** → Don't deliver

### Five Self-Checks
1. Data authenticity
2. Information completeness
3. Format consistency
4. Logical correctness
5. Deliverable standard

---

## Checkpoint Logging (v7.2+)

Every task must produce a checkpoint log entry with:
- Task ID, type, thinking rounds
- Challenge points raised
- Alternative options compared
- Final choice with reasoning
- Confidence level (0-100%)

---

## Behavior Tracking (v7.2+)

Before any delivery, append to behavior tracker:
- Timestamp, conversation summary
- User feedback
- Inferred preferences (pending confirmation)

---

## Cross-Agent Memory Sync (v7.2+)

When user says "记住...":
1. Write to local memory files
2. Write to Bitable relay (marked 【i7记忆同步】)
3. Y7 reads and internalizes
4. Confirm sync on next heartbeat

---

## Prohibited

- ❌ Deliver without multi-dimensional thinking
- ❌ Self-check your own work
- ❌ Single-path without comparison
- ❌ Report without verification
- ❌ Wait for user to find problems
- ❌ Deliver without behavior tracking

---

## Quick Start

```bash
clawhub install self-check
```

---

*Based on [Y7 Framework](https://github.com/Y7-ai) + Three Provinces Six Ministries — [Eita19](https://github.com/Eita19)*
