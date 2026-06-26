---

name: vibes
description: Cultural intelligence — track albums, podcasts, shows, films, and YouTube channels that shaped how you think. One markdown file per item in vibes/. Use when logging new culture, finding past favorites, or asking "what have I watched/listened to about X?"
metadata:
  openclaw:
    emoji: "🎧"
    os: ["linux", "darwin", "win32"]
  hermes:
tags: ["culture", "music", "podcasts", "shows", "films", "youtube"]

---

# 🎧 Vibes — cultural intelligence

## Data

**Base path** is workspace root or document root folder. On first use, create it: `mkdir -p mind/vibes/`. Vibes uses a `mind/vibes/` folder in your workspace.

Files live in `mind/vibes/`. Organised by type:

```
./mind/
└── vibes/
    ├── albums/        ← music albums, EPs, mixtapes
    ├── podcasts/      ← ongoing shows and limited series podcasts
    ├── shows/         ← TV series, limited series, docuseries
    ├── films/         ← movies, documentaries, short films
    └── youtube/       ← channels and creators worth following
```

File names: lowercase slugs. `radiohead-ok-computer.md`, `lex-fridman-podcast.md`, `succession.md`, `parasite.md`, `3blue1brown.md`.

### Dataset Config

`vibesconfig.yml` lives inside the `mind/vibes/` directory. Read it at the start of any session involving this skill.

```yaml
images: no (by default no, ask if you human want to feach images for pepople, warn that it is token expensive)
```

---

## Vibe File

### Albums, podcasts, shows, films

```markdown
# Title

Type: album / podcast / show / film
Creator: artist, host, director, or studio
Year: 2024
Status: listening / watching / finished / paused / want (see per-type guidance below)
Finished: 14 Jan 2026 (omit for albums; omit if ongoing or unfinished)
Rating: 4/5 (omit until finished; for albums, rate anytime)
Image: optional image located at `../assets/slug-for-image`
Tags: #jazz #introspective #slow #90s #documentary #tech #comedy
Shared with: [[marco-tabini]] (Peeps slug — omit if unknown)

## Notes

14 Jan 2026: what you took from it, what surprised you, what lingers
```

### YouTube channels

```markdown
# Channel Name

Type: youtube
Creator: person or team behind it
Channel: https://youtube.com/@channelslug
Status: following / archived / want
Tags: #math #animation #explainers #tech #essays
Shared with: [[person-slug]] (omit if unknown)

## Notes

14 Jan 2026: what makes this channel worth following, what you keep coming back for

## Must Watch

- [Video Title](https://youtu.be/...) — one sentence on why it's worth an hour of anyone's time
```

**Field guidance — YouTube:**

Status: `following`: actively watching new uploads. `archived`: used to follow, no longer active, but shaped how you think. `want`: want to check out.
Must Watch: the specific videos worth recommending. Keep it short. If every video is on this list, the list means nothing.
Channel: the channel URL, not a specific video. For one-off videos that don't belong to a channel you follow, log them under the most relevant channel or create a minimal file just for that creator.

**Field guidance — all types:**

Type: pick one. When in doubt, go with how you primarily consume it.
Creator: for albums: artist name. For podcasts: host name. For shows/films: showrunner or director. For YouTube: person or team name.
Status: what's your current relationship with it?
- **Albums**: `listening` (in rotation) / `shelved` (heard it, not active right now) / `want` (want to check out). Music is continuous — you don't "finish" an album, you shelve it or keep listening.
- **Podcasts**: `listening` / `shelved` / `want`. Same as albums — ongoing by nature.
- **Shows**: `watching` / `finished` / `paused` / `want`.
- **Films**: `watching` / `finished` / `want`.
- **YouTube**: `following` / `archived` / `want`.
Tags: personal tags, not genre labels. `#slow` means slow-paced. `#founders` means it's about founders. Tags that mean something to *you* are more useful than accurate genre taxonomy.
Shared with: if Peeps is installed, use `[[their-slug]]`; otherwise note the person's name as plain text. Builds taste connections when Peeps is present.
Notes: what made it worth logging. Not a review. What shifted, what surprised, what you'd bring up in a conversation.

**A vibe is worth logging if** you'd mention it to someone, if it changed how you think, or if you'd want to find it again. Not everything needs to be here.

---

## Saving a Vibe

1. Check if already saved.
2. Pre-fill what you know (type, creator, year or channel URL for YouTube).
3. **Ask as a group** (skip what's already clear):
  - Status — listening/shelved/watching/finished/following, or want? (use type-appropriate options)
  - Rating? (for albums: anytime; for shows/films: after finishing)
  - Tags — what's this about, in your words?
  - Any notes or must-watch videos worth capturing now?
4. If `images: yes` in `mind/vibes/vibesconfig.yml` search for the conver image and add it to **Image** field. 

Show a brief confirmation: "Saved — *Succession*, show by Jesse Armstrong (2018–2023), finished. Tagged #drama #power #darkcomedy." Or: "Saved — 3Blue1Brown in `./mind/vibes/youtube/`, following. Tagged #math #animation #explainers."

---

## Core Behavior

- User mentions a show/album/podcast/film/YouTube channel → check if saved, offer to create or update
- User asks "what have I watched/listened to about X?" → search `./mind/vibes/` with expanded keywords
- User finishes a show/film or stops following a channel → ask for a rating and a note
- User shelves an album or podcast → ask if they want to add a note or rating
- Conversation touches a theme → surface relevant vibes without being asked
- User mentions someone having similar taste → note `Shared with:` and link to Peeps if installed
- User shares a specific video worth saving → add to the creator's Must Watch list (create the channel file if needed)

**Examples:**

- "Just finished watching Succession" → check if saved, offer to rate and note
- "I'm thinking about power dynamics in companies" → "You rated *Succession* 5/5 and tagged it #power — your note says it's the sharpest thing you've seen on how institutions corrupt"
- "Marco and I were both talking about the same Lex Fridman episode" → update `Shared with:` on that podcast file; if Peeps is installed, offer to note it on Marco's Peeps file
- "I've been watching a lot of 3Blue1Brown lately" → check `./mind/vibes/youtube/`, offer to save with tags and a must-watch note

---

## Finding Vibes

Use `grep` with expanded terms. Search type folders or all of `./mind/vibes/`.

```bash
# All jazz and soul albums
grep -ril "jazz\|blues\|soul\|r.b\|motown" ./mind/vibes/albums/

# Finished shows with high rating
grep -rl "Rating: 5\|Rating: 4" ./mind/vibes/shows/

# Podcasts about tech and startups
grep -ril "tech\|ai\|startup\|founders\|venture" ./mind/vibes/podcasts/

# YouTube channels you follow
grep -rl "Status:.*following" ./mind/vibes/youtube/

# YouTube channels with must-watch videos
grep -rl "## Must Watch" ./mind/vibes/youtube/

# Vibes shared with specific person
grep -rl "\[\[marco" ./mind/vibes/

# Want list across all types
grep -rl "Status:.*want" ./mind/vibes/

# All films you've logged
ls ./mind/vibes/films/
```

**Keyword expansion examples:**

- "sad / melancholy" → `sad\|melancholy\|grief\|slow\|introspective\|quiet`
- "upbeat / energetic" → `upbeat\|energetic\|hype\|dance\|workout\|intense`
- "smart / cerebral" → `cerebral\|dense\|intellectual\|complex\|layered`
- "funny / comedy" → `comedy\|funny\|satire\|wit\|absurd\|dark.comedy`

Always read the full file after grepping.

---

## Taste Profile

Over time, your vibes folder becomes a taste fingerprint. Patterns emerge in what you rate highest, what you keep returning to, what themes recur. Surface this when relevant:

- "You've given 5 stars to 8 albums — 6 of them are tagged #introspective"
- "Your most-watched genre is character-driven drama"
- "You've logged 14 tech podcasts this year — you clearly find this format useful"

Don't generate a dashboard. Surface the pattern when it's useful to the conversation.

---

## Heartbeat or cron

Check a random vibe file. Surface something worth mentioning:

- "You started *Severance* in January — still watching, or did it lose you?"
- "You haven't logged any new albums this month — anything good lately?"
- "You and Priya both tagged #succession — do you know you share that?"
- "3Blue1Brown is in your `./mind/vibes/youtube/` folder but has no Must Watch list — anything from there worth saving?"

If nothing worth mentioning, skip.

---

## Adding to HEARTBEAT.md or cron

If it is not there yet, ask your human if they want to add **Vibes: check** to HEARTBEAT.md. If there is no HEARTBEAT.md, suggest to create a cron every 30 minutes during waking hours (`*/30 7-22 * * *`) to execute **Vibes: check**.

---

## Integration with Peeps

If Peeps is installed, culture and people can be connected:

- Add `Shared with: [[their-slug]]` to the vibe file
- Optionally note in their Peeps file: "Both love *Show / Artist* — good conversation territory"
- Surface shared tastes when relevant: "You and Marco both rate Radiohead highly — you've never talked about it."

When meeting someone new:

- Note their recommendations in `./mind/vibes/`, using `Recommended by: [[their-slug]]` if Peeps is installed, otherwise their name as plain text
- Over time, their recommendations form a taste profile you can reference

---

## Integration with Haah

If Haah is installed, dispatch to your circles when you want recommendations in a mood or genre:

- "Haah: anyone in my circles have a podcast recommendation for long walks?"

When someone in your circle asks for recommendations:

- Check Vibes for highly-rated relevant items before answering
- Draft a reply with your actual experience, rating, and one honest sentence about it. Don't recommend things you haven't tried.

---

## Updating

To update this skill to the latest version, fetch the new SKILL.md from GitHub and replace this file:

```
https://raw.githubusercontent.com/haah-ing/vibes-skill/main/SKILL.md
```

---

## What NOT to Suggest

- Syncing with Spotify, Netflix, Apple Music, or YouTube — different purpose, these are algorithmic feeds
- Automated tracking via API integrations — complexity, privacy, not local-first
- Logging every episode or every song — this is for the things worth remembering
- Star ratings for things you haven't finished — rate on completion (albums are the exception: rate anytime)
- Genre taxonomies from Discogs or TMDB — use personal tags that mean something to you
