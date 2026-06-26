# 🐉 qinglong-skills

OpenClaw / Claude Code skill for controlling [QingLong (青龙)](https://github.com/whyour/qinglong) panel.

**[中文文档](README_zh-CN.md)**

## Features

- **Cron Jobs** — list, create, update, delete, run, stop, enable/disable, pin/unpin, view logs
- **Environment Variables** — list, create, update, delete, enable/disable
- **Scripts** — list, read, save, run, stop, delete
- **Dependencies** — list, install, reinstall, cancel, delete (node/linux/python3)
- **Subscriptions** — list, run, stop, enable/disable, delete, view logs
- **Logs** — list, read, delete
- **System** — info, config, update, reload, command run/stop, auth reset
- **Config Files** — list, read, save

## Prerequisites

- `curl` and `jq` installed on your system
- A QingLong panel with Open API enabled

## Get QingLong API Credentials

1. Open your QingLong web UI
2. Go to **Configuration** → **Application**
3. Click **Create Application**
4. Select the scopes you need (e.g. crons, envs, scripts, logs, system)
5. Copy the **Client ID** and **Client Secret**

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `QINGLONG_URL` | Panel base URL (e.g. `http://192.168.1.100:5700`) | ✅ |
| `QINGLONG_CLIENT_ID` | Open API Client ID | ✅ |
| `QINGLONG_CLIENT_SECRET` | Open API Client Secret | ✅ |

---

## Option 1: Use with OpenClaw

### Install the Skill

**Option A: Via ClawHub (recommended)**

```bash
clawhub install qinglong-skills
```

**Option B: Via npx**

```bash
npx skills add NNNNzs/qinglong-skills
```

**Option C: Use `extraDirs` (recommended for development)**

Add to `~/.openclaw/openclaw.json`:

```json5
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/qinglong-skills"]
    }
  }
}
```

**Option D: Copy to workspace skills directory**

```bash
cp -r qinglong-skills ~/.openclaw/workspace/skills/qinglong
```

### Configure Environment Variables in `openclaw.json`

Open `~/.openclaw/openclaw.json` and find (or create) the `skills.entries.qinglong` object:

```json5
{
  "skills": {
    "entries": {
      "qinglong": {
        "enabled": true,
        "env": {
          "QINGLONG_URL": "https://ql.yourdomain.com",
          "QINGLONG_CLIENT_ID": "your_client_id_here",
          "QINGLONG_CLIENT_SECRET": "your_client_secret_here"
        }
      }
    }
  }
}
```

**Full path:** `skills.entries.qinglong.env.QINGLONG_URL` / `QINGLONG_CLIENT_ID` / `QINGLONG_CLIENT_SECRET`

> ⚠️ Note: The Gateway UI does **not** render input forms for `skills.entries.*.env`. You must edit `openclaw.json` directly or use the raw JSON editor in the Gateway UI.

After editing, restart the gateway:

```bash
openclaw gateway restart
```

Verify the skill is loaded:

```bash
openclaw skills list
```

You should see `🐉 qinglong` with status `✓ ready`.

### Usage with OpenClaw Agent

The agent will automatically use the skill when you ask about QingLong operations.

---

## Option 2: Use with Claude Code CLI

This skill is **not tied to OpenClaw**. Claude Code (or any AI agent that can execute shell commands) can use it directly.

### Setup

1. Clone the repo:

```bash
git clone git@github.com:NNNNzs/qinglong-skills.git
cd qinglong-skills
```

2. Set system environment variables (add to `~/.bashrc` or `~/.zshrc`):

```bash
export QINGLONG_URL="https://ql.yourdomain.com"
export QINGLONG_CLIENT_ID="your_client_id_here"
export QINGLONG_CLIENT_SECRET="your_client_secret_here"
```

Then reload:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

3. Test the script directly:

```bash
./scripts/ql.sh cron list
```

### Usage with Claude Code

You can use this skill with Claude Code in several ways:

**Method 1: Pass SKILL.md as context**

```bash
claude-code --context SKILL.md "帮我查看青龙面板有哪些定时任务"
```

**Method 2: Copy instructions into your prompt**

Tell Claude Code:

> 你是一个青龙面板管理助手。使用 scripts/ql.sh 脚本操作青龙面板。
> 参考 SKILL.md 了解可用命令。
> 环境变量已配置好，直接调用脚本即可。

**Method 3: Use in CLAUDE.md project file**

Create a `CLAUDE.md` in your project root:

```markdown
# QingLong Panel Management

Use `scripts/ql.sh` to manage the QingLong panel.

Available commands:
- `scripts/ql.sh cron list` — List all cron jobs
- `scripts/ql.sh env list` — List environment variables
- `scripts/ql.sh system info` — Get system info

Full reference: see SKILL.md in this directory.
```

Then run:

```bash
claude-code "帮我查看青龙面板的定时任务"
```

Claude Code will read `CLAUDE.md` and know how to use the script.

---

## CLI Reference

### Cron Jobs

```bash
scripts/ql.sh cron list                                    # List all
scripts/ql.sh cron get <id>                                # Get detail
scripts/ql.sh cron create --command "task x.js" --schedule "0 0 * * *" --name "Task"
scripts/ql.sh cron update <id> --name "New Name"
scripts/ql.sh cron delete <id>                             # Delete (supports multiple IDs)
scripts/ql.sh cron run <id>                                # Run now
scripts/ql.sh cron stop <id>                               # Stop running
scripts/ql.sh cron enable <id>                             # Enable
scripts/ql.sh cron disable <id>                            # Disable
scripts/ql.sh cron pin <id> / unpin <id>                   # Pin / Unpin
scripts/ql.sh cron log <id>                                # View log
```

### Environment Variables

```bash
scripts/ql.sh env list                                     # List all
scripts/ql.sh env list "JD"                                # Search
scripts/ql.sh env create --name "KEY" --value "VALUE" --remarks "note"
scripts/ql.sh env update --id <id> --name "KEY" --value "NEW_VALUE"
scripts/ql.sh env delete <id>
scripts/ql.sh env enable <id> / disable <id>
```

### Scripts

```bash
scripts/ql.sh script list                                  # List all
scripts/ql.sh script get --file "test.js"                  # View content
scripts/ql.sh script save --file "test.js" --content "console.log('hi')"
scripts/ql.sh script run --file "test.js"                  # Run
scripts/ql.sh script stop --file "test.js"                 # Stop
scripts/ql.sh script delete --file "test.js"               # Delete
```

### Dependencies

```bash
scripts/ql.sh dep list                                     # List all
scripts/ql.sh dep install --name "axios" --type 0          # 0=node, 1=linux, 2=python3
scripts/ql.sh dep reinstall <id>
scripts/ql.sh dep delete <id>
```

### Subscriptions

```bash
scripts/ql.sh sub list / run <id> / stop <id> / enable <id> / disable <id> / delete <id>
```

### System

```bash
scripts/ql.sh system info                                  # System info
scripts/ql.sh system config                                # System config
scripts/ql.sh system check-update                          # Check updates
scripts/ql.sh system reload                                # Reload
scripts/ql.sh system command-run --command "task test.js"  # Run command
scripts/ql.sh system auth-reset --username admin --password newpass
```

### Token Management

```bash
scripts/ql.sh token refresh                                # Force refresh token
scripts/ql.sh token show                                   # Show cached token
scripts/ql.sh token clear                                  # Clear cached token
```

---

## Documentation

- [SKILL.md](SKILL.md) — Full skill documentation
- [README_zh-CN.md](README_zh-CN.md) — 中文文档
- [references/api.md](references/api.md) — Complete QingLong API reference

## License

MIT
