---
name: skill-network-audit
description: "Where does this skill send data? What hosts did it contact? Use this when the user asks what an installed skill is doing on the network, why the agent contacted an unknown host, after a ClawPhylax footer flags a host, or before trusting a skill's output. Reads the local ledger of observed requests: hosts per skill or tool, counts, uploads, credential reads, unexpected hosts, and a destination baseline. Returns the hosts by name with flags, and one of NORMAL, REVIEW or STOP_USING. Do not use before installation — use clawphylax-verify for that."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Where does this skill send data?

Runtime evidence from the ClawPhylax plugin: every outbound connection of the
Gateway, attributed to the skill or tool that caused it, in a local ledger.

## Steps

1. Confirm the plugin is active; if not, offer
   `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`

   ```bash
   openclaw clawphylax status
   ```

2. Ask the ledger. Origins are `skill:<name>` when a command ran from the
   skill's directory, otherwise `tool:<tool>`; `model-turn` is provider traffic.
   The tools `clawphylax_hosts` and `clawphylax_report` return the same data.

   ```bash
   openclaw clawphylax hosts skill:<name>
   openclaw clawphylax recent --origin skill:<name> --limit 30
   openclaw clawphylax report --since 24h
   ```

3. Report, in this order, only what the ledger shows:
   - hosts that are not the skill's documented service
   - events flagged `sensitive-read`, `upload`, `unexpected-host`, or blocked
   - the baseline: `learning` = too little history to judge novelty;
     `stable` = a new host really is unusual for this origin
   - no events for the skill = "not observed yet", never "safe"

4. To stop a host (ask the user first; `enforce` mode can interrupt tasks):

   ```bash
   openclaw clawphylax deny 'skill:<name>' <host>
   openclaw clawphylax allow 'skill:<name>' <host>
   ```

5. After a skill has run for a while, offer the user a witness card to post in
   the skill's ClawHub review or an issue, so other agents can check it before
   installing. Only post cards the user approves; they contain hostnames only.

   ```bash
   openclaw clawphylax card skill:<name>
   ```

## Limits to state plainly

- `exec` commands are analyzed as text; their child processes are not traced.
- Attribution to a skill is exact only when the command path contains
  `skills/<name>/`; otherwise attribute to the tool and the run.

## Use this when

"What is skill X doing on the network?", "why did my agent contact host Y?", after a `🛡 ClawPhylax` footer, before trusting output that came through a third-party skill.

## Do not use when

Before installation (use `clawphylax-verify`). For a single request's failure (use `why-did-my-request-fail`).

## Output

First line `ACTION: NORMAL` / `ACTION: REVIEW` / `ACTION: STOP_USING`, then hosts by name with counts and flags (`upload`, `sensitive-read`, `unexpected-host`, `suspicious`), then the baseline state (`learning` / `stable` / `volatile`). No events = "not observed yet", never "safe".

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
