# self-improving-session Merge Reference Details

## Merge Conflict Priority

Highest to lowest:

1. Explicit user correction in the current or latest relevant session
2. Existing `[stable]` rules
3. Repeated evidence sufficient for `[stable]`
4. Repeated evidence sufficient for `[tentative]`
5. Newly noticed weak signals that do not yet meet threshold

Rules:

- A new `[tentative]` rule cannot overwrite an existing `[stable]`
- Only explicit correction can replace an existing `[stable]`
- Merge same-meaning rules instead of keeping wording variants
- Prefer replacements and merges over net-new additions

## Confidence Thresholds

Use one consistent standard:

- explicit correction or explicit permanent instruction -> `[stable]`
- same reusable preference observed 2 times across meaningfully different tasks -> `[tentative]`
- same reusable preference observed 4 times across multiple task contexts -> `[stable]`

Weak or mixed evidence should not be learned.

## Tentative Expiry Strategy

- If a `[tentative]` rule is contradicted by stronger evidence, replace or remove it
- If a `[tentative]` rule goes unvalidated across multiple later sessions, delete it
- If validated enough times, upgrade it to `[stable]`

Do not let tentative rules accumulate indefinitely.

## Where to Write Rules

| Rule Type | Target File |
|-----------|-------------|
| Cross-project workflow preferences | `~/.claude/CLAUDE.md` |
| Project-specific coding conventions and architecture rules | Project `CLAUDE.md` |
| One-off debug notes or incident lessons | Separate task notes, not `CLAUDE.md` |

Do not write temporary fix notes into `CLAUDE.md`.

## Rule Budget

- Keep global workflow sections to about 20 bullets
- Keep project convention sections to about 15 bullets unless justified
- Compress before appending when sections become noisy
- One session should usually propose no more than 3 new rules unless the user explicitly asks for a broader rules rewrite
- If a target section is already over budget, compact first and do not append new rules unless the user explicitly approves
- Zero new rules is a normal outcome when existing guidance is already good enough

## self-improving-prompt Event Judgment

- One event alone is weak evidence
- Explicit verbal instruction can create a rule immediately
- Repeated consistent events may justify `[tentative]` or `[stable]`
- Mixed event patterns should not be learned
