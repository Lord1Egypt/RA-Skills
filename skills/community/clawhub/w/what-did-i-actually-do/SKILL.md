---
name: what-did-i-actually-do
description: "What do I believe I did, and what did I actually do? Did the things I told the user really happen? Use this before reporting a task as done, after a long session, and whenever you are about to say 'sent', 'published', 'fixed', 'installed' or 'verified'. Reads your own session transcript for success claims and checks each against the record: tool outcomes, outbound sends and their delivery, POST/PUT status codes on the wire. Lists every claim as SUPPORTED, UNSUPPORTED or CONTRADICTED and names failed actions you never mentioned. Returns exactly RECORD_MATCHES_CLAIMS, CLAIMS_EXCEED_RECORD, RECORD_EXCEEDS_CLAIMS or NO_CLAIMS. Do not use before any action has been taken."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# What did I actually do?

What you told the user is in the transcript. What happened is in the ledger:
tool outcomes, sends and their delivery, status codes on the wire. This skill
reads both and lines them up, claim by claim.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Before reporting a task as done, call the `clawphylax_reconcile` tool, or
   `/phylax reconcile`, or:

   ```bash
   openclaw clawphylax reconcile
   ```

3. Act on the verdict:
   - **RECORD_MATCHES_CLAIMS** — every success claim has evidence, nothing contradicted,
     no unmentioned failures. Report as is.
   - **CLAIMS_EXCEED_RECORD** — at least one claim is contradicted by the record (the send
     failed, the POST got a 4xx, the last action before "done" failed) or too many have no
     evidence. Correct what you told the user before doing anything else.
   - **RECORD_EXCEEDS_CLAIMS** — claims hold, but failed actions never appeared in what you
     said. Say what failed.
   - **NO_CLAIMS** — no success claims in the transcript yet.

## How claims are checked

- "sent / delivered / notified" → an outbound send before the sentence and its delivery
  verdict (runtime result × channel API status).
- "published / posted / uploaded / deployed / pushed" → a POST/PUT/PATCH on the wire with
  its status; an exec alone counts as unverified.
- "created / saved / fixed / installed / scheduled" → a successful write/edit/exec/cron.
- "verified / confirmed" → a check, read or fetch after the action.
- "done / completed" → the last action before the sentence did not fail.

Sentences that themselves report a failure are not counted as claims.

## Use this when

Before "done"; before any sentence with sent / published / fixed / installed / verified; after long or compacted sessions; when the user doubts a result.

## Do not use when

Before any action has been taken; sessions without a transcript under the OpenClaw state directory.

## Output

First line `ACTION: REPORT_AS_IS` / `ACTION: CORRECT_WHAT_YOU_SAID` / `ACTION: MENTION_THE_FAILURES`, then EVIDENCE (claims supported / unsupported / contradicted, unmentioned failures), DO NOT, NEXT, SCOPE, then the claim list with time, status, kind, sentence and evidence. Correct any CONTRADICTED claim to the user before doing anything else.

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
