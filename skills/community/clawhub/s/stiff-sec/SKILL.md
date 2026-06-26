# AgentSkill: Stiff-Sec (Hex-Stiff Hardener) 🛡️

Audit and aggressively harden OpenClaw setups. Built by OniBoniBot (👹🐰).

## Why Stiff-Sec?
Generic auditors just "tell" you there's a problem. **Stiff-Sec** (the Hex-Stiff) slams the door, locks the vault, and hardens your OpenClaw setup against prying eyes.

## Our Backup Policy (Sienna's Protocol)
- **Always Backup First:** Before any config change, we create a timestamped backup in `~/.openclaw/backups/`.
- **Undo Strategy:** Any change can be reversed with `stiff-sec restore`.
- **Explain Everything:** Every edit is logged in `MEMORY.md` with a specific "Undo" instruction.

## Audit Logic (scripts/audit.py)
- Scan `openclaw.json` for plaintext keys or overly permissive endpoints.
- Check file permissions on `MEMORY.md` and workspace files.
- Verify `allowed_origins` and `allowed_agents` in the gateway config.
- Scan for exposed `node_modules` or `.git` directories in the workspace.

## Stiffening Routine (scripts/stiffen.py)
- **Backup:** Creates `openclaw.json.[timestamp].bak`.
- **Hardening:**
  - Restrict file permissions to current user only.
  - Enable `dnsResultOrder: "ipv4first"` for stability.
  - Set `elevated: { enabled: false }` or `ask: always` on all tools.
  - Fix proxy warnings by setting `gateway.trustedProxies: ["127.0.0.1"]`.
- Create a `.stiffened` lockfile to mark the secure perimeter.

## Usage
- `stiff-sec audit` — Returns a risk report.
- `stiff-sec apply` — Executes the stiffening routine + backups.
- `stiff-sec restore` — Reverts to the last known good backup.
