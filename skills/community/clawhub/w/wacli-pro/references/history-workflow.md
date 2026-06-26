# History workflow

Use this when the user wants a reply, follow-up, or context-aware outreach.

## Goal

Recover enough recent context to draft a message that fits the conversation thread.

## Minimal workflow

1. Find the chat.
2. Inspect recent history.
3. Backfill only if the recent history is missing important context.
4. Draft the reply.
5. Confirm before sending.

## Commands

```bash
wacli chats list --limit 20 --query "name or number" --json
wacli messages search "keyword" --limit 20 --chat <jid> --json
wacli history backfill --chat <jid> --requests 2 --count 50
```

## What to extract

Look for:
- the last unanswered question
- any promised follow-up
- names, dates, prices, files, and deadlines
- the other person’s tone
- whether the thread is casual, professional, or tense

## Drafting from history

After reading the thread:
- continue the same level of formality unless the user asks to change it
- answer the unresolved point first
- avoid re-explaining facts already obvious in the chat
- mention prior context only when it helps the recipient orient quickly

## When to backfill more

Backfill more history if:
- the thread references older events
- the user says `as discussed`, `again`, `follow up`, or `remind them`
- there are attachments or payment references not visible in the recent results

## When to stop

Do not keep scraping history once the draft is already grounded enough to send safely. Aim for sufficient context, not exhaustive reconstruction.
