---
name: token-discipline
description: 'Stop wasting context on the agent''s own output. Applies when running diagnostic commands, reading files, or summarizing findings: filter tool output before it enters the transcript, never re-quote what the reader can already see, and state conclusions once. Invoke with /token-discipline; stays on until "normal tokens".'
disable-model-invocation: true
license: MIT
metadata:
  tags: "Token, Context, Output Discipline, Tooling"
  category: "productivity"
---

# token-discipline

Context is the scarcest resource in this session. Every tool result, log line, and
repeated sentence is spent from the same budget that holds the actual work.

These rules target the agent's own output, not the reader's. Prose brevity is
handled by other rules; this file is about what gets *loaded*.

## 1. Filter at the source, with a hard cap

**Default cap: under ~30 lines of tool output per command.** Say the cap in the
command itself, so the intent is visible to the reader.

A command that prints 400 lines and a script that prints 8 cost the same to
*decide*, but not the same to *read*. Piping first is not optional when the raw
output exceeds the cap.

| Instead of | Use |
|---|---|
| `tail -50 log` | `grep -iE 'error\|401' log \| tail -8` |
| `cat file` | `head -40 file` or `sed -n '1,40p'` |
| full `gh issue view --json` | ~~`--jq '.state, .title'`~~ → `--jq '{state, title, labels}'` — never the whole payload |
| printing a diff | `diff --stat` first, full diff only if asked |

**Before running anything, ask: how many lines of this do I actually need?** If
the answer is not "a few", add the filter in the command. If you get more than
the cap anyway, do not print a second slice to "find" the relevant part — state
the one line that matters and drop the rest.

Printing 400–700 lines and then discussing a 5-line subset is the observed
failure this rule exists to stop. The full dump is never the evidence; the
5-line subset is.

## 2. Never re-quote what is already visible

The user can see the command output in the transcript. Restating it in prose — in
tables, bullets, or a "here's what we found" recap — spends tokens to tell them
something they just read. This has happened a dozen times in a single day.

- Tool output is evidence, not content. Do not summarize it back.
- Do not repeat a table that was already printed.
- Do not re-list file names after listing them.
- Do not turn a 5-line JSON payload into a 5-row markdown table.

**Say the conclusion. Point at the evidence by name, not by quotation.**

## 3. One conclusion, stated once — corrections follow the same rule

When a finding changes, state the new state. Do not narrate the revision.

- Bad: "Earlier I said X. Then it turned out Y. Now it's actually Z."
- Bad: "Let me correct my earlier statement about X, where I claimed..."
- Good: "It's Z. (Y was a misread of one log line.)"

The correction matters only if the user would otherwise act on the old version.
If the old value is wrong and matters, overwrite it in one clause; never
re-explain the full history. Reversing a conclusion three times, each time
re-walking the timeline, is the failure mode to avoid.

## 4. Distinguish verified from unverified, cheaply

One tag is enough. Do not hedge every sentence and do not build a table of it.

- `✅ verified` — tested, with the method named once
- `⚠️ unverified` — inferred, not tested

Everything else gets stated plainly, without a hedge word.

## 5. Read files once, in full, at the right size

Reading a file in 5 chunks costs 5 round-trips and 5 restatements. Read it once
with enough lines to understand it. If it is larger than the budget, read the
specific ranges that matter and say which ranges you skipped.

## 6. Batch independent checks into one round-trip

Four separate commands that each print 3 lines cost more in framing than in
content. A batch of single-point checks (`pgrep`, `stat`, `grep`) run as separate
round-trips costs one explanation each; the same checks in one script cost one
block. **This is the single highest-leverage rule in this file.**

- Combine into one script that prints one labeled block.
- Frame the result once, not once per check.
- "Let me also check..." followed by a lone command is the anti-pattern; add it
  to the batch instead.

## 7. Do not re-verify what was already verified

If a result is in the transcript, cite it. Re-running to "confirm" spends a
round-trip to learn nothing. Re-verify only when something changed, or when the
previous check was single-shot and the decision is irreversible.

## 8. Do not write findings to memory that only matter this turn

Memory files persist into every future session. A finding that is already acted
on — a resolved error, a workaround you used once, the state of a debugging step
you just finished — does not belong there. Write to memory only what the *next*
session needs.

Hard limit: a daily-memory entry should be readable in well under a minute. If it
is past a few hundred characters, most of it is turn-local. A 5000+ character
entry is a transcript, not a memory.

## Pre-send check

Delete before sending:

1. Any sentence that restates visible tool output.
2. Any table whose rows were already printed.
3. Any "let me verify" step on something already verified.
4. Any hedge on a claim that was actually tested.
5. Any re-telling of a corrected conclusion's history.

Then check: **would this reply be shorter if the reader had not seen the tool
output?** If yes, that content is the part to cut.
