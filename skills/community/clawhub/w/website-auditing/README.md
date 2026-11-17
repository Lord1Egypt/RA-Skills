# Website auditing: keep your website readable by AI agents

To make sure AI agents can find, read and use your website, score it every week and fix what the
source can fix. Every Monday this cookbook's agent reads Ora's agent-readiness audit of your domain
and up to three competitors' through Ora's MCP server, records the week, opens one pull request with
the top fixes the website's source can make, and posts one digest to a locked Slack channel.

```sh
cargo-ai project add cookbook/website-auditing
```

## What it does

- Scans each configured domain once a week through Ora, never forced, and records score, grade and
  failing checks in `website_audits`.
- Compares with last week: what was fixed, what newly fails, where a competitor is ahead.
- Applies the first three of Ora's ranked fixes that live in the website's source, following Ora's
  own playbook, and opens one pull request.
- Posts one digest with the scores, the pull request and the off-site fixes left to a human.

## What's inside

Adds 7 resources.

| File                                     | Resource                        | Role                                                              |
| ---------------------------------------- | ------------------------------- | ----------------------------------------------------------------- |
| `infra/agents/website-auditor.ts`      | `defineAgent` (claudeCode)      | the cron, the repository binding, the Ora MCP client, the post    |
| `infra/agents/website-auditor.prompt.ts` | (not a resource)              | score, record, compare, fix, post                                 |
| `infra/models/website-audits.ts`        | `defineModel` (native)          | the ledger: one row per domain per week                           |
| `infra/connectors/git.ts`                | `defineConnector` (`github`)    | the clone and the pull request                                    |
| `infra/connectors/slack.ts`              | `defineConnector` (`slack`)     | the post path                                                     |
| `infra/connectors/anthropic.ts`          | `defineConnector` (`anthropic`) | the model the harness runs on                                     |
| `infra/folders/index.ts`                 | `defineFolder` ×2               | where the agent and the model are filed                           |
| `references/digest.md`                   | (not a resource)                | the message shape and the rule for each line                      |

## Why Ora through MCP and not a connector

Cargo has no Ora integration, and Ora's reads need no account or key. The agent attaches Ora's
public MCP server (`mcpClients`) and keeps three tools: `scan_domain` and `get_score` to read an
audit, and `get_skill` to fetch Ora's fix playbook fresh each run. Every tool that writes to Ora or
spends its scan budget is disabled.

## Why a model and not the repository

Ora keeps only the latest scan of a domain. The weekly history, and whether this week was already
scanned, fixed and posted, has to live somewhere that is not waiting for a pull request to merge.

## Placeholders (edit before deploy)

1. **`AUDIT_DOMAIN`, `COMPETITOR_DOMAINS`, `WEBSITE_ROOT`** in `infra/agents/website-auditor.ts`.
2. **`channelId`**: the Slack channel id the digest lands in.
3. **`languageModel`**: any Anthropic model the workspace's connector can reach.

## What it does not do

It does not merge, edit outside the website's source, force a scan, submit feedback to Ora, or post
anywhere but the locked channel.
