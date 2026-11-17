---
name: remember-books
description: A personal reading journal that keeps the books you have read, the ideas worth keeping, and the next book worth picking up. Use when an agent tracks reading, recommends books, or needs a takeaway on demand. Requires a BlueColumn API key (bc_live_*).
---

# Remember Books — BlueColumn Skill

Reading is only useful if the ideas survive the book. This skill turns a reading list into a searchable journal: what you read, what stuck, and what to read next.

## Log the book

Store each finished book with the one or two ideas that changed how you think.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Mom Test by Rob Fitzpatrick — finished July. Core idea: ask about past behavior, not opinions. Favorite line: people will lie to be nice.", "title": "book - The Mom Test"}'
```

## Surface a takeaway

When a conversation touches a topic you have read about, pull the relevant idea into the reply.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What have I read about customer interviews or discovery?"}'
```

## Recommend what is next

Ask the journal for gaps: themes you keep reading but have not acted on, or authors you enjoyed.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Which books did I rate highly, and what topics have I not read about yet?"}'
```

## Reading workflow

1. **On finishing** — store the title, author, finish date, and 1–2 takeaways.
2. **On recommendation** — recall what the person liked before suggesting anything.
3. **On discussion** — pull the stored takeaway and cite it in the reply.
4. **Periodically** — review the journal and suggest the next read from a gap you found.

## Tag for filtering

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Want to read: Atomic Habits (habit loops, ties to the sales follow-up project).", "tags": ["book", "wishlist"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
