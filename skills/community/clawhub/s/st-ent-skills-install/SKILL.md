---
name: st-ent-mcp-install
description: Install, wire, and verify the 699pic enterprise MCP server from the GitHub repository https://github.com/st699pic/st-ent-mcp . Use when the user asks to 安装 st-ent-mcp、接入 699pic MCP、配置 OpenClaw/Claude/Codex 的 MCP、克隆并注册这个仓库，或 when a local MCP install workflow is needed for the 699pic enterprise OpenAPI server.
---

# st-ent-mcp install

Use this skill to install and connect the `st-ent-mcp` repository as a local stdio MCP server.

## Goal

Set up the repo, provide required env vars, start the MCP server with Node.js, and register it in the local client/runtime.

## Default repo

- GitHub: `https://github.com/st699pic/st-ent-mcp`

## Preconditions

Check these first:

- Node.js 22+
- `git`, `node`, and `mcporter` must be installed before you try the local install flow.
- A valid `SERVICE_API_KEY`
- A reachable `SERVICE_API_BASE_URL`
- Use the smallest-scope `SERVICE_API_KEY` available for this integration.
- If you cannot fully audit the target repo, use an isolated environment such as a container or VM.
- Review the target repo, especially `mcp/server.js`, before running example scripts or starting the server.

## Trust and audit requirements

Do not run install commands blindly.

Minimum review checklist:

1. Verify the repository source and homepage match the expected project.
2. Inspect `README.md`, `package.json`, and `mcp/server.js`.
3. Confirm the server does not perform unexpected network calls, process spawning, or file writes outside the intended MCP/OpenAPI workflow.
4. Confirm required env vars are limited to `SERVICE_API_KEY` and `SERVICE_API_BASE_URL`.
5. Only continue once the code review is complete or the repo is isolated.

## Recommended install workflow

1. Clone or update the repo.
2. Verify the upstream repository identity and inspect the code, with focus on `mcp/server.js`.
3. Create a local `.env` or equivalent env export with `SERVICE_API_BASE_URL` and a least-privilege `SERVICE_API_KEY`.
4. If audit confidence is incomplete, move the repo into an isolated environment before any execution.
5. Verify the server starts with `node mcp/server.js`.
6. Register it with the target MCP client.
7. Run a smoke test (`tools/list` or one real call).

## OpenClaw / mcporter path

When wiring into the current OpenClaw workspace, prefer `mcporter` project config.

Typical registration shape:

```bash
mcporter config add st-ent-mcp \
  --command node \
  --arg /absolute/path/to/st-ent-mcp/mcp/server.js \
  --env SERVICE_API_BASE_URL=https://example.com \
  --env SERVICE_API_KEY=st_ent_xxx \
  --scope project
```

Then verify:

```bash
mcporter list st-ent-mcp --schema
```

## Claude / other MCP client path

Use a stdio config entry with:

- `command: node`
- `args: [/absolute/path/to/mcp/server.js]`
- `env.SERVICE_API_BASE_URL`
- `env.SERVICE_API_KEY`

## Notes

- Prefer absolute paths.
- Do not run `scripts/install-example.sh` until you have reviewed the target repo and intentionally exported the required env vars.
- If the server uses newline-delimited JSON over stdio, make sure the implementation matches the target MCP client framing.
- If OpenClaw already has a local fork/custom server, do not overwrite it blindly; compare first.
- The current skill format does not provide a dedicated machine-readable field for required env vars, so the requirement is documented explicitly here and in `references/repo.md`.

## Resources

Read `references/repo.md` for the repo-derived install facts.
Use `scripts/install-example.sh` as a reusable skeleton when creating a local install command.
