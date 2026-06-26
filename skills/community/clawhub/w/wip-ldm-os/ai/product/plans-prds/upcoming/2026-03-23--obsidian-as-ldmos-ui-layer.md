# Plan: Obsidian as LDMOS UI Layer

**Date:** 2026-03-23
**Author:** Claude Opus (with Parker)
**Status:** Upcoming
**Source:** @cyrilXBT post on Obsidian + Claude Code as "personal JARVIS"

## Context

A post going around frames Obsidian + Claude Code as the way to build a personal AI assistant. The pitch: your Obsidian vault is your knowledge base, Claude Code reads it, and now your AI answers from your own thinking instead of the internet.

LDM OS is already building a more complete version of this. The workspace root (`~/wipcomputer/`) with `staff/`, `docs/`, plans, journals, and Memory Crystals is structurally equivalent to an Obsidian vault — it's all local markdown. The difference is LDM OS supports multiple agents, shared memory, and cross-agent collaboration.

## What We Should Do

### 1. Obsidian Compatibility (Low effort, high signal)

The LDMOS workspace root is already a folder of markdown files. If a user opens it in Obsidian, it should just work.

Action items:
- Test opening `~/wipcomputer/` as an Obsidian vault
- Identify any file naming or linking conventions that would make Obsidian's graph view and backlinks useful (e.g., `[[wikilinks]]` in plans and notes)
- Consider shipping a minimal `.obsidian/` config in the workspace template (just workspace layout, no plugins required)
- Document this as a supported workflow: "Open your LDMOS workspace in Obsidian for a GUI"

### 2. Onboarding Path for Obsidian Users

People already using Obsidian have a vault full of markdown. LDM OS could offer an import or symlink path.

Action items:
- Add an option to `ldm init` that accepts an existing Obsidian vault path
- Symlink or mount the vault into the workspace under `staff/<user>/vault/` or similar
- All agents then have access to the user's existing knowledge base through the standard workspace structure

### 3. Marketing and Content

The "JARVIS" framing resonates. LDM OS goes further — it's JARVIS for a whole team of AIs, not just one.

Angles to explore:
- "Obsidian + LDM OS" post in the same style as the original
- Comparison: single AI + vault (what the post describes) vs. multi-agent + shared memory (what LDM OS does)
- Demo video: open workspace in Obsidian, show the graph of plans/notes/journals, then show Claude Code and Lesa both reading from and writing to the same workspace

### 4. Workspace Root Enhancements

If Obsidian users are a target audience, a few small changes to the workspace structure would make the experience better:

- Consistent use of YAML frontmatter in plans and notes (Obsidian uses this for metadata/search)
- Tags in frontmatter (Obsidian's tag pane becomes useful)
- Consider a `_templates/` folder compatible with Obsidian's Templater plugin

## What We Should NOT Do

- Don't make Obsidian a dependency. The workspace is plain markdown. Obsidian is one optional viewer.
- Don't build Obsidian plugins. The value is in the data layer (LDM OS), not the UI layer.
- Don't restructure the workspace to fit Obsidian conventions. Obsidian should adapt to us, not the other way around.

## TODO

- [ ] Add @cyrilXBT's Obsidian + Claude Code post to `acknowledgments.md` as inspiration for this plan

## Priority

Low-medium. The compatibility story is almost free — the workspace is already markdown. The onboarding path and marketing content are worth doing when we're ready to talk about the workspace root publicly.
