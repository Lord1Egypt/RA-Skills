# Image generation: gen_image

Task type: `AIGC_IMAGE_GENERATION`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/517411420e0)

Default model: gpt-image-2.5-sunburst; default size: 1024x1024. Explicit model and size are preserved. Inputs: prompt, model, size and optional reference_image_urls. The singular reference_image_url and mask fields are not supported; verify the returned image and dimensions.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `prompt` | string | Yes |
| `model` | string | Yes |
| `size` | string | Yes |
| `reference_image_urls` | urls | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "prompt": "A blue ceramic cup on a white background",
  "model": "gpt-image-2.5-sunburst",
  "size": "1024x1024"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --input /absolute/path/request.json
~~~

The client sends a native object in `input_info.input`. Do not change encoding and automatically resubmit after an error.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Defaults and supported inputs

The API requires prompt/model/size. The client fills omitted model with gpt-image-2.5-sunburst and size with 1024x1024, preserving explicit choices. Models: gpt-image-2, gpt-image-2.5-flare, gpt-image-2.5-sunburst. Reject empty or unsupported values and unknown fields.

Size is checked as a nonempty string; no complete supported-size list is published. This does not imply arbitrary sizes work. Optional reference_image_urls must be a nonempty URL array. Singular reference_image_url and mask are unsupported and rejected.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --prompt 'A blue ceramic cup on a white background' --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --input /absolute/path/image.json --wait
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --prompt 'Edit the reference background' --ref-url 'https://example.com/reference.png' --dry-run
~~~

Choose JSON input or inline fields, without mixing overrides. --ref-url maps to a one-element reference_image_urls array. No --allow-legacy is required.

Query the returned task ID using GET. Client polling starts conservatively at 5 seconds with a 50-second wait; no image-specific rate is documented. At completion parse the JSON string task_result.result and extract image_url. Resume timeouts without resubmitting.

Output count, quality, transparency toggles, masks, and exact pricing parameters are not defined. Check the actual image and metadata.

[Image capability](../capabilities/generation/image-generation.md) · [GPT Image guide](../models/gpt-image.md) · [Result reference](https://vibbit.apifox.cn/517413731e0).
