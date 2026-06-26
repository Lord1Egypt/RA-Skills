# Example — Triage and reply to inbox conversations

> **User:** "Any new DMs? If anyone is asking about pricing, send them my saved 'pricing reply'."

**Agent's reasoning:**
1. Fetch open conversations via `inbox:list-conversations`.
2. For each, fetch recent messages via `inbox:get-messages` and check for keywords ("price", "pricing", "cost", "how much").
3. Find the saved reply named "pricing reply" via `inbox:list-saved-replies`.
4. Reply with the saved reply's content. Otherwise summarize the rest for the user.

**Agent execution:**

```bash
# 1. List open inbox threads
so-me inbox:list-conversations --status open

# 2. For each, peek at the latest 5 messages
so-me inbox:get-messages <conversationId> --limit 5

# 3. Find the saved reply
so-me inbox:list-saved-replies | jq '.data[] | select(.title=="pricing reply")'

# 4. Reply
so-me inbox:reply <conversationId> --message "<saved-reply-content>"
```

**Reply to user:**

> 4 open conversations:
> - **@designer_jen** (Twitter): asked about pricing → replied with your saved "pricing reply" template ✓
> - **@hello_eric** (Instagram): collaboration request → flagged for your review
> - **+1-555-...** (WhatsApp): order status question → flagged
> - **@maria_b** (LinkedIn): said "thanks!" → no reply needed
>
> Want me to draft replies to the two flagged ones?

## Notes for the agent

- Saved replies live under `inbox:list-saved-replies` / `inbox:get-saved-reply`.
- Match keywords case-insensitively. Don't rely on exact title matches — let the user disambiguate if multiple saved replies could fit.
- WhatsApp has stricter rules: only **template messages** outside the 24-hour customer service window. Use `whatsapp:list-templates` and `whatsapp:send-template` for proactive outreach.
