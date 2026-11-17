# SKILL.md — Slack Integration for OpenClaw

---

## 1. Metadata

**Name:** `slack-integration`  
**Description:** Send messages, list channels, query users, upload files, and manage scheduled messages in Slack via the Web API. All in English.  
**Trigger Phrases:** See Section 2.  
**Capabilities:** See Section 3.  
**Prerequisites:** See Section 4.  
**Output Format:** See Section 6.  
**Caveats:** See Section 9.

---

## 2. Trigger Phrases

The following natural English phrases activate this skill. The user does not need to use the exact wording — any reasonable paraphrase of these intents will trigger it.

1. "Send a message to #general in Slack"
2. "Post a message to the engineering channel"
3. "Message someone on Slack by email"
4. "Send a direct message to John on Slack"
5. "Upload this file to Slack"
6. "Post a message to Slack with a block kit attachment"
7. "List all channels in our Slack workspace"
8. "What channels do we have in Slack?"
9. "Find a user on Slack by name"
10. "Look up a Slack user by their email address"
11. "Who is this Slack user? — @sarah.chen"
12. "Schedule a message in Slack for tomorrow at 9am"
13. "Create a scheduled Slack message"
14. "Delete a scheduled Slack message"
15. "Search messages in Slack"
16. "Find messages in Slack about the deployment"
17. "Set my Slack status to DND"
18. "What's the Slack user ID for someone?"

---

## 3. Capabilities

This skill is modular. Each capability maps to one or more Slack Web API methods. The skill performs only the capability requested; it never combines unrelated operations.

### 3.1 Send a Plain Text Message

**Slack API:** `POST https://slack.com/api/chat.postMessage`  
**Auth:** Bot Token (`xoxb-...`)  
**Scope required:** `chat:write`

Send a plain-text message to a public channel, private channel, or DM. The target can be specified by channel name (`#general`), channel ID (`C0123456789`), or user ID (`U0123456789`) for DMs.

**Required arguments:**
- `channel` — channel name, ID, or user ID
- `text` — message text (max 40,000 characters)

**Optional arguments:**
- `username` — display name override for the bot
- `icon_emoji` — emoji icon (e.g., `:robot_face:`)
- `thread_ts` — to reply in a thread, pass the parent message's `ts`

### 3.2 Send a Formatted Block Kit Message

**Slack API:** `POST https://slack.com/api/chat.postMessage`  
**Auth:** Bot Token  
**Scope required:** `chat:write`

Send a richly formatted message using Slack Block Kit (sections, dividers, buttons, images, etc.). Pass a JSON array of blocks as the `blocks` argument. The skill will validate the block structure before sending.

**Required arguments:**
- `channel` — channel name, ID, or user ID
- `blocks` — JSON array of Block Kit objects

**Optional arguments:**
- `text` — plain-text fallback (required by Slack if using blocks, used in notifications/previews)

### 3.3 List Channels / Conversations

**Slack API:** `GET https://slack.com/api/conversations.list`  
**Auth:** Bot Token  
**Scope required:** `channels:read` (public), `groups:read` (private), `im:read` (DMs), `mpim:read` (MPIMs)

Retrieve a paginated list of all channels the bot has access to. Supports filtering by type (`public_channel`, `private_channel`, `im`, `mpim`).

**Optional arguments:**
- `types` — comma-separated list: `public_channel,private_channel,im,mpim`
- `limit` — results per page (default 200, max 1000)
- `cursor` — pagination cursor from a previous response

**Returns:** An array of channel objects with `id`, `name`, `is_private`, `num_members`, `topic`, `purpose`.

### 3.4 Get User Info

**Slack API:** `GET https://slack.com/api/users.info`  
**Auth:** Bot Token  
**Scope required:** `users:read`

Look up a Slack user by their user ID. Returns profile, status, timezone, and workspace info.

**Required arguments:**
- `user` — Slack user ID (e.g., `U0123456789`)

**Alternative lookup by email:**
1. `GET https://slack.com/api/users.lookupByEmail?email=<email>`  
   Scope required: `users:read`

**Returns:** User object with `id`, `name`, `real_name`, `profile` (avatar, title, email, phone), `status`, `tz`.

### 3.5 Upload a File

**Slack API:** `POST https://slack.com/api/files.uploadV2`  
**Auth:** Bot Token  
**Scope required:** `files:write`

Upload a file to a Slack channel or DM. The file can be referenced by local path (the skill will read and upload it) or by URL.

**Required arguments:**
- `filename` — name of the file to display in Slack
- `channel` — target channel or user ID
- `file` — local file path or HTTPS URL

**Optional arguments:**
- `title` — file title
- `initial_comment` — comment to include with the file
- `filetype` — MIME type hint (e.g., `pdf`, `png`, `json`)

**Note:** Files are uploaded in a single request with `multipart/form-data`. Maximum file size is 1 GB for paid workspaces, 256 MB for free.

### 3.6 Scheduled Messages

**Slack APIs:**
- `POST https://slack.com/api/chat.scheduleMessage` — create
- `GET https://slack.com/api/chat.scheduledMessages.list` — list
- `DELETE https://slack.com/api/chat.deleteScheduledMessage` — delete

**Auth:** Bot Token  
**Scopes required:** `chat:write` (post), `chat:write` (list/delete)

Create a message to be delivered at a specified time. Delete or list pending scheduled messages.

**Create required arguments:**
- `channel` — target channel
- `text` — message text
- `post_at` — Unix timestamp or ISO 8601 datetime string for delivery time

**Create optional arguments:**
- `blocks` — Block Kit JSON array
- `thread_ts` — reply in thread

**List required arguments:** none (returns all scheduled messages for the app)  
**List optional arguments:**
- `channel` — filter to a specific channel
- `limit` — max results (default 100)

**Delete required arguments:**
- `channel` — channel ID where the scheduled message will post
- `scheduled_message_id` — ID returned from scheduleMessage

### 3.7 Search Messages

**Slack API:** `GET https://slack.com/api/search.messages`  
**Auth:** Bot Token  
**Scope required:** `search:read`

Search message history across all visible channels.

**Required arguments:**
- `query` — search query string (supports Slack search operators like `from:@user`, `in:#channel`, `has:file`, `on:2024-01-15`)

**Optional arguments:**
- `count` — results per page (default 100, max 100)
- `page` — page number
- `sort` — `score` (default) or `timestamp`
- `sort_dir` — `asc` or `desc`

**Returns:** Matches with message text, channel, user, timestamp, and highlights.

### 3.8 Set User Status (Bot Own Status)

**Slack API:** `POST https://slack.com/api/users.profile.set`  
**Auth:** Bot Token  
**Scope required:** `users.profile:write`

Set the bot user's custom status emoji and status text. Also used to set away/dnd status via `users.setPresence`.

**Required arguments for status:**
- `profile` — JSON object with `status_emoji` and `status_text`

**Required arguments for presence:**
- `presence` — `auto` (active) or `away` (away)

---

## 4. Prerequisites

### 4.1 Slack App & Bot Token

You must create a Slack App with a Bot Token before using this skill.

1. Go to **https://api.slack.com/apps** and click **Create New App** → **From scratch**.
2. Give the app a name (e.g., "OpenClaw Integration"), pick your workspace, and click **Create App**.
3. Under **Features**, click **OAuth & Permissions** in the left sidebar.
4. Scroll to **Bot Token Scopes** and add these scopes depending on which capabilities you need:

| Capability | Required Scopes |
|---|---|
| Send plain message | `chat:write` |
| Send Block Kit message | `chat:write` |
| List channels | `channels:read`, `groups:read`, `im:read`, `mpim:read` |
| Get user info | `users:read` |
| Lookup by email | `users:read` |
| Upload file | `files:write` |
| Scheduled messages | `chat:write` |
| Search messages | `search:read` |
| Set status | `users.profile:write`, `users:write` |

5. Click **Install to Workspace** → **Allow** to generate a Bot Token (format: `xoxb-...`)
6. Copy and securely store the Bot Token — **it cannot be retrieved later** (you can regenerate it)

### 4.2 Environment Variable Setup

Add to your OpenClaw environment config (`~/.openclaw/.env` or as OpenClaw config vars):

```bash
SLACK_BOT_TOKEN=REDACTED-SECRET
SLACK_SIGNING_SECRET=your-signing-secret-here   # for webhook verification (optional)
```

### 4.3 Enable App Home / Interactivity (Optional)

For interactive blocks (buttons, modals, shortcuts):
1. In your Slack App, go to **Interactivity & Shortcuts**
2. Toggle on **Interactivity**
3. Set the **Request URL** to your OpenClaw gateway URL + `/webhooks/slack/interactive`

---

## 5. API Helper Functions

These helper patterns should be used by the AI when executing any Slack API call.

### 5.1 Base Request Pattern

```bash
# Always include the Authorization header with the Bot Token
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H 'Authorization: Bearer REDACTED-SECRET' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "channel": "#general",
    "text": "Hello from OpenClaw!"
  }'
```

### 5.2 Response Validation

Every Slack API response includes an `ok` boolean field:
- `ok: true` → success, proceed
- `ok: false` → failure, check `error` field

**Always validate before reporting to the user:**
```
If response.ok == false:
  → Report error: "Failed to send message. Slack error: [error_code]. Suggestion: [fix]"
```

### 5.3 Rate Limit Handling

Slack rate limits most APIs at **1,000 calls per minute** per workspace. For some endpoints (e.g., `chat.postMessage`), it's **1 per second** per channel.

**Best practice:** When sending many messages in sequence, add a `sleep 1` between calls per channel.

### 5.4 Token Refresh

Bot Tokens do not expire unless manually revoked. No refresh logic needed.

---

## 6. Output Format

### Success — Message Sent

```
✅ Message sent to #channel-name
📝 Text: "Hello team, the deployment is complete."
👤 Sent as: OpenClaw Bot
🕐 Timestamp: 2026-07-04 20:35:12 UTC
🔗 View in Slack: https://slack.com/archives/C0123456789/p1234567890
```

### Success — Channels Listed

```
✅ Found 8 channels
#engineering   (42 members, public)  — "Engineering team discussions"
#general       (128 members, public) — "Company-wide announcements"
#random        (89 members, public)  — "Non-work banter"
...
```

### Success — User Found

```
✅ User found: Sarah Chen
🆔 User ID: U0123456789
📧 Email: sarah.chen@company.com
💼 Title: Senior Software Engineer
🕐 Timezone: America/Los_Angeles
🟢 Status: active
```

### Error — Not in Channel

```
❌ Failed to send message
Reason: "not_in_channel" — Bot is not a member of #channel-name
Fix: Add the bot to the channel first (/invite @OpenClaw Bot in Slack)
```

### Error — Rate Limited

```
❌ Rate limited by Slack
Retry after: ~1 second
Suggestion: Space out message sends by at least 1 second per channel
```

---

## 7. Example Conversations

### Example 1: Send a Plain Message

**User:** "Send a message to #engineering saying the new build is ready for testing"

**AI:** "Sure, posting to #engineering now..."

**Execute:**
1. Validate channel name `#engineering`
2. POST to `chat.postMessage` with text "The new build v2.4.1 is ready for testing. Please review here: https://ci.example.com/builds/241"

**AI:** "✅ Message sent to #engineering
📝 The new build v2.4.1 is ready for testing. Please review here: https://ci.example.com/builds/241
🕐 Sent at 20:35 UTC"

---

### Example 2: Find User by Email

**User:** "Who is alex.johnson@company.com on Slack?"

**AI:** "Looking up alex.johnson@company.com..."

**Execute:**
1. GET `users.lookupByEmail?email=alex.johnson@company.com`
2. Parse returned user object

**AI:** "✅ Found it!
👤 Alex Johnson
🆔 U9876543210
📧 alex.johnson@company.com
💼 Product Manager
🏢 Operations
🕐 Timezone: America/New_York"

---

### Example 3: Schedule a Reminder Message

**User:** "Schedule a message in #releases for tomorrow at 9am reminding the team about the deploy"

**AI:** "Scheduling a message for tomorrow at 9:00 AM UTC..."

**Execute:**
1. Calculate tomorrow 9am UTC as Unix timestamp
2. POST to `chat.scheduleMessage` with channel `#releases`, text, and `post_at` timestamp

**AI:** "✅ Scheduled message created
📢 Channel: #releases
📝 'Friendly reminder: the production deploy is scheduled for 2pm UTC today. Please ensure all PRs are reviewed and your feature flags are configured. — The OpenClaw Bot'
⏰ Scheduled for: 2026-07-05 09:00:00 UTC
🆔 Scheduled ID: Q1234567890 (save this if you need to cancel)
🔗 Will appear at: https://slack.com/archives/C0123456789"

---

## 8. Installation Guide

### Step-by-Step Setup

**Step 1: Create a Slack App**

1. Go to https://api.slack.com/apps and click **Create New App**
2. Select **From scratch** (not "From an app manifest")
3. Name it "OpenClaw Integration" (or any name you prefer)
4. Select your workspace from the dropdown
5. Click **Create App**

**Step 2: Configure Bot Token Scopes**

1. In the left sidebar, click **OAuth & Permissions**
2. Scroll to **Bot Token Scopes** and click **Add an OAuth Scope**
3. Add all scopes for the capabilities you need (see Section 4.1 table)
4. Scroll up and click **Install to Workspace**
5. Click **Allow** — you'll see a Bot Token starting with `xoxb-`
6. Copy this token (you'll use it in Step 4)

**Step 3: Enable Necessary App Features**

For each feature you want to use, enable it in the app:

- **Messaging (chat.postMessage):** No extra feature needed — just `chat:write` scope
- **File Uploads:** In left sidebar → **Permissions** → Add `files:write` scope, reinstall app
- **Scheduled Messages:** No extra feature needed
- **Search:** In left sidebar → **Permissions** → Add `search:read` scope, reinstall app

**Step 4: Configure OpenClaw**

Add to `~/.openclaw/.env`:

```bash
SLACK_BOT_TOKEN=REDACTED-SECRET
SLACK_SIGNING_SECRET=4a7b9c2d8e1f3g6h5j0k2l4m6n8p9q
```

Then restart OpenClaw to load the new environment variables.

**Step 5: Add the Bot to a Channel**

1. Open Slack and go to the channel you want the bot in
2. Type `/invite` and select **Add apps to this channel**
3. Search for your app name and add it

Alternatively, the bot can be invited programmatically via `conversations.invite` (requires `channels:write` scope).

**Step 6: Test the Setup**

Try: "List all channels in Slack" — you should get back a list of channels the bot has access to.

---

## 9. Caveats

### Common Errors

| Error Code | Meaning | Fix |
|---|---|---|
| `not_in_channel` | Bot not added to target channel | Invite bot via `/invite @AppName` in Slack |
| `channel_not_found` | Channel name/ID invalid | Use channel ID (`C0123456789`) not name |
| `users_not_found` | Email lookup failed | Check email spelling; user may not be in workspace |
| `file_incorrect_permissions` | File read failed | Ensure file path is accessible to OpenClaw process |
| `missing_scope` | Token missing required scope | Reinstall app with needed scope in OAuth & Permissions |
| `token_revoked` | Bot token was invalidated | Regenerate token in Slack App dashboard |
| `rate_limited` | Too many API calls | Wait and retry with 1-second delay per channel |

### Rate Limits (Critical)

| Endpoint | Limit |
|---|---|
| `chat.postMessage` | 1/second per channel |
| `conversations.list` | 1/minute per workspace |
| `users.list` | 1/minute per workspace |
| Most other methods | ~1,000/minute per workspace |

**Always implement a 1-second sleep between consecutive `chat.postMessage` calls to the same channel.**

### Channel ID vs Name

- Always prefer **channel ID** (`C0123456789`) over channel name (`#engineering`)
- Channel names can be ambiguous; IDs are unique and unambiguous
- You can get the channel ID from `conversations.list` output

### Bot Token Security

- Bot Tokens (`xoxb-...`) are **permanent and non-expiring** unless manually revoked
- Never expose the token in logs or user-facing messages
- If compromised: go to **OAuth & Permissions** → **Tokens for Your Workspace** → **Revoke** → recreate

### Message Formatting

- Plain text messages support basic formatting: `<@U0123456789>` for user mention, `<#C0123456789>` for channel link, `<!channel>` for @channel, `<!here>` for @here
- For advanced formatting (tables, images, buttons), use **Block Kit** (Section 3.2)

### Scheduled Messages

- Scheduled messages can be set up to **120 days in the future**
- You cannot edit a scheduled message after creation — delete and recreate instead
- The scheduled message will appear as if sent by the bot at the specified time

### File Upload Limits

- Free workspaces: **256 MB** per file
- Paid workspaces: **1 GB** per file
- Supported file types: all standard types (pdf, png, jpg, mp4, csv, zip, etc.)

### Search Limitations

- Free workspaces: **~10,000 recent messages** searchable
- Paid workspaces: **90 days** of message history
- Search results include only messages the bot's token has access to

### Block Kit Validation

- Slack validates block JSON structure — malformed blocks return `parse.error` in the response
- Always include a `text` fallback field when sending blocks (required for notifications)
- Block total size must be under **3,000 characters** per message
