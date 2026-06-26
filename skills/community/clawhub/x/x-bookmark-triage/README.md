# x-bookmark-triage

Turns X/Twitter bookmarks into structured knowledge cards posted to a Discord channel. Captures tweet content, scores relevance with Claude Haiku, assigns tier (1–10), freshness, and topic tags — then unbookmarks automatically so your list stays clean.

**What it does:**
- Polls X bookmarks 2× daily and triages each one
- One-time backlog sweep to drain an existing bookmark list
- Manual drop handler — post a URL to your channel for immediate triage
- Posts formatted cards to Discord with tier, freshness, topic, and proposed action
- Auto-unbookmarks after capture (optional)

**Works standalone** — no OpenClaw required. See [references/adapting.md](references/adapting.md) for setup without OpenClaw.

---

## Install

```bash
git clone https://github.com/jeremyknows/x-bookmark-triage
cd x-bookmark-triage
node scripts/setup-check.js
```

---

## Setup

1. **Create an X OAuth 2.0 app** at [developer.x.com](https://developer.x.com)  
   Free tier works. Needs `bookmark.read` scope (+ `bookmark.write` to auto-unbookmark).  
   See [references/oauth-setup.md](references/oauth-setup.md) for step-by-step.

2. **Create a Discord bot** at [discord.com/developers](https://discord.com/developers/applications)  
   Bot needs `Send Messages` permission in your target channel.

3. **Get an Anthropic API key** at [console.anthropic.com](https://console.anthropic.com)

4. **Set environment variables:**
   ```bash
   export DISCORD_BOT_TOKEN=your_bot_token
   export ANTHROPIC_DEFAULT_KEY=your_anthropic_key
   export X_OAUTH2_CLIENT_ID=your_client_id
   export X_OAUTH2_CLIENT_SECRET=your_client_secret
   export KNOWLEDGE_INTAKE_CHANNEL_ID=your_discord_channel_id
   ```
   Or create a `.env` file in the skill root (loaded automatically by `run-poll.sh`).

5. **Authorize X OAuth:**
   ```bash
   node scripts/x-oauth2-authorize.js
   ```

6. **Verify setup:**
   ```bash
   node scripts/setup-check.js
   ```

7. **Test with a manual triage:**
   ```bash
   node scripts/triage-url.js "https://x.com/someone/status/123" --source "manual drop"
   ```

8. **Schedule polling** (pick one):
   ```bash
   # Option A: cron (every 2 min)
   */2 * * * * cd /path/to/x-bookmark-triage && bash scripts/run-poll.sh >> /tmp/knowledge-intake.log 2>&1

   # Option B: launchd (macOS)
   # Edit scripts/ai.watson.knowledge-intake-poll.plist — fill in all YOUR_* placeholders
   launchctl load ~/Library/LaunchAgents/ai.watson.knowledge-intake-poll.plist
   ```

---

## Usage

### Natural language (in your agent)

> "Triage my bookmarks"  
> "Set up the bookmark pipeline"  
> "Drain my bookmark backlog"  
> "Drop this URL for triage: https://x.com/..."

### CLI commands

```bash
# Drain full bookmark backlog
node scripts/backlog-sweep.js

# Dry run — triage only, no unbookmark
node scripts/backlog-sweep.js --dry-run

# Limit to N bookmarks
node scripts/backlog-sweep.js --limit 5

# Triage a single URL
node scripts/triage-url.js "https://x.com/..." --source "manual drop"

# Start the channel poll daemon
bash scripts/run-poll.sh
```

### Script reference

| Script | Purpose |
|--------|---------|
| `bookmark-poll.js` | Scheduled poll — fetches latest 20 bookmarks, triages + unbookmarks |
| `backlog-sweep.js` | One-time sweep — paginates all bookmarks, triages + unbookmarks each |
| `poll-channel.js` | Channel poller — watches Discord channel for dropped URLs every 2 min |
| `triage-url.js` | Core triage engine — called by all three scripts |
| `run-poll.sh` | Wrapper for poll-channel.js — loads credentials from `.env` or plist |
| `setup-check.js` | Pre-flight check — validates Node.js version and required env vars |
| `x-oauth2-authorize.js` | Interactive OAuth 2.0 PKCE flow — saves tokens to secrets file |

---

## Card Format

Cards posted to Discord look like:

```
🟡 Tier 6 · evergreen · #ai #tool
**Claude Artifacts for rapid prototyping**
Why it matters: Enables instant HTML/JS prototypes without local setup — useful for demos.
Key Features: Inline rendering, shareable links, zero-config deployment
Proposed Action: Add to knowledge doc
📅 Freshness: evergreen
🏷️ Tags: #tool #ai #ux
🔗 https://x.com/anthropic/status/...
```

Tier guide: 1–4 = noise (silent skip for automated polls), 5–7 = relevant, 8–10 = high-value.

---

## Configuration

| Env var | Required | Description |
|---------|----------|-------------|
| `DISCORD_BOT_TOKEN` | ✅ | Discord bot token |
| `ANTHROPIC_DEFAULT_KEY` | ✅ | Anthropic API key |
| `X_OAUTH2_CLIENT_ID` | ✅ | X app client ID |
| `X_OAUTH2_CLIENT_SECRET` | ✅ | X app client secret |
| `X_OAUTH2_REFRESH_TOKEN` | ✅ | OAuth 2.0 refresh token (from auth script) |
| `KNOWLEDGE_INTAKE_CHANNEL_ID` | ✅ | Discord channel ID to post cards to |
| `OPENCLAW_WORKSPACE` | ⬜ | Workspace root for data files (defaults to `../../..`) |
| `X_OAUTH2_SECRETS_FILE` | ⬜ | Path to secrets JSON file (for token rotation persistence) |

---

## Refresh Token Rotation

X rotates refresh tokens on each use. When rotation is detected, scripts:
1. Update the in-process env var immediately (current run continues)
2. Save the new token to `data/x-oauth2-new-refresh-token.txt`
3. Log a warning: `⚠️ Refresh token rotated — update X_OAUTH2_REFRESH_TOKEN in your env`

**You must update `X_OAUTH2_REFRESH_TOKEN`** in your `.env` file or plist after each rotation, or the next run will fail with `invalid_grant`. The new token is always at `data/x-oauth2-new-refresh-token.txt`.

---

## Security

- OAuth tokens stored with `0o600` permissions (owner read/write only)
- Token values never printed to stdout
- `.env` and all token files are in `.gitignore`
- `emit-event.sh` integration is optional and degrades gracefully if absent

---

## Limitations

- X free tier rate limits: ~10 bookmark reads/15 min. Large backlogs may take time.
- Discord channel must already exist — the bot won't create it.
- Freshness scoring is heuristic (Claude-based), not date-aware for all content types.
- Unbookmark requires `bookmark.write` OAuth scope.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Auth failed: invalid_grant` | Stale refresh token | Copy `data/x-oauth2-new-refresh-token.txt` → update env var |
| Cards not posting to Discord | Wrong channel ID or bot missing permissions | Verify `KNOWLEDGE_INTAKE_CHANNEL_ID` and bot `Send Messages` perm |
| `setup-check.js` fails | Missing env var | Set the missing variable listed in the output |
| Bookmark count shows 0 | Bookmarks list is empty or API rate-limited | Wait 15 min and retry |
| `emit-event.sh not available` | Running without OpenClaw | Normal — core functionality is unaffected |

---

## File Structure

```
x-bookmark-triage/
├── SKILL.md                          # Agent skill instructions
├── README.md                         # This file
├── LICENSE.txt                       # MIT License
├── .gitignore                        # Excludes data/, secrets, .env
├── scripts/
│   ├── triage-url.js                 # Core triage engine
│   ├── bookmark-poll.js              # Scheduled bookmark poll
│   ├── backlog-sweep.js              # One-time backlog sweep
│   ├── poll-channel.js               # Discord channel URL poller
│   ├── run-poll.sh                   # Wrapper with credential loading
│   ├── setup-check.js                # Pre-flight env validation
│   ├── x-oauth2-authorize.js         # Interactive OAuth flow
│   └── ai.watson.knowledge-intake-poll.plist  # launchd template
└── references/
    ├── oauth-setup.md                # X OAuth 2.0 setup guide
    ├── cron-setup.md                 # Scheduling guide
    └── adapting.md                   # Customization + standalone setup
```

---

## License

MIT — see [LICENSE.txt](LICENSE.txt)
