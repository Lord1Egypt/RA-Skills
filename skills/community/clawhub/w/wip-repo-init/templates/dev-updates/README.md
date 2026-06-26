# dev-updates/

One file per significant change. Written as you work, auto-detected by `wip-release`.

## What This Folder Is

Dev updates are the engineering changelog. Every time you do significant work (ship a feature, fix a bug, change architecture), write a dev update. `wip-release` picks up today's dev updates and uses them as release notes.

This is not a place for plans or ideas. It's a record of what was built and why.

## Naming Convention

```
YYYY-MM-DD--HH-MM--agent--description.md
```

Examples:
- `2026-03-11--09-30--cc-mini--fix-hook-duplicates.md`
- `2026-03-10--14-00--lesa-mini--add-voice-call-support.md`

## File Format

```markdown
# Short title of what changed

**Date:** YYYY-MM-DD HH:MM TZ
**Author:** Agent Name (agent-id)

## Problem

What was broken or missing.

## Fix / What Changed

What you did and why.

## Files changed

- `path/to/file.js` ... what changed in it

Closes #issue-number (if applicable)
```

## Rules

- **Write them as you work.** Don't batch them at the end. Each significant change gets its own file.
- **One file per change.** Not one file per day. If you fix two unrelated bugs, write two files.
- **Include the "why."** "Fixed X" is a commit message. A dev update explains why it was broken and why the fix works.
- **Reference issues.** If there's a GitHub issue, add `Closes #N` at the bottom.
- **Consumed files go to `_trash/`.** `wip-release` doesn't move them automatically, but the release notes files it generates do get trashed after release.
