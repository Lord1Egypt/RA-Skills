# Promotion Guide

Use promotion only when a learning is broadly reusable.

## Promote to AGENTS.md
When the learning changes execution workflow.
Examples:
- deploy ownership rules
- acceptance ownership rules
- escalation timing

## Promote to TOOLS.md
When the learning is an environment/tool routing rule.
Examples:
- use Tavily before Brave
- key locations in Keychain
- browser session attach rules

## Promote to SOUL.md
When the learning is a behavior/principle rule.
Examples:
- do not let no-assignment closeout replace required deliverables
- do not treat shallow checks as full acceptance

## Promote to Obsidian
When the learning should become reusable operator material, marketing proof, or an operations note outside transient chat.

By default, Obsidian-style exports go to the local safe fallback:
- `.learnings/exports/obsidian/`

If you want a real vault destination, set `OBSIDIAN_LEARNINGS_DIR` explicitly before running the promotion script.
Always confirm the printed target path first, or use `--dry-run`.

Example:
- `node scripts/promote-learning.mjs obsidian "Reusable learning" --dry-run`
- then rerun without `--dry-run` after confirming the path
