# Skill-to-Agent

Transform OpenClaw skills into fully functional, properly configured agents with correct workspace setup, binding strategies, and system registration.

## Overview

This skill provides a methodology for converting any OpenClaw skill into an autonomous agent. It solves common agent creation failures including thread binding errors, workspace isolation issues, file access problems, and improper session spawning.

## Quick Start

### The 5-Phase Methodology

1. **Skill Analysis** - Extract requirements from SKILL.md
2. **Workspace Setup** - Create agent directory with proper structure
3. **Agent Configuration** - Craft identity, memory, and tool access
4. **Agent Registration** - Add to OpenClaw's `agents.list` configuration
5. **Session Spawning** - Launch with correct binding for the channel

### Critical Success Factors

- **Always set `cwd`** - Agent workspace directory for file access
- **Always register agents** - Use `gateway config.patch` to add to configuration
- **Choose correct binding** - Based on channel capabilities (thread-bound, isolated, run-mode)

## Common Problems Solved

### Thread Binding Errors
- `thread=true is unavailable because no channel plugin registered subagent_spawning hooks`
- `mode="session" requires thread=true so the subagent can stay bound to a thread`

### Workspace Issues  
- Agents can't find identity files (IDENTITY.md, SOUL.md)
- File permission and access problems
- Memory configuration failures

### Registration Problems
- Agents not recognized by OpenClaw system
- Configuration not applied after creation

## File Structure

```
skill-to-agent/
├── README.md           # This overview
├── SKILL.md            # Main skill documentation
├── _meta.json          # Skill metadata
└── references/         # Detailed guides
    ├── usage-guide.md      # Complete workflow
    ├── troubleshooting.md  # Error solutions  
    └── war-room-example.md # Conversion example
```

## Usage Examples

### Create a Weather Agent from Weather Skill

```javascript
// Phase 1-3: Create workspace and configure
// ... create agent directory and files ...

// Phase 4: Register agent
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      list: [
        {
          id: "weather-agent",
          name: "Weather Specialist",
          workspace: "/Users/username/.openclaw/workspace",
          agentDir: "/Users/username/.openclaw/agents/weather-agent"
        }
      ]
    }
  }),
  note: "Added weather-agent to agents configuration"
});

// Phase 5: Spawn with correct binding
sessions_spawn({
  task: "Check Amsterdam weather forecast",
  label: "weather-check",
  runtime: "subagent",
  mode: "run",
  cwd: "/Users/username/.openclaw/agents/weather-agent",
  timeoutSeconds: 180
});
```

## Binding Strategy Decision Tree

```
Is channel Discord/Telegram? → Yes → thread=true, mode=session
                              ↓ No
Is isolated processing needed? → Yes → thread=false, mode=session  
                                ↓ No
Default: thread=false, mode=run
```

## Skill vs Agent

| Aspect | Skill | Agent |
|--------|-------|-------|
| **Format** | SKILL.md + references/ | Full workspace with identity files |
| **Execution** | Guides AI behavior | Autonomous operation |
| **Memory** | None | Persistent memory/ directory |
| **Binding** | N/A | Thread-bound, isolated, or run-mode |
| **Registration** | Auto-discovered | Must be added to `agents.list` |

## Testing Methodology

This skill has been proven by creating the `skill-converter-agent`:

1. ✅ Created workspace with all identity files
2. ✅ Configured tools and memory strategy  
3. ✅ Registered in OpenClaw configuration via `gateway config.patch`
4. ✅ Successfully spawned and tested
5. ✅ Gateway restarted and recognized agent

## Getting Help

- Read `SKILL.md` for complete documentation
- Check `references/troubleshooting.md` for common errors
- Review `references/war-room-example.md` for detailed conversion example
- OpenClaw Discord: `#skills` channel

## License & Contributions

This skill is part of the OpenClaw ecosystem. Contributions and improvements welcome.

---

**Remember:** Skill-to-agent conversion transforms instructional templates into autonomous actors with their own identity, memory, and workspace isolation.