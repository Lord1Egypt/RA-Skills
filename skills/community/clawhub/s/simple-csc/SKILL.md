---
name: simple-csc
description: >
  Use the simple-csc repository to perform Chinese Spelling Correction (CSC) and Chinese Character Error Correction (C2EC)
  using large language models in a training-free manner. Trigger when: user asks to correct Chinese text spelling errors,
  run CSC/C2EC experiments, evaluate correction results, set up the simple-csc environment, use LMCorrector API,
  start the correction API server, or work with Chinese text error correction datasets.
  Also trigger when code imports `lmcsc` or references `LMCorrector`.
compatibility: >
  Requires: NVIDIA GPU with CUDA support, Python 3.7+, ~16GB+ VRAM for 7B models.
  This skill is a usage guide for the simple-csc repository (https://github.com/Jacob-Zhou/simple-csc).
  The repository must be cloned locally before use. All file paths (configs/, scripts/, data/, etc.)
  are relative to the cloned repository root.
---

# Simple CSC

A training-free approach to Chinese Spelling Correction using LLMs as pure language models with beam search and distortion modeling.

## Prerequisites

This skill is a usage guide for the [simple-csc](https://github.com/Jacob-Zhou/simple-csc) repository. Before using any commands or APIs described here, clone the repository and work from its root:

```bash
git clone https://github.com/Jacob-Zhou/simple-csc.git
cd simple-csc
```

All paths referenced below (e.g., `configs/`, `scripts/`, `data/`, `eval/`, `datasets/`) are relative to this repository root. The repository contains the actual code, config files, data dictionaries, and scripts — this skill provides the knowledge of how to use them.

## Quick Reference

### Environment Setup

```bash
# Standard setup (creates venv, installs deps)
bash scripts/set_environment.sh

# For Qwen3 models
bash scripts/set_environment_qwen3.sh

# Recommended: install flash-attn for better performance and lower VRAM
pip install flash-attn --no-build-isolation
```

**Qwen2/Qwen2.5 warning**: Without flash-attn, set `torch_dtype=torch.bfloat16` to avoid unexpected behavior.

### Python API

```python
import torch
from lmcsc import LMCorrector

corrector = LMCorrector(
    model="Qwen/Qwen2.5-7B",
    prompted_model="Qwen/Qwen2.5-7B",       # use same model to save VRAM
    config_path="configs/c2ec_config.yaml",   # or "configs/default_config.yaml" for substitution-only
    torch_dtype=torch.bfloat16,               # recommended for Qwen2/2.5 without flash-attn
)

# Single sentence
outputs = corrector("完善农产品上行发展机智。")
# => [('完善农产品上行发展机制。',)]

# Batch
outputs = corrector(["句子一", "句子二"])

# With context (same length lists)
outputs = corrector(["未挨前兆"], contexts=["患者提问："])

# Streaming (batch_size=1 only)
for output in corrector("完善农产品上行发展机智。", stream=True):
    print(output[0][0], end="\r", flush=True)
```

### Config Selection

| Config | Use Case |
|--------|----------|
| `configs/default_config.yaml` | Substitution-only CSC (v1.0.0 style) |
| `configs/c2ec_config.yaml` | Full C2EC with insert/delete support (v2.0.0) |
| `configs/demo_config.yaml` | Same as c2ec_config, used by demo app |

Key difference: `c2ec_config.yaml` includes `ROR` (reorder), `MIS` (missing char), `RED` (redundant char) distortion types and `length_immutable_chars` data file.

### Recommended Models

- **v2.0.0 (C2EC)**: `Qwen/Qwen2.5-7B` or `Qwen/Qwen2.5-14B` — best performance/speed balance
- **v1.0.0 (CSC)**: `baichuan-inc/Baichuan2-13B-Base` — best performance
- Always prefer `Base` models over `Instruct`/`Chat` variants

### RESTful API Server

```bash
python api_server.py \
    --model "Qwen/Qwen2.5-7B" \
    --prompted_model "Qwen/Qwen2.5-7B" \
    --config_path "configs/c2ec_config.yaml" \
    --host 127.0.0.1 --port 8000 --workers 1 --bf16
```

Endpoints:
- `GET /health` — health check
- `POST /correction` — `{"input": "...", "stream": false, "contexts": null}`

```bash
# Non-streaming
curl -X POST 'http://127.0.0.1:8000/correction' \
  -H 'Content-Type: application/json' \
  -d '{"input": "完善农产品上行发展机智。"}'

# With context
curl -X POST 'http://127.0.0.1:8000/correction' \
  -H 'Content-Type: application/json' \
  -d '{"input": "未挨前兆", "contexts": "患者提问："}'
```

For detailed API parameters, config options, evaluation pipeline, and dataset formats, see [references/details.md](references/details.md).

## Key Architecture Concepts

The approach works by:
1. Using an LLM as a pure language model (left-to-right generation)
2. At each step, computing a distortion probability for each candidate token based on how "similar" it is to the observed (possibly erroneous) character
3. Combining LM probability with distortion probability via beam search
4. Distortion types encode the relationship between observed and candidate characters (identical, same pinyin, similar shape, etc.)

The `prompted_model` parameter adds a second probability source: a prompt-based LLM that scores candidates given the full input sentence as context, improving correction quality.
