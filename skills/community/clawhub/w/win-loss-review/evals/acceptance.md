# Acceptance

Walk every line before calling the pipeline done. Report each with its evidence: a command output,
a run link, or a pull request link. A line that could not be checked is reported as unchecked, not
as passed.

## Before deploy

- `node --import tsx evals/contract.mjs` passes, run from the skill folder.
- The project holds exactly one `crm` connector and one each of `crm_accounts` and `crm_contacts`;
  copies this cookbook brought were dropped where another cookbook already declares them.
- `LOST_REASON_COLUMN` in the prompt names the portal's lost-reason property, and no model's config
  filters or picks columns.
- The Slack channel id is an id, not a name, and not a customer shared channel.
- `cargo-ai project check` prints `agent:win_loss_analyst` bound to `<repo>#<branch>` at the repository
  root, and `cargo-ai project plan` shows the agent, the models, the bound connectors and two folders.

## After the models sync

- The `pipelines` query, run by hand, returns non-zero won and lost counts.
- `crm_deals` holds open deals too, and the `pipelines` counts match the closed deals the team
  knows about: the queries, not the model, narrow to closed.

## The first pass

- Exactly one pull request, unmerged, titled `[win-loss-review] first pass <date>`; the Slack digest
  is posted once, five lines, ending with its link.
- The body opens with the two hygiene findings, each with its denominator, then the mode and the won
  count that set it.
- `outputs/<date>-win-loss-review/README.md` holds each query's result, counts and ids only, no
  amount and no email.
- `icp/` carries a disqualifier, as a new file or one dated section appended to the seeded one.
- `insight/` holds dated files in the three buckets; every title at a won account is mapped to a
  persona or listed as undetected, and the file says the titles are at the accounts, not only on
  the deals.
- With the fill rate under half, no `objection/` file exists and the body says why.
- Every `client/` file carries `reference_permission: unknown` and no amount.
- Nothing under `persona/` changed.

## A monthly run

- It read the deals closed since the date of the last merged run record.
- With new deals: a pull request that adds files and modifies none under `icp/` or `persona/`.
- With none: no pull request, and the digest says so.

## After merge

- The verified ICP section is readable from the workspace context repository after
  `cargo-ai project deploy`, and an agent with the `context` capability quotes it back with its tag.
