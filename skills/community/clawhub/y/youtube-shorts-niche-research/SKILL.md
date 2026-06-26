---
name: youtube-shorts-research
description: Find viral YouTube Shorts channels that started recently and are doing really well. Use when Abdullah asks to find shorts niches, find channels, research YouTube Shorts, or find me channels. Runs the youtube-research.js script with criteria (≤60 days old, ≥15M total views) and returns qualifying channels with links. Uses a subagent (2.5-flash-lite) to process results.
---

# YouTube Shorts Channel Research Skill

Find viral new YouTube Shorts channels that meet strict criteria.

## Criteria (hardcoded in script)
- Channel age: ≤ 60 days old
- Total views: ≥ 15,000,000
- Average views per video: ≥ 100,000
- Results needed: whatever Abdullah specifies — default to 3 if no number given

## Script Location
`C:\Users\sarum\.openclaw\workspace\youtube-research.js`

## How to Run

1. Set `RESULTS_NEEDED` in the script to match the number Abdullah requested (default 3)
2. Always update this value before running
3. Run the script in background:
   ```
   cd C:\Users\sarum\.openclaw\workspace; node youtube-research.js
   ```
4. Poll until complete — the script runs until it finds all requested results, up to 10 rounds
5. If it exits with fewer than requested, run again immediately (different incognito session = different feed)
6. Keep running until you have the total requested.

## Processing Results (Token Optimization)
- **Mandatory**: When the script completes, **do not read the full JSON result file in the main session**.
- Use `sessions_spawn` with `model: "google/gemini-2.5-flash-lite"` and `runtime: "subagent"`.
- Task the subagent to read `youtube-research-YYYY-MM-DD.json`, filter for winners, and return a concise summary (handle, name, link, stats).
- Use the subagent's summary to respond in the main session.

## Output Format
When all requested channels are found, reply to Abdullah with:

```
Found your [N] channels! 🔥

1. **[Channel Name]** (@handle)
[URL]/shorts
[age]d old · [total views]M views · [avg views]K avg · [subs]K subs

2. **[Channel Name]** (@handle)
...
```

## Rules
- Always include the full YouTube link
- Always run in incognito (already configured in script)
- Never stop until the requested number of qualifying channels are found
- Do not report partial results — wait for the batch to complete then reply
- Each run uses a fresh incognito session so channels will differ
- Save results to `youtube-research-YYYY-MM-DD.json` (script does this automatically)

## Weekly Schedule
Every Wednesday, run this automatically and send results to Abdullah on Telegram unprompted.
Update HEARTBEAT.md to track last run date.
