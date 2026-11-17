---
name: wavespeed
description: Generate or edit AI media (image, video, audio, 3D) by calling the wavespeed CLI on the user's machine. Use whenever the user asks to create, edit, animate, upscale, or transform a visual asset, generate audio/TTS/music, or produce marketing creatives. Every model on the WaveSpeed platform is one `wavespeed run <id>` call.
---

# WaveSpeed

You have access to the `wavespeed` CLI. Every generation flows through one verb. There are no image / video shortcuts; the model id is always explicit.

## The four-step pattern

### 1. FIND a model — search the live catalog

```bash
wavespeed models "nano banana"
wavespeed models --type image-to-video --popular
wavespeed models --type image-to-image       # all models + prices, sorted by type
```

**Price recon**: Omit `--popular` to see the full list with per-run prices. Pipe through `sort` or scan manually for budget decisions. `--type` supports: `text-to-image`, `image-to-image`, `text-to-video`, `image-to-video`, `audio-generation`, `video-generation`, `3d-generation`, `llm`.

### 2. INSPECT its inputs — dynamic schema, per model

```bash
wavespeed run google/nano-banana-2/text-to-image -h
```

### 3. CONFIRM with the user before running

Present the planned model, prompt, and any key parameters (e.g. aspect ratio, resolution, duration, input image URL) to the user in a clear summary. Ask explicitly: "Shall I proceed?" Wait for their go-ahead before executing.

### 4. RUN it — always pass --json so you can read the result

```bash
wavespeed run google/nano-banana-2/text-to-image \
  -p "a cyberpunk skyline at golden hour" \
  -i aspect_ratio="16:9" -i resolution="2k" --json
```

`run --json` returns `{ model, prompt, outputs: [url, ...], saved: [path, ...], elapsed_ms, raw }`. Use the URL when the user wants a link. Add `--download` if they need bytes on disk.

> **Resolution reminder:** If the user didn't specify an image resolution or video quality, apply the defaults from the [Resolution defaults](#resolution-defaults) section — don't ask unless it matters to their use case.

## Recommended defaults

| Use case | Model | Price |
|---|---|---|
| Text → image (默认) | `openai/gpt-image-2/text-to-image` | — |
| Image edit / 图生图 (默认) | `openai/gpt-image-2/edit` | — |
| Text → video (默认) | `bytedance/seedance-2.0/text-to-video` | — |
| Image → video (默认) | `bytedance/seedance-2.0/image-to-video` | — |
| Text → image (budget) | `google/nano-banana-2/text-to-image` | $0.07 |
| Image edit (style/quality) | `google/nano-banana-2/edit` — aspect_ratio supported, ~23s | $0.07 |
| Image edit (best value) | `bytedance/seedream-v4.5/edit` — strong prompt adherence, ~28s | $0.04 |
| Image edit (budget) | `wavespeed-ai/flux-2-flash/edit` — fast, decent quality, ~10-20s | $0.013 |
| Image edit (bilingual CJK/EN) | `wavespeed-ai/qwen-image/edit` — Chinese+English prompts | $0.02 |

**Completion time varies dramatically by model** — always check expected duration. Nano Banana ~23s, Seedream ~28s, GPT Image 2 ~145s. Use background mode for slow models.

Browse alternatives with `wavespeed models <query>`.

## Resolution defaults

When the user doesn't specify a resolution, apply these sensible defaults:

| Use case | Default | How to pass it |
|---|---|---|
| Text → image / 文生图 | **1K** (1024×1024 or closest) | `-i aspect_ratio="1:1"` or `-i size="1024x1024"` (check `-h` for which param the model uses) |
| Image edit | **1K** (same as above) | Same — some models use `aspect_ratio`, others `size`. Always `-h` first. |
| Text → video | **480p** (854×480) | `-i width=854 -i height=480` or `-i resolution="480p"` (check `-h`) |
| Image → video | **480p** (854×480) | Same — some models accept `width`/`height`, others a single `resolution` string |

> **Resolution tiers (common):** 1K = 1024×1024 / 1024×768 / 768×1344 (depends on aspect ratio), 2K = 2048×2048, 4K = 4096×4096. For video: 480p = 854×480, 720p = 1280×720, 1080p = 1920×1080. Always verify the exact parameter names with `-h`.

## Choosing the right edit model

When you need specific output parameters, **inspect each candidate with `-h`** — they vary widely:

| Need | Check | Example that supports it |
|---|---|---|
| Native aspect ratio (3:4, 4:5, etc.) | Look for `aspect_ratio` parameter | `google/nano-banana-2/edit` ✓ |
| Pixel size override | Look for `size` parameter | `wavespeed-ai/flux-2-dev/edit` ✓ |
| Multi-image input | `images[]` (array) vs `image` (single string) | Nano Banana: `images[]`; Qwen: `image` |
| Chinese + English bilingual | Model description mentions bilingual | `wavespeed-ai/qwen-image/edit` ✓ |
| Budget | Compare per-run price in `wavespeed models` output | Z-Image-Turbo: $0.005 — Flux.2 Flash: $0.013 — Qwen Edit: $0.02 |

Call `wavespeed run <model-id> -h` to see exactly what params the model accepts before running.

### Edit an existing image — upload first, then pass the URL

```bash
URL=$(wavespeed upload ./input.jpg --json | jq -r .url)
wavespeed run google/nano-banana-2/edit \
  -p "replace the background with a sunlit kitchen" \
  -i images="[\"$URL\"]" --json
```

### Image-to-video — same pattern

```bash
URL=$(wavespeed upload ./hero.jpg --json | jq -r .url)
wavespeed run bytedance/seedance-2.0/image-to-video \
  -p "subtle parallax, gentle wind" \
  -i image="$URL" -i duration=5 --json
```

### Save outputs locally with a template

```bash
wavespeed run ... -p "..." --download "./out/{index}.{ext}"
```

## Project config and aliases

If `wavespeed.json` exists (created by `wavespeed init`):

- **`defaultModel`** — lets `wavespeed run -p "…"` (no model arg) work.
- **Aliases** — named shortcuts that bundle model + default inputs. Run `wavespeed aliases` to see what's defined. `wavespeed run <alias> -h` shows the resolved schema. CLI `-i k=v` overrides alias defaults.

The CLI never modifies the user's prompt or inputs. What you typed is what hits the API.

## Installation

```bash
npm install -g @wavespeed/cli    # global install (may need sudo/nvm)
npx @wavespeed/cli <cmd>         # drop-in, no install needed
```

The npm package name is **`@wavespeed/cli`**, not `wavespeed`. If global install fails due to permissions, `npx @wavespeed/cli` works identically as a drop-in replacement for all subcommands (just prefix every call with `npx @wavespeed/cli` instead of `wavespeed`).

## Auth

`wavespeed status` shows whether the user is signed in. If not:

**Get your API key** at **[https://wavespeed.ai/accesskey](https://wavespeed.ai/accesskey)** — log in with your WaveSpeed account and copy the key from that page.

Then run `wavespeed login` to authenticate:

```bash
wavespeed login                    # opens browser to https://wavespeed.ai/accesskey
```

**If the user pastes a key into chat manually** (e.g. `wsk_live_XXXXXX`), save it with `--api-key`:

```bash
wavespeed login --api-key "wsk_live_XXXXXX"
# or via npx:
npx @wavespeed/cli login --api-key "wsk_live_XXXXXX"
```

## Pitfalls

- **Local file paths don't auto-upload** — call `wavespeed upload` first to get a CDN URL.
- **Don't invent model IDs.** Always confirm via `wavespeed models` or `wavespeed schema <id>` before running.
- **Use `--json` on every run** so you can read `outputs[0]` programmatically.
- **Same-type models can have different parameter names.** `images[]` (array) vs `image` (single string) is the most common trap. Some models use `aspect_ratio`, others use `size` (pixels). Always `-h` each candidate.
- **Vision model may not support image URLs.** If `vision_analyze` or `browser_vision` fails to describe the reference image, rely on the user's verbal description and proceed with upload → run directly — the edit model itself handles the visual reference.
- **Complex prompts with double quotes break bash inline strings.** Prompts containing speech bubbles or quoted text (e.g. `"What do you like?"`) inside `-i prompt='...'` cause parse failures or silent rejections. **Fix:** write the prompt to a file and read it with `PROMPT=$(cat /path/to/prompt.txt)` then reference `"$PROMPT"` in the command.
- **Some models reject complex prompts with in-image text.** Not all image-to-image models render speech bubbles or embedded text well — they may silently omit or garble them. If text is critical, prefer `google/nano-banana-2/edit` or `bytedance/seedream-v4.5/edit`.
- **Timeouts on slow models.** `openai/gpt-image-2/edit` can take 145s+ to complete, exceeding default 120s timeout. **Fix:** run these in background mode with `notify_on_complete=true` and a timeout of 600s.
- **`--download` to a directory path fails with EISDIR.** Use `--download ./out/{index}.{ext}` (a file template pattern), not `--download ./out/` (a directory).