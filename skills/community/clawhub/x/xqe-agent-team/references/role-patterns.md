# Role Patterns — Agent Team

Ready-made role combinations for common scenarios.

---

## 代码分析 / Code Review

**Trigger:** "review this codebase", "analyze and refactor", "找出代码问题"

| Worker | Task |
|--------|------|
| `reader` | Read all relevant files, produce a structured summary of architecture, dependencies, and key logic |
| `security-reviewer` | Audit for security issues: injection, auth, data exposure, dependency CVEs |
| `refactor-planner` | Given reader's summary, propose concrete refactor actions with priority ranking |

**Flow:** `reader` finishes → sends summary to `security-reviewer` and `refactor-planner` → both finish → orchestrator synthesizes

---

## 市场调研 / Market Research

**Trigger:** "research this market", "调研竞品", "analyze competitors"

| Worker | Task |
|--------|------|
| `data-analyst` | Gather quantitative data: market size, growth rates, key metrics |
| `sentiment-analyst` | Analyze sentiment from news, social, forums around the topic |
| `risk-assessor` | Identify risks, regulatory issues, macro headwinds |

**Flow:** All three spawn in parallel → each reports to orchestrator → orchestrator synthesizes into briefing

---

## 交易信号分析 / Trading Signal Analysis

**Trigger:** "analyze $NVDA signal", "交易信号多角度分析", "should I enter this trade"

| Worker | Task |
|--------|------|
| `technical-analyst` | Analyze price action: RSI, MACD, support/resistance, trend |
| `fundamental-analyst` | Review recent earnings, analyst ratings, guidance changes |
| `macro-watcher` | Check macro context: Fed stance, sector rotation, risk-on/off |

**Flow:** All three spawn in parallel → reports back → orchestrator gives BUY/HOLD/SKIP with confidence + reasoning

**Extra:** Add a `risk-manager` worker when position sizing or stop-loss calculation is needed.

---

## 文档/报告生成 / Document Generation

**Trigger:** "write a report on X", "生成分析报告"

| Worker | Task |
|--------|------|
| `researcher` | Gather all relevant facts, data, and context |
| `writer` | Draft the document structure and prose based on researcher's output |
| `editor` | Review draft for clarity, accuracy, consistency |

**Flow:** `researcher` → sends to `writer` → `writer` draft → sends to `editor` → editor feedback → final to orchestrator

---

## 调试 / Debugging

**Trigger:** "debug this error", "find the bug", "为什么报错"

| Worker | Task |
|--------|------|
| `log-reader` | Parse error logs, stack traces, reproduce the error path |
| `code-inspector` | Read relevant source files around the error, identify root cause candidates |
| `fix-writer` | Given root cause from code-inspector, write the fix and explain it |

**Flow:** `log-reader` → sends findings to `code-inspector` → `code-inspector` → sends to `fix-writer` → fix to orchestrator

---

## 自定义团队 / Custom Team

When no pattern fits, orchestrator should:
1. Decompose the task into N independent subtasks (N = 2–4)
2. Assign one worker per subtask
3. Identify any cross-worker dependencies and sequence those pairs
4. Spawn independent workers in parallel, dependent ones sequentially
