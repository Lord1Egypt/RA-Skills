---
name: twtapi
description: Access live Twitter/X data through TwtAPI's hosted public skill gateway. Search tweets, look up users, read timelines, inspect followers and following, fetch tweet details, and check trends with structured JSON for OpenClaw and other compatible skill runners.
version: 1.2.0
metadata: {"openclaw":{"requires":{"env":["TWTAPI_SKILL_KEY"],"bins":["python3"]},"primaryEnv":"TWTAPI_SKILL_KEY","homepage":"https://www.twtapi.com/en/","install":[{"kind":"brew","formula":"python","bins":["python3"]}]}}
---

# TwtAPI - Twitter/X Data

Access live Twitter/X data through TwtAPI's hosted skill gateway. Search tweets, look up users, read timelines, browse followers, and check trends with structured JSON built for AI agents. Get your skill key at https://www.twtapi.com/en/.

## Setup

1. Install the public skill:

```
clawhub install twtapi
```

2. Sign up and open the `Skill` tab in your TwtAPI dashboard.
3. Copy your dedicated `skill_key`.
4. Set the required environment variable:

```
export TWTAPI_SKILL_KEY="tsk-your-skill-key"
```

The public hosted gateway `https://skill.twtapi.com` is built in by default, so most users do not need to set a base URL.

If you are overriding the gateway for a self-hosted or custom deployment, you can optionally set:

```
export TWTAPI_SKILL_BASE_URL="https://your-skill-host.example.com"
```

If you use OpenClaw, you can also set `skills."twtapi".env.TWTAPI_SKILL_KEY` in `~/.openclaw/openclaw.json`. Other compatible skill runners only need an equivalent way to inject `TWTAPI_SKILL_KEY`.

### Verify the skill connection

Run this first after setup:

```
python3 {baseDir}/scripts/twtapi.py tools
```

If auth and routing are correct, you should get a JSON list of available skill tools.

## Usage

### Search tweets

```
python3 {baseDir}/scripts/twtapi.py search "AI agents"
python3 {baseDir}/scripts/twtapi.py search "#bitcoin" --type Top --count 10
python3 {baseDir}/scripts/twtapi.py search "from:elonmusk" --cursor "scroll_xxx"
```

### Look up a user profile

```
python3 {baseDir}/scripts/twtapi.py user elonmusk
python3 {baseDir}/scripts/twtapi.py user-by-id 44196397
```

### Get user tweets / replies / media

Requires a numeric user ID. Look up the user first if you only have a username.

```
python3 {baseDir}/scripts/twtapi.py tweets 44196397
python3 {baseDir}/scripts/twtapi.py tweets 44196397 --count 5
python3 {baseDir}/scripts/twtapi.py replies 44196397
python3 {baseDir}/scripts/twtapi.py media 44196397
```

### Get a single tweet by ID

```
python3 {baseDir}/scripts/twtapi.py tweet 1897023456789012345
```

### List followers / following

```
python3 {baseDir}/scripts/twtapi.py followers 44196397 --count 50
python3 {baseDir}/scripts/twtapi.py following 44196397
```

### Get trending topics

```
python3 {baseDir}/scripts/twtapi.py trending
```

## Workflow tips

- **Username → user ID**: run `user <username>` first, then use the `rest_id` from the result for `tweets`, `followers`, etc.
- **Pagination**: most list commands accept `--cursor` for the next page. The cursor value is included in the response when more results are available.
- **Search operators**: the `search` command supports Twitter search syntax — `from:handle`, `to:handle`, `#hashtag`, `lang:en`, date ranges, etc.

## Notes

- This skill uses TwtAPI's hosted public gateway plus your dedicated `skill_key`, not your main API key.
- The hosted gateway is built in. Most end users only need `TWTAPI_SKILL_KEY`.
- Each API call consumes credits from your TwtAPI account.
- Returns raw Twitter JSON from the TwtAPI skill backend. Present results in a readable format with post content, author names, metrics, and timestamps.
- Rate limits and credit balance are managed by your plan.
