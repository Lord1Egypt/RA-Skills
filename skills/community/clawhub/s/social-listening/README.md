# Social listening: find the LinkedIn conversations worth joining each week

To find the LinkedIn conversations about your problem worth joining, search the week's public posts
for your buyers' own words and judge them against your ICP. Every Monday this cookbook syncs one
capped post search, has an agent pick at most five posts and up to ten commenters who look like
buyers, and posts one digest to a locked Slack channel. It never engages on anyone's behalf.

```sh
cargo-ai project add cookbook/social-listening
```

## What it does

- Syncs the past week's LinkedIn posts for your buyer-language keywords every Monday.
- Drops posts already surfaced, then picks at most five worth joining, each tied to a context line.
- Reads comments on those five only, and quotes up to ten commenters whose headline matches an ICP
  persona.
- Posts one digest, then records the picked posts in a ledger so none headlines twice.

## What's inside

Adds 9 resources.

| File                              | Resource                        | Role                                                      |
| --------------------------------- | ------------------------------- | --------------------------------------------------------- |
| `infra/models/linkedin-posts.ts`  | `defineModel` (`fetchPosts`)    | the weekly, capped keyword search: what you buy           |
| `infra/models/surfaced-posts.ts`  | `defineModel` (native)          | the ledger: one row per post surfaced, no people          |
| `infra/agents/listener.ts`        | `defineAgent`                   | the cron, the reads, the comment pull, the locked post    |
| `infra/agents/listener.prompt.ts` | (not a resource)                | read context, pick, read comments, post, record           |
| `infra/connectors/linkedin.ts`    | `defineConnector` (`linkedin`)  | the search and the comment read; no engagement wired      |
| `infra/connectors/slack.ts`       | `defineConnector` (`slack`)     | the post path                                             |
| `infra/connectors/anthropic.ts`   | `defineConnector` (`anthropic`) | the model the agent runs on                               |
| `infra/folders/index.ts`          | `defineFolder` ×2               | where the agent and the models are filed                  |
| `references/digest.md`            | (not a resource)                | the digest shape and the rule for each section            |

## Why the search is in the model

The search is a paid source: it bills per post returned. That makes its query the purchase, so it
sits in the model's config with a `limit`, rather than pulling everything and narrowing in SQL. The
sync replaces the rows each week, which is why "already surfaced" lives in a separate ledger.

## Placeholders (edit before deploy)

1. **`searchKeywords`** in `infra/models/linkedin-posts.ts`: buyer-language phrases and competitor
   names from your workspace context.
2. **`channelId`** in `infra/agents/listener.ts`.
3. **`languageModel`**: any Anthropic model the workspace's connector can reach.

## What it does not do

It does not like, comment, connect, message, follow or visit a profile; store a list of people;
look anyone up beyond the comment they wrote; or post anywhere but the locked channel.
