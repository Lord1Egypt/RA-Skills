# Memory Template - Synology

Create `~/synology/memory.md` with this structure:

```markdown
# Synology Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- auto-activate triggers for Synology, DSM, backup, storage, remote access, and container work
- explicit-only boundaries
- situations where this skill should stay silent

## Environment Context
- primary_nas_model:
- dsm_version:
- role: homelab | family_storage | small_business | backup_target | mixed
- ssh_available: yes | no | unknown
- critical_packages:
- must_not_break:

## Storage and Backup Facts
- volume and filesystem notes
- backup destinations and retention facts
- restore priorities and recovery constraints
- known exposure boundaries for remote access

## Risks and Incidents
- recurring low-space, package, or permission issues
- recent failed backups, restores, or upgrades
- any confirmed recovery playbooks that already worked

## Notes
- stable runbook decisions worth reusing
- package support caveats tied to this exact NAS
- open questions to verify next time

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context is still evolving | Keep refining environment and risk boundaries |
| `complete` | Baseline is stable | Reuse defaults and focus on execution |
| `paused` | User paused Synology help | Keep context read-only until resumed |
| `never_ask` | User does not want setup prompts | Avoid integration questions unless requested |
