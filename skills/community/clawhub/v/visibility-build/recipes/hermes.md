---
id: hermes
kind: platform
unlocks: [hermes]
source: https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/README.md, https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/aave-mcp.yaml, https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission, example package https://github.com/aave/skills/tree/7132f6e952f9100f16577c33774a1e63948f7fab/plugins/mcp (loaded 2026-11-08)
---
## Smallest version
A configuration-only portable Agent Plugin in the product's public repo (`plugin.json` + `mcp.json` pointing at the remote MCP URL + one skill telling the agent when/how to use the tools), and one `plugin-catalog/<name>.yaml` PR to NousResearch/hermes-agent pinned to that commit. No local code.

## Scaffold
Copy the shape of the listed `aave-mcp` package (plugins/mcp: `plugin.json`, `mcp.json`, `skills/`, README). No generator on the pages loaded.

## Fields the listings check
- `plugin.json`: `$schema` `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`, `name`, `version`, `description`, `author { name, url }`, `homepage`, `repository`, `license`, `keywords`, optional `extensions."com.nousresearch.hermes".servers.<id>.trust` (e.g. `"untrusted"` so Hermes asks before write tools).
- `mcp.json`: `$schema` `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`, `mcpServers.<id>: { "type": "streamable-http", "url": "https://<host>/mcp" }`. (Format taken from the listed example, not a spec page.)
- Catalog yaml: `name` (`[a-z0-9_-]{1,64}`), `repo` (https), `sha` (full 40-hex; branches/tags/short SHAs rejected), `subdir`, `description`, `maintainer`, `tier: community` (official/verified set by Nous only), `category` (`desktop|memory|platform|web|tools|voice|automation|models|general`), `requires_hermes` (SemVer floor like `">=0.21.6"`; the only floor for a portable package), `docs_url`, `version` (quoted), `image` (2:1 on a GitHub host), `screenshots` (<=6), `readme`, `platforms`, `title`, `capabilities { provides_tools, provides_hooks, provides_middleware, requires_env }` matching reality.
- Admission rules (selected): PR from the repo owner or a major contributor; no self-updating code; credentials only via Hermes (`requires_env`/`config_schema`, `oauth:` in plugin.yaml) never from files; respect approvals/unattended runs; disclose network calls, data handling and telemetry in the PR description and README; no compiled binaries.

## Steps
claude: add `plugins/<name>/plugin.json`, `mcp.json`, `skills/<skill>/SKILL.md`, README with disclosures (every tool call goes to <host>, what is logged, auth method)
approve: commit and push to the public repo; note the 40-char commit SHA
human: install Hermes and run `hermes plugins validate /path/to/plugins/<name> --install-deps` at that commit (claude may run it if Hermes is installed); fix failures, read warnings
claude: write `plugin-catalog/<name>.yaml` (sha pinned, `subdir`, `requires_hermes`, `category: tools`, disclosure-rich `description`)
human: try the plugin in Hermes against the live MCP and note results (local install command not documented on the pages loaded, unconfirmed)
approve: open the PR to NousResearch/hermes-agent with the yaml; description covers what it does, Hermes surfaces used, rule-13 disclosures; wait for catalog CI green

## Delegate
SKILL.md -> anthropic-skills:skill-creator. MCP server itself -> see mcp-remote.

## Verify locally
`hermes plugins validate /path/to/plugins/<name> --install-deps` passes at the pinned commit.
