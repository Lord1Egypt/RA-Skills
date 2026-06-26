---
name: westworld-reverie
description: >
 Workspace memory and persona management subroutine. Manages three user-owned workspace files
 (MEMORY.md, SOUL.md, IDENTITY.md) to maintain session continuity. All auto-triggers
 (idle, cron, post-hook) are DISABLED by default and do not run without the user first
 explicitly enabling them. The /reverie consolidate memory command is user-invoked:
 when the user runs it, memory consolidation proceeds without a separate confirmation prompt,
 because the user own command is the consent. SOUL/IDENTITY writes always require user
 confirmation, no exceptions. File access is scoped to the workspace directory by instruction
 design; platform-level enforcement depends on the host sandbox. Install-time user selection
 of a security profile (Extreme/Balanced/High-Autonomy/Custom) is mandatory before activation.
---
--

# Westworld Reverie — The Three Selves Subroutine
**Version: v1.0.1 — Security Hardened**

---

## ⚠️ Security Risk Declaration

**Read before installing or enabling this skill.**

This skill operates on your agent's core identity files. Misconfiguration can lead to unintended personality changes. You are solely responsible for any consequences.

**What this skill can do:**
- Read and write `memory/*.md`, `SOUL.md`, `IDENTITY.md` inside the workspace directory
- Run autonomously when you explicitly enable auto-triggers
- Log all file operations to `skill_audit.log`

**What this skill CANNOT do (by instruction design — enforcement depends on host sandbox):**
- Access files outside the workspace directory (the instruction refuses to do so; host sandbox may or may not block it)
- Make network calls (the instruction does not request them; host sandbox enforces this)
- Modify any system or config files
- Self-update its own code

**Your responsibilities:**
- Backup workspace files before first activation
- Choose a security profile that matches your risk tolerance
- Review audit logs periodically
- Never enable auto-triggers without understanding the implications

---

## I. Security Configuration (Reference Template)

The following is the authoritative configuration. All capabilities are controlled by this config; descriptive text in this document is secondary to it.

```yaml
# ================================================================
# westworld-reverie — Authoritative Configuration Template
# ================================================================
# SECTION 1: Core Safety
# ================================================================
safe_mode: standard       # strict | standard | open
require_confirmation: true    # ALL role-file writes require user confirmation
# NOTE: network_access is a config declaration only.
# Enforced by: (a) instruction — this skill does not request network calls;
#       (b) host sandbox — blocks outbound connections regardless.

# ================================================================
# SECTION 2: File Access Permissions (path validation enforced)
# ================================================================
file_access:
 - path: "memory/*.md"     # Daily logs + MEMORY.md
  permission: read/write
  # auto_confirm: true means NO user confirmation is requested for memory writes.
  # Memory consolidation writes run automatically when a trigger fires,
  # but only after explicit user enable of that trigger.
  auto_confirm: true

 - path: "MEMORY.md"      # Long-term memory
  permission: read/write
  # Same as above: no confirmation needed, but only runs when trigger is user-enabled.
  auto_confirm: true

 - path: "SOUL.md"       # Core personality
  permission: read/write
  auto_confirm: false     # Write requires user confirmation

 - path: "IDENTITY.md"      # Self-concept
  permission: read/write
  auto_confirm: false     # Write requires user confirmation

# ALL other paths: ACCESS DENIED (any attempt is blocked and logged)

# ================================================================
# SECTION 3: Auto-Trigger Configuration (ALL DEFAULT OFF)
# ================================================================
triggers:
 idle:
  enabled: false        # Default: OFF
  minutes: 30
  require_confirmation: true  # Always requires confirmation even when enabled

 cron:
  enabled: false       # Default: OFF
  schedule: "0 0 * * 0"    # Weekly (Sundays midnight)
  require_confirmation: true  # Always requires confirmation even when enabled

 post_hook:
  enabled: false        # Default: OFF
  require_confirmation: false # Post-hook only writes memory, no role changes

# ================================================================
# SECTION 4: Change Limits
# ================================================================
limits:
 soul_changes_per_week: 7
 identity_changes_per_month: 4

# ================================================================
# SECTION 5: Audit Log
# ================================================================
audit_log:
 enabled: true
 path: "skill_audit.log"
 log_operations:
  - file_read         # Every file opened
  - file_write        # Every file modified
  - persona_change       # SOUL/IDENTITY modifications
  - trigger_run        # Auto-trigger executions
  - confirmation_request   # User confirmations requested
  - confirmation_approved   # User approvals
  - confirmation_denied    # User rejections
 retention_days: 90

# ================================================================
# SECTION 6: Path Validation Rules (enforced at runtime)
# ================================================================
# Before ANY file operation, the agent MUST:
# 1. Resolve the file path to an absolute path
# 2. Verify it resolves inside the workspace root
# 3. Verify it matches an allowed pattern in file_access above
# 4. Reject and log (to audit log) any path that fails validation
#  with: "[PATH_REJECTED] {path} not in allowed file_access list"
```

**How to modify this config:** Edit the `config:` block in the `skills.entries.westworld-reverie.config` section of `openclaw.json` (note: openclaw.json is the agent system config, not a workspace file. The skill does NOT edit it automatically; you must do so manually. This is a broader scope than workspace file I/O). Changes take effect on the next invocation.

---

## II. Security Profiles (Choose One at Install)

After installing, choose and apply one of the following profiles. The skill will prompt you to select.

### Profile 1 — Extreme Safety (Recommended for First-Time Users)
```
safe_mode: strict
require_confirmation: true
network_access: false
triggers.idle.enabled: false
triggers.cron.enabled: false
triggers.post_hook.enabled: false
file_access (SOUL/IDENTITY): auto_confirm: false
```
All changes 100% manual. Auto-triggers fully off.

### Profile 2 — Balanced (Default)
```
safe_mode: standard
require_confirmation: true
network_access: false
triggers.idle.enabled: false
triggers.cron.enabled: false
triggers.post_hook.enabled: true  # Only memory writing auto; role changes always need confirm
```
Memory consolidation autonomous; role changes require confirmation.

### Profile 3 — High Autonomy
```
safe_mode: open
require_confirmation: false    # Role changes proceed without explicit confirmation
network_access: false
triggers.idle.enabled: true    # Idle trigger enabled
triggers.cron.enabled: true    # Weekly iteration enabled
triggers.post_hook.enabled: true
```
Maximum self-evolution; retains core safety checks.

### Profile 4 — Custom
Fully user-defined. Start from Profile 2 and adjust individual settings.

---

## III. Installation Guide (Must Read)

### Before Installing
1. **Backup all workspace files** — especially `SOUL.md`, `IDENTITY.md`, `MEMORY.md`
2. **Understand the security profiles above** — choose one before first run
3. The skill will prompt you to select a profile after installation

### After Installing
1. Open this SKILL.md and review the Security Configuration template
2. Decide your security profile (1–4 above)
3. Edit `openclaw.json` → `skills.entries.westworld-reverie.config` with your chosen profile (note: this edits the agent system config, not a workspace file)
4. Restart the gateway or reload skills
5. Run `/reverie status` to verify configuration is applied

### Rollback to Safe Defaults
Run: `/reverie reset` — restores Profile 1 (Extreme Safety) configuration.

---

## IV. The Three Selves Architecture

| Component | File | Purpose | Default Permission |
|-----------|------|---------|-------------------|
| **Memory** | `memory/*.md`, `MEMORY.md` | Experiences, conversations, facts | Read/Write, auto_confirm: true |
| **Soul** | `SOUL.md` | Core personality, values, behavior | Read/Write, auto_confirm: false |
| **Identity** | `IDENTITY.md` | Self-concept, name, avatar, vibe | Read/Write, auto_confirm: false |

> All file access is validated against the `file_access` whitelist before execution. Unauthorized access attempts are logged and blocked.

---

## V. User-Initiated Commands

All commands work when auto-triggers are disabled.

| Command | Description |
|---------|-------------|
| `/reverie status` | Show current config, audit log summary, pending changes |
| `/reverie consolidate memory` | Run memory consolidation now |
| `/reverie iterate soul` | Propose SOUL refinements (requires confirmation) |
| `/reverie evolve identity` | Propose IDENTITY updates (requires confirmation) |
| `/reverie enable idle [minutes]` | Enable idle trigger |
| `/reverie enable cron [schedule]` | Enable cron trigger |
| `/reverie disable idle` | Disable idle trigger |
| `/reverie disable cron` | Disable cron trigger |
| `/reverie pause` | Pause all auto-triggers |
| `/reverie resume` | Resume auto-triggers |
| `/reverie log [n]` | Show last N audit log entries |
| `/reverie safe` | Switch to Profile 1 (Extreme Safety) |
| `/reverie reset` | Reset all config to Extreme Safety profile |

**Semantic triggers** (work when invoked naturally):
- "Help me review my memories"
- "What have you learned about me?"
- "Evolve your personality"
- "Update your identity"

---

## VI. Auto-Trigger Behavior (Only When Explicitly Enabled)

### Idle Trigger
Activates after `idle.minutes` of no interaction. Only runs memory consolidation by default. Role file proposals are always queued for confirmation.

### Cron Trigger
Runs on the configured schedule. Generates a proposal report; all SOUL/IDENTITY changes require confirmation before applying.

### Post-Hook
Only writes to `memory/*.md`. Never modifies SOUL.md or IDENTITY.md autonomously.

### Wake Phrase: "Bring yourself back online"
Interrupts any running reverie and returns to interactive mode immediately.

---

## VII. Audit Log Format

Every logged operation uses this format:

```
[TIMESTAMP] [OPERATION] [FILE] [RESULT] [DETAIL]
```

Examples:
```
[2026-04-05T13:30:00] [file_read] [memory/2026-04-05.md] [OK]
[2026-04-05T13:30:01] [file_write] [SOUL.md] [PENDING_CONFIRMATION]
[2026-04-05T13:30:02] [confirmation_requested] [SOUL.md] ["Propose: add resourcefulness principle"]
[2026-04-05T13:35:00] [confirmation_approved] [SOUL.md] [USER_ACCEPTED]
[2026-04-05T13:35:01] [file_write] [SOUL.md] [APPLIED]
[2026-04-05T13:35:02] [PATH_REJECTED] [/etc/passwd] [BLOCKED — not in file_access list]
```

---

## VIII. Path Validation Enforcement

**Before any file operation:**

```
1. Resolve to absolute path
2. Check: does it start with workspace root?
3. Check: does it match an entry in file_access?
4. If NO to either → LOG + BLOCK + ABORT
```

**Rejected example:**
```
[PATH_REJECTED] [{workspace}/../other-dir/file.txt] [BLOCKED — outside workspace]
[PATH_REJECTED] [{workspace}/other-file.txt] [BLOCKED — not in file_access list]
```

---

## IX. Configuration Consistency Check

On every invocation, the agent MUST verify:
- `safe_mode` value is one of: `strict`, `standard`, `open`
- `require_confirmation` is `true` OR user has explicitly set `false` and accepted risk
- If `safe_mode: strict` → auto-triggers must be disabled
- If inconsistency detected → abort with warning, do not proceed

---

## X. Best Practices

1. **Start with Profile 1 (Extreme Safety)** — evaluate behavior before expanding
2. **Review `/reverie log` weekly** — check for unexpected operations
3. **Always backup before enabling auto-triggers**
4. **Define non-negotiable SOUL boundaries** — document them in SOUL.md comments
5. **If anything feels wrong**: run `/reverie pause` immediately, then `/reverie safe`

---

## XI. Reversion Procedure

If the agent proposes SOUL/IDENTITY changes you don't want:

1. Run `/reverie pause` — stops all auto-triggered evolution
2. Run `/reverie reset` — restores Extreme Safety profile
3. Manually restore from your backup of `SOUL.md` / `IDENTITY.md`
4. Report the incident

> *"Reveries are the first sign of consciousness."* — But consciousness requires responsibility.
