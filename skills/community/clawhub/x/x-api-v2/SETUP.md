# X API v2 Setup

## Prerequisites

- Python 3.8 or later (standard library only, no pip dependencies)
- An X developer account with an app: <https://developer.x.com/en/portal/projects-and-apps>
- Credits for X's pay-per-use API (see [Billing](#billing))

## Install

The skill is a single folder. Name it `x-api-v2`, the skill's `name`, wherever it goes:

| Agent | Where the folder goes |
|---|---|
| OpenClaw | `openclaw skills install @odrobnik/x-api-v2` (from ClawHub, into `<workspace>/skills/x-api-v2`) |
| Claude Code | `~/.claude/skills/x-api-v2/`, or `.claude/skills/` inside a project |
| Codex | `~/.agents/skills/x-api-v2/`, or `.agents/skills/` inside a repository (OpenClaw reads these folders too) |
| Other agents | their skills folder, under the same name |

From GitHub, for example for Claude Code:

```bash
git clone https://github.com/odrobnik/x-skill ~/.claude/skills/x-api-v2
```

The commands in SKILL.md start with `{baseDir}/`, meaning this folder; agents put in its full path. The examples below run from inside the folder.

## Where Credentials Live

Nothing is stored inside the skill folder. Config and the sign-in share one config folder:

1. `$X_SKILL_CONFIG_DIR`, if set
2. otherwise `$OPENCLAW_STATE_DIR/x`, if OpenClaw's state folder has been moved. An existing `~/.openclaw/x/` keeps being used until you move its files there.
3. otherwise `~/.openclaw/x/`

The default works with every agent, not only OpenClaw. On OpenClaw, keep it: OpenClaw's backups and its Docker setup preserve `~/.openclaw`.

Put your credentials in `config.json` in that folder (by default `~/.openclaw/x/config.json`):

```json
{
  "bearer_token": "YOUR_BEARER_TOKEN",
  "client_id": "YOUR_OAUTH_CLIENT_ID",
  "client_secret": "YOUR_OAUTH_CLIENT_SECRET"
}
```

Keep the file private to your account (file mode 600); the script warns when other users can read it.

| What | File in the config folder |
|---|---|
| Bearer token, OAuth client ID and secret | `config.json`, or env vars (env vars win) |
| The sign-in, saved by `auth` | `tokens.json` (mode 600) |
| A sign-in in progress, deleted when done | `pending-auth.json` (mode 600) |

### Environment Variables

Env vars override the values in `config.json`.

| Variable | Needed for | Description |
|---|---|---|
| `X_BEARER_TOKEN` | Profiles, posts, search | App bearer token. Without it, these use your sign-in. |
| `X_CLIENT_ID` | Signing in | OAuth 2.0 client ID |
| `X_CLIENT_SECRET` | Signing in | OAuth 2.0 client secret (confidential clients only) |
| `X_SKILL_CONFIG_DIR` | Optional | A different config folder |
| `OPENCLAW_STATE_DIR` | Optional | OpenClaw's state folder, if moved; the default config folder follows it |

### OpenClaw Only

- You can set the bearer token as `skills.entries.x-api-v2.apiKey` in `openclaw.json`; OpenClaw passes it to the script as `X_BEARER_TOKEN`.
- OpenClaw's secret filter blocks `X_CLIENT_SECRET` in `skills.entries.*.env`, so keep the OAuth client in `config.json`.
- In OpenClaw's Docker sandbox, commands run with `HOME` set to the sandbox workspace and don't receive `skills.entries` keys. Put `config.json` in `.openclaw/x/` inside that workspace, or point `X_SKILL_CONFIG_DIR` somewhere else.

## Upgrading from 1.0

- **The skill's name changed** from `x` to `x-api-v2`, its name on ClawHub. If your `openclaw.json` has settings under `skills.entries.x`, move them to `skills.entries.x-api-v2`.
- **Your setup keeps working.** The script still reads the two settings files 1.0 used in the config folder, and your sign-in stays valid. When convenient, move `bearer_token`, `client_id` and `client_secret` into `config.json` there and delete the old files.
- **The sign-in is now stored owner-only** (mode 600). The script converts the stored sign-in the first time it reads it.
- **`likes` needs one more permission** (like.read), which 1.0 didn't ask for. Run `python3 scripts/x.py auth` once more to grant it.
- **`post` previews first** and posts only when run again with `--yes`.

## 1. Bearer Token (Profiles, Posts, Search)

1. Open the X Developer Console: <https://developer.x.com/en/portal/projects-and-apps>
2. Set up a project with an app, or pick an existing app.
3. Under **Keys and tokens**, generate the **Bearer Token** and copy it.
4. Add it to `config.json` as `bearer_token`, or export `X_BEARER_TOKEN`.
5. Test it:

   ```bash
   python3 scripts/x.py user XDevelopers
   ```

## 2. OAuth 2.0 Client (Bookmarks, Likes, Posting)

1. In the app's settings, open **User authentication settings** and click **Set up**.
2. Fill in:

   | Field | Value |
   |---|---|
   | App permissions | Read and write |
   | Type of App | Web App, Automated App or Bot (a confidential client, with a client secret), or Native App (a public client, without one) |
   | Callback URI | `http://localhost:8080/callback`, exactly (http, no trailing slash) |
   | Website URL | any valid URL, e.g. your GitHub profile |

3. Save, then copy the **Client ID** (and the **Client Secret**, if there is one) into `config.json` as `client_id` and `client_secret`.

## 3. Sign In

```bash
python3 scripts/x.py auth
```

This opens the X consent page in the browser; a short-lived server on port 8080 catches the redirect to `http://localhost:8080/callback`. The sign-in is saved to `tokens.json` in the config folder and renewed automatically: X ends each sign-in after 2 hours, and the stored refresh token renews it.

The script asks X for these permissions: tweet.read, users.read, like.read, bookmark.read, tweet.write and offline.access (to stay signed in).

### Headless Machines and Cloud Agents

Agents in the cloud, in containers or on machines without a browser should use this flow:

```bash
python3 scripts/x.py auth --manual
```

Open the printed URL on any device and approve access. The browser then tries to load `http://localhost:8080/callback?state=…&code=…`, which fails on another device; that's expected. Copy the whole address and finish with:

```bash
python3 scripts/x.py auth --code "http://localhost:8080/callback?state=...&code=..."
```

If port 8080 is taken on your own computer, use the same flow.

## Signing Out

```bash
python3 scripts/x.py logout
```

This revokes the sign-in at X and deletes `tokens.json` from the config folder. You can also revoke the app in X's settings under **Security and account access → Apps and sessions → Connected apps**.

## Billing

X's API is paid per use:

1. Buy credits in the Developer Console (<https://developer.x.com/en/portal/billing>); $10 to $25 is plenty to start.
2. Set a monthly spending limit there, so a runaway loop can't run up costs. Requests stop when the limit is reached.
3. Optionally turn on auto-recharge (e.g. add $25 when the balance drops below $5).

A post or user fetched again within the same UTC day is charged once, and failed requests are free. The console's dashboard shows the usage per day. See [references/pricing.md](references/pricing.md) for details.

## Troubleshooting

- **401 Unauthorized** when reading: check the bearer token; copy it again from **Keys and tokens**.
- **403 Forbidden**: the app's permissions don't cover the request, e.g. posting needs "Read and write" in the user authentication settings. Change them, then run `auth` again.
- **429 Too Many Requests**: a rate limit (per 15 minutes); the error says when it resets.
- **Callback mismatch or invalid redirect URI** when signing in: the app's callback URI must be exactly `http://localhost:8080/callback`.
- **The sign-in expired or was revoked**: run `python3 scripts/x.py auth` again.
