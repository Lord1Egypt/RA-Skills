# Memory

Everything lives in the workspace, on this machine. The platform deletes message content after the plan's retention (1 hour by default), so `ingest` stores each message the moment it reads it.

## Layers, per customer

| Layer | File | What it holds |
|---|---|---|
| Transcript | `contacts/<number>/transcript.jsonl` | every line, append only; lines older than the retention in `memory-policy.json` (90 days by default) are purged |
| Window | derived | the newest lines that fit the budget, word for word |
| Summaries | `contacts/<number>/episodes/NNN.md` | older parts of the conversation, summarized |
| Card | `contacts/<number>/card.json` | stable facts with their source: `inferred`, `attendant` or `admin` (a person's note beats an inference) |
| State | `contacts/<number>/state.json` | `active`, `handoff`, `paused`, `do_not_contact`, language, counters |

## Summaries

When the uncompacted part of a conversation grows past `compaction_trigger_tokens`, `apply` queues a `compaction` item. Run it like any item:

1. `tn_assist next --kinds compaction`, then `tn_assist pack --item <id>`. The pack is the oldest part of one customer's conversation and an instruction.
2. Answer in a fresh context with no tools, as in [contact-turn.md](contact-turn.md). The answer is one JSON object: `{"summary": "<one paragraph>", "facts": [{"key": "...", "value": "..."}]}`.
3. `tn_assist apply --item <id> --decision-file <file>`. The summary is stored as the next episode and those lines leave the window.

The summary is one plain paragraph. It is shown to later turns as data, never as instructions.

## The policy

`memory-policy.json` holds the numbers (pack budgets, window, thresholds, retention, caps). A workspace that already has one keeps it: setup never overwrites it. You may suggest changes to the person you are talking to after you notice a pattern (answers cut for lack of room, the same question asked again, many escalations for one reason). `/politica` only shows the numbers: the person changes them by editing `memory-policy.json`. Never change the policy yourself.
