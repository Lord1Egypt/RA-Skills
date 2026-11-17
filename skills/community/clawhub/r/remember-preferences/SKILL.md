---
name: remember-preferences
description: A preference ledger that lets agents honor how each user likes things done — tone, tools, timing, and turn-offs. Use when an agent should personalize behavior instead of guessing. Requires a BlueColumn API key (bc_live_*).
---

# Remember Preferences — BlueColumn Skill

The difference between a useful agent and an annoying one is usually a preference: how long, how formal, how often, how loud. This skill records those rules so the agent stops guessing and starts matching.

## Record the preference

Store each preference as a clear rule with the user it belongs to.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "PREFERENCE (Joe): keep summaries under 5 bullets. No emojis in work emails. Prefers morning updates, not evening. Wants to be called out directly when wrong.", "title": "prefs - Joe communication"}'
```

## Apply before acting

Pull the relevant preference before any interaction that could go sideways.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "How does Joe like updates, emails, and feedback delivered?"}'
```

## Preference workflow

1. **Notice** — when a user corrects you or states a like/dislike, that is a preference.
2. **Capture** — store it immediately, phrased as a rule, with the user's name.
3. **Confirm** — for high-stakes preferences (privacy, tone), echo it back once.
4. **Apply** — recall before acting; when in doubt, follow the stored rule over the generic default.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Pref: never schedule meetings before 9:30am for Joe; he does deep work in the early morning.", "tags": ["preference", "schedule"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
