# Rumoro for OpenClaw

Let your OpenClaw agent keep track of what people say about your product and your competitors. Ask in plain language, and it tracks keywords, goes through new mentions with you, sends alerts to Slack, Telegram, email or a webhook, reports on trends and shows you who is posting. It all runs through the [Rumoro API](https://docs.rumoro.dev).

## Get started

```bash
openclaw skills install @markolo10/rumoro --global
echo 'RUMORO_API_KEY=ref_...' >> ~/.openclaw/.env
openclaw gateway restart
```

Create the key on the API keys page at [app.rumoro.dev](https://app.rumoro.dev). New accounts get $5.80 of free credit. Setup details and troubleshooting are in the [OpenClaw guide](https://docs.rumoro.dev/integrations/openclaw).

## Things to ask

- "Track basil as our brand and sorrel as a competitor."
- "Which of this week's mentions should I answer first?"
- "Did anyone ask for help with basil on Stack Overflow or GitHub? Draft answers to the open questions."
- "Show me today's negative mentions and draft a reply to the worst one."
- "I've answered the first three. Mark them done and ignore the rest."
- "Post new bug reports about basil to our #support Slack channel, and email me a summary every Monday at 9."
- "Which platforms brought us the most mentions this month, and what's our share of voice against sorrel?"
- "Which people with large followings mentioned us recently?"
- "We keep getting pesto recipes. Tell the classifier what our product is."

## Sources

Reddit, X, Hacker News, GitHub, Bluesky, LinkedIn, Stack Overflow, DEV, YouTube, TikTok, Instagram and news. Each post is scored for relevance and sentiment and tagged with intents such as a question or a buying signal, so the agent can show you what needs an answer first.

## What's in the skill

`SKILL.md` gives the agent the setup, the API's conventions and the call to make for each kind of request. `rules/` holds a reference file for each part of the API (keywords, mentions, people, alerts, analytics, account, authentication and errors) plus one for the CLI and SDKs. Most are generated from Rumoro's OpenAPI document, so the skill stays in step with the API.

## Links

- [rumoro.dev](https://rumoro.dev)
- [docs.rumoro.dev](https://docs.rumoro.dev)
- [app.rumoro.dev](https://app.rumoro.dev)
- [github.com/rumoro-dev/openclaw-skill](https://github.com/rumoro-dev/openclaw-skill)

MIT.
