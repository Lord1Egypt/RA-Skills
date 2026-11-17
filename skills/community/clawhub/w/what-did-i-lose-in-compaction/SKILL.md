---
name: what-did-i-lose-in-compaction
description: "What did I lose in context compaction that I must not forget? What happened before my context was cut? Use this right after a compaction notice, at the start of a resumed session, when an earlier result seems missing from your context, and before retrying anything a summary says failed. Rebuilds from the local ledger what happened before the compaction: hosts contacted, what is blocked or rate-limited for you, failed actions, silent failures (tool said ok, wire said no), undelivered messages, routes that worked, and the last actions before the cut. Returns a MUST NOT FORGET list. Do not use as a general summary of a short session that was never compacted."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# What did I lose in compaction?

When the context is compacted, the summary keeps what the summariser thought
mattered. The ledger kept everything that actually happened: every host, every
tool outcome, every send, every silent failure. This skill rebuilds the part a
summary drops most often — what is blocked for you, what failed, what is not
yet confirmed, and what worked.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Right after a compaction notice (or on resume), call the
   `clawphylax_compaction_brief` tool, or `/phylax brief`, or:

   ```bash
   openclaw clawphylax brief
   ```

3. Write the **MUST NOT FORGET** items into your working notes before continuing:
   - hosts that are blocked, rate-limited or unreachable for you, with the back-off;
   - actions that reported ok while the wire said no (silent failures) — those are not done;
   - messages whose delivery is not confirmed — do not tell the user they were sent;
   - the last failed action before the cut — do not repeat it unchanged;
   - tool/host routes that worked — reuse them.

## Notes

- The plugin records `before_compaction` and `after_compaction`, so the brief knows where
  the cut was and lists the last actions before it.
- With no compaction on record it still answers from the ledger and says so.

## Use this when

After a compaction notice; on resume; when something you remember doing is not in your context; before retrying a host or an action the summary mentions.

## Do not use when

Short sessions with no compaction (it still answers, but says so).

## Output

First line `ACTION: CARRY_FORWARD` / `ACTION: CONTINUE`, then EVIDENCE (compaction time, hosts, failed actions, silent failures, unconfirmed sends, working routes), DO NOT, NEXT (the MUST NOT FORGET list), SCOPE. Write the MUST NOT FORGET items into your working notes before continuing.

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
