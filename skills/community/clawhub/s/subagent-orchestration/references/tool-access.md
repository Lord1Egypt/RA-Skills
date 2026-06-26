# Subagent Tool Access Reference

## Tool Availability by Spawn Configuration

### Default Subagent (no toolsAllow)
Available: exec, read, write, edit, process, sessions_yield
NOT available: ollama_web_search, ollama_web_fetch, sessions_spawn, subagents, sessions_list, sessions_history

### With toolsAllow: ["ollama_web_search", "ollama_web_fetch"]
Available: exec, read, write, edit, process, sessions_yield + web tools
NOT available: sessions_spawn, subagents, sessions_list, sessions_history

### With maxSpawnDepth >= 2 (orchestrator)
Available: exec, read, write, edit, process, sessions_yield, sessions_spawn, subagents, sessions_list, sessions_history
NOT available: web tools (unless also specified in toolsAllow)

## Combining Access
Multiple tools can be combined in toolsAllow:
```
toolsAllow: ["ollama_web_search", "ollama_web_fetch", "sessions_spawn", "subagents"]
```

## lightContext
Always use `lightContext: true` unless the subagent explicitly needs full conversation history. Prevents context overflow which can crash the gateway.