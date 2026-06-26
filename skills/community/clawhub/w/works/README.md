# Works 🛠

> *Most of what you're working on lives in your head. Put it somewhere it can keep growing.*

**Works** is an open-source agent skill that turns your multi-session projects into a private, living record — kept on your machine, owned by you.

## Philosophy

A work is something you're _doing_. Not a question you're figuring out (that's [Digs](https://github.com/haah-ing/digs-skill)), not a person you're getting to know (that's [Peeps](https://github.com/haah-ing/peeps-skill)), not a place you've been (that's [Nooks](https://github.com/haah-ing/nooks-skill)). It's an effort that spans sessions and produces artifacts — a trip, a launch, a long piece of writing, a move, a build.

Without Works, multi-session efforts rot in daily memory. The launch you're planning gets mentioned on Monday, buried by Wednesday, and rediscovered three weeks later with half the details missing. Works gives each effort its own folder, its own log, and its own next steps — so nothing has to be reconstructed from scratch.

No project manager. No kanban board. Just files and your AI agent.

---

## What it does

- **Holds each effort in its own folder** — one `work.md` per project, plus drafts, assets, or anything else the project needs
- **Tracks status and next steps** — `active` / `paused` / `closed`, always with 1–5 concrete next steps
- **Logs progress** — dated entries of what actually happened, not every message
- **Links across your skills** — `Peeps:`, `Orgs:`, `Nooks:`, `Pages:`, `Vibes:`, `Digs:` in the frontmatter, maintained in both directions
- **Closes cleanly** — finished or dropped works move to `closed/` with an Outcome, preserved as the record of how the year was spent

```
mind/works/
  berlin-trip/
    work.md
    itinerary.md
  book-launch/
    work.md
    drafts/
      press-release.md
    assets/
      cover.png
  closed/
    kitchen-reno/
      work.md
```

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/works
curl -o ~/.claude/skills/works/SKILL.md https://raw.githubusercontent.com/haah-ing/works-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add haah-ing/works-skill
```

Works with OpenClaw, Cursor, Codex, OpenCode, GitHub Copilot, and any agent that supports the skills ecosystem.

### Hermes

```bash
hermes skills install works
```

---

## Then just talk about what you're working on

```
"I'm planning a Berlin trip with Alex in May."
"Booked the flights — logging that."
"What am I working on right now?"
"Move the kitchen reno to closed — we finished last week."
"That's for the book launch, right? Add it there."
"Priya's joining the Berlin trip."
```

Each work file looks like this:

```markdown
# Berlin trip with Alex

Status: active
Opened: 12 Apr 2026
Target: 3 May 2026
Tags: #travel #personal

Peeps: [[alex-chen]], [[priya-nair]]
Nooks: [[factory-berlin]]
Digs: [[why-berlin-feels-different]]

## Next

- Book flights by 20 Apr
- Ask Priya for Mitte recommendations
- Decide on apartment vs hotel

## Log

12 Apr 2026: Opened. Alex suggested overlapping with his conference 2–5 May.
14 Apr 2026: Priya sent three cafe picks — added to Nooks.
```

---

## Works best with

Works is part of a suite of personal intelligence skills:

- [**Peeps** 👥](https://github.com/haah-ing/peeps-skill) — your personal network. When someone joins a work, it's linked to their peep file in both directions.
- [**Digs** 🔭](https://github.com/haah-ing/digs-skill) — your active research threads. When a dig turns actionable ("I figured out what to do about X"), it hands off to a work.
- [**Nooks** 📍](https://github.com/haah-ing/nooks-skill) — your saved places. Destinations and meeting spots link into the work that happens there.
- [**Pages** 📖](https://github.com/haah-ing/pages-skill) — your reading life. Books informing the project land in `Pages:`.
- [**Vibes** 🎧](https://github.com/haah-ing/vibes-skill) — your cultural context. References that set the tone or inspire go in `Vibes:`.
- [**Haah** 🪩](https://github.com/haah-ing/haah-skill) — network dispatch. When a work needs external input, Haah can ask your trusted circles.

Install all six and your agent knows your people, your places, your reads, your culture, your open questions — and what you're actually doing.

---

## Contributing

The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Haah Inc*
