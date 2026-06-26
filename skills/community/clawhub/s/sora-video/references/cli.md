# CLI Reference (`scripts/sora.py`)

Full command reference for the bundled Sora CLI. The CLI is adapted from Codex's production Sora 2 skill.

## Commands
| Command | Description |
|---------|-------------|
| `create` | Create a new video job |
| `create-and-poll` | Create, poll until complete, optionally download |
| `create-character` | Upload a reusable non-human character reference |
| `edit` | Edit an existing generated video by ID |
| `extend` | Continue a completed video |
| `poll` | Wait for an existing job to finish |
| `status` | Retrieve job status/details |
| `download` | Download video/thumbnail/spritesheet |
| `list` | List recent video jobs |
| `delete` | Delete a video job |
| `create-batch` | Create multiple jobs from JSONL input (local fan-out) |
| `remix` | Legacy remix endpoint (deprecated — use `edit`) |

Live API calls require `OPENAI_API_KEY`. `--dry-run` does not.

## Setup
```bash
export SORA_CLI="<path-to-sora-video-skill>/scripts/sora.py"
```

If uv cache fails with permission errors:
```bash
export UV_CACHE_DIR="/tmp/uv-cache"
```

## Defaults
- Model: `sora-2`
- Size: `1280x720`
- Seconds: `4`
- Variant: `video`
- Poll interval: `10` seconds

Allowed seconds: `4`, `8`, `12`, `16`, `20`

Allowed sizes:
- `sora-2`: `1280x720`, `720x1280`
- `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`, `1920x1080`, `1080x1920`

## Create
```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2 \
  --prompt "Wide tracking shot of a teal coupe on a desert highway" \
  --size 1280x720 \
  --seconds 8
```

With input reference image:
```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2-pro \
  --prompt "She turns around and smiles, then slowly walks out of frame." \
  --size 1280x720 \
  --seconds 8 \
  --input-reference sample_720p.jpeg
```

With characters:
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Mossy, a moss-covered teapot mascot, rushes through a market at dusk." \
  --character-id char_123 \
  --seconds 8
```

With augmentation fields (instead of writing a structured prompt):
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Premium headphones on display" \
  --use-case "product teaser" \
  --scene "dark studio, soft haze" \
  --camera "85mm, slow orbit" \
  --lighting "soft key, gentle rim" \
  --seconds 8
```

With pre-structured prompt (disable augmentation):
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt-file prompt.txt \
  --no-augment \
  --seconds 16
```

## Create and Poll
```bash
uv run --with openai python "$SORA_CLI" create-and-poll \
  --model sora-2-pro \
  --prompt "Close-up of steaming coffee on a wooden table" \
  --size 1920x1080 \
  --seconds 16 \
  --download \
  --variant video \
  --out coffee.mp4
```

## Create Character
```bash
uv run --with openai python "$SORA_CLI" create-character \
  --name Mossy \
  --video-file character.mp4
```

## Edit
```bash
uv run --with openai python "$SORA_CLI" edit \
  --id video_abc123 \
  --prompt "Same shot and camera move; shift palette to teal, sand, rust."
```

## Extend
```bash
uv run --with openai python "$SORA_CLI" extend \
  --id video_abc123 \
  --seconds 8 \
  --prompt "Continue as camera rises above rooftops revealing sunrise."
```

## Poll / Status / Download
```bash
uv run --with openai python "$SORA_CLI" poll --id video_abc123 --download --out out.mp4
uv run --with openai python "$SORA_CLI" status --id video_abc123
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant thumbnail --out thumb.webp
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant spritesheet --out sheet.jpg
```

## List / Delete
```bash
uv run --with openai python "$SORA_CLI" list --limit 20 --order asc
uv run --with openai python "$SORA_CLI" delete --id video_abc123
```

## Batch (Local Fan-Out)
```bash
cat > prompts.jsonl << 'EOF'
{"prompt":"Neon-lit rainy alley, slow dolly-in","seconds":"8"}
{"prompt":"Warm sunrise over misty lake, gentle pan","seconds":"8"}
EOF

uv run --with openai python "$SORA_CLI" create-batch \
  --input prompts.jsonl \
  --out-dir batch-output \
  --concurrency 3
```

**Note:** `create-batch` is a local concurrent helper, NOT the official Batch API.

## JSON Output (`--json-out`)
All commands support `--json-out <path>` to save API responses to a file.
- `create-and-poll` writes `{ "create": ..., "final": ... }`
- In `--dry-run` mode, writes the request preview
- Extension `.json` added automatically if omitted

## Prompt Augmentation Fields
| Flag | Maps to |
|------|---------|
| `--use-case` | Use case |
| `--scene` | Scene/background |
| `--subject` | Subject |
| `--action` | Action |
| `--camera` | Camera |
| `--style` | Style/format |
| `--lighting` | Lighting/mood |
| `--palette` | Color palette |
| `--audio` | Audio |
| `--dialogue` | Dialogue |
| `--text` | Text (verbatim) |
| `--timing` | Timing/beats |
| `--constraints` | Constraints |
| `--negative` | Avoid |

Use `--no-augment` to disable and pass raw prompts through.
