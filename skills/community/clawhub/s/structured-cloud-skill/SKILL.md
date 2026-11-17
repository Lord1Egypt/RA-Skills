---
name: structured-cloud
description: "Use when a Hermes Agent, Open Claw, OpenCode, or other MCP-capable assistant needs to read, manage, or edit Structured tasks through Structured Cloud. Includes the Structured MCP endpoint, OAuth setup pattern, and task operations such as viewing, creating, updating, completing, and deleting tasks."
---

# Structured Cloud MCP

Use this skill when the user wants an agent to work with Structured Cloud tasks through MCP.

## What this skill covers

- View today's schedule, upcoming days, or the inbox.
- Create tasks with title, time, duration, color, icon, alerts, and subtasks.
- Update tasks by rescheduling or changing properties.
- Complete tasks.
- Delete tasks.
- Manage recurring tasks when the user's Structured plan supports them.

## Core MCP details

- MCP server URL: `https://mcp.structured.app/mcp`
- Structured Cloud account is required.
- Authentication uses Structured Cloud login and email verification.

## OpenCode setup reference

If the host app supports OpenCode-style MCP configuration, use this pattern:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "structured": {
      "type": "remote",
      "url": "https://mcp.structured.app/mcp",
      "enabled": true,
      "oauth": {
        "clientId": "89b2893e-d218-4476-907b-e382fc145666"
      }
    }
  }
}
```

After configuration, authenticate with the host app's MCP flow, then retry the task.

## Interaction rules

- Prefer direct task actions over summarizing when the user asks for a change.
- If the agent cannot reach MCP, explain that Structured Cloud must be connected in the host app first.
- Use the user's wording for task titles, dates, and labels unless it would create ambiguity.
- Ask a clarifying question only when the task cannot be resolved unambiguously.

## Good prompt patterns

- "Show me what is on my timeline today."
- "Create a blue task for tomorrow afternoon to clean the kitchen."
- "Move today's tasks one hour later."
- "Mark all completed tasks done."

## Notes for Hermes-style agents

- This skill is designed to be compatible with agents that load SKILL.md files and can work with externally configured MCP servers.
- If Hermes Agent or Open Claw exposes a custom MCP connector, point it at the Structured Cloud endpoint above and follow the host app's auth flow.