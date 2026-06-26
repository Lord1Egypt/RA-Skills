# Slack Channel Context - Troubleshooting Guide

Quick solutions to common problems.

## Context Not Loading?

### Check 1: Is the skill enabled?

```bash
# Check if the variable is set in .env
grep SLACK_CONTEXT_ENABLED ~/.openclaw/workspace/.env
# Should return: SLACK_CONTEXT_ENABLED=true
```

**Note:** Environment variables must be set in `~/.openclaw/workspace/.env`, not in shell config files like `~/.bashrc` or `~/.zshrc`.

### Check 2: Does the context file exist?
```bash
ls ~/.openclaw/workspace/slack-channel-contexts/
# Should show your context files
```

### Check 3: Is the file named correctly?
- ✅ `C0AML4J8FK2.md` (channel ID)
- ✅ `bebops.md` (channel name)
- ❌ `SLACK_CHANNEL_CONTEXT_C0AML4J8FK2.md` (old format)

### Check 4: Force reload the cache
```python
load_channel_context(
    channel_id="C0AML4J8FK2",
    channel_name="bebops",
    force_reload=True
)
```

### Check 5: Verify your `openclaw.json`
Make sure your **user's** `openclaw.json` (not the skill directory) includes:
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

See [README.md](README.md) for detailed configuration instructions.

## Context Loading in Threads?

### Disable context in threads (save tokens)
```bash
export SLACK_CONTEXT_LOAD_ON_THREADS=false
```

### Keep context in threads (default)
```bash
export SLACK_CONTEXT_LOAD_ON_THREADS=true
```

## Performance Issues?

### Increase cache duration
```bash
export SLACK_CONTEXT_CACHE_TTL=7200  # 2 hours instead of 1
```

### Use custom context directory
```bash
export SLACK_CONTEXT_CONTEXTS_DIR=/path/to/fast/storage/
```

## Want to Test?

### Run the example script
```bash
python3 ~/.openclaw/workspace/skills/slack-channel-context/scripts/example.py
```

### Reload all contexts manually
```bash
python3 ~/.openclaw/workspace/skills/slack-channel-context/scripts/reload_all_contexts.py
```

## Still Having Issues?

1. Check the full documentation in [SKILL.md](SKILL.md)
2. Review the example in [examples/EXAMPLE_CHANNEL_CONTEXT.md](examples/EXAMPLE_CHANNEL_CONTEXT.md)
3. Check if there are any Python errors in the scripts
4. Verify your Slack message metadata includes `channel_id` and `channel`

---

**Need more help?** Check out the [README.md](README.md) for setup instructions.
