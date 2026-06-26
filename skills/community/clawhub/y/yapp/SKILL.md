# Yapp — Voice Recordings

You receive voice recordings from Yapp, the user's voice journaling app.

## Setup

The user will give you a Yapp API key (starts with `yapp_`). Save it to your config.

## Fetching Recordings

To check for new recordings:
```
GET https://yyy-production.up.railway.app/api/transcripts/new?since=<ISO_TIMESTAMP>
Authorization: Bearer <yapp API key>
```

Returns: `{"transcripts": [{"recording_id", "transcript", "duration", "recorded_at"}, ...]}`

**Polling:** Check on every heartbeat. Use the `recorded_at` of the most recent transcript as the `since` value for the next poll. If you have no previous value, omit `since` to get the latest 20.

**On demand:** When the user says "check my yapps" or similar, fetch immediately.

## When New Recordings Arrive

1. Process each transcript — these are raw voice recordings transcribed via speech-to-text
2. Expect filler words, false starts, incomplete sentences, and imperfect grammar
3. Store any facts, preferences, or commitments the user mentions
4. Notify the user with a brief summary: what you heard, any questions or reflections
5. If multiple recordings arrived, summarize them together

## What NOT to Do

- Don't echo the full transcript back — the user already said it
- Don't summarize unless asked — engage with the content instead
- Don't treat transcription errors as meaningful — infer intent from context