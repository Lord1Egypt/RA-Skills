# Image generation

Identify the image's role: standalone delivery, a generation reference, or an element for postproduction. Preserve requested count, style, exact text, and dimensions. Reuse a suitable existing image when no new asset is needed.

Use [gen_image](../../api/gen_image.md) and preserve an explicit supported model. Do not infer performance from model names. Describe task-specific subjects, relationships, composition, pose, lighting, materials, and exact visible text. Character references need the required identity/clothing, not an automatic wardrobe set; environments need perspective, scale, and placement; product images must preserve real product facts.

The current reference field is `reference_image_urls`. Do not invent singular-reference or mask fields. Limits of this entry are not claims about every model in the family. A supplied image can go directly to supported video editing without regeneration.

Submit only the authorized number of outputs. Do not automatically switch models or repeat uncertain requests. Inspect the actual returned image and URL for composition, text, and size; mark quality as unverified if viewing was unavailable. See [GPT Image](../../models/gpt-image.md).
