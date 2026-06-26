# Dev Update: CLAUDE.md Repo Paths Fix + Boot Sequence Enforcement

**Date:** 2026-03-07 15:50 PST
**Author:** CC-Mini

---

## What happened

CC-Mini booted without reading the full boot sequence (skipped steps 6-10). When asked to find the mdview repo, guessed wrong paths, tried to glob Lesa's folders, almost cloned a repo that already existed. Parker had to manually direct CC to the correct location. This is the same class of failure that happened on 2026-03-01.

Root cause: CLAUDE.md had stale repo paths pointing to the old flat `repos/` layout. The ldm-os organizational folder structure (set up 2026-02-26) was never reflected in CLAUDE.md. CC's auto-memory file (`repo-locations.md`) had the correct info but wasn't read because steps 6-10 of the boot sequence were treated as optional.

## Changes to CLAUDE.md

1. **Directory structure tree** updated to show `ldm-os/` with all six subfolders (apps, components, operations, utilities, apis, identity)
2. **wip-release path** fixed: `repos/wip-release/` changed to `ldm-os/operations/wip-dev-tools-private/tools/wip-release/`
3. **mdview reference** fixed: removed "repo clone was trashed", added correct source path `ldm-os/apps/wip-markdown-viewer-private/`
4. **dream-weaver-protocol-private path** fixed to `ldm-os/components/`
5. **wip-healthcheck paths** fixed to `ldm-os/utilities/`
6. **Plugin source repos** reference fixed to point inside `ldm-os/`
7. **open-claw-upgrade path** fixed to `ldm-os/utilities/`
8. **Boot sequence steps 6-10** changed from "also read these" to **"ALL steps are mandatory. Do not skip any."**
9. Added step 10: read `~/.claude/projects/.../memory/repo-locations.md`
10. Added note: repos without `-private` haven't been converted to the public/private pattern yet

## Changes to repo-locations.md (CC auto-memory)

- Removed "monorepo" language. It's an organizational folder structure, not a monorepo.
- Added complete listing of all repos in all six ldm-os subfolders
- Added boot sequence reminder at the bottom

## Lesson learned

CLAUDE.md is the first thing CC reads. If it has stale paths, CC starts the session with wrong assumptions and every subsequent action is based on bad data. The boot sequence exists to correct for this, but only if all steps are read. Making steps 6-10 "optional" was a design error.
