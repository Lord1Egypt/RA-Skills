---
name: vke-decision-workflow
description: Build VKE evidence-led decision workflows and business knowledge products from a request. Use when OpenClaw or Codex needs to create or update VKE case artifacts such as problem briefs, research plans, evidence ledgers, analysis notes, red-team reviews, commercial decision reports, watchlists, and retrospectives.
---

# VKE Decision Workflow

## Overview

Use this skill to turn an ambiguous knowledge request into a traceable decision package. The workflow is evidence-led: separate facts, judgments, and assumptions; bind every core judgment to evidence IDs and confidence; use red-team review before producing the final business report.

The standard artifact sequence is:

1. `00_request.md` - original request
2. `01_problem-brief.md` - decision framing
3. `02_research-plan.md` - resource and evidence plan
4. `03_evidence-ledger.csv` - evidence table
5. `04_analysis-notes.md` - reasoning notes
6. `05_red-team-review.md` - adversarial review
7. `06_knowledge-product.md` - decision product or commercial report
8. `07_watchlist.md` - monitoring indicators
9. `08_retrospective.md` - process review

Read `references/artifact-templates.md` when creating or rewriting any artifact.

## Operating Rules

- Do not change source case files unless the user asks to update them.
- Preserve user-provided evidence boundaries. If the user says not to add external facts, only use the supplied ledger, notes, and files.
- Treat evidence relevance and reliability separately. A reliable source with low relevance cannot support a strong conclusion.
- Keep the decision question visible. Every artifact should serve the user's decision, not become general research.
- Distinguish facts, judgments, and assumptions:
  - Fact: what a source or evidence record says.
  - Judgment: what those facts imply for the decision.
  - Assumption: a necessary but not yet proven condition.
- Attach confidence to each core judgment, not only to the whole report.
- Prefer conservative wording when evidence is indirect, adjacent, or low relevance.
- Red-team before finalizing the knowledge product.

## Workflow

### 1. Frame the Problem

Create or update `01_problem-brief.md`.

Capture:

- core decision question
- decision use
- known facts
- key uncertainties
- scope boundaries
- success criteria
- deadline or time horizon

Convert vague interest into a decision form such as: "Should we invest, enter, pause, continue observing, or run a limited validation?"

### 2. Plan Research and Resources

Create or update `02_research-plan.md`.

Specify:

- hypotheses to verify
- evidence types and priority
- expert/resource needs
- institution or center-of-excellence types
- databases and public sources
- tools and search paths
- validation priorities
- likely source bias

Use resource planning to avoid over-collecting background information.

### 3. Build the Evidence Ledger

Create or update `03_evidence-ledger.csv`.

Use stable evidence IDs such as `EVD-001`. Required fields:

```csv
evidence_id,case_id,claim_supported,evidence_summary,source_id,source_name,source_date,collection_date,evidence_type,reliability,relevance,confidence_effect,notes
```

For each row, state what the evidence can support and what it cannot support. Mark reliability and relevance independently as `高`, `中`, or `低`.

### 4. Write Analysis Notes

Create or update `04_analysis-notes.md`.

Structure each major claim as:

- judgment
- evidence used
- reasoning chain
- alternative explanation
- confidence
- remaining verification

Use the pattern:

```text
Evidence -> intermediate inference -> alternative explanation filter -> decision judgment -> confidence
```

Do not let evidence volume substitute for evidence quality.

### 5. Red-Team the Judgment

Create or update `05_red-team-review.md`.

Actively challenge the preferred conclusion:

- Is the main judgment sufficiently supported?
- Is there selective evidence?
- Are negative or ambiguous signals ignored?
- Are stronger alternative explanations available?
- Which assumption is most fragile?
- Should confidence be lowered?
- What evidence would improve judgment quality?

Lead with the strongest objections, not the conclusion.

### 6. Produce the Knowledge Product

Create or update `06_knowledge-product.md`.

For business decisions, use a commercial report structure:

1. Core conclusion and executive summary
2. Evidence chain and confidence
3. Analysis and counter-arguments
4. Business boundaries and impact assessment
5. Action plan and dynamic triggers

Requirements:

- Start with a one-sentence conclusion.
- Separate core facts, judgments, and assumptions.
- Cite evidence IDs in facts, evidence tables, reasoning, and counter-arguments.
- Mark confidence for each core judgment.
- Include uncertainty, alternative explanations, action matrix, and monitoring indicators.
- Avoid adding facts outside the approved evidence set.

### 7. Create a Watchlist

Create or update `07_watchlist.md`.

Translate the report into monitorable indicators:

- indicator
- why it matters
- source
- frequency
- trigger condition
- action after trigger
- status

Make watchlist items capable of raising, lowering, or redirecting the decision.

### 8. Write the Retrospective

Create or update `08_retrospective.md`.

Capture:

- whether the original question was answered
- most valuable sources
- noisy or misleading sources
- reusable analysis methods
- assumptions needing verification
- how to go faster next time
- resources to add to the pool
- templates to preserve

## Confidence Rubric

- `高`: direct, reliable, relevant, and corroborated evidence; few plausible counter-explanations.
- `中`: useful evidence exists, but some pieces are indirect, adjacent, or not independently verified.
- `低`: evidence is sparse, indirect, or dependent on unverified assumptions.
- `低到中`: enough evidence for cautious action or limited validation, not enough for full commitment.

## Output Style

- Use Chinese when the case artifacts are Chinese unless the user requests otherwise.
- Keep executive summaries short and decision-oriented.
- Use tables for ledgers, evidence summaries, action matrices, and triggers.
- Preserve evidence IDs exactly across artifacts.
- Prefer "current evidence supports..." over categorical claims when confidence is not high.
