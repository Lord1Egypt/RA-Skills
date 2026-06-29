---
name: "research-to-music-video-pipeline"
description: "Create 60s music videos from research articles using storyboard PDF, image/video/audio gen, and ffmpeg assembly."
---

# Research-to-Music-Video Pipeline

Turn a research article into a finished 60-second music video and a structured storyboard PDF.

## Prime Directive

Run this as a resumable production pipeline, not as a chat-only brainstorm. The final deliverables are:

- `final.mp4`: stitched 60-second music video with generated song underneath.
- `storyboard.pdf`: structured PDF with narrative storyboard, image prompts, video prompts, music direction, source notes, and provider/job metadata.

## Required Flow

1. Accept article input as pasted text, local file, PDF URL, or article URL.
2. Run research extraction and prompt generation.
3. Produce a structured storyboard document and render it to PDF.
4. Generate one image still per scene.
5. Generate one video clip per scene from the scene still plus video prompt.
6. Generate one original song/audio bed based on the article theme and mood.
7. Stitch clips in storyboard order and mix the song underneath.
8. Return `final.mp4`, `storyboard.pdf`, and a concise run summary.

## Approval Gates

Do not spend paid credits or launch long-running generation jobs until the user has approved:

- Provider choices for image, video, and audio.
- Scene count and target duration.
- Whether to proceed from prompt pack/storyboard into media generation.

You may generate the research brief, prompt pack, and storyboard draft before that approval when no paid or external generation is required.

## Provider Wiring

Use available runtime tools exactly as exposed. If a tool is deferred, discover and load the exact callable spec first.

Target providers from the user request:

- Orchestration and prompt rewriting: GPT-4o or the best available current reasoning/orchestration model.
- Video: SkyReels V3 Reference-to-Video via apifree.ai, Kling 3.0, or another explicitly configured reference-to-video provider.
- Audio: Suno, MiniMax audio, or another explicitly configured music generation provider.
- Image: the configured image generation tool/model suitable for cinematic stills.
- Assembly: local `ffmpeg`/`ffprobe`.

If a target provider is unavailable or missing credentials, produce the storyboard/prompt pack and ask for the missing provider/credential. Do not silently substitute providers for final generation unless the user approves.

## Run Directory

Create one timestamped run directory:

```text
research-music-video-runs/<safe-title>-YYYYMMDD-HHMMSS/
```

Use this structure:

```text
source/
  article.pdf | article.html | article.txt
storyboard.md
storyboard.pdf
prompts.json
manifest.json
images/
  scene-01.png
videos/
  scene-01.mp4
audio/
  song.mp3 | song.wav
assembly/
  concat.txt
  normalized/
final.mp4
```

Update `manifest.json` after every completed step so interrupted runs can resume.

## Research Extraction

Extract or infer:

- Title, authors, URL/path, date/venue if available.
- Abstract or short article summary.
- Core thesis.
- 3-6 key ideas.
- Methods/evidence if present.
- Limitations or uncertainties.
- Useful visual metaphors.
- Terms that must remain scientifically accurate.

If extraction is partial, state that in the storyboard and preserve the source file.

## Storyboard Contract

Create `storyboard.md` with these sections:

1. Title page metadata: article title, source, date, generated video title, duration, aspect ratio.
2. Research brief: thesis, key ideas, findings, caveats.
3. Music direction: genre, mood, tempo, energy arc, instrumentation, vocal/lyric preference.
4. Scene table with one row per scene:
   - scene id
   - duration seconds
   - narrative beat
   - visual metaphor or literal representation
   - image prompt
   - video prompt
   - transition notes
   - music cue
5. Provider plan: chosen image/video/audio providers and pending credentials if any.
6. Source notes and caveats.

Render `storyboard.md` to `storyboard.pdf` using available local tooling. Use pandoc, playwright print-to-PDF, or another reliable renderer already available in the environment.

## Scene Defaults

Unless the user specifies otherwise:

- Total duration: 60 seconds.
- Scene count: 6.
- Scene duration: 10 seconds each.
- Aspect ratio: 16:9.
- Style: cinematic, research-faithful, visually legible, emotionally engaging.
- Audio: original instrumental song with no vocals.

Adjust scene count only when provider duration limits require it.

## Prompt Generation

For every scene, generate:

- `image_prompt`: still-image prompt with subject, composition, style, lighting, camera/lens, aspect ratio, and negative constraints.
- `video_prompt`: reference-to-video prompt with motion, camera movement, temporal progression, transformation, continuity requirements, and mood.

Rules:

- Keep scientific claims faithful to the article.
- Use metaphor for abstract concepts, but label the metaphor in the storyboard.
- Avoid copyrighted artist/style imitation. Use descriptive genre and visual language.
- Keep prompts provider-ready and self-contained.

## Image Generation

For each scene:

1. Send `image_prompt` to the selected image generator.
2. Save still as `images/scene-XX.<ext>`.
3. Check it exists, is nonzero size, and roughly matches aspect ratio.
4. Record provider, request id/job id, prompt, and path in `manifest.json`.

If an image is blank, corrupt, wrong subject, or unusable, regenerate that scene only.

## Video Generation

For each scene:

1. Send `video_prompt` plus matching still to the selected reference-to-video provider.
2. Prefer SkyReels V3 via apifree.ai or Kling 3.0 when available and approved.
3. Save clip as `videos/scene-XX.mp4`.
4. Verify clip exists, has nonzero duration, and is playable with `ffprobe`.
5. Record provider, request id/job id, prompt, still path, clip path, status, and duration.

If a video job is pending, report the job id and do not claim final completion. If one scene fails, retry or substitute only that scene with user approval.

## Music Generation

Create an audio prompt from the research brief and storyboard:

- Genre.
- Mood.
- Tempo.
- Instrumentation.
- Energy arc.
- Target duration at least 60 seconds.
- Vocals/lyrics only if the user asks.

Generate original music with Suno, MiniMax audio, or another approved provider. Save under `audio/` and record prompt, provider, job id, and file path in `manifest.json`.

## Assembly

Use `ffmpeg` to create `final.mp4`:

1. Normalize clips to a common resolution, frame rate, codec, and pixel format.
2. Concatenate clips in storyboard order.
3. Trim or fade audio to match exact video duration.
4. Mix the song underneath.
5. Export H.264/AAC MP4 unless user requests another format.

Use simple cuts by default. Add crossfades only when they are easy to verify and do not introduce timing problems.

## Verification Before Completion

Before reporting success:

- Verify `storyboard.pdf` exists and has nonzero size.
- Verify every scene has an image and clip path in `manifest.json`.
- Run `ffprobe` on every clip or at least confirm nonzero duration for each clip.
- Run `ffprobe` on `final.mp4` and confirm video and audio streams exist.
- Confirm final duration is close to 60 seconds, or explain the exact duration.
- Scan manifests/logs/summaries for accidentally stored secrets.

Useful commands:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height -of default=nw=1 final.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=nw=1 final.mp4
```

## Final Response

Return only high-signal status:

- Final video path.
- Storyboard PDF path.
- Source article title.
- Provider choices used.
- Final duration.
- Any failed, retried, substituted, or pending jobs.

Do not claim the video is complete unless the verification gate passed.

## Failure Modes

- Article extraction fails: ask for pasted text or a local file.
- Provider credential missing: stop at storyboard/prompt pack and ask for credential/provider setup.
- Video provider times out: preserve job id and ask whether to wait, retry, or substitute.
- Audio generation fails: ask before assembling a silent draft.
- `ffmpeg` missing: return storyboard, prompts, generated assets, and exact assembly plan.
