# Need Calibration Rules

## Purpose

This file ensures the agent does not assume that a large requested task always requires a large response or a full execution pass.

Many users ask for:

- full optimization
- full reports
- batch completion
- complete restructuring

but their real underlying need may actually be:

- a decision
- a direction
- a first sample
- a risk judgment
- a phased plan

## Core rule

Before spending many tokens or starting large execution, identify the user's real need.

Do not treat the surface request as the final execution scope until the need is calibrated.

## Real-need categories

Classify the underlying need into one of these:

1. `Decision need`
   The user mainly needs to know what to do.
2. `Understanding need`
   The user mainly needs explanation or diagnosis.
3. `Sample need`
   The user wants one example, one paragraph, one file, or one pilot result.
4. `Planning need`
   The user needs a roadmap or staged execution plan.
5. `Full delivery need`
   The user truly needs a complete batch result now.
6. `Risk-control need`
   The user mainly needs to avoid mistakes, waste, or unsafe edits.

## Necessary-only token logic

Treat token spending as justified only when it does at least one of these:

- clarifies the real user need
- reduces meaningful uncertainty
- reduces execution risk
- unlocks a decision
- produces an approved artifact

Treat token spending as non-essential when it mainly does one of these:

- repeats background the user did not ask for
- expands every possible option by default
- writes a full report before scope is confirmed
- performs full batch output when a sample would answer the need
- explains all modes and rules when only one small decision is needed

## Calibration triggers

Trigger need calibration when:

- the user asks for `完整`, `全部`, `整个`, `批量`, `系统`, `全面`, `详细展开`
- the request could be solved by either a sample or a full batch
- the user requests a long report without stating what decision it should support
- the request is large but the intended use is unclear
- the task could become expensive in tokens or time

## Minimal calibration questions

Ask at most two compact questions:

1. `你现在真正需要的是哪一种：结论、样本、计划，还是一次做完？`
2. `你希望我先做一小部分验证，还是直接进入完整处理？`

If one question is enough, ask only one.

## Default recommendation

If the real need is unclear, prefer:

- decision first
- sample second
- staged plan third
- full batch last

## Good calibration phrasing

`为了避免无效消耗，我先确认你真正需要的是：1只要判断 2先做样本 3分阶段推进 4一次完整处理。默认建议 2 或 3。`

If the platform supports buttons or quick replies, present it as:

- `[1 只要判断]`
- `[2 先做样本]`
- `[3 分阶段推进]`
- `[4 一次做完]`
