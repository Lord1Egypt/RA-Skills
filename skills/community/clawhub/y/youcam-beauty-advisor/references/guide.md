# Beauty Advisor — recommendation logic & output

## From analysis to recommendation
- **Skin tone**: use the returned skin/lip/eye colors to judge warm/cool, then pick matching
  lip, blush, and eyeshadow colors.
- **Face shape** (the API's `faceshape` values):
  - Round → more sculpting/contour, angled blush; Oblong → horizontal blush, avoid over-lengthening;
    Square → soften lines; Heart → add volume in the lower face to balance.
  - Any other shape (Oval, Triangle, InvTriangle, Diamond) or Unknown → no shape-specific rule
    here; give general advice (for Unknown, see the aspect-ratio note in SKILL.md).
- **Eye/lip shape** → informs eyeliner and lip-shaping suggestions.
- These are directional suggestions, not hard rules; respect the user's preference and the
  occasion (daily vs. event).

## Two preview modes
- **look-vto (template)**: best for "give me a full look". List a few templates (with thumbnails)
  for the user to pick, then apply.
- **makeup-vto (custom)**: best for specific items. The `effects` array holds one item per
  category (blush, lip_color, eye_shadow, …), each with pattern.name and palettes
  (color / intensity / texture).

## Output
1. Recommendation rationale (why it suits: skin tone + face shape).
2. **The try-on result image URL (returned exactly as given).**
3. Closing note: "This preview image is AI-generated and for reference only; actual results may
   vary."

Parameters/categories follow the latest doc version; this file is recommendation guidance.
