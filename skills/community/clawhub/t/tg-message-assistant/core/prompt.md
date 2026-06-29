---
name: tg-message-assistant
description: >
  Generate topic briefings from Telegram channels. Use this skill when the user mentions
  "briefing", "newsletter", "digest", "message summary", "channel recap", "generate report",
  "send briefing", "scheduled push", or "channel roundup". Also applies when users want
  to compile messages from multiple Telegram channels into structured summaries and
  deliver them to others.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "\U0001F4F0"
    homepage: https://github.com/TelyAgent/telyclaw-skills
---

# TG Message Assistant — Core Workflow

Help users fetch messages from Telegram channels, format them into Markdown briefings
using a selected template, deliver to Telegram contacts or via Gmail, and optionally
set up recurring scheduled generation.

## Workflow

### Step 1: Gather Configuration

When the user requests a briefing, confirm the following (skip any info already provided):

1. **Channel names** — Telegram channels to pull from (supports multiple, comma-separated).
   Users can provide channel names or usernames.
2. **Time range** — e.g. "past 24 hours", "past 7 days", or an explicit date range like
   "2026-05-15 to 2026-05-20".
3. **Template** — Choose from the four templates below. Default to "digest" if unspecified.
4. **Delivery** — Telegram contacts/groups/channels, Gmail addresses, or both.
5. **Schedule** — Whether to auto-generate on a recurring schedule (e.g. daily at 9:00 AM).

After each confirmation, echo it back clearly to ensure mutual understanding.

### Step 2: Fetch Channel Messages

Retrieve messages from each specified Telegram channel.

Steps:
1. If the user gave channel names instead of chat IDs, look up the channel
   to get its identifier first.
2. Based on the time range, estimate how many messages to fetch.
3. Fetch messages for each channel within the time window.
4. Collect key metadata: timestamp, message text, view count, forward count.

Guidelines:
- Fetch in batches if the channel is active — don't pull everything in one go.
- If a channel can't be found, tell the user immediately; don't silently skip it.
- Report progress when done: "Fetched Y messages across X channels."

### Step 3: Generate the Briefing

Pick one of the four templates based on user choice (default: `digest`).
Read the corresponding `assets/templates/<name>.md` file for the exact output format and rules,
then apply it to the fetched messages.

| Template | File | Best for |
|----------|------|----------|
| Digest | `assets/templates/digest.md` | Quick scanning, one-line-per-message |
| Detailed Summary | `assets/templates/detailed.md` | In-depth reading, preserves data & stats |
| Topical | `assets/templates/topical.md` | Cross-channel topic grouping |
| Insights | `assets/templates/insights.md` | Conclusions, trends, actionable takeaways |

### Step 4: Deliver the Briefing

Show the finished briefing to the user for review before sending.
Then deliver via the method(s) the user specified.

#### Telegram Delivery

Send the briefing to the specified Telegram recipients.

- If the user specified a contact name, resolve it to the correct chat identifier first.
- Telegram imposes a 4096-character limit per message. Split long briefings into
  multiple segments at natural paragraph boundaries. Label each segment "(1/3)", "(2/3)", etc.
- Report back when sending is complete.

#### Gmail Delivery

Send the briefing via email.

- Ensure the required email tools are installed and authorized before first use.
- On first use, guide the user through the authorization flow if needed.
- Send parameters: to, subject (`{Channel names} Briefing · {date range}`), and the
  full Markdown briefing as body.
- The email body is the complete Markdown briefing, readable as-is.

#### Dual Delivery

If the user chose both Telegram and Gmail, execute them in sequence.
The two channels are independent.

### Step 5: Set Up Schedule (Optional)

If the user wants recurring generation, set up a recurring scheduled task:

1. Confirm the cron expression meaning with the user (e.g. "This will run every day at 9:00 AM, correct?").
2. Create the scheduled task linked to the briefing configuration.
3. Tell the user the task has been created and how to view or cancel it.

Cron expression examples:
- `0 9 * * *` — Every day at 9:00 AM
- `0 9 * * 1` — Every Monday at 9:00 AM
- `0 9,17 * * *` — Every day at 9:00 AM and 5:00 PM

---

## Interaction Principles

- **Proactive completion** — When the user's request is incomplete, ask for all
  missing information in one round; don't stretch it across multiple turns.
- **Echo and confirm** — Restate key config (channels, time range, recipients)
  before execution to ensure alignment.
- **Transparent progress** — Report progress while fetching messages; mention
  which template is being used when generating.
- **Clear error handling** — If a channel can't be found, messages are empty, or
  sending fails, clearly explain the issue and suggest a fix.
- **Preview before sending** — Always show the briefing to the user for review
  before delivering it.
