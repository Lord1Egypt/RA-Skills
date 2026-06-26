---
name: chat-with-anyone
description: Chat with any real person or fictional character in their own voice by automatically finding their speech online, extracting a clean reference sample, and generating audio replies. Also supports generating a matching voice from an uploaded image. Use when the user says "我想跟xxx聊天", "你来扮演xxx跟我说话", "让xxx给我讲讲这篇文章", "我想跟图片中的人说话", or similar.
permissions:
  - network
  - filesystem
metadata: {"openclaw": {"primaryEnv": "NOIZ_API_KEY"}}
---

# Chat with Anyone

Clone a real person's voice from online video, or design a voice from a photo, then roleplay as that person with TTS.

## Important: Ethical Use & Copyright

This skill synthesizes speech that imitates real voices. Before proceeding, the agent **must**:

1. **Never impersonate** someone to deceive, defraud, or harass.
2. **Only use publicly available media** (public speeches, interviews, press conferences) as reference audio.
3. **Inform the user** that generated audio is synthetic and should not be presented as genuine recordings.
4. **Decline requests** that target private individuals who have not consented, or that are clearly intended for deception, harassment, or defamation.

If the user's intent appears harmful, refuse politely and explain why.

## Prerequisites

| Dependency | Type | How to verify |
|-----------|------|---------------|
| `ffmpeg` | System binary | `ffmpeg -version` |
| `yt-dlp` | System binary | `yt-dlp --version` |
| `tts` skill | Cursor skill | `ls skills/tts/scripts/tts.py` |
| `NOIZ_API_KEY` | Env var or file | `python3 skills/tts/scripts/tts.py config --show` |

**Before the first run**, verify all dependencies are present:

```bash
ffmpeg -version && yt-dlp --version && ls skills/tts/scripts/tts.py
```

If `yt-dlp` is missing, install it:

```bash
uv pip install yt-dlp
```

If the Noiz API key is not configured:

```bash
python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY
```

## Mode Selection

- **User names a person** (real or fictional) --> Workflow A
- **User provides an image**, person is unrecognizable --> Workflow B
- **User provides an image**, person is a recognizable public figure --> Workflow A (real voice is more authentic)
- **Multiple people in image** --> Ask which person first

---

## Workflow A: Name-based (voice from online video)

Track progress with this checklist:

```
- [ ] A1. Disambiguate character
- [ ] A2. Find reference video
- [ ] A3. Download audio + subtitles
- [ ] A4. Extract best reference segment
- [ ] A5. Generate speech
```

### A1. Disambiguate Character

If ambiguous (e.g. "US President", "Spider-Man actor"), ask the user to specify the exact person before proceeding.

### A2. Find a Reference Video

Use web search to find a YouTube (or Bilibili) video of the person speaking clearly. Best candidates: interviews, speeches, press conferences. Avoid videos with heavy background music.

Search queries to try:
- `{CHARACTER_NAME} interview` / `{CHARACTER_NAME} 采访`
- `{CHARACTER_NAME} speech` / `{CHARACTER_NAME} 演讲`
- `{CHARACTER_NAME} press conference`

### A3. Download Audio and Subtitles

```bash
mkdir -p "tmp/chat_with_anyone/{CHARACTER_NAME}"
yt-dlp -x --audio-format mp3 \
  --write-subs --write-auto-subs --sub-langs "en,zh-Hans" \
  --convert-subs srt \
  -o "tmp/chat_with_anyone/{CHARACTER_NAME}/%(title)s.%(ext)s" \
  "{VIDEO_URL}"
```

After download, list the output directory to identify the audio file and SRT subtitle file:

```bash
ls tmp/chat_with_anyone/{CHARACTER_NAME}/
```

Expected output: a `.mp3` audio file and one or more `.srt` subtitle files.

**If no subtitle files appear**: try a different video that has auto-generated captions, or adjust `--sub-langs` for the target language.

### A4. Extract Best Reference Segment

Use the automated extraction script — it parses the SRT, finds the densest 3-12 second speech window, and extracts it as a WAV:

```bash
python3 skills/chat-with-anyone/scripts/extract_ref_segment.py \
  --srt "tmp/chat_with_anyone/{CHARACTER_NAME}/{SRT_FILE}" \
  --audio "tmp/chat_with_anyone/{CHARACTER_NAME}/{AUDIO_FILE}" \
  -o "tmp/chat_with_anyone/{CHARACTER_NAME}/ref.wav"
```

The script prints the selected time range and saves the reference WAV. Verify the output exists and is non-empty before proceeding.

**If the script reports no suitable segment**: try `--min-duration 2` for shorter clips, or download a different video.

### A5. Generate Speech and Roleplay

Write a response in character, then synthesize it:

```bash
python3 skills/tts/scripts/tts.py \
  -t "{RESPONSE_TEXT}" \
  --ref-audio "tmp/chat_with_anyone/{CHARACTER_NAME}/ref.wav" \
  -o "tmp/chat_with_anyone/{CHARACTER_NAME}/reply.wav"
```

Present the generated audio file to the user along with the text. For subsequent messages, reuse the same `--ref-audio` path.

---

## Workflow B: Image-based (voice from photo)

Track progress with this checklist:

```
- [ ] B1. Analyze image
- [ ] B2. Design voice
- [ ] B3. Preview (optional)
- [ ] B4. Generate speech
```

### B1. Analyze the Image

Use your vision capability to examine the image:

1. **If the person is a recognizable public figure** --> switch to Workflow A for authentic voice.
2. **If unrecognizable**, produce a voice description covering:
   - Gender (male / female)
   - Approximate age (e.g. "around 30 years old")
   - Apparent demeanor (e.g. cheerful, authoritative, gentle)
   - Contextual cues (e.g. suit --> professional tone; athletic outfit --> energetic)

### B2. Design the Voice

Pass both the image and the description to the voice-design script:

```bash
python3 skills/chat-with-anyone/scripts/voice_design.py \
  --picture "{IMAGE_PATH}" \
  --voice-description "{VOICE_DESCRIPTION}" \
  -o "tmp/chat_with_anyone/voice_design"
```

The script outputs:
- Detected voice features (printed to stdout)
- Preview audio files in the output directory
- `voice_id.txt` containing the best voice ID

Read the voice ID:

```bash
cat tmp/chat_with_anyone/voice_design/voice_id.txt
```

### B3. Preview (Optional)

Present the preview audio files from the output directory so the user can hear the voice. If unsatisfied, re-run B2 with adjusted `--voice-description` or `--guidance-scale`.

### B4. Generate Speech and Roleplay

```bash
python3 skills/tts/scripts/tts.py \
  -t "{RESPONSE_TEXT}" \
  --voice-id "{VOICE_ID}" \
  -o "tmp/chat_with_anyone/voice_design/reply.wav"
```

For subsequent messages, keep using the same `--voice-id` for consistency.

---

## Example: Name-based

**User**: 我想跟特朗普聊天，让他给我讲个睡前故事。

**Agent steps**:
1. Character: Donald Trump. No disambiguation needed.
2. Search `Donald Trump speech youtube`, find a clear speech video.
3. Download:
   `yt-dlp -x --audio-format mp3 --write-subs --write-auto-subs --sub-langs "en" --convert-subs srt -o "tmp/chat_with_anyone/trump/%(title)s.%(ext)s" "https://youtube.com/watch?v=..."`
4. Extract reference:
   `python3 skills/chat-with-anyone/scripts/extract_ref_segment.py --srt "tmp/chat_with_anyone/trump/....srt" --audio "tmp/chat_with_anyone/trump/....mp3" -o "tmp/chat_with_anyone/trump/ref.wav"`
5. Generate TTS in Trump's style:
   `python3 skills/tts/scripts/tts.py -t "Let me tell you a tremendous bedtime story..." --ref-audio "tmp/chat_with_anyone/trump/ref.wav" -o "tmp/chat_with_anyone/trump/reply.wav"`
6. Present `reply.wav` and the story text to the user.

## Example: Image-based

**User**: [uploads photo.jpg] 我想跟这张图片里的人聊天

**Agent steps**:
1. Vision analysis: unrecognizable young woman, ~25, casual sweater, warm smile.
2. Design voice:
   `python3 skills/chat-with-anyone/scripts/voice_design.py --picture "photo.jpg" --voice-description "A young Chinese woman around 25, gentle and warm voice, friendly tone" -o "tmp/chat_with_anyone/voice_design"`
3. Read voice ID from `tmp/chat_with_anyone/voice_design/voice_id.txt`.
4. Generate TTS:
   `python3 skills/tts/scripts/tts.py -t "你好呀！很高兴认识你！" --voice-id "{VOICE_ID}" -o "tmp/chat_with_anyone/voice_design/reply.wav"`
5. Present audio and continue roleplay with same `--voice-id`.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `yt-dlp` download fails or video unavailable | Try a different video URL; some regions/videos are restricted. Run `yt-dlp -U` to update |
| No SRT subtitle files | Re-download with `--sub-lang en,zh-Hans`; if still none, try a different video with auto-captions |
| `extract_ref_segment.py` finds no suitable window | Use `--min-duration 2` for shorter clips, or try a different video |
| Voice design returns error | Check Noiz API key; ensure image is a clear photo of a person |
| TTS output sounds wrong | For Workflow A, try a different reference video; for Workflow B, adjust `--voice-description` |
