# YouTube Playlist Manager Setup

## Prerequisites

- Python 3.8 or later (standard library only, no pip dependencies)
- A Google Cloud project with the **YouTube Data API v3** enabled

## Install

The skill is a single folder. Name it `youtube-playlist-manager`, the skill's `name`, wherever it goes:

| Agent | Where the folder goes |
|---|---|
| OpenClaw | `openclaw skills install @odrobnik/youtube-playlist-manager` (from ClawHub, into `<workspace>/skills/youtube-playlist-manager`) |
| Claude Code | `~/.claude/skills/youtube-playlist-manager/`, or `.claude/skills/` inside a project |
| Codex | `~/.agents/skills/youtube-playlist-manager/`, or `.agents/skills/` inside a repository (OpenClaw reads these folders too) |
| Other agents, e.g. Grok | their skills folder, under the same name |

From GitHub, for example for Claude Code:

```bash
git clone https://github.com/odrobnik/youtube-skill ~/.claude/skills/youtube-playlist-manager
```

The commands in SKILL.md start with `{baseDir}/`, meaning this folder; agents put in its full path. The examples below run from inside the folder.

## Where Credentials Live

Nothing is stored inside the skill folder. Config and the sign-in share one config folder:

1. `$YOUTUBE_SKILL_CONFIG_DIR`, if set
2. otherwise `$OPENCLAW_STATE_DIR/youtube`, if OpenClaw's state folder has been moved. An existing `~/.openclaw/youtube/` keeps being used until you move its files there.
3. otherwise `~/.openclaw/youtube/`

The default works with every agent, not only OpenClaw. On OpenClaw, keep it: OpenClaw's backups and its Docker setup preserve `~/.openclaw`.

| What | File in the config folder |
|---|---|
| API key, OAuth client ID and secret | `config.json`, or env vars (env vars win) |
| Sign-in tokens, saved by `auth` | `tokens.json` (mode 600) |
| Sign-in in progress, removed when done | `pending-auth.json` (mode 600) |

Put your credentials in `config.json` in that folder (by default `~/.openclaw/youtube/config.json`):

```json
{
  "api_key": "YOUR_YOUTUBE_API_KEY",
  "client_id": "YOUR_OAUTH_CLIENT_ID",
  "client_secret": "YOUR_OAUTH_CLIENT_SECRET"
}
```

Keep the file private to your account (file mode 600); the script warns when other users can read it.

### Environment Variables

Env vars override config.json values. [.env.example](.env.example) lists them; the script reads the environment, not that file.

| Variable | Needed for | Description |
|---|---|---|
| `YOUTUBE_API_KEY` | Search, video details | YouTube Data API v3 key. Without it, both use your sign-in. |
| `YOUTUBE_CLIENT_ID` | Playlists | OAuth 2.0 client ID (Desktop app) |
| `YOUTUBE_CLIENT_SECRET` | Playlists | OAuth 2.0 client secret |
| `YOUTUBE_SKILL_CONFIG_DIR` | Optional | A different config folder |
| `OPENCLAW_STATE_DIR` | Optional | OpenClaw's state folder, if moved; the default config folder follows it |

### OpenClaw Only

- You can set the API key as `skills.entries.youtube-playlist-manager.apiKey` in `openclaw.json`; OpenClaw passes it to the script as `YOUTUBE_API_KEY`.
- OpenClaw's secret filter blocks `YOUTUBE_CLIENT_SECRET` in `skills.entries.*.env`, so keep the OAuth client in `config.json`.
- In OpenClaw's Docker sandbox, commands run with `HOME` set to the sandbox workspace and don't receive `skills.entries` keys. Put `config.json` in `.openclaw/youtube/` inside that workspace, or point `YOUTUBE_SKILL_CONFIG_DIR` somewhere else.

## 1. Enable the API

1. Open <https://console.cloud.google.com/> and choose the project to use (a new one is fine).
2. **APIs & Services → Library → YouTube Data API v3 → Enable**.

## 2. API Key (Search and Video Details)

1. **APIs & Services → Credentials**, open the **+** menu at the top and choose **API key**.
2. Edit the key and restrict it to **YouTube Data API v3**.
3. Add it to config.json as `api_key`, or export `YOUTUBE_API_KEY`.

## 3. OAuth Client (Playlist Management)

1. Open **Google Auth Platform** (formerly *OAuth consent screen*) and set it up with user type **External**.
2. Under **Audience**, add your Google account as a **test user**. While the app is in *Testing*, only test users can sign in.
3. Still under **Audience**, click **Publish app** to move it to *In production*. Google limits sign-ins to apps in Testing to **7 days**, after which every playlist command fails until you sign in again. An unverified app in production is fine for personal use; you click through the "Google hasn't verified this app" warning once.
4. Under **Clients**, add a client of type **Desktop app** and copy its client ID and secret into config.json (or the env vars).

## 4. Sign In

```bash
python3 scripts/youtube.py auth
```

This opens a browser for Google consent; a short-lived server on `http://127.0.0.1:8923` catches the redirect (pick another port with `--port`). Tokens are saved to `tokens.json` in the config folder and refresh automatically.

### Headless Machines and Cloud Agents

Agents in the cloud, in containers or on other machines without a browser should always use this flow:

```bash
python3 scripts/youtube.py auth --manual
```

Open the printed URL on any device and approve access. The browser then tries to load `http://127.0.0.1:8923/?state=…&code=…`, which fails on another device; that's expected. Copy the whole address and finish with:

```bash
python3 scripts/youtube.py auth --code "http://127.0.0.1:8923/?state=...&code=..."
```

Or forward the port (`ssh -L 8923:127.0.0.1:8923 <host>`) and run plain `auth` on the remote machine.

## Signing Out

```bash
python3 scripts/youtube.py logout
```

This revokes the sign-in at Google and deletes `tokens.json` from the config folder. You can also remove the app's access at <https://myaccount.google.com/permissions>.
