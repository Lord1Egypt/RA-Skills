# Adapting x-bookmark-triage to Your Workspace

## ⚠️ Before You Start: Remove Persona References

This skill was authored for a specific user and AI assistant. Before deploying, replace these in `scripts/triage-url.js`:

- System prompt `"You are a knowledge triage assistant..."` — already generic in v1.1+
- User prompt `"for the user's work"` — replace with your name/role if desired
- Topic taxonomy `#agent-systems` — customize to your domains (see Customizing Topics below)

If you see references to "Watson", "Jeremy", or "@jeremyknowsvf" in any script, replace with your own identity.

---

## Change the Target Discord Channel

In `scripts/triage-url.js` and `scripts/poll-channel.js`, update:
```js
const CHANNEL_ID = '1481057788590297302'; // ← your channel ID here
```

## Customize the Triage Prompt

In `scripts/triage-url.js`, find the `userPrompt` string. Key sections to adapt:

**Relevance context** — replace Jeremy's context with yours:
```
// Change this line:
Be concise, opinionated, and specific to Jeremy's work with OpenClaw, VeeFriends, and AI agents.
// To your context:
Be concise, opinionated, and specific to [your name]'s work with [your domain].
```

**Topic taxonomy** — replace the topic list with your own domains:
```
// In the userPrompt, replace the Topic guide section:
Topic guide (pick ONE primary topic):
- "#ai" — your AI/tech work
- "#client-x" — client X projects
- "#marketing" — content and growth
...
```

**Tier thresholds** — adjust if your work priorities differ. The default 9–10/7–8/5–6/3–4/1–2 breakdown maps well to most knowledge workflows.

## Refresh Token Auto-Rotation

X rotates refresh tokens on each use. To avoid manual updates, implement a write-back:

```js
// In getAccessToken(), after saving token cache:
if (data.refresh_token && data.refresh_token !== REFRESH_TOKEN) {
  // Option A: Write to a secrets file your infra reads at startup
  fs.writeFileSync('/path/to/secrets/x-refresh-token.txt', data.refresh_token);

  // Option B: Update a .env file
  // (requires file-based env management)

  // Option C: Call a secrets manager API (1Password, Vault, etc.)
  // spawnSync('op', ['item', 'edit', 'x-oauth2', `refresh_token=${data.refresh_token}`]);
}
```

The scripts write to `data/x-oauth2-new-refresh-token.txt` as a fallback signal.

## Multiple X Accounts

To support multiple accounts, parameterize the token cache path and credentials:

```js
const ACCOUNT = process.env.X_ACCOUNT || 'default'; // e.g. 'jeremy', 'brand'
const TOKEN_CACHE = path.join(WORKSPACE, `data/x-oauth2-token-cache-${ACCOUNT}.json`);
```

Run separate cron jobs with different `X_ACCOUNT` and credential env vars.

## Skip Unbookmarking

Pass `--no-unbookmark` to `backlog-sweep.js`, or remove the `deleteBookmark()` call from `bookmark-poll.js`. Useful if you want to keep bookmarks and only mirror them to Discord.

## Read-Only Mode (no bookmark.write scope)

If your app only has `bookmark.read`:
1. Remove `deleteBookmark()` calls from both poll scripts
2. Remove `bookmark.write` from your OAuth scope request
3. The triage pipeline still works — bookmarks just won't be cleared

## Non-Discord Output

Replace `postToDiscord()` in `triage-url.js` with your preferred output:
- **Slack**: POST to incoming webhook URL
- **Notion database**: POST to Notion API `/pages` endpoint
- **Local markdown file**: `fs.appendFileSync('knowledge.md', card + '\n\n')`
- **Telegram**: POST to Bot API `/sendMessage`

---

## Running Without OpenClaw

The core triage pipeline works standalone on macOS/Linux. You don't need OpenClaw.

**Credential setup without OpenClaw:**

Create a `.env` file in the skill root:
```
DISCORD_BOT_TOKEN=your_bot_token
ANTHROPIC_DEFAULT_KEY=your_anthropic_key
X_OAUTH2_CLIENT_ID=your_client_id
X_OAUTH2_CLIENT_SECRET=your_client_secret
X_OAUTH2_REFRESH_TOKEN=your_refresh_token
KNOWLEDGE_INTAKE_CHANNEL_ID=your_channel_id
```

`run-poll.sh` automatically loads `.env` if present.

**Scheduling without OpenClaw:**

Use a cron job:
```
*/2 * * * * cd /path/to/x-bookmark-triage && bash scripts/run-poll.sh >> /tmp/knowledge-intake.log 2>&1
```

Or use the launchd template in `scripts/ai.watson.knowledge-intake-poll.plist` — customize all `/PATH/TO/` placeholders and `YOUR_*` values, then:
```bash
launchctl load ~/Library/LaunchAgents/ai.watson.knowledge-intake-poll.plist
```
