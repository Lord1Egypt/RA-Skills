# Gemini CLI ripgrep Detection Fix

## Problem
During super-router runs, the Gemini CLI repeatedly logs:
> "Ripgrep is not available. Falling back to GrepTool"

This occurs even when ripgrep is correctly installed at `/opt/homebrew/bin/rg` and PATH is set in `~/.openclaw/.env`.

## Root Cause
The Gemini CLI binary performs its own internal tool discovery for commands like `rg`. When invoked via `subprocess.run`, these child processes do not always inherit the environment variables (including PATH) that the router sets from `~/.openclaw/.env`.

## Solution
Force-prepend the required tool paths directly inside `invoke_gemini_cli()` before every subprocess call.

### Patch Applied
```python
# Force inject ripgrep + common tool paths
extra_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
current_path = env.get("PATH", "")
path_parts = [p for p in extra_paths if p not in current_path.split(":")]
if path_parts:
    env["PATH"] = ":".join(path_parts + [current_path]) if current_path else ":".join(path_parts)
```

This replaces the previous conditional injection and ensures `rg` is always visible to Gemini's internal tools.

## Verification
After applying the patch, run any complex task through the router and confirm the "Ripgrep is not available" message no longer appears in the Gemini CLI stderr.
