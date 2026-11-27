# Production stack: free first, paid optional

Tool features, limits and prices change. The notes marked "checked 23 Nov 2026" come from the vendors' own pages on that date; everything else is general knowledge, so confirm it before relying on it.

## The free path (default)

| Step | Free options | Notes |
|---|---|---|
| Script | Claude | Use `script_tools.py check` for timing and `budget` for word counts |
| Voice | The user's own voice on a phone mic; an editor's built-in text to speech; open-source offline text to speech such as Piper | Own voice usually sounds most natural. Built-in and open-source voices vary in quality and language coverage; check each voice's licence for commercial use. Avoid unofficial tools that scrape read-aloud services, which can break or breach terms |
| Visuals | Own footage; phone screen recording; OBS Studio for desktop screen capture; free-licensed stock such as Pexels and Pixabay | Read each stock licence (restrictions often apply to identifiable people, brands and resale). Search with the keywords from the B-roll column |
| Music and SFX | YouTube Audio Library for YouTube; each platform's own sound library | Business and brand accounts on some platforms can only use commercially licensed music; check the account type |
| Editing | CapCut (free tier), DaVinci Resolve (free desktop version) | Free tiers differ in which features are paid; check before planning around a specific effect or export setting |
| Captions | `script_tools.py srt` for a timed file from the script, or the editor's auto captions | Auto captions on Urdu, Roman Urdu and Hinglish are often inaccurate; always proofread them |
| Cover frame and title | Pick a clear frame; write the title as a short version of the hook | |

Workflow in order: script, record or generate voiceover, assemble visuals to the shot list, import `captions.srt` or auto-caption, add on-screen text and SFX, export vertical 9:16, upload natively. Batch several videos in one session (write all, record all, edit all) to cut setup time.

### Using the SRT from the script

`script_tools.py srt` estimates caption timing from word counts. Once the real voiceover exists, pass its length with `--audio-seconds` so the timings stretch to match; then import the SRT into the editor and nudge any lines that drift. If the editor can auto-caption from audio, use that for timing and the script only to check spelling.

## Paid upgrades (only when the user asks)

### ElevenLabs (voiceover)

Checked 23 Nov 2026 against ElevenLabs docs:

- Eleven v3 and v4 use bracketed audio tags (for example `[whispers]`, `[sighs]`, `[laughs]`) and punctuation for delivery. They do not support SSML break tags. Ellipses create pauses, capitals add emphasis, and v4's speed setting ranges from 0.7 to 1.2.
- Multilingual v2, Flash v2 and Flash v2.5 use the break tag `<break time="1.5s" />` for pauses, up to 3 seconds each. Many breaks can speed up speech or add artefacts, and some voices insert "uh" sounds in pauses.
- Pronunciation of hard words can be steered with IPA in slashes (v4); test each with the chosen voice.
- Prices and free-tier limits were not checked; send the user to the pricing page.

Hand-off format: a clean voiceover-only text, scene by scene, with delivery tags matched to the chosen model, a list of hard-to-pronounce words with a suggested spelling or IPA, and a note on target pace. If the user names no model, ask which they selected, since the pause method differs.

### HeyGen (avatar videos)

Checked 23 Nov 2026 on HeyGen's pricing page: the free plan allowed 3 watermarked videos a month of up to 1 minute each; the Creator plan was listed at $29 a month with longer videos and no watermark. Plans change.

Hand-off format: a script of short, speakable sentences with no stage directions inside the spoken text, split into one block per scene so the avatar can be re-rendered scene by scene; on-screen text, B-roll and music are added in the editor. Keep each block short, and for free-plan use keep the total under a minute. Disclose avatar use where platform rules require it.

### Veo (AI video clips)

Checked 23 Nov 2026 against Google DeepMind's Veo prompt guide: effective prompts spell out shot framing and camera motion, style, lighting, character description, location, action and, where wanted, dialogue and audio. Clip length limits and prices were not confirmed; check the current limit in the tool you use.

Hand-off format: one prompt per shot, written as: framing and motion, subject and appearance, location, action, lighting and style, audio or dialogue, plus a "consistency block" (the same character and style description repeated in every prompt). Plan to mix generated shots with real footage, keep shots short, and review every clip for artefacts before use. Label realistic AI footage according to platform rules.

### Sora

Discontinued. OpenAI announced the shutdown on 24 March 2026, and its developer documentation states that the Sora 2 models and Videos API were shut down on 24 September 2026. Do not recommend it; if the user asks, point to the options above or to other current tools after checking they are available.

## AI content disclosure

Many platforms ask creators to label realistic AI-generated or altered media (voices, faces, scenes). Check the current rule on each platform before posting, and label when in doubt.
