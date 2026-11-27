# Output templates

Write the deliverable in the user's own language and register. Keep the voiceover in the audience's language and the production notes in a language the user reads comfortably.

## Script document

1. **Setup line:** platform, length, audience, language, goal and CTA, presenter style, assumptions.
2. **What the data says:** 3 to 5 observations from the research with their source (or a note that none was collected).
3. **Hooks:** the 3 best options with type and a one-line reason, and the chosen one.
4. **Script table:**

| # | Time | Voiceover | On-screen text | Visual and camera | B-roll | SFX and music | Notes |
|---|---|---|---|---|---|---|---|

5. **CTA:** wording, placement and what it asks the viewer to do.
6. **Voiceover only:** the full spoken text in one block, with no stage directions, ready to read aloud or paste into a text-to-speech tool.
7. **Platform variants:** only what changes (first line, length, CTA, caption or title).
8. **Production checklist (free path):** voice, footage and B-roll to collect with keywords, editing steps, captions.
9. **Test plan:** what to compare across the next 5 to 8 videos (hook type, length, CTA), the metric that decides, and the decision rule.

If the session offers a document artifact type, put the script document there; otherwise write markdown.

## Script JSON (input for `script_tools.py`)

```json
{
  "title": "3 mistakes killing your reels",
  "platform": "youtube_shorts",
  "target_seconds": 30,
  "language": "en",
  "wpm": 165,
  "scenes": [
    {
      "voiceover": "These 3 mistakes are killing your reels.",
      "on_screen_text": "3 MISTAKES",
      "visual": "Presenter close-up, mid-gesture",
      "broll": "",
      "camera": "close-up, handheld",
      "sfx": "hit on 'kill'",
      "seconds": null,
      "cta": false
    }
  ]
}
```

Fields: `voiceover`, `on_screen_text`, `visual`, `broll`, `camera`, `sfx` are text. `seconds` (optional) overrides the estimated duration of a scene, which is useful for silent beats. `cta: true` marks a scene as the call to action. `wpm` is the presenter's pace; the command line can override it. Only `scenes` is required.

## Commands

```bash
python scripts/script_tools.py budget --seconds 15 30 60 90 --wpm 165
python scripts/script_tools.py check script.json --target 30 [--json report.json] [--strict]
python scripts/script_tools.py srt script.json --out captions.srt [--max-words 4] [--upper] [--audio-seconds 28.4]
python scripts/script_tools.py shotlist script.json --out shotlist [--md] [--audio-seconds 28.4]
```

Timings are estimated from word counts and sentence pauses. When the real voiceover exists, pass its length as `--audio-seconds` so the SRT and shot list stretch to match.

## Files to hand over

- the script document
- `script.json`
- `shotlist.csv`
- `captions.srt`
- the voiceover-only text (inside the document, and as a `.txt` if the user will paste it into a tool)

## Length

The script document should be easy to read in a few minutes. Put the long production detail in the shot list, not the document.
