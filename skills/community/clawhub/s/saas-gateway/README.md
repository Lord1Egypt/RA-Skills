# Saas Gateway

Release-ready ClawHub skill package generated from `targetSkills/saas-gateway`.

- Skill name: `saas-gateway`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Unified SaaS integration gateway via api.aisa.one (AISA gateway, v3.1): manage OAuth auth for third-party SaaS apps (Gmail/Slack/GitHub/Notion etc.), tool execution, tool-router sessions, triggers, webhooks, MCP servers, and usage stats. Use when connecting third-party SaaS accounts, running cross-SaaS tools, managing MCP servers, setting up triggers, or checking usage. Keywords: SaaS gateway, connect app, OAuth link, run tool, auth config, tool router, MCP server, trigger, webhook, connected account, usage stats
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
