# Interview Flow Reference (v5.0)

Complete methodology for the adaptive multi-round interview in skill-forge Phase 0.

**When to read**: When entering Phase 0.2 (adaptive interview). Read this file in full before starting any interview round.

---

## Core Principle: One Question at a Time (一次一问)

**Every round, ask only ONE question.** Give 2-3 options to pick from, not a blank space to fill.

Why: 一次甩你三个问题，你只会挑最好答的那个，剩下随手糊弄过去。

```
❌ BAD: "你想要什么输出格式？什么时候触发？输入是什么？"
✅ GOOD: "你最后要的是一个能下载的文件，还是直接贴在对话里的内容？"
```

After each answer → Why × 1 (B2) → next question.

---

## Level Adaptation (水平自适应)

**Never ask "你几级水平"**. Detect from user's language:

| User says | Level | Adaptation |
|-----------|-------|------------|
| ".xlsx", "pandas", "JSON", "API", "assertion" | 老手 | 用术语，不啰嗦，跳过基础解释 |
| "那种东西", "差不多就行", "就是帮我整理一下" | 小白 | 换大白话，零术语，给更多选项 |
| Mixed signals | 中间 | 用通俗语言+关键术语标注 |

**Rule**: Adapt in real-time. If user suddenly uses technical terms, upgrade. If user seems confused, downgrade.

---

## Confirmation Gate (确认门)

**理解没对齐，绝不动手写。**

After four elements are gathered, present a one-page summary:

```
我理解是这样——
· 做什么：[一句话描述]
· 何时触发：[用户会说的话]
· 输入：[输入格式]；输出：[输出格式]
· 边界：[不做什么]

这样对吗？没问题我就开始写了。
```

**User confirms → proceed to Phase 1.**
**User corrects → fix and re-present.**

---

## Interview Rules (apply EVERY round)

| Rule | Description |
|------|------------|
| **B1: Behavioral probing** | Ask "tell me about the last time you did X, step by step" — not "what do you want?" |
| **B2: Why × 1-2** | After each answer, ask "why?" or "then what?" 1-2 times until hitting concrete behavior |
| **B3: Bias detection** | Scan for "I should / I plan to / 都行 / 随便" → redirect to "what actually happened?" |
| **B4: Contradiction writeback** | If answers contradict, quote both and let user choose |
| **B5: Option-first** | 3 strong options + Other. Labels ≤ 12 chars. No suggestive words. |
| **B6: Creative option probe** | If user picks unusual option → "do you really want this, or just find it interesting?" |

---

## Interview Rounds (一次一问版)

### Round 1 — Scenario Discovery (1 question)

Q: "你想让这个 Skill 帮你做什么？" → 3 strong options + Other
After: Why × 1 (B2)
🔍 Broad search: `"<domain> best practices <current year>"`

### Round 2 — Behavioral Deep-Dive (1 question)

Q: "想想最近一次你做这件事的经过，一步步告诉我" (B1)
After: Bias check (B3), Why × 1 (B2)
🔍 Deepen search: `"<domain> <specific direction> 标准 规范 方法"`

### Round 3 — Output Lock (1 question)

Q: "你最后要的产出长什么样？" → 2-3 format proposals + Other
After: Why × 1 (B2)
🔍 Precision search: `"<domain> <output type> template example"`

### Round 4 — Boundary Lock (1 question)

Q: "有哪些情况它千万别插手？" → 3 overreach patterns + Other
After: Contradiction check (B4), Creative option probe (B6)

### Round 5 — Safety Net (only if elements still incomplete)

- Fill remaining gaps with targeted questions
- AI proposes completions for unclear elements
- User confirms or corrects

---

## Convergence Check (after EACH round)

Update the 4-element checklist:

| # | Element | Clear? | Source |
|---|---------|--------|--------|
| 1 | 做什么 (What to do) | Y/N | Which round/answer |
| 2 | 何时触发 (When to trigger) | Y/N | Which round/answer |
| 3 | 输入输出 (Input/Output) | Y/N | Which round/answer |
| 4 | 边界 (Boundaries) | Y/N | Which round/answer |

**≥3 elements clear → present 确认门 summary.**
**<3 elements clear → continue to next round.**
**Round 5 reached → force proceed with AI-inferred completions.**

---

## Recursive Search Pattern

```
R1 → Broad:    "<domain> best practices"           → discover dimensions
R2 → Deepen:   "<domain> <user's direction> 方法"    → find methods
R3 → Precision: "<domain> <output type> template"    → find standards
R4 → Verify:   only if needed
```

**Rules**: Max 2 searches per round. Extract ONLY actionable insights. Feed into next question. Don't dump raw results. If domain is well-known, skip search.
