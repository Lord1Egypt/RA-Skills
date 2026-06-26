# Process Logging

Use this reference when an agent is updating a running `process-import` bundle from user workout data.

## Program Versus Process

The program is the prescription. Do not edit it during ordinary workout logging.

Program `weekly_notes` are part of the prescription. Use them only for program facts the schema cannot express directly, such as:

- rep ranges like `4-6 reps`
- branch rules like optional max attempts
- special prescription logic that cannot fit in fixed reps, weight, or RPE fields

Do not use program `weekly_notes` for generic coaching cues by default.

The process is the user's execution diary. Actual performed sets and per-exercise day notes belong in the process.

## Normal Logging

If a user reports a set that corresponds to a prescribed set slot, write it to that slot with `process update-set`.

Use:

- `weight` for actual load used
- `reps` for actual reps completed
- `rpe` for actual reported RPE
- `completed: true` when the set was performed

Do not change the source program just because the user's actual set differs from the prescription.

## Off-Plan Work

If the user tries to do something materially outside the prescription, the agent should first resist and explain the mismatch.

Examples:

- prescribed triples but the user wants an extra heavy single
- prescribed 3 sets but the user wants a fourth or fifth set
- prescribed percentage work but the user wants a much heavier load
- fatigue or pain makes the attempted work unsafe or clearly inconsistent with the plan

If the user insists, or reports that the off-plan work already happened, preserve the record without corrupting the prescription:

- If the set still corresponds to a prescribed set slot, log it into that prescribed slot as the actual performed set.
- If the work is extra or too far from any prescribed slot, do not create fake prescribed sets just to hold it.
- Put the off-plan detail in the process exercise note for that week using `process update-note`.

The note should be factual and concise:

```text
Off-plan: user performed an extra 405x1 @9.5 single after the prescribed squat work.
```

Do not write this into program `weekly_notes`.

## Finding State

For an installed CLI workflow, prefer these commands:

1. `sigmalifting-cli process list --compact`
2. `sigmalifting-cli process show --process-id <id> --compact`
3. `sigmalifting-cli render process-overview --file <stored-json> --raw`
4. `sigmalifting-cli render exercise-detail --file <stored-json> --exercise-id <id> --raw`
5. `sigmalifting-cli process get-recording --process-id <id> --exercise-id <id> --compact`

Use `SIGMALIFTING_HOME` or `--store-root` to make sure you are reading and writing the intended store.

## Answering "What Is Next?"

To answer what the user should do next:

1. inspect the process recordings for completed sets
2. inspect the program exercise set groups for prescribed set count, reps, RPE, and percentage
3. compute percentage-based loads from the process one-rep-max profile and weight rounding config
4. check `backoff_config.enabled` before describing a set as backoff or deriving it from another set
5. account for program notes only when they encode prescription facts
6. recommend the next uncompleted prescribed set

Do not infer Sigma backoff semantics from ordinary gym wording. A later set at a lower fixed percentage is not a backoff unless `backoff_config.enabled` is true and it depends on an earlier set group.

If the CLI cannot compute the next set directly, do the calculation explicitly and state the assumption.
