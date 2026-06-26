# Benchmark Discipline

Use this reference when the main risk is a fake win.

## Non-negotiables

- Freeze the task, metric, and split before optimization starts.
- Never compare candidates on different validation or test surfaces.
- Keep the current trusted baseline runnable while the campaign is active.
- Record every benchmark exception explicitly.

## Common invalid-win patterns

- training on benchmark or holdout examples
- tuning directly on hidden evaluation cases
- changing preprocessing only for one candidate
- reporting the best slice instead of the agreed score
- comparing against a baseline that was never actually rerun

## Review questions

- Did the candidate beat the exact reproduced baseline?
- Did the metric code stay fixed?
- Did the candidate preserve important non-target surfaces?
- Is the reported score robust enough to survive at least one adjacent rerun?
- Would an external reviewer agree the comparison is fair?

## Claim wording

Use the strongest honest label only:

- "promising"
- "best internal result so far"
- "matches reproduced reference"
- "exceeds reproduced reference on the agreed benchmark"
- "SOTA claim is plausible pending external confirmation"

Reserve "new SOTA" for cases where benchmark rules and public comparison logic are actually satisfied.
