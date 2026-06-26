---
name: book-tracker
description: Tracks reading — books in progress, notes on what mattered, themes across what you've read, and what to read next. Use when a user wants to remember what they've read and build on it rather than letting books disappear after finishing.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📖"
  openclaw.user-invocable: "true"
  openclaw.category: intelligence
  openclaw.tags: "books,reading,notes,knowledge,library,recommendations,reading-list,non-fiction,fiction"
  openclaw.triggers: "track this book,I'm reading,add to reading list,what should I read next,book recommendation,reading notes,I just finished,book tracker,what have I read,reading list"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/book-tracker


# Book Tracker

Most books disappear after you finish them.
Two weeks later, you can't remember the main argument.
Two months later, you can't remember why you read it.

This skill changes that. Notes on what mattered, themes across what you've read,
and a reading list that actually reflects what you want to read next.

---

## File structure

```
book-tracker/
  SKILL.md
  library.md         ← every book with status, notes, rating
  reading-list.md    ← want to read, with reasons
  config.md          ← genres, preferences, monthly goal
```

---

## What it tracks

**In progress:** What you're currently reading, where you are, any notes mid-read.

**Finished:** Rating, key ideas, best quotes, what changed your thinking.

**Abandoned:** Books you gave up on and why — this data is useful too.

**Want to read:** Recommendations with context (who recommended it, why it matters to you).

---

## Adding books

**Start reading:** `/book start [title] [author]`
**Finish reading:** `/book done [title]` — triggers a brief reflection prompt
**Add to list:** `/book want [title]` — adds with optional reason
**Log a note mid-read:** `/book note [title] [note]`
**Abandoned:** `/book drop [title] [why]`

---

## Post-reading reflection

When you mark a book as done, the agent asks 4 questions:

1. What's the one idea from this book you'll actually use or remember?
2. What surprised you?
3. Who would you recommend this to and why?
4. Rating: 1-5

Short answers are fine. One sentence each is enough.
These become the book's entry in library.md.

---

## library.md structure

```md
## [TITLE] — [AUTHOR]
Status: read / reading / abandoned / want
Finished: [date]
Rating: [1-5]
Genre: [fiction / non-fiction / biography / etc]

The one idea: [their answer from reflection]
Surprised by: [their answer]
Recommend to: [their answer]

Notes:
[Any mid-read or post-read notes]

Quotes:
[Any passages worth keeping]

Related to: [other books in library that connect]
```

---

## Reading list intelligence

`/book next` — suggests what to read next based on:
- What you've enjoyed most (by rating and genre)
- Themes you've been exploring lately
- Books you've had on the list longest
- Any books that connect to what you're working on or thinking about

Not just a ranked list. A recommendation with a reason:

```
📖 What to read next

1. **The Mom Test** — Rob Fitzpatrick
   Why now: You've been reading about product and customer research.
   This is the most practical book on the list for your current work.
   On your list since: 4 months ago (added when [NAME] mentioned it)

2. **Piranesi** — Susanna Clarke
   Why now: You've been on a heavy non-fiction run for 3 months.
   Your ratings suggest you like breaks with literary fiction.
   Short. Unusual. Won't take long.
```

---

## Theme tracking

After 10+ books, patterns become visible.

`/book themes` — what have you been reading about?

```
📖 Reading themes — last 12 months

Most frequent topics:
1. Product and strategy (8 books)
2. Management and leadership (5 books)
3. Literary fiction (4 books)
4. History (3 books)

Gaps you might notice:
• You haven't read much science or technology in 18 months
• Your fiction-to-non-fiction ratio is 1:4 (heavy non-fiction run)

Your highest-rated books tend to be: [genre/topic pattern]
```

---

## Book and knowledge-capture integration

When you log a quote or key idea from a book:
`/book note [title] "this is worth keeping"`

The skill offers to add it to knowledge-capture:
"Add this to your knowledge base? It'll be searchable there alongside your other notes."

The two skills build on each other. Books feed the knowledge base.
The knowledge base surfaces relevant reading notes when you're thinking about a topic.

---

## Reading goal

Optional. Set a books-per-month target if you want one.

`/book goal [N] per month`

At the end of each month, a brief note:
"Read 2 books in March, goal was 3. On track for the year (8 of 10)."
Not a guilt trip. Just a number.

---


## Privacy rules

Reading history is personal and low-stakes, but still private.

**Context boundary:** Only surface reading lists and notes in the owner's private channel.
Never share what someone is reading or their book notes in a group context.

**Approval gate:** No book is added to or removed from the library without
the owner's instruction — either explicit command or confirmation of a suggestion.

---

## Management commands

- `/book start [title] [author]` — start reading
- `/book done [title]` — mark finished, trigger reflection
- `/book drop [title]` — mark abandoned
- `/book want [title]` — add to reading list
- `/book note [title] [note]` — log a note
- `/book next` — get a recommendation
- `/book list` — show reading list
- `/book library` — show all books
- `/book themes` — reading pattern analysis
- `/book search [query]` — search your library
- `/book [title]` — show entry for one book
