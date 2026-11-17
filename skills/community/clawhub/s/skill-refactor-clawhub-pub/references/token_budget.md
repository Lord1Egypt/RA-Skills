# Token budget and compaction headroom

## Source of the numbers (verified online 2026-10-11)

- **Claude / Agent Skills official**: body **<500 lines** (hard), target 1500–2000
  words; `name` ≤64 chars; `description` ≤1024 chars.
- **Compaction budget (Claude Code)**: **5,000 tokens per skill**, with a
  **25,000-token combined budget** across all active skills in a session.
- **Empirical line→token anchors** (observed, English prose+code, ~4 chars/token):
  100 lines ≈700 · 300 ≈2,000 · **500 ≈3,500** · 1000 ≈7,000.

So the practical **per-skill body budget is ~3,500 tokens (≈500 lines)**, with the
first ~1,500–2,000 tokens holding the core that must survive compaction. The linter's
default `--token-budget` is set to **3500** to match the 500-line official cap; raise
it only if the host context window genuinely allows more.

## The three budget lines

| Line | Value | Meaning |
|---|---|---|
| **Per-skill body budget** | ~3500 tokens (≈500 lines) | the optimized SKILL.md body should fit under this (matches Claude official cap) |
| **Core up front** | first ~1500–2000 tokens | hard constraints + criteria core + five-step flow skeletons; these survive compaction |
| **Compaction headroom** | 5000 tokens/skill | Claude Code compaction budget per skill; combined cap 25000 across active skills |

The point is not to pack 8000 tokens of content - it is to keep the **core** in the
first ~3000 and reserve the rest as headroom for a long running conversation.

## Estimating tokens without an encoder

A good-enough rule for English prose and code: **~4 characters per token**. The
bundled linter uses this to flag:

- `body_est_tokens = len(body) // 4`
- over the budget -> **blocker** (must sink details)
- over 80% of the budget -> **low** (warning, close to the line)

To get a stricter count, run a real encoder; the linter's number is a planning
estimate, not a measurement.

## What stays in the body, what sinks to references/

Keep in the body (every turn):

- hard-constraint table
- criteria core (T/L/C/B)
- the five-step flow skeletons (input / output / fallback per step)
- the routing table that points into `references/`

Sink to `references/` (load on demand):

- per-platform frontmatter matrices
- wording templates and the changelog spec
- budget details and the token-estimation method
- worked examples beyond the three trigger cases

Rule of thumb: if a passage is not read on *every* trigger, it belongs in
`references/` with a single navigation pointer in the body.
