---
name: github-mcp
description: Use the GitHub MCP server (github-mcp-server) to browse repositories, manage issues and PRs, analyze code, search files, monitor CI/CD workflows, and automate GitHub operations. Triggers when user asks to search code, manage GitHub issues/PRs, view commits, analyze repository structure, check CI/CD status, fork repos, create branches, or any GitHub-related operations that require API access. Works with local stdio-based github-mcp-server binary or remote HTTP endpoint (https://api.githubcopilot.com/mcp/).
---

# GitHub MCP Skill

This skill provides integrated GitHub operations via the GitHub MCP Server.

## Quick Start

### Remote Server (HTTP) — Recommended

```bash
mcporter config add github --type http --url "https://api.githubcopilot.com/mcp/" --header "Authorization=Bearer ${GITHUB_TOKEN}"
```

### Local Stdio Server

Download from: https://github.com/github/github-mcp-server/releases

```bash
mcporter config add github --type stdio --command "github-mcp-server" --env "GITHUB_TOKEN=${GITHUB_TOKEN}"
```

## Common Operations

### List available tools
```bash
mcporter list github --schema
```

### Call a tool
```bash
mcporter call github.<tool_name> key=value
```

## Reference

See `references/tools.md` for full tool schema and examples.
