---
name: reddgrow
version: 0.1.6
description: "Reddit intelligence CLI for AI agents. Use when working with reddit posts, subreddit research, comments, user profiles, wiki pages, domain mentions, marketing, community rules, or URL checking."
metadata: {"openclaw":{"emoji":"🔴","homepage":"https://reddgrow.ai","requires":{"bins":["reddgrow"],"env":["REDDGROW_API_KEY"]},"install":[{"id":"npm","kind":"node","package":"@reddgrow/cli","bins":["reddgrow"],"label":"Install via npm"}],"primaryEnv":"REDDGROW_API_KEY"}}
---

# ReddGrow — Reddit Intelligence for AI Agents

Reddit API access for AI agents. All commands output JSON to stdout. Errors go to stderr with exit code 1.

## Setup

```bash
# Install
npm install -g @reddgrow/cli

# Authenticate (one-time)
reddgrow auth login rg_your_api_key_here

# Or use environment variable
export REDDGROW_API_KEY=rg_your_api_key_here
```

## Commands

### Subreddits

```bash
reddgrow subreddits search "<query>" [--limit N]                                            # (3 cr)
reddgrow subreddits about <name>                                                            # (1 cr)
reddgrow subreddits rules <name>                                                            # (1 cr)
reddgrow subreddits wiki <name>                                                             # list wiki pages (5 cr)
reddgrow subreddits wiki-page <name> <page>                                                 # read wiki page (5 cr)
reddgrow subreddits posts <name> [--sort hot|new|top|rising|controversial] [--time hour|day|week|month|year|all] [--limit N]  # (2 cr)
reddgrow subreddits comments <name> [--limit N]                                             # comment stream (2 cr)
reddgrow subreddits check-url <name> "<url>"                                                # check if URL submitted (3 cr)
reddgrow subreddits traffic <name>                                                          # traffic stats (1 cr)
reddgrow subreddits widgets <name>                                                          # sidebar widgets (1 cr)
```

### Posts

```bash
reddgrow posts search "<query>" [--subreddit <name>] [--sort relevance|hot|top|new|comments] [--limit N]  # (3 cr)
reddgrow posts comments <subreddit> <post_id> [--sort best|top|new|controversial] [--limit N]             # (2 cr)
reddgrow posts duplicates <subreddit> <post_id>                                                           # (5 cr)
reddgrow posts batch <id1,id2,...>                                                                        # (5 cr)
```

### Users

```bash
reddgrow users profile <username>               # karma, account age, activity (1 cr)
reddgrow users posts <username> [--limit N]     # post history (2 cr)
reddgrow users comments <username> [--limit N]  # comment history (2 cr)
```

### Domains

```bash
reddgrow domains mentions <domain> [--limit N]  # all posts linking to domain (5 cr)
```

### Auth

```bash
reddgrow auth whoami         # identity & credits remaining (1 cr)
reddgrow auth status         # connection status
reddgrow auth login <key>    # save API key (run once)
```

## Workflows

### Before posting to a subreddit

1. Read rules: `reddgrow subreddits rules <name>` — rule violations get posts removed instantly
2. Check community type: `reddgrow subreddits about <name>` — if `subreddit_type` is `restricted` or `private`, stop; if `submission_type` is `link` or `self`, respect it
3. Check URL not already submitted: `reddgrow subreddits check-url <name> "<url>"`
4. Read wiki for extra guidelines: `reddgrow subreddits wiki-page <name> index`
5. Post only after all checks pass

### Research a subreddit

1. Find communities: `reddgrow subreddits search "<topic>"`
2. Inspect details: `reddgrow subreddits about <name>` — size, type, activity
3. Browse content: `reddgrow subreddits posts <name> --sort top --time week --limit 50`
4. Check activity: `reddgrow subreddits traffic <name>`
5. Discover guidelines: `reddgrow subreddits wiki <name>` then `wiki-page <name> <page>`

### Monitor a domain / brand

1. Discover mentions: `reddgrow domains mentions <domain> --limit 100`
2. Read discussion: `reddgrow posts comments <subreddit> <post_id> --sort best`
3. Check for duplicates: `reddgrow subreddits check-url <name> "<url>"` before re-sharing

### Analyze a Reddit user

1. Get overview: `reddgrow users profile <username>` — karma, age, verified status
2. Review posts: `reddgrow users posts <username> --limit 50`
3. Review comments: `reddgrow users comments <username> --limit 50`

## Rules

1. ALWAYS run `reddgrow subreddits rules <name>` before posting — rule violations get posts removed
2. ALWAYS run `reddgrow subreddits check-url <name> "<url>"` before sharing any link — duplicate posts are banned
3. Read wiki (`wiki-page <name> index`) when rules reference additional guidelines
4. Respect `subreddit_type`: `restricted` or `private` means posting is not allowed
5. Respect `submission_type`: some subreddits only accept links or only text posts
6. ALWAYS check `reddgrow auth whoami` before large batch operations to avoid credit exhaustion
7. Never post promotional content to communities that explicitly prohibit self-promotion

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `REDDGROW_API_KEY` | API key (overrides saved key) | — |
| `REDDGROW_API_URL` | API base URL | `https://api.reddgrow.ai` |
| `REDDGROW_MODE` | Output mode (`human` or `json`) | `json` |
