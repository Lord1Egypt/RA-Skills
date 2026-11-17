# ClawHub Security Audit — July 2026

**Auditor:** SkillSpector by NVIDIA
**Scope:** ssh-executor skill v2.1.0
**Total findings:** 47 (25 detailed, 22 hidden)

## Findings Fixed in v2.2.0 (High Severity)

| # | Category | Confidence | Finding | Fix |
|---|----------|-----------|---------|-----|
| 1 | Tool Poisoning | 99% | Documented behavior contradicts safety model (passwords, key restore, sudo, auto-accept host keys) | Description updated to match actual capabilities; host-key default → strict |
| 2 | Credential Mismanagement | 99% | Header forbids passwords but docs instruct storage | Header clarified: "passwords for automation may be stored in Vaultwarden with explicit approval" |
| 3 | Key Exfiltration | 99% | Rsync workflow copies private key to remote server | server-to-server-rsync.md deprecated; ForwardAgent preferred |
| 4 | Host-Key Bypass | 99% | AutoAddPolicy in Python, accept-new in native | Default RejectPolicy (Python), StrictHostKeyChecking=yes (native), accept-new removed |
| 5 | Destructive Commands | 94% | sudo find ... -delete without confirmation | Warning banner in remote-backup-cleanup.md |
| 6 | Undeclared MCP | 92% | Shell, file, env-var access undeclared | MCP Permissions Declaration section added |

## Findings Fixed in v2.2.1 (Medium Severity)

| # | Category | Confidence | Finding | Fix |
|---|----------|-----------|---------|-----|
| 7 | Temp Key Cleanup | 93-95% | trap EXIT only, kill -9 bypasses | trap EXIT INT TERM HUP + shred -u |
| 8 | restore-to-file Path | 92% | Writes to any caller-specified path | Path validation: rejects /etc, /boot, /sys, /proc, /dev, /run; warns non-tmp |
| 9 | Missing User Warning | — | No warning on --host-key-checking no | Explicit stderr MITM warning |
| 10 | Pass-through Bug | — | --host-key-checking ignored by Python backend | ssh-run.sh now captures and passes to ssh-client.py |
| 11 | SSL/TLS | — | check_hostname=False without caveat | "Only safe on trusted local networks" |

## Confirmed Safe (No Action Needed)

- vault-resolver uses direct API with session cache — not vulnerable to bw CLI dependency issues
- ssh-run.sh JSON output omits key paths, SSH config paths, resolved identity files
- --sudo auto-enables --confirm-dangerous, no separate flag needed
- Password-based sudo pipes via stdin, never appears in ps aux

## Remaining Low-Severity / Informational

47 total findings minus 11 fixed = 36 remaining. The remaining are either:
- Low-severity informational (e.g., "skill enables shell execution" — by design)
- False positives (e.g., "SSH key in vault is stored" — Vaultwarden is AES-256 encrypted at rest)
- Duplicates of the 11 already fixed

## Lessons for Skill Authors

1. **Default-deny for host keys.** Never auto-accept in any backend.
2. **Description must match implementation.** If the skill supports password auth, say so honestly — don't pretend it's key-only.
3. **Trap all signals, not just EXIT.** INT, TERM, and HUP are common; kill -9 remains a known gap.
4. **Validate caller paths.** Any restore-to-file action should reject system directories.
5. **Declare MCP permissions.** Even if the platform doesn't enforce them yet, document what capabilities the skill needs.
6. **Warn explicitly on unsafe choices.** --host-key-checking no should produce a visible stderr warning.
7. **Deprecate, don't hide.** The key-copy rsync pattern is still documented but clearly marked as deprecated with preferred alternatives.
