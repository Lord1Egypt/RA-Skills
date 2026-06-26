# Innovation Frontier Rubric

Use this rubric when a target repo starts from incomplete assets such as a README, toy benchmark, partial question bank, reviewer notes, or inherited scripts. The goal is to prevent the loop from becoming an asset-polishing machine that never escapes the initial framing.

## Core Rule

Current assets are the **evidence floor**, not the **imagination ceiling**.

Use current repo files to decide what is supported, but do not assume they define the best research question, benchmark axis, intervention, or paper contribution.

## Asset Fixation Signals

Flag `asset_fixation_risk` when any of these appear:

- the loop repeatedly edits README, locators, or packaging files without adding a new experimental mechanism
- all next steps are derived only from the existing file tree
- toy rules or synthetic rows become the center of the research agenda
- venue packaging starts before the benchmark has real empirical results
- reviewer feedback is treated as the whole research roadmap
- the same task taxonomy is extended without asking whether it is the right taxonomy
- prior MemPalace memory is copied forward without current-head or literature challenge

## Required Three-Lane Reading

Before selecting a micro-step, maintain three lanes:

1. `repair`: fix false claims, reproducibility issues, CI gaps, naming drift, or README drift.
2. `exploit`: strengthen the best current asset with tests, data, or a runnable probe.
3. `explore`: open a bounded new angle suggested by literature, expert council critique, or blank-slate reasoning.

The selected micro-step can be only one lane, but the advisor should keep all three visible.

## Blank-Slate Counterplan

Every major advisor pass should ask:

```text
If this repo only contained the original research theme and no current assets, what would be the strongest first benchmark or experiment design?
```

Write a short counterplan that includes:

- alternative research question
- alternative benchmark axis
- alternative intervention or mechanism
- minimal experiment to test it
- why it may beat the inherited asset path
- why it is not yet supported by current evidence

Do not execute the counterplan wholesale. Use it to generate one small exploration probe.

## Exploration Probe Rules

Exploration probes must be bounded and safe:

- create a small design note, fixture, benchmark slice, or dry-run script
- do not overwrite current empirical assets
- do not rename the whole project unless the advisor explicitly chooses a repositioning step
- do not claim empirical support until real outputs exist
- keep the connection to the current repo evidence visible

Good probe examples:

- add `docs/frontier_questions.md` with three alternative mechanisms and falsifiable tests
- add a tiny fixture that tests a missing benchmark axis
- write a dry-run evaluator that checks whether the current task taxonomy can express a new failure mode
- add a literature-backed benchmark dimension as `candidate_axis`, not as a result

Bad probe examples:

- start a full manuscript package before results
- replace the project direction based only on expert vibes
- generate many speculative hypotheses with no runnable next step
- treat a toy fixture as a confirmed empirical finding

## External Challenge

Use current literature and expert council as challenge lenses:

- ask what strong reviewers would say the current asset cannot test
- ask what adjacent benchmark families measure that the current repo ignores
- ask what negative control or counterexample would break the current framing
- ask whether the current task set is measuring proxy quality instead of the intended phenomenon

Expert memory is not evidence. It only helps identify questions to test.

## Cycle Policy

If two consecutive cycles are `repair` or `exploit` only, the next advisor pass should propose at least one `explore` or `bridge` micro-step unless an unresolved safety/reproducibility gate blocks it.

`bridge` means a micro-step that connects current assets to a broader frontier without abandoning them, such as adding a missing axis, counterexample fixture, or alternative protocol note.
