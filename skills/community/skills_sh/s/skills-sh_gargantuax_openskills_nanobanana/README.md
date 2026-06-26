# nanobanana

An agent skill for Gemini-native **Nano Banana** image generation and editing, covering the current three-tier lineup:

- **Nano Banana**: `gemini-2.5-flash-image`
- **Nano Banana 2**: `gemini-3.1-flash-image-preview`
- **Nano Banana Pro**: `gemini-3-pro-image-preview`

Built in the same style as this repository's `gpt-image-2` skill: one Python CLI, offline validation, `.env` support, and agent-friendly dry runs.

## Features

- One CLI with two subcommands: `generate` and `batch`.
- Text-to-image, image-to-image edits, and multi-reference image inputs.
- Custom Gemini-compatible base URL support for self-hosted or gateway deployments.
- Model aliases for `nanobanana`, `nanobanana-2`, and `nanobanana-pro`.
- Strict pre-flight validation for model-specific `aspect_ratio` and `image_size` support.
- Config via CLI flags, process environment, or `.env`, with a predictable override order.
- Zero third-party dependencies.

## Requirements

- Python 3.10+
- A Gemini-compatible `generateContent` endpoint
- `GEMINI_API_KEY`

## Install

After publishing the repository, the recommended install path is through [Skills](https://skills.sh/):

```powershell
pnpm dlx skills add https://github.com/GargantuaX/openskills --skill nanobanana
```

Equivalent shorthand:

```powershell
pnpm dlx skills add GargantuaX/openskills@nanobanana
```

If you want the whole collection instead, install:

```powershell
pnpm dlx skills add GargantuaX/openskills
```

You can also clone or copy the folder and run the script directly.

Register with Codex by pointing at [agents/openai.yaml](./agents/openai.yaml). Skill-aware agents can consume [SKILL.md](./SKILL.md) directly.

## Setup After skills.sh Install

1. Set credentials with environment variables, or create a `.env` in the working directory where you will run the script.
2. Start from the repository example [`.env.example`](../../.env.example), then adjust the Nano Banana section for your endpoint and model defaults.
3. Run a `--dry-run` command first to confirm the final request shape before making live API calls.

Minimal `.env`:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_MODEL=nanobanana-2
GEMINI_TIMEOUT=300
GEMINI_ASPECT_RATIO=16:9
GEMINI_IMAGE_SIZE=2K
```

Dry-run check:

```powershell
python .\scripts\nanobanana.py generate `
  --prompt "A launch poster for an AI developer tool" `
  --output .\out\poster.png `
  --dry-run
```

## Quick Start

```powershell
# 1. Configure credentials
$env:GEMINI_API_KEY = "..."
$env:GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# 2. Generate
python .\scripts\nanobanana.py generate `
  --prompt "A bold product hero image" `
  --output .\out\hero.png `
  --model nanobanana-2 `
  --ratio 16:9 `
  --size 2K
```

If you run against a custom gateway, point `GEMINI_BASE_URL` at a Gemini-compatible root such as `http://your-gateway.example.com/v1beta`. If the gateway expects bearer auth instead of `x-goog-api-key`, set `GEMINI_AUTH_MODE=bearer`.

## Project Layout

```text
nanobanana/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ config.md
│  └─ models-and-api.md
├─ scripts/
│  └─ nanobanana.py
└─ tests/
   └─ test_nanobanana.py
```

## Tests

Run the offline regression tests with:

```powershell
python -m unittest discover -s .\skills\nanobanana\tests -p "test_*.py"
```

## License

MIT. See the repository root [LICENSE](../../LICENSE).
