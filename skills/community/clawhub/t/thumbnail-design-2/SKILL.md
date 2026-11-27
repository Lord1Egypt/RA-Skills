---
name: thumbnail-design
description: Design professional, high-clarity YouTube thumbnails (1280x720 videos, 9:16 Shorts covers) from a video title, script or topic. Produces 3 to 5 distinct concepts, builds the images (own photos, free stock, optional AI images, background removal), composes text, subject and effects with Pillow, makes variations, checks readability and file limits, and exports final JPG/PNG. Use this skill whenever the user asks for a thumbnail, thumbnail ideas, a thumbnail redesign, a Shorts cover, CTR-focused visuals, or says things like "make a thumbnail", "thumbnail for this video", "give me thumbnail concepts", even if they only paste a title or script.
---

# Thumbnail design

Goal: from a title, script or topic, deliver thumbnail concepts and finished, export-ready images that are clear at feed size, honest about the video, and on-brand. Replies follow the user's language preference; file contents and commands stay in English.

## What to say up front (briefly)

No tool or design can guarantee a click-through rate. The rules here are widely used design heuristics, not measured laws, and the scripts check legibility and file rules, not performance. The only real test is the user's own analytics: compare thumbnails on the same video, or across similar videos, and keep what wins. Say this in one sentence, then get to work.

## Workflow

1. **Intake.** Title, script or topic; channel niche and audience; brand (colours, fonts, logo, face or mascot); the creator's own photos (with expressions) if a face is wanted; platform (video 16:9 or Shorts 9:16); API keys or tools they have. Ask only for what is missing; if nothing is given, proceed with sensible defaults and state them.
2. **Topic analysis.** Write the video's one promise, the viewer's emotion (curiosity, fear, desire, surprise), the "gap" (what they will want to find out), and the one visual that carries it. The thumbnail should complement the title, not repeat it. Read `references/design-principles.md`.
3. **Niche check (optional but valuable).** Look at what already ranks: use the YouTube search skill/script if available (`viral-content-research`), or the user's reference links, then `python scripts/thumb_assets.py competitors IDS --out research/` to compare colours, brightness and layout. This is for study; the output must be a different, original direction. The sandbox may block downloads; if so say it and work from the user's references.
4. **Concepts.** Write 3 to 5 genuinely different concepts (different focal subject, layout, colour mood), each with: one-line idea, subject and expression, text (1 to 4 words), colours, layout, asset needs, and why it might work. Use the template in `references/workflow-and-concepts.md`. Offer a recommendation.
5. **Assets.** In order of preference: the user's own photos or footage frames; free stock (`thumb_assets.py search`); AI-generated backgrounds or objects (`thumb_assets.py prompt` to write the prompt, then the user's generator or `ai-image`); cut subjects out with `thumb_assets.py cutout` (local rembg first). Record attribution. Never use a real person's likeness without their consent, and never use celebrities or public figures. See `references/tools-and-apis.md`.
6. **Compose.** Write a spec JSON per concept and render: `python scripts/thumb_compose.py render spec.json`. Then `variants` for text, theme and left-right flips, which also makes a contact sheet.
7. **Check.** `python scripts/thumb_check.py out/thumb.jpg --preview out/prev` checks format, ratio, size, brightness, contrast, text size at feed size, margins, the duration-badge corner and text-vs-subject overlap. Look at the small preview yourself; fix every FAIL and each WARN that is real.
8. **Export.** JPG for photos (under 2 MB by default), PNG when sharp text and flat colour matter. Resize for other targets with `resize` only as a last resort; a re-laid-out spec is better than cropping.
9. **Deliver.** Send the final image(s) and the variants sheet with SendUserFile, plus a short note: which concept is recommended and why, text used, assets and credits, and an A/B plan (what to compare, how long, which metric). Keep spec files so edits are quick.

## Commands

```bash
python scripts/thumb_compose.py render SPEC.json [--out PATH]
python scripts/thumb_compose.py variants SPEC.json --texts "A|B|C" --themes dark,bright,warm,cool [--flip] [--max 6]
python scripts/thumb_compose.py resize IMAGE --to youtube|youtube_hd|shorts|WxH [--focus 0.5,0.5]
python scripts/thumb_compose.py sheet IMG [IMG ...] --out sheet.jpg
python scripts/thumb_check.py IMAGE [--layout IMAGE.layout.json] [--preview DIR] [--json out.json]
python scripts/thumb_assets.py search "query" --out assets [--source auto|pexels|pixabay]   # auto: Pexels if its key is set, else Pixabay
python scripts/thumb_assets.py cutout IMAGE [--engine rembg|removebg]
python scripts/thumb_assets.py ai-image "prompt" --out assets/bg.png --model MODEL [--size 1536x1024]
python scripts/thumb_assets.py prompt --subject "..." [--emotion ..] [--setting ..] [--palette ..]
python scripts/thumb_assets.py upscale IMAGE --factor 2
python scripts/thumb_assets.py competitors IDS_OR_FILES... --out research
```

Pillow is required (`pip install pillow`). Keys come from environment variables only (`PEXELS_API_KEY`, `PIXABAY_API_KEY`, `REMOVEBG_API_KEY`, `OPENAI_API_KEY`, `THUMB_IMAGE_MODEL`); never write a key into a file or the chat. The spec format is documented at the top of `thumb_compose.py` and in `references/workflow-and-concepts.md`.

## Rules

- Honest thumbnails: the image must show something the video delivers. No fake play buttons, fake UI, fake news banners, fake before/after, or text that promises what is not in the video. YouTube can reject thumbnails that break the Community Guidelines and can restrict thumbnail privileges after strikes.
- Original work: use references for direction only. Do not copy, trace or lightly edit another creator's thumbnail, and do not use logos or brand assets the user does not own.
- People: use the user's own photos, or stock photos whose licence allows it; for stock people, avoid implying endorsement. No celebrity or public-figure images, and no AI faces of real individuals.
- Text: 1 to 4 words usually, large, high contrast, not a copy of the title. AI image tools often misspell text, so add text with `thumb_compose.py` unless the tool is known for reliable text and the result is checked letter by letter.
- Keep key content away from the bottom-right corner (duration badge) and the edges.
- Report only what was verified: the scripts were tested with generated test images; live API calls (stock search, AI image, background-removal services) were not tested here. If a live call fails, show the error and adjust.

## References

- `references/design-principles.md`: composition, text, colour, faces, niche patterns, Shorts, testing. Read before concepts.
- `references/workflow-and-concepts.md`: concept template, spec examples, prompt writing, brand kit, deliverable layout.
- `references/tools-and-apis.md`: what each recommended tool and API does, what was verified, limits and plan requirements.
- `references/specs-and-policy.md`: YouTube thumbnail specs and policy points.
