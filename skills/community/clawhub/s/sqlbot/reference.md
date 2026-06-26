# SQLBot Workspace Dashboard Skill Reference

This repository is packaged as an **Agent Skills** compatible skill directory.

Core files:

- `SKILL.md`: skill entrypoint for Claude Code / Agent Skills tools
- `sqlbot_skills.py`: bundled Python script executed by the skill
- `.env.example`: template for required SQLBot connection settings
- `README.md`: manual usage guide

## Supported operations

- List accessible workspaces
- Switch current workspace
- List datasources in the current or specified workspace
- Switch current datasource in the skill-local state file
- Ask data questions with a specified datasource or the current switched datasource
- List dashboards in the current or specified workspace
- Show dashboard details
- Export dashboard to `jpg` (default), `png`, or `pdf`

## Required configuration

Create `.env` next to `SKILL.md`:

```bash
cp .env.example .env
```

Minimum required fields:

```bash
SQLBOT_BASE_URL=http://127.0.0.1:8000/api/v1
SQLBOT_API_KEY_ACCESS_KEY=your-access-key
SQLBOT_API_KEY_SECRET_KEY=your-secret-key
```

Optional fields:

```bash
SQLBOT_API_KEY_TTL_SECONDS=300
SQLBOT_TIMEOUT=30
SQLBOT_BROWSER_PATH=/path/to/chrome
SQLBOT_STATE_FILE=/absolute/path/to/.sqlbot-skill-state.json
```

## Claude Code installation

Personal skill:

```bash
mkdir -p ~/.claude/skills/sqlbot-workspace-dashboard
cp -R /path/to/SQLBot-skills/* ~/.claude/skills/sqlbot-workspace-dashboard/
```

Project skill:

```bash
mkdir -p .claude/skills/sqlbot-workspace-dashboard
cp -R /path/to/SQLBot-skills/* .claude/skills/sqlbot-workspace-dashboard/
```

Then invoke it from Claude Code with:

```text
/sqlbot-workspace-dashboard
```

and pass an instruction such as:

```text
/sqlbot-workspace-dashboard list workspaces
/sqlbot-workspace-dashboard switch workspace 2
/sqlbot-workspace-dashboard list datasources in workspace 2
/sqlbot-workspace-dashboard switch datasource 12
/sqlbot-workspace-dashboard ask 本周销售额是多少
/sqlbot-workspace-dashboard list dashboards in workspace 2
```

## OpenClaw / Agent Skills compatible tools

This skill follows the Agent Skills directory format (`SKILL.md` + supporting files). If your OpenClaw setup supports Agent Skills, copy this entire directory into the tool's configured skills location and keep the file structure unchanged.

## Notes

- SQLBot dashboard APIs are scoped by the current workspace and current user.
- SQLBot datasource list and ask-data flows also depend on the current workspace.
- SQLBot does not expose a standalone datasource-switch API, so the skill persists the current datasource in a local state file.
- Export relies on the SQLBot frontend preview route, but the script derives that URL automatically from `SQLBOT_BASE_URL`.
- The script authenticates with SQLBot API Key headers: `X-SQLBOT-ASK-TOKEN: sk <signed-jwt>`.
