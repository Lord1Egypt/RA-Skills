# Troubleshooting

This document is intentionally generic for the ClawHub release version.

## Common issues

### YouTube download gets blocked

Use a valid `cookies.txt` export and set:

```powershell
$env:YTDLP_COOKIES_FILE="path\to\www.youtube.com_cookies.txt"
```

If the JavaScript challenge is heavy, also set:

```powershell
$env:NODE_OPTIONS="--max-old-space-size=4096"
```

### Prepare stage fails on a large video

The pipeline already resizes cover images before intro replacement.
If prepare still fails, rerun the same video or inspect the generated processed file.

### TTS or dub stage needs a rebuild

Use the controller with `--refresh-tts` so the translation, TTS, dub, retime, and subtitle outputs are regenerated consistently.

### An editor picked the wrong subtitle file

Use the cache-safe final subtitle:

- `*_zh_retimed_v4_final.srt`

### Output files look incomplete

Check these directories in order:

1. `data/structured/`
2. `data/dubbed_audio/`
3. `data/output/`
4. `data/subtitles/`

If one stage completed but the next did not, rerun the controller or the specific downstream script.

## Release notes for agents

- Do not hardcode API keys in the skill.
- Do not hardcode cookies paths.
- Do not rely on old rescue scripts.
- Prefer the main controller over piecemeal manual steps unless the user explicitly asks for a partial rerun.

