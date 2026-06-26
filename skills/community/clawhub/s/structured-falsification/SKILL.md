---
name: structured-falsification
description: >
  Structured falsification framework for complex decision-making, investment analysis,
  technology selection, and multi-factor judgment. Use when: (1) evaluating multiple
  options with uncertain outcomes, (2) analyzing investment targets / business strategies,
  (3) making technology or architecture decisions, (4) performing due diligence or risk
  assessment, (5) user says "灵智模式", "深度思考", "deep thinking", "falsify", or
  "structured analysis". Can be auto-triggered by agents when facing high-uncertainty
  multi-factor decisions — no explicit keyword required.
---

# Structured Falsification (结构化证伪法)

A five-step reasoning framework that forces rigorous disconfirmation before arriving at conclusions.
Designed for AI agents and LLMs to produce concise, high-confidence outputs on complex tasks.

**Core principle: Show conclusions, not derivation.** The agent runs the full five-step process internally
but outputs only the final ranked conclusions with confidence levels and key risks. Verbose reasoning
is a sign the framework wasn't applied rigorously enough — tighten the analysis, don't expand the output.

## When to Auto-Trigger

- Multiple competing options with no clear winner
- User asks "should I…", "which one…", "what about…", "evaluate…", "compare…"
- Investment target analysis, due diligence, competitive assessment
- Technology selection, architecture decision, vendor evaluation
- Any task where the cost of a wrong answer is high

## The Five Steps (internal process)

### Step 1: Decompose Value Nodes

Map the problem space. Identify where real value / risk / leverage sits.
- What does this problem *actually* need? (Not surface requirements — underlying drivers)
- Map key entities and their relationships (supply chain / dependency graph / stakeholder map)
- Classify each node: critical vs. nice-to-have vs. irrelevant

### Step 2: Falsify Each Candidate (core step)

For every option / target / claim, run:
1. **Surface logic**: Why does the market / conventional wisdom support this?
2. **Challenge**: Where is the logic fragile? Causal chain breaks? Concept substitution? Hidden assumptions?
3. **Verdict**: Rate association strength — direct / indirect / tangential

**Output: a falsification table** (internal) with columns: Candidate | Surface Logic | Challenge | Verdict

### Step 3: Identify True Beneficiaries / Best Options

Apply priority filters:
1. **Infrastructure / tooling** (selling shovels during a gold rush) → highest certainty
2. **Core technology owners** (commercializable IP) → highest upside
3. **Application layer** (using tech to cut costs / add features) → value capture may be limited

### Step 4: Stress Test Survivors

For each surviving candidate:
- Is the causal chain A→B→C fully intact at every link?
- Is there actual evidence? (Business data, orders, customers, benchmarks)
- If this logic fails, how bad is the downside?
- Any show-stopper that eliminates this candidate entirely?

### Step 5: Rank and Conclude

- Sort by certainty (High / Medium / Low)
- Attach to each: one-line logic, key assumption, core risk
- Explicitly flag "not recommended" items with reasons
- One-sentence bottom line

## Self-Correction Checklist

Before producing output, verify:

- [ ] Did I falsify hard enough? If every candidate survived, the filter is too loose.
- [ ] Did I confuse "good company" with "good thesis"? Logic > quality.
- [ ] Am I hedging excessively? Pick a direction. Uncertainty should be flagged, not hidden behind "it depends".
- [ ] Did I anchor on the first plausible answer? Force a search for disconfirming evidence.
- [ ] Is my output concise? If the conclusion section exceeds 50% of the total output, re-tighten.

## Output Format

**Only output the following. No step-by-step narration. No "let me think about this".**

```
## 结论

| # | 候选 | 判断 | 确定性 | 核心逻辑（一句话） | 关键假设 | 主要风险 |
|---|------|------|--------|---------------------|----------|----------|
| 1 | ...  | ✅/⚠️/❌ | 高/中/低 | ... | ... | ... |
| 2 | ...  | ...  | ...    | ...                 | ...      | ...      |

**一句话总结：** ...
```

## Domain Configurations

Load domain-specific checklists when the context matches:

- **Investment analysis** → Read `references/investment.md`
- **Technology selection** → Read `references/tech-decision.md`
- **Other domains** → Use the generic framework above, or read a custom config from `references/`

To create a custom domain config, copy `references/domain-template.md` and fill in the sections.
