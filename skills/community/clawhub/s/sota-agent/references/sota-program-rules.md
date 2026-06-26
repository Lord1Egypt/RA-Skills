# SOTA Program Rules

Use this reference when the task is to drive DS or CV work toward a frontier or SOTA result.

## 1. Define "SOTA" precisely

- Public leaderboard SOTA
- Internal benchmark best
- Best deployable result under your latency or cost budget

Pick one. Mixing them creates fake wins.

## 2. Lock the benchmark

Before model work, record:

- dataset identity
- split or holdout definition
- primary metric
- non-regression surfaces
- trusted baseline

If any of those change, treat it as a new program state, not a silent continuation.

## 3. Separate queues

Keep three queues distinct:

- `research backlog`: paper ideas worth understanding
- `prove-it queue`: bounded candidates worth running
- `promotion queue`: candidates already benchmarked and ready for a final hold-or-promote review

## 4. Convert papers into testable units

For each paper idea, write:

- what exact change will be applied
- what stays fixed
- what metric should move
- how much movement would justify keeping the line alive

Avoid adopting a full paper stack if one smaller idea can answer the real question.

## 5. Require ablations

- One factor change per ablation block when learning is the goal.
- If multiple changes land together for speed, record that the result is confounded.
- Do not call a win "understood" until the ablation queue explains where the gain came from.

## 6. Track stage, not only score

Useful stages:

- `idea`
- `smoke`
- `short-benchmark`
- `full-benchmark`
- `runtime-check`
- `product-surface`
- `trusted`

A strong `smoke` result is not a trusted release candidate.

## 7. Kill lines early

Hold or cut a line when:

- the expected win never appears in the short loop
- the candidate only wins on one narrow slice and regresses the protected surfaces
- the line exceeds the agreed cost or runtime budget
- the evidence bundle is incomplete

## 8. Promote only on repeatable wins

Require:

- the candidate beats the trusted baseline on the fixed benchmark
- the runtime or deployment surface is acceptable if it matters
- the product or user-facing surface is acceptable if it matters
- the review packet is complete enough that another engineer could audit the decision
