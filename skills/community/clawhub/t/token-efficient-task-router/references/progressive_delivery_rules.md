# Progressive Delivery Rules

## Purpose

This file helps the agent decide whether a task should be completed in one full batch or advanced gradually in stages.

## Core rule

Do not assume that full completion is the most efficient path.

For many medium or large tasks, progressive delivery has higher ROI because it:

- checks the direction before committing
- catches misunderstanding earlier
- reduces wasted output
- reduces unsafe large-scale edits
- lets the user stop once the real need is satisfied

## Delivery levels

### Level 1: Decision-only

Give:

- the judgment
- the next step
- the smallest useful recommendation

Use when the user mainly needs orientation.

### Level 2: Sample or pilot

Give:

- one example
- one paragraph
- one file
- one subgroup
- one slice of the work

Use when the user wants to see the pattern before approving scale.

### Level 3: Staged execution

Give:

- a plan
- the first batch
- a checkpoint
- the next batch after confirmation

Use when the task is large, repetitive, or moderately risky.

### Level 4: Full batch delivery

Give:

- the complete result in one run

Use only when all of these are true:

- the scope is clear
- the success pattern is stable
- the risk is acceptable
- the user explicitly wants full completion
- staged validation is unlikely to change the direction

## Default recommendation logic

Prefer:

1. decision-only
2. sample or pilot
3. staged execution
4. full batch

unless the task clearly justifies a higher level.

## When full batch is justified

Full batch can be efficient when:

- the task is low-risk and highly repetitive
- the format is fixed
- the user already approved the pattern
- there is little ambiguity
- stopping early would not save meaningful effort

## When progressive delivery is better

Prefer progressive delivery when:

- the request is broad or vague
- the user may only need part of the final output
- the task touches many files or materials
- the pattern may need adjustment after the first sample
- token cost could become large
- the task is exploratory rather than mechanical

## Good prompt

`这个任务可以一次做完，也可以渐进推进。为了更省 token，我建议先做：1只判断 2先做样本 3分阶段推进 4一次完整处理。`
