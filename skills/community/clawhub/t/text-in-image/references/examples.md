# Worked recipes

Three end-to-end recipes for the most common text-in-image deliverables. Each gives the scenario, the actual `imageInference` request, and the result shape. AIRs and fields are confirmed against the Runware catalog and the live request schemas. Confirm field names and dimension presets against the live schema (`runware-run`) before you send, since presets change per model.

Across all three: quote every required string verbatim, state placement and style after the scene, and inspect the returned image at full resolution before returning it.

## Recipe 1: poster with a quoted headline (Ideogram structured JSON)

Use Ideogram when the copy has to be byte-for-byte correct and there is a real type hierarchy. The structured prompt puts each line of copy in its own `text` element, so the model renders it literally instead of paraphrasing.

**Scenario.** A 2:3 portrait gig poster. Title `"NIGHT SIGNALS"`, support act `"with THE LOW HOURS"`, venue and date `"THE ATLAS ROOM · FRI MAR 14"`, and a small price line `"DOORS 8PM · $18"`. Brand palette is amber on near-black.

**Request.** `settings.structuredPrompt` and `positivePrompt` are mutually exclusive, so send only the structured path here. `renderingSpeed: "QUALITY"` for typography-dense final art. Width and height must match an allowed preset (`1664 × 2496` is the 2:3 preset).

```json
[
  {
    "taskType": "imageInference",
    "taskUUID": "11111111-1111-1111-1111-111111111111",
    "model": "ideogram:4@0",
    "settings": {
      "renderingSpeed": "QUALITY",
      "structuredPrompt": {
        "high_level_description": "A modern indie gig poster, bold typographic hierarchy over a dark stage-lit background, amber and off-black palette.",
        "style_description": {
          "aesthetics": "Contemporary music-poster design, confident type hierarchy, restrained ornament.",
          "lighting": "Moody low stage light, soft amber glow rising from the lower edge.",
          "art_style": "Modern screen-print poster with thick display type and a single warm accent colour.",
          "color_palette": ["#0E0C0A", "#E8A13B", "#F2E6D0"]
        },
        "compositional_deconstruction": {
          "background": "Near-black textured field filling the frame, a soft amber gradient glow rising from the bottom edge.",
          "elements": [
            { "type": "text", "text": "NIGHT SIGNALS", "desc": "Headline in massive amber condensed sans-serif capitals, dominating the upper half, broken across two stacked lines, tightly leaded." },
            { "type": "text", "text": "with THE LOW HOURS", "desc": "Support act in medium off-white sans-serif, centred directly beneath the headline." },
            { "type": "text", "text": "THE ATLAS ROOM · FRI MAR 14", "desc": "Venue and date in small amber spaced capitals across the lower third." },
            { "type": "text", "text": "DOORS 8PM · $18", "desc": "Price and doors line in small off-white capitals along the very bottom edge, centred." }
          ]
        }
      }
    },
    "width": 1664,
    "height": 2496,
    "numberResults": 3,
    "outputFormat": "PNG"
  }
]
```

**Result shape.** Three candidate images in the `data` array. Each item carries `imageURL` (or `imageBase64Data` / `imageDataURI` if requested) plus `imageUUID` and the echoed `taskUUID`. Pick the candidate whose four lines all read correctly at 100%.

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "11111111-1111-1111-1111-111111111111",
      "imageUUID": "aaaaaaaa-1111-1111-1111-111111111111",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/aaaaaaaa-1111-1111-1111-111111111111.png"
    }
  ]
}
```

To iterate one line without rewriting the whole poster, send a natural-language `positivePrompt` first, capture the `structuredPrompt` returned in the response, edit only the element you want to change, and re-send it as `settings.structuredPrompt`.

## Recipe 2: packaging with exact copy (Grok Imagine, prompt-only)

Grok renders short quoted strings on product mockups fast and has no structured-prompt layer. Drive everything through `positivePrompt`: product description, then the brand and product copy as quoted strings, then the photography context. Request a batch and pick the cleanest text.

**Scenario.** A kraft coffee bag mockup. Brand `"NORDIC ROAST"` as the primary line, `"Single Origin · Ethiopia"` as the subtitle, and a small roast tag `"MEDIUM ROAST · 250g"`.

**Request.** Grok takes either a `resolution` preset or a `width`/`height` preset pair, never both. A square 1:1 packshot uses `1024 × 1024`. `resolution: "2K"` is the larger alternative when you do not pass explicit dimensions.

```json
[
  {
    "taskType": "imageInference",
    "taskUUID": "22222222-2222-2222-2222-222222222222",
    "model": "xai:grok-imagine@image-quality",
    "positivePrompt": "A premium kraft-paper coffee bag standing on a rustic wooden surface with a few scattered roasted beans, soft natural window light, shallow depth of field, product photography. The brand name \"NORDIC ROAST\" is printed in matte-black bold serif across the upper third, with \"Single Origin · Ethiopia\" as a smaller centred subtitle directly below, and a small \"MEDIUM ROAST · 250g\" tag in the lower-left corner.",
    "width": 1024,
    "height": 1024,
    "numberResults": 4
  }
]
```

**Result shape.** Four candidates in `data`, each with `imageURL`, `imageUUID`, and the echoed `taskUUID`. Inspect each at full resolution and confirm all three copy blocks spell correctly.

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "22222222-2222-2222-2222-222222222222",
      "imageUUID": "bbbbbbbb-2222-2222-2222-222222222222",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/bbbbbbbb-2222-2222-2222-222222222222.jpg"
    }
  ]
}
```

If one candidate is clean except for a single wrong word, do not regenerate. Pass that image back via `inputs.referenceImages` and describe only the change, with a preserve list for everything that stays.

## Recipe 3: UI mockup with dense small labels (GPT Image 2)

GPT Image 2 parses a full design brief and renders small, dense labels reliably, which fits UI and dashboard mockups. Quote every label, add a verbatim cue, and raise quality for small text.

**Scenario.** A mobile app dashboard screen. App title `"FLOWBANK"`, a balance card reading `"Available balance"` over `"$4,820.55"`, and a row of three nav labels `"Home"`, `"Cards"`, `"Settings"`.

**Request.** GPT Image 2 takes free `width`/`height` (multiples of 16, up to 3840). A `768 × 1408` portrait reads as a phone screen. Use `providerSettings.openai.quality: "high"` for the small nav and balance text. There is no `negativePrompt` field. Write any exclusion as a `negative prompt:` clause inside the prompt.

```json
[
  {
    "taskType": "imageInference",
    "taskUUID": "33333333-3333-3333-3333-333333333333",
    "model": "openai:gpt-image@2",
    "positivePrompt": "A clean mobile banking app dashboard screen, modern flat UI, soft drop shadows, light background with a single teal accent. Top bar app name reads \"FLOWBANK\" in a bold sans-serif wordmark. A rounded balance card in the upper half shows \"Available balance\" as a small grey label with \"$4,820.55\" beneath it in large bold dark type. A bottom navigation bar shows three evenly spaced labels: \"Home\", \"Cards\", \"Settings\", each under a simple line icon. Render every label verbatim, exactly as written, no extra characters, no other text anywhere in the frame.\n\nnegative prompt: lorem ipsum, placeholder text, watermark",
    "width": 768,
    "height": 1408,
    "providerSettings": {
      "openai": {
        "quality": "high"
      }
    }
  }
]
```

**Result shape.** One image in `data` with `imageURL`, `imageUUID`, and the echoed `taskUUID`.

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "33333333-3333-3333-3333-333333333333",
      "imageUUID": "cccccccc-3333-3333-3333-333333333333",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/cccccccc-3333-3333-3333-333333333333.png"
    }
  ]
}
```

Check the balance figure and every nav label character by character. If the model splices an extra digit into the balance, fix it with a reference-image text edit rather than a fresh generation.
