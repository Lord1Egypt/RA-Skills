# QingLong Skill Setup Guide

## Prerequisites

- `curl` and `jq` installed
- A running QingLong panel with Open API enabled

## Get QingLong API Credentials

1. Open QingLong web UI → **Configuration** → **Application**
2. Click **Create Application**
3. Select the scopes you need (crons / envs / scripts / logs / system)
4. Copy the **Client ID** and **Client Secret**

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `QINGLONG_URL` | Panel base URL (e.g. `http://192.168.1.100:5700`) |
| `QINGLONG_CLIENT_ID` | Open API Client ID |
| `QINGLONG_CLIENT_SECRET` | Open API Client Secret |

---

## Setup for Claude Code CLI

### 1. Set environment variables

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export QINGLONG_URL="https://ql.yourdomain.com"
export QINGLONG_CLIENT_ID="your_client_id"
export QINGLONG_CLIENT_SECRET="your_client_secret"
```

Then reload: `source ~/.bashrc`

### 2. Test the connection

```bash
scripts/ql.sh cron list
```

### 3. Use with Claude Code

Create a `CLAUDE.md` in your project root:

```markdown
# QingLong Panel Management

Use `scripts/ql.sh` to manage the QingLong panel.

Common commands:
- `scripts/ql.sh cron list` — List all cron jobs
- `scripts/ql.sh env list` — List environment variables
- `scripts/ql.sh system info` — Get system info

Full reference: see SKILL.md in this directory.
```

Then run: `claude "帮我查看青龙面板的定时任务"`

---

## Setup for OpenClaw

### Install

```bash
# Via ClawHub (recommended)
clawhub install qinglong-skills

# Or via npx
npx skills add NNNNzs/qinglong-skills

# Or manual copy
cp -r qinglong-skills ~/.openclaw/workspace/skills/qinglong
```

### Configure environment variables

Open `~/.openclaw/openclaw.json` and add under `skills.entries`:

```json5
{
  "skills": {
    "entries": {
      "qinglong": {
        "enabled": true,
        "env": {
          "QINGLONG_URL": "https://ql.yourdomain.com",
          "QINGLONG_CLIENT_ID": "your_client_id",
          "QINGLONG_CLIENT_SECRET": "your_client_secret"
        }
      }
    }
  }
}
```

Restart the gateway: `openclaw gateway restart`
