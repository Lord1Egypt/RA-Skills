---
name: slack-channel-context
description: Automatically loads Slack channel context files (e.g., bebops.md, C0AK8SDFS4W.md) into session context for Slack channels and threads. Use this skill whenever you're in a Slack channel or thread and need channel-specific context, project information, or channel-specific rules to be loaded into your session.
version: 1.0.0
---

# Slack Channel Context - Technical Documentation

**For quick start: See [README.md](README.md)**

## Overview

This skill automatically loads channel context files from `slack-channel-contexts/` into your session context whenever you're interacting in a Slack channel or thread. This ensures you have the right context for each channel without manual intervention.

In my Openclaw workflow, I use Slack with diffrent channels for different purposes. As a developer, I have dedicated Slack channels for each project. I needed a way to ensure that the Openclaw Agent knew which project I meant when I said something like; run all unit tests. Or if I wanted to discuss a new feature, I wanted to simply be able to start discussing in the appropriate channel and have the Agent know which project I meant. This Skill is the artifact that solved for my case.

**Key Design Decision:** Context files are named simply as `<CHANNEL_ID>.md` or `<CHANNEL_NAME>.md` (e.g., `bebops.md`, `C0AK8SDFS4W.md`). There is NO default fallback file - channels without context files return `None`.

## How It Works

### Context Loading Process

1. **Detection**: Skill detects when you're in a Slack channel or thread
2. **Thread Check**: If the message is in a thread (has `thread_id` or `thread_ts`), checks `SLACK_CONTEXT_LOAD_ON_THREADS` setting
   - If `SLACK_CONTEXT_LOAD_ON_THREADS=false`, skips context loading in threads
   - If `SLACK_CONTEXT_LOAD_ON_THREADS=true` (default), loads context in threads
3. **File Discovery**: Looks for context files in `slack-channel-contexts/` folder in priority order:
   - `slack-channel-contexts/<CHANNEL_ID>.md` (e.g., `C0AK8SDFS4W.md`) - **highest priority**
   - `slack-channel-contexts/<CHANNEL_NAME>.md` (e.g., `bebops.md`) - medium priority
   - No default fallback - returns `None` if no file exists
4. **Context Injection**: Loads the found file into session context
5. **Caching**: Caches the loaded context for 1 hour (3600 seconds) to avoid repeated file reads

## Tools

### `load_channel_context()`

**Load Slack channel context into the current session.**

This tool automatically loads the appropriate channel context file based on the current Slack channel. Call this at session startup to ensure you have full channel awareness.

**Signature:**
```python
load_channel_context(
    channel_id: str,
    channel_name: str,
    workspace_dir: str = None,
    force_reload: bool = False,
    is_thread: bool = False
) -> dict
```

**Parameters:**
- `channel_id` (str, required): Slack channel ID (e.g., "C0AK8SDFS4W")
- `channel_name` (str, required): Slack channel name (e.g., "bebops")
- `workspace_dir` (str, optional): Custom workspace directory (defaults to `~/.openclaw/workspace`)
- `force_reload` (bool, optional): If True, bypass cache and read file fresh (use after editing context files)
- `is_thread` (bool, optional): If True, checks `SLACK_CONTEXT_LOAD_ON_THREADS` setting (default: False)

**Returns:**
```json
{
  "success": true,
  "context": "# Channel Context: #bebops\n\n## Purpose...",
  "channel_id": "C0AK8SDFS4W",
  "channel_name": "bebops",
  "message": "Loaded channel context for bebops channel"
}
```

Or if no context file exists:
```json
{
  "success": false,
  "context": "",
  "channel_id": "C0AK8SDFS4W",
  "channel_name": "bebops",
  "message": "No context file found for this channel. Context files must be created in slack-channel-contexts/ directory."
}
```

**Example:**
```python
result = load_channel_context(channel_id="C0AK8SDFS4W", channel_name="bebops")
if result["success"]:
    print(f"Loaded context: {result['context'][:200]}...")
else:
    print(f"No context available: {result['message']}")
```

**Behavior:**
- Looks for context files in priority order:
  1. `slack-channel-contexts/<CHANNEL_ID>.md`
  2. `slack-channel-contexts/<CHANNEL_NAME>.md`
  3. No default - returns `None` if no file exists
- Caches results for 1 hour (3600 seconds) by default
- Use `force_reload=True` after editing context files to bypass cache

## Implementation Files

### `scripts/skill.py`

**Location:** `scripts/skill.py`

Main implementation file containing the `SlackContextLoader` class and `load_channel_context()` function.

### `scripts/load_context.py`

**Location:** `scripts/load_context.py`

Legacy module for backward compatibility. Contains the core `SlackContextLoader` class.

### `scripts/reload_all_contexts.py`

**Location:** `scripts/reload_all_contexts.py`

Utility script to reload all channel context files, bypassing cache.

**Usage:**
```bash
python3 ~/.openclaw/workspace/skills/slack-channel-context/scripts/reload_all_contexts.py
```

### `scripts/example.py`

**Location:** `scripts/example.py`

Demo script showing how the context loader works with different channels.

**Usage:**
```bash
python3 ~/.openclaw/workspace/skills/slack-channel-context/scripts/example.py
```

## Environment Variables

Set these in **`~/.openclaw/workspace/.env`** (preferred method):

| Variable | Default | Description |
|----------|---------|-------------|
| `SLACK_CONTEXT_ENABLED` | `true` | Enable/disable the skill |
| `SLACK_CONTEXT_LOAD_ON_THREADS` | `true` | Load context in threaded messages |
| `SLACK_CONTEXT_LOAD_ON_THREAD_START` | `true` | Load context on thread/session start |
| `SLACK_CONTEXT_CACHE_TTL` | `7200` | Cache duration in seconds (120 min) |
| `SLACK_CONTEXT_CONTEXTS_DIR` | `~/.openclaw/workspace/slack-channel-contexts/` | Custom contexts directory |

**Note:** Do not use `export` - just set the variables directly in `~/.openclaw/workspace/.env`.

## Context File Structure

Context files follow this structure:

```markdown
# Channel Context: #channel-name

## Purpose
[What is this channel for?]

## Associated Projects
- [project-name]: [description]

## Rules & Guidelines
- [Rule 1]
- [Rule 2]

## Recent Activity
- [YYYY-MM-DD]: [Update]

## People to Know
- [@username]: [role]

---

```

See [`examples/EXAMPLE_CHANNEL_CONTEXT.md`](examples/EXAMPLE_CHANNEL_CONTEXT.md) for a complete working example.

## Important Notes

### Force Reload After Editing

After editing a context file, you **MUST** use `force_reload=True` to bypass the cache:

```python
load_channel_context(
    channel_id="C0AK8SDFS4W",
    channel_name="bebops",
    force_reload=True
)
```

### No Default Fallback

There is NO default `SLACK_CHANNEL_CONTEXT.md` file. If a channel doesn't have a context file, the skill returns `success: false` with an empty context. This is intentional - channels without context simply have no context.

### Simple File Names

Context files are named simply as `<CHANNEL_ID>.md` or `<CHANNEL_NAME>.md`. The `SLACK_CHANNEL_CONTEXT_` prefix has been removed to make file names shorter and more readable.

## Troubleshooting

See [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) for detailed troubleshooting steps.

## Files

| File | Purpose |
|------|---------|
| `scripts/skill.py` | Main implementation |
| `scripts/load_context.py` | Legacy module |
| `scripts/example.py` | Demo script |
| `scripts/reload_all_contexts.py` | Utility script |
| `examples/EXAMPLE_CHANNEL_CONTEXT.md` | Complete working example |
| `_meta.json` | ClawHub publishing metadata |

---

*For quick start: [README.md](README.md)*
*For troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)*

