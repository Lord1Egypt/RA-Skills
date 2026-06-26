# Freepik Ancillary Assets for Product Videos

Use this guide to enrich Remotion scenes with generated assets.

Do not outsource narrative structure to generated clips. Keep Remotion as the final editor and timeline authority.

## 1) Allowed Use

Use Freepik outputs for:

- Stills and backgrounds.
- Very short inserts or transition clips.
- Voiceover generation.
- Background music generation.

Avoid using one generated video as the full ad.

## 2) Recommended Routing

Pick the lightest model that solves the scene goal:

- Product or concept stills: Nano Banana 2 or Freepik image generation models.
- Motion inserts/transitions: Kling family (`kling-v3-omni-pro` as default).
- Narration: ElevenLabs voiceover endpoint.
- Music bed: music generation endpoint.

## 3) Scene-by-Scene Asset Suggestions

### Attention

- Generate one high-impact visual metaphor still.
- Optionally create a 2-4s motion accent clip for opening punch.

### Interest

- Generate a clean product-context image or short motion overlay.
- Keep visuals explanatory, not ornamental.

### Desire

- Generate use-case context visuals by persona/environment.
- Prefer 1 asset per use case over many shallow assets.

### Action

- Build CTA card in Remotion (text/vector layout in code).
- Optionally support with subtle animated background clip.

## 4) Prompt Patterns

Use concise, outcome-oriented prompts:

- Problem frame: "Frustrated [persona] dealing with [pain], cinematic lighting, high contrast, room for headline text."
- Solution frame: "Same [persona] using [product context], clear relief and control, clean composition."
- Use-case frame: "[Persona] achieving [result] with [product], authentic workplace/home context."

Add constraints:

- Aspect ratio (`16:9` or `9:16`)
- Camera language (close-up, wide, over-shoulder)
- Style consistency keywords reused across scenes

## 5) Voiceover and Music

### Voiceover (ElevenLabs via Freepik)

- Generate section-by-section narration from the AIDA script.
- Keep sentence cadence aligned to scene durations.
- Export a single final narration track when timing is locked.

### Music

- Generate a track matching pace and emotional arc.
- Use lower intensity in problem section and lift near CTA.

## 6) Integration Pattern in Remotion

1. Generate assets externally.
2. Save URLs/paths in an asset manifest.
3. Pull assets into Remotion as `OffthreadVideo`, `Audio`, or `Img`.
4. Control trims, fades, and volume in timeline code.

## 7) Source Notes

The model names and endpoints above are based on current local Freepik skill references, including:

- Kling video models.
- ElevenLabs voiceover endpoint.
- Music generation endpoint.

If API payloads change, update this reference and keep `SKILL.md` workflow unchanged.
