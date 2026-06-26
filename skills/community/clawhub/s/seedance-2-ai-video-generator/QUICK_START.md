# Quick Start – Seedance 2.0 Video Generator

Generate AI videos from text prompts or images using the Loova Seedance 2.0 API. **Video generation can take up to 3 hours**; the script will poll until the task completes and prints a notice at start.

## 1. Get your API key

1. Open [https://loova.ai/api](https://loova.ai/api) and log in.
2. Get your API key from the Loova API page in your Loova account.
3. Create a `.env` file in the project root (or next to the script):

```bash
# Copy from example
cp .env.example .env
# Edit .env and set:
LOOVA_API_KEY=your_api_key_here
```

Or set the variable in your shell:

```bash
export LOOVA_API_KEY="your_api_key_here"
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run your first video

**Text prompt only (no input image):**

```bash
python scripts/run_seedance.py --prompt "Camera slowly pushes in, person smiles"
```

**With optional parameters:**

```bash
python scripts/run_seedance.py --prompt "A cat walking in the sun" --duration 8 --ratio "16:9"
```

**With local image file(s):**

```bash
python scripts/run_seedance.py --prompt "Person turns head" --files "photo.jpg"
```

The script submits the job, polls until the video is ready, and prints the result JSON (including the video URL when succeeded).

## Scripts reference

| Script | Description |
|--------|-------------|
| `scripts/run_seedance.py` | Submit Seedance 2.0 video job and poll for result (prompt, optional images, duration, ratio) |

## Parameters

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--prompt` | Yes | — | Text prompt for the video |
| `--model` | No | `seedance_2_0` | `seedance_2_0` or `seedance_2_0_fast` |
| `--duration` | No | `5` | Duration in seconds (4–15) |
| `--ratio` | No | `16:9` | Aspect ratio |
| `--function-mode` | No | — | `first_last_frames` or `omni_reference` |
| `--files` | No | — | Comma-separated local file paths (sent as FormData File uploads; images/video/audio) |

For full API details, see [reference.md](reference.md). For ClawHub/OpenClaw usage, see [SKILL.md](SKILL.md).
