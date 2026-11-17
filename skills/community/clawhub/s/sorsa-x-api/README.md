# Sorsa Twitter / X API Skill

A SKILL.md agent skill that lets Claude, Cursor, Codex, and other SKILL.md-compatible
AI agents pull public **Twitter / X data** through the [Sorsa API](https://api.sorsa.io/overview):
profiles, tweets, followers, search, mentions, Communities, Lists, and crypto-focused
influence analytics (Sorsa Score).

Sorsa is a developer-friendly, lower-cost **alternative to the official X (Twitter) API**
and to providers like **twitterapi.io**. Pricing is per request, with no app review or OAuth setup.

## What this skill does

Once installed, your agent can, on its own, decide to call Sorsa whenever a task needs
X/Twitter data. Covered capabilities:

- **Users:** profile lookup (single and batch up to 100), followers, following, verified followers, about info
- **Tweets:** a user's tweets, single and bulk tweet data, replies, quotes, retweeters, long-form Articles
- **Search:** tweet search with Twitter advanced-search operators, user search, mention monitoring with filters
- **Checks:** does a user follow / comment / retweet / quote, community membership
- **Communities & Lists:** members, feeds, in-community search, list members/followers/tweets
- **Trends & Spaces:** trending topics by location (WOEID), Twitter/X Space metadata and participants
- **Crypto analytics (Sorsa Score):** influence score, score changes, follower category breakdown, top followers/following

Sorsa is focused on read-only public X/Twitter data. It does not post tweets, like,
follow, DM, or perform any action on behalf of a user. For write actions, use the
official X API. For read workloads, Sorsa is a lower-cost drop-in.

## Use cases

- Monitor brand or ticker mentions on X
- Collect tweets for sentiment or trend analysis
- Verify follows, retweets, quotes, and comments for campaigns and airdrops
- Analyze crypto influencer audiences with Sorsa Score
- Build AI agents that can search and read public X data
- Migrate read-only workloads off the official X API

## Useful for

Twitter API alternative, X API scraper, Twitter/X search API, Twitter followers API,
Twitter mentions monitoring, twitterapi.io alternative, AI agent Twitter data access.

## Install

This skill works with any agent that reads the open `SKILL.md` format (Claude Code,
Claude apps, Cursor, Codex CLI, and others).

**Manual install** (works everywhere): copy this folder into your agent's skills directory.

```bash
# Claude Code, user-scoped example
git clone https://github.com/YOUR_ORG/sorsa-x-api-skill ~/.claude/skills/sorsa-x-api
```

For project-scoped use, place it under `.claude/skills/` in your repo instead. Other agents
use their own skills directory; the contents are the same.

## Usage

1. Get an API key at [api.sorsa.io/overview](https://api.sorsa.io/overview).
2. Expose it to your environment:
   ```bash
   export SORSA_API_KEY=your_key
   ```
3. Ask your agent something like *"get the 100 most recent followers of @elonmusk"* or
   *"search X for popular posts mentioning Solana this week"*. The skill tells the agent
   how to authenticate, choose the endpoint, and paginate.

Quick manual check:

```bash
curl -H "ApiKey: $SORSA_API_KEY" "https://api.sorsa.io/v3/info?username=elonmusk"
```

See [`examples/`](examples/) for runnable Python and curl, and
[`references/api-reference.md`](references/api-reference.md) for the full endpoint list.

## Repo contents

```
sorsa-x-api-skill/
├── SKILL.md                       # the skill (frontmatter + instructions)
├── README.md
├── LICENSE
├── .env.example                   # copy to .env and add your key
├── requirements.txt
├── .gitignore
├── references/
│   └── api-reference.md           # full v3 endpoint reference
├── examples/
│   ├── quickstart.py
│   ├── search_with_pagination.py
│   ├── analyze_account.py
│   └── curl_snippets.sh
└── scripts/
    └── sorsa_client.py            # reusable client (auth, retry, pagination)
```

## Links

- API plans and dashboard: https://api.sorsa.io/overview
- Docs: https://docs.sorsa.io/ (LLM index: https://docs.sorsa.io/llms.txt)
- OpenAPI spec: https://docs.sorsa.io/v3/openapi.json
- Analytics app: https://app.sorsa.io
- Website: https://sorsa.io

## About Sorsa

Sorsa (formerly TweetScout) is a Twitter/X data and analytics platform for traders,
researchers, and funds. The same data is available programmatically through the Sorsa API.

X and the X logo are trademarks of X Corp. Sorsa is not affiliated with X Corp.

## License

MIT. See [LICENSE](LICENSE).
