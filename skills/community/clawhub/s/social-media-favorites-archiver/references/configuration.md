# Configuration

Application settings use a YAML file plus `SMFA_`-prefixed environment variables. Command-line overrides take precedence over environment variables, which take precedence over the file and built-in defaults.

Safe example:

```yaml
vault_path: ~/Documents/SMFA-Vault
state_db_path: ~/Documents/SMFA-Vault/.social-media-favorites-archiver/archive.db
cache_path: ~/.cache/social-media-favorites-archiver
cache_quota_bytes: 21474836480
browser_cdp_url: http://127.0.0.1:9222
browser_profile_path: ~/.local/share/social-media-favorites-archiver/browser
enabled_platforms: [bilibili, xiaohongshu, douyin]
concurrency: 2
retries: 3
early_stop_threshold: 20
cleanup_policy: after-verified
asr_backend: auto
asr_model: funasr-paraformer-zh
ocr_backend: rapidocr
terminology_dictionary: ~/.config/social-media-favorites-archiver/terms.txt
enrichment_enabled: false
```

Every YAML key has an uppercase `SMFA_` environment equivalent, such as `SMFA_VAULT_PATH`, `SMFA_CONCURRENCY`, and `SMFA_ASR_BACKEND`. Do not place cookies, browser storage, passwords, or platform tokens in this file.

Optional OpenAI-compatible enrichment reads `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` only when enrichment runs. These variables are not persisted in application settings, and `smfa doctor` reports only whether each one is present. Local collection, ASR, OCR, and Markdown output continue to work when enrichment is disabled or those variables are absent.

`OPENAI_API_KEY` and `OPENAI_MODEL` are required only when enrichment is enabled. `OPENAI_BASE_URL` is optional and defaults to the OpenAI API root; when configured, it must be an HTTP(S) API root without embedded credentials, query parameters, or fragments. The client tries the Responses API first and falls back to Chat Completions only when the provider reports that the Responses endpoint is unsupported.

The request contains only an allowlist of redacted text fields: title, author, platform, original text, transcript, and OCR text. It never contains source/media URLs, local paths, assets, browser state, cookies, headers, or raw platform responses. The result follows the strict `summary`, `key_points`, `topics`, `tags`, `language`, and `safety_notes` schema described by [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs). Invalid output and transient provider errors retain the complete local source text and return a retryable state; disabled, missing-configuration, and permanent-error paths do not block the base archive.

Successful records persist only provider/model/prompt-version provenance, the text-input hash, the validated structured result, latency, character count, and token counts when supplied. They never persist the key, authorization metadata, endpoint URL, request body, or raw response.

## OpenAI-compatible smoke evidence

On 2026-08-08, one opt-in real call used only synthetic text and the already configured local environment. The strict structured result passed validation in 16,049 ms; the provider reported 4,641 input tokens, 112 output tokens, and 4,753 total tokens. The model value was intentionally not recorded because the environment-provided identifier may be private. No input/output text, endpoint, credential, or authorization metadata was logged or committed.

## Local OCR compatibility evidence

The macOS default is RapidOCR backed by ONNX Runtime. PaddleOCR is intentionally not a required 1.0 dependency. Install the local backend with `uv sync --extra ocr`, then verify it without exposing content or credentials:

```bash
uv run smfa doctor --json
uv run pytest tests/integration/test_rapidocr.py -q -m heavyweight
```

On 2026-08-08, the generated high-contrast text check passed on Apple Silicon (`arm64`, macOS 26.6.1) with `rapidocr-onnxruntime` 1.4.4, `onnxruntime` 1.28.0, and `opencv-python` 5.0.0.93. The doctor reported `RapidOCR is available`. This proves that local runtime combination, not universal recognition quality; rotated, low-contrast, Chinese, and platform-sourced images remain explicit regression and live-validation cases.
