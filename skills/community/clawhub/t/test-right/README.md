# TestRight: Get Answers Without Endless Testing

TestRight helps your AI test whether something actually works or improves results. Say “Use TestRight to test this,” and it examines the relevant project, chooses meaningful checks, runs them and inspects the outputs. It addresses common AI testing mistakes: testing the wrong thing, using incorrect expected answers, coaching the baseline, leaking information between comparisons and claiming success without evidence. It also keeps testing scoped, preserves useful results and directs the AI to stop when it has enough evidence to answer your question.

## Why It Matters

An AI can run plenty of tests and still miss the actual problem. It can check a helper while the workflow fails, write assertions that accept a bug, or report success without inspecting the result.

Comparisons have another trap. The AI adds helpful instructions to the baseline, teaching it the behavior a new skill is supposed to add. A useful improvement then looks ineffective, and you waste time or money repeating the wrong test.

The author noted a recurring problem with GPT 6.1 Sol: extra instructions were added to the "before" baseline case, invalidating the comparison with the "after" case.

For example, when evaluating TestRight:

| Run | Request |
| --- | --- |
| Ordinary baseline | "Test this." |
| Evaluator-coached baseline | "Test this. Inspect the full workflow, check edge cases, verify the results and explain your evidence." |

The second request supplies part of TestRight's guidance. Preserve the original request and its relevant context, then apply TestRight in the experimental run. Keep instructions the real user actually supplied.

[Research behind the instructions](REFERENCES.md) explains these failures and the evidence supporting the chosen approach.

## Install and Use

Send your OpenClaw:

```text
Install TestRight from https://github.com/RedRookAI/openclaw-skills/tree/main/skills/test-right into this workspace's skills/test-right folder. Keep the supporting files together.
Then use TestRight to test [what you want tested].
```

After installation:

> Use TestRight to test this feature.

> Use TestRight on this pipeline change.

> Use TestRight to test this skill.

It uses your configured model and tools. Ask for a plan or review when that is all you want. Start a new chat if the installed skill does not appear. `$test-right` also works where supported.

For a fiction pipeline, TestRight checks the relevant execution path and reads the resulting fiction against the author's brief. A successful run and readable prose are separate outcomes.

## Optional Input Protection

For local AI comparisons, the included [Python input guard](references/input-guard.md) checks whether declared inputs changed after preparation. It makes no model calls and installs no hooks. Python 3 is needed only for this helper. Review the source request for coaching before preparing inputs.

## Use as a Prompt

Paste the body of [SKILL.md](SKILL.md), starting at its title, followed by what you want tested. The [AI comparison guide](references/ai-comparisons.md) provides additional detail for that workflow.

[Research](REFERENCES.md) · Version 0.1.2 · [MIT-0 license](LICENSE)
