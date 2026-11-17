# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- The collector was run by hand once (`PLANNING_TIMEZONE=America/Los_Angeles npx tsx
  scripts/weekly-planning/collect/week.ts --dry-run`) and printed a dump for the
  previous ISO week in that timezone, then the run without `--dry-run` wrote
  `cadence/log/raw/planning/<YYYY-Www>.md`.
- Running it a second time that same Monday overwrote the same file, not a
  second one. The dump is a snapshot of the week, not an append-only archive of
  runs.
- `scripts/weekly-planning/package.json` exists in the project, and
  `cargo-ai project plan` did not run git or `gh` while planning. If it did, that
  file is missing and the loader is importing the collector.
- `cargo-ai project check` prints `agent:weekly_planning bound to <your repo>#<branch>`
  with no trailing subdirectory. The repo is the one holding `cadence/`, and
  the GitHub grant can push to it. A trailing `in infra/` means the harness was
  rooted where there is no node_modules, so the collector cannot run.
- `cargo-ai connection connector list` shows an authorized Anthropic connector,
  and `languageModel` in `infra/agents/planner.ts` names a model it can reach.
  The harness runs against Cargo's proxy, so a missing one throws at `plan`.
- `cargo-ai whoami` names the workspace this recap should read. It is §1b's
  first command; whether the harness sandbox carries a session of its own is
  what the first scheduled run establishes, and the PRs say so either way.
- `node --import tsx evals/contract.mjs` passes against the adapted graph:
  harness is `claudeCode` bound to an Anthropic connector and a model, no
  capability is wired on the agent, there is no Slack action.
- The cadence and initiatives paths in the system prompt match what
  `cadence/README.md` describes, or the new folders are introduced
  deliberately and that README is updated to name them.

## First scheduled run

- **Zero active initiatives:** exactly one pull request, unmerged, titled
  `[cadence] workspace <YYYY-Www>`. The diff contains
  `cadence/log/raw/planning/<YYYY-Www>.md` and `cadence/plan/<YYYY-Www>.md`
  with `## Recommendations`.
- **N active initiatives:** exactly N pull requests, unmerged, each titled
  `[cadence] <slug> <YYYY-Www>`. Each diff contains the dump and exactly one
  `cadence/plan/<YYYY-Www>-<slug>.md`. No pull request holds two initiatives.
- No raw dump was deleted. An existing plan file written by another week is
  still there.
- Re-running the agent the same Monday opens no additional pull request for a
  target whose `## Recommendations` section is already on disk.
- A quiet week still produced the pull request(s), rather than skipping the
  run.
- No number, account, or quote in a plan file is absent from the raw dump,
  the cadence files, or a `cargo-ai` read the agent actually ran.
  Spot-check two bullets against the dump. A CLI read that errors is a note
  on the PR, not a made-up count.

## Isolation

- This is one root skill. Its supporting Markdown files live under `references/`,
  and no nested `SKILL.md` exists.
- Recommendations land as pull requests. No Slack token, no `chat.postMessage`
  script, no GitHub Action, no `execute_action`.
- `evals/contract.mjs` still passes after adaptation: harness is `claudeCode`
  bound to an Anthropic connector, no capability is wired on the agent, there
  is no Slack action, and no tool wraps git or the CLI.
- The `cargo-ai` calls in the run's transcript were read-only (whoami, play
  and agent list, run count / list, usage). No `orchestration action execute`,
  no `batch create`, no `cargo-ai project deploy`. If `whoami` failed, each PR says so and
  the recap continued from the git dump.
