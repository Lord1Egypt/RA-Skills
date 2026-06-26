# RTK Plugin for OpenClaw

Transparently rewrites shell commands executed via OpenClaw's `exec` tool to their RTK equivalents, achieving 60-90% LLM token savings.

This is the OpenClaw equivalent of the Claude Code hooks in `hooks/rtk-rewrite.sh`.

## How it works

The plugin registers a `before_tool_call` hook that intercepts `exec` tool calls. It delegates rewriting to `rtk rewrite`, which is the single source of truth used by Claude Code hooks too. When the agent runs `git status`, the plugin asks RTK for a rewrite and executes the rewritten command if available.

## Installation

### Prerequisites

RTK must be installed and available in `$PATH`:

```bash
brew install rtk-ai/tap/rtk
# or
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

### Install the plugin

```bash
# Copy the plugin to OpenClaw's extensions directory
mkdir -p ~/.openclaw/extensions/rtk-rewrite
cp openclaw/index.ts openclaw/openclaw.plugin.json ~/.openclaw/extensions/rtk-rewrite/

# Enable in OpenClaw config
openclaw config set plugins.entries.rtk-rewrite.enabled true

# Restart the gateway
openclaw gateway restart
```

### Or install via OpenClaw CLI

```bash
openclaw plugins install ./openclaw
```

## Configuration

In `openclaw.json`:

```json5
{
  plugins: {
    entries: {
      "rtk-rewrite": {
        enabled: true,
        config: {
          enabled: true, // Toggle rewriting on/off
          verbose: false, // Log rewrites to console
          audit: false, // Write hook-style audit logs to hook-audit.log
          auditDir: "~/.local/share/rtk", // Optional custom audit directory
        },
      },
    },
  },
}
```

## What gets rewritten

Anything supported by `rtk rewrite` in your installed RTK version. This keeps OpenClaw and Claude Code behavior aligned automatically.

Quick check:

```bash
rtk rewrite "git status"
rtk rewrite "cargo test"
```

## What's NOT rewritten

Anything `rtk rewrite` decides not to rewrite (already-rtk commands, unsupported commands, complex shells like heredocs/pipelines, and commands excluded by RTK config).

## Troubleshooting logs

Enable structured audit logs for issue analysis:

```json5
{
  plugins: {
    entries: {
      "rtk-rewrite": {
        enabled: true,
        config: {
          audit: true,
          // Optional. If omitted, uses RTK_AUDIT_DIR or ~/.local/share/rtk
          auditDir: "~/.local/share/rtk",
        },
      },
    },
  },
}
```

Then inspect summary with:

```bash
rtk hook-audit --since 7 -v
```

Audit format is compatible with Claude Code hook logs:

```text
timestamp | action | original_cmd | rewritten_cmd
```

## Measured savings

| Command              | Token savings |
| -------------------- | ------------- |
| `git log --stat`     | 87%           |
| `ls -la`             | 78%           |
| `git status`         | 66%           |
| `grep` (single file) | 52%           |
| `find -name`         | 48%           |

## How it compares to Claude Code hooks

| Feature          | CC Hook (`hooks/rtk-rewrite.sh`) | OpenClaw Plugin               |
| ---------------- | -------------------------------- | ----------------------------- |
| Hook type        | Shell script (PreToolUse)        | TypeScript (before_tool_call) |
| Rewrite approach | `rtk rewrite` delegation         | `rtk rewrite` delegation      |
| Installation     | `rtk init --global`              | Copy to extensions dir        |
| Configuration    | `.claude/settings.json`          | `openclaw.json`               |
| Scope            | Claude Code sessions             | All OpenClaw agents           |

## License

MIT — same as RTK.
