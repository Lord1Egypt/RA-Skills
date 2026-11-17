# Facial Consultant — interpretation & output

## Skin tone (skin-tone-analysis)
Returns per-region colors (skin / eye / eyebrow / lip / hair): hex + name. **Report colors only**;
do not infer an undertone (the API does not return one). Useful as a color reference for later
makeup/hair suggestions.

## Facial attributes (face-attr-analysis)
- **Shape attributes** (eyeShape, lipShape, faceShape, …): present the returned category label.
  `faceShape` may not be returned — if missing, skip it, do not fill it in.
- **Golden ratio** (horizontalThird, verticalFifth, faceAspectRatio, upperLipToLowerLip, …):
  numeric values. Bucketing relative to the golden target (within ±10% = Balanced):
  - below target −10% → "Short / narrow"
  - within ±10% → "Balanced"
  - above target +10% → "Long / wide"
  Values drift slightly between runs, so **label them as approximate** and never claim precision.

## Output format
1. Color palette (per-region swatches + names).
2. Feature summary (shape labels).
3. Facial proportions (each Balanced / Short / Long + a plain-language line).
4. Closing note: "This is an AI-based facial analysis for reference only, not medical or
   cosmetic-surgery advice."

Exact fields follow the latest doc version; this file is interpretation guidance.
