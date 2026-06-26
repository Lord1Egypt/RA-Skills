# Eval Loop for Self-Improvement

Use this reference when a repeated failure should become a tested operational improvement instead of only a logged lesson.

## Goal

Do not only ask "what did we learn?"
Also ask:
- what is the current baseline?
- what exact guardrail or rule changed?
- how will we measure whether it helped?
- should we keep or discard the change?

## Use this loop for
- repeated Mission Control wording failures
- missing receipts / missing proof chains
- deploy closeout failures
- stale operator-facing surfaces
- repeated handoff mistakes between agents
- recurring SOP/checklist changes

## 1. Define the target

State one concrete thing you want to improve.

Examples:
- Hunter summary should always include concrete links and details
- ClawLite deploy closeout should never stop at code-ready status
- Mission Control front-end should render source links from structured fields

## 2. Write 3-5 binary evals

Each eval must be yes/no.

Examples for summary quality:
- Does the summary include at least one artifact path or URL?
- Does the summary include evidence links when external proof matters?
- Does the summary include a detail block describing what actually changed?
- Does the summary include the next handoff or recovery action?
- Does the operator-facing surface actually render these fields?

Examples for deploy closeout:
- Is the deployed commit hash recorded?
- Is a deployment ref/URL recorded?
- Was the production page or sitemap actually verified?
- Was a structured receipt written?
- Is the final state classified with the correct deploy-state vocabulary?

## 3. Capture baseline

Before changing the rule/SOP/skill/checklist:
- record the current failure pattern
- record which evals currently fail
- treat this as the baseline state

## 4. Change only one thing

Good changes:
- one wording rule
- one new checklist item
- one schema field
- one render mapping
- one validation step

Bad changes:
- rewriting everything at once
- adding five new rules at once
- changing wording and schema and code together unless absolutely required

## 5. Re-check and classify

After the single change:
- run the same evals again
- note which checks improved
- decide:
  - KEEP
  - DISCARD
  - PARTIAL_KEEP

## 6. Promotion rule

Only promote broadly reusable changes after they pass the eval loop or after operator review confirms the change materially reduced the failure.

## Suggested experiment entry format

```md
## [EXP-YYYYMMDD-XXX] experiment

**Logged**: ISO-8601 timestamp
**Priority**: medium | high | critical
**Status**: baseline | testing | keep | discard | partial_keep
**Area**: workflow | tools | product | growth | security | infra | ops

### Target
What repeated problem is being improved

### Baseline
What was failing before the change

### Mutation
The single change introduced

### Binary Evals
- [ ] Eval 1
- [ ] Eval 2
- [ ] Eval 3

### Result
What improved / did not improve

### Keep or Discard
keep | discard | partial_keep

### Metadata
- Source: review | postmortem | user_feedback | qa
- Related Files:
- Tags:
```

## Important limit

A logged experiment is not the same as a finished fix. If the production surface or operator-visible truth is still wrong, the experiment remains incomplete even if the local change looks promising.
