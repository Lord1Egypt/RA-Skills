# Freepik Ancillary Assets for Product Videos

Use this guide to enrich Remotion scenes with generated assets.
Treat this as the default path for scene visuals and audio unless the user opts out.

Do not outsource narrative structure to generated clips. Keep Remotion as the final editor and timeline authority.

## 1) Default Use

Use Freepik outputs for:

- Stills and backgrounds.
- Very short inserts or transition clips.
- Voiceover generation.
- Background music generation.
- Optional sound effects.

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
- Add a 2-4s motion accent clip if it strengthens the opening.

### Interest

- Generate a clean product-context image or short motion overlay.
- Keep visuals explanatory, not ornamental.

### Desire

- Generate use-case context visuals by persona/environment.
- Prefer 1 asset per use case over many shallow assets.

### Action

- Build CTA card in Remotion (text/vector layout in code).
- Support with a subtle animated background clip.

## 4) Prompt Patterns

Use concise, outcome-oriented prompts:

- Problem frame: "Frustrated [persona] dealing with [pain], cinematic lighting, high contrast, room for headline text."
- Solution frame: "Same [persona] using [product context], clear relief and control, clean composition."
- Use-case frame: "[Persona] achieving [result] with [product], authentic workplace/home context."

Add constraints:

- Aspect ratio (`16:9` or `9:16`)
- Camera language (close-up, wide, over-shoulder)
- Style consistency keywords reused across scenes

## 5) Voiceover, Music, and SFX

### Voiceover (default)

1. Use scene `voiceover` lines from `plan.json`.
2. Generate one file per scene via ElevenLabs (`text-to-speech` skill is preferred default).
3. Save files as `public/audio/vo-<scene-id>.mp3`.
4. Mount VO in each `Sequence` with `<Audio volume={1} />`.

### Background Music (default)

1. Generate one track for full composition duration (`music` skill default).
2. Prompt pattern: "Cinematic ambient track, builds from minimal to hopeful, no vocals."
3. Save as `public/audio/music.mp3`.
4. Mount at composition root and duck to `0.15-0.25` under voiceover.

### Sound Effects (opt-in)

- Use `sound-effects` only if brief explicitly requests SFX.
- Keep SFX sparse and supportive.
- Avoid overpowering VO/music balance.

## 6) Integration Pattern in Remotion

1. Generate assets externally.
2. Save files to `public/assets/` and `public/audio/` plus asset manifest metadata.
3. Pull assets into Remotion as `OffthreadVideo`, `Audio`, or `Img`.
4. Control trims, fades, and volume in timeline code.

## 7) Source Notes

The model names and endpoints above are based on current local Freepik skill references, including:

- Kling video models.
- ElevenLabs voiceover endpoint.
- Music generation endpoint.

If API payloads change, update this reference and keep `SKILL.md` workflow unchanged.
