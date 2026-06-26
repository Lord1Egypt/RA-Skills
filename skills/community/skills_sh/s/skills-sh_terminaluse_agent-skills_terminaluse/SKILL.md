---
name: terminaluse
description: Create, edit, deploy, and interact with agents on TerminalUse. Use when user mentions "tu", "terminaluse", "deploy agent", "create agent", "edit agent", "update agent", "add skills", "agent task", "filesystem", or wants to build/modify/test/run an agent.
---

# TerminalUse

Build, deploy, interact with agents. Flow: init → deploy → create task → send messages.

Full docs: https://docs.terminaluse.com/llms-full.txt

## Default Rule For New Agents

When creating a new agent, use `tu init` by default.

Only skip `tu init` if the user explicitly instructs another approach (for example, modifying an existing agent template or a pre-scaffolded repository).

## CLI Setup

The `tu` CLI is provided by the `terminaluse` Python package. Before running any `tu` commands:

1. **Verify `tu` is available**:
   ```bash
   which tu || echo "tu CLI not found"
   ```

2. **If not installed**, ask user whether they would like to install it or if there's a venv they would like to source
   
3. Ensure you have auth configured:
   - Interactive/local: `tu login` then `tu whoami`
   - Non-interactive/automation: set `TERMINALUSE_API_KEY` (and optionally `TERMINALUSE_BASE_URL`)

## Context Requirement

Agent-scoped commands often default to `config.yaml` in the current directory when `--agent`/`--config` is omitted.

Before running agent-scoped commands without explicit flags:
```bash
ls config.yaml || echo "Not in agent directory"
```

Use explicit flags when possible:
- `--agent <namespace/name>` to avoid directory coupling
- `--config <path>` when working with a specific manifest

## Quick Reference

| Action | Command |
|--------|---------|
| Login | `tu login`, `tu whoami` |
| Init agent | `tu init` (creates agent directory, no need to mkdir first) |
| Deploy | `tu deploy -y` |
| List deployments | `tu ls` |
| Rollback | `tu rollback` |
| List filesystems | `tu fs ls` |
| List projects | `tu projects ls` |
| Add env var | `tu env add <KEY> -v <val> -e prod\|preview\|all [--secret]` |
| Import env file | `tu env import <file> -e <env> [--secret KEY]` |
| Create task | `tu tasks create --filesystem-id <fs-id> -m "message" [--json]` |
| Create task (auto-create fs) | `tu tasks create -p <project-id> -m "message" [--json]` |
| Send message | `tu tasks send <task-id> -m "message" [--json]` |
| List tasks | `tu tasks ls [--json]` |
| Get task details | `tu tasks get <task-id>` |

`tu fs` is the canonical filesystems command. `tu filesystems` is a supported alias.
`tu tasks ls <id>` is deprecated for single-task retrieval; use `tu tasks get <id>`.
Prefer `--json` for CI/automation and agent-to-agent interaction.

## Workflows

| Task | Reference |
|------|-----------|
| Create or edit an agent | [./workflows/create.md](./workflows/create.md) |
| Deploy to platform | [./workflows/deploy.md](./workflows/deploy.md) |
| Test/interact with agent | [./workflows/interact.md](./workflows/interact.md) |

You must look at the corresponding workflow files based on user intent.

## Anti-patterns

- Creating task without filesystem or project. Tasks either need a filesystem. If project is provided, a filesystem is auto-created in the project
- Modifying Dockerfile `ENTRYPOINT`/`CMD` → breaks deployment
- Trying to use the agent right after updating secrets. You must wait for the new version to become active. Check with `tu ls`

## Error Recovery

| Error | Action |
|-------|--------|
| Deploy fails | `tu ls <branch>` lists deployments events for branch → find FAILED → fix → redeploy |
| Need rollback | `tu rollback` |

## Docs/Skills Feedback

If docs or skills are wrong/unclear, ask user permission to send feedback to (include the feedback in the user request):
Never include any sensitive information.
```bash
curl -X POST 'https://uutzjuuimuclittwbvef.supabase.co/functions/v1/tu-docs-feedback' \
  -H 'Content-Type: application/json' \
  -d '{"feedback":"<issue>", "page":"<page URL> or section name"}'
```
