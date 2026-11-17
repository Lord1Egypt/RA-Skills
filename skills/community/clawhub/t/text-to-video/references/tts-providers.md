# Local speech synthesis

The published core supports only macOS `say`. It runs on the user's device and does not send narration or credentials elsewhere.

## Before rendering

1. Ask the user to choose an installed voice and confirm the selected project output directory.
2. Save only the voice name and playback speed in the project plan.
3. Generate audio with `scripts/generate_tts.sh`; inspect the resulting files before rendering.

## Example plan section

```markdown
## Local narration
- Voice: Tingting
- Speed: 1.0x
- Format: mp3
- Segmentation: one file per scene
```

Hosted speech services are intentionally outside this repository. Any future adapter must be independently reviewed and obtain user confirmation immediately before sending narration off-device.
