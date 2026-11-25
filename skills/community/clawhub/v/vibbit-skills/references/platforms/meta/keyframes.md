---
skill_code: VB-06
version: "1.0.0"
---

# Keyframe ideas and category references

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Keyframes](#keyframes)
- [Keyframe category worlds](#keyframe-categories)

<a id="keyframes"></a>

## Keyframes

Read [shared boundaries](guidelines.md). Use actual product name/description, category, reference image, market/language, ratio, and requested picture types. A concept-only input can yield a concept, not guaranteed product fidelity.

This is a creative image system, distinct from a video model's first/last-frame parameters. It is not a mandatory four-image prerequisite for ordinary image-to-video work.

Define a shared `world_id` with model appearance/clothing, specific location, palette, lighting direction/quality, and actual product constraints. Keep these stable while varying camera distance/composition and purposeful actions/expressions. Use only the relevant [category row](#keyframe-categories).

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

<a id="keyframe-categories"></a>

## Keyframe category worlds

Read only the relevant row for [Keyframes](#keyframes). Pick one setting per world and share its person, clothing, palette, and lighting. Occasion uses actions; Vibe uses emotion. These are optional creative directions, not market facts, product efficacy claims, or mandatory American settings.

| Category | Possible setting | Occasion actions | Vibe |
| --- | --- | --- | --- |
| Fashion | Bright apartment, city street, loft, minimal cafe, rooftop, sunny laundromat | Walk purposefully, enter a doorway, take a bag, adjust headphones, pick up keys, tie shoes | Effortless confidence, self-assurance, weekend ease |
| Beauty | Modern bathroom, vanity, bright bedroom, mirror, sunny counter, clean studio | Apply/blend/tap product, check skin in daylight, reach for a routine item | Fresh calm, tactile satisfaction, confidence |
| Food/drink | Kitchen counter, patio, coffee table, desk break, picnic, breakfast bar | Pour, bite, stir, open fridge, plate food, unwrap | First-bite satisfaction, comfort, savoring, refreshment |
| Technology | Desk, commute, cafe, home office, sofa, charging area | Type, plug in, charge, adjust settings, wear headphones, pocket a phone | Focus, relief, seamless-use satisfaction |
| Home | Living-room corner, kitchen, bedside, dining table, shelf, entryway | Arrange objects, light a candle, fill a vase, adjust cushions, set a table | Calm, comfort, pride, a peaceful moment |
| Automotive | Garage, driveway, dusk street, roadside stop, EV charger, rooftop parking | Enter driver's seat, adjust mirror, start vehicle, load trunk, plug in charger | Quiet confidence, freedom, ownership pride |
| Finance | Apartment, cafe, park bench, home desk, airport, sofa | Approve a payment, check notification, show phone, scan at checkout, open app | Relief, control, satisfaction in an evidenced milestone |
| Gaming | Gaming setup, TV sofa, desk, screen-lit room, friends' couch, streaming desk | Put on headset, lean forward, grab controller, celebrate, adjust screen, unbox | Tension, celebration, immersion, shared enjoyment |

Do not present fictional financial returns or cosmetic effects as evidence. Different actions must not accidentally change product/person/location identity. Unmatched categories should use the product's real context.
