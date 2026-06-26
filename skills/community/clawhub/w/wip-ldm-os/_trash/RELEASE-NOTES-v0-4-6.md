# LDM OS v0.4.6

`ldm status` now tells you what needs updating before you ask.

## What changed

`ldm status` checks every installed extension against npm and shows version diffs. No more "everything looks fine" when 3 extensions are behind. The SKILL.md now tells the AI to run `ldm status` before presenting the summary, so users see updates upfront.

Also reads from the actual installed package.json, not the registry (which could be stale).

## Issues closed

- Closes #34
- Closes #60
