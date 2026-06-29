# VideoLens Video Intelligence OCC Skill

Manual-only OCC local skill wrapper for VideoLens.

Repo: https://github.com/shadoprizm/videolens

## Actions

Use task `pre_instructions` as JSON or YAML.

### Preflight

```json
{"action":"preflight"}
```

Checks git, ffmpeg, ffprobe, uv/python, repo/bootstrap state, and OpenAI key availability.

### Bootstrap

```json
{"action":"bootstrap"}
```

Clones VideoLens into OCC data and runs `uv sync --extra ui`.

### Analyze

```json
{
  "action": "analyze",
  "allow_credit_spend": true,
  "source": "https://www.youtube.com/watch?v=...",
  "mode": "bug",
  "prompt": "Identify the bug and create reproduction steps.",
  "max_frames": 20,
  "frame_interval": 5.0
}
```

Analysis writes artifacts under OCC data: `videolens-video-intelligence/runs/<run_id>/`.

Returns structured metadata including report/analysis paths and CLI output.

## Guardrails

Real analysis is credit-spending and requires `allow_credit_spend: true`.

Default action is preflight.
