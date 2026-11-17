---
name: x-api-v2
description: "Read and post on X (Twitter) via the official X API v2. With an app bearer token: look up a profile, read an account's recent posts (optionally without retweets or replies), read a thread its author wrote in the last 7 days, search posts from the last 7 days with X's search operators, and look up posts by URL or ID (up to 100 at once). With a one-time OAuth 2.0 sign-in in the browser: read the signed-in account's home timeline (newest first), list its bookmarks (filtered by text, or just their links), list liked posts, and publish a post, which only shows a preview until run again with --yes. The bearer token and the OAuth client come from env vars or config.json; the sign-in is stored owner-only (by default in ~/.openclaw/x), renewed automatically, and revoked by logout. Every command can also print JSON (--json). X bills API use per request. Use when the user asks to look someone up on X, read recent posts or a thread, search X, see their home timeline, bookmarks or likes, or post on X."
summary: "X (Twitter) API v2: profiles, posts, threads, recent search, home timeline, bookmarks, likes, and posting with a preview first."
version: 1.2.0
homepage: https://github.com/odrobnik/x-skill
compatibility: "Python 3.8+ (standard library only) and network access to the X API. Works in OpenClaw, Claude Code, Codex and other agents that read SKILL.md."
permissions:
  - "network: X only (https://api.x.com for the API and for signing in and out, https://x.com for the sign-in page in the browser), plus the local sign-in callback on http://localhost:8080"
  - "file_read: config.json, tokens.json and pending-auth.json in the skill's config folder (~/.openclaw/x by default, or X_SKILL_CONFIG_DIR, or ${OPENCLAW_STATE_DIR}/x), and the two settings files that version 1.0 kept there"
  - "file_write: tokens.json and pending-auth.json in that config folder (owner-only)"
  - "env: X_BEARER_TOKEN, X_CLIENT_ID, X_CLIENT_SECRET, X_SKILL_CONFIG_DIR, OPENCLAW_STATE_DIR"
metadata:
  openclaw:
    emoji: "🐦"
    homepage: https://github.com/odrobnik/x-skill
    requires:
      bins: ["python3"]
    primaryEnv: X_BEARER_TOKEN
    envVars:
      - name: X_BEARER_TOKEN
        required: false
        description: "App bearer token for profiles, posts and search (or bearer_token in config.json)."
      - name: X_CLIENT_ID
        required: false
        description: "OAuth 2.0 client ID for bookmarks, likes and posting (or client_id in config.json)."
      - name: X_CLIENT_SECRET
        required: false
        description: "OAuth 2.0 client secret of a confidential client (or client_secret in config.json)."
      - name: X_SKILL_CONFIG_DIR
        required: false
        description: "Folder for config.json and the stored sign-in (default ~/.openclaw/x)."
      - name: OPENCLAW_STATE_DIR
        required: false
        description: "OpenClaw's state folder; when set, the default config folder is ${OPENCLAW_STATE_DIR}/x."
---

# X (Twitter) API v2

Look up profiles, posts and threads on X, search recent posts, read the signed-in account's bookmarks and likes, and publish posts, through the official X API v2.

**Entry point:** `{baseDir}/scripts/x.py` (Python 3 standard library only)

`{baseDir}` stands for this skill's folder, the one that contains this SKILL.md. Replace it with that folder's full path in every command, because commands run in the agent's workspace. In Claude Code the folder is `${CLAUDE_SKILL_DIR}`, which Claude Code fills in here; OpenClaw's agent resolves `{baseDir}` itself; other agents use the folder where they found this file.

## When to use

- The user asks to look up an X (Twitter) account or post, read someone's recent posts or a thread, search X, see their own bookmarks or likes, or publish a post on X.
- Not for other social networks, direct messages, or downloading media.
- `user`, `timeline`, `thread`, `search`, `tweet`, `tweets`, `bookmarks` and `likes` only read. `post` publishes on the user's account: run it only for a post the user asked for, and only after they approved the exact text (see How to use it).

## Setup

See [SETUP.md](SETUP.md). Profiles, posts and search need an app bearer token from the X Developer Console. Bookmarks, likes and posting need a one-time sign-in with `auth`, which uses the app's OAuth 2.0 client ID (and secret).

Credentials are read from config.json in the config folder: ~/.openclaw/x by default, ${OPENCLAW_STATE_DIR}/x when OpenClaw's state folder is moved (an existing ~/.openclaw/x stays in use until its files move), or any folder named by X_SKILL_CONFIG_DIR. The env vars X_BEARER_TOKEN, X_CLIENT_ID and X_CLIENT_SECRET override it. The sign-in is stored in tokens.json in the same folder, readable by the owner only. Never print or share these files.

## Commands

```bash
# Read (with the bearer token; without one, with the sign-in)
python3 {baseDir}/scripts/x.py user USERNAME                       # profile: bio, counts, verification
python3 {baseDir}/scripts/x.py timeline USERNAME [--max 5-100] [--exclude retweets,replies]
python3 {baseDir}/scripts/x.py thread POST_URL_OR_ID               # the author's own posts in that conversation
python3 {baseDir}/scripts/x.py search "QUERY" [--max 10-100]       # posts from the last 7 days
python3 {baseDir}/scripts/x.py tweet POST_URL_OR_ID
python3 {baseDir}/scripts/x.py tweets POST_URL_OR_ID [more ...]    # up to 100 in one request

# The signed-in account (needs auth)
python3 {baseDir}/scripts/x.py home [--max 1-3200] [--exclude retweets,replies]   # home timeline, newest first
python3 {baseDir}/scripts/x.py bookmarks [--max 1-100] [--contains "TEXT"] [--urls]
python3 {baseDir}/scripts/x.py likes USERNAME [--max 1-100]
python3 {baseDir}/scripts/x.py post "TEXT" [--yes]                 # without --yes: preview only, exit 3

# Sign in (one-time) and out
python3 {baseDir}/scripts/x.py auth                                # opens the browser, waits for the callback on localhost:8080
python3 {baseDir}/scripts/x.py auth --manual                       # prints the sign-in URL and exits
python3 {baseDir}/scripts/x.py auth --code "REDIRECT_ADDRESS"
python3 {baseDir}/scripts/x.py logout                              # revokes the sign-in at X, deletes tokens.json
```

USERNAME takes a name, @name or a profile link. POST_URL_OR_ID takes a post link from x.com or twitter.com, or the numeric ID.

## JSON output (`--json`)

Add `--json` before or after the subcommand (`x.py --json user NAME` = `x.py user NAME --json`) to get machine-readable output:

- **stdout carries exactly one JSON document**, also for errors. Human-readable text, emoji and warnings go to stderr (discard with `2>/dev/null`).
- Pretty-printed (indent 2) when stdout is a terminal, compact one-line JSON when piped. UTF-8, not ASCII-escaped. Posts and users are passed through as X sends them, plus a `url`.
- **Errors:** `{"error": {"message": "...", "code": "..."}}` on stdout, non-zero exit (1 = failure, 2 = usage, including bad option values). `code` is X's error type (e.g. `usage-capped`, `resource-not-found`, `invalid_request`, `rate_limited`), or `not_signed_in`, `missing_credentials`, `missing_oauth_client`, `unknown_account`, `invalid_tweet`, `invalid_username`, `not_found`, `network_error`, `filesystem_error`, `usage`; `error` for anything else.

| Command | JSON shape |
|---|---|
| `user` | the user from X (`id`, `name`, `username`, `description`, `created_at`, `verified`, `public_metrics`) plus `url` |
| `timeline`, `search`, `likes`, `bookmarks` | `[post, ...]` in X's order |
| `home` | `[post, ...]` newest first; each post also has `author_username`, `author_name` and `full_text` (the untruncated text: a long post's `note_tweet`, or for a repost `RT @user: ` plus the original's full text) |
| `thread` | `[post, ...]`, oldest first |
| `tweet` | one post |
| `tweets` | `[post, ...]` in the order asked; a post that can't be found is `{id, found: false, error}` (exit 1) |
| `bookmarks --urls` | the links in the bookmarks, as a list of strings |
| `post` | `{ok, posted, id, text, account, url}`; without `--yes`: `{text, characters, account, ok: false, needs_confirmation: true, dry_run: true}`, exit 3 |
| `auth --manual` | `{ok, auth_url, redirect_uri, next}`; `auth` and `auth --code`: `{ok, token_file, account, scopes, has_refresh_token}` |
| `logout` | `{ok, revoked, tokens_deleted, was_signed_in}` |

A post is the post from X (`id`, `text`, `created_at`, `public_metrics`, `author_id` and more) plus its `url`, and `author_username` when X sent the author along.

```bash
python3 {baseDir}/scripts/x.py --json search "from:XDevelopers -is:retweet" --max 10 | jq -r '.[] | .url'
python3 {baseDir}/scripts/x.py bookmarks --urls --json | jq -r '.[]'
python3 {baseDir}/scripts/x.py home --max 20 --json | jq -r '.[] | "@\(.author_username): \(.full_text)"'
```

## How to use it

- **Posting needs a clear yes.** Run `post` without `--yes` first: it shows the text, its length and the account, posts nothing, and exits with status 3. Show that preview to the user, and only after a clear yes run the same command with `--yes`. Never post text the user hasn't seen, and never post on your own initiative.
- **The home timeline, bookmarks and likes are private.** Show them to the user in the conversation. Don't post them, send them anywhere else, or save them to files unless the user asks for that.
- `search` and `thread` only reach back 7 days (X's recent search). Older posts need X's full-archive search, which this skill doesn't use.
- `thread` returns the author's own posts in the conversation (a self-thread), oldest first, not other people's replies.
- `home --max` above 100 pages through in requests of up to 100 posts; X serves at most the latest 3,200 posts or 7 days.
- Every request costs money on X's pay-per-use plan. Use the smallest `--max` that answers the question, and look up many posts with one `tweets` call rather than many `tweet` calls.
- **Signing in needs the user.** In cloud, container or other headless sessions always use `auth --manual`: send the user the URL and ask for the address their browser shows afterwards. It starts with http://localhost:8080/callback, and that page not loading is expected. Then run `auth --code "<that address>"`. On the user's own computer, plain `auth` opens the browser and finishes by itself.
- If a command reports that the sign-in expired or was revoked, run `auth` again.

## Security and permissions

- **Network:** only X. https://api.x.com for the API and for signing in and out; the sign-in page itself opens at https://x.com in the browser.
- **Files:** reads config.json from the config folder (default ~/.openclaw/x); reads and keeps tokens.json there and, during sign-in, pending-auth.json, both owner-only (mode 600). Setups from version 1.0 keep working: the two settings files 1.0 kept in that folder are still read. Nothing else on disk.
- **Local:** `auth` opens the browser and listens on 127.0.0.1 port 8080 for up to 5 minutes. Apart from that, the script starts no other programs and downloads no code.
- **Sign-in:** asks X for tweet.read, users.read, like.read, bookmark.read, tweet.write and offline.access (to stay signed in). It is renewed automatically; `logout` revokes it at X and deletes tokens.json.
- **Declared scope:** the `permissions` list in the frontmatter states this same scope for reviewers and scanners. Hosts don't enforce it; it describes what the script does.

## Costs and rate limits

X bills API use per request on its pay-per-use plan, from credits bought in the X Developer Console. A post or user fetched again within the same UTC day is charged once, and failed requests are free. See [references/pricing.md](references/pricing.md).

Rate limits per 15 minutes:

| Request | App (bearer token) | Signed-in account |
|---|---|---|
| Profile lookup | 900 | 900 |
| An account's posts | about 1,500 | about 900 |
| Search | 450 | 300 |
| Post lookup | 900 | 900 |
| Bookmarks | none | about 180 |
| Likes | none | about 75 |

When a limit is hit, the error (code `rate_limited`) says when it resets.

## Search operators

`search` takes X API v2 query syntax, which differs from the search box on the X website:

| Operator | Example | Finds |
|---|---|---|
| `from:` | `from:XDevelopers` | posts by that account |
| `to:` | `to:XDevelopers` | replies to that account |
| `@` | `@XDevelopers` | posts that mention it |
| `-is:retweet` | `OpenClaw -is:retweet` | posts that aren't retweets |
| `is:reply`, `-is:reply` | `from:XDevelopers -is:reply` | only replies, or no replies |
| `has:links`, `has:media` | `OpenClaw has:links` | posts with links or media |
| `lang:` | `OpenClaw lang:de` | posts in that language |
| `"..."` | `"open source"` | the exact phrase |
| `OR`, `( )` | `(OpenClaw OR ClawHub) -is:retweet` | either term |

## Limits

- Search and thread reach back 7 days only.
- X has kept likes private since 2024, so expect `likes` to work for the signed-in account only.
- Posts are limited to 280 characters for most accounts. X counts each link as 23 characters and some characters (emoji, CJK) as 2; the preview shows the plain length.
- No media uploads, replies, reposts, quote posts, deleting posts, or direct messages.
