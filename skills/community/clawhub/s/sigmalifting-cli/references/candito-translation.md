# Candito Translation

This reference captures modeling rules extracted from a real app-exported Candito sample that validated and normalized cleanly through the standalone CLI.

## First Principle

When a user gives you an exported Candito bundle, validate and normalize that file first.

Do not start from the public spreadsheet and assume the structure.

The exported app bundle is authoritative for how SigmaLifting chose to model the program.

## Structural Lessons

The sample is not one block.

It is six blocks, each with `duration: 1`:

1. Muscular Conditioning
2. Hypertrophy
3. Linear Progression
4. Heavy Acclimation& Po
5. Maximal Strength
6. Deload or Max Test

The key lesson is not the exact phase names. It is the modeling choice:

- each structurally distinct week became its own block
- the block count matches the real phase boundaries
- the process `blockly_one_rm` array length also matches block count

For this family of Candito translations, unique-week structure is strong evidence for `duration: 1` blocks.

Observed phase footprint in the sample:

- Muscular Conditioning: 6 scheduled days, 16 exercises
- Hypertrophy: 5 scheduled days, 16 exercises
- Linear Progression: 4 scheduled days, 12 exercises
- Heavy Acclimation& Po: 4 scheduled days, 12 exercises
- Maximal Strength: 3 scheduled days, 7 exercises
- Deload or Max Test: 1 scheduled day, 1 exercise

## What Actually Changes Across Blocks

The sample changes:

- number of training days used in the week
- which days are blank in the 7-slot schedule
- which exercises appear in the week
- which exercises are anchored
- how many set groups each exercise has
- whether a lift is fixed percentage work, source-dependent backoff work, a multi-step percentage ladder, an accessory stack, or a special-rule set

That is why compressing these weeks into one block is wrong even if the schema can technically hold all the numbers.

## Candito Modeling Rules

### 1. Use one-week blocks when the week skeleton changes

If the day layout or exercise structure changes materially from week to week, keep those weeks as separate blocks with `duration: 1`.

### 2. Trust schedule shape, not day labels

The exported sample uses day names like `Untitled` and copied suffixes.

Do not infer semantics from those names.

Use these as the real signals:

- block name
- `weekly_schedule`
- day occupancy
- exercise membership per day

### 3. Use anchors conservatively and explicitly

Observed anchor patterns in the sample:

- competition squat: `squat` with ratio `1`
- competition bench: `bench` with ratio `1`
- competition deadlift: `deadlift` with ratio `1`
- deadlift variations: `deadlift` with ratio `0.9`
- accessories: anchor disabled

Do not invent anchors for accessories.

### 4. Use `rpe` as the variable parameter for percentage-driven rep-range work

In the sample, many main-lift set groups look like:

- `variable_parameter: "rpe"`
- fixed `weekly_weight_percentage`
- `weekly_rpe: [-1]`

That means the set is modeled as a percentage-based prescribed set where the realized RPE is the variable outcome.

This is important for Candito-style rep-range and max-rep work.

### 5. Use `weight` as the variable parameter for accessories and manual-rule work

In the sample, accessories and special-rule work usually look like:

- `variable_parameter: "weight"`
- `weekly_weight_percentage: [-1]`
- fixed reps and set counts

That is the right choice when the work is load-progressed manually rather than percentage-prescribed from the anchor.

### 6. Keep special rules in notes unless they are truly machine-derived

The sample preserves important instructions in `weekly_notes`, including:

- extra volume squat rules
- back-off squat decision rules
- rep-range reminders like `4-6 reps`, `3-6 reps`, `1-2 reps`, `1-4 reps`
- deadlift-variation special handling

Do not convert these into fake automation unless the app actually has a precise mechanic for them.

For Candito, notes are often the correct representation.

### 7. Prefer explicit set groups over over-abstract backoff logic

The sample mostly encodes Candito work as explicit set groups rather than using automatic backoff or fatigue-drop configs.

That is a useful default when the spreadsheet logic is human-rule-heavy.

Do not call every lower-load follow-up set a Sigma backoff. If the weight is independently prescribed, such as a fixed percentage from 1RM, model it as an explicit set group. Use `backoff_config` only when the later set group's weight depends on a previous set group's actual or calculated weight.

## Process-Side Lessons

The exported sample is a `process-import`, not just a `program-import`.

Important consistency checks:

- the sample has 64 exercises and 64 exercise recordings
- `exercise_recordings.length` matches `exercises.length`
- each recording belongs to one exported exercise id
- each recording `weekly.length` matches its block `duration`
- `blockly_one_rm.length` matches `program.blocks.length`

When synthesizing similar process bundles, keep those alignments exact.

## Practical Heuristic

For Candito-style translations:

1. validate the exported bundle with the CLI
2. normalize it to inspect the canonical shape
3. identify the phase boundaries from structure, not just chronology
4. keep unique weeks as separate blocks
5. use anchors and variable parameters the way the exported sample does
6. store human decision rules in notes unless the app has real automation for them

If your translated bundle feels smaller only because you compressed unlike weeks together, it is probably wrong.
