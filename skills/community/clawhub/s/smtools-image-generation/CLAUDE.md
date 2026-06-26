# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SMTools-ImageGenerationSkill is a Python plugin ("skill") for the OpenClaw AI assistant framework. It generates images from text prompts using pluggable AI provider APIs (OpenRouter and Kie.ai).

## Commands

```bash
# First-time setup (creates venv, installs deps, scaffolds config.json and .env)
bash setup.sh

# Generate an image
bash scripts/run.sh -p "A cat in space"

# Generate with specific provider/model
bash scripts/run.sh -p "A sunset" --provider openrouter -m openai/gpt-image-1

# List available models for a provider
bash scripts/run.sh --list-models
bash scripts/run.sh --list-models --provider kie

# Run diagnostics (checks Python, venv, deps, API keys, output dir)
bash check.sh
```

There is no build step, test suite, or linter configured.

## Architecture

The project uses a **Strategy/Provider pattern**:

```
run.sh → generate.py (argparse CLI)
           ↓
       config_manager.load_config()    # .env + config.json + env var overrides
           ↓
       providers.get_provider(name)    # registry lookup in providers/__init__.py
           ↓
       provider.generate(prompt, model, output_path)
           ↓
       JSON to stdout + image saved to output/
```

- **`scripts/generate.py`** — Single CLI entry point. All output (success and error) is JSON to stdout. Auto-injects venv site-packages so it works without explicit venv activation.
- **`scripts/config_manager.py`** — Loads config with priority: env vars > `.env` > `config.json`.
- **`scripts/providers/base_provider.py`** — Abstract base class (`BaseImageProvider`) with three abstract methods: `generate()`, `list_models()`, `validate_config()`.
- **`scripts/providers/__init__.py`** — Provider registry (`PROVIDERS` dict + `get_provider()` factory).
- **`scripts/providers/openrouter_provider.py`** — Working OpenRouter implementation (synchronous HTTP).
- **`scripts/providers/kie_provider.py`** — Kie.ai implementation (async task + polling). **Note: API endpoints and response fields are unverified/placeholder (see TODOs).**

## Adding a New Provider

1. Create `scripts/providers/new_provider.py` implementing `BaseImageProvider`
2. Register it in `scripts/providers/__init__.py` `PROVIDERS` dict
3. Add its config block to `assets/config.example.json`
4. Map its API key env var in `scripts/config_manager.py`

## Configuration

- **`config.json`** (gitignored) — Created from `assets/config.example.json` by `setup.sh`
- **`.env`** (gitignored) — API keys (`OPENROUTER_API_KEY`, `KIE_API_KEY`)
- **`SKILL.md`** — OpenClaw skill definition (YAML frontmatter + agent instructions)

## Key Conventions

- All CLI output must be valid JSON (`{"status": "success", ...}` or `{"status": "error", "error": "..."}`) for OpenClaw integration.
- API keys must never be logged, displayed, or committed. `.env` and `config.json` are gitignored.
- Python 3.8+ required. Only two external deps: `requests` and `python-dotenv`.
