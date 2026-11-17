# Weekly planning: decide what the go-to-market team works on this week

To decide what to work on this week, rank last week's go-to-market work against your active
initiatives and against what is declared and actually running. Every Monday this cookbook's Claude
Code harness agent does that ranking and delivers it as one reviewable pull request per initiative,
or one workspace pull request when there are none.

```sh
cargo-ai project add cookbook/weekly-planning
```

## What it does

- **Collects.** `scripts/collect/week.ts` dumps the previous ISO week's git
  commits, pull requests, initiative inventory, declared infra, and cadence
  files dated in that week into `cadence/log/raw/planning/`. Deterministic, no
  LLM anywhere near it.
- **Reads the workspace.** The agent runs read-only `cargo-ai` commands (what is
  deployed, runs, usage). No capability is wired on it. If `cargo-ai whoami`
  fails, it notes that on every pull request and continues from the dump.
- **Recommends.** Zero active initiatives: one file, `cadence/plan/<week>.md`.
  N active: one file per initiative, `cadence/plan/<week>-<slug>.md`.
- **Stops.** One unmerged pull request per file. Never a deploy. Never a Slack
  post — standup already owns the daily channel.

## How it works

1. **The cron trigger fires** at 15:00 UTC Monday (8am PT during PDT), after
   Sunday's standup has landed.
2. **The agent clones the repository** — the project's own, resolved from the
   checkout's git origin at deploy rather than written down.
3. **It runs the collector** — `npx tsx scripts/weekly-planning/collect/week.ts`
   — which reads `PLANNING_TIMEZONE` from the harness environment. The agent is
   told not to fetch the week itself.
4. **It reads the workspace** with Cargo's own CLI, which the checkout already
   has: `whoami`, what is deployed, last week's run counts and failures, usage.
5. **It writes the plan file(s)** and opens the pull requests from step 2 of
   the prompt: one per active initiative, or one workspace pull request.
6. **A human merges.** The agent never does.

Adds 4 resources plus a script bundle.

| File                               | Resource                     | Role                                                              |
| ---------------------------------- | ---------------------------- | ----------------------------------------------------------------- |
| `infra/agents/planner.ts`          | `defineAgent` (claudeCode)   | schedule, repository binding, env                                 |
| `infra/agents/planner.prompt.ts`   | (not a resource)             | the recap contract: window, one-PR-per-initiative rule, limits    |
| `infra/connectors/git.ts`          | `defineConnector` (`github`) | the clone, branch, push and PR path, resolved by binding          |
| `infra/connectors/anthropic.ts`    | `defineConnector` (`anthropic`) | the model the harness runs on, billed and metered              |
| `infra/folders/index.ts`           | `defineFolder`               | the workspace folder this pipeline's resources are filed in       |
| `scripts/collect/week.ts`          | (not a resource)             | the entrypoint: dump git / `gh` / initiatives / infra for the week |

## The two halves, and where they land

This pipeline has one directory per layer it touches, and the install mirrors
each into its namesake in the project:

```
weekly-planning/infra/     ->  infra/weekly-planning/      what is declared and deployed
weekly-planning/scripts/   ->  scripts/weekly-planning/    what the agent runs
```

Those are the layers `cargo-ai project init` already scaffolds — `infra/` holds
the resources `cargo.json` names, `scripts/` is imperative glue for runtime
surfaces a project cannot declare yet — so a pipeline that needs both
contributes to both under its own name rather than inventing a third place.

`scripts/package.json` is belt and braces. The loader imports only the
resources folder `cargo.json` names (`infra/` in a scaffolded project), so
nothing under `scripts/` is ever imported as a resource. In a project whose
`cargo.json` names the repo root instead, the loader imports every `.ts` it
finds **except** directories carrying a `package.json` — without that file,
`cargo-ai project plan` would import the collector and run git/`gh` on every plan.

## Why the split

The collection and the judgement are different jobs, and the failure modes for
mixing them are not symmetric.

A fetch loop an agent re-derives every Monday is a fetch loop that silently
changes shape: a window that drifts, a `gh` flag that quietly widens. Nothing
downstream can tell, because the dump is what everything downstream is diffed
against. So the fetch is a committed script and the agent is told not to
improvise it.

The recommendation is the opposite. It is judgement — which initiative is idle,
whether a declared play ran, who owns the next step — and it produces one diff
per bet. That is what `harness: "claudeCode"` buys: a working tree, the git
history to read before writing, and a pull request. It does not buy its own
model: the harness runs against Cargo's LLM proxy, so `connector` and
`languageModel` are required here exactly as they are on a `streamText` agent,
and they are what the run is billed and metered against.

## Why one pull request per initiative

A single weekly diff with five initiatives in it is how the loud bet gets
merged and the overdue one rides along unread. Split them, and a reviewer
can merge one and send another back.

Zero active initiatives is the empty-queue case that still has something to
say: the workspace, the infra, the runs. That is one pull request, not zero,
because a quiet repo with plays that ran (or did not) is still a finding.

Unclaimed runs — a play no active initiative names — stay in the dump. They
are not a sixth pull request. Mention them in an initiative file only when they
compete with that initiative.

## Placeholders (edit before deploy)

1. **`PLANNING_TIMEZONE`** — `infra/agents/planner.ts`: IANA timezone the
   previous ISO week is computed in. Change it together with `cron`.
2. **`languageModel`** — same file: any Anthropic model the workspace's
   connector can reach. `claudeCode` pairs with the `anthropic` integration and
   nothing else.

## What it does not do

It does not contact customers, write to a CRM, merge its own pull request, run
a CLI command that spends or deploys, edit or delete a raw dump or an
existing recommendation file, promote first-occurrence claims into `context/`,
or touch `plan/` and `infra/`. It recommends the week; it does not change the
strategy or the deployed engine. It does not post to Slack — that is standup.
