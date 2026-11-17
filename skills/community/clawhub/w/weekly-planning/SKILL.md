---
name: weekly-planning
description: 'Decide what the go-to-market team works on this week: every Monday last week''s work is ranked against active initiatives, declared infra, and live runs, as one reviewable pull request per initiative, or one workspace pull request when there are none. Triggers: "what should we work on this week", "are the bets we already have on track", "what should we do next this week", "rank our initiatives against what is actually running", "weekly GTM plan from the cadence log", "recommend next work from infra and runs", "the play is deployed but I don''t think it ran". Cargo project, defineAgent, harness claudeCode, GitHub, cargo-ai CLI reads, initiatives, cadence. Skip when: you want today recapped and posted to Slack, which is standup; or you want call transcripts scribed into context, which is call-capture.'
version: "0.2.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later, which binds a harness agent to the project's connected state, with `env` at the top level of `defineAgent`. Also needs a Cargo workspace, an authenticated LLM connector (the harness runs against Cargo's proxy, so the agent needs a `connector` and `languageModel` like any other), and a GTM repository with `cadence/` at its root (the shape `cargo-ai project init` scaffolds). `initiatives/` is optional: without it the run still opens one workspace pull request."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/weekly-planning
metadata:
  author: getcargo
  source: cookbook
  personas:
    - sales-leadership
    - revops
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Weekly planning

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

What to do next stops living in someone's head until the next planning meeting. Every Monday one
agent runs, and two things land:

1. **The raw dump.** A committed script writes last week's git commits, pull requests, initiative
   inventory, declared infra, and cadence files dated in that week into
   `cadence/log/raw/planning/<YYYY-Www>.md`. That is the evidence, and it is never edited by the
   agent.
2. **The recommendation file(s).** The agent reads the dump, the workspace (runs, usage, models,
   through read-only `cargo-ai` calls), and the initiative files, and writes markdown a human can merge:
   - **No active initiatives** — one file, `cadence/plan/YYYY-Www.md`, one pull request titled
     `[cadence] workspace YYYY-Www`. It checks what is happening: declared infra, live runs, usage.
   - **One or more active initiatives** — one file and one pull request **per** initiative, titled
     `[cadence] <slug> YYYY-Www`. Two bets do not share a diff.

Then it stops. A human merges. Recommendations are not a deploy: the agent does not edit `infra/`,
does not start a play, and does not merge itself.

This is a scheduled CI workflow plus a hosted agent, collapsed into resources declared in the same
project as everything else the workspace runs. The schedule and the repository binding live in
`infra/weekly-planning/agents/planner.ts`, and the instructions beside it in `planner.prompt.ts`.
`harness: "claudeCode"` is what buys the working tree: the output of a week is a diff across
markdown files, and only an agent with a checkout can produce one.

Three properties make it safe enough to run unattended:

- **The collection is deterministic.** The agent does not fetch PRs. `scripts/collect/week.ts`
  does, the same way every Monday, and the agent is told not to improvise that step. Workspace data
  (runs, usage, what is deployed) comes from named read-only `cargo-ai` commands at recap time, not
  from a second fetch inside the collector.
- **One pull request per initiative, or one for the workspace.** Combining five bets into one diff
  is how a reviewer merges the loud one and skips the overdue one. Splitting them is the gate.
- **The pull request is the gate.** The agent has repository write access and no other write path.
  It cannot email anyone, cannot touch the CRM, cannot run a `cargo-ai` command that spends or
  deploys, and cannot merge itself.

## Example

> Every Monday morning, check last week's runs against our initiatives and open one pull request per initiative saying what to do next.

Illustrative output, fictional records:

```text
[cadence] eu-outbound 2026-W41   ->  cadence/plan/2026-W41-eu-outbound.md
---
title: 2026-W41 EU outbound
description: Blocked. The sourcing play is declared but did not run once this week.
week: 2026-W41
target: eu-outbound
---
## The gap
Play is declared, no runs this week: source-eu-accounts shows 0 runs since Oct 2
(orchestration run list), while the initiative's deadline is Oct 31.
## Recommendations
- Dana: re-enable source-eu-accounts today and confirm one run succeeds by Wednesday.
- Dana: if it fails again, move the deadline in initiatives/eu-outbound.md this week.
```

Each active initiative gets its own verdict and at most three owned recommendations in its own pull
request, so the blocked bet cannot hide behind the one that is on track.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/weekly-planning` writes this example to `infra/weekly-planning/`
   (resources **and** `scripts/`) and this procedure to `.agents/skills/weekly-planning/`. No
   project yet? `cargo-ai project init <dir> --cookbook weekly-planning && cd <dir> && npm install` does
   both; this folder never ships a shell. **If you are reading this from the project's
   `.claude/skills/`, the install already happened — start at step 2.** On a CLI too old to have
   `add`, copy this folder in as a sibling of what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a GitHub connector or
   an agents folder, rewire the imports to the existing one and drop the copy; two resources with
   one slug is a collision at deploy. Append this folder's env needs to the project's `.env.example`;
   never overwrite it.
3. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted (nobody asks for a variant they do not know exists); _What you will be asked_ is
   the floor, and you derive before you ask. If you are asking more than about four questions you
   have skipped lookups. Record what you changed and why under a `## Decisions` section in your copy
   of this file.
4. **Run the collector by hand once, then plan.** `npx tsx
   scripts/weekly-planning/collect/week.ts --dry-run` first: it prints the dump and writes nothing.
   Then drop `--dry-run`. If it does not produce a raw file locally it will not produce one on a
   schedule, and that is far cheaper to find out now. Then
   `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root, show the diff, and
   deploy only on an explicit yes: `cargo-ai project deploy`. Never `cargo-ai project init --force` into a non-empty
   directory.
5. **Verify.** Walk _Done when_ line by line and report each with evidence. Deployed cleanly and
   produced nothing is the normal failure.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input                                              | Kind  | How it is answered                                                                                                                                                                                                                          | Why it matters                                                                                                                                                                                                                          |
| -------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project binding (`infra/agents/planner.ts`) | value | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox. | This is the working tree the harness clones and the only place its plan files can land. An `owner/name` written by hand is the one value nobody notices is wrong until a pull request opens against a stranger's repository.            |
| GitHub connector (`infra/connectors/git.ts`)       | value | **derived**: `cargo-ai connection connector list` shows whether one is authorized; if not, `cargo-ai project add connector/github` opens the OAuth consent. The declaration is `default: true` because a deploy cannot mint an OAuth grant.         | It is the agent's entire write path into the repository. Without it the run does the work and has nowhere to put it.                                                                                                                    |
| LLM connector and model (`infra/connectors/anthropic.ts`) | value | **derived**: `cargo-ai connection connector list` shows whether an Anthropic connector is authorized; if not, `cargo-ai project add connector/anthropic` takes the key. `default: true` because a deploy cannot mint one. Any Anthropic model pairs with `claudeCode`; the agent's `languageModel` is a placeholder to set. | A harness does not bring its own model — it runs against Cargo's LLM proxy, so this is what the Monday run is billed and metered against. Omit either and `defineAgent` throws at `plan`; pair `claudeCode` with an `openAi` connector and it typechecks green and fails at deploy. |
| `PLANNING_TIMEZONE` (`infra/agents/planner.ts`)    | value | **derived**: default `America/Los_Angeles`. Change it only if the team's week is not Pacific. Change it together with `cron`.                                                                                                                 | The previous ISO week is computed in this timezone. A timezone the collector does not share with the prompt splits the dump and the plan files across two weeks.                                                                      |
| cadence and initiatives paths                      | value | **derived**: read `cadence/README.md` and `ls initiatives/` for what already exists                                                                                                                                                           | The agent writes into a layer humans already curate. A second parallel folder splits the record in half. An empty `initiatives/` is not an error: it is the one-workspace-PR path.                                                      |

Checked before moving on, not after the deploy:

- the collector was run by hand once and wrote a real raw file
- `cargo-ai project check` prints `agent:weekly_planning bound to <your repo>#<branch>` with no trailing
  subdirectory — the repo is the one holding `cadence/`, and the GitHub grant can push to it. A
  trailing `in infra/` is the failure to catch here: it roots the harness where there is no
  node_modules, so the collector cannot run
- `scripts/weekly-planning/package.json` is present in the project after the install
- `cargo-ai whoami` names the workspace this recap should read. That is the prompt's first
  command, and the first scheduled run is what proves the harness sandbox carries a session of
  its own; if it does not, every pull request says so and the recap lands from the dump
- `node --import tsx evals/contract.mjs` passes

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the
default.

| Variation        | When it is right                                                                                         | How                                                                                                                                                         | What it costs                                                                                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `move-the-hour`  | The team reads pull requests at a different time, or you are not on Pacific time                         | Change `cron` and `PLANNING_TIMEZONE` together in `infra/agents/planner.ts`. The cron is 15:00 UTC Monday because that is 8am PT in PDT.                    | A Sunday cron recaps an incomplete week. A timezone the collector does not share with the prompt splits the dump and the plan files across two weeks.                  |
| `skip-on-track`  | An on-track initiative should not ping the reviewer                                                      | In `infra/agents/planner.prompt.ts`, skip the pull request when The gap is "on track"                                                                       | Silence on an on-track week is indistinguishable from a missed run for that initiative. The default still opens the PR, because a written "keep going" is the record.  |
| `git-only`       | The sandbox has no Cargo session, or this agent must not reach the workspace at all                      | Drop §1b of `infra/agents/planner.prompt.ts`                                                                                                                | "Deployed is not running" stops being answerable, which is most of the point: the gap collapses to what git can see. The dump still lands, which is what §1b already falls back to when `cargo-ai whoami` fails. |
| `one-pr`         | You want one weekly diff even when there are five initiatives                                            | Collapse step 2 of `infra/agents/planner.prompt.ts` to a single pull request that holds every plan file                                                     | The reviewer merges the loud initiative and skips the overdue one. The default splits them because that is the gate.                                                   |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The agent does not fetch git; the script does.** (`scripts/collect/week.ts`) A fetch loop an
  agent re-derives every Monday is a fetch loop that silently changes shape — a window that drifts, a
  `gh` flag that quietly widens. The raw dump is the one thing here that has to be byte-identical in
  its rules every week, because everything downstream is diffed against it. Cargo workspace data is
  the other half of the week, and it is read at recap time by the agent, not by a `cargo-ai` loop
  bolted into the collector.
- **Zero active initiatives is one workspace pull request. N active is N pull requests, plus
  one `unplanned` only when work outside them is significant.** (`infra/agents/planner.prompt.ts`)
  Combining them is how a reviewer merges one bet and skips another. Opening a workspace pull
  request *and* the initiative ones gives routine unclaimed runs a second home they were not asked
  to have: they stay in the dump. The `unplanned` pull request is the exception, and its bar is
  concrete (more credits than any initiative, a play failing one run in five, a customer or
  revenue event no initiative claims). Drop it and an unplanned play can burn the week's credits
  without ever reaching a reviewer.
- **The workspace reads are read-only, and they are the CLI.** (`infra/agents/planner.prompt.ts`)
  §1b names the commands: `whoami`, what is deployed, run counts and failures, usage. No
  `capabilities` block is wired on the agent, because the read path is already in the sandbox and
  only the prompt can say "read, never execute". `orchestration action execute`, `batch create`,
  `cargo-ai project deploy` and anything that removes are the forbidden half of that list — a planner that can
  start a batch is a planner that can spend, and a recommendation is not a deploy. If
  `cargo-ai whoami` fails, every pull request says so and the recap continues from the git dump; it
  does not invent the numbers.
- **`scripts/weekly-planning/package.json` stays.** (`scripts/package.json`) It is not decoration.
  The loader imports only the resources folder `cargo.json` names, but in a project whose
  `cargo.json` names its root it imports every `.ts` there except directories carrying a
  `package.json`; delete it and `cargo-ai project plan` imports the collector and runs git/`gh` on every
  plan.
- **The harness root stays the directory holding the `package.json` that declares `@cargo-ai/cdk`.**
  (`infra/agents/planner.ts`) That is where `node_modules` is, so it is the only place
  `npx tsx …/collect/week.ts` resolves — and in the scaffolded layout it is the repository root,
  which is also where `cadence/` and `initiatives/` live. The harness clones the project's
  connected state at that state's directory, so the state must be connected at the directory
  holding that `package.json`. **Check it, do not assume it:** `cargo-ai project check` prints the
  binding. A state connected at a subdirectory with no package.json leaves the collector unable
  to run, and Monday reports clean and empty; an unconnected state deploys the agent unbound.
- **The agent opens pull requests and never merges them.** (`infra/agents/planner.prompt.ts`) The
  recommendation is what next week's work is chosen from. Remove the review gate and a hallucinated
  gap, a play misread as idle, or a stuck item filed against the wrong owner becomes the team's
  next bet.
- **Every file opens with a verdict, in a founder's words.** (`infra/agents/planner.prompt.ts`)
  On track, Behind, At risk or Blocked, then why, then at most three recommendations each with
  an owner and a day. Without the verdict a reviewer has to read the whole file to learn whether
  the bet is in trouble, and a plan nobody finishes reading is one nobody acts on.
- **Do not invent a number.** (`infra/agents/planner.prompt.ts`) Drop a metrics line rather than
  carry last week's ARR forward. A made-up delta is worse than no delta, because the plan file is
  what leadership reads. A CLI read that errors is a note on the PR, not a count you fill in.
- **Never edit `plan/` or `infra/`.** (`infra/agents/planner.prompt.ts`) The planner recommends. A
  pull request that rewires a play is a deploy wearing a plan file's name.

## Done when

- `--dry-run` printed the dump for the previous ISO week, and the run without it wrote
  `cadence/log/raw/planning/<YYYY-Www>.md`; running it twice that Monday overwrote the same file
- `node --import tsx evals/contract.mjs` passes: harness is `claudeCode` bound to an Anthropic
  connector and a model, no capability is wired on the agent, there is no Slack action, and no
  tool wraps git or the CLI
- `cargo-ai project plan` reports the agent, the GitHub and Anthropic connectors and the folder, and
  does **not** run git or `gh` while planning
- with **zero** active initiatives, the first scheduled run opened exactly one unmerged pull
  request titled `[cadence] workspace <YYYY-Www>` whose diff contains the dump and
  `cadence/plan/<YYYY-Www>.md` with `## Recommendations`
- with **N** active initiatives, it opened exactly N unmerged pull requests, one per slug, each
  diff containing the dump and exactly one `cadence/plan/<YYYY-Www>-<slug>.md` — never a second
  initiative in the same diff — plus one `[cadence] unplanned <YYYY-Www>` pull request only when
  work no initiative claims met the bar in the prompt
- every plan file's `description` and PR body open with the same verdict (On track, Behind, At
  risk, Blocked, Unplanned, or No active initiatives), and every recommendation names an action and a day
- a re-run the same Monday opened no additional pull request for a target whose
  `## Recommendations` section was already on disk
- no number in a plan file is absent from the raw dump, a metrics file dated that week, or a
  `cargo-ai` read the agent actually ran. A CLI read that errors is a note on the PR, not a
  made-up count

## What it costs

The collector talks to git and, when `gh` is installed, to GitHub from the harness environment.
Those calls are not Cargo connector actions.

The recurring cost is the harness run itself, once a week, billed as LLM tokens through the bound
Anthropic connector, and it scales with how much the agent reads — the dump, the week's cadence
files, the active initiative files, declared infra, and the read-only `cargo-ai` calls in §1b
(whoami, what is deployed, run counts, usage). Those reads are API calls, not connector actions, so
they bill nothing. There is no per-record fan-out, and the recap never runs a command that spends.

## Composes into

Nothing in particular comes after it: the plan it opens is the next week's work.
