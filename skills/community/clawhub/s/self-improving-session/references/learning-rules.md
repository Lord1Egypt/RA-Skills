# Learning Rules

## What to Learn

### High-value signals

- Explicit user correction of your behavior
- Explicit durable workflow rule
- Explicit project convention
- Repeated reusable preference across tasks

### Medium-value signals

- Repeated prompt-workflow choices from `self-improving-prompt`
- Repeated output-format preferences
- Repeated tool-usage preferences

These should only become rules once they meet the confidence thresholds.

If an existing rule already captures the behavior well enough, prefer no change.

### Low-value signals

- One-off debugging choices
- Temporary workarounds
- Decisions tied tightly to a single scenario
- Generic praise without clear reusable meaning

## What NOT to Learn

Never store:

- full prompt text
- secrets, passwords, tokens, or sensitive data
- highly changeable paths or code facts already derivable from source
- temporary task state

Usually skip:

- framework defaults
- obvious common sense rules
- anything already clearly documented in repo docs or config

## Confidence Thresholds

| Pattern | Action |
|--------|--------|
| User explicitly says "always do X" or "don't do X" | Record as `[stable]` |
| Same reusable preference appears 2 times across different tasks | Record as `[tentative]` |
| Same reusable preference appears 4 times across multiple task contexts | Upgrade or record as `[stable]` |
| Preference signal is mixed or inconsistent | Do not record |

## How to Judge self-improving-prompt Signals

| Pattern | Action |
|--------|--------|
| User explicitly says "compare first" | Record immediately as `[stable]` workflow rule |
| User explicitly says "don't compare, just execute" | Record immediately as `[stable]` workflow rule |
| User repeatedly chooses refined version across tasks | May become `[tentative]` then `[stable]` using the thresholds above |
| User alternates between refined and original depending on context | Do not overfit |
| Single refined/original choice with no explanation | Usually skip |

## Merge Strategy Examples

### Add a new rule

```text
Before: no relevant workflow rule exists
Signal: user says "always show acceptance criteria for risky tasks"
After:  - Show acceptance criteria for risky tasks [stable]
```

### Update a conflicting rule

```text
Before: - Always compare refined and original prompts [stable]
Signal: user says "only compare when the rewrite materially changes execution"
After:
- ~~Always compare refined and original prompts~~ [corrected: 2026-04-14]
- Compare prompts only when refinement materially changes execution [stable]
```

### Upgrade a tentative rule

```text
Before: - Prefer concise final answers [tentative]
Signal: user reinforces the same preference in later sessions
After:  - Prefer concise final answers [stable]
```

### Merge redundant rules

```text
Before:
- Do not store full prompt text
- Do not keep the exact prompt content
- Learn only abstract preference rules

After:
- Learn abstract preference rules only; never store full prompt text
```

### Prefer replacement over expansion

```text
Before:
- Show refined prompts before confirmation [stable]
- Compare prompts only for ambiguous tasks [tentative]

Signal: user repeatedly prefers compare-first only when refinement materially changes execution

After:
- Show compare-first only when prompt refinement materially changes execution [stable]
```
