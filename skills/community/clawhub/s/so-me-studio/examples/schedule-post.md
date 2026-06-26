# Example — Schedule a cross-platform post with an AI caption

> **User:** "Write something about our Friday product launch and schedule it to Twitter and LinkedIn for 5pm tomorrow."

**Agent's reasoning:**
1. The user wants two posts (Twitter + LinkedIn), each with a tailored caption.
2. "Tomorrow at 5pm" → compute ISO 8601 in UTC. Confirm with the user once before scheduling.
3. Use `ai:generate-and-schedule` for each platform — it handles caption + scheduling in one call.

**Agent execution:**

```bash
# 1. Confirm the time with the user
# (If today is 2026-04-25 and the user is in UTC-5: 2026-04-26 22:00 UTC)

# 2. Twitter post
so-me ai:generate-and-schedule \
  --prompt "Friday product launch announcement, casual tone, hashtags" \
  --platform TWITTER \
  --scheduled-at 2026-04-26T22:00:00Z

# 3. LinkedIn post (longer-form, professional tone)
so-me ai:generate-and-schedule \
  --prompt "Friday product launch announcement, professional tone, no hashtags" \
  --platform LINKEDIN \
  --scheduled-at 2026-04-26T22:00:00Z
```

**Sample response (parsed):**

```json
{
  "id": "p_01H...",
  "socialMedia": "TWITTER",
  "postStatus": "SCHEDULED",
  "scheduledAt": "2026-04-26T22:00:00.000Z",
  "text": "🚀 Tomorrow's the day. Our biggest launch yet drops at 5pm. #productlaunch"
}
```

**Reply to user:**

> Scheduled two posts for tomorrow at 5pm UTC:
> - **Twitter** (`p_01H...`): "🚀 Tomorrow's the day..."
> - **LinkedIn** (`p_02J...`): "We're excited to announce..."
>
> Both are visible in your calendar at app.so-me.studio. Want to tweak either before they go out?
