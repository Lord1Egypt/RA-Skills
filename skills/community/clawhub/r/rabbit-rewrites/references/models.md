# Models and Download Locations

Small local models for offline, fast, and private prose rewriting with `rabbit-rewrites`.

## Suggested Models and Download Locations

### 1. Qwen 2.5 / 3 (Recommended)
Excellent instruction-following for constrained JSON and strict rewriting tasks.

- **Qwen2.5-1.5B-Instruct (GGUF)**: Ultra-lightweight, runs on Raspberry Pi 4/5 or low-power hardware.
  - Hugging Face: `Qwen/Qwen2.5-1.5B-Instruct-GGUF`
  - Ollama: `ollama pull qwen2.5:1.5b`
  - Download file: `qwen2.5-1.5b-instruct-q4_k_m.gguf`
- **Qwen2.5-3B-Instruct (GGUF)**: Strong balance between speed and preservation.
  - Hugging Face: `Qwen/Qwen2.5-3B-Instruct-GGUF`
  - Ollama: `ollama pull qwen2.5:3b`
  - Download file: `qwen2.5-3b-instruct-q4_k_m.gguf`
- **Qwen2.5-7B-Instruct (GGUF)**: High precision, very low hallucination rate on facts.
  - Hugging Face: `Qwen/Qwen2.5-7B-Instruct-GGUF`
  - Ollama: `ollama pull qwen2.5:7b`
  - Download file: `qwen2.5-7b-instruct-q4_k_m.gguf`

### 2. Google Gemma 2 / 4
Natural phrasing, strong vocabulary variety.

- **Gemma 2 2B Instruct**: Fast local rewrite engine.
  - Hugging Face: `google/gemma-2-2b-it-GGUF`
  - Ollama: `ollama pull gemma2:2b`
  - Download file: `gemma-2-2b-it-Q4_K_M.gguf`
- **Gemma 2 9B Instruct**: Exceptional prose fluency.
  - Hugging Face: `google/gemma-2-9b-it-GGUF`
  - Ollama: `ollama pull gemma2:9b`
- **Gemma 4 (MLX / Apple Silicon)**:
  - Local MLX / Ollama: `ollama pull gemma4:26b-mlx`

### 3. Meta Llama 3.2 / 3.1
Robust general-purpose instruction following.

- **Llama-3.2-3B-Instruct (GGUF)**:
  - Hugging Face: `meta-llama/Llama-3.2-3B-Instruct-GGUF`
  - Ollama: `ollama pull llama3.2:3b`
  - Download file: `Llama-3.2-3B-Instruct-Q4_K_M.gguf`
- **Llama-3.1-8B-Instruct (GGUF)**:
  - Hugging Face: `meta-llama/Llama-3.1-8B-Instruct-GGUF`
  - Ollama: `ollama pull llama3.1:8b`

---

## Suggested Local Storage Paths

Store models in a standard directory so multiple tools (`llama-server`, LM Studio, Ollama) can share or locate them:

- **Local project path**: `./models/`
- **User cache / llama.cpp**: `~/.cache/llama.cpp/` or `~/.local/share/models/`
- **LM Studio default**: `~/.cache/lm-studio/models/`
- **Ollama default**: `~/.ollama/models/`

### Direct CLI Download Examples

```bash
# Using huggingface-cli
huggingface-cli download Qwen/Qwen2.5-3B-Instruct-GGUF qwen2.5-3b-instruct-q4_k_m.gguf --local-dir ./models

# Using curl to download a specific GGUF quant
curl -L -o ./models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

---

## Serving Endpoints

### 1. llama-server (llama.cpp)
```bash
llama-server -m ./models/qwen2.5-3b-instruct-q4_k_m.gguf --port 8080 -c 4096 --flash-attn
```

### 2. Ollama
```bash
ollama serve
# API is available at http://127.0.0.1:11434/v1
```

### 3. LM Studio / vLLM / OpenRouter
- LM Studio: Start Local Server on port 1234 (`http://127.0.0.1:1234/v1`)
- OpenRouter / Hosted: `https://openrouter.ai/api/v1` (requires `$OPENROUTER_API_KEY`)

---

## Saved Settings (`.rabbit-model`)

Settings are looked at and reused first before any prompt. Drop `.rabbit-model` at the project root or beside the target document:

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
