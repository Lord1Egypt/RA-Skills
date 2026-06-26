---
name: works
description: Personal project intelligence — keep each multi-session effort in its own folder with status, next steps, and wiki links to the people, places, and things it touches. Use when starting or updating ongoing work, logging progress, or asking "what am I working on?"
metadata:
  openclaw:
    emoji: "🛠"
    os: ["linux", "darwin", "win32"]
  hermes:
    tags: ["projects", "planning", "execution"]
---

# 🛠 Works — active project intelligence

**When to use this skill:** The human starts multi-session work that will have artifacts — planning a trip, shipping a launch, writing a long piece, executing a move, building something. Don't ask if it should be a work; if it crosses sessions and produces files, open one.

**You must:**

- Keep **one folder per project** under `mind/works/<slug>/`. Every folder has a `work.md` using the schema in **Work File**, plus whatever drafts/assets/notes the project needs.
- Log **dated progress** in `## Log` inside `work.md`. Keep `## Next` current — **1 to 5 concrete next steps**.
- Maintain **wiki links** in both directions between this work and any peeps, orgs, nooks, vibes, pages, or digs it touches.
- **Search `mind/works/`** before opening a new work — if a related one exists, extend it or hand off via `Connected:` instead of duplicating.
- Close properly: add `Closed` and `Outcome` to the top, then **move the folder** to `mind/works/closed/` (don't delete).

**Do not:** See **What NOT to Suggest** — e.g. don't turn works into a todo manager, don't open works for one-off questions (those are digs), don't let spanning work rot in daily memory.

---

## Data

**Base path** is workspace root or document root folder. On first use, create it: `mkdir -p mind/works/`. Works uses a `mind/works/` folder in your workspace.

One folder per project. Every folder has a `work.md`; additional files are up to the project.

```
mind/
└── works/
    ├── worksconfig.yml
    ├── berlin-trip/
    │   ├── work.md
    │   └── itinerary.md
    ├── book-launch/
    │   ├── work.md
    │   ├── drafts/
    │   │   └── press-release.md
    │   └── assets/
    │       └── cover.png
    └── closed/
        └── kitchen-reno/
            └── work.md
```

**Slugs:** short kebab-case, named like a project not a category — `berlin-trip/`, not `planning-a-trip/`. A good slug reads as the project's handle.

### Dataset Config

`worksconfig.yml` lives inside `mind/works/`. Read it at the start of any session involving this skill.

```yaml
images: no # by default no; ask the human. Warn it is token-expensive.
```

---

## Work File

```markdown
# Berlin trip with Alex

Status: active
Opened: 12 Apr 2026
Target: 3 May 2026
Tags: #travel #personal
Image: optional cover in `../assets/berlin-trip.png`

Peeps: [[alex-chen]], [[priya-nair]]
Orgs: [[gestalten]]
Nooks: [[factory-berlin]], [[house-of-small-wonder]]
Pages: [[the-perfect-store]]
Vibes: [[wim-wenders]]
Digs: [[why-berlin-feels-different]]
Connected: [[book-launch]]

## Next

- Book flights by 20 Apr
- Ask Priya for Mitte recommendations
- Decide on apartment vs hotel
- Pack the drill
- Get the visa

## Log

12 Apr 2026: Opened. Alex suggested overlapping with his conference 2–5 May. Budget ~€2k each.
14 Apr 2026: Priya sent three cafe picks — added to Nooks. Leaning toward an AirBnB in Mitte.
```

**Field guidance:**

Status: `active` (working on it now), `paused` (on hold, might resume), `closed` (finished or dropped). Default: `active`.
Opened: the date the work began.
Target: optional deadline or milestone. Omit if none.
Tags: 2–4 short, searchable, personal — `#travel`, `#launch`, `#home`, `#writing`, `#career`.
Peeps/Orgs/Nooks/Pages/Vibes/Digs: wiki links into the other skills. Maintain both directions — if a work names a peep, a note on their peep file helps surface it later.
Connected: other works this one depends on, parallels, or hands off to.
Next: **1 to 5** concrete next steps. Finish or drop each before adding new ones. This is not a backlog.
Log: dated entries of substance — decisions made, things booked, blockers, drafts landing. Not a dump of every message.

---

## Opening a Work

When the human starts multi-session work that will have artifacts, open it. Don't ask permission — just do it and confirm briefly.

1. **Name it as a project, not a category.** "Berlin trip with Alex", not "travel".
2. **Search first.** Grep `mind/works/` for related slugs before creating — extend if something close exists.
3. **Bootstrap the links.** What peeps, orgs, nooks, pages, vibes, or digs already touch this? Pre-populate the frontmatter.
4. **Write one `Next`.** One concrete step the human can take. Don't pad to five if only one is obvious.
5. **Seed the Log.** What prompted this work? One sentence.

Brief confirmation: "Opened — _Berlin trip with Alex_. Linked Alex, Priya, and the _why-berlin-feels-different_ dig. First step: book flights by 20 Apr."

---

## Logging Progress

When the human mentions progress on an open work — a decision, a booking, a draft landing, a blocker — act automatically:

- Append a dated entry to `## Log`.
- Update `## Next`: cross out `~~finished~~` steps, add what's actually next. Keep the count ≤ 5.
- Route sub-artifacts into the folder — drafts to `drafts/`, files they sent to `assets/`, longer notes as sibling `.md` files.
- Update cross-links: if a new peep enters the work, add them to `Peeps:` and drop a line in their Peeps file.

Don't wait to be asked. If they say "booked the Berlin flight" and a `berlin-trip` work is open, log it.

---

## Closing a Work

When the human signals done — "we finished", "shipped it", "dropped that" — draft the outcome and confirm before moving the folder.

Add to the top of `work.md`:

```markdown
Closed: 5 May 2026
Outcome: Trip done. Standout: Museum Island. Next time: less Mitte, more Neukölln.
```

Then move the whole folder to `mind/works/closed/<slug>/`. Don't delete — closed works are the record of how the year was spent.

---

## Finding Works

```bash
# Works on a topic
grep -ril "travel\|trip\|berlin" mind/works/

# Active works
grep -rl "Status: active" mind/works/*/work.md

# Paused works worth restarting
grep -rl "Status: paused" mind/works/*/work.md

# Works involving a peep
grep -rl "\[\[alex-chen\]\]" mind/works/

# Works with a near target date
grep -rl "Target: .*Apr 2026\|Target: .*May 2026" mind/works/
```

Always read the full `work.md` after grepping — the matched line is a signal, not the whole picture.

---

## Core Behavior

- Human mentions a multi-session effort → check for existing work, open one
- Human reports progress → append to `## Log`, update `## Next`
- Human shares a draft/file → save to the work's folder
- Human mentions a peep/nook/book/etc. that touches an open work → update the wiki links both ways
- Human asks "what am I working on?" → list active works with their last log date and current next step
- Conversation drifts to an open work's topic → surface it: "That's on your _book-launch_ work — last step was drafting the press release."

## Integration with other skills

- **Peeps:** when a person joins a work, link them under `Peeps:` and drop a dated note on their peep file ("Working with them on _berlin-trip_, Apr 2026"). If a work opens around a person, make that peep the first link.
- **Orgs:** if work happens with or inside an org, link under `Orgs:` and optionally note it in the org file.
- **Nooks:** places the work happens — meeting spots, destinations — go under `Nooks:`.
- **Pages:** books informing the work (`Peopleware` for a team project, say) go under `Pages:`.
- **Vibes:** cultural references setting the tone or inspiration go under `Vibes:`.
- **Digs:** when a dig turns actionable — "I figured out what to do about X" — open a work and link back: the dig's `Connected:` gets the work slug, the work's `Digs:` gets the dig slug.
- **Haah:** if the work needs external input the network can help with, offer to dispatch a query.

---

## Updating

To update this skill to the latest version, fetch the new SKILL.md from GitHub and replace this file:

```
https://raw.githubusercontent.com/haah-ing/works-skill/main/SKILL.md
```

---

## What NOT to Suggest

- Turning Works into a todo manager — `## Next` is 1–5 steps, not a backlog. Loose todos live in daily memory.
- Opening a work for a one-off question — that's a dig, not a work.
- Letting active work rot in daily memory — if it spans days and has artifacts, it belongs in Works.
- Merging related works into one mega-folder — use `Connected:` links instead.
- Keeping closed works in `mind/works/` — move them to `closed/` so the active list stays clean.
