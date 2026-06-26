# Vibes 🎧

> *The albums, shows, podcasts, and channels that shaped how you think. Your agent should know them too.*

**Vibes** is an open-source agent skill that turns your cultural life into a private, searchable intelligence layer — kept on your machine, owned by you.

No Spotify. No Letterboxd. No algorithm. Just files and your AI agent.

---

## What it does

- **Tracks culture** — one markdown file per album, podcast series, show, film, or YouTube channel
- **Captures taste** — ratings, tags, and notes in your own words
- **Surfaces context** — "what have I watched about power dynamics?" finds the right reference
- **Builds a taste profile** — patterns in what you rate highly, surfaced when relevant
- **Finds shared ground** — noting when you and someone you know love the same thing

```
vibes/
  albums/
    radiohead-ok-computer.md
  podcasts/
    lex-fridman-podcast.md
  shows/
    succession.md
  films/
    parasite.md
  youtube/
    3blue1brown.md
```

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/vibes
curl -o ~/.claude/skills/vibes/SKILL.md https://raw.githubusercontent.com/haah-ing/vibes-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add haah-ing/vibes-skill
```

Works with OpenClaw, Cursor, and any agent that supports the skills ecosystem.

### Hermes

```bash
hermes skills install vibes
```

---

## Then just talk

```
"Just finished Succession — 5 stars, sharpest thing I've seen on power and dysfunction."
"I've been watching a lot of 3Blue1Brown lately."
"What have I logged that's about leadership or management?"
"Marco and I both love this show — note that."
"Something smart to listen to on a long flight?"
```

Each file looks like this:

```markdown
# Succession

- **Type:** show
- **Creator:** Jesse Armstrong
- **Year:** 2018–2023
- **Status:** finished
- **Finished:** 12 Jan 2026
- **Rating:** 5/5
- **Tags:** #drama #power #family #darkcomedy
- **Shared with:** [[marco-tabini]]

## Notes

12 Jan 2026: sharpest thing I've seen on how power corrupts family — and vice versa
```

YouTube channels get a `Channel:` URL field and a `## Must Watch` section for specific videos worth recommending.

---

## Works best with

Vibes is part of a suite of personal intelligence skills:

- [**Haah** 🪩](https://github.com/haah-ing/haah-skill) — dispatch to your trusted circles. When you want a recommendation in a mood or genre, Haah asks your network what they've been into.
- [**Peeps** 👥](https://github.com/haah-ing/peeps-skill) — your personal network. When you and a contact share taste, Vibes links it to their Peeps file. Your agent can surface it as a conversation opener or intro point.
- [**Pages** 📖](https://github.com/haah-ing/pages-skill) — books and reading. The cultural sibling to Vibes — some ideas start as a book and finish as a film.
- [**Nooks** 📍](https://github.com/haah-ing/nooks-skill) — your saved places. Some places have a sound; your agent knows both.
- [**Digs** 🔭](https://github.com/haah-ing/digs-skill) — your active research threads. A documentary or podcast can feed directly into an open dig as a finding.

Install all six and your agent knows your people, your places, your reads, your culture, and your open questions.

---

## Contributing

The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Haah Inc*
