# Path Resolution Rules

Use these rules to resolve the archive root for system change archives.

## Resolution order

1. Explicit CLI argument: `--archive-root`
2. Environment variable: `SYSTEM_CHANGE_ARCHIVE_ROOT`
3. Known persistent candidates (first existing and writable):
   - `/data/disk`
   - `/mnt/data`
   - `/data`
   - `/srv/data`
   - `/Volumes/Data`
4. Fallback under the current workspace:
   - `<workspace>/.system-change-archive-fallback`

## Behavior requirements

- Prefer persistent storage whenever possible.
- Never silently pretend fallback storage is equivalent to a mounted persistent volume.
- If fallback is used, explicitly report that restart-failure survivability is weaker.
- The skill must not hardcode one user’s host-specific path as the universal default.

## Output contract

The initializer script should print or return:
- selected archive root
- whether it is persistent or fallback
- the created change directory
- any warnings

## Why this exists

Different users keep durable backups in different places. The portable part of the skill is the archive structure and workflow, not the mount path itself.
