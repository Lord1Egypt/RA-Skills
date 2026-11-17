# Stalled-deal nudge: flag stalled deals and draft the follow-up

To keep open deals from going cold, find the ones with no logged activity and put a ready follow-up
in front of their owner. Every Monday this cookbook sends each rep one Slack digest of their open
deals quiet for fourteen days or more, with the line the last activity left off on, why the deal is
worth a touch now, and a follow-up drafted for them to send; it never sends anything to a prospect.

```sh
cargo-ai project add cookbook/stalled-deal-nudge
```

## What it does

- Computes each open deal's last activity in SQL, as the latest logged email, meeting, call or note.
- Each Monday, selects the open deals quiet for `QUIET_DAYS` or more, and drops any already nudged
  this ISO week.
- Reads the last note, meeting or call on each, and writes a reason and a draft grounded in it.
- Posts one digest per owner to a locked channel, then records each deal in the ledger.

## What's inside

Adds 9 resources.

| File                            | Resource                        | Role                                                            |
| ------------------------------- | ------------------------------- | --------------------------------------------------------------- |
| `infra/agents/nudger.ts`        | `defineAgent`                   | the Monday cron, the model reads, the locked Slack post         |
| `infra/agents/nudger.prompt.ts` | (not a resource)                | the SQL rule, the owner map, research, digest, ledger           |
| `infra/models/gtm-opportunities.ts`         | `defineModel` (native deal)     | the pipeline: stage, amount, close date, owner, is_closed       |
| `infra/models/gtm-accounts.ts`      | `defineModel` (native account)  | the company name each deal belongs to                           |
| `infra/models/gtm-activities.ts`    | `defineModel` (native custom)   | one row per logged email, meeting, call or note                 |
| `infra/models/deal-nudges.ts`   | `defineModel` (native)          | the ledger: one row per deal nudged per week                    |
| `infra/connectors/slack.ts`     | `defineConnector` (`slack`)     | the post path                                                   |
| `infra/connectors/anthropic.ts` | `defineConnector` (`anthropic`) | the model the agent runs on                                     |
| `infra/folders/index.ts`        | `defineFolder` ×2               | where the agent and the models are filed                        |
| `references/digest.md`          | (not a resource)                | the digest shape and the rule for each line                     |

## Why one agent and not a play

The output is a digest grouped by owner, and grouping is a judgment over the whole list. A play
enrolls deals one at a time and would need a second step to gather them back into one post per
owner. The agent runs the selection itself, in SQL over a model that holds every deal, so the rule
is one readable query in the prompt.

## Placeholders (edit before deploy)

1. **`channelId`** in `infra/agents/nudger.ts`: the Slack channel id the digests land in.
2. **`OWNERS`** in `infra/agents/nudger.prompt.ts`: `owner_id` to the name the digest prints.
3. **`QUIET_DAYS`** in the same file: fourteen by default.
4. **The hour and timezone**: the cron (UTC) and the timezone named in the trigger `text`.
5. **`languageModel`**: any Anthropic model the workspace's connector can reach.

## Deals in a CRM

Swap `gtm_opportunities` and `gtm_activities` for connector-backed models that extract every record and every
column, and adapt the column names in the prompt's SQL. `SKILL.md`, `crm-backed`, maps the last
activity property for HubSpot and Salesforce.

## What it does not do

It does not write to the deal models, send the drafts, message a prospect, post anywhere but the locked
channel, or edit the workspace context.
