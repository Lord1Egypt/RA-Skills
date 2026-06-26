# gpt-image-2

An agent skill for the full **GPT Image 2** surface on any OpenAI-compatible gateway. One Python entrypoint covers `images/generations`, `images/edits`, and `responses` (with the `image_generation` tool), including streaming and partial-image previews.

Built for Codex, Claude, and other skill-aware agents, but the script also runs fine by hand.

## Features

- Three subcommands in one CLI: `generations`, `edits`, `responses`.
- Text-to-image, multi-image batches, mask edits, multi-reference edits, mixed text + image input.
- Streaming (SSE) with optional `partial_images` progressive previews.
- Strict pre-flight validation of GPT Image 2 constraints (size, aspect, pixel count, transparent background, `output_compression`, `stream` + `n`, and unsupported `response_format` usage on OpenAI GPT image models).
- Automatic base64 de-duplication and multi-image filename templating (`out-{index}.png`).
- Config via CLI flags, process environment, or `.env` — with a predictable override order.
- Zero third-party dependencies (standard library only).

## Requirements

- Python 3.10+
- An OpenAI-compatible endpoint that serves `gpt-image-2` (default: `https://api.openai.com/v1`).
- For `responses`, a text-capable Responses model such as `gpt-5.4` when using the hosted `image_generation` tool.
- `OPENAI_API_KEY`.

## Install

After publishing the repository, the recommended install path is through [Skills](https://skills.sh/):

```powershell
pnpm dlx skills add https://github.com/GargantuaX/openskills --skill gpt-image-2
```

Equivalent shorthand:

```powershell
pnpm dlx skills add GargantuaX/openskills@gpt-image-2
```

If you want the whole collection instead, install:

```powershell
pnpm dlx skills add GargantuaX/openskills
```

You can also drop the folder into your agent's skill directory, or clone/copy it anywhere and invoke the script directly.

Register with Codex by pointing at [agents/openai.yaml](./agents/openai.yaml). Claude-style agents can consume [SKILL.md](./SKILL.md) directly.

## Setup After skills.sh Install

1. Set credentials with environment variables, or create a `.env` in the working directory where you will run the script.
2. Start from the repository example [`.env.example`](../../.env.example), then adjust values for your endpoint and model defaults.
3. Run a `--dry-run` command first to confirm the final request shape before making live requests.

Minimal `.env`:

```dotenv
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_IMAGE_MODEL=gpt-image-2
OPENAI_RESPONSES_MODEL=gpt-5.4
OPENAI_IMAGE_SIZE=auto
OPENAI_IMAGE_QUALITY=high
OPENAI_IMAGE_FORMAT=webp
OPENAI_IMAGE_TIMEOUT=300
```

Dry-run check:

```powershell
python .\scripts\gpt_image.py responses `
  --input-text "Generate a poster for an AI tool launch" `
  --output .\out\poster.webp `
  --dry-run
```

## Quick start

```powershell
# 1. Configure credentials (either export or put in .env next to the script)
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"

# 2. Generate
python .\scripts\gpt_image.py generations `
  --prompt "A bold product hero image" `
  --output .\out\hero.webp
```

Built-in defaults now match the example `.env`: `size=auto`, `quality=high`, `format=webp`, `timeout=300`. For `responses`, the default top-level model is `gpt-5.4`; `OPENAI_IMAGE_MODEL` only applies to `generations` and `edits`.

See [SKILL.md](./SKILL.md) for the full command catalog, including multi-image batches, masked edits, and streaming Responses.

## Project layout

```
gpt-image-2/
├─ SKILL.md                  # Agent-facing entry point (workflow + examples + rules)
├─ README.md                 # You are here
├─ agents/
│  └─ openai.yaml            # Codex registration metadata
├─ references/
│  ├─ api-surface.md         # When to use generations vs edits vs responses
│  └─ config.md              # Environment variables and resolution order
└─ scripts/
   └─ gpt_image.py           # Single entrypoint, stdlib only
```

## Configuration

All options can be set via CLI flags, process environment variables, or a `.env` file. Full table and resolution rules in [references/config.md](./references/config.md).

## Runtime Notes

- `OPENAI_IMAGE_MODEL` controls `generations` and `edits`.
- `OPENAI_RESPONSES_MODEL` controls the top-level model for `responses`.
- `OPENAI_IMAGE_TOOL_MODEL` optionally overrides the hosted image model inside the `image_generation` tool.
- CLI flags override environment variables, and environment variables override `.env`.
- `.env` is resolved from the current working directory unless you pass `--env-file`.
- For OpenAI-hosted GPT image requests, omit `response_format`.

## Dry run

Add `--dry-run` to any command to print the exact request that would be sent (URL, headers, JSON payload, or multipart preview) without calling the API. Handy for agents that want to validate a plan before spending tokens or credits.

## Tests

Run the local regression tests with:

```powershell
python -m unittest discover -s .\skills\gpt-image-2\tests -p "test_*.py"
```

These tests stay offline and focus on argument validation plus `--dry-run` request shapes.

## Troubleshooting

- **`Missing OPENAI_API_KEY`** — set it in the environment or in `.env`.
- **`gpt-image-2 requires width and height to be multiples of 16`** — adjust `--size`.
- **`Public Images routes do not support stream=true with n>1`** — use `responses` instead, or drop `--n`.
- **`OpenAI GPT image models return base64 image data by default. Omit response_format.`** — remove `--response-format` for OpenAI-hosted GPT image requests.
- **`For responses with the image_generation tool, use a text-capable Responses model such as gpt-5.4`** — do not reuse `gpt-image-2` as the top-level `responses` model.
- **`output_compression is only valid with output_format jpeg or webp`** — set `--format jpeg` or `--format webp`.
- **`partial_images requires stream=true`** — add `--stream`.

## License

MIT. See the repository root [LICENSE](../../LICENSE).
