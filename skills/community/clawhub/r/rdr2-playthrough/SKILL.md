---
name: rdr2-playthrough
description: Use when maintaining RDR2 (Red Dead Redemption 2) playthrough notes — logging an acquisition ("acquired X", "got N gold bars", "finished X"), answering in-game location/crafting questions, or reviewing the notes for duplicate or stale info. Triggers on RDR2, Red Dead Redemption, playthrough, legendary animal, talisman, trinket, valerian root, gold bar, horse, weapon, berry.
---

# RDR2 Playthrough Notes

Maintain the user's RDR2 Chapter 2 playthrough notes — typically a single Markdown file (e.g. `rdr2-ch2.md`).

## About this skill

- RDR2 = **Red Dead Redemption 2**, one of the most famous, iconic games in gaming history.
- This skill exists to write the playthrough notes — just for fun.
- Not affiliated with Rockstar Games, the producer of the game.
- No business or commercial intent.

## Hard rules

- **Just for fun — low stakes.** These playthrough notes are personal and not sensitive; no confidentiality handling is required.
- **Get the user's approval before writing into the note.** Propose the exact edit (section, row, text) and wait for the user's go-ahead before touching the notes file. A progress report ("acquired X") is not by itself approval to write; structural changes (new sections, reordering, rewrites, deleting rows) always require approval.
- **Keep notes as simple as possible.** One fact, one place.
- **Alert the user about duplicated info found** — say so, don't silently delete or merge. Deletion of existing content needs approval.
- **Escape `$` as `\$` in Markdown tables** (e.g. `\$45`) to avoid parse errors.
- **Never guess game facts.** Verify names, locations, recipes, prices, and effects via web search before writing. If unverified, say so and leave it out.
- **Never commit or publish the user's notes without explicit approval.**

## Status markers (conventions)

- List items: wrap the title in `~~strikethrough~~` and append `(acquired)`.
- Table rows: append `— acquired` (or `— shot` for hunted legendary animals).
- Pending items: append `— pending` and describe what is still needed.

## Workflow

1. **Locate the section.** A typical RDR2 Chapter 2 notes file is organized into:
   - Progress Strategy — chapter-2 gating rules
   - Weapon Strategy & Acquisitions — weapons; method/source; cross-reference the Store Backroom section instead of restating robbery steps
   - Horse and Equipment — horses and tack
   - Gold Bars — the quantity table plus per-treasure subsections (Strange Statues, Jack Hall Gang, Poisonous Trail)
   - Valerian Root (Dead Eye XP) — fixed spawn locations
   - Store Backroom (Illicit) Business Robberies — the four backroom robberies
   - Legendary Animal Pelts — animal / location / trapper crafting
   - Trinket Components — one-of-a-kind components and talisman recipes
   - Herbal Collection Challenge — berry species
   - Serial Killer "American Dreams" — murder scenes and reward
2. **Verify** any fact not already established in the file (web search). Prefer IGN, RDR2.org, Fandom wiki, GamesRadar.
3. **Edit minimally.** Add or annotate a row/bullet. If a description already lives in another section, point to it (`see Store Backroom ...`) rather than duplicating.
4. **New section?** Add it to the Table of Contents with a matching anchor, and place it in a sensible spot relative to related sections.
5. **Check for duplicates** across sections; report findings to the user.
6. **Reply concisely** with what changed (show the row when useful) and offer the obvious next in-game step.

## Output conventions

- Docs are English; keep the existing tone (terse, location-first).
- Keep each table's existing column structure.
- Use `→` for "yields/leads to" and `—` for status, matching existing rows.
- Images referenced as `../imgs/<filename>`.
- No hard-wrapping prose: one paragraph per line (rewrap with the repo's unwrap script, if it has one).

## Checklist before finishing

- [ ] User approved the write before editing the note
- [ ] Fact verified or explicitly marked unverified
- [ ] `$` escaped in any table cell
- [ ] Status marker applied (`— acquired` / `— shot` / `~~…~~`)
- [ ] No duplicated description (cross-referenced instead)
- [ ] TOC updated if a section was added
- [ ] Duplicate info reported to the user
- [ ] No commit or push without explicit user approval