---
name: validate-plugin
description: Validate a Claude Code plugin structure, frontmatter, and MCP tool references
argument-hint: "[plugin-path]"
allowed-tools: mcp__claude-flow__transfer_plugin-info Bash Read Glob Grep
---

# Validate Plugin

Validate that a plugin follows the correct Claude Code plugin format.

## When to use

After creating or modifying a plugin, run validation to catch structural issues before publishing.

## Checks performed

1. **Directory structure** — `.claude-plugin/plugin.json` exists at plugin root
2. **plugin.json schema** — required fields present (name, description, version)
3. **Skills** — each skill in `plugin.json.skills` has a matching `skills/<name>/SKILL.md`
4. **Commands** — each command in `plugin.json.commands` has a matching `commands/<name>.md`
5. **Agents** — each agent in `plugin.json.agents` has a matching `agents/<name>.md`
6. **SKILL.md frontmatter** — each skill has `name`, `description`, and `allowed-tools`
7. **Agent frontmatter** — each agent has `name`, `description`, and `model`
8. **No files in wrong locations** — skills/commands/agents not inside `.claude-plugin/`
9. **MCP tool references** — tools in `allowed-tools` are valid `mcp__claude-flow__*` identifiers

## Steps

1. Read the plugin's `plugin.json`
2. For each skill, command, and agent declared, verify the file exists
3. For each SKILL.md, verify frontmatter has required fields
4. For each agent .md, verify frontmatter has required fields
5. Report pass/fail for each check with actionable fix suggestions
