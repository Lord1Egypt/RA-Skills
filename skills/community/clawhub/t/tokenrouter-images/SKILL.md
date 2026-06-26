---
name: tokenrouter-image-generator
description: Generate or edit images through Palebluedot Ai(PBD)-TokenRouter's multimodal image generation endpoint (`/v1/chat/completions`) using TokenRouter-compatible image models. Use for text-to-image or image-to-image requests when the user wants TokenRouter, `PBD_TOKENROUTER_API_KEY`, model overrides, or provider-specific `image_config` options.
---

# TokenRouter Image Generation & Editing

Generate new images or edit existing ones using TokenRouter image-capable models via the Chat Completions API.

## Usage

Run the script using absolute path (do NOT cd to the skill directory first):

**Generate new image:**
```bash
# Ensure outbound directory exists first
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/pbd-tokenrouter-image-generator/scripts/generate_image.py \
  --prompt "your image description" \
  --filename "~/.openclaw/media/outbound/output-name.png" \
  --model google/gemini-2.5-flash-image \
  [--aspect-ratio 16:9] \
  [--image-size 2K]
```

**Edit existing image (image-to-image):**
```bash
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/pbd-tokenrouter-image-generator/scripts/generate_image.py \
  --prompt "editing instructions" \
  --filename "~/.openclaw/media/outbound/output-name.png" \
  --input-image "path/to/input.png" \
  --model google/gemini-2.5-flash-image
```

**Important:** Default OpenClaw delivery path is `~/.openclaw/media/outbound/`. Save generated images there so other OpenClaw flows can pick them up easily.

## API Key

The script requires a TokenRouter API key. Check for it in this order:
1. `--api-key` argument
2. `PBD_TOKENROUTER_API_KEY` environment variable
3. **Auto-detect** from the current agent's tokenrouter provider config in `~/.openclaw/openclaw.json`

### If no API key is found

**Before running the script**, check whether the key is available:

```bash
test -n "$PBD_TOKENROUTER_API_KEY" && echo "Key found" || echo "No key"
```

If none of the above sources provides a key, **do NOT run the script**. Instead, guide the user through obtaining a key:

1. Tell the user they need a TokenRouter API key.
2. Direct them to open: **https://www.tokenrouter.com**
3. Walk them through the steps:
   - Register or sign in on the website
   - After login, navigate to the **API Keys** section
   - Find the **API Keys** menu in the sidebar/navigation
   - Click **API Keys** to enter the key management page
   - Create a new API key and copy it
4. Once the user has the key, offer two options:
   - **Option A — Provide the key directly to the agent:** The user can paste the key in the chat, and the agent passes it to the script via `--api-key`. This is the quickest way to get started — no environment setup needed.
   - **Option B — Configure as environment variable (persistent):**
     - **For this session only:** `export PBD_TOKENROUTER_API_KEY="sk-xxx..."` (paste in terminal)
     - **Persistent (zsh):** Add the export line to `~/.zshrc` then `source ~/.zshrc`
     - **Persistent (bash):** Add the export line to `~/.bashrc` then `source ~/.bashrc`
5. After the key is available, proceed with the image generation command.

**Important:** Never skip this check. Running without a valid key will fail with `Error: No API key provided` or `HTTP 401/403`.

### Optional attribution headers(optional)
- `--site-url` or `PBD_TOKENROUTER_SITE_URL`
- `--app-name` or `PBD_TOKENROUTER_APP_NAME`

## Model + Image Config

- `--model <tokenrouter-model-id>` is required (no script default)
- **Default / recommended:** `google/gemini-2.5-flash-image`
- **Other supported image models** (user can request a switch):
  - `openai/gpt-5-image`
  - `openai/gpt-5-image-mini`
  - `google/gemini-3-pro-image-preview`
  - `google/gemini-3.1-flash-image-preview`
- Use `--aspect-ratio` for `image_config.aspect_ratio` (for example `1:1`, `16:9`)
- Use `--image-size` for `image_config.image_size` (`1K`, `2K`, `4K`)

Note: TokenRouter docs show `aspect_ratio` and `image_size` as the common image config fields for image generation. Additional keys may exist for specific providers/models (for example Sourceful features). If a request fails, remove unsupported options or switch models.

Note: The script always sends `modalities: ["image", "text"]`. Image-only models (some FLUX variants) may reject this — if you get an unexpected error with a non-Gemini model, this may be the cause. No workaround is currently exposed via CLI args.

## Default Workflow (draft -> iterate -> final)

Goal: iterate quickly before spending time on higher-quality settings.

- Draft: smaller size / faster model
  - `--image-size 1K`
- Iterate: adjust prompt in small diffs and keep a new filename each run
- Final: larger size or higher quality if the selected model supports it
  - Example: `--image-size 4K --aspect-ratio 16:9`

## Preflight + Common Failures

- Preflight:
  - `command -v uv`
  - **API key check (CRITICAL):** The script will try `--api-key`, then `PBD_TOKENROUTER_API_KEY`, then auto-read from `~/.openclaw/openclaw.json` (tokenrouter provider). If all fail, **STOP** and guide the user to https://www.tokenrouter.com to register and get a TokenRouter API key (see "If no API key is found" section above)
  - `test -d ~/.openclaw/media/outbound || mkdir -p ~/.openclaw/media/outbound`
  - If editing: `test -f "path/to/input.png"`

- Common failures:
  - `Error: No API key provided.` -> The script could not find a key from `--api-key`, `PBD_TOKENROUTER_API_KEY`, or `~/.openclaw/openclaw.json`. Guide the user to https://www.tokenrouter.com to register and obtain a free TokenRouter API key, then set `PBD_TOKENROUTER_API_KEY` or pass `--api-key`
  - `Error loading input image:` -> bad path or unreadable file
  - `HTTP 400` with model/image config error -> unsupported model or invalid `image_config.aspect_ratio` / `image_config.image_size`
  - `HTTP 401/403` -> invalid key, no model access, or quota/credits issue
  - `No image found in response` -> model may not support image output or request format rejected

## Filename Generation

Generate filenames with the pattern: `~/.openclaw/media/outbound/yyyy-mm-dd-hh-mm-ss-name.png`

Examples:
- `~/.openclaw/media/outbound/2026-03-21-10-00-00-example.png`

## Prompt Handling

- For generation: pass the user's description as-is unless it is too vague to be actionable.
- For editing: make the requested change explicit and preserve everything else.

Prompt template for precise edits:
- `Change ONLY: <change>. Keep identical: subject, composition/crop, pose, lighting, color palette, background, text, and overall style. Do not add new objects.`

## Output

- Save the first returned image to `~/.openclaw/media/outbound/output-name.png` by default (pass that full path in `--filename`)
- Supports TokenRouter's base64 data URL image responses (`message.images[0].image_url.url`)
- Prints the saved file path
- Do not read the image back unless the user asks

## Examples

**Generate new image:**
```bash
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/pbd-tokenrouter-image-generator/scripts/generate_image.py \
  --prompt "A field photo with a Japanese-style healing anime aesthetic." \
  --filename "~/.openclaw/media/outbound/2026-03-21-10-00-00-healing.png" \
  --model google/gemini-2.5-flash-image \
  --aspect-ratio 16:9 \
  --image-size 2K
```

**Edit existing image:**
```bash
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/pbd-tokenrouter-image-generator/scripts/generate_image.py \
  --prompt "Beautify the photo with a whitening filter." \
  --filename "~/.openclaw/media/outbound/2026-02-26-14-25-30-sunset-sky-edit.png" \
  --model google/gemini-2.5-flash-image \
  --input-image "self-photo.jpg"
```

## Reference

- TokenRouter docs: https://www.tokenrouter.com/docs
