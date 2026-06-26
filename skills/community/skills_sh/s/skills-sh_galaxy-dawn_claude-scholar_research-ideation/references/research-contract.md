# Research Contract

Use this contract to carry research state across Claude Scholar workflows.

The goal is to preserve:
- what question is being studied,
- what evidence currently exists,
- what claim is allowed by that evidence,
- what uncertainty remains,
- what decision or next action should happen.

## Research Question Card

Use this card when a vague idea becomes a research direction.

```md
## Research Question Card

Question:
Type: exploratory | confirmatory | applied
Hypothesis:
Why it matters:
Current evidence:
Missing evidence:
What would support it:
What would falsify it:
Minimal next action:
Decision: explore | read more | run experiment | stop
```

## Evidence Record

Use this record for paper evidence, project notes, experiment outputs, and analysis artifacts.

```md
## Evidence Record

Evidence ID:
Source:
Source type: full paper | preprint | dataset | experiment artifact | project note | abstract-only | webpage placeholder
Supports:
Contradicts:
Method / dataset / metric:
Limitation:
Project relevance:
Claim strength: speculative | observed | supported | strong
```

Evidence ID format:
- Use `ER-YYYYMMDD-shortslug-NN`, for example `ER-20260513-tta-eeg-01`.
- Keep IDs unique within the project or research thread.
- Use stable, human-readable slugs. Do not use vague IDs such as `E1`, `paper1`, or `source-a`.
- Reuse the same Evidence ID when the same evidence record is referenced downstream; create a new ID only for a distinct source, artifact, or analysis result.

## Claim Candidate

Use this candidate when an analysis or synthesis suggests language that may later enter a report, paper, rebuttal, or project plan.

```md
## Claim Candidate

Claim:
Source evidence:
Allowed wording:
Forbidden stronger wording:
Uncertainty:
Next check:
Decision: keep | weaken | revise | discard
```

## Source Trust Levels

Use source trust to decide whether a note can support downstream synthesis.

- `full paper` / `preprint`: can support `observed`, `supported`, or `strong` claims when the relevant method, dataset, metric, and limitation are named.
- `dataset` / `experiment artifact`: can support project claims when the unit of analysis, metric, provenance, and analysis limits are named.
- `project note`: can support hypotheses and plans, but not literature-backed claims unless it links to separate evidence records.
- `abstract-only` / `webpage placeholder`: can support discovery and `To-Read` routing only. Do not use it to support `Knowledge`, manuscript, or rebuttal claims unless it is later replaced by a full paper, preprint, or verified artifact.

## Claim Promotion Gate

Before a claim moves into `Knowledge`, `Writing`, a report, a manuscript draft, or a rebuttal, check:

1. The claim has at least one Evidence Record ID.
2. The source type is strong enough for the intended claim.
3. The claim strength is not silently upgraded.
4. The allowed wording and forbidden stronger wording are both recorded.
5. Contradictory evidence or missing evidence is preserved.

If any item fails, keep the claim as a hypothesis, motivation, warning, or `To-Read` item. Do not polish it into a durable conclusion.

## Proposal Readiness Gate

Generate a `research-proposal.md` only when:

- one Research Question Card is selected,
- current evidence is enough to justify the question and method,
- missing evidence is explicit and tractable,
- the minimal next action is more specific than "read more",
- citations or evidence records are available for the key motivation claims.

If these conditions are not met, generate `research-question-card.md`, a gap note, or an intake summary instead of a proposal.

## Strength Rules

- `speculative`: plausible idea, weak or indirect evidence only.
- `observed`: seen in a paper, note, or experiment, but not yet enough for a durable conclusion.
- `supported`: backed by explicit evidence such as a paper result, experiment, or analysis bundle.
- `strong`: supported by multiple evidence anchors or statistically rigorous project evidence.

Do not promote a claim to a stronger level without naming the evidence that justifies the upgrade.
