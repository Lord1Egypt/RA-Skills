---
name: sqlbot-workspace-dashboard
description: Manage SQLBot workspaces, datasources, ask-data flows, and dashboards, including listing and switching workspace or datasource context, asking questions against a datasource, listing dashboards, viewing dashboard details, and exporting dashboards as PNG or PDF.
argument-hint: "[list-workspaces | switch-workspace <workspace> | list-datasources [--workspace <workspace>] | switch-datasource <datasource> [--workspace <workspace>] | ask <question> [--workspace <workspace>] [--datasource <datasource>] [--chat-id <id>] | list-dashboards [--workspace <workspace>] [--node-type folder|leaf] [--flat] | show-dashboard <dashboard-id> [--workspace <workspace>] | export-dashboard <dashboard-id> --format png|pdf [--workspace <workspace>] [--output <path>]]"
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read, Glob, Grep
---

# SQLBot Workspace Datasource Dashboard Skill

Use this skill when the user wants to operate SQLBot workspaces, datasources, ask-data flows, or dashboards from Claude Code / Agent Skills compatible tools.

This skill wraps the bundled script `${CLAUDE_SKILL_DIR}/sqlbot_skills.py`.

## Before you run it

1. Check whether `${CLAUDE_SKILL_DIR}/.env` exists.
2. If it does not exist, tell the user to copy `${CLAUDE_SKILL_DIR}/.env.example` to `.env` and fill in:
    - `SQLBOT_BASE_URL`
    - `SQLBOT_API_KEY_ACCESS_KEY`
    - `SQLBOT_API_KEY_SECRET_KEY`
3. For export requests, if Playwright is missing, tell the user to install it with:

```bash
pip install playwright
playwright install chromium
```

## Map the user request to one of these commands

- List workspaces:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" workspace list
```

- Switch workspace:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" workspace switch "<workspace>"
```

- List datasources:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" datasource list --workspace "<workspace>"
```

- Switch datasource:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" datasource switch "<datasource>" --workspace "<workspace>"
```

- Ask data:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" ask "<question>" --datasource "<datasource>" --workspace "<workspace>"
```

or continue an existing chat:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" ask "<question>" --chat-id 101
```

- List dashboards:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" dashboard list --workspace "<workspace>"
```

Optional flags:
- `--node-type folder`
- `--node-type leaf`
- `--flat`

- Show dashboard:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" dashboard show "<dashboard-id>" --workspace "<workspace>"
```

- Export dashboard:

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" dashboard export "<dashboard-id>" --workspace "<workspace>" --format png --output "./dashboard.png"
```

or

```bash
python3 "${CLAUDE_SKILL_DIR}/sqlbot_skills.py" dashboard export "<dashboard-id>" --workspace "<workspace>" --format pdf --output "./dashboard.pdf"
```

## Execution rules

- Prefer exact workspace names or numeric workspace IDs when switching or querying.
- Prefer exact datasource names or numeric datasource IDs when switching or asking.
- Remember that SQLBot dashboard APIs are scoped by the current workspace and current user, so switch workspace before listing or showing dashboards in another workspace.
- Datasource list and ask-data also depend on the current workspace context.
- SQLBot has no standalone datasource-switch API, so `datasource switch` updates the skill-local state file and `ask` uses that datasource by default when starting a new chat.
- Preserve the user's requested output path for exports whenever possible.
- If the user does not provide an export path, use the script default.
- Summarize the command output clearly after execution.

## Additional resources

- Detailed usage and installation notes: [reference.md](reference.md)
- Repository overview and manual usage examples: [README.md](README.md)
