# RedReplier plugin for OpenClaw

Monitor Reddit, Hacker News, X, Bluesky and Facebook for keyword mentions of your
product, AI-scored 0-100 for relevance so you act on real leads instead of
noise. From inside OpenClaw.

## Install

```bash
openclaw plugins install clawhub:@redreplier/openclaw-plugin
openclaw plugins enable redreplier
openclaw gateway restart
```

Create a dedicated, revocable token at
[redreplier.com](https://redreplier.com) under Settings, then API Tokens.

```json5
{
  plugins: {
    entries: {
      redreplier: {
        enabled: true,
        config: { apiToken: "redreplier_..." }
      }
    }
  }
}
```

The token decides the account, so you never pass an account or group id.

## Tools

| tool | what it does |
|---|---|
| `redreplier_websites` | List monitored websites with their keywords and statuses. Call this first. |
| `redreplier_mentions` | List AI-scored mentions, filtered by site, status, score, keyword, source or date. |
| `redreplier_explain_mention` | Read why one mention scored the way it did. |
| `redreplier_set_mention_status` | Approve, reject, or reset a mention. |
| `redreplier_add_keywords` | Add keywords to a website. |

Five tools out of the API's twenty-two operations, and the omissions are deliberate.

## What is deliberately missing

Nothing here can delete data or change plan capacity. Deleting a keyword also
erases every mention it produced, and deleting a website stops all monitoring,
so both stay out of the plugin. So do keyword activation and the billing
preview endpoints: the API never charges, and going past the plan's keyword cap
means upgrading in the RedReplier app. Call the REST API yourself for those, or
reach the deletes and keyword activation through the
[MCP server](https://github.com/RedReplier/agent/tree/main/mcp-server), where the
confirmation rules are spelled out.

`redreplier_add_keywords` is the one write that touches keywords, and it is
safe by construction: new keywords that fit the current plan go ACTIVE at once
for free, and only the rest land as PENDING and sit inert until a slot frees
up or the plan is upgraded in the RedReplier app.

## Things worth knowing

Two filters hide rows by default. `redreplier_mentions` excludes REJECTED
mentions, and hides anything under the website's minimum score (30 by
default) unless you pass `includeLowRelevance`. A query that "returns nothing" is often one of those.

Only ACTIVE keywords match new mentions. PENDING ones match nothing, so a
website with a long pending list looks quiet for reasons that have nothing to
do with the internet.

`redreplier_explain_mention` generates the explanation on first call and
consumes AI quota. Use it on a score that looks wrong, not across a list.

The API allows 600 requests per minute per token. A 429 comes back with
`Retry-After` and the plugin surfaces it rather than hammering.

## Develop

```bash
npm install
npm run build
openclaw plugins install --link . --force --accept-capabilities
openclaw plugins inspect redreplier --runtime --json
```

Needs Node `>=22.22.3 <23 || >=24.15.0 <25 || >=25.9.0`. `npm install` runs
OpenClaw's version guard on postinstall and stops outside that range.

MIT licensed. Source: [RedReplier/redreplier-openclaw](https://github.com/RedReplier/redreplier-openclaw)
