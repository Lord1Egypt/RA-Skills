# Release Notes: wip-ai-devops-toolbox v1.9.51

## Branch Guard: Workspace Files Allowlist (#185)

Added TOOLS.md, MEMORY.md, IDENTITY.md, SOUL.md, WHERE-TO-WRITE.md, HEARTBEAT.md to the shared state allowlist. Both agents can now write to workspace files on main without being blocked.

Previously only SHARED-CONTEXT.md was allowed. This broke Lesa's ability to edit her own workspace files during the migration to ~/wipcomputerinc/.

## TECHNICAL.md: Backup Documentation

Updated LDM Dev Tools.app backup section to reflect the unified backup system. backup.sh now calls `~/.ldm/bin/ldm-backup.sh` (deployed by ldm install from wip-ldm-os-private/scripts/).
