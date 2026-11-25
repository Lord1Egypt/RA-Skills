# Configuration - resolving provider and API key

## Provider selection

Set `VISION_PROVIDER` to choose the backend:

| Value | Backend | Default endpoint | Default model |
|-------|---------|-----------------|---------------|
| `ark` (default) | Volcengine Ark / doubao | `https://ark.cn-beijing.volces.com/api/plan/v3` | `doubao-seed-2.0-lite` |
| `openai` | Any OpenAI-compatible API | `https://api.openai.com/v1` | `gpt-4o-mini` |

## Overrides

All of these can be set as environment variables to override the defaults:

| Variable | Purpose |
|----------|---------|
| `VISION_PROVIDER` | `ark` or `openai` |
| `VISION_API_KEY` | API key (works for **any** provider, highest priority) |
| `VISION_BASE_URL` | Base URL up to (but not including) `/chat/completions` |
| `VISION_MODEL` | Model name to use |
| `VISION_ENV_FILE` | Explicit dotenv file path |

## API key resolution order

The key MUST be resolved before any request. Resolve in this exact order and
stop at the first source that yields a non-empty value:

1. **`VISION_API_KEY`** - universal override, works for any provider (preferred).
2. **Provider-specific env var**:
   - `ark` → `ARK_API_KEY`
   - `openai` → `OPENAI_API_KEY`
3. **Env file** - source a dotenv-style file if present. Try these paths in
   order until one exists:
   - `$VISION_ENV_FILE` (explicit override, if set)
   - `~/.env_vars`
   - `/root/.env_vars`

   Inside the file, check `VISION_API_KEY` first, then the provider-specific
   var for the current provider.
4. If none of the above yields a non-empty key:
   - Do NOT make the API request.
   - Report to the user which provider was attempted and which env vars were checked.

## Concrete resolution command

This logic is implemented in `scripts/resolve-config.sh`. Key resolution
order:

1.  **Dotenv pre-parse** - before applying provider defaults, read
    `VISION_PROVIDER`, `VISION_BASE_URL`, `VISION_MODEL` from dotenv files
    (only if not already set as env vars). This lets users configure the
    provider in `~/.env_vars` without exporting it.
2.  **Provider defaults** - apply `:=` defaults for `VISION_BASE_URL` and
    `VISION_MODEL` based on `VISION_PROVIDER`.
3.  **API key** - resolve in order: `VISION_API_KEY` env var →
    provider-specific env var (`ARK_API_KEY` / `OPENAI_API_KEY`) → dotenv
    files (safe grep parse, no sourcing).

```bash
: "${VISION_PROVIDER:=ark}"
: "${VISION_ENV_FILE:=}"

# Provider defaults
case "$VISION_PROVIDER" in
  ark)   KEY_ENV="ARK_API_KEY" ;;
  openai) KEY_ENV="OPENAI_API_KEY" ;;
  *) echo "ERROR: invalid VISION_PROVIDER"; exit 1 ;;
esac

# 1. VISION_API_KEY
KEY="${VISION_API_KEY:-}"
# 2. Provider-specific env
[ -z "$KEY" ] && eval "KEY=\"\${${KEY_ENV}:-}\""
# 3. Dotenv files (safe parse, no sourcing)
if [ -z "$KEY" ]; then
  for f in "$VISION_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
    [ -n "$f" ] && [ -f "$f" ] || continue
    KEY="$(grep -E "^\s*VISION_API_KEY=" "$f" | head -1 | sed -E 's/^\s*VISION_API_KEY=//; s/^"(.*)"$/\1/; s/^'"'"'(.*)'"'"'$/\1/')"
    [ -z "$KEY" ] && KEY="$(grep -E "^\s*${KEY_ENV}=" "$f" | head -1 | sed -E "s/^\s*${KEY_ENV}=//; s/^\"(.*)\"$/\1/; s/^'(.*)'$/\1/")"
    [ -n "$KEY" ] && break
  done
fi
[ -z "$KEY" ] && { echo "ERROR: no API key resolved"; exit 1; }
```

## Example `~/.env_vars`

```bash
# Provider config (optional, env vars take precedence)
VISION_PROVIDER=openai
VISION_BASE_URL=https://your-provider.com/v1
VISION_MODEL=your-vision-model

# Universal - works for any provider
VISION_API_KEY=«redacted:sk-…»

# OR provider-specific
ARK_API_KEY=xxxxxxxxxxxxxxxx
# OPENAI_API_KEY=«redacted:sk-…»
```

## Common configurations

### Doubao (default, no configuration needed)

```bash
export VISION_PROVIDER=ark
export ARK_API_KEY=your-ark-key
```

### OpenAI

```bash
export VISION_PROVIDER=openai
export OPENAI_API_KEY=sk-...
```

### Third-party OpenAI-compatible (e.g. OpenRouter, Azure, local vLLM, etc.)

```bash
export VISION_PROVIDER=openai
export VISION_API_KEY=sk-...
export VISION_BASE_URL=https://your-provider.com/v1
export VISION_MODEL=your-vision-model
```
