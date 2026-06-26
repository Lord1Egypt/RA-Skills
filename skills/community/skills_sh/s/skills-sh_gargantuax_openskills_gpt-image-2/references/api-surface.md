# API Surface

Run `scripts/gpt_image.py` with one of these subcommands. Each one targets a different OpenAI-compatible route and has its own constraint set.

## `generations`

Target route: `POST /v1/images/generations`

Use for:

- Text-to-image
- Public Images API compatibility checks
- Multi-image batches via `--n`
- Public-route streaming and `--partial-images`

Constraints:

- `--prompt` is required.
- `--n` must be in `1..10`.
- On OpenAI GPT image models, omit `--response-format` entirely.
- `background=transparent` is rejected.
- `--stream` together with `--n > 1` is rejected.

## `edits`

Target route: `POST /v1/images/edits`

Use for:

- Multipart image edits
- Multiple uploaded source images
- Mask uploads
- Public Images API edit compatibility checks

Constraints:

- `--prompt` is required.
- At least one `--image` must be provided.
- Repeated image field style can be `simple`, `brackets`, or `indexed`; `brackets` matches OpenAI's documented multipart shape.
- `background=transparent` is rejected.
- On OpenAI GPT image models, omit `--response-format` entirely.
- `--stream` together with `--n > 1` is rejected.

## `responses`

Target route: `POST /v1/responses`

Use for:

- Advanced image workflows
- Streaming-first flows
- Mixed text + image input
- `previous_response_id`
- `tool_choice`
- `action`
- Image inputs from local files, URLs, data URLs, or file references

Constraints:

- Uses a text-capable Responses model at the top level (default: `gpt-5.4`).
- Sends an `image_generation` tool by default.
- Supports `--mask`, `--mask-url`, and `--mask-file-id`.
- `--tool-model` optionally overrides the hosted image model for the tool.
- `--tool-choice image_generation` is normalized to `{"type":"image_generation"}`.
- `--input-fidelity` is only valid for supported non-`gpt-image-2` tool models.
- `quality` is passed through to the hosted image tool.
- Local image files are converted to data URLs before being sent.

## Shared GPT Image 2 validation

The script runs these checks before every request:

- Size must be `auto` or `WIDTHxHEIGHT`.
- Width and height must be multiples of `16`.
- Longest edge must be `<= 3840`.
- Aspect ratio must be `<= 3:1`.
- Total pixels must be in `655360..8294400`.
- Transparent background is not supported.
- `output_compression` must stay in `0..100` and only applies to `jpeg` or `webp`.
- `partial_images` must be in `0..3` and requires `stream=true`.
