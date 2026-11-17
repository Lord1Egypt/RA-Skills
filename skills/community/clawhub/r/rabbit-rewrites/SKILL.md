---
name: rabbit-rewrites
description: Rewrite the prose the engine flagged using a small local model over an OpenAI-compatible endpoint, instead of spending a frontier model on it. Use when the user wants to de-slop or humanize a draft offline, on a Raspberry Pi, in CI, or in a pre-commit hook, mentions llama.cpp, llama-server, Ollama, LM Studio, vLLM, or OpenRouter for writing work, asks which local model is good enough to clean up their writing, wants rewriting that costs no API tokens, or asks to benchmark or compare models on a rewriting task. Covers endpoint setup, planning what would be sent, applying gated rewrites in place, and measuring a model's pass rate.
license: MIT-0
homepage: https://github.com/whit3rabbit/rabbit-writes
metadata: {"version": "0.5.0", "openclaw": {"requires": {"bins": ["python3"]}, "envVars": [{"name": "RABBIT_MODEL_API_KEY", "required": false, "description": "API key for a remote --apply-model endpoint. Read only when scan.py runs with --apply-model. Never logged or persisted."}, {"name": "RABBIT_MODEL_BASE_URL", "required": false, "description": "Base URL of an OpenAI-compatible model endpoint. Read only when scan.py runs with --apply-model. There is no default endpoint and nothing is contacted without one."}, {"name": "RABBIT_MODEL_NAME", "required": false, "description": "Model name for --apply-model. Read only when scan.py runs with --apply-model. Falls back to local when unset."}]}}
---

# Model-backed rewriting

Detection in this plugin needs no model. `scan.py` is pure Python and runs on a Pi today. Rewriting is the part that needs one, and this is the path that uses a small local model for it rather than a frontier model.

**Paths.** `{baseDir}` below expands to this skill's own directory, the one holding this file. On a host that leaves the placeholder literal, resolve each path relative to that directory.

The design rests on three core principles: targeted chunking, persistent settings reuse, and gated execution.

## 1. Targeted chunking and context

Rather than sending entire documents (which exceed small model context windows and cause hallucinated edits), the engine chunks flagged prose into focused, contextual units:

- **Sentence units with local context**: A tell sitting in a sentence is chunked alongside its preceding sentence context. The model receives the target sentence, the specific problem to remove, and surrounding context to resolve pronoun referents, antecedents, and narrative tone without being asked to rewrite the context itself.
- **Passage and block units**: Structural and density tells (`uniformity`, `tier2-cluster`, `tier3-density`) are chunked at the full paragraph level, sized against the endpoint's input budget.
- **Unit merging**: Multiple findings landing within the same sentence are merged into a single rewrite unit, preventing colliding edits from invalidating the comparison baseline.

A 10,000-word draft with 40 findings becomes 40 focused 150- to 350-token requests, keeping token budgets tight while giving the model enough context to preserve flow.

## 2. Settings: Looked at and saved first

Always look for existing settings before prompting or reconfiguring. The engine checks configuration sources in this order:

1. `.rabbit-model` in the directory beside the document or the current working directory.
2. `.rabbit-model` at the repository root.
3. Environment variables: `$RABBIT_MODEL_BASE_URL`, `$RABBIT_MODEL_NAME`, `$RABBIT_MODEL_API_KEY`.

Save user configuration to `.rabbit-model` so settings persist and are automatically reused on every run:

```json
{
  "base_url": "http://127.0.0.1:8080/v1",
  "model": "qwen2.5-3b-instruct",
  "context_tokens": 4096,
  "max_output_tokens": 640,
  "temperature": 0.2,
  "disable_thinking": true
}
```

For hosted endpoints (e.g. OpenRouter), specify the environment variable holding the key (`api_key_env`) rather than committing raw keys:

```json
{
  "base_url": "https://openrouter.ai/api/v1",
  "model": "qwen/qwen3-4b-instruct",
  "api_key_env": "OPENROUTER_API_KEY"
}
```

## 3. Recommended models and download locations

Small local models (1.5B to 8B parameters) perform reliably when guided by strict prompts and the verification gate. Detailed download sources, commands, and quantization notes live in `references/models.md`.

| Model Family | Recommended Sizes | Primary Download Source | Ollama Tag |
|---|---|---|---|
| **Qwen 2.5 / 3** | 1.5B, 3B, 7B | Hugging Face (`Qwen/Qwen2.5-3B-Instruct-GGUF`) | `qwen2.5:1.5b`, `qwen2.5:3b`, `qwen2.5:7b` |
| **Gemma 2 / 4** | 2B, 9B, 26B (MLX) | Hugging Face (`google/gemma-2-2b-it-GGUF`) | `gemma2:2b`, `gemma2:9b`, `gemma4:26b-mlx` |
| **Llama 3.2 / 3.1** | 3B, 8B | Hugging Face (`meta-llama/Llama-3.2-3B-Instruct-GGUF`) | `llama3.2:3b`, `llama3.1:8b` |

### Suggested storage paths

- Local project directory: `./models/`
- User model cache: `~/.cache/llama.cpp/` or `~/.local/share/models/`
- LM Studio / Ollama cache: `~/.cache/lm-studio/models/` or `~/.ollama/models/`

### Serving an endpoint

```bash
# llama-server
llama-server -m ./models/qwen2.5-3b-instruct-q4_k_m.gguf --port 8080 -c 4096 --flash-attn

# Ollama (endpoint at http://127.0.0.1:11434/v1)
ollama serve
```

## 4. System prompt and editing rules

The rewriting system prompt blends plain-language simplification with targeted de-slopping:

```text
You are a copy editor. You rewrite one short passage at a time into clear, natural, and plain language.

Remove these machine-writing characteristics:
- Weird subject and verb combinations, and roundabout pseudo-epiphanies.
- Objects performing action verbs (keep actions for humans, groups, or agents; avoid phrases like "this file carries..." or "the module names...").
- Self-praise, AI hedges, and conversational padding.
- Distracting beats and unnecessary complexity.

Absolute rules:
- Keep every number, date, name, file path, URL, and quoted phrase exactly as written.
- Keep all markdown unchanged: code spans, links, list markers, headings, and emphasis.
- Leave fenced code blocks completely unchanged.
- Never use an em dash (—).
- Do not add facts, opinions, examples, or a closing summary sentence.
- Do not change the meaning. Say the same thing in plainer, everyday words.
- Reply ONLY with the rewritten passage and nothing else: no preamble, no commentary, no labels, no surrounding quotes, no code fence.
```

### Style presets
- **Default (Plain Language)**: Everyday vocabulary, active verbs, concise sentences.
- **TL;DR**: Short summary retaining every key fact, cutting length by half.
- **5-Year-Old (5y)**: Maximum simplicity, short conversational phrasing.

**Thinking / reasoning tokens:** Disabled by default (`"disable_thinking": true`, sending `reasoning_effort: "none"` and `enable_thinking: false`). Reasoning blocks consume the output token budget before the model emits the rewrite.

## 5. The gating mechanism

A small model is never trusted blindly:
1. **Fact preservation**: Every candidate must pass `verify.py` validation (numbers, dates, paths, code spans, quotes, and links must match exactly).
2. **Rescan validation**: A rescan verifies that the flagged tell is gone and no new tells were introduced.
3. **Retry loop**: Rejected completions are retried with the rejection reason appended. If all attempts fail, the original text is preserved untouched.

## Run it

Deterministic fixes first:
```bash
python3 {baseDir}/scripts/scan.py draft.md --apply-safe --write
```

Dry run / plan what would be sent:
```bash
python3 {baseDir}/scripts/scan.py draft.md --apply-model --model-plan
```

Apply model rewrites:
```bash
python3 {baseDir}/scripts/scan.py draft.md --apply-model
python3 {baseDir}/scripts/scan.py draft.md --apply-model --write
python3 {baseDir}/scripts/scan.py draft.md --apply-model --stdout | diff draft.md -
```

`--model-limit N` stops after N passages. `--model-attempts N` controls retry attempts per passage.

## Benchmarking models

Measure actual pass rates using the fixed 12-passage test battery:

```bash
python3 {baseDir}/scripts/bench.py --model-endpoint http://127.0.0.1:8080/v1 --model-name qwen2.5-3b
python3 {baseDir}/scripts/bench.py --repeat 3 --json > qwen2.5-3b.json
```

## What this will not do

- **Will not match a voice profile**: Matching a personal voice fingerprint requires broader context and a capable frontier model. Use `rabbit-writes` for voice conversion.
- **Will not touch code, tables, headings, or lists**: Only prose blocks are processed.
- **Will not alter safety band findings**: Any concealed instructions or prompt injections are rejected prior to sending.

## Where things live

| Path | What it holds |
| --- | --- |
| `{baseDir}/scripts/rwlib/endpoint.py` | endpoint configuration, resolution, and security checks |
| `{baseDir}/scripts/rwlib/rewrite.py` | unit planning, prompt templates, gate validation, retry loop |
| `{baseDir}/references/models.md` | recommended models, download sources, and endpoint setup |
| `{baseDir}/scripts/bench.py` | the model benchmarking runner |
| `{baseDir}/scripts/battery.json` | the twelve passages scored in the benchmark |
