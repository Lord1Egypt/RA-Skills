# Testing Pitfalls — Discovered 2026-07-23

Pitfalls found during live deployment testing of ssh-executor v2.2.1.

## 1. UserKnownHostsFile /dev/null Nullifies StrictHostKeyChecking

**Symptom:** `Host key verification failed` (exit 255) even though the host key is in `~/.ssh/known_hosts`.

**Root cause:** `~/.ssh/config` has `UserKnownHostsFile /dev/null` — SSH effectively has no trust store. When our skill sets `StrictHostKeyChecking=yes` (hardening v2.2.0), strict checking fails because there's nothing to check against.

**Fix applied:** In `ssh-run-native.sh`, when `HOST_KEY_CHECKING=yes`, the script now forces:
```
-o UserKnownHostsFile=${HOME}/.ssh/known_hosts
```
This overrides the `/dev/null` from the SSH config and points to the real known_hosts file. A `touch` ensures the file exists (SSH refuses nonexistent UserKnownHostsFile paths).

**Checklist:**
- [ ] Grep SSH config for `UserKnownHostsFile` directives
- [ ] Ensure `${HOME}/.ssh/known_hosts` is writable
- [ ] Use `ssh-keyscan` to add host keys before connecting

## 2. Ghost Exit Code 1 from ssh-keys.sh restore

**Symptom:** `ssh-keys.sh restore id-rsa` prints "✓ SSH key loaded into ssh-agent" to stderr (success messages) but returns exit code 1 instead of 0. This causes `ssh-run-native.sh` to incorrectly route to the "Failed to restore SSH key" error handler (exit 98).

**Root cause:** Combined effect of `set -euo pipefail` + trap + double cleanup:

1. Success path in `cmd_restore()` does `shred -u "$tmp_key"` + `rm -f "$tmp_key"` → deletes temp file
2. Prints "✓ loaded" success messages  
3. Calls `exit 0`
4. `exit 0` triggers EXIT trap: `shred -u "$tmp_key" 2>/dev/null; rm -f "$tmp_key"`
5. File is already deleted → `shred -u` fails
6. `set -e` catches the trap failure and converts to exit 1

**Fix applied:** Changed trap from `shred -u ...; rm -f ...` to just `rm -f`. The `rm -f` on a missing file always succeeds (exit 0). The `shred -u` secure wipe still happens in the explicit code paths (success + error branches) before the trap fires. The trap is now purely a safety net for interrupted execution — it removes the temp file but does not attempt secure wipe (acceptable since /tmp is typically tmpfs/RAM).

## 3. --host-key-checking Silently Ignored by Python Backend

**Symptom:** Using `--host-key-checking no` with the Python/Paramiko backend had no effect — the backend always used its default policy.

**Root cause:** `ssh-run.sh` (dispatcher) had `--host-key-checking) shift 2 ;; # ignored in Python backend`. The variable was never captured or passed to `ssh-client.py`.

**Fix applied:** 
- `ssh-run.sh`: Capture `HOST_KEY_CHECKING` variable, pass to Python backend via `--host-key-checking "$HOST_KEY_CHECKING"`
- `ssh-client.py`: Already supports the flag (added in v2.2.0), defaults to `RejectPolicy`
