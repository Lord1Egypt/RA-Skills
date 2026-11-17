# Configuration

Strix resolves settings once per process, in this order:

1. Process environment (what `uv run --env-file .env` injects, plus anything already exported).
2. The `env` object in `~/.strix/cli-config.json`, or in the file passed as `--config`.
3. Field defaults in `strix/config/settings.py`.

A variable present in the environment wins over the JSON file, including when the JSON value is newer. After a run, `persist_current` merges the variables that were set in the environment into the JSON file (mode `0600`). A value already in the file stays when its variable is unset. An empty string removes that field from the file.

`STRIX_LLM`, `LLM_API_KEY` (and its alias `OPENAI_API_KEY`), and `LLM_API_BASE` (and its aliases) are one connection. Changing any of them in the environment drops the stored values of all three, so a new model is not paired with the previous key or base URL.

The project `.env` is not read by Strix. `uv run` loads it only when you pass `--env-file` or when uv's own default `.env` discovery is left on. This skill always passes `--env-file .env` from the checkout. `--no-env-file` skips that load.

Write secrets only in `<checkout>/.env` (gitignored) or let Strix persist them to `~/.strix/cli-config.json`. Keep keys out of the scan command line, shell history pasted into chat, and git.

## Required for a hosted model

| Variable | Role |
| --- | --- |
| `STRIX_LLM` | LiteLLM model id. Examples this repository documents: `vercel_ai_gateway/zai/glm-5.3`, `openrouter/z-ai/glm-5.3`, `openai/gpt-5.4`, `anthropic/claude-opus-4-7`. Use the id the user supplies. |
| `LLM_API_KEY` | Provider key. Alias: `OPENAI_API_KEY`. Omitted for a local model, Vertex AI, or Bedrock when those providers authenticate another way. |
| `STRIX_IMAGE` | Sandbox image. After `bash scripts/docker.sh`, set `strix-sandbox:dev` (or the tag you passed). Unset pulls `RuntimeSettings.image` in `strix/config/settings.py`. |

`chatgpt/<model>` uses a ChatGPT subscription. Sign in first with `uv run --env-file .env strix auth login chatgpt`. That path stores OAuth outside `cli-config.json`.

## LLM connection

| Variable | Default | Role |
| --- | --- | --- |
| `LLM_API_BASE` | unset | Custom base URL. Aliases: `OPENAI_API_BASE`, `OPENAI_BASE_URL`, `LITELLM_BASE_URL`, `OLLAMA_API_BASE`. |
| `STRIX_API_TYPE` | model decides | `responses` or `chat_completions`. Alias: `STRIX_FORCE_API`. A custom `LLM_API_BASE` does not switch this; a chat-only gateway needs `chat_completions`. |
| `LLM_EXTRA_HEADERS` | unset | JSON object of extra HTTP headers. The bearer token still comes from `LLM_API_KEY`. |
| `LLM_EXTRA_BODY` | unset | JSON object merged into each main-model request body. Leave `model`, `messages`, `input`, `tools`, and `stream` alone. Reasoning effort is `STRIX_REASONING_EFFORT`. |
| `LLM_TIMEOUT` | `300` | Seconds for a scan LLM call. |
| `LLM_PREFLIGHT_TIMEOUT` | `30` | Seconds for the startup connection check. Failure text: `LLM CONNECTION FAILED`. |
| `LLM_STREAM_IDLE_TIMEOUT` | `300` | Idle time between stream events. |
| `LLM_STREAM_FIRST_EVENT_TIMEOUT` | `120` | Wait for the first stream event. |
| `LLM_STREAM_TOTAL_TIMEOUT` | `600` | Whole-stream cap. |
| `LLM_DISABLE_STREAMING` | `false` | Force non-streaming responses. |
| `LLM_MAX_TOOL_CALLS_PER_TURN` | `32` | Tool-call cap for one model turn. |
| `STRIX_REASONING_EFFORT` | `high` | `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. The default stays `high` in every scan mode unless this variable changes it. |
| `STRIX_LLM_INPUT_COST_PER_MTOK` | unset | USD per 1M input tokens. Set with the output price for a model LiteLLM cannot price. An unset side counts as `0` once any of these prices is set, and the configured prices replace provider-reported cost for `STRIX_LLM` in reports and `--max-budget`. |
| `STRIX_LLM_OUTPUT_COST_PER_MTOK` | unset | USD per 1M output tokens. |
| `STRIX_LLM_CACHED_INPUT_COST_PER_MTOK` | unset | USD per 1M cached input tokens. Unset uses the input price. |
| `STRIX_FORCE_REQUIRED_TOOL_CHOICE` | `false` | Force required tool choice. |
| `STRIX_PARALLEL_TOOL_CALLS` | `false` | Allow parallel tool calls. |
| `STRIX_PROMPT_CACHE` | `true` | Prompt caching. |
| `STRIX_CACHE_BLOCK_TOKENS` | `128` | Cache block size used to decide a cache miss in the run report. DeepSeek and GLM use 64; vLLM often uses 16. |
| `STRIX_OPENROUTER_STICKY_SESSIONS` | `false` | Pin each agent to one OpenRouter provider so its prompt cache survives turns. |

## Deduplication model

Finding dedupe is a separate classification call. Unset, it uses `STRIX_LLM`. A dedicated model does not inherit the main model's extra headers or body.

| Variable | Role |
| --- | --- |
| `STRIX_DEDUPE_MODEL` | Model id. Falls back to `STRIX_LLM`. Keeps LiteLLM pricing even when the main model has manual prices. |
| `DEDUPE_LLM_API_KEY` | Key for that model. |
| `DEDUPE_LLM_API_BASE` | Base URL for that model. |
| `DEDUPE_LLM_EXTRA_HEADERS` | JSON object. |
| `DEDUPE_LLM_EXTRA_BODY` | JSON object. |
| `STRIX_DEDUPE_REASONING_EFFORT` | Effort for the dedupe model. Unset uses the model's baseline. |

## Sandbox and runtime

| Variable | Default | Role |
| --- | --- | --- |
| `STRIX_IMAGE` | `RuntimeSettings.image` in `strix/config/settings.py` | Image to run. Also the image startup pulls when it is missing locally. |
| `STRIX_RUNTIME_BACKEND` | `docker` | Sandbox backend. |
| `DOCKER_HOST` | current docker context, else the default socket | Daemon address, for example `unix:///var/run/docker.sock`. When unset, Strix uses the active docker context (Docker Desktop, OrbStack, Colima). |
| `STRIX_DOCKER_SANDBOX_NETWORK` | unset | Docker network for the sandbox. Setting it drops published ports. |
| `STRIX_DOCKER_SANDBOX_DEVICES` | unset | Comma-separated host devices mapped into the container at the same path with `rwm` access. A tunnel inside the sandbox needs `/dev/net/tun`. |
| `STRIX_SANDBOX_MEM_LIMIT` | unset | Container memory cap. Unset leaves Docker's default. |
| `STRIX_SANDBOX_SHM_SIZE` | unset | `/dev/shm` size. |
| `STRIX_SANDBOX_CPUS` | unset | CPU count passed as nano CPUs. |
| `STRIX_SANDBOX_PIDS_LIMIT` | unset | Process-count cap. |
| `STRIX_SANDBOX_LOG_MAX_SIZE` | `50m` | Per-file cap for the container json log. `0`, `off`, `none`, or `unlimited` leaves Docker's unbounded default. |
| `STRIX_SANDBOX_LOG_MAX_FILE` | `3` | Rotated log files. On-disk cap is size times file count. |
| `STRIX_MAX_CONTEXT_IMAGES` | `3` | Screenshot and image tool outputs kept in one agent context. `0` keeps none. |

## Context window

| Variable | Default | Role |
| --- | --- | --- |
| `STRIX_CONTEXT_AUTO_COMPACT` | `true` | Summarize history as the window fills. |
| `STRIX_CONTEXT_BUFFER_TOKENS` | `20000` | Tokens reserved before compaction. |
| `STRIX_CONTEXT_KEEP_TOKENS` | `8000` | Recent tokens kept verbatim. |
| `STRIX_CONTEXT_FALLBACK_TOKENS` | `200000` | Assumed window when the model does not report one. |
| `STRIX_CONTEXT_SUMMARY_TOKENS` | `4096` | Summary length cap. |
| `STRIX_TOOL_OUTPUT_MAX_TOKENS` | `8000` | Per tool-output token cap. |
| `STRIX_TOOL_OUTPUT_MAX_LINES` | `2000` | Per tool-output line cap. |
| `STRIX_TOOL_OUTPUT_MAX_BYTES` | `51200` | Per tool-output byte cap. |

## Integrations

| Variable | Default | Role |
| --- | --- | --- |
| `EXA_API_KEY` | unset | Exa web search and `web_get_contents`. Preferred when both search keys exist. |
| `PERPLEXITY_API_KEY` | unset | Perplexity web search. |
| `STRIX_WEB_SEARCH_PROVIDER` | `auto` | `auto`, `perplexity`, or `exa`. `auto` uses Exa when `EXA_API_KEY` is set. |
| `STRIX_EXA_SEARCH_TYPE` | `auto` | `auto`, `fast`, `instant`, `deep-lite`, `deep`, `deep-reasoning`. |
| `STRIX_EXA_NUM_RESULTS` | `5` | Exa results, 1–100. |
| `POSTMAN_API_KEY` | unset | Required for `postman://<collection-uid>`. A local collection export does not need it. |

Web search keys are optional. The startup check lists them as optional; a scan still starts without them.

## Telemetry and viewer

| Variable | Default | Role |
| --- | --- | --- |
| `STRIX_TELEMETRY` | on | `0`, `false`, `no`, or `off` disables PostHog and Scarf. |
| `STRIX_RUN_RECORD_TIMINGS` | `false` | Record per-request timings under `llm_requests` and `tool_calls` in `run.json`. |
| `STRIX_APP_URL` | `https://app.strix.ai` | Relay the local viewer proxies to. The browser talks only to the local viewer. |
| `STRIX_DEBUG` | off | `1` / `true` / `yes` / `on` raises log verbosity. |
| `STRIX_NO_UPDATE_CHECK` | unset | Skip the update notice. |

## Example `.env`

```bash
STRIX_LLM=openrouter/z-ai/glm-5.3
LLM_API_KEY=sk-or-...
STRIX_IMAGE=strix-sandbox:dev
STRIX_REASONING_EFFORT=high
EXA_API_KEY=
```

Provider-specific base URLs and auth live under `docs/llm-providers/` in the checkout. When a doc and this file disagree on a default, `strix/config/settings.py` and the `os.environ` reads under `strix/runtime/docker_client.py` win.

`docs/advanced/configuration.mdx` also names `STRIX_LLM_MAX_RETRIES`, `STRIX_MEMORY_COMPRESSOR_TIMEOUT`, `STRIX_SANDBOX_EXECUTION_TIMEOUT`, `STRIX_SANDBOX_CONNECT_TIMEOUT`, and `TRACELOOP_*`. This checkout's `strix/` package does not read those names. Transient LLM retries are `DEFAULT_MODEL_RETRY` in `strix/config/models.py` (5 attempts, backoff from 2s to 90s). Sandbox caps the code does read are the `STRIX_SANDBOX_*` and `STRIX_DOCKER_SANDBOX_*` rows above.
