# Video generation

Read this reference for `video` requests. Routing and polling rules remain in `SKILL.md`.

Supported Seedance workflows include text-to-video, image-to-video, and first/last-frame video. `--image` cannot be mixed with first/last frames, and both frame arguments are required together.

Common parameters for `doubao-seedance-1-5-pro-251215`:

- `resolution`: 480p, 720p, 1080p
- `ratio`: 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive
- `duration`: 2–12 seconds
- audio, draft, watermark, fixed-camera, seed

```bash
python3 scripts/showmeai.py video --prompt "Rain moves across a neon window" --resolution 720p --duration 5 --audio
python3 scripts/showmeai.py video --prompt "The subject turns toward camera" --image source.png
python3 scripts/showmeai.py video --prompt "Seasons change" --first-frame spring.png --last-frame winter.png
```

The command submits the job, journals its task ID, polls `/task/{task_id}` until a terminal state, and downloads the video. Do not replace it with one-shot status checks.
