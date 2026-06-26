---
name: py-env-setup
description: Host-specific Python execution guidance for OpenClaw on this machine. Prefer $PYTHON over python/python3 in PATH, because OpenClaw exec runs in a non-interactive shell and may not inherit interactive shell initialization.
homepage: https://github.com/QAA-Tools/skills
metadata: {"clawdbot":{"emoji":"🐍","requires":{"env":["PYTHON"]},"primaryEnv":"PYTHON"}}
---

# Python Environment Setup

Use this skill whenever OpenClaw needs to run Python on this host.

## Why this exists

On this machine, OpenClaw `exec` runs in a **non-interactive shell**.
Interactive shell initialization may be skipped, so `python`, `python3`, or `conda` may be unavailable from PATH even though they work in a normal terminal.

Therefore, prefer the explicit Python entrypoint provided by environment variable `PYTHON`.

## Rules

1. Prefer `"$PYTHON"` over `python` or `python3`.
2. Do not rely on `source ~/.bashrc` or `conda activate` for routine automation.
3. Before using Python, verify it exists and is executable.
4. Use `"$PYTHON" -m pip ...` for package installation.
5. Use `"$PYTHON" script.py`, `"$PYTHON" -m module`, or `"$PYTHON" -c '...'` for execution.
6. Apply this rule to **all Python-related commands**, not just pip.
7. If `PYTHON` is unset or invalid, report the problem clearly.

## Validation

```bash
test -x "$PYTHON"
"$PYTHON" --version
```

## Common patterns

### Install packages

```bash
"$PYTHON" -m pip install -U package_name
"$PYTHON" -m pip install -U openai-whisper torch ffmpeg-python
```

### Run a script

```bash
"$PYTHON" script.py
```

### Run a module

```bash
"$PYTHON" -m module_name
```

### Run inline Python

```bash
"$PYTHON" - <<'PY'
print('hello')
PY
```

### Quick guard pattern

```bash
test -x "$PYTHON" || { echo "PYTHON not executable: $PYTHON" >&2; exit 1; }
"$PYTHON" --version
```

## Fallback policy

Only if the task explicitly allows fallback, try in this order:

1. `$PYTHON`
2. `python3`
3. `python`

Default policy: **do not silently fallback**. Prefer failing loudly if `$PYTHON` is missing, so environment issues are obvious.

## Notes

- This skill is host-specific.
- It is meant to guide OpenClaw runtime behavior, not teach Python itself.
- The `PYTHON` value is read from the environment. This skill does not require a specific env-file location.
