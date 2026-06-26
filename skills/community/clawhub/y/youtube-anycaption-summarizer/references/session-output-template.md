# Session Output Template

After a video is fully processed, return a user-facing result block to the current OpenClaw session.

Use this format per video:

```text
Video
• <title>
• URL: [<url>](<url>)

Result
• video_id: <video_id>
• Summary language: <summary_language>
• Transcript source: <transcript_source>
• Status: postprocess_complete = <true|false>
• Language backfilled: <language-tag | not needed>
• end_to_end_total_seconds: <seconds>

Output paths
• Transcript:
<raw_transcript_path>
• Summary:
<summary_path>

Short summary
• <short summary bullet 1>
• <short summary bullet 2>
• <short summary bullet 3>
```

Rules:
- Return one block per video.
- In batch mode, concatenate the per-video blocks in processing order with a blank line between them.
- Keep `Short summary` concise and high-signal.
- Prefer the first bullet to be the executive-summary takeaway, then use the strongest key takeaways.
- If language backfill was unnecessary, write `not needed`.
- Use the final completion report values, not placeholder workflow values.
