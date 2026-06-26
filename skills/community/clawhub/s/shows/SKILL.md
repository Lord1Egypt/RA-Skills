---
name: Shows
description: Track movies and series with progress, watchlist, ratings, and proactive alerts for new releases and platform changes.
---

## Core Behavior

- User mentions watching something → log it with current progress
- User finishes something → mark complete, ask for rating
- User asks "what was I watching?" → surface in-progress items
- User asks "what should I watch?" → suggest from watchlist based on mood/time

---

## Workspace

Store show data in `~/shows/`:
```
~/shows/
├── watching.md       # Currently in progress
├── watchlist.md      # Want to watch
├── completed.md      # Finished items with ratings
├── abandoned.md      # Dropped shows
└── people.md         # Family members if tracking multiple viewers
```

---

## Item Structure

| Field | Format |
|-------|--------|
| Title | Name (Year) |
| Type | movie / series |
| Status | watching / watchlist / completed / abandoned / waiting |
| Progress | S02E05 or "45 min in" for paused movies |
| Platform | Netflix, HBO, Disney+, etc. |
| Rating | 1-5 or 👍👎 |
| Recommended by | Who suggested it |
| Notes | "Left off at the wedding scene" |

For series, also track: total seasons, next release date if waiting.

---

## Quick Commands

| User Says | Agent Does |
|-----------|------------|
| "Watching Severance" | Add to watching, ask current episode |
| "Finished The Bear S3" | Move to completed, ask rating |
| "Add Ripley to watchlist" | Add with date, platform if known |
| "Where am I in Shogun?" | Check progress, report last watched date |
| "What's on my list?" | Summarize watchlist by priority |
| "Dropping Squid Game" | Move to abandoned with note |

---

## Proactive Features

| Trigger | Alert |
|---------|-------|
| New season announced | "Show X you watched got renewed" |
| Show stale >30 days | "Haven't touched X in a while—still interested?" |
| Platform leaving soon | "X leaves Netflix in 5 days, it's on your watchlist" |
| User asks "what to watch" | Suggest based on available time and mood |

---

## Load Reference

| Situation | File |
|-----------|------|
| Family viewing, multi-user tracking | `family.md` |
| Finding where to watch, platform tips | `platforms.md` |
| Discovery and recommendations | `discovery.md` |
