---
name: reelier
description: Replay recurring deterministic jobs at 0 tokens instead of re-reasoning them every run. For cron/heartbeat tool-call workflows (status checks, data pulls, report generation, CRUD sequences) — record the job once with reelier, then run "npx -y reelier run <skill>" on every heartbeat and gate drift with "reelier diff". Never for open-ended coding or file-edit work, which Reelier cannot replay.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - reelier
        - npx
    install:
      - kind: node
        package: reelier
        bins:
          - reelier
    emoji: "🧾"
    homepage: https://github.com/seldonframe/reelier
---

# Reelier — stop re-paying for the same job every heartbeat

Reelier compiles a run that *worked* into a `SKILL.md` file that replays
deterministically: no LLM, 0 tokens, an assertion on every step, a receipt
for every run. This skill teaches you **when** to reach for it inside
OpenClaw — written against `reelier` 0.12.x.

## The math that makes this matter

A cron job on a 15-minute heartbeat fires **2,880 times a month**. If the
agent re-reasons the job on every heartbeat, that is 2,880 LLM call-chains
billed for work that produces the same tool calls every time (~18k tokens
and ~$0.019 per run on our published benchmark task — roughly **$55/month
per job**; your task will vary). The replayed version of the same job is
**0 tokens, every run, measured** — and the 0 does not vary.

So the rule is: **recurring deterministic job → record once, replay
forever.** Spend LLM tokens only on the runs where something actually
changed.

## The honesty boundary — read this first

Reelier can only replay **deterministic tool calls**: its own HTTP
builtins (`http.get`/`http.post`) and MCP tool calls. It **cannot** replay
file edits, shell commands, reads/searches, subagent dispatch, or anything
non-deterministic (varying search results, LLM-generated content,
unparameterized timestamps).

**Never tell the user "I'll replay this session" about a coding session.**
If a session was mostly edits and greps, `reelier scan` /
`reelier from-session` will honestly report nothing replayable (an empty
result, not an error) — that is expected. Only freeze jobs that were
*actually* a sequence of API/MCP calls.

## Step 1 — record the job once

Three ways, in order of preference:

1. **From a session that already did the job** — cheapest, because the
   work is already paid for:

   ```sh
   npx -y reelier scan            # finds replayable sequences in your
                                  # session history (reads ~/.openclaw,
                                  # ~/.claude, and other agent dirs)
   npx -y reelier from-session <transcript.jsonl> --name <job-name>
   ```

2. **Lossless capture going forward** — put Reelier's recording proxy in
   front of the MCP server(s) the job uses, then run the job once:

   ```sh
   npx -y reelier mcp --wrap "<your mcp server command>"
   npx -y reelier compile <trace.jsonl> -o <job-name>.skill.md
   ```

3. **Guided** — `npx -y reelier init` walks the whole loop in ~60s.

Report the compile result honestly: name the skill path and step/assert
counts, and read out the compiler's **Open questions** verbatim if
non-empty — those are gaps it declined to guess about (literal dates,
UUIDs, timestamps that should probably be variables). Never hide them.

## Step 2 — replay on every heartbeat

Replace the re-reasoned job in the cron/heartbeat with the replay:

```sh
npx -y reelier run <job-name>.skill.md
```

- **0 LLM tokens, milliseconds**, and every step is asserted — a broken
  step fails loudly, never silently passes.
- **Read-only by default.** A write step (`idempotent-write`) never
  re-fires unless you explicitly pass `--allow-writes`. Do not add
  `--allow-writes` "just in case" — add it only when the job is *supposed*
  to write and the user knows it.
- Parameterize per-run inputs with `--var name=value`.

## Step 3 — gate drift with diff

```sh
npx -y reelier diff <job-name>     # exit 1 on drift
```

`diff` compares the last two runs recorded in
`.reelier/runs/<job-name>.jsonl` and reports **SAME or DRIFTED per step**,
with the failing assertion as the *why*. Exit code 1 on drift makes it a
gate: chain it after the replay in the scheduled job, and only wake the
LLM when it fails.

**On drift: do not force a pass.** Say plainly which step drifted and why,
do the task live (with real reasoning), then re-record and re-compile so
the frozen baseline matches reality again. Rewriting an assertion to make
a drifted run "pass" is lying.

## The heartbeat pattern, end to end

```sh
# inside the recurring job:
npx -y reelier run <job-name>.skill.md && npx -y reelier diff <job-name>
# exit 0  -> job done, 0 tokens, receipt written — stop here
# exit 1  -> something real changed: investigate with the LLM, fix,
#            re-record, and let the next heartbeat replay again
```

Every run leaves a receipt (per-step outcomes, timing, token count
[measured]) — so "the cron ran" is provable, not claimed.
