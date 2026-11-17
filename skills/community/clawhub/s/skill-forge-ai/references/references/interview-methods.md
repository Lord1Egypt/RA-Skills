# Interview Methods Reference

Detailed methodology for the adaptive multi-round interview in skill-creator v3.1.

---

## B1: Behavioral Probing — Actions over Intentions

**Core principle**: Users美化 their intentions but cannot fake their behaviors. Always push "what do you want" back to "what did you actually do last time."

| | Question | Why |
|---|---|---|
| BAD | "你想要 AI 做什么？" | Users idealize their needs |
| BAD | "你希望 AI 是怎样的？" | Social desirability bias |
| GOOD | "想想最近一次你做这件事的经过——一步步告诉我那次发生了什么。" | Forces concrete recall |
| GOOD | "上一次你做这个的时候，具体是怎么操作的？" | Behavioral anchor |

**When to use**: Every round when the user's answer is abstract or aspirational.

---

## B2: Why × 1-2 — Chase the Concrete

After each user answer, automatically ask "why?" or "then what?" 1-2 times until the answer lands on:
- A **concrete behavior** ("I open Notion and write 3 bullet points")
- A **specific emotion** ("I hate it when AI uses 套话")
- A **tangible artifact** ("I need a table with 4 columns")

**Stop when**: The answer is actionable enough that an intern could execute it.

**Example**:
```
User: "I want AI to write better articles"
  → Why? "Because my current AI output is too generic"
    → What specifically is generic? "It always starts with 在当今社会 and ends with 综上所述"
      → ✅ NOW you have a concrete anti-pattern for the Skill's rules
```

---

## B3: Bias Detection — Scan Every Answer

After each user answer, scan for these bias signals:

| Bias signal | Example | Redirect |
|-------------|---------|----------|
| Social desirability | "我应该每天写日报" | "上次实际发生时是怎样的？" |
| Aspirational framing | "我打算用更专业的方式" | "目前你是怎么做的？" |
| Vague generality | "一般来说我会..." | "最近一次具体是什么情况？" |
| One-word answer | "是" / "有" / "还行" | Ask them to elaborate with a specific example |
| Deflection | "都行" / "随便" / "你看着办" | Switch to option-based question (B5) |

**Rule**: Never accept a biased answer at face value. Always redirect once.

---

## B4: Contradiction Writeback — Never Decide for the User

When user's answers contradict across rounds:

1. **Quote both answers verbatim**
2. **Present the contradiction without judgment**
3. **Let the user choose**

**Example**:
```
"你在 Round 1 说自己每天写技术博客；Round 3 说最讨厌写长文。
这两个有冲突——你更倾向哪个？或者两者可以并存（比如写短技术笔记）？"
```

**Never**: Silently pick one side. Never assume which answer is "more correct."

---

## B5: Option-First Design — 3+1 Method

**Core insight**: Users choose more accurately than they describe. Give them handles to react to, not blank space to construct on.

### Design Philosophy: 3 Strong + Other

Each question offers:
- ① ② ③ **Strong options**: Cover ~80% typical scenarios, mutually exclusive, no overlap
- **Other**: Always available as open-ended fallback (AskUserQuestion adds this automatically)

### Option Design Rules

1. **①②③ must NOT overlap** and must cover typical scenarios
2. **Labels ≤ 12 chars**, descriptions 5-15 chars
3. **No suggestive words** in options: "高质量" / "更好" / "推荐" are forbidden
4. **Other is always available** — user's free text may be the most valuable answer

### AskUserQuestion Format

```json
{
  "question": "你做什么 + 给谁交付？",
  "header": "工作形态",
  "multiSelect": false,
  "options": [
    {"label": "文字内容创作", "description": "公众号/Newsletter/视频"},
    {"label": "软件产品", "description": "Indie Hacker/SaaS"},
    {"label": "知识服务", "description": "顾问/教练/培训"},
  ]
}
```

### After-Choice Follow-up

| User picks | Follow-up |
|-----------|-----------|
| ①②③ (strong options) | Why × 1 (B2): "为什么选这个？上次是这样吗？" |
| Other (free text) | Bias check (B3) — free text may be highest value but also most biased |

---

## B6: Creative Option Probe — Distinguish Reaction from Commitment

When a user picks an unusual or creative option:

**Ask**: "你是真的想要这个，还是觉得有趣？"

**Why**: Users often pick creative options because they're novel, not because they reflect real needs. Distinguishing "reaction" (interesting!) from "commitment" (I actually need this) prevents building the wrong Skill.

---

## Recursive Search Pattern

Search depth increases with each interview round:

### Round 1: Broad Discovery

**Purpose**: Identify the key dimensions of the domain.

**Search queries**:
- `"<domain> best practices <year>"`
- `"<domain> 核心维度 方法"`

**Extract**: Key dimensions, common approaches, industry standards.

**Feed into**: Round 2 question design — use discovered dimensions as option choices.

### Round 2: Directional Deepen

**Purpose**: Go deeper in the specific direction the user indicated.

**Search queries**:
- `"<domain> <user's chosen direction> 标准 规范"`
- `"<domain> <specific method> 实践 案例"`

**Extract**: Specific methods, standards, common pitfalls, professional terminology.

**Feed into**: Round 3 question design — use discovered standards as boundary options.

### Round 3: Precision Standards

**Purpose**: Find concrete output formats and quality standards.

**Search queries**:
- `"<domain> <output type> template format"`
- `"<domain> 质量标准 checklist"`

**Extract**: Concrete templates, quality criteria, professional output formats.

**Feed into**: Round 4 question design — propose specific output formats based on search.

### Round 4: Verification (only if needed)

**Purpose**: Confirm specific details that are still unclear.

**Search queries**: Targeted, specific queries based on remaining gaps.

### Search Rules

- **Max 2 searches per round** — this is enrichment, not research
- **Extract ONLY actionable insights** — dimensions, methods, standards, templates
- **Never dump raw search results** into the Skill
- **Feed results into question design**, not directly into Skill content
- **If domain is well-known** (e.g., "JSON formatting"), skip search — use AI expertise

---

## Convergence Check

After each round, update the 5-element checklist:

| # | Element | Clear? | Source |
|---|---------|--------|--------|
| 1 | Single scenario | Y/N | Which round/answer clarified it |
| 2 | Trigger condition | Y/N | Which round/answer clarified it |
| 3 | Output format | Y/N | Which round/answer clarified it |
| 4 | Scope boundary | Y/N | Which round/answer clarified it |
| 5 | Hard constraints | Y/N | Which round/answer clarified it |

**Decision**:
- ≥4 elements clear → Can proceed to Phase 1
- <4 elements clear → Continue to next round
- Round 5 reached → Force proceed with AI-inferred completions for missing elements

**Never** skip the convergence check. **Never** proceed to Phase 1 with <3 elements clear without explicit user confirmation.

---

## Game Complexity Arc

Question ordering follows a natural difficulty curve:

1. **Warm-up** (R1): Factual, low cognitive load — "what do you do?"
2. **Medium** (R2): Task recall — "tell me about the last time..."
3. **Complex** (R3-R4): Emotional/failure/ideal state — "what must NEVER happen?" / "what does 'done right' look like?"
4. **Closing** (R4-R5): Open synthesis — "anything else I should know?"

This arc puts users at ease before asking harder questions, yielding more honest and detailed answers.
