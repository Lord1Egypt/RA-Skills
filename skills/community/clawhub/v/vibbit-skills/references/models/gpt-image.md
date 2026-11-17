# GPT Image

Use the models accepted by [gen_image](../api/gen_image.md): `gpt-image-2`, `gpt-image-2.5-flare`, and the default `gpt-image-2.5-sunburst`. Preserve a requested supported model and size. They share the current entry's input structure; names alone do not establish comparative quality or cost.

Describe the image's actual downstream role and distinguish creating a new image from reusing an adequate existing reference. Pass reference URLs through `reference_image_urls`. The public entry does not expose masks, quality, transparency, or output-count controls; do not invent fields based on other image APIs.

Do not test every model or resubmit with another model without authorization for the additional outputs. Review the actual image for subject, composition, required text, and size. Reuse approved images downstream. See [image generation](../capabilities/generation/image-generation.md).
