---
name: reply-cli
description: Manage sequences, contacts, email accounts, and schedules in Reply.io directly from the terminal. Use this skill when users want to view Reply.io stats, manage campaigns, or add contacts to sequences.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - REPLY_API_KEY
      bins:
        - node
        - curl
    primaryEnv: REPLY_API_KEY
---

# Reply.io CLI (reply-cli)

This skill provides a command-line interface to interact with [Reply.io](https://reply.io) via the official `reply-cli` tool. It allows you to manage outreach sequences, view statistics, manage contacts, and check connected email accounts directly from your terminal.

## Prerequisites & Setup

1. The tool requires Node.js >= 20.
2. It can be run on the fly via `npx reply-cli` without global installation.
3. You need a **Reply.io API Key** to authenticate. Get it from [Reply.io Settings > API](https://run.reply.io/Dashboard/Material#/settings/api).

### Providing Credentials

The skill requires `REPLY_API_KEY` to be set in the environment. Configure it in your OpenClaw config (`openclaw.json`) under the agent's env block:

```json
{
  "agents": {
    "defaults": {
      "env": {
        "REPLY_API_KEY": "your-api-key"
      }
    }
  }
}
```

Alternatively, add it to your `~/.openclaw/.env` file, or provide it as a Docker secret at `/run/secrets/reply_key`.

## Quick Reference / Commands

Use `npx reply-cli` (or just `reply` if installed globally) to execute commands. All commands support `--json` for easy machine parsing.

### 1. Sequences (Campaigns)
```bash
# List all sequences and basic stats
npx reply-cli sequences list --json

# Get details and email steps for a specific sequence
npx reply-cli sequences get <id> --json

# Start or Pause a sequence
npx reply-cli sequences start <id>
npx reply-cli sequences pause <id>

# View detailed per-step stats for a sequence
npx reply-cli sequences stats <id> --json

# Top 3 sequences by reply rate
npx reply-cli sequences stats --top
```

### 2. Contacts & Enrollment
```bash
# Search for a contact by email
npx reply-cli contacts search --email john@example.com --json

# Create a new contact
npx reply-cli contacts create --email john@example.com --first-name John --company Acme

# View campaign history and email activity for a contact
npx reply-cli contacts stats john@example.com --json

# Add contact to a sequence
npx reply-cli sequence-contacts add --contact john@example.com --sequence 12345

# Create and enroll in one step
npx reply-cli sequence-contacts add-new --contact jane@example.com --first-name Jane --sequence 12345

# Remove from a sequence
npx reply-cli sequence-contacts remove --contact john@example.com --sequence 12345
```

### 3. Accounts & Schedules
```bash
# List all connected email accounts
npx reply-cli accounts list --json

# List sending schedules
npx reply-cli schedules list --json
```

## Usage Guidelines for the Agent
1. **Always use `--json` or `--pretty`** when you need to parse the data for the user.
2. **Never hardcode or log the API key**. Suggest the user store it in their `.env` file or provide it securely via Docker Secrets.
3. **If a user asks for performance or stats**, use `sequences list` and `sequences stats <id>` to give them a detailed breakdown of opens, replies, bounces, and clicks.
