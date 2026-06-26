# Production Workflows

## Brief To HTML Video Project

1. For LLM-written copy and storyboard, run `llm-plan --provider deepseek --brief "..." --output plan.json`.
2. Run `styles --json` and choose a `--style-preset`, then run `compose --project <dir> --brief "..." --plan-file plan.json --beat-mode layered --offline` to create the editable project shell, or use `compose --llm deepseek` to call DeepSeek inline.
3. Review `index.html`, `assets/llm-plan.json`, `assets/narration.txt`, `assets/storyboard.json`, `assets/beats.json`, and `assets/captions.json`.
4. Add generated media slots with `compose --generate-images --generate-broll --asset-dry-run`, or run `generate-assets --dry-run` after composing.
5. Remove `--offline` and provide `--voice-id` when live SenseAudio TTS/ASR should generate final narration and captions.
6. Remove `--asset-dry-run` or run `generate-assets` without `--dry-run` when image/video credits should be used.
7. Run `beats --project <dir>` after storyboard edits, then run `timeline --project <dir> --preset cinematic --transition-preset editorial --timeline-engine gsap-compat` when scene boundaries and element tracks need stronger authored motion.
8. Run `lint --project <dir> --json` to catch missing assets or caption sources.
9. Run `motion-audit --project <dir> --strict` and `motion-map --project <dir> --strict` to catch mismatches, dead zones, and weak motion coverage.
10. Run `inspect` to catch visual timing issues.
11. Run `build --project <dir>` for the local pipeline, or `render --audio assets/narration.mp3` for manual control.
12. Export external subtitles with `captions-export --format srt` or `--format vtt` when the target platform needs a sidecar file.

## DeepSeek Planning

- Default base URL: `https://api.deepseek.com`
- Default model: `deepseek-v4-pro`
- Auth env var: `DEEPSEEK_API_KEY`
- Override with `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`, `--base-url`, `--model`, `--llm-base-url`, or `--llm-model`.

The planner asks for strict JSON with `title`, `headline`, `narration`, `visual_style`, and `storyboard`. Video copy defaults to Chinese (`zh-CN`) unless the brief explicitly asks for another language. Save plans with `llm-plan --output plan.json` when you want reproducible drafts.

## Text Prompt To Finished Video

1. Expand the user's idea into a concise visual prompt with subject, camera motion, lighting, style, and ending frame.
2. Run `video-create --prompt ... --poll --manifest manifest.json`.
3. If the result is too loose, generate a still with `image-sync`, then rerun as first-frame video.

## Narrated Short Video

1. Write a short narration script. Keep voiceover shorter than the target duration.
2. Run `tts` and save `narration.mp3`.
3. Run `asr --timestamps word --output transcript.json` to create caption timing.
4. Run `captions --transcript transcript.json --output captions.json`.
5. Use local HTML for controlled UI/layout, or `video-create` for generative motion inserts. If background music or narration should influence generation, provide a public `--audio-url`.
6. Return `asset-manifest.json`, `narration.mp3`, `transcript.json`, `captions.json`, and `result.mp4` or `video_url`.

## QA And Delivery

1. Run `lint --strict` before final render.
2. Run `asset-report --json` and fix missing files.
3. Render with `render` or `build`; both write a render report JSON next to the MP4 unless `--report` is set.
4. Return the MP4, render report, SRT/VTT if created, and `assets/asset-manifest.json`.

## Image To Video

1. Use an existing image URL or generate one with `image-sync`.
2. For controlled motion from one image, use `--image-role first_frame`.
3. For interpolation between two stills, pass first and last images with `Seedance-Pro-1.5` or a supported Seedance mode.
4. Keep prompts explicit about camera movement; otherwise generated motion may drift.

## Fallbacks

- If a video task is slow, return the task ID and manifest so the user can resume polling later.
- If local media cannot be accepted as a video/audio reference, ask for a public URL or upload the file to the user's chosen storage.
- If ASR lacks useful timestamps, retry with `senseaudio-asr-pro-1.5-260319` and `timestamp_granularities[]=word`.
