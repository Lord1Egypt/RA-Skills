# Agent Security Checks

## What to Examine

From `config.agents.list[]`, check each agent's permissions.

## Check 1: Tool Profile

**Location**: `agents.list[].tools.profile`

| Profile | Risk Level | Notes |
|---------|------------|-------|
| `minimal` | 🟢 Low | Read, basic tools only |
| `standard` | 🟡 Medium | Includes exec |
| `coding` | 🟡 Medium | Full coding capabilities |
| `full` | 🟠 High | Everything enabled |
| (none specified) | Check defaults | Inherits from `agents.defaults` |

## Check 2: Dangerous Tool Combinations

**Location**: `agents.list[].tools.alsoAllow` and `.deny`

**Critical tools to flag**:
- `exec` - Shell command execution
- `gateway` - Can modify bot configuration
- `browser` - Web browsing (prompt injection surface)
- `sessions_spawn` - Can create sub-agents
- `cron` - Can schedule persistent tasks
- `nodes` - Remote execution on paired devices

**Finding Pattern**:
```
Agent exposed to external input (non-main) + exec + no deny = 🔴 Critical
Agent with gateway access (non-main) = 🔴 Critical (can reconfigure itself)
Agent with browser + exec = 🟠 High (fetch-and-execute chain)
```

## Check 3: Workspace Sharing

**Location**: `agents.list[].workspace`

**Risk if multiple agents share workspace**:
- One compromised agent can affect others
- Cross-agent data leakage possible

**Check**:
- Count agents sharing same workspace path
- If >1 and any has external exposure: 🟡 Medium
- **Exception**: Single-user deployment = 🟢 Low (no cross-user risk)
- **Exception**: All agents are internal subagents = 🟢 Low

## Check 4: Subagent Permissions

**Location**: `agents.list[].subagents.allowAgents`

**Risk Assessment**:
- Main agent can spawn subagents listed here
- If subagent has more permissions than caller context: 🟡 Medium
- If subagent list includes `"*"` (all agents): 🟠 High

## Check 5: Message Tool as Exfiltration Vector

**Location**: `agents.list[].tools.alsoAllow`

**If agent has `message` tool**:
- Can send data to external channels
- Combined with file read = data exfiltration

**Risk Assessment**:
```
External-facing agent + message + Read = 🟠 High (exfiltration path)
Internal agent + message = 🟢 Low (expected for notifications)
```

## Check 6: Main Agent Special Risks

The `main` agent typically has:
- Direct user interaction
- Highest trust level
- Access to most tools

**Check main agent specifically for**:
- Overly broad `subagents.allowAgents`
- External channel connections without proper isolation

## Contextual Factors

Consider the agent's purpose:

1. **Coding agent** (like dev-expert)
   - exec is expected and necessary
   - Focus on channel exposure instead

2. **Data analyst agent**
   - Should NOT need exec or browser
   - Flag if present: 🟠 High

3. **External-facing agent** (public bot)
   - Should have minimal tools
   - Any exec/browser/gateway: 🔴 Critical
