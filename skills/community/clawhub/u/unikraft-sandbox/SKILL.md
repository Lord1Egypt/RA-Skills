---
name: unikraft-sandbox
description: Run agent tasks inside an isolated Unikraft Cloud (UKC) sandbox VM. Use when the agent needs a clean, isolated execution environment — e.g. running untrusted code, testing scripts, reproducing build issues, or any task that should not execute on the host. Triggers on phrases like "run this in a sandbox", "spin up a sandbox", "execute in an isolated environment", or any case where isolation is necessary. Requires UKC_TOKEN, UKC_METRO, UKC_USER, and UKC_SANDBOX_IMAGE env vars.
---

# Unikraft Sandbox

Runs tasks inside a per-session Unikraft Cloud (UKC) sandbox VM. One sandbox per session.

Full API shapes: see `references/ukc_api.md`.

---

## Prerequisites

Check that these env vars are set before proceeding. They are inherited by all child processes (scripts, curl calls) automatically — no injection needed.

- `UKC_TOKEN`, `UKC_METRO`, `UKC_USER`, `UKC_SANDBOX_IMAGE`

If any are missing, stop and ask the user to export them.

---

## Session State

Hold these in memory for the duration of the session:

- `sandbox_name` — generated name (also the tmp dir name under `/tmp/`)
- `session_dir` — local directory to sync with the sandbox (task-specific)

The FQDN is persisted to `/tmp/<sandbox-name>/fqdn` by `create-sandbox.sh` and read from there by other scripts — no need to track it separately in memory.

---

## Lifecycle

### 1. Create sandbox

Generate a name: `sandbox-<short-session-id>-<unix-timestamp>` (lowercase, hyphens only, valid as a directory name). Store as `sandbox_name`.

```bash
bash scripts/create-sandbox.sh <sandbox-name>
```

Capture stdout as `sandbox_fqdn`. The script:
- Checks if a sandbox with that name already exists — exits with an error if so
- Creates `/tmp/<sandbox-name>/` with the SSH keypair inside
- Creates the UKC instance (passing the pubkey)
- Prints the instance FQDN

### 2. Sync local → sandbox (before a task)

```bash
bash scripts/sync-to-sandbox.sh <sandbox-name> <session-dir>
```

> ⚠️ **Destructive sync:** `sync-to-sandbox.sh` uses `--delete`, meaning any files present in `/workspace` on the sandbox that don't exist locally **will be deleted**. Do not manually create files in `/workspace` that you want to keep — they will be wiped on the next sync.

### 3. Execute commands

Prefer the exec API for most commands:

```bash
node scripts/exec-sandbox.js "$(cat /tmp/<sandbox-name>/fqdn)" "cd /workspace && <your command>"
```

Check exit code. Non-zero means the command failed. See `references/ukc_api.md` for response shape.

Use SSH directly only for interactive/PTY needs:
```bash
ssh -i /tmp/<sandbox-name>/id_ed25519 \
  -o StrictHostKeyChecking=no \
  -o ProxyCommand="openssl s_client -quiet -connect $(cat /tmp/<sandbox-name>/fqdn):2222 2>/dev/null" \
  root@"$(cat /tmp/<sandbox-name>/fqdn)"
```

### 4. Sync sandbox → local (after a task)

```bash
bash scripts/sync-from-sandbox.sh <sandbox-name> <session-dir>
```

### 5. Delete sandbox

When the session ends or the sandbox is no longer needed:

```bash
bash scripts/delete-sandbox.sh <sandbox-name>
```

This removes the UKC instance and the local `/tmp/<sandbox-name>/` directory (including SSH keys).

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Required env var missing | Stop, ask user to export it |
| `create-sandbox.sh` fails | Surface the error; do not proceed |
| Exec API returns non-200 | Surface `.error`; treat as hard failure |
| `code` non-zero in exec response | Command failed; surface `.stderr` |
| SSH connection refused | Sandbox may be suspended; retry after a few seconds |
