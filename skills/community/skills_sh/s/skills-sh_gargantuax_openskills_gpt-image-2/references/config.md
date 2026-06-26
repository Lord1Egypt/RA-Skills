# Config

Environment variables consumed by `scripts/gpt_image.py`:

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | yes | none | API key for the OpenAI-compatible endpoint |
| `OPENAI_BASE_URL` | no | `https://api.openai.com/v1` | Base URL, must include `/v1` |
| `OPENAI_IMAGE_MODEL` | no | `gpt-image-2` | Default model for `generations` and `edits` |
| `OPENAI_RESPONSES_MODEL` | no | `gpt-5.4` | Default top-level model for `responses` |
| `OPENAI_IMAGE_TOOL_MODEL` | no | unset | Optional hosted image model override for the `responses` image tool |
| `OPENAI_IMAGE_TIMEOUT` | no | `300` | HTTP timeout in seconds |
| `OPENAI_IMAGE_SIZE` | no | `auto` | e.g. `1024x1024`, `1536x1024`, `auto` |
| `OPENAI_IMAGE_QUALITY` | no | `high` | `auto`, `low`, `medium`, `high` |
| `OPENAI_IMAGE_BACKGROUND` | no | unset | `auto` or `opaque` |
| `OPENAI_IMAGE_FORMAT` | no | `webp` | `png`, `jpeg`, `webp` |
| `OPENAI_IMAGE_COMPRESSION` | no | unset | `0..100`, only for `jpeg` or `webp` |
| `OPENAI_IMAGE_MODERATION` | no | unset | `auto` or `low` |
| `OPENAI_IMAGE_USER` | no | unset | Optional OpenAI-compatible `user` field |
| `OPENAI_IMAGE_N` | no | `1` | Default image count for `generations` and `edits` |
| `OPENAI_IMAGE_RESPONSE_FORMAT` | no | unset | Legacy compatibility field for non-GPT image models; omit it for OpenAI GPT image models |
| `OPENAI_IMAGE_STREAM` | no | `false` | Default streaming flag |
| `OPENAI_IMAGE_PARTIAL_IMAGES` | no | unset | `0..3`, used together with streaming |
| `OPENAI_IMAGE_INPUT_FIDELITY` | no | unset | Optional `input_fidelity` for supported tool models in `responses` |
| `OPENAI_IMAGE_TOOL_CHOICE` | no | `image_generation` | Default `tool_choice` for `responses`; the script maps this to `{\"type\":\"image_generation\"}` |

Resolution order:

1. CLI flags
2. Process environment variables
3. `.env` file
4. Built-in defaults

`.env` lookup:

1. `--env-file <path>` when provided
2. Search from `<cwd>/.env` upward through parent directories until the first `.env` is found

Minimal `.env` example:

```dotenv
OPENAI_API_KEY=sk-example
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_IMAGE_MODEL=gpt-image-2
OPENAI_RESPONSES_MODEL=gpt-5.4
OPENAI_IMAGE_SIZE=auto
OPENAI_IMAGE_QUALITY=high
OPENAI_IMAGE_FORMAT=webp
OPENAI_IMAGE_TIMEOUT=300
```

Notes:

- `OPENAI_BASE_URL` must already include `/v1`.
- `OPENAI_IMAGE_MODEL` does not control the top-level model for `responses`; use `OPENAI_RESPONSES_MODEL` for that.
- `OPENAI_IMAGE_STREAM=true` is valid for all three subcommands, but public Images routes still reject `stream=true` together with `n>1`.
- On OpenAI GPT image models, omit `OPENAI_IMAGE_RESPONSE_FORMAT` entirely.
- `OPENAI_IMAGE_INPUT_FIDELITY` is not configurable for `gpt-image-2`.
- Process environment variables override `.env`, so local shell overrides stay predictable.
