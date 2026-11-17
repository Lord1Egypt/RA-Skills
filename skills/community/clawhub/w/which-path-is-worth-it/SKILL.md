---
name: which-path-is-worth-it
description: "Which path is worth it? Which research or action path should I try next under incomplete information? Use this when choosing between two or more approaches, planning research, deciding where to spend a limited budget, or when the user asks which option to pursue. Given each path's successes, failures, prior, cost per attempt and value on success, computes success probability with bounds, expected value, safe value (lower bound) and optimistic value (upper bound). Returns exactly EXPLOIT, EXPLORE or FOLD per path with a plan; hostnames pull their outcomes from the ledger. Do not use with a single option — then use should-i-stop-and-ask."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Which path is worth it?

Choosing among approaches under incomplete information is a bandit problem,
and the poker rule applies: never fold on a point estimate, and pay for
information only where the upside is wide.

## Steps

1. List the candidate paths. For each, write down what you know:
   `successes`, `failures` (0 if untried), a `prior` (0.5 if no idea),
   `costPerAttempt` and `valueIfSuccess` in the same unit (tokens, minutes,
   or euros — it only needs to be consistent). Paths that are hostnames need
   no counts; the ledger supplies them.

2. Ask — the `clawphylax_which_path` tool, `/phylax paths <json>`, or:

   ```bash
   openclaw clawphylax paths '[{"name":"official-api","successes":3,"failures":1,"costPerAttempt":1,"valueIfSuccess":10},{"name":"scrape-site","costPerAttempt":2,"valueIfSuccess":10}]' --budget 12
   ```

3. Read the verdict per path:
   - **exploit** — run it; it already guarantees value at the lower bound.
   - **explore** — one or two attempts buy the most information per cost.
   - **fold** — cannot pay even in the best case; drop it and say why.
   - **hold** — neither; revisit after the explore result.

4. Follow the plan lines. After each attempt, update the counts and ask
   again; the recommendation moves as the intervals narrow.

5. Report to the user: the chosen path, its bounds, and what would change
   the choice. Numbers, not adjectives.

## Limits

The model assumes attempts are independent and payoffs constant. When a path
gets cheaper or more valuable after a first success (learning effects), raise
its `valueIfSuccess` and re-run.

## Use this when

Two or more candidate approaches; research planning; budget allocation; "which option should I pursue?".

## Do not use when

A single option (use `should-i-stop-and-ask`). Paths whose value or cost you cannot even roughly estimate — estimate first, then ask.

## Output

First line `ACTION: EXPLOIT <path>` / `ACTION: EXPLORE <path>` / `ACTION: ALL_FOLD`, then per path: P with bounds, n, EV per attempt, safe and optimistic value, its verdict; then the plan lines. Re-run after each attempt with updated counts.

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
