---
name: video-post-production
description: >
  End-to-end short-video post-production from one raw talking-head video:
  transcribe speech, build timed subtitle phrases, highlight key words,
  place sound effects (SFX), choose background music (BGM), and render a
  polished final video. Use when the user provides a raw video and wants
  subtitles, SFX, BGM, or a finished short-form edit. Triggers on: 口播,
  字幕, 短视频后期, 加字幕, 加音效, 加BGM, 后期制作, 视频剪辑, raw video,
  subtitle, video editing, post-production.
---

# Video Post-Production

Use this skill when the user gives you **one raw video** and wants a finished
short video with:
- readable subtitles
- highlighted key phrases
- basic SFX emphasis
- optional BGM
- a rendered export

The default workflow is **single-input automation**: the user provides the
video, and you handle the rest.

## Inputs

Required:
- one raw video file with spoken audio

Optional:
- preferred subtitle color/style
- preferred BGM mood
- preferred SFX intensity
- existing BGM file
- existing SFX directory

If optional inputs are missing, proceed with defaults.

## Outputs

Create a working directory next to the input video:
- `<video_name>_output/`

Expected output files:
- `alignment.json`
- `production_plan.json`
- `subtitles.ass`
- `final.mp4`

## Default behavior

If the user does not specify a style:
- subtitles: bold, high-contrast, mobile-readable
- highlights: only on high-value phrases
- SFX: light to medium density
- BGM: optional, low-volume, ducked under speech

Do not block on missing BGM or SFX. A valid delivery can still be:
- subtitles only
- subtitles + generated simple SFX
- subtitles + BGM

## Workflow

### 1. Check prerequisites

Confirm these are available:
- `ffmpeg`
- `ffprobe`
- `python3`
- `faster-whisper` if transcription is needed
- a Chinese-capable font for ASS rendering

Use:

```bash
ffmpeg -version | head -1
ffprobe -version | head -1
python3 -c "from faster_whisper import WhisperModel; print('faster_whisper OK')" 2>/dev/null || echo "Need: pip3 install faster-whisper"
```

If `faster-whisper` is missing:

```bash
pip3 install faster-whisper
```

### 2. Transcribe the video

Run:

```bash
python3 <skill-path>/scripts/align_speech.py \
  --video "<input_video>" \
  --output "<workdir>/alignment.json" \
  --model "medium" \
  --language "zh"
```

This produces word-level timing and segment-level timing.

### 3. Build a post-production plan

Read `alignment.json` and produce `production_plan.json`.

The plan must contain:
- `subtitle_groups`
- `sfx`
- `bgm`

Minimum shape:

```json
{
  "subtitle_groups": [],
  "sfx": [],
  "bgm": {
    "mood": "inspirational",
    "tempo": "medium",
    "volume": -18
  }
}
```

#### Planning rules

Subtitle grouping:
- group into natural spoken phrases
- do not split a phrase awkwardly
- prefer 3-8 Chinese characters per phrase
- prefer 0.5s or longer readable display windows
- keep within mobile reading comfort

Keyword highlighting:
- highlight emotional, contrastive, numeric, warning, CTA, and payoff phrases
- do not over-highlight
- default target: 1-3 highlighted phrases per 10 seconds

SFX placement:
- opening transitions
- key claims
- warnings
- CTA moments
- major topic pivots

Do not place SFX on every subtitle. Keep it sparse enough to feel intentional.

BGM choice:
- educational / explainer -> uplifting / neutral
- warning / risk -> tense / restrained
- positive / benefit-driven -> hopeful / energetic

### 4. Generate ASS subtitles

Run:

```bash
python3 <skill-path>/scripts/generate_subtitles.py \
  --plan "<workdir>/production_plan.json" \
  --output "<workdir>/subtitles.ass" \
  --video-width 720 \
  --video-height 1280 \
  --font "Heiti SC" \
  --font-size 48
```

If you need deeper ASS styling guidance, read:
- `<skill-path>/references/ass_effects.md`

### 5. Prepare audio

#### BGM

Preferred order:
1. user-provided BGM
2. existing local BGM in workspace
3. proceed without BGM

If BGM exists, prepare it:

```bash
ffmpeg -stream_loop -1 -i "<bgm_file>" -t <video_duration> \
  -af "volume=-18dB,afade=t=in:d=2,afade=t=out:st=<duration-3>:d=3" \
  -y "<workdir>/bgm_prepared.wav"
```

#### SFX

Preferred order:
1. user-provided SFX directory
2. existing local SFX directory
3. generate simple fallback tones/noise

If no SFX files are available, read:
- `<skill-path>/references/audio_resources.md`

### 6. Render final video

Run:

```bash
python3 <skill-path>/scripts/render_video.py \
  --input "<input_video>" \
  --subtitles "<workdir>/subtitles.ass" \
  --plan "<workdir>/production_plan.json" \
  --bgm "<workdir>/bgm_prepared.wav" \
  --sfx-dir "<workdir>/sfx" \
  --output "<workdir>/final.mp4" \
  --resolution "720x1280"
```

If no BGM exists, omit `--bgm`.
If no SFX directory exists, omit `--sfx-dir`.

## Quality bar

The result should feel like a polished short-form knowledge video:
- subtitles are easy to read on mobile
- highlighted words are meaningful, not noisy
- SFX emphasize real rhetorical beats
- BGM stays below speech and never masks intelligibility
- final export is usable without extra manual cleanup

## Fallback rules

If the raw video is usable but supporting resources are missing:
- still deliver subtitles and a rendered video
- note what was skipped
- do not block the whole workflow waiting for perfect assets

If transcription quality is poor:
- keep subtitle grouping conservative
- prefer fewer highlights
- avoid aggressive SFX timing

## Bundled resources

Scripts:
- `scripts/align_speech.py`
- `scripts/generate_subtitles.py`
- `scripts/render_video.py`

References:
- `references/ass_effects.md`
- `references/audio_resources.md`

## Final delivery checklist

Before finishing, ensure:
- `alignment.json` exists
- `production_plan.json` exists
- `subtitles.ass` exists
- final video renders successfully
- subtitles are visible
- speech remains clear
- SFX and BGM are not overpowering
