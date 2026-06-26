# Program Modeling

## Block Definition

In SigmaLifting, a block is not merely "some consecutive weeks."

A block is the longest consecutive span of weeks where each exercise keeps the same structural role and only the weekly values change.

This is similar to combining like terms:

- if the structure is the same, keep it in one block and vary the weekly arrays
- if the structure changes, it is not the same term anymore and should become a new block

## Structural Sameness

Treat weeks as structurally the same only if all of the following stay stable:

- day count and day identity
- exercise identity per day
- set-group count per exercise
- set-group ordering
- variable parameter selection
- dependency graph between set groups
- meaning of the exercise within the phase

Numeric drift alone does not require a new block.

Examples of numeric drift that can stay inside one block:

- 5 reps becomes 3 reps
- 72.5% becomes 80%
- 4 sets becomes 5 sets
- notes change week to week

Examples of structural drift that should usually create a new block:

- fixed percentage work becomes source-dependent backoff work
- an accessory disappears and a competition lift variation replaces it
- a day changes from bench volume day to bench intensity day with a different lift stack
- a lift changes from a single set-group structure to multiple semantically distinct set groups

## Backoff Semantics

Do not use generic lifting slang as the schema model.

In SigmaLifting, a set group is a backoff only when `backoff_config.enabled` is true and `depends_on_set_group_id` points to an earlier set group.

Use `backoff_config` when the later set group's weight should be derived from a previous source set group, such as:

- a percentage of the source group's actual weight
- a target-RPE calculation from the source set's actual weight, reps, and RPE

Do not model fixed lower-percentage work as backoff. If the program says `1x3 @85%` followed by `2x5 @75%`, and both weights are prescribed directly from 1RM, that is two explicit percentage set groups, not a source-dependent backoff.

For real backoff work, the source set group should normally make weight the workout-recorded variable. If the source weight is already fully prescribed by percentage, there is usually no reason to make later work depend on it; model the later work explicitly instead.

The dependent backoff group itself should not use `variable_parameter: "weight"` when the app is expected to calculate its weight. Record a different variable, usually RPE or reps, while the backoff config supplies the weight.

## Variable Parameter Semantics

Each set group chooses one parameter to record at workout time:

- `weight`: prescribe reps and RPE
- `reps`: prescribe weight and RPE
- `rpe`: prescribe weight and reps

The selected variable parameter is not another prescribed progression column. It is the slot the lifter fills in during execution.

Backoff and fatigue-drop behavior depends on runtime performance and is represented in the app as RPE-variable work. Use `variable_parameter: "rpe"` for dependent backoff or fatigue-drop set groups. Do not enable mixed-weight prescription when `variable_parameter` is `weight`, because mixed weight is itself a weight prescription.

## Anti-Pattern

Bad modeling pattern:

- start from program duration
- create one block with that duration
- force every week into that block using zeros and notes

This produces a bundle that may validate, but it hides the real phase structure and makes the program harder to edit, inspect, and reason about.

## Better Heuristic

When translating a manual or spreadsheet:

1. write down each week's day and exercise skeleton
2. compare adjacent weeks for structural equivalence
3. split the program whenever structural equivalence breaks
4. only then fill in weekly arrays for the block

If a generated bundle feels "technically representable" but not "true to the phase structure," the block model is probably too compressed.
