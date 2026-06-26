# Seven-Axis Review Checklist

Synthesizes Completed Staff Work (1942 US Army), BLUF, Staff Study, Policy Memo, and Devil's Advocate / Red Team patterns.

Every finding the review agent emits must be tagged with an axis, a severity, and a **concrete** suggestion. Vague feedback ("needs to be more complete") is banned.

---

## Axis 1: Ask Clarity (BLUF)

**Pass criterion**: Within the first 3 lines (or the first paragraph if no line break), the reader can answer:
- Who needs to do what?
- By when?
- At what cost / with what resource?

**Fail signals**:
- Draft opens with history / background
- "Just wanted to share an update" with no ask
- Ambiguous verbs: "consider", "think about", "maybe"

**Default severity**: BLOCKER

**Template suggestion**: "Rewrite opening to: '<BossTitle>, please <verb> <specific thing> by <date> so that <outcome>.'"

---

## Axis 2: Completeness

**Pass criterion**:
- At least 2 alternatives / options evaluated (A vs B vs status quo minimum)
- A clear recommendation picked
- Reasoning for the choice (not just a vote)

**Fail signals**:
- Single-option briefing (looks like a done deal)
- "Options" listed without comparison
- Recommendation stated but no rationale

**Default severity**: BLOCKER

**Template suggestion**: "Add an Option B with estimated cost/time/risk alongside current A. Explicitly state why A wins (e.g., faster to market, lower burn, aligns with H2 goals)."

---

## Axis 3: Evidence Freshness

**Pass criterion**:
- Every numeric claim has a source + date
- Internal data (metrics, financials) AND external anchor (market, benchmark, competitor) both present where relevant
- No data older than the decision horizon (e.g., 6mo for quarterly decisions)

**Fail signals**:
- "Our users love it" (anecdote, no data)
- Data without date stamp
- Only internal or only external (half-blind)

**Default severity**: IMPROVEMENT (BLOCKER if the whole decision hinges on one stale number)

**Template suggestion**: "The '$1.2M TAM' figure is from the 2024 deck — pull latest from [source] and update. Also add competitor pricing for comparison."

---

## Axis 4: Explicit Assumptions

**Pass criterion**:
- 3–5 assumptions listed explicitly
- Each labeled with "if this is wrong, then [consequence]"
- Assumptions are falsifiable (not platitudes)

**Fail signals**:
- No assumptions section
- Assumptions are disguised conclusions ("we assume customers will love it")
- No "if wrong" analysis

**Default severity**: BLOCKER

**Template suggestion**: "Add Assumptions section: (1) CAC stays < $50 through H2 — if rises, ROI window shrinks by X months; (2) Vendor Y ships SDK by April — if delayed, must swap to Z or defer launch."

---

## Axis 5: Red Team / Counterarguments

**Pass criterion**:
- Strongest opposing view stated (stronger than a strawman)
- Rebuttal or acknowledgement of the counterpoint
- Fallback position if recommendation fails

**Fail signals**:
- No risk section, or risks are generic ("market may change")
- Red team treated as a checkbox
- No fallback / "what if A doesn't work"

**Default severity**: BLOCKER

**Template suggestion**: "Add a 'Strongest case against' paragraph. If a smart skeptic were in the room, they'd argue [X]. The rebuttal is [Y]. If A fails within 60 days, fallback to [B] at [cost]."

---

## Axis 6: Stakeholder Reality

**Pass criterion**:
- Positions of affected parties reflect actual conversations / data, not imagination
- Internal (team, ops) + external (customer, investor, regulator) both considered where relevant
- Dissent within stakeholders is surfaced, not smoothed over

**Fail signals**:
- "Team is excited" without any team voice
- "Customers want X" without customer evidence
- Only one stakeholder group considered

**Default severity**: IMPROVEMENT

**Template suggestion**: "Add 2 quotes from team stand-up and 1 customer interview quote. Name specifically if investors X or Y have signaled concerns."

---

## Axis 7: Decision Readiness (CSW gate)

**Pass criterion**: The boss, after reading, can say **yes / no / pick A or B** — nothing else remains for the boss to do that should have been done by the briefer.

**Fail signals**:
- Draft ends with "let me know what you think"
- Boss is asked to "weigh in" without a structured choice
- Calculations / lookups left for boss
- "We'll figure out X after" — X is something the briefer should have figured out

**Default severity**: BLOCKER (this is the gate)

**Template suggestion**: "End with a decision block: [ ] Approve Option A ($X, by date); [ ] Approve Option B ($Y, by date); [ ] Defer, reason. Fill in the blanks so boss only ticks a box."

---

## Hybrid conversation rules

When emitting findings into IM conversation (not the JSONL batch), apply:

| Axis + severity | Delivery style |
|---|---|
| Axis 1/2/4/7 BLOCKER | Direct ("前 3 行没说要什么。建议改成 X。") |
| Axis 3/5/6 IMPROVEMENT | Socratic ("如果竞品下周先发，你现在的 A 还成立吗？") |
| Any NICE-TO-HAVE | Only send if < 3 per round; else defer to annotations.jsonl |

Never:
- Emit > 5 NICE-TO-HAVE in a single round (noise)
- Ask the briefer to do work that the review agent should surface
- Recommend the boss "also look into X" — that violates CSW
- Keep the briefer talking past a BLOCKER without resolving it
