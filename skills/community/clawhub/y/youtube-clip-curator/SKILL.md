# YouTube Clip Curator

Analyze a long-form YouTube video (e.g. VTuber stream, podcast, lecture) and extract a ranked list of "clip candidates" with start/end timestamps, hook descriptions, click-worthy titles, and emotion tags. Optionally generate FCPXML for Premiere Pro / DaVinci Resolve, plus thumbnail briefs ready for an image AI.

## When to use

Use this skill when the user needs to:
- Turn a 1-3 hour stream into 5-10 short YouTube clip candidates
- Reverse-engineer the editing thinking of a target clip channel
- Get start/end seconds + title + hook for each clip — ready to cut
- Emotion-tag each clip for thumbnail and promotion strategy
- Bridge from raw long video to a Premiere Pro / DaVinci Resolve timeline
- Suggest the most click-worthy moments without reviewing the full video

## How it works

1. Ask for the source video (YouTube URL, MP4 path, or transcript)
2. Optionally ask for a "style template" channel (e.g. ちばちゃんねる) to mimic editing thinking
3. Ask for the target clip count (default: 5) and duration target (short / medium / long)
4. Analyze the transcript to find hooks, punchlines, emotion peaks, character moments
5. Score each candidate by:
   - Emotion intensity (laughter, surprise, chaos, cuteness)
   - Clear punchline / story structure
   - Quotable phrases / meme potential
   - Character trait expression
   - Standalone comprehensibility
6. Output a ranked JSON list with start/end times, titles, hooks, and reasons

## Output format

```json
{
  "source_video": {"title": "...", "duration_min": 87},
  "template_style": "@ChannelChiba (chaos+character observation)",
  "clips": [
    {
      "rank": 1,
      "start_sec": 595,
      "end_sec": 932,
      "duration_sec": 337,
      "score": 0.95,
      "title_suggestion": "【ふざけるな】サイコロ振りながら偽フワワに応募してきたフブブにもこ田が本気でブチギレるwww",
      "hook_description": "ふぶき『ホロライブのふわふわしたとこからやってきたフブブです』+直後にカラカラ音→もこ田『ふざけるなよ!』の即ツッコミ",
      "expected_appeal": "笑い・カオス・ツッコミ",
      "emotion_tags": ["笑い", "カオス", "ツッコミ", "天然"],
      "peak_frame_sec": 658,
      "reason": "明確なパンチライン+キャラの濃い側面+ギャップ構造+ビジュアル化しやすい瞬間"
    }
  ]
}
```

## Selection rules (built-in)

The skill uses these criteria when analyzing candidates:

### High priority
- **Clear punchline / story structure** — must have a beat that closes
- **Strong emotion peak** — laughter, surprise, chaos, or cuteness above baseline
- **Character expression** —天然 / 暴走 / ツッコミ / 暴言 / drysarcasm shines through
- **Standalone comprehensibility** — viewer can understand without prior context

### Medium priority
- **Quotable phrases** — short impactful lines that meme well
- **Visual moment** — facial expression / situation that thumbnails strongly
- **First 3 seconds hook** — opens with strong statement or visual
- **Gap / contrast structure** — serious situation × silly reaction etc.

### Hard avoids
- Pure gameplay walkthrough with no reaction
- Long silence or downtime without payoff
- Inside-joke moments that need 5+ minutes of context
- Content that risks defamation / harm

## Composition rules

- Target length: 30-90 sec for short, 2-5 min for standard, 5-10 min for story
- Open with the strongest 3 seconds
- Maintain フリ→展開→オチ structure
- Cut tempo: faster during chaos peaks, slower during character moments
- Caption emphasis on power words: やばい / 神 / 草 / 終わった / ヤバ / うわ

## Optional outputs

- **Premiere Pro FCPXML** — drop into File > Import > XML, builds a timeline
- **DaVinci Resolve script** — places clips on tracks, creates render queue
- **Thumbnail brief JSON** — peak_frame_sec + emotion_tags + title hints for image AI
- **SRT subtitles** — Whisper-derived per-clip captions, editable in any NLE

## Tips for best results

- Provide stream subtitles if available (auto-captions are OK but Whisper transcripts are better)
- Specify a reference clip channel — output style adapts to that channel's thinking
- For VTuber clips: include character name + game name so context-specific phrases score correctly
- Ask for "3-5 clips" first to validate, then re-run for full set
