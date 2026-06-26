---
name: qinglong
version: "1.0.2"
description: >
  Manage QingLong (青龙) panel via REST API — cron jobs, environment variables,
  scripts, dependencies, subscriptions, logs and system operations.
  Use this skill whenever the user mentions QingLong, 青龙面板, scheduled tasks
  on a self-hosted panel, or wants to manage cron jobs / env vars / scripts on
  their QingLong instance, even if they don't say "QingLong" explicitly.
  Also trigger for requests like "帮我查看定时任务", "添加环境变量", "运行脚本",
  "禁用任务", "查看日志" when the context is a QingLong panel.
metadata: {"openclaw": {"emoji": "🐉", "requires": {"bins": ["curl", "jq"], "env": ["QINGLONG_URL", "QINGLONG_CLIENT_ID", "QINGLONG_CLIENT_SECRET"]}}}
---

# QingLong Panel Skill

Control your [QingLong (青龙)](https://github.com/whyour/qinglong) scheduled task panel via REST API using `scripts/ql.sh`.

📦 ClawHub: https://clawhub.ai/nnnnzs/qinglong-skills
📖 GitHub: https://github.com/NNNNzs/qinglong-skills

> First time setup? See [references/setup.md](references/setup.md) for installation and credential configuration.

> **Security note**: This skill only communicates with the user's own self-hosted QingLong panel using credentials they provide. It does not access any external services or exfiltrate data.

---

## How to approach user requests

When the user asks to manage their QingLong panel, follow this pattern:

1. **List first, then act** — before modifying anything, list the relevant resources so you know the IDs. For example, before disabling a cron job, run `cron list` to find its ID.
2. **Batch when possible** — most commands accept multiple IDs. If the user wants to disable all JD-related env vars, search first then pass all IDs in one call.
3. **Confirm destructive actions** — for delete operations, show the user what will be deleted before running the command.
4. **Check logs on failure** — if a cron job fails, use `cron log <id>` to fetch the latest log and surface the error.

---

## Quick Reference

### Cron Jobs

```bash
scripts/ql.sh cron list                                    # List all
scripts/ql.sh cron get <id>                                # Get detail
scripts/ql.sh cron create --command "task x.js" --schedule "0 0 * * *" --name "Task"
scripts/ql.sh cron update <id> --name "New Name"
scripts/ql.sh cron delete <id>                             # Delete (supports multiple IDs)
scripts/ql.sh cron run <id>                                # Run now
scripts/ql.sh cron stop <id>                               # Stop
scripts/ql.sh cron enable <id> / disable <id>              # Enable / Disable
scripts/ql.sh cron pin <id> / unpin <id>                   # Pin / Unpin
scripts/ql.sh cron log <id>                                # View latest log
```

### Environment Variables

```bash
scripts/ql.sh env list                                     # List all
scripts/ql.sh env list "JD"                                # Search by keyword
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
scripts/ql.sh token refresh                                # Force refresh
scripts/ql.sh token show                                   # Show cached
scripts/ql.sh token clear                                  # Clear cache
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | Wrong credentials | Verify `QINGLONG_CLIENT_ID` and `QINGLONG_CLIENT_SECRET` |
| `Connection refused` | Panel unreachable | Check `QINGLONG_URL` is accessible; try `curl $QINGLONG_URL` |
| `Scope error` | Missing API scope | In QingLong UI → Application → edit app → add the required scope |
| Token keeps expiring | Clock skew | The script auto-refreshes; if it loops, run `token clear` then retry |
| Command not found | Missing deps | Ensure `curl` and `jq` are installed: `which curl jq` |

If a cron job fails silently, fetch its log: `scripts/ql.sh cron log <id>`

---

## API Reference

Full API documentation: [references/api.md](references/api.md)

| Resource | Base path |
|----------|-----------|
| Cron Jobs | `/crons` |
| Envs | `/envs` |
| Scripts | `/scripts` |
| Dependencies | `/dependencies` |
| Subscriptions | `/subscriptions` |
| Logs | `/logs` |
| System | `/system` |
| Config Files | `/configs` |
