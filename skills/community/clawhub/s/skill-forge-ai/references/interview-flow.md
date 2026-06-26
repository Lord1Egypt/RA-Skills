# Interview Flow Reference

Complete methodology for the adaptive multi-round interview in skill-forge Phase 0.

**When to read**: When entering Step 0.2 (adaptive interview). Read this file in full before starting any interview round.

---

## Interview Rules (apply EVERY round)

| Rule | Description |
|------|------------|
| **B1: Behavioral probing** | Ask "tell me about the last time you did X, step by step" — not "what do you want?" Users idealize intentions but cannot fake behaviors. |
| **B2: Why × 1-2** | After each answer, ask "why?" or "then what?" 1-2 times until hitting concrete behavior or emotion word. |
| **B3: Bias detection** | Scan answers for "I should / I plan to / generally / 都行 / 随便" → redirect to "what actually happened last time?" |
| **B4: Contradiction writeback** | If answers contradict, quote both verbatim and let user choose — never decide for them. |
| **B5: Option-first** | Use AskUserQuestion with 3 strong options + Other. Users choose more accurately than they describe. Labels ≤ 12 chars, descriptions 5-15 chars. No suggestive words ("高质量"/"更好"/"推荐"). |
| **B6: Creative option probe** | If user picks unusual option → ask "do you really want this, or just find it interesting?" Distinguish reaction from commitment. |

---

## Interview Rounds

### Round 1 — Scenario Discovery (2-3 questions, option-first)

Q1: "你想让这个 Skill 帮你做什么？" → 3 strong options + Other
Q2: "什么情况下你会用到它？" → 3 typical scenarios + Other
After each: Why × 1 (B2)
🔍 **Broad search**: `"<domain> best practices <current year>"` — identify key dimensions

### Round 2 — Behavioral Deep-Dive + Search Deepen (2-3 questions)

Q3: "想想最近一次你做这件事的经过，一步步告诉我" (B1)
Q4: "做完之后，你最常改的是什么？" → 3 pain points + Other
After each: Bias check (B3), Why × 1 (B2)
🔍 **Deepen search**: `"<domain> <specific direction from R1> 标准 规范 方法"`

### Round 3 — Boundary Lock + Search Precision (2-3 questions)

Q5: "这个 Skill 绝对不能做什么？" → 3 overreach patterns + Other
Q6: "基于行业实践，[domain]通常有这些关键维度：[search]，你最看重哪几个？" → 3-4 options + Other
After each: Contradiction check (B4), Creative option probe (B6)
🔍 **Precision search**: `"<domain> <output type> template example"`

### Round 4 — Output Lock (2-3 questions)

Q7: "你期望的输出长什么样？" → 2-3 format proposals based on search results + Other
Q8: "什么情况下输出算'做好了'？什么算'没做好'？" → 3 quality criteria + Other
After each: Why × 1 (B2)

### Round 5 — Safety Net (only if elements still incomplete)

- Fill remaining gaps with targeted questions
- AI proposes completions for unclear elements based on all gathered info
- User confirms or corrects AI's proposals

---

## Convergence Check (after EACH round)

Update the 5-element checklist:

| # | Element | Clear? | Source |
|---|---------|--------|--------|
| 1 | Single scenario | Y/N | Which round/answer |
| 2 | Trigger condition | Y/N | Which round/answer |
| 3 | Output format | Y/N | Which round/answer |
| 4 | Scope boundary | Y/N | Which round/answer |
| 5 | Hard constraints | Y/N | Which round/answer |

**≥4 elements clear → can stop interviewing and proceed to Phase 1.**

Do NOT force all 5 rounds if elements converge early. Do NOT skip rounds if elements are still unclear.

**Hard limit**: 5 rounds max. At round 5, proceed with available info + AI-inferred completions.

---

## Recursive Search Pattern

Search depth increases each round:

```
R1 → Broad:    "<domain> best practices"           → discover dimensions
R2 → Deepen:   "<domain> <user's direction> 方法"    → find methods
R3 → Precision: "<domain> <output type> template"    → find standards
R4 → Verify:   only if needed, to confirm specific details
```

**Search rules**:
- Max 2 searches per round (not a research project)
- Extract ONLY actionable insights (dimensions, methods, standards, templates)
- Feed search results into next round's question design
- Don't dump raw search results into the Skill
- If domain is well-known, skip search — use AI expertise
