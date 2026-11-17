# Workflow Guard Rails

A horizontal safety layer for multi-step agent workflows. It wraps — not replaces — your workflow logic with seven guards that catch what the workflow itself cannot see.

## Why it exists

LLM and agent workflows fail in ways traditional error handling misses:

- A tool call returns "success" but the output is invalid → **false success**
- A side effect fires before validation → broken content reaches users
- A retry runs twice → **duplicate send**
- Small deviations compound across runs → **silent drift** until collapse

Workflow Guardian intercepts these at the boundaries.

## The seven guards

| # | Guard | Catches |
|---|---|---|
| 1 | Pre-execution check | Missing prerequisites, wrong scope |
| 2 | Checkpointing | Unrecoverable mid-task crash |
| 3 | Side-effect queue | Broken output reaching users |
| 4 | Retry budget | Duplicate sends, partial corruption |
| 5 | Result validation | False success |
| 6 | Audit log | Lost context, undetectable drift |
| 7 | Rule accumulation | Recurring, un-codified errors |

## How it works

1. **Before execution**: verify input, permissions, success criteria, idempotency key (guard #1).
2. **During execution**: emit checkpoints at each irreversible boundary (guard #2).
3. **Before external actions**: queue them; release only after validation (guard #3).
4. **After output**: run independent assertions (guard #5); failure triggers rebirth within budget (guard #4).
5. **After success**: write audit log (guard #6) and capture confirmed failures into the staging file (guard #7) — in the same run; promotion into the authoritative playbook is gated by recurrence or human confirmation.

## Key patterns

- **Result validation**: never trust "tool returned OK." Force self-check + independent code verification. When asserting `A == B`, also assert `A > 0`.
- **Side-effect queue**: external actions fire only after validation passes.
- **Drift monitoring**: track compliance across runs, not per run. First deviation = early warning.
- **Rule accumulation**: confirmed failures become standing assertions.

## Required companion file

Guard #7 writes confirmed failures into an error knowledge base at:

```
~/.workbuddy/ERROR-PLAYBOOK.md
```

This file is **not** bundled inside the skill directory, on purpose. Automation prompts and
`~/.workbuddy/MEMORY.md` reference it by absolute path, so its location has to survive this skill
being renamed, removed, or republished. Fetch it once:

```bash
mkdir -p ~/.workbuddy
# Pinned to commit d945aee0 — a mutable `main` URL is a supply-chain risk.
# To upgrade the playbook, deliberately move the pin to a new reviewed commit.
curl -o ~/.workbuddy/ERROR-PLAYBOOK.md \
  https://raw.githubusercontent.com/haiyangchenbj/error-playbook/d945aee01384c6163beb287446147ce768d50661/ERROR-PLAYBOOK.md
```

After downloading, verify before relying on it: the file must be non-empty and start with the
expected playbook header (§0 structure). Do not wire the downloaded file into any workflow until
that check passes.

It is indexed by **operation type** (write JSON, run shell, call API, git, publish, compute…), not
by date — the retrieval key for an error is the operation that failed. Do not fork it into a second
location; a second copy drifts, and a drifted rule is worse than no rule.

## Human in the loop

Explicit confirmation required before: first high-privilege tool use, any irreversible/external action, low-confidence results, and exhausted retry budget.

Rule accumulation (guard #7) is two-stage: confirmed failures are captured in the same run into `~/.workbuddy/ERROR-PLAYBOOK.staging.md`, with no approval gate on the capture (most failures surface during unattended runs where no human is present — that approval gate is why the rule library stayed empty for two months). A staged entry reaches the authoritative `ERROR-PLAYBOOK.md` only through the promotion gate: the failure recurs (count >= 2) or a human confirms it. A single unreviewed append never becomes durable global guidance.

## Output

```
🛡️ Guardian Report
- Pre-check: ✅ / ❌
- Checkpoints: N
- Side-effects queued: N, executed: N
- Validation: ✅ / ❌ (assertions: X/Y passed)
- Retries used: N / budget
- Audit log: written / skipped
- Rule captured: yes/no (staged this run; promoted: yes/no)
- Verdict: ✅ released / ❌ held for human
```

## Limitations

- Guards #5/#6 catch machine-checkable problems only. Style, semantics, and judgment drift need a separate review layer.
- Adds one validation step per run (<20% overhead).
- Only protects actions routed through the queue.