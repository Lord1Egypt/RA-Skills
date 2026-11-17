---
name: text-in-image
description: >
  Generate images where the copy has to be exactly right: posters, packaging, ads, social
  graphics, UI mockups, menus, signage, infographics. Use when the user says "put the text X on
  it", "a poster that reads ...", "a label with the brand name", "make the headline say ...", "an
  ad with this tagline", or any design where a misspelled or paraphrased word is a failure. The
  thing most image models get wrong, so reach for this whenever exact lettering matters, even if
  the user just says "a poster" or "a label". For scalable vector output like a logo or SVG icon,
  use logos-and-vectors instead.
---

# Text in image

Produce an image where specific words must render correctly, in the right place, in the right style. The lever is quoting the exact copy so the model treats it as literal content instead of paraphrasable scene description, then directing placement and typographic treatment. Most image models read letters as visual texture and garble them. The models below are the ones that actually render legible, spelled-correct text.

## Inputs to collect

- **The exact copy.** The verbatim string(s) the image must show, including apostrophes, accents, prices, dates, line breaks. (If the user hasn't given exact wording, ask. Do not invent on-image copy.)
- **The deliverable.** Poster, packaging, ad, social banner, UI mockup, menu, signage, infographic. Sets aspect ratio and layout conventions.
- **Placement and hierarchy.** Where each piece of copy sits and which is primary vs secondary, when it matters.
- Optional: a brand palette, a fixed aspect ratio, a reference image to edit text inside.

## Models

- **Default for typography-heavy design: Ideogram 4.0** (`ideogram:4@0`). Treats text as a first-class element on a structured JSON prompt, so each line of copy is rendered byte-for-byte. Best for posters, packaging, dense multilingual labels, and anything with a real type hierarchy.
- **Best for natural-language briefs + world knowledge: GPT Image 2** (`openai:gpt-image@2`). LLM-based, parses a full design brief, strong on infographics and ad creatives where the model also generates plausible data/content. Renders quoted text reliably.
- **Strong general pick with legible text: Nano Banana 2** (`google:4@3`). Names objects and positions accurately, renders short quoted strings well, has a `thinking` level for dense layouts.
- **Fast text-on-image for marketing/signage: Grok Imagine** (`xai:grok-imagine@image-quality`, or the lighter `xai:grok-imagine@image`). Prompt-only text rendering, good for headlines, pricing callouts, packaging mockups, A/B variants.
- Confirm the model is `live` and inspect its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice.

## Workflow

1. Resolve the chosen model's schema (`runware-run`) and confirm the field names (`positivePrompt`, `width`/`height` or the aspect-ratio presets, plus any per-model settings).
2. Write the prompt with every required string **quoted verbatim** and its placement + style stated (see Technique). For Ideogram, build the structured JSON instead of a sentence.
3. Run `imageInference` synchronously. Request a few variants with `numberResults` so you can pick the cleanest text rendering.
4. **Inspect at full resolution.** Text errors invisible in a thumbnail are obvious at 100%. Check every character against the source copy.
5. If one word is off but the rest is good, do not regenerate. Edit the text in place: pass the image via `inputs.referenceImages` and describe only the change (Grok, GPT Image 2, and Nano Banana 2 support this). For a localized repaint, Ideogram 3.0 Edit takes a seed image plus a mask.

## Technique

- **Quote the exact text. This is non-negotiable.** Wrap every string the image must show in quotation marks inside the prompt. Quotes are the delimiter that tells the model "this is literal content, render it character by character", not a description to interpret. Unquoted, the model keeps the *intent* and invents its own wording, which is where misspellings and nonsense glyphs come from.
- **State placement and style after the scene.** Lead with the scene context, end with the text and where it goes. Specify position ("centered top", "lower third", "across the storefront window"), weight/style ("bold sans-serif", "engraved gold serif", "handwritten chalk"), and size ("large headline", "small subtitle"). Unspecified, the model picks for you.
- **Build a hierarchy for multi-line copy.** Name the primary line (brand/headline) and the secondary lines (subtitle, price, date, credits) separately so the model sizes them in order. This is the difference between a poster that reads as designed and one the model laid out by guess.
- **Keep rendered text short.** Headlines, brand names, short phrases render reliably. Accuracy slips on paragraphs and is worst on dense CJK. For long copy, generate the text element on its own and compose it into the layout afterward.
- **Ideogram operates on a structured JSON, not a sentence.** Text is a first-class element. Each `text` element's `text` field is rendered literally and its `desc` carries position/weight/treatment. `obj` elements are interpreted as natural language. Reserved keys are snake_case in a fixed order: `high_level_description`, `style_description` (`aesthetics`, `lighting`, `photo` *or* `art_style`, `medium`, `color_palette`), and `compositional_deconstruction` (`background`, `elements[]`). You can send a natural-language `positivePrompt` and let Magic Prompt expand it (the JSON comes back in the response to iterate on), or hand the JSON via `settings.structuredPrompt`. The two are mutually exclusive per request. Reach for the structured path when the exact copy matters, there are multiple text elements with hierarchy, or the layout must repeat across runs.
- **Ideogram structured-prompt skeleton.** Fill in the slots and pass it as `settings.structuredPrompt`. Keep one line of copy per `text` element, list elements in reading order, pick `photo` *or* `art_style` (not both), and use uppercase `#RRGGBB` in `color_palette`.

  ```json
  {
    "high_level_description": "<one sentence framing the whole deliverable>",
    "style_description": {
      "aesthetics": "<design school or mood>",
      "lighting": "<flat poster light, soft side light, none>",
      "art_style": "<illustration or print style, or use \"photo\" instead when photographic>",
      "color_palette": ["#RRGGBB", "#RRGGBB"]
    },
    "compositional_deconstruction": {
      "background": "<surface, light, atmosphere only, no subjects>",
      "elements": [
        { "type": "text", "text": "<primary headline verbatim>", "desc": "<size, weight, position>" },
        { "type": "text", "text": "<secondary line verbatim>", "desc": "<size, weight, position>" },
        { "type": "obj", "desc": "<any non-text element described in natural language>" }
      ]
    }
  }
  ```

  Load `references/examples.md` for full worked recipes (poster, packaging, UI mockup) with real AIRs, dimensions, and result shapes.
- **For GPT Image 2, prompt like a brief and reinforce with "verbatim".** Add `render text verbatim, exactly as written, no extra characters` after a quoted string to stop the model rewriting it. It also generates plausible data for infographics and pulls real-world facts into ad/editorial scenes, so describe the deliverable rather than dictating every label.
- **For non-Latin scripts, add a script cue.** Quote the characters and name the script ("written in Japanese kanji", "in traditional Arabic calligraphy") so the model selects the correct glyph set. Latin is most reliable, then CJK with short strings, then RTL scripts (which render best with a calligraphic style cue).
- **Editing copy is a sibling move.** To change the wording inside an existing image rather than generate from scratch, give the image as a reference and describe only what changes, with an explicit preserve list for everything that stays.

## Parameters that matter

- `positivePrompt` carries the quoted copy + placement + style for GPT Image 2, Nano Banana 2, and Grok.
- **Ideogram structured prompt:** `settings.structuredPrompt` (the JSON), or `positivePrompt` for the Magic Prompt path. Never both. `text` renders literal, `obj` interprets. Optional per-element `bbox` is `[y_min, x_min, y_max, x_max]`, integers in 0-1000, row-first (`y` before `x`), origin top-left. `color_palette` is uppercase `#RRGGBB`: up to 16 image-level, up to 5 per element. Set `outputFormat: "PNG"` for transparent backgrounds. `settings.renderingSpeed` tiers `TURBO`/`DEFAULT`/`QUALITY` trade speed for fine-text crispness. Use `QUALITY` for typography-dense hero assets. Width/height must match an allowed aspect-ratio preset.
- **GPT Image 2:** `providerSettings.openai.quality` (`high` for small/dense text, `medium` otherwise). `inputs.referenceImages` accepts up to 16. No `negativePrompt` field. Write `negative prompt:` inline.
- **Nano Banana 2:** `settings.thinking` (`MINIMAL` default, `HIGH` for prompts stacking many constraints). No `negativePrompt` field. Write a `Negative prompt:` clause inline.
- **Grok Imagine:** prompt-only (no text layers, fonts, or bounding boxes). `numberResults` for A/B variants. `inputs.referenceImages` for text editing.
- `numberResults`: request 3-4 and pick the best text rendering. Variance within a batch beats consistency across separate calls.
- Confirm exact field names against the live schema (`runware-run`). Never guess a parameter.

## Quality bar

- Every required string is spelled correctly, character for character, checked at full resolution (not a thumbnail).
- Placement and hierarchy match the brief: primary copy reads as primary, secondary as secondary, nothing drifted off its assigned spot.
- No invented copy, fake logos, fabricated awards, or testimonials beyond what the user supplied.
- Transparency (when needed) survived because the output was PNG, not JPG.
- If one word is wrong, fix it with a text edit rather than regenerating the whole image.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `logos-and-vectors` (typographic marks and flat vector output), `product-photography` (branded packaging and labels in a shot).
