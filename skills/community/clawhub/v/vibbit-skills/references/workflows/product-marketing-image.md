# Product marketing images

Create listing main images, lifestyle images, feature graphics, detail-page images or ad creatives from a product link, saved product or customer facts. Deliver planning when requested; explicit production requests proceed to actual images without mandatory copy/layout approval stages.

## Product and goal

Use [product inputs](../resources/products.md) to parse/select the product. Link-based production includes saving by default, reusing an identical existing product. Respect no-save and analysis-only requests. Read detail and real references; retain claims, purpose, market, language, style, dimensions and count. One image does not authorize a whole set.

| Purpose | Design and review focus |
| --- | --- |
| Listing main image | Accurate product/specification and clear presentation; check the specified platform/category requirements without adding prohibited text or props |
| Lifestyle image | A real use context with credible size, appearance and usage relationships |
| Feature/detail graphic | A clear message supported by actual features; no invented comparison numbers, certifications, gifts or offers |
| Ad creative | Audience-specific context, purchase reason and call to action; distinguish facts from creative expression and preserve readability |

US audiences may use English when no language is specified; retain another explicit language. Keep real currency. Omit prices when no US price exists instead of relabeling a value as dollars. Check current placement requirements when compliant delivery is requested; do not impose a platform's rules when none is selected.

## Generate and review

When direction is needed, choose the image's message, product presentation, background, composition and necessary copy. Preserve supplied prompts/layouts. Meta tasks may use [keyframe methods](../platforms/meta/keyframes.md) without loading the full strategy package.

1. Inspect adopted references and pass their actual URLs in [gen_image](../api/gen_image.md) reference_image_urls. Describe model, shape, color, proportions, material, labels and logos to preserve, keeping reference roles consistent with the prompt.
2. Submit through [image generation](../capabilities/generation/image-generation.md) and retain task IDs. Explicit model, dimensions and count take priority. Otherwise use that capability's defaults and state the choice. Placeholder references are not production inputs.
3. Inspect actual output for variant identity, spelling, supported claims, layout and measured dimensions. If exact complex text needs postproduction, use an authorized workable route; do not invent mask/local-edit fields.
4. Deliver real images with product ID, adopted references, copy and generation records. Revise affected images/content without automatically generating repeated alternatives.

Replace [example request](../../examples/product-marketing-image.json) references with the chosen product's real images. A product save does not attach the generated images; current public product operations do not provide that association.

## Continue or combine

Reuse product and constraints for background, style, language or claim changes. Updating stored facts is a separate product operation. Inspected/adopted images can feed [product video](product-video.md) without reparsing, resaving or redrawing the product. For an image/video set, plan and deliver the explicitly requested counts separately.
