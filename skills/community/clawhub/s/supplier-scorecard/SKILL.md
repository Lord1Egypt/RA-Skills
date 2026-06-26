---
name: supplier-scorecard
description: Track and score supplier reliability, quality consistency, lead time accuracy, and communication to make sourcing decisions based on evidence. Use when comparing suppliers for the same product, deciding whether to switch or dual-source, negotiating with data instead of feelings, or building a quarterly supplier review process for an ecommerce business.
---

# Supplier Scorecard

Choosing the wrong supplier costs far more than the price difference on a quote — it shows up as late shipments, inconsistent quality, customer returns, and listing suspensions. This skill builds a structured scoring framework for evaluating your suppliers across reliability, quality, lead time accuracy, communication responsiveness, and cost competitiveness so you can make sourcing decisions backed by evidence instead of gut feeling or whoever quoted cheapest last month.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Scoring dimensions | 5 weighted: quality 30%, reliability 25%, lead time 20%, communication 15%, cost 10% | Equal-weighted 5 dimensions | Cost-only comparison |
| Evidence basis | Order-level logs (defect counts, promised vs. actual dates) | Last 90 days from memory, flagged as estimate | "They seem fine" |
| Review cadence | Quarterly scorecard + ad-hoc after any critical incident | Semi-annual | Only when something breaks |
| Switching threshold | Score gap ≥15 points sustained 2 quarters + transition plan | Gap ≥20 points one quarter | Switching over one bad order |
| Dual sourcing | Hero SKUs dual-sourced at 70/30 volume split | Backup supplier qualified but inactive | Single-sourced bestsellers |
| Sample evaluation | Blind side-by-side against spec sheet, 3 units per supplier | Single sample vs. spec | Photos from the sales rep |
| Negotiation use | Scorecard shared with supplier; improvement targets attached to volume commitments | Scores referenced verbally | Scores kept secret, used to ambush |

## Solves

- Supplier choices made on unit price while late shipments and defects eat the savings
- No objective basis for "should we switch?" conversations — just frustration and anecdotes
- Quality drift after the first orders (golden-sample syndrome) going unmeasured until reviews tank
- Single-source dependency on bestsellers discovered only when the supplier fails
- Negotiations with nothing to trade — no data showing where the supplier under-delivers
- Costly switches to a new supplier who turns out worse on everything except price
- Sourcing knowledge living in one person's head instead of a reviewable system

## Workflow

### Step 1: Define what each dimension means for your product

Set the five dimensions with default weights: **Quality consistency 30%** (defect rate, spec adherence, batch-to-batch variance), **Reliability 25%** (orders fulfilled complete and correct), **Lead time accuracy 20%** (promised vs. actual days — accuracy, not raw speed), **Communication 15%** (response time, proactive problem disclosure, English/your-language clarity), **Cost competitiveness 10%** (landed cost vs. market, payment terms, MOQ flexibility). Adjust weights only with a written reason (e.g., fashion seasonality → lead time 30%).

### Step 2: Build the evidence log

Per order, record: order date, promised ship date, actual ship date, units ordered/received, defects found (incoming inspection + customer-reported within 60 days), spec deviations, and communication incidents (slow replies, surprise changes, proactive warnings). Start from the last 90 days of order history, email, and chat logs — estimates are acceptable for the first scorecard if flagged.

### Step 3: Score each dimension 1–10 with anchored rubrics

Use the anchors in `references/scoring-rubrics.md` so scores mean the same thing across suppliers and quarters — e.g., lead time accuracy: 10 = within ±2 days on 95%+ of orders; 5 = within ±7 days on 80%; 1 = misses by >2 weeks or unannounced delays. Never score from impression; every score cites log entries.

### Step 4: Compute weighted totals and rank

Weighted score = Σ(dimension score × weight) × 10, giving 0–100. Band: 85+ strategic partner; 70–84 solid, monitor; 55–69 improvement plan required; <55 begin transition. Tie-breaks go to quality, never cost.

### Step 5: Act on the bands

- **85+:** consolidate volume, negotiate terms (the scorecard is your leverage), consider exclusivity or priority-production agreements.
- **70–84:** share the scorecard with the supplier; attach one improvement target to the next PO.
- **55–69:** formal improvement plan with 1-quarter deadline; qualify a backup now.
- **<55:** transition plan — qualify replacement, overlap orders, never cut over in one PO.

### Step 6: Stress-test before any switch

Before switching for a higher-scoring or cheaper supplier: order blind samples (3 units, evaluated side-by-side against the spec sheet), run one small paid pilot order through full inspection, and model the switching cost (tooling, MOQ, re-inspection, listing risk from quality change). A 15-point score gap sustained two quarters justifies a switch; one bad month does not.

### Step 7: Institutionalize the cadence

Quarterly re-score from the log (30 minutes per supplier once the log exists), ad-hoc re-score after any critical incident (failed inspection, missed launch date), and an annual deep review including factory audit or video walkthrough for top-volume suppliers. Verify each scorecard with `assets/scorecard-quality-checklist.md`.

## Example 1: Two suppliers, same gadget

**Inputs:** Supplier A (current): $4.20/unit, 18 orders logged. Supplier B (candidate): $3.65/unit, 4 pilot orders.

**Output (excerpt):**

> | Dimension (weight) | A | B | Evidence |
> |---|---|---|---|
> | Quality 30% | 8 | 5 | A: 1.1% defect rate, stable across batches. B: 3.8% on pilots, one batch with off-spec USB ports |
> | Reliability 25% | 9 | 7 | A: 18/18 complete. B: 3/4 complete, one 8% short-ship "resolved" with credit |
> | Lead time 20% | 6 | 8 | A: avg +5 days vs. promise (holiday slippage). B: ±2 days all pilots |
> | Communication 15% | 9 | 6 | A: <4h responses, proactively flagged a material change. B: 1–2 days, vague on defect root cause |
> | Cost 10% | 6 | 9 | B is 13% cheaper landed |
> | **Weighted total** | **78.5** | **65.3** | |
>
> **Recommendation:** Stay with A; the $0.55 saving costs ~2.7 points of defect rate — at your 4.2% return-rate sensitivity that's negative ROI. Action: share lead-time scores with A and attach a ±3-day target to Q3 POs; keep B warm as a 20% dual-source for the holiday capacity crunch.

## Example 2: Quarterly review catches quality drift

**Inputs:** Supplier C, kitchenware, scored 86 in Q1. Q2 log shows defects 0.9% → 2.6%, two unannounced material substitutions, response time stable.

**Output (excerpt):**

> **Q2 score: 73 (−13).** Quality 9→6 (defect trend + golden-sample deviation on handle material), communication 8→6 (substitutions disclosed only after inspection caught them). Band drops to "solid, monitor" with a flag: two unannounced substitutions is a leading indicator of margin-squeeze behavior. Action: (1) written spec re-confirmation with material certificates per batch, (2) incoming inspection raised from 10% to 25% sampling for 2 orders, (3) improvement target in next PO: zero unapproved substitutions, defects <1.5%, (4) re-score in 6 weeks instead of next quarter. Do NOT consolidate the new SKU launch with C until back above 80.

## Common Mistakes

1. **Cost-led comparison.** Unit price is 10% of the weighted score for a reason: a 10% discount that brings a 3% defect rate is a loss after returns, reviews, and re-shipping.
2. **Scoring from memory.** Impressions over-weight the latest incident and the friendliest sales rep. The log is the scorecard; no log, no score.
3. **Golden-sample syndrome.** First-order quality is marketing; batch 5 is the truth. Track batch-to-batch variance explicitly, and re-confirm specs in writing each order.
4. **Punishing speed instead of rewarding accuracy.** A supplier who promises 30 days and delivers in 30 beats one who promises 15 and delivers in 25. Score accuracy against promise.
5. **Switching on one bad order.** Every supplier has a bad month; switching costs (tooling, MOQ, pilot inspection, listing risk) usually exceed one incident's cost. Require a sustained gap.
6. **Keeping scores secret.** The scorecard's negotiation power comes from sharing it: suppliers improve measurably when they know the rubric and what volume rides on it.
7. **Single-sourcing bestsellers.** Dual-source hero SKUs at ~70/30 even when the primary scores 90 — the 30% line is insurance priced at slightly worse unit economics.
8. **Ignoring communication as a leading indicator.** Slowing responses and post-hoc disclosures precede quality and delivery failures by about a quarter. Weight it, log it, act on its trend.
9. **One-time exercise.** A scorecard built once and never re-scored is sourcing theater. The quarterly cadence is the product; the first scorecard is just setup.

## Resources

- `references/output-template.md` — scorecard table, banding, and recommendation format
- `references/scoring-rubrics.md` — 1–10 anchored rubrics for all five dimensions
- `references/sourcing-playbook.md` — evidence logging, sample testing, dual-sourcing, and switching protocols
- `assets/scorecard-quality-checklist.md` — scorecard completeness checklist (40+ items)
