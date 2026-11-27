# Tools and APIs

Confidence: **verified** (read from the provider's page in Nov 2026), **not verified** (listed by the user or from general knowledge; the page was not checked in this session). Confirm pricing, limits and licence terms on the provider's site before relying on them. Not legal advice.

## Built into this skill

| Tool | Role | Status |
|---|---|---|
| Pillow | all composition, effects, checks, export | scripts tested with generated images |
| Pexels API | free stock photos (`thumb_assets.py search`) | verified: 200 requests/hour, 20,000/month, credit the creator/Pexels when possible |
| Pixabay API | free stock photos (`--source pixabay`) | verified: 100 requests/60 s, cache 24 h, no bulk downloading; photo downloads from this script top out near 1280 px |
| rembg (local) | free background removal, `pip install "rembg[cpu]"` | not verified here; default engine for cutouts |
| remove.bg API | background removal (`--engine removebg`) | verified: `POST https://api.remove.bg/v1.0/removebg`, header `X-Api-Key`, first 50 API calls per month free. **remove.bg says its standalone website closes on 1 Dec 2026 and background removal moves to Canva and Leonardo.ai; check what that means for the API before depending on it.** |
| OpenAI Image API | optional AI backgrounds/objects (`ai-image`) | verified: image generations endpoint, base64 in `data[0].b64_json`, model names change (docs showed `gpt-image-2.5-*` and `2.6` references), may need organization verification. The script takes the model name from `--model` or `THUMB_IMAGE_MODEL` and does not guess it. Sizes: pass what the docs allow; `1536x1024` is the default but not confirmed in this session. Billed per image. |

## Manual or not scripted

| Tool | Use | Status |
|---|---|---|
| Photopea, GIMP | hand editing, fixing cutout edges, layers | free; suggest for finishing |
| Canva / Canva Pro | templates, brand kits, manual design | verified: the Connect Autofill API needs a plan that includes Autofill (Pro, Teams or Enterprise), MFA on the account, a published brand template with tagged data fields, and image fields accept only uploaded assets by `asset_id` (external URLs are not accepted directly); exports go through a separate export-job API. Not scripted here; use only if the user already works in Canva. |
| Ideogram | AI images with better text rendering | not verified; user generates in the app, then composes here |
| Midjourney, Leonardo AI | premium AI visuals | not verified; use the apps; check each tool's terms for commercial use |
| Photoroom, Clipdrop, Stability AI, Replicate | cutouts, cleanup, other models | not verified; no script provided. If the user wants one, ask for the docs link or check them first |
| Magnific, other AI upscalers | real detail upscaling | not verified; `thumb_assets.py upscale` is plain resampling only |
| Adobe Photoshop | professional compositing | paid; use the cutout PNGs and background from this workflow |

## Choosing

1. No budget: own photos + Pexels/Pixabay + rembg + Pillow + Photopea for touch-ups.
2. Need custom visuals: add an AI generator for backgrounds or objects (no text, no real people), compose text here.
3. Team with brand templates in Canva: consider Canva autofill if their plan and an approved integration allow it; otherwise use this skill's output as the base.

## Licensing notes

- Stock photos: keep `attribution.json`; credit as the source asks. Pixabay and Pexels photos of people can still raise likeness or implied-endorsement issues; avoid recognisable people in misleading contexts.
- AI images: check the tool's current terms on commercial use and ownership. Do not generate likenesses of real people or copyrighted characters.
- Fonts and icons: use ones whose licence allows commercial use.
- The user's own photos: confirm they hold the rights and the consent of anyone else in them.
