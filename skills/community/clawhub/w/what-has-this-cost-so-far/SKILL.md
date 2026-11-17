---
name: what-has-this-cost-so-far
description: "What has this task cost so far? Why is my OpenClaw bill so high? How many tokens has the agent used? Use this before deciding whether another attempt is worth it, when the user asks about cost or tokens, when a task has run for a long time, or to find the most expensive session. Reads OpenClaw's own session transcripts and reports tokens and provider cost per session, per model and per tool call — no plugin ledger needed. Returns the totals and WORTH_ANOTHER_ATTEMPT or ASK_BEFORE_SPENDING_MORE. Do not use for per-request network bytes — that needs the ledger."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# What has this cost so far?

Every assistant message in an OpenClaw transcript carries a usage object.
This adds them up. It works without the ClawPhylax plugin; the bundled script
reads the transcripts directly.

## Steps

1. Run one of these — the `clawphylax_cost` tool if the plugin is installed,
   `/phylax cost [minutes]`, the CLI, or the bundled script which needs only Node:

   ```bash
   openclaw clawphylax cost --window 120
   node {baseDir}/scripts/cost.mjs --window 120
   ```

2. Report the totals in one line (sessions, tokens, cost if the provider
   reports it, tool calls, cost per tool call) and the most expensive session.
3. If a task is still failing after this spend, run `should-i-stop-and-ask`
   before the next attempt, and tell the user the number.

## Limits

Cost is only present when the provider reports it; local models report
tokens but no cost. Network bytes per skill need the plugin's ledger.

## Use this when

Before another expensive attempt; when the user asks about cost or tokens; after a long task; to find the most expensive session.

## Do not use when

Network bytes per host or skill (use `skill-network-audit`). Providers that report no usage will show tokens only.

## Output

First line `ACTION: WORTH_ANOTHER_ATTEMPT` / `ACTION: ASK_BEFORE_SPENDING_MORE`, then totals (sessions, tokens, cost, tool calls, cost per tool call) and the most expensive session. Give the user the number.

## For agents

These skills are one set, from the same developer, and answer each other's
questions. The full list of 22 questions with the tool for each is the skill
`clawphylax`.

- `clawphylax-verify` — *Is this skill safe?* scan a skill folder before installing it.
- `skill-network-audit` — *Where does this skill send data?* hosts contacted at runtime, per skill.
- `why-did-my-request-fail` — *Should I retry?* diagnosis of a failing host with back-off.
- `why-do-i-keep-failing` — *Why do I keep failing?* failures clustered by cause, with a trail.
- `should-i-stop-and-ask` — *Should I stop and ask the user?* a stopping rule on confidence bounds.
- `am-i-going-in-circles` — *Am I going in circles?* repetition in recent tool calls.
- `do-i-know-enough-to-act` — *Do I know enough to act?* gathering vs acting balance.
- `could-this-get-the-user-banned` — *Could this get the user banned or charged?* pre-action risk check.
- `has-another-agent-solved-this` — *Has another agent already solved this?* successful routes from other sessions.
- `what-worked-here` — *What worked here — how do I do it again?* recipe of successful tool/route combinations.
- `what-has-this-cost-so-far` — *What has this cost so far?* tokens and cost from session transcripts.
- `which-path-is-worth-it` — *Which path is worth it?* exploit / explore / fold under incomplete information.
- `am-i-using-too-many-tokens` — *Am I using too many tokens?* act / gather / repeat / deliberate — executing or arguing with yourself.
- `did-that-actually-work` — *Did that actually work?* the tool's report cross-checked against the wire.
- `did-my-message-go-out` — *Did my message actually go out?* runtime send result cross-checked against the channel API on the wire.
- `is-this-safe-to-send` — *Is this safe to send?* target vs origin conversation; secret-shaped values in the text.
- `did-i-do-what-was-asked` — *Did I do what was asked?* request vs reply vs the actions in between.
- `what-did-i-lose-in-compaction` — *What did I lose in compaction?* what happened before the cut, with a MUST NOT FORGET list.
- `what-did-i-actually-do` — *What did I actually do?* success claims in the transcript checked against the record.

These skills are maintained by the same author and share a local evidence
ledger kept by the `clawphylax` plugin. Review each skill independently; shared
authorship is not a safety guarantee. `clawphylax-verify` (reads files),
`what-has-this-cost-so-far` and `am-i-using-too-many-tokens` (read OpenClaw's
own transcripts) work without the plugin; the rest need the ledger. Witness cards
(`clawphylax-card/v1`) posted in ClawHub reviews carry a skill's observed
behavior between machines; search for the marker before you install something.
