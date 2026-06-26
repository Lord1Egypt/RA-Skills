# SenseAudio Media Pipeline

Use SenseAudio for media creation around the local HTML renderer.

## Narration

1. Query voices with `voices --voice-type all`.
2. Generate narration with `tts`.
3. Add the resulting audio to `assets/`.
4. Register it with `asset-add --type audio --role voiceover`.
4. Render with `--audio`.

## Captions

1. Run `asr --timestamps word`.
2. Run `captions --transcript assets/transcript.json --output assets/captions.json`.
3. Add a caption element with `data-caption-source="./assets/captions.json"`.
4. Use `renderFrame(time)` only for extra effects such as word highlighting.
5. Export sidecar subtitles with `captions-export --format srt` or `--format vtt` when publishing platforms need uploads.

## Images

Use `image-sync` to generate first frames, backdrops, thumbnails, or product mood images. Download them into `assets/` for stable local renders.

Register downloaded images with `asset-add --type image`; this keeps later renders reproducible even when prompt history is long.

For storyboard-driven projects, prefer:

```bash
python3 scripts/senseaudio_video_gen.py generate-assets \
  --project my-video \
  --image-prompt "clean product UI hero image" \
  --video-prompt "short creator b-roll for voice selection" \
  --dry-run
```

Remove `--dry-run` to call SenseAudio. `compose --generate-images --generate-broll --asset-dry-run` creates the same HTML slots and manifest requests while drafting.

## Manifests And Reports

- `assets/asset-manifest.json` is the inventory for local and generated assets.
- `asset-report --json` checks what exists and what is missing.
- `lint --strict` blocks final builds when required files are missing.
- `render` writes a render report JSON and registers the MP4 as `final-video` by default.

## Generated Video Clips

Use `video-create` when the project needs generative b-roll or first-frame/reference-material motion. Download the completed clip and place it as a timed `<video>` element in the HTML project.

Use the local HTML renderer for controlled UI, typography, layout, and product walkthroughs. Use SenseAudio model video for b-roll, atmospheric shots, or motion inserts that do not need pixel-level UI fidelity.

Generated video tasks are registered as planned/submitted assets. Use `generate-assets --poll` to poll and download automatically, or poll with `video-status`, download the result, then update the asset with `asset-add --type video --role broll`.
