# Config

Environment variables consumed by `scripts/nanobanana.py`:

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | yes | none | API key for the Gemini-compatible endpoint |
| `GEMINI_BASE_URL` | no | `https://generativelanguage.googleapis.com/v1beta` | Base URL root before `/models/...` |
| `GEMINI_MODEL` | no | `nanobanana` | Default model alias or exact model ID |
| `GEMINI_TIMEOUT` | no | `300` | HTTP timeout in seconds |
| `GEMINI_AUTH_MODE` | no | `auto` | `auto`, `x-goog-api-key`, or `bearer` |
| `GEMINI_ASPECT_RATIO` | no | unset | Example: `1:1`, `16:9`, `4:5` |
| `GEMINI_IMAGE_SIZE` | no | unset | `512`, `1K`, `2K`, or `4K` on supported models |
| `GEMINI_USE_SEARCH` | no | `false` | Add the `google_search` tool |
| `GEMINI_OUTPUT_DIR` | no | `./nanobanana-images` | Default directory when `generate` has no explicit `--output`, and the base directory for `batch` |
| `GEMINI_BATCH_PREFIX` | no | `image` | Default filename prefix for `batch` |
| `GEMINI_BATCH_COUNT` | no | `10` | Default number of batch requests |
| `GEMINI_BATCH_DELAY` | no | `3.0` | Delay between sequential batch requests |
| `GEMINI_BATCH_PARALLEL` | no | `1` | Parallel worker count for `batch` |

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
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_MODEL=nanobanana-2
GEMINI_TIMEOUT=300
GEMINI_ASPECT_RATIO=16:9
GEMINI_IMAGE_SIZE=2K
```

Notes:

- `GEMINI_BASE_URL` should end at the API root such as `/v1beta`; do not append `/models`.
- `GEMINI_AUTH_MODE=auto` uses `x-goog-api-key` for the official Google endpoint and both header styles for custom endpoints.
- CLI `--size` is rejected for `gemini-2.5-flash-image`.
- Inherited `GEMINI_IMAGE_SIZE` values from the environment or `.env` are automatically ignored when the selected model is `gemini-2.5-flash-image`.
- `512` is only supported on `gemini-3.1-flash-image-preview`.
