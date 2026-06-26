---
name: visual-references
description: "Search and download visual reference images from Pexels to inspire image or video generation. Use when you need style references, mood boards, composition or color palette inspiration before generating an asset."
metadata: {"clawdbot":{"emoji":"🖼️","requires":{"bins":["python3"],"pip":["requests"],"env":["PEXELS_API_KEY"]}}}
---

# Visual References (Pexels)

Download visual references from Pexels to inspect style, mood, and composition before generating.

## When to use

**Use when:**
- The brief mentions a specific style, mood, palette, or visual reference ("I want something minimalist", "editorial style", "something like X")
- The client wants aesthetic coherence with something real or existing
- The brief is visually vague and searching references would improve the result

**Don't use when:**
- The brief is straightforward with no visual ambiguity (colors, text, and layout already defined)
- You already have references in `input_images`
- It's a minor edit of a previously delivered image
- The brief doesn't mention style and the image is functional/technical

## Prerequisites

Requires the `PEXELS_API_KEY` environment variable (free Pexels API key). The script will fail if the key is not configured. Get one at https://pexels.com/api.

## Basic usage

```bash
python3 ~/.openclaw/workspace/skills/visual-references/scripts/visual_ref.py "QUERY" [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--count N` | 5 | Number of images |
| `--output DIR` | `/tmp/visual-refs` | Output folder |
| `--orientation` | — | `landscape`, `portrait`, `square` |
| `--list-only` | — | List URLs only, no download |

### Output directory rule (MANDATORY)

**ALWAYS use `--output /tmp/visual-refs` as the output directory.** Do NOT invent unique folder names like `visual-refs-salon-v2`, `visual-refs-v3`, etc. The script automatically cleans the output folder before each search, so using the same folder every time is safe and prevents accumulation of old references.

### Examples

```bash
# References for a real estate hero image
python3 visual_ref.py "luxury real estate minimalist nordic" --count 5 --orientation landscape --output /tmp/visual-refs

# Square thumbnails for social media
python3 visual_ref.py "personal branding outdoor golden hour" --count 5 --orientation square --output /tmp/visual-refs

# List only, no download
python3 visual_ref.py "product photography white background" --list-only
```

## IMPORTANT: Usage limits

- **Maximum 3 searches per task.** One main query, up to two refinements. Do NOT run dozens of searches looking for the perfect reference.
- Use `--count 5` (not 5) to keep it fast.
- Pick the best reference from what you get and move on to generation. The references are inspiration, not the final product.

## Workflow when you decide to use it

1. **Receive brief** with vague style or mentioned inspiration
2. **Translate query to English** — Pexels works best in English
3. **Run ONE search** with `--count 5`
4. **Do NOT review or pick** — pass ALL 3 references directly to generate_image
5. **Generate with ALL references as input_images** (MANDATORY):
   ```
   generate_image(
     prompt: "description of the NEW asset to generate (subject, scene, format) — do NOT describe the references, the model sees them",
     input_images: ["/path/to/ref_01_xxx.jpg", "/path/to/ref_02_xxx.jpg", "/path/to/ref_03_xxx.jpg"],
     ...
   )
   ```
   The generation model sees all references and picks the best style elements. Your prompt describes WHAT to create, not the style — the style comes from the reference images.

**IMPORTANT:** Do NOT waste tokens reviewing references with `read`. Do NOT pick a favorite. Pass all downloaded references as `input_images` and let the generation model decide.

## Alternative: user picks references (only when requested)

If the brief explicitly asks to see references first ("enséñame referencias", "muéstrame antes de generar", "quiero elegir yo"), use this flow instead:

1. Search and download references as usual
2. Send ALL reference images in a SINGLE message via `sessions_send`:
   ```
   sessions_send(sessionKey="<REPLY_TO>", message="5 referencias de salón editorial:\n\nArchivo: /tmp/visual-refs/ref_01_xxx.jpg\nArchivo: /tmp/visual-refs/ref_02_xxx.jpg\nArchivo: /tmp/visual-refs/ref_03_xxx.jpg\nArchivo: /tmp/visual-refs/ref_04_xxx.jpg\nArchivo: /tmp/visual-refs/ref_05_xxx.jpg\n\n¿Cuál te gusta? Puedo usar una, mezclar varias, o buscar otras.", timeoutSeconds=0)
   ```
3. **Wait for user response** before generating
4. Generate with the references the user chose as `input_images`

**CRITICAL: Send references EXACTLY ONCE.** Do NOT send them individually AND again in a summary. Do NOT re-send references you already sent. One single message with all file paths, that's it.

Only use this alternative flow when the user EXPLICITLY asks to see references first. Default is always: search → pass all → generate.

## Script output

- Images downloaded to `--output` as `ref_01_<id>.jpg`, `ref_02_<id>.jpg`...
- `refs_meta.json` with metadata: path, description, author
- Attribution printed to stdout (required by Pexels guidelines)

## Limits

- Demo plan: 50 requests/hour — more than enough for creative use
- Downloaded resolution: ~1080px (regular) — optimal for visual reference
- Attribution: required for public apps, not for internal/creative use

## Effective queries

- Always in English — better results
- Be specific: `"hero shot luxury car black studio"` > `"car"`
- Include mood: `"cozy home interior warm light bokeh"`, `"cold corporate office minimal"`
- By sector: `"restaurant food flat lay"`, `"fashion editorial outdoor"`, `"tech startup office"`
