# RTK Configuration Guide

## Default behavior

By default, RTK uses **all available command handlers** — no configuration needed. This is recommended for maximum token savings.

## Custom configuration (optional)

RTK config lives at `~/.config/rtk/config.toml` (Linux/macOS).

### Enable only specific commands

If you want to limit RTK to a subset of commands (e.g., git-only):

```toml
[commands]
# Explicitly enable only what you need
enabled = ["git", "grep", "find", "ls"]
```

### Disable specific commands (keep rest enabled)

```toml
[commands]
# Disable specific handlers if their output is too compressed
disabled = ["docker", "read"]
```

### Filter aggressiveness level

```toml
[filter]
# Options: minimal | default | aggressive
# - minimal: light deduplication only
# - default: smart filtering + grouping (recommended)
# - aggressive: signatures only, maximum compression
level = "default"
```

### Per-command overrides

```toml
[commands.read]
level = "aggressive"   # Only show function signatures for file reads

[commands.git]
level = "default"

[commands.test]
level = "minimal"      # Keep more context for test failures
```

## Config for different use cases

### React Native / TypeScript developer

```toml
[filter]
level = "default"

[commands.test]
level = "minimal"   # Tests need more context

[commands.tsc]
level = "aggressive"  # TypeScript errors group well
```

### Minimal setup (just git + grep + find)

```toml
[commands]
enabled = ["git", "grep", "find", "ls", "diff"]
```

### Maximum compression (CI-like)

```toml
[filter]
level = "aggressive"
```

## Agent-specific notes

### OpenClaw / Беляш

OpenClaw uses the `exec` tool for shell commands. RTK hooks (installed via `rtk init`) **do NOT apply** to exec tool calls automatically.

**Solution**: The skill instructs the agent to always prefix commands manually with `rtk`. No hook needed.

### Claude Code

Hooks work automatically after `rtk init --global`. Shell tool calls are transparently rewritten.

### OpenCode

```bash
rtk init --global --opencode
```

### Other agents (MiniMax, GPT, Gemini via API)

No hook support — agent must call `rtk <cmd>` explicitly. This skill handles that by teaching the agent the correct syntax.

## Checking current config

```bash
rtk config show     # Show active config
rtk gain            # Show savings stats
rtk --version       # Verify installation
```
