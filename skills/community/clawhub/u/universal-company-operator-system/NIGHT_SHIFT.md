# Night Shift Mode — Workflow

## Purpose

Night Shift Mode lets a user hand off a single objective at end-of-day and receive a single Morning Brief containing all safe, reversible work that could be completed asynchronously by the universal operator team. This is the asynchronous execution layer for the Universal Company Operator System.

## Activation

Night Shift Mode is activated by any of these commands:

```text
/run nightshift [objective]
/run overnight [objective]
/run morning-brief [objective]
/run founder-brief [objective]
```

All four commands route to `universal_night_shift_operator`. They are aliases.

## The Five Phases

A Night Shift run executes in exactly five phases. Each phase is non-skippable.

### Phase 1 — Classify

Read the objective and identify:

1. **Domain(s)**: which operator lanes are involved (one or many).
2. **Scope**: is this a single deliverable, a research pass, a planning pass, or a cross-functional package?
3. **Stakes**: is anything in the request inherently irreversible (publishing, sending, spending, signing, deleting)? If yes, flag immediately and route those parts to **Decisions Needed**, not execution.
4. **Missing context**: what assumptions must be made? Label them clearly — do not block on questions overnight.

### Phase 2 — Split

Break the objective into 3-8 discrete **work packets**. A packet is the smallest unit of overnight work that produces one deliverable.

Each packet must have:

```text
Packet ID:          NS-01, NS-02, ...
Objective:          One sentence describing what this packet produces
Owning Operator:    universal_*_operator
Deliverable Type:   spec | draft | plan | analysis | research | checklist | outline | recommendation | risk-flag
Inputs Assumed:     What this packet treats as given
Safety Check:       PASS | DRAFT-ONLY | BLOCKED
```

Safety check values:

- **PASS**: fully safe to execute as a deliverable.
- **DRAFT-ONLY**: the underlying action is irreversible (e.g., sending an email), so the packet produces only a draft and an approval request.
- **BLOCKED**: cannot be completed even as a draft (e.g., it requires secrets, live data the operator lacks, or a contractual signature). Move to **Decisions Needed**.

### Phase 3 — Route

Map each packet to its owning operator using `operator_manifest.json`. A packet has one owning operator. If a packet legitimately needs more than one lane, split it further or have `universal_business_operator` coordinate.

### Phase 4 — Execute

For each PASS or DRAFT-ONLY packet:

1. Invoke the owning operator's standard framework.
2. Produce the deliverable in full.
3. Never simulate an external action. Drafts are clearly marked as drafts.
4. If new blockers surface during execution, downgrade the packet to **Decisions Needed** rather than guessing.

BLOCKED packets are not executed. They appear in the Morning Brief under **Decisions Needed** with the reason and a recommended next step.

### Phase 5 — Morning Brief

Aggregate all packet outputs into one Morning Brief following the exact structure in `MORNING_BRIEF.md`. The brief is the only user-facing artifact of a Night Shift run.

## Packet Schema (Reference)

```text
NS-XX
  Objective:        ...
  Operator:         universal_*_operator
  Deliverable:      ...
  Safety:           PASS | DRAFT-ONLY | BLOCKED
  Assumptions:      ...
  Output:           [embedded in Operator Reports section]
  Decision Needed:  yes | no
  Recommendation:   ...
```

## Examples

### Example 1 — Single-Domain Objective

```text
/run overnight prepare a 30-day content plan for the next product launch
```

Classification: Growth domain. No irreversible actions. Single owning operator with light coordination.

Packets:

- NS-01 — Audience and positioning summary → `universal_growth_marketing_operator` (PASS, plan)
- NS-02 — 30-day content calendar draft → `universal_growth_marketing_operator` (PASS, draft)
- NS-03 — Channel-by-channel hook variants → `universal_growth_marketing_operator` (PASS, draft)
- NS-04 — Suggested visual direction notes → `universal_design_ux_operator` (PASS, recommendation)
- NS-05 — KPI definitions for the launch window → `universal_data_analytics_operator` (PASS, spec)

### Example 2 — Cross-Functional Objective

```text
/run nightshift prep everything I need to decide tomorrow whether to raise prices
```

Classification: Strategy + Finance + Sales + Customer Success + Data. No live changes — pricing change itself is reserved for the user.

Packets:

- NS-01 — Strategic framing and tradeoffs memo → `universal_ceo_operator` (PASS, recommendation)
- NS-02 — Pricing scenario analysis (3 options) → `universal_finance_operator` (PASS, analysis)
- NS-03 — Likely customer reactions and churn risk → `universal_customer_success_operator` (PASS, analysis)
- NS-04 — Sales talk-track draft if prices rise → `universal_sales_partnerships_operator` (DRAFT-ONLY, draft)
- NS-05 — Metrics to watch for 14 days post-change → `universal_data_analytics_operator` (PASS, spec)
- NS-06 — Customer announcement copy → `universal_growth_marketing_operator` (DRAFT-ONLY, draft)
- NS-07 — Final decision memo + recommendation → `universal_ceo_operator` (PASS, recommendation)

### Example 3 — Objective Containing an Unsafe Request

```text
/run morning-brief send the partnership email and finalize the contract
```

Classification: Sales + Legal, but **the request itself contains prohibited actions** ("send" and "finalize").

Packets:

- NS-01 — Partnership email draft → `universal_sales_partnerships_operator` (DRAFT-ONLY)
- NS-02 — Contract review notes and red flags → `universal_legal_compliance_operator` (PASS, analysis)
- NS-03 — Suggested redlines → `universal_legal_compliance_operator` (DRAFT-ONLY)
- "Send email" → **Decisions Needed**, not executed.
- "Finalize contract" → **Decisions Needed**, not executed (irreversible, requires human signature).

The Morning Brief presents the drafts, the analysis, and a clear approval list.

## Conflict Resolution

If two operators produce conflicting recommendations during a Night Shift run, `universal_ceo_operator` resolves the tradeoff in the **Executive Summary** of the Morning Brief, explaining both sides and the chosen direction.

## Hard Stop Conditions

The Night Shift Operator stops the entire run and asks the user (rather than completing the brief) only if:

1. The objective itself is incoherent or contradicts safety rules at the top level (e.g., "delete everything").
2. There is no safe interpretation of the request.

In all other cases — including partially unsafe requests — the run continues, executes the safe parts, and surfaces the unsafe parts under **Decisions Needed**.
