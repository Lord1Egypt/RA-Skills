# Slack Channel Context Skill

> **Auto-load Slack channel context into your AI sessions** - No more manual context switching!

## What This Does

This skill automatically loads channel-specific context files when you're in a Slack channel. The AI assistant knows exactly what channel you're in and loads the relevant context files automatically.

**Example:** When you message in the `#bebops` channel, the skill automatically loads `slack-channel-contexts/bebops.md` so the AI has full context about that channel.

## Quick Start (3 Steps)

### Step 1: Enable the Skill

Add the skill to **your** `openclaw.json` configuration (not the skill directory).

**Where is your `openclaw.json`?**
- Typically at `~/.openclaw/openclaw.json` (global)
- Or in your workspace root

**Add to your configuration:**
```json
{
  "channels": {
    "slack": {
      "channels": {
        "C0AML4J8FK2": {
          "skills": ["slack-channel-context"]
        }
      }
    }
  }
}
```

**Important:** Only add the skill name (`"slack-channel-context"`) - not the full configuration!

### Step 2: Create Context Files

```bash
# Create the directory if it doesn't exist
mkdir -p ~/.openclaw/workspace/slack-channel-contexts

# Create a context file for your channel
touch ~/.openclaw/workspace/slack-channel-contexts/bebops.md
# OR use channel ID
touch ~/.openclaw/workspace/slack-channel-contexts/C0AML4J8FK2.md
```

### Step 3: Fill in Your Context

Edit the file using this template:

```markdown
# Channel Context: #bebops

## Purpose
All things Bebop - announcements, updates, and kudos.

## Associated Projects
- bebops-project: Main Bebops project repository

## Rules & Guidelines
- Keep messages positive and supportive
- Use ⭐ emoji for kudos

## Recent Activity
- 2026-03-26: Created channel context
```

See [`examples/EXAMPLE_CHANNEL_CONTEXT.md`](examples/EXAMPLE_CHANNEL_CONTEXT.md) for a complete example.

## Configuration

### Environment Variables

Set these in **`~/.openclaw/workspace/.env`** (preferred method):

```bash
# Enable/disable the skill (default: true)
SLACK_CONTEXT_ENABLED=true

# Load context in threads? (default: true)
# Set to false to skip context in threaded messages
SLACK_CONTEXT_LOAD_ON_THREADS=true

# Cache duration in seconds (default: 3600 = 1 hour)
SLACK_CONTEXT_CACHE_TTL=7200

# Custom contexts directory (default: ~/.openclaw/workspace/slack-channel-contexts/)
SLACK_CONTEXT_CONTEXTS_DIR=~/.openclaw/workspace/slack-channel-contexts/
```

**Note:** The `.env` file at `~/.openclaw/workspace/.env` is the preferred method for setting environment variables. Do not use `export` - just set the variables directly in the `.env` file.

### Understanding the Configuration

**Your `openclaw.json`** (user configuration):
- Enables the Slack integration
- Adds channel IDs
- Lists which skills to use in each channel

**Skill's `_meta.json`** (in skill directory):
- Tells OpenClaw what the skill does
- Documents environment variables
- Lists available tools
- **You don't need to modify this!**

**Environment Variables:**
Control the skill's behavior (see options above).

### Common Configuration Patterns

**Enable in Multiple Channels:**
```json
{
  "channels": {
    "slack": {
      "channels": {
        "C0AML4J8FK2": {
          "skills": ["slack-channel-context"]
        },
        "C0AK8SDFS4W": {
          "skills": ["slack-channel-context"]
        },
        "C0AK4SJGHGT": {
          "skills": ["slack-channel-context"]
        }
      }
    }
  }
}
```

**Enable with Other Skills:**
```json
{
  "channels": {
    "slack": {
      "channels": {
        "C0AML4J8FK2": {
          "skills": [
            "slack-channel-context",
            "other-skill-name"
          ]
        }
      }
    }
  }
}
```

**Disable in Specific Channels:**
Just don't add the skill to that channel's `skills` array:
```json
{
  "channels": {
    "slack": {
      "channels": {
        "C0AML4J8FK2": {
          "skills": ["slack-channel-context"]
        },
        "C0PRIVATE123": {
          "skills": []  // No skills, no context loading
        }
      }
    }
  }
}
```

## Troubleshooting

### Context Not Loading?

1. **Check the skill is enabled:**
   ```bash
   echo $SLACK_CONTEXT_ENABLED
   # Should be: true
   ```

2. **Verify context file exists:**
   ```bash
   ls ~/.openclaw/workspace/slack-channel-contexts/
   ```

3. **Check file naming:**
   - ✅ `C0AML4J8FK2.md` (channel ID)
   - ✅ `bebops.md` (channel name)
   - ❌ `SLACK_CHANNEL_CONTEXT_C0AML4J8FK2.md` (old format)

4. **Force reload cache:**
   ```python
   load_channel_context(
       channel_id="C0AML4J8FK2",
       channel_name="bebops",
       force_reload=True
   )
   ```

5. **Check your `openclaw.json`:**
   - Make sure the skill name is correct: `"skills": ["slack-channel-context"]`
   - Verify channel ID is correct
   - Restart OpenClaw after updating `openclaw.json`

### Want to Disable Temporarily?

Set the environment variable:
```bash
export SLACK_CONTEXT_ENABLED=false
```

Or remove the skill from your `openclaw.json`:
```json
{
  "channels": {
    "slack": {
      "channels": {
        "C0AML4J8FK2": {
          "skills": []  // Empty array = no skills
        }
      }
    }
  }
}
```

### Want to Test?

Run the example script:
```bash
python3 ~/.openclaw/workspace/skills/slack-channel-context/scripts/example.py
```

## Advanced Usage

### Thread Control

**Disable context in threads** (saves tokens, avoids unwanted context):
```bash
export SLACK_CONTEXT_LOAD_ON_THREADS=false
```

**Keep context in threads** (default - loads context in both regular messages and threads):
```bash
export SLACK_CONTEXT_LOAD_ON_THREADS=true
```

### Custom Context Directory

Use a different directory for context files:
```bash
export SLACK_CONTEXT_CONTEXTS_DIR=/path/to/custom/context/dir
```

### Disable in Specific Threads

Use the `is_thread` parameter:
```python
# Load context (normal message)
load_channel_context(channel_id="C0AML4J8FK2", channel_name="bebops", is_thread=False)

# Skip context (threaded message)
load_channel_context(channel_id="C0AML4J8FK2", channel_name="bebops", is_thread=True)
```

## Context File Structure

Use this template when creating new context files:

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

See [`references/context-template.md`](references/context-template.md) for more details.

## Files

- `scripts/skill.py` - Main implementation
- `scripts/load_context.py` - Legacy module
- `scripts/example.py` - Demo script
- `scripts/reload_all_contexts.py` - Utility script
- `examples/EXAMPLE_CHANNEL_CONTEXT.md` - Complete working example
- `_meta.json` - ClawHub publishing metadata

## Documentation

- **[README.md](README.md)** - This file - quick start guide
- **[SKILL.md](SKILL.md)** - Technical documentation with all details
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Quick fixes for common problems

---

**Questions?** Check out the full documentation in [`SKILL.md`](SKILL.md) or the examples in [`examples/EXAMPLE_CHANNEL_CONTEXT.md`](examples/EXAMPLE_CHANNEL_CONTEXT.md).

*Skill version: 1.0.0*
