---
name: wip-repo-permissions-hook
description: Repo visibility guard. Blocks repos from going public without a -private counterpart.
license: MIT
interface: [cli, module, mcp, hook, plugin]
metadata:
  display-name: "Repo Visibility Guard"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - visibility-check
    - org-audit
    - public-gate
  requires:
    bins: [node, gh]
  openclaw:
    requires:
      bins: [node, gh]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-repo-permissions-hook"
        bins: [wip-repo-permissions]
        label: "Install via npm"
    emoji: "🔒"
compatibility: Requires node, gh (GitHub CLI). Node.js 18+.
---

# Repo Permissions Hook

## What This Does

Prevents repos from being made public unless a `-private` counterpart exists on GitHub. Protects internal plans, todos, and development context from accidental exposure.

## The Rule

Every repo that goes public must have a `{name}-private` repo. The private repo holds `ai/` folders with plans, todos, dev updates, and notes. The public repo has the same code without `ai/`.

Forks of external projects are exempt.

## How to Use

### Check before changing visibility
```bash
node cli.js check <org>/<repo>
```

### Audit all public repos
```bash
node cli.js audit <org>
```

### Install as Claude Code hook
Add to `~/.claude/settings.json` under `hooks.PreToolUse` with matcher `"Bash"`.

### Install as OpenClaw plugin
Copy to `~/.ldm/extensions/wip-repo-permissions-hook/` and restart gateway.

### MCP

Tools: `repo_permissions_check`, `repo_permissions_audit`

Add to `.mcp.json`:
```json
{
  "wip-repo-permissions": {
    "command": "node",
    "args": ["/path/to/tools/wip-repo-permissions-hook/mcp-server.mjs"]
  }
}
```
