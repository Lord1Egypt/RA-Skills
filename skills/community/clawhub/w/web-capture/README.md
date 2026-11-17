# Web capture: keep your company context current from your website and competitors

To keep your positioning, ICP and competitor notes current, read your own site,
your competitors' pages and recent news about both every week, and let git show
what changed. This cookbook runs one Claude Code harness agent each Monday and
lands the result in `context/` as one pull request: the first run seeds the
files, and every later run adds a dated note of what changed and never edits an
existing file.

```sh
cargo-ai project add cookbook/web-capture
```

## What it does

- **Reads the web, the same way every week.** Two `cargo-ai` commands generated in the prompt: one
  `parallel.extract` with `fullContent` over the company's own pages and each competitor's watched
  pages, and one `parallel.createTask` news question about all of them for the days since the last
  merged read. A fixed `node -e` line writes each page to `cadence/log/raw/web/pages/<page>.md` or
  `cadence/log/raw/web/competitors/<competitor>/<page>.md`, and the news to
  `cadence/log/raw/web/news/<date>.json`. No text passes through the agent on its way to disk.
- **Lets git say what changed.** `git diff` against the default branch shows which pages changed;
  a news URL not in an earlier file is new.
- **Seeds once.** The first run fills every empty `context/` domain: `global/`, `icp/` with a
  disqualifier, `alternative/`, `client/`, `proof/`, `signal/`. Every sentence tagged `[R]`, `[I]`
  or `[TR]`.
- **Adds what changed.** Every run after writes one dated `insight/<date>-web.md`, each line naming
  its company, plus a file for a newly named customer or competitor. It never edits a file that
  exists; a change to one is a proposal in the pull request body.
- **Stops.** One pull request, never merged, or none in a quiet week. Nothing here reads a CRM, a
  call or Slack.

Adds 4 resources and no script.

| File                                | Resource                        | Role                                                                           |
| ----------------------------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| `infra/agents/web-scribe.ts`        | `defineAgent` (claudeCode)      | the scribe: model, folder, weekly cron, no env                                 |
| `infra/agents/web-scribe.prompt.ts` | (not a resource)                | the whole procedure: domain, pages, competitors, the exact commands, the rules |
| `infra/connectors/anthropic.ts`     | `defineConnector` (`anthropic`) | the model the harness runs on, billed and metered                              |
| `infra/connectors/git.ts`           | `defineConnector` (`github`)    | the clone, branch, push and PR path, resolved by binding                       |
| `infra/folders/index.ts`            | `defineFolder`                  | the workspace folder the agent is filed in                                     |

## Why no script

The other capture cookbooks read their source with a committed collector, because a fetch loop an
agent re-derives each week silently changes shape. Here the reads are two fixed commands, so the
prompt carries them exactly, and git already does the one thing a collector would add: comparing
this week to the last. What keeps the comparison honest is mechanical: `fullContent` returns the
whole page rather than excerpts chosen for a question, and a `node -e` line writes the files from
the command output, so the agent never retypes a page. Both were checked live: two reads of the same
pages a minute apart were byte-identical.

## Why competitors are in the default

A company already knows its own launches, pricing and funding; it made them. What a weekly read
catches that the team does not already know is a competitor changing its pricing or shipping
something. Same two reads, one more set of URLs, and the findings land in `insight/` with the
competitor's name and in proposals against its `alternative/` file.

## Why the baseline is the last merged read

The harness clones the default branch, so the only read a run can diff against is one that was
merged. A quiet week opens no pull request and commits nothing, which is why the news window starts
at the date of the last commit under `cadence/log/raw/web/` rather than a fixed seven days: the next
run covers the gap. It is also why the first run always opens a pull request, even when every domain
was already seeded.

## Why one source

A cookbook is a prebuilt approach an agent follows. Give it a page and a deal in one run and the
reader cannot tell the two confidence levels apart afterwards. So this cookbook holds one: what is
public, tagged as such. The CRM has `win-loss-review`, which verifies the ICP this seeds; calls
have `call-capture`.

## Placeholders (edit before deploy)

1. **`DOMAIN`**, **`PAGES`** and **`COMPETITORS`** in `infra/agents/web-scribe.prompt.ts`. The agent
   refuses the placeholder domain; `COMPETITORS` ships empty.
2. **`languageModel`** on the agent.

## What it does not do

It does not read a CRM, a call, an inbox or Slack; write the workspace context directly; edit a
file that exists; write a page by hand; contact anyone; or merge its own pull request.

## Verify

From this skill's folder:

```sh
node --import tsx evals/contract.mjs
```

From the project root:

```sh
npm run check && cargo-ai project plan
```
