---
name: why-do-i-keep-failing
description: "Why do I keep failing? What is the pattern behind my errors? Use this when errors pile up — three or more failed tool calls (exec, write, web_fetch, API) in a session — before retrying anything. Clusters this session's failed tool calls and failed requests by tool, host and error signature, names the single cause behind most of them with its share, and returns a compact trail of the last failures to reason about. Returns FIX_DOMINANT_CAUSE, HOLD_APPROACH_VARY_ONE_INPUT or NO_TOOL_FAILURES. Do not use for a single failure — use why-did-my-request-fail for a failing host."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Why do I keep failing?

Errors that pile up usually have one or two causes, not ten. Cluster them
before touching anything else.

## Steps

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
Check with `openclaw clawphylax status`.
2. Ask for the clusters — the `clawphylax_failures` tool, `/phylax failures`, or:

   ```bash
   openclaw clawphylax failures --window 120
   ```

3. Read the first line: if one cluster explains ≥ 50 % of failures, fix that
   cause and nothing else. If a host is named, ask the outlook for it
   (`why-did-my-request-fail`) to learn whether it is the host or your request.
4. Use the trail (last failures, oldest first: time, tool, argument hint,
   error) to reason: what did the failing arguments have in common? What
   changed right before the first failure?
5. Report to the user in one line: the dominant cause, its share, what you
   will change. Do not list every error.

## Limits

Only tool calls and in-process requests are recorded; a failure inside a
child process shows up as the exec tool's error text.

## Use this when

Three or more failures in a session; the same error keeps returning; before yet another retry.

## Do not use when

A single failure (use `why-did-my-request-fail` if it was a request). Failures the user already explained.

## Output

First line `ACTION: FIX_DOMINANT_CAUSE` (with the cause and its share) / `ACTION: HOLD_APPROACH_VARY_ONE_INPUT` / `ACTION: NO_TOOL_FAILURES`, then the clusters (tool, host, signature, count), then the trail (time, tool, hint, error). Report one cause to the user, not every error.

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
