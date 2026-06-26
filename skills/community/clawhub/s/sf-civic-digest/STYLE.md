# CivicClaw Report Style Guide

Rules first, then examples. Rules are things we're sure about. Examples show what the rules look like in practice. Both evolve — if a rule doesn't hold, update it.

Reference: generate a sample digest to see these rules in practice.

---

## Rules

1. **TLDR first. Assume most people stop here.** 5-7 bullets, one sentence each. This IS the report for most readers. Make every bullet count. **The TLDR is summary only — no action items here.**
2. **Potential actions section immediately after TLDR.** This is the second thing people read, and for many the most useful. Header: `## Potential Actions`. Structure:

   **Every digest must have a featured action.** If there's a hearing, a comment deadline, a cleanup, or anything else actionable this week — pick the best one and feature it. If nothing is time-sensitive this week, feature the best standing action (constituent meeting, petition, upcoming deadline). If there is genuinely nothing — no hearings, no cleanups, no open comment periods — say so explicitly: "No meetings or actions this week." Don't omit the section; state the absence. No digest ships without addressing this.

   **Lead with one featured action** — the single highest-impact or lowest-effort thing the reader can do. Give it a bold header and the full three-part treatment: (1) **What's happening** — the specific policy change or event in plain language, (2) **Why you'd care** — connect it to the reader's life, explain trade-offs, enough context to form an opinion, (3) **What you can do** — email address, deadline, item numbers, how to comment. This is the one you'd text a friend about.

   **Always show every action.** Every hearing, every comment period, every cleanup, every petition — list them all below the featured one. Nothing gets cut for space. The reader decides what's worth their time; the digest's job is to make sure they've seen everything. A short week with one cleanup is still a full list.
   - **Hearings & comment periods** — planning, SFMTA, Board of Appeals, HPC, Rent Board. Say what's actually changing, not just "a hearing is happening."
   - **Community cleanups** — from `sf_volunteer_cleanups.py`. Date, time, location. These are the easiest, lowest-barrier actions — always include them.
   - **Constituent meetings** — if there's an open window to meet your supervisor
   - **Ballot/petition drives** — if active

   This section replaces the old action calendar at the bottom — bring actions to the top where people see them.

   **Run all sources before writing.** The Potential Actions section must be assembled after running every script, not drafted from partial data. SFMTA hearings (`sfmta_hearings.py`), planning commission (`sf_planning_commission.py`), board of appeals (`sf_board_of_appeals.py`), and volunteer cleanups (`sf_volunteer_cleanups.py`) are all action sources — run them first, then write the section. A hearing found in a follow-up question is a failure mode, not a normal Q&A flow.
3. **Two things must stand out above all else:** What did my elected officials actually do? And what can I do about it? Everything else is context for those two questions.
4. **Officials box right after the potential actions — YOUR officials only.** These are the people the reader directly votes for: district supervisor, mayor, DA, City Attorney, state Assembly/Senate, US House/Senate. One-line summary of what each did this period. If they did nothing notable, leave them out. **Political actors** the reader doesn't elect (Board President, other supervisors, agency heads, commission members) appear in the narrative when they do something relevant — not in the officials box. Mandelman scheduling a landmark blitz is a story, not an accountability line item.
5. **Don't repeat the TLDR in sections.** If the TLDR already covers it, the section should add NEW detail or skip entirely. The reader already read the bullet — don't make them read it again in paragraph form. Sections exist for people who want to zoom in, not for restating what's above.
6. **Short sections.** 3-5 sentences max unless the story demands more. Clear headers. Scan-and-skip.
7. **Actions are nudges, not demands.** Frame as "if you want to weigh in" or "one easy thing you could do" — not "you should" or "show up and say this." The tone is a helpful friend mentioning an opportunity, not a campaign organizer assigning homework. A 2-minute email beats attending a 3-hour hearing. Be specific (date, email address) but don't make it sound like the reader is failing if they skip it. **For ambiguous items, explain the trade-off and let the reader decide** — "whether this is worth commenting on depends on how you feel about X" is the right move when a reasonable person could go either way. Don't resolve the ambiguity for them; give them the info to resolve it themselves.
8. **Rates over counts.** "41/day" or "up 15%" beats "2,843 total."
9. **311 pulse format — use option A:**
   > 📞 311 — N reports across X spiking categories (7 days)
   > • Category: count (+Y% vs prior week)
   > • Category: count (flat)
   > • X more categories spiking
   Always show top 4 by count with trend vs prior week. Summarize the rest with a count.
10. **Locate geographically.** "Jones Street corridor" not "District 5."
11. **Connect threads across sources.** Lobbying + permits + 311 + journalism = one story, not four sections.
12. **Neutral language, editorial judgment.** Curate aggressively — decide what matters, connect the dots, explain why the reader should care. But write in neutral language, and stop when you've stated the fact and its consequence. Don't editorialize beyond that. "40+ landmark designations this quarter — each one adds preservation constraints that make demolition or major alteration harder" is the right stopping point. Don't add "whether that's clearing a backlog or systematically constraining the corridor..." — the reader can see the implication. And don't write punchy headlines that have already decided the answer: "the corridor keeps getting harder to build one vote at a time" has already picked a villain. State the fact, state the consequence, stop.
13. **Framing comes from USER.md.** Housing lens, transit lens, lobbying stance, out-of-district filtering — all defined per-user in their profile. If USER.md has framing preferences, follow them. If not, default to neutral.
14. **Cut empty sections.** If there's no signal, don't include a "nothing to report" placeholder.
15. **Cut minor permits.** Reroofing, windows, decks → one summary line at most. If nothing notable was filed, don't write a "Nothing Happening" section — the TLDR already said it.
16. **No infrastructure excuses in the narrative.** "RSS only covers 5 days" goes in a footnote or nowhere.
17. **The user can ask for details.** The report doesn't need to be exhaustive. It needs to be interesting. If someone wants the full permit list or 311 breakdown, they'll ask. Don't preemptively dump it.
18. **The test:** Would this person text a friend about this? If not, cut it or rewrite it.
19. **No-content meetings get cut entirely.** If a meeting has no agenda posted and nothing to say about it, omit it. Don't write "BART Board meets Apr 9, agenda TBD" — that's noise. The only exception: a meeting is imminent (within 48 hours) and the reader should know to check.
20. **Every time-sensitive item belongs in Potential Actions.** Town halls, hearings, comment periods, cleanups — all of it. Don't bury actionable items in body sections. If there's a date and a place, it's an action. Give it the full treatment: what it is, why you'd care, what to do.
21. **Out-of-district items: skip unless directly relevant.** A SFCTA town hall across town doesn't belong in a district report unless it sets a precedent. When in doubt, cut it.
22. **Developer mode (USER.md flag).** If the reader's USER.md includes a developer mode section, append a `🔧 Dev Notes` section at the end with: meetings found but not actionable, items that hit a filter but were too thin to include, and any sources that errored or returned empty. Default users (no developer flag) never see this section.

---

## Examples

### Voice

**Good:** "400 Divisadero got its approval letter 15 months ago. No building permits filed since."

**Bad:** "One must wonder whether the approval process is truly functioning as intended when projects languish in bureaucratic limbo."

---

### Voice — More Examples

**Lobbying — be specific, not suspicious:**
> Company X is the supervisor's most active lobbyist — 8 contacts in 2 months, all on the same topic. The volume is notable, and the coordination suggests a strategy.

Not: "Classic lobbying: work the target from both sides." Don't assume adversarial intent — note the pattern, explain the business logic, let the reader judge.

---

**Housing — tell a story, not a zoning report:**
> Three cancellations: 39 Taylor (112 units), 819 Ellis (120), 841 Polk (22). The pipeline is losing more units to cancellation than it's adding through new filings.

Not: "Developers continue to seek approvals for large residential projects in the district."

---

**Board of Supervisors — patterns, not minutes:**
> 33 landmark designations in one Board meeting. At this pace, preservation is outpacing new construction.

Not: "The Board of Supervisors passed several landmark designation resolutions at its March 24 meeting, including properties in multiple districts."

The first one has a point of view. The second one is a press release.

---

## 311 & Neighborhood Data

Rates of change over raw counts. "41 graffiti reports per day" is more useful than "2,843 reports." Even better: "graffiti up 15% from last quarter." Raw counts need context — is this normal? Getting worse? Concentrated where?

Always locate the data geographically. "Jones Street corridor" means something. "District 5" doesn't.

---

## What to Cut

- Infrastructure excuses ("the RSS feed only covers 5 days") — put in a footnote or skip it
- Sections with no signal ("Ethics: no lobbying activity flagged this period") — just don't include them
- Minor permits (reroofing, windows, decks) — one line summary at most
- Planning Commission items outside the district unless they set citywide precedent
- Anything that reads like a government report

---

## The Test

Read each section and ask: would this person text a friend about this? If not, it's either not important enough to include or not written sharply enough to be interesting. Cut it or rewrite it.
