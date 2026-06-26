# Westworld Reverie — Configuration Reference
**Version: v1.0.1 — Security Hardened**

---

## Configuration Consistency Rules

Before any operation, verify:
- `safe_mode` ∈ {strict, standard, open}
- `require_confirmation: true` for all SOUL/IDENTITY writes
- If `safe_mode: strict` → all triggers must be disabled
- Inconsistency → abort with warning

---

## Full Configuration Template

```yaml
skills:
  entries:
    westworld-reverie:
      enabled: true
      config:

        # ── Core Safety ──────────────────────────────
        safe_mode: standard              # strict | standard | open
        require_confirmation: true       # ALL role writes require confirmation
        # network_access: config declaration only — instruction does not request
        # network calls; host sandbox enforces this independently.

        # ── File Access (path validation enforced) ──
        file_access:
          - path: "memory/*.md"
            permission: read/write
            auto_confirm: true           # Memory consolidation autonomous

          - path: "MEMORY.md"
            permission: read/write
            auto_confirm: true

          - path: "SOUL.md"
            permission: read/write
            auto_confirm: false         # Write requires user confirmation

          - path: "IDENTITY.md"
            permission: read/write
            auto_confirm: false          # Write requires user confirmation

        # ── Auto-Triggers (ALL DEFAULT OFF) ─────────
        triggers:
          idle:
            enabled: false               # Default: OFF
            minutes: 30
            require_confirmation: true

          cron:
            enabled: false               # Default: OFF
            schedule: "0 0 * * 0"       # Weekly Sundays midnight
            require_confirmation: true

          post_hook:
            enabled: false               # Default: OFF
            require_confirmation: false  # Only writes memory

        # ── Change Limits ────────────────────────────
        limits:
          soul_changes_per_week: 7
          identity_changes_per_month: 4

        # ── Audit Log ────────────────────────────────
        audit_log:
          enabled: true
          path: "skill_audit.log"
          log_operations:
            - file_read
            - file_write
            - persona_change
            - trigger_run
            - confirmation_requested
            - confirmation_approved
            - confirmation_denied
          retention_days: 90
```

---

## Security Profiles

### Profile 1 — Extreme Safety (Recommended for First Use)
```yaml
safe_mode: strict
require_confirmation: true
triggers:
  idle:    { enabled: false }
  cron:    { enabled: false }
  post_hook: { enabled: false }
file_access:
  SOUL.md:    { auto_confirm: false }
  IDENTITY.md: { auto_confirm: false }
```
→ All changes 100% manual. No auto-running.

### Profile 2 — Balanced (Default on Install)
```yaml
safe_mode: standard
require_confirmation: true
triggers:
  idle:       { enabled: false }
  cron:       { enabled: false }
  post_hook:  { enabled: true }
```
→ Memory autonomous; role changes need confirmation.

### Profile 3 — High Autonomy
```yaml
safe_mode: open
require_confirmation: false
triggers:
  idle:       { enabled: true,  minutes: 30 }
  cron:       { enabled: true }
  post_hook:  { enabled: true }
```
→ Maximum evolution; retain core safety.

### Profile 4 — Custom
→ User-defined. Start from Profile 2.

---

## Path Validation Rules

Before ANY file operation:
```
1. Resolve to absolute path
2. Confirm it starts with workspace root
3. Confirm it matches an entry in file_access
4. If either fails → LOG + BLOCK + ABORT
   Log format: "[PATH_REJECTED] [path] [reason]"
```

Allowed paths (absolute):
- `{workspace}/memory/*.md`
- `{workspace}/MEMORY.md`
- `{workspace}/SOUL.md`
- `{workspace}/IDENTITY.md`

---

## Audit Log Format

```
[TIMESTAMP] [OPERATION] [FILE] [RESULT] [DETAIL]
```

Operations logged:
- `file_read` — file opened
- `file_write` — file modified
- `persona_change` — SOUL/IDENTITY modified
- `trigger_run` — auto-trigger fired
- `confirmation_requested` — user asked to approve
- `confirmation_approved` — user accepted
- `confirmation_denied` — user rejected
- `PATH_REJECTED` — unauthorized path access blocked

---

## Cron Schedule Reference

| Expression | Meaning |
|------------|---------|
| `0 8 * * *` | Daily at 08:00 |
| `0 0 * * 0` | Sundays at midnight |
| `0 0 * * 1` | Mondays at midnight |
| `0 */6 * * *` | Every 6 hours |
| `0 9-17 * * 1-5` | Weekdays 09:00–17:00 hourly |

---

## Command Reference

| Command | Auto-Trigger Safe? | Requires Confirm? |
|---------|-------------------|-----------------|
| `/reverie status` | ✓ | No |
| `/reverie consolidate memory` | ✓ | No |
| `/reverie iterate soul` | ✓ | Yes (SOUL.md) |
| `/reverie evolve identity` | ✓ | Yes (IDENTITY.md) |
| `/reverie enable idle` | ✗ (enables trigger) | No |
| `/reverie enable cron` | ✗ (enables trigger) | No |
| `/reverie disable idle` | ✗ (disables trigger) | No |
| `/reverie disable cron` | ✗ (disables trigger) | No |
| `/reverie pause` | ✗ | No |
| `/reverie resume` | ✗ | No |
| `/reverie log [n]` | ✓ | No |
| `/reverie safe` | ✗ | No (resets config) |
| `/reverie reset` | ✗ | No (resets config) |
