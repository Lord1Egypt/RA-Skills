# Example Prompts

These prompts show the intended use of `use-skills`.

## Direct Request

```text
$use-skills
```

## Planning

```text
Turn this feature request into a clear implementation plan with testing notes.
```

## Coding

```text
Patch this bug report with the most relevant skill guidance driving the fix.
```

## Documentation

```text
Rewrite this README for clarity, structure, and actionability.
```

## Review

```text
Review this change and give me the strongest findings first.
```

## Product Spec

```text
This spans planning, implementation, and review. Use the best combination of skills and keep the final output clean.
```

## All Related Use

```text
Use all related skills for this request.
```

## Recommended Use

```text
Use the recommended skill set for this request.
```

## Restricted Use

```text
Use restricted mode. Recommend only the strongest skills.
```

## Reuse Previous Choice

```text
$use-skills again
```

Expected behavior: reuse the previous mode and working set if the task has not materially changed.

## First Mode Choice

```text
$use-skills
```

Expected behavior: if no previous mode applies, ask a numbered `1`, `2`, `3` mode question with likely skill candidates for each option.

## Ambiguous Mode

```text
Patch this bug report with the most relevant skill guidance driving the fix. $use-skills
```

Expected behavior: ask the numbered mode question before reading files or selecting skills, because `most relevant` is not an explicit mode.

Example first response:

```text
1. All related - use every available skill that is meaningfully related.
   Using: use-skills, brainstorming, writing-plans, humanizer, enhance-prompt
   For: broad coverage across fix strategy, report structure, prompt clarity, and wording

2. Recommended - use the best balanced working set.
   Using: use-skills, brainstorming, writing-plans
   For: strong output without unnecessary noise

3. Restricted - use only the strongest matches.
   Using: use-skills, brainstorming
   For: focused output with minimal skill involvement

Choose skill mode. Reply with 1, 2, or 3.
```
