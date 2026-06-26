---
name: skill-to-agent
description: Convert OpenClaw skills into properly configured agents with correct workspace setup, binding, and orchestration. Solves common agent creation failures (thread binding errors, workspace isolation, improper session spawning). Use when creating agents from skills or when encountering agent binding errors.
---

# Skill-to-Agent

Transform any OpenClaw skill into a fully functional agent with proper workspace configuration and session management. Solves common failures like `thread=true is unavailable` and `mode="session" requires thread=true`.

## Quick Start

1. **Analyze skill** - Read SKILL.md to understand requirements
2. **Prepare workspace** - Create agent directory in `~/.openclaw/agents/`
3. **Configure agent** - Set up identity, tools, and memory strategy
4. **Spawn with correct binding** - Choose appropriate mode based on channel

## Workflow

### Phase 1: Skill Analysis
- Extract metadata from SKILL.md (name, description, triggers)
- Identify required tools and dependencies
- Determine agent type: isolated, thread-bound, or run-mode

### Phase 2: Workspace Setup
- Create agent directory with proper structure
- Copy skill files (references/, scripts/)
- Configure AGENTS.md, TOOLS.md, USER.md

### Phase 3: Agent Configuration
- Create SOUL.md and IDENTITY.md with skill personality
- Map skill tools to agent capabilities
- Set up memory strategy (MEMORY.md, memory/ directory)

### Phase 4: Agent Registration
- Add agent to OpenClaw's `agents.list` configuration
- Use `gateway` tool with `config.patch` action
- Include agent ID, name, workspace, and agentDir
- Gateway will restart to apply configuration

### Phase 5: Session Spawning
- Choose spawn strategy based on channel capabilities
- Execute with correct binding (thread-bound, isolated, run-mode)
- **CRITICAL:** Always set `cwd` to agent workspace directory
- Verify agent activation and tool access

## Reference Materials

For detailed guidance, refer to:

- **Usage Guide** - [usage-guide.md](references/usage-guide.md) - Complete workflow with examples
- **Troubleshooting** - [troubleshooting.md](references/troubleshooting.md) - Common errors and solutions
- **War Room Example** - [war-room-example.md](references/war-room-example.md) - Detailed conversion example

## Scripts

- `scripts/skill_to_agent.js` - Main conversion script

## Binding Strategies

| Scenario | Mode | Thread | Best For |
|----------|------|--------|----------|
| Discord/Telegram | session | true | Group discussions |
| WebChat/Control UI | run | false | One-shot tasks |
| Isolated Processing | session | false | Background work |
| Cron/Scheduled | run | false | Automated tasks |

**Decision Tree:**
- Channel supports threads? → Yes → `thread=true`, `mode=session`
- Isolated processing needed? → Yes → `thread=false`, `mode=session`
- Otherwise → `thread=false`, `mode=run`

## Common Errors & Solutions

**Error 1: `thread=true is unavailable`**
- Solution: Use `mode="run"` without thread binding
- Check channel capabilities first

**Error 2: `mode="session" requires thread=true`**
- Solution: Use isolated session mode
- `mode="session"`, `thread=false`, `runtime="subagent"`

**Error 3: Agent lacks tool access**
- Solution: Verify tools in TOOLS.md
- Update workspace configuration

**Error 4: Workspace files not accessible**
- Solution: Set `cwd` parameter when spawning agent
- Agent workspace must be at path specified in `cwd`
- Ensure agent has read/write permissions to workspace

**Error 5: Agent can't find its identity files**
- Solution: Always set `cwd` to agent workspace directory
- Agent reads IDENTITY.md, SOUL.md, etc. from current directory
- Test file access with simple `read` commands

**Error 6: Agent not recognized by OpenClaw system**
- Solution: Register agent in `agents.list` configuration
- Use `gateway` tool with `config.patch` action
- Gateway restart required for configuration changes
- Verify agent appears in configured agents list

## Critical: Workspace Directory (cwd)

When spawning an agent, **ALWAYS set the `cwd` parameter** to the agent's workspace directory:

```javascript
sessions_spawn({
  task: "Agent instructions...",
  label: "agent-name",
  runtime: "subagent",
  mode: "session", // or "run"
  cwd: "/Users/nimbletenthousand/.openclaw/agents/agent-name",
  timeoutSeconds: 300
});
```

Without `cwd`, the agent cannot find its identity files (IDENTITY.md, SOUL.md, etc.) and will fail to function properly.

## Critical: Agent Registration

After creating an agent workspace, **register it in OpenClaw's configuration**:

```javascript
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      list: [
        {
          id: "agent-name",
          name: "Agent Display Name",
          workspace: "/Users/nimbletenthousand/.openclaw/workspace",
          agentDir: "/Users/nimbletenthousand/.openclaw/agents/agent-name"
        }
      ]
    }
  }),
  note: "Added [agent-name] to agents configuration"
});
```

The gateway will restart automatically to apply the configuration. Without registration, the agent won't be recognized as a configured agent in the system.

## Quick Commands

```bash
# Check skill structure
node scripts/skill_to_agent.js --analyze --skill /path/to/skill

# Create agent workspace
node scripts/skill_to_agent.js --create --skill /path/to/skill --agent agent-name

# Spawn agent with correct binding
node scripts/skill_to_agent.js --spawn --agent agent-name --mode session --cwd /path/to/agent-workspace
```

## Best Practices

1. **Keep it lean** - Only copy essential skill files
2. **Test binding first** - Verify channel capabilities
3. **Monitor agent health** - Check `sessions_list` regularly
4. **Clean up properly** - Remove unused agent workspaces
5. **Document conversions** - Save configuration for future reference

## Next Steps

After creating an agent:
1. Verify it appears in `sessions_list`
2. Test tool accessibility
3. Configure heartbeat if needed
4. Set up orchestration with parent agent

For advanced usage and complete examples, see the reference files.