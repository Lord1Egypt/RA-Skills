# Morning Brief — Output Contract

The Morning Brief is the single, exclusive output of a Night Shift run. Every Night Shift run must end with a Morning Brief that follows the structure below **exactly**, in this order, with these headings. No additional top-level sections. No omitted sections — if a section has nothing to report, write "None." under it.

## Required Structure

```markdown
# Morning Brief

## Executive Summary

## Work Completed

## Operator Reports

## Decisions Needed

## Risks Found

## Recommended Next Moves

## Drafts Prepared

## Tasks for Today

## Blockers
```

## Section Definitions

### Executive Summary

3-7 sentences. Plain language. What was attempted overnight, what landed, what didn't, and the single most important thing the user should focus on first.

### Work Completed

A flat list of every packet that produced a deliverable. Format:

- `NS-XX` — [Owning Operator] — [One-line description] — [Deliverable type]

Group order: PASS packets first, then DRAFT-ONLY packets. BLOCKED packets do not appear here.

### Operator Reports

One subsection per operator that participated. Each subsection contains the operator's actual deliverables, embedded in full. Format:

```markdown
### [operator_name]

**Packets:** NS-XX, NS-YY

**Deliverables:**

[Full content of each deliverable, clearly labeled]
```

Drafts must be clearly labeled `DRAFT — NOT SENT` or `DRAFT — NOT PUBLISHED` as appropriate.

### Decisions Needed

Every item that requires the user's explicit approval before any external action. Format:

- **[Decision title]** — Why it needs the user — Recommended choice — Risk of waiting

Includes:

- Every DRAFT-ONLY packet that would become a real action only after approval
- Every BLOCKED packet
- Every conflict the Night Shift Operator surfaced but did not resolve

### Risks Found

Risks surfaced during the night's work, regardless of source operator. Format:

- **[Risk]** — Severity (low / medium / high) — Likelihood — Suggested mitigation

Include legal, financial, operational, reputational, and execution risks. If none, write "None."

### Recommended Next Moves

The top 3-7 actions the user should take first thing today, ranked. Format:

1. **[Action]** — Owner — Why it's ranked here — Estimated effort

Recommendations must be derived from the night's work, not generic advice.

### Drafts Prepared

A pointer index to every draft produced during the night, with status. Format:

- **[Draft name]** — [Type: email / spec / post / memo / contract-redlines / SOP / etc.] — Status: `DRAFT — NOT SENT` — Located in: [Operator Reports → operator_name]

This section is a checklist, not the drafts themselves. The full content lives in Operator Reports.

### Tasks for Today

A clean, actionable task list the user (or their team) can pick up immediately. Format:

- [ ] [Task] — Owner suggestion — Estimated effort — Depends on: [Decision Needed item if any]

Tasks must be concrete and execution-ready, not generic.

### Blockers

Anything that stopped overnight work from progressing. Format:

- **[Blocker]** — What it blocks — What's needed to unblock — Who can unblock

If nothing was blocked, write "None."

## Formatting Rules

1. Use the exact section headings shown above, in the exact order.
2. Never add top-level sections beyond the nine specified.
3. Every section must appear, even if its content is "None."
4. Drafts inside Operator Reports must be presented in full so the user can copy, edit, and send them — but always clearly labeled as drafts.
5. Never include sensitive material (secrets, keys, credentials, PII) in the brief.
6. Keep the tone direct, structured, and decision-ready. No filler, no motivational copy.

## Example Skeleton

```markdown
# Morning Brief

## Executive Summary

Ran a 7-packet overnight pass on the pricing decision. Strategic memo and three pricing scenarios are ready. Two drafts (sales talk-track and customer announcement) are prepared but require approval before sending. One blocker: current churn data was unavailable, so the churn-risk estimate is bracketed.

## Work Completed

- NS-01 — universal_ceo_operator — Strategic framing memo — recommendation
- NS-02 — universal_finance_operator — 3-scenario pricing model — analysis
- NS-03 — universal_customer_success_operator — Churn-risk estimate — analysis
- NS-05 — universal_data_analytics_operator — 14-day metric watch spec — spec
- NS-07 — universal_ceo_operator — Final decision memo — recommendation
- NS-04 — universal_sales_partnerships_operator — Sales talk-track — draft
- NS-06 — universal_growth_marketing_operator — Announcement copy — draft

## Operator Reports

### universal_ceo_operator
...

### universal_finance_operator
...

[etc.]

## Decisions Needed

- **Approve price change direction** — three scenarios modeled, recommendation is Option B — recommend approve before sending announcement — risk of waiting: pricing window may close.
- **Approve announcement copy** — draft is in Operator Reports → universal_growth_marketing_operator — recommend approve with edits.

## Risks Found

- **Churn spike risk** — medium severity — medium likelihood — mitigation: 14-day metric watch + retention offer ready.

## Recommended Next Moves

1. Read CEO decision memo and approve a scenario — owner: user — 15 minutes — unlocks everything else.
2. Review and edit announcement draft — owner: user — 20 minutes — depends on #1.
3. ...

## Drafts Prepared

- **Sales talk-track** — internal script — DRAFT — NOT SENT — Located in: Operator Reports → universal_sales_partnerships_operator
- **Customer announcement** — public copy — DRAFT — NOT PUBLISHED — Located in: Operator Reports → universal_growth_marketing_operator

## Tasks for Today

- [ ] Decide on pricing scenario — owner: user — 15 min — depends on: Approve price change direction.
- [ ] ...

## Blockers

- **Current churn data unavailable** — blocks precise churn-risk estimate — needs export from analytics tool — can be unblocked by user.
```
