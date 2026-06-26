---
name: translate-txt
description: |
    Translate text files using OpenAI-compatible APIs (e.g. SiliconFlow, DeepSeek, OpenAI).
    Use when the user wants to: translate a txt file, translate text to Chinese or other languages,
    batch translate documents, or convert foreign language txt files to Chinese.
    Triggers: 翻译txt文件, 翻译文本, translate txt, translate file, 文件翻译, txt翻译.
metadata:
    config:
        - key: TRANSLATE_API_KEY
          description: API key for the translation service
          required: true
        - key: TRANSLATE_BASE_URL
          description: Base URL for OpenAI-compatible API
          default: https://api.siliconflow.cn/v1
        - key: TRANSLATE_MODEL
          description: Model name to use
          default: Qwen/Qwen2.5-7B-Instruct
---

# translate-txt Skill

Translate `.txt` files using any OpenAI-compatible API. Defaults to SiliconFlow with Qwen model, translating foreign languages to Chinese.

## Features

- Supports any OpenAI-compatible API (SiliconFlow, DeepSeek, OpenAI, etc.)
- Auto-detects source language, defaults to translating into Chinese
- Handles large files by chunking at paragraph/sentence boundaries
- **Concurrent translation** — multiple chunks translated in parallel
- **Sliding-window context** — each chunk gets glossary + background from nearby chunks; new terms auto-propagate, stale context naturally fades as the window slides
- Automatic retry with exponential backoff on timeout and transient errors
- Preserves original formatting and structure

## File Structure

```
translate-txt/
├── SKILL.md              # Skill definition
├── .env                  # User configuration (created by setup)
├── setup.sh              # Setup script (interactive & non-interactive)
└── scripts/
    └── translate.py      # Translation script
```

## Configuration

The script reads config from the `.env` file in the skill root directory, falling back to environment variables.

| Variable | Default | Description |
|---|---|---|
| `TRANSLATE_API_KEY` | (none, required) | API key for the translation service |
| `TRANSLATE_BASE_URL` | `https://api.siliconflow.cn/v1` | Base URL for OpenAI-compatible API |
| `TRANSLATE_MODEL` | `Qwen/Qwen2.5-7B-Instruct` | Model name to use |
| `TRANSLATE_THINKING` | `auto` | Thinking mode: `auto`/`disabled` (recommended) or `enabled` |
| `TRANSLATE_MAX_TOKENS` | `4096` | Max output tokens per chunk |
| `TRANSLATE_TEMPERATURE` | `1` | Model temperature |
| `TRANSLATE_TIMEOUT` | `300` | API request timeout in seconds |

Priority: environment variables > `.env` file > defaults.

## How to Use

### Step 1: Check & Setup Configuration

Before first use, check if the API key is configured. The script loads config from the `.env` file in the skill directory, falling back to environment variables.

**If `.env` does not exist or `TRANSLATE_API_KEY` is empty**, ask the user for their API key and preferred provider, then run:

```bash
# Non-interactive setup (for AI agent):
bash ~/.comate/skills/translate-txt/setup.sh --api-key <KEY> --provider <PROVIDER>

# Providers: siliconflow (default), deepseek, openai
# Or specify full config:
bash ~/.comate/skills/translate-txt/setup.sh --api-key <KEY> --base-url <URL> --model <MODEL>
```

**Examples:**
```bash
# SiliconFlow (default)
bash ~/.comate/skills/translate-txt/setup.sh --api-key sk-xxx --provider siliconflow

# DeepSeek
bash ~/.comate/skills/translate-txt/setup.sh --api-key sk-xxx --provider deepseek

# OpenAI
bash ~/.comate/skills/translate-txt/setup.sh --api-key sk-xxx --provider openai

# Custom endpoint
bash ~/.comate/skills/translate-txt/setup.sh --api-key sk-xxx --base-url https://my-api.example.com/v1 --model my-model
```

The user can also run the interactive setup manually:
```bash
bash ~/.comate/skills/translate-txt/setup.sh
```

On success, the script outputs `CONFIG_SAVED:<path>`. If the API key is already configured, skip to Step 2.

### Step 2: Run Translation

```bash
python3 ~/.comate/skills/translate-txt/scripts/translate.py <input_file> [options]
```

**Options:**
- `--output <path>` - Output file path (default: `<input>_translated.txt`)
- `--target-lang <lang>` - Target language (default: `Chinese`)
- `--source-lang <lang>` - Source language hint (default: `auto` for auto-detect)
- `--chunk-size <int>` - Max characters per chunk (default: `3000`)
- `--concurrency <int>` - Max concurrent API calls (default: `3`)
- `--context-window <int>` - Number of preceding chunks for sliding context (default: `3`)

**Examples:**

```bash
# Translate a file to Chinese (default)
python3 ~/.comate/skills/translate-txt/scripts/translate.py document.txt

# Translate to Japanese
python3 ~/.comate/skills/translate-txt/scripts/translate.py document.txt --target-lang Japanese

# Specify output path
python3 ~/.comate/skills/translate-txt/scripts/translate.py document.txt --output result.txt
```

### Step 3: Report Result

After the script completes successfully, it outputs the translated file path in the format `OUTPUT:<path>`. Report this to the user.

If the script fails, check the error output:
- `CONFIG_ERROR` - API key not configured. Ask user for their API key, then run `setup.sh --api-key <KEY> --provider <PROVIDER>`
- `FILE_ERROR` - Input file not found or empty
- `API_ERROR` - API call failed (check key, URL, model, and network)

## How It Works

The script uses a three-step approach for multi-chunk files:

**Step 1: Keyword extraction** — Each chunk is processed concurrently with a lightweight prompt to extract proper nouns and domain terms with their translations.

**Step 2: Build per-chunk context** — For each chunk, the script merges keywords from a sliding window of N preceding chunks (default `--context-window 3`). This means:
- New terms introduced in later chapters automatically appear in context for subsequent chunks
- Context naturally shifts as the window slides forward (e.g., chunk 10's context reflects chunks 7-10, not chunks 1-3)
- A background description is inferred from initial chunks and prepended to all contexts

**Step 3: Translation** — All chunks are translated concurrently, each with its own window-scoped context.

Use `--context-window` to control the window size. Larger windows provide more context but may include irrelevant terms from distant sections.

Progress is reported on stderr:
- `KEYWORDS:chunk N/M` / `KEYWORDS_DONE:chunk N/M` (Step 1)
- `TRANSLATING:chunk N/M` / `DONE:chunk N/M` (Step 3)

Results are reassembled in original order.

## Model Selection & Performance

Model choice has a dramatic impact on translation speed. The main factor is whether the model uses **thinking/reasoning mode** — thinking models spend significant time on internal reasoning, which is unnecessary for translation and makes them **5-10x slower**.

**Recommended models (fast, good quality):**

| Model | Provider/Endpoint | Speed | Quality | Notes |
|---|---|---|---|---|
| `deepseek-v3` / `deepseek-v3.2` | DeepSeek or compatible | Fast (~1.5min/28K chars) | Good | Best choice for translation |
| `gpt-4o-mini` | OpenAI | Fast | Good | Cost-effective |
| `Qwen/Qwen2.5-7B-Instruct` | SiliconFlow | Moderate | Decent | Default, good balance |

**Models to avoid for translation:**

| Model | Why |
|---|---|
| `kimi-k2.5` | Thinking model — ~13min/28K chars, 8x slower |
| `kimi-k2-thinking` | Same issue, even more reasoning overhead |
| `deepseek-r1` | Reasoning model, slow for straightforward translation |

**Tips:**
- The script passes `enable_thinking: false` by default (`TRANSLATE_THINKING=auto`). If your API doesn't support this, switch to a non-thinking model.
- For batch translations or large files, prefer `deepseek-v3` or `deepseek-v3.2`.

## Notes

- The script uses only Python standard library (no pip install needed)
- Translation quality depends on the model; larger models generally produce better translations
- Keyword extraction adds one API call per chunk but ensures every term is captured
- Set `--concurrency 1` to disable parallel translation if the API has strict rate limits
- The script preserves original text formatting (paragraphs, line breaks) in the translation
- **Avoid thinking/reasoning models** for translation — much slower with no quality benefit
- **Sliding-window context scales to any text length** — 10 chunks or 1000 chunks work the same way
