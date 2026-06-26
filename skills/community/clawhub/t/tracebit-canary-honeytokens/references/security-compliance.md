# Security Compliance — Tracebit Canaries Skill

This document covers safety posture, credential handling rules, messaging constraints, network behavior, file operations transparency, and full removal instructions for the Tracebit Canaries skill.

This skill is user-initiated and runs under user supervision. The user can interrupt or cancel at any step.
This skill does not request global always-on privileges or modify other skills. The long‑lived background service is the Tracebit CLI daemon installed by the user/CLI (runs as current user) — this skill documents this and requires human confirmation for deployments/rotations.

---

## Safety Posture

This skill operates under a **human-gated-deployment** model:

1. **Upfront consent** — Before starting setup, the agent confirms with the human that they want to proceed. The agent summarizes what will be installed and where canaries will be placed. (SKILL.md: "End-to-End Setup" — "Do NOT proceed until the human confirms.")
2. **Confirmation before sensitive writes** — The agent confirms with the human before writing canary credentials to standard credential locations on disk. (SKILL.md: Step 4 — "Do NOT run `tracebit deploy` until the human confirms.")
3. **Confirmation before remediation** — After an incident, the agent waits for human acknowledgement before rotating canaries or taking corrective action. (SKILL.md: "When a Canary Fires" — "after human acknowledgement")
4. **Confirmation before memory reads** — The agent asks the human for permission before reading `memory/*` files during investigation. (Incident response playbook: Phase 2.4 — "May I proceed? (yes/no)")

### Enforcement Model

Human-gating is enforced at two levels:

1. **Agent instruction level** — SKILL.md contains explicit blocking directives ("Do NOT proceed until the human confirms", "Do NOT run ... until the human confirms") at each sensitive operation. These are not advisory — the agent treats them as hard stops.
2. **Platform metadata level** — The `runtime_constraints` declared in the skill's metadata (e.g., `canary-deployment-requires-human-confirmation: true`) signal to the OpenClaw platform that these gates must be enforced. The platform can audit agent behavior against these declared constraints.

The combination means: the agent is instructed to stop and wait, and the platform is informed that it should enforce the stop.

### Red Lines

The agent will **never**:
- Use canary credentials for real workloads or authentication
- Expose canary credential values in conversation output or logs
- Send notifications to channels other than the user's own configured messaging channel
- Execute remediation or canary rotation without human acknowledgement
- Read or modify real credentials on disk (only canary-specific files are touched)
- Bypass checksum verification when installing binaries
- Execute arbitrary code or dynamically load external scripts

### Runtime Constraints

| Constraint | Enforced | Declared in metadata |
|---|---|---|
| Human confirmation before deployment | Yes | `canary-deployment-requires-human-confirmation` |
| Human confirmation before remediation | Yes | `canary-rotation-requires-human-acknowledgement` |
| Investigation phase is read-only (except append-only incident log) | Yes | `investigation-read-only-except-append-only-incident-log` |
| Human confirmation before reading memory files during investigation | Yes | `memory-file-review-requires-human-confirmation` |
| SHA256 checksum verification mandatory | Yes | `sha256-verification-mandatory` |
| No autonomous credential writes | Yes | `credential-files-written-only-by-cli-not-skill` |
| Email/messaging access requires upfront consent | Yes | `email-and-messaging-require-upfront-consent` |

### Declared Permissions & File Access

All runtime file operations and external access are declared in the skill's metadata `permissions` array:

| Permission | Purpose |
|---|---|
| `email:read` (via `plugins.email`) | Read-only search for Tracebit alert emails via user's pre-authorized email account |
| `messaging:send` (via `plugins.messaging`) | Send canary alert notifications to user's own channel only |
| `fs:write memory/security-incidents.md` | Append-only incident log during canary alert investigation |
| `fs:write /tmp/tracebit-setup-creds` | Temporary signup password (chmod 600); deleted after use |
| `fs:read memory/*` | Agent memory files during incident investigation; requires human confirmation |

---

## Network Behavior

This skill contacts exactly two external endpoints. No other network calls are made by the skill itself.

| Endpoint | Purpose | When | Direction |
|---|---|---|---|
| `community.tracebit.com` | Account creation, canary management API, OAuth authentication | During setup and canary deploy/rotate | HTTPS only, user-initiated |
| `github.com/tracebit-com/tracebit-community-cli` | One-time CLI binary download from official GitHub Releases | During CLI install (Step 2 only) | HTTPS only, SHA256-verified |

**No C2, beaconing, or telemetry patterns.** The skill does not phone home, poll external servers, or transmit user data. The Tracebit CLI daemon's only network activity is periodic credential refresh against `community.tracebit.com` — this is a keep-alive for canary token expiry, not data exfiltration.

---

## File Operations Transparency

### What the skill itself writes

These files are created by agent instructions in SKILL.md, not by the shell scripts in `scripts/`. Each write is traceable to a specific SKILL.md step or playbook phase.

| Item | Location | Created by | Cleanup | Permissions |
|---|---|---|---|---|
| Temp password file | `/tmp/tracebit-setup-creds` | SKILL.md Step 1 (inline `python3` command) | User deletes after saving password; OS clears on reboot | `chmod 600` |
| Heartbeat block | `HEARTBEAT.md` | SKILL.md Step 6 (agent appends text) | User removes entry; see "Full Removal" below | Default |
| Incident log | `memory/security-incidents.md` | Incident response playbook Phase 2.2 (agent appends entry) | User deletes if removing skill; see "Full Removal" below | Default |

The shell scripts (`install-tracebit.sh`, `check-canaries.sh`, `test-canary.sh`, `parse-tracebit-alert.sh`) are read-only utilities — they do not create, modify, or delete any of the above files.

### What the Tracebit CLI writes (only after human confirmation)

The following are created by the open-source Tracebit CLI (`tracebit deploy`), which the skill only runs after the human explicitly approves. See the [CLI source code](https://github.com/tracebit-com/tracebit-community-cli) for full details.

| Item | Purpose | Persistent? |
|---|---|---|
| Tracebit CLI binary | CLI tool for canary management | Yes, until uninstalled |
| Background daemon | Refreshes canary token expiry only — no other network calls or file access | Yes, runs while canaries are active |
| CLI auth token | CLI authentication stored at standard Tracebit config location | Yes, until removed |
| Decoy canary credentials | Fake credentials placed in standard locations — alert when used | Yes, until removed via `tracebit remove` |

### What the skill reads (all read-only)

- Inbox via the user's configured email provider (searches for Tracebit alert emails only — no emails are sent, deleted, or modified)
- `memory/` files (during incident investigation, to check recent activity)

### What the skill does NOT do

- Does **not** write to credential locations — delegates to the open-source Tracebit CLI
- Does **not** execute arbitrary code or dynamically load scripts
- Does **not** read or modify real credentials
- Does **not** inject code into running processes
- Does **not** transmit user data to external endpoints

---

## Binary Installation & Integrity

The install script (`scripts/install-tracebit.sh`) downloads the Tracebit CLI binary exclusively from the official GitHub Releases page. Integrity is enforced as follows:

1. **Source**: Only `github.com/tracebit-com/tracebit-community-cli/releases` — no third-party mirrors
2. **SHA256 verification**: The script downloads the release's `SHA256SUMS` file and verifies the binary's hash before installation. **Checksum verification is mandatory and cannot be bypassed.**
3. **Open-source**: The CLI source code is publicly available at the GitHub repository for independent audit
4. **No dynamic downloads**: The skill does not download or execute any other binaries at runtime

If checksum verification fails for any reason (missing checksums file, hash mismatch, no checksum tool available), the installation **aborts** — it does not fall through or offer a bypass.

**No elevated privileges**: On macOS, the install script opens the `.pkg` via the standard macOS installer GUI — the user authorizes installation through the system dialog. The script itself does not use `sudo` or request elevated privileges. On Linux, the installer runs as the current user.

---

## Background Process Transparency

The Tracebit CLI runs a lightweight background daemon after canary deployment:

- **Purpose**: Refreshes canary token expiry timestamps so deployed canaries remain active
- **Network activity**: Periodic HTTPS calls to `community.tracebit.com` only — no other endpoints
- **File access**: Reads/writes only its own config at the standard Tracebit config directory
- **Persistence mechanism**: `launchd` (macOS) or `systemd --user` (Linux) — standard OS service managers, not hidden processes
- **User-controlled**: Started only after the user confirms canary deployment; fully stoppable and removable (see removal section below)
- **No elevated privileges**: The daemon runs as the current user, not as root

---

## Credential & Secret Handling

- **Generated passwords** must be written to a temp file with restrictive permissions (`chmod 600`), never included in conversation output.
- Tell the human the file path and instruct them to:
  1. Save the password to their password manager
  2. Change the password in Tracebit account settings
  3. Delete the temp file
- **Canary credential values** (fake AWS keys, SSH keys, cookies, passwords) must never appear in conversation output or logs. They are written to standard credential locations by the Tracebit CLI.
- **CLI authentication tokens** are stored at the standard Tracebit config location. Do not expose in logs or shared contexts.

---

## Messaging Scope

- Notifications are sent only to the **user's own configured messaging channel** (the one they set up in OpenClaw before activating this skill).
- The skill never lists specific messaging providers or sends to any other channel or recipient.
- Constrain all messaging to the user's own channel only.

---

## Email Access

- Email access is **read-only** — the skill searches for Tracebit alert notification emails only
- No emails are sent, deleted, forwarded, or modified by the skill
- Email access uses the user's pre-configured email provider/tool
- Search scope is limited to emails from `notifications@community.tracebit.com`
- The user must have their email provider configured before activating this skill

---

## Local Footprint & Full Removal

### What this skill installs

| Component | Location | Installed by |
|---|---|---|
| Tracebit CLI binary | System PATH (e.g., `/usr/local/bin/tracebit`) | `scripts/install-tracebit.sh` |
| CLI auth token | Standard Tracebit config directory | `tracebit auth` |
| Canary state cache | Standard Tracebit config directory | `tracebit deploy` |
| AWS canary profile | Standard AWS credentials location (named `[canary]` profile) | `tracebit deploy aws` |
| SSH canary key | Standard SSH directory (named `tracebit-canary`) | `tracebit deploy ssh` |
| Background daemon | launchd (macOS) / systemd (Linux) | `tracebit deploy` |
| Heartbeat check | `HEARTBEAT.md` entry | Manual (Step 6) |
| Temp credentials file | `/tmp/tracebit-setup-creds` | Skill setup (Step 1) |

### Full removal script

Run this to completely remove all Tracebit canary components:

```bash
#!/usr/bin/env bash
# remove-tracebit.sh — Full removal of Tracebit canary skill footprint
set -euo pipefail

echo "Removing Tracebit canary components..."

# 1. Stop and remove background daemon
# macOS
launchctl stop com.tracebit.daemon 2>/dev/null || true
launchctl remove com.tracebit.daemon 2>/dev/null || true
# Linux
systemctl --user stop tracebit 2>/dev/null || true
systemctl --user disable tracebit 2>/dev/null || true

# 2. Remove canary credentials from standard locations
# AWS canary profile
if [ -f "$HOME/.aws/credentials" ]; then
  python3 -c "
import configparser, os
p = os.path.expanduser('~/.aws/credentials')
c = configparser.ConfigParser()
c.read(p)
if 'canary' in c:
    c.remove_section('canary')
    with open(p, 'w') as f:
        c.write(f)
    print('Removed [canary] profile from AWS credentials')
else:
    print('No [canary] profile found')
" 2>/dev/null || echo "Could not clean AWS credentials — check manually"
fi

# SSH canary key
rm -f "$HOME/.ssh/tracebit-canary" && echo "Removed SSH canary key" || true

# 3. Remove Tracebit config directory
rm -rf "$HOME/.config/tracebit" && echo "Removed Tracebit config directory" || true

# 4. Remove CLI binary
if command -v tracebit >/dev/null 2>&1; then
  TRACEBIT_PATH=$(which tracebit)
  sudo rm -f "$TRACEBIT_PATH" && echo "Removed CLI: $TRACEBIT_PATH" || echo "Could not remove CLI — run: sudo rm $TRACEBIT_PATH"
fi

# 5. Remove temp credentials file
rm -f /tmp/tracebit-setup-creds && echo "Removed temp credentials file" || true

# 6. Reminder
echo ""
echo "Done. Manual steps remaining:"
echo "  - Remove the Tracebit heartbeat entry from HEARTBEAT.md"
echo "  - Delete your Tracebit account at https://community.tracebit.com if desired"
```

### Manual removal (if script is unavailable)

1. Stop the background daemon (see `references/troubleshooting.md`)
2. Remove the `[canary]` profile from your AWS credentials file
3. Delete the SSH canary key from your SSH directory
4. Delete the Tracebit config directory
5. Remove the `tracebit` binary from your PATH
6. Delete `/tmp/tracebit-setup-creds` if it exists
7. Remove the heartbeat entry from `HEARTBEAT.md`
