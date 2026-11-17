---
skill_code: VB-06
version: "1.0.0"
---

# Keyframes

Read [shared boundaries](guidelines.md). Use actual product name/description, category, reference image, market/language, ratio, and requested picture types. A concept-only input can yield a concept, not guaranteed product fidelity.

This is a creative image system, distinct from a video model's first/last-frame parameters. It is not a mandatory four-image prerequisite for ordinary image-to-video work.

Define a shared `world_id` with model appearance/clothing, specific location, palette, lighting direction/quality, and actual product constraints. Keep these stable while varying camera distance/composition and purposeful actions/expressions. Use only the relevant [category row](libraries/keyframe-categories.md).

| Type | Purpose and treatment |
| --- | --- |
| `hook` | Product-centered attention, clear attitude; framing depends on category; short headline often 2–6 words |
| `occasion` | Wide/full-body real activity with visible environment and product; activity headline often 3–8 words |
| `texture` | Readable real material/craft, optionally touched; 60–80% product detail as a compositional starting point |
| `vibe` | Close face/product portrait, real microexpression, soft background, visible product; distinct from occasion |

A standard set includes all four; requested subsets take priority. `variant_index` means another world, not a requirement to generate three sets.

Natural phone photography, cool neutrals, soft daylight, and realistic skin/hair are optional presets. Brand/market choices may require warmth, studio lighting, or different locations. Contemporary American style does not override the target market.

Use real image inputs to constrain shape, color, material, labels, and proportions. “This exact product” alone cannot bind identity. Preserve genuine markings while avoiding invented logos/watermarks. Keep headline text as a separate controlled layer when appropriate. Depth-of-field wording guides appearance, not verified camera metadata.

Output shared `world` plus each frame's ID/type/headline/self-contained prompt/rationale/product-reference IDs. Include full world information in every prompt. User-facing headlines follow the target language. Prompt requests end with prompts; image requests use [image generation](../../capabilities/generation/image-generation.md) within authorized count, then attach actual asset references.

For video, use [storyboard production](../../workflows/storyboard-video.md) and the model's real frame modes. Revising one frame preserves the rest unless the world itself changes.
