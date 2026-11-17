# team-loop — Autonomous Swarm with Self-Verifying TDD Loops

> *Each cycle triggers meta-validation: a skeptic scores alignment; low score halts. Snapshots capture intent, delta, confidence for breakpoint resume. Token budgets gate phases; coverage blocks hollow progress. Human only on value failure.*

---

## RSF Main Loop (11 steps, 14 flows)

```mermaid
sequenceDiagram
    participant main
    participant coder
    participant reviewer
    participant tester
    participant auditor
    participant publicist

    Note over main: seq1 GoalAgent(LLM) Parse → StandardGoal
    Note over main: seq2 Planner(LLM) Read RDF → 3-tier KR → TaskDAG + TokenEst + ADR

    main->>main: seq3 /status + budget guard → TaskUnit + Snap(t0)
    main->>coder: seq4/5 f4 async 300s: TaskUnit
    activate coder
    coder-->>main: f5 TaskResult + commit
    deactivate coder

    main->>reviewer: seq6 f6 async 120s: TaskResult
    main->>tester: seq6 f7 async 120s: TaskResult
    activate reviewer
    activate tester
    reviewer-->>main: seq7 f8 Verdict
    deactivate reviewer
    tester-->>main: seq7 f9 Verdict + CoverageReport
    deactivate tester

    main->>auditor: seq8 f10 async 120s: TaskResult + Verdictx2 + CovRpt
    activate auditor
    auditor-->>main: seq9 f11 Verdict (13-item checklist)
    deactivate auditor

    Note over main: seq10 2/3 vote → Decision + TokenReport + Snap(t1) + RoundSummary

    main->>publicist: seq10 f12 TaskResult + Decision
    activate publicist
    publicist-->>main: seq11 f13 MemoryEntry (feedback → seq2)
    deactivate publicist

    Note over main: fR: retry|next_kr → seq3 (max 3 retries)
```

---

## Architecture

- **11-step RSF** with formal `X ∈ A.out ∩ B.in` validation — all 14 flows programmatically verified closed
- **3-tier KR**: Foundation (K1) → Coverage (K2) → Quality (K3)
- **3-perspective verification**: reviewer + tester + auditor → 2/3 voting
- **9 interaction ID carriers** — end-to-end traceability

## Principles

1. Human defines goal, never enters loop
2. Different agents / different models / different verification methods
3. State on disk, fresh context every round
4. Infrastructure first — logging, IDs, exception capture before business code

## Features

| Feature | Mechanism |
|---------|-----------|
| Token budget guard | 80% downgrade → 90% no retry → 95% pause → 100% halt |
| Coverage gates | L1 syntax → L2 func (>80% line, >70% branch) → L3 semantic |
| Health scoring | `100 - ERROR×5 - WARNING×2 - risk_flags×3 - stagnation - excess retry` |
| Exception capture | L1 tool / L2 session / L3 loop + watchdog + crash log |
| Breakpoint resume | StateSnapshot(t0/t1): intent, delta, confidence per round |
| Test death penalty | Delete wrong tests; never patch them |

---

## Configuration

This skill is configured with safety-first settings to prevent accidental invocation:

| Parameter | Value | Effect |
|-----------|-------|--------|
| `disable-model-invocation` | `true` | Model will **never** auto-invoke this skill. Requires explicit user command (`team-loop`, `loop`, `迭代研发`, `迭代`). |
| `user-invocable` | `true` | User can explicitly invoke this skill via trigger keywords. |

These settings ensure a human always consciously initiates the autonomous loop — the model cannot accidentally start code-modifying cycles without your awareness.

---

## Quick Start

```bash
/goal handler layer branch coverage 0%→≥50%, budget≤¥20
/team-loop src/handlers/ complete tests, coverage≥80%
```

---

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Full English specification |
| `skill-cn.md` | Full Chinese specification |
| `README.md` | This file |

---

# team-loop — 自主任务循环引擎

> *每轮触发元验证：审查者评分对齐；低分暂停。快照捕获意图、增量、置信度支持断点续传。Token 预算门控各阶段；覆盖率阻止空洞进展。人仅在价值失败时介入。*

---

## RSF 主循环 (11步 14流)

```mermaid
sequenceDiagram
    participant main
    participant coder
    participant reviewer
    participant tester
    participant auditor
    participant publicist

    Note over main: seq1 GoalAgent(LLM) 解析 → StandardGoal
    Note over main: seq2 Planner(LLM) 读RDF → 三层KR → TaskDAG + TokenEst + ADR

    main->>main: seq3 /status + 预算守卫 → TaskUnit + Snap(t0)
    main->>coder: seq4/5 f4 async 300s: TaskUnit
    activate coder
    coder-->>main: f5 TaskResult + commit
    deactivate coder

    main->>reviewer: seq6 f6 async 120s: TaskResult
    main->>tester: seq6 f7 async 120s: TaskResult
    activate reviewer
    activate tester
    reviewer-->>main: seq7 f8 Verdict
    deactivate reviewer
    tester-->>main: seq7 f9 Verdict + CoverageReport
    deactivate tester

    main->>auditor: seq8 f10 async 120s: TaskResult + Verdictx2 + CovRpt
    activate auditor
    auditor-->>main: seq9 f11 Verdict (13项checklist)
    deactivate auditor

    Note over main: seq10 2/3裁决 → Decision + TokenReport + Snap(t1) + RoundSummary

    main->>publicist: seq10 f12 TaskResult + Decision
    activate publicist
    publicist-->>main: seq11 f13 MemoryEntry (反馈 → seq2)
    deactivate publicist

    Note over main: fR: retry|next_kr → seq3 (最多重试3次)
```

---

## 核心原则

1. 人只定义目标，不进循环
2. 不同 agent / 不同模型 / 不同验证手段
3. 状态在磁盘，每轮 fresh context
4. 基础设施先行 — 日志、编号、异常捕捉在业务代码之前

## 功能

| 功能 | 机制 |
|------|------|
| Token 预算守卫 | 80% 降级 → 90% 不重试 → 95% 暂停 → 100% 终止 |
| 覆盖率门禁 | L1 语法 → L2 功能(>80%行, >70%分支) → L3 语义 |
| 健康度评分 | `100 - ERROR×5 - WARNING×2 - risk_flags×3 - 停滞 - 过度重试` |
| 异常捕捉 | L1 工具 / L2 Session / L3 循环 + 看门狗 + 兜底日志 |
| 断点续传 | StateSnapshot(t0/t1)：意图、增量、置信度 |
| 测试死刑 | 错误测试 → 删+重写，禁止修补 |

---

## 快速开始

```bash
/goal handler层分支覆盖率 0%→≥50%，预算≤¥20
/team-loop src/handlers/ 补全测试，覆盖率≥80%
```

---

## License

MIT
