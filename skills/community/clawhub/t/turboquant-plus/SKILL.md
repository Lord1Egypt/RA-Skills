# TurboQuant+ — KV Cache Compression for Local LLM Inference

> Accelerate local LLM inference on Apple Silicon with 3.8-6.4x KV cache compression via PolarQuant + Walsh-Hadamard rotation.

## Trigger Keywords
量化, KV压缩, 本地推理, llama.cpp, turboquant, KV cache, compression, Apple Silicon, Metal, turbo2, turbo3, turbo4

## Overview

TurboQuant+ implements [TurboQuant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) (ICLR 2026) for llama.cpp with Metal GPU kernels. It compresses the transformer KV cache to squeeze larger models and longer contexts into limited Apple Silicon memory — with minimal quality loss.

### Core Capabilities
- **turbo2** (2-bit, 6.4x compression) — Extreme memory savings, +6.48% PPL. Best for asymmetric V-only compression.
- **turbo3** (3-bit, 4.6-5.1x compression) — Maximum memory savings with acceptable quality. +1.06% PPL vs q8_0.
- **turbo4** (4-bit, 3.8x compression) — Best quality/compression tradeoff. +0.23% PPL vs q8_0, closer to q8_0 than q4_0.
- **Asymmetric K/V** — Keep K at q8_0 for attention quality, compress V aggressively. Rescues quality on low-bit weight models.
- **Boundary V** — Layer-aware V compression (first 2 + last 2 layers at q8_0, rest turbo2). Recovers 37-91% of quality gap.
- **Sparse V dequant** — Skip low-weight V positions during decode. +22.8% decode speed at 32K context, no PPL impact.

## Dependencies
None. Works with the [llama.cpp TurboQuant fork](https://github.com/TheTom/llama-cpp-turboquant).

## Configuration Guide

### Basic Usage (llama-server)

```bash
# Recommended default — turbo4 symmetric
llama-server -m model.gguf --cache-type-k turbo4 --cache-type-v turbo4 -fa 1

# Maximum compression — turbo3 symmetric
llama-server -m model.gguf --cache-type-k turbo3 --cache-type-v turbo3 -fa 1

# Extreme compression — turbo2 (best with asymmetric)
llama-server -m model.gguf --cache-type-k q8_0 --cache-type-v turbo2 -fa 1
```

### Asymmetric K/V (for Q4_K_M models)

Some low-bit weight models degrade with symmetric turbo. Use asymmetric K/V:

```bash
# K stays at q8_0, V compressed with turbo
llama-server -m model-Q4_K_M.gguf --cache-type-k q8_0 --cache-type-v turbo4 -fa 1

# Even more V compression
llama-server -m model-Q4_K_M.gguf --cache-type-k q8_0 --cache-type-v turbo3 -fa 1
```

> **Note**: Larger models (70B, 104B) handle symmetric turbo fine. Asymmetric mainly benefits smaller Q4_K_M models.

### Long Context on Large Models

For 70B+ models at 32K+ context on 128GB Macs, raise the GPU memory cap:

```bash
# Set to 90% of 128GB
sudo sysctl iogpu.wired_limit_mb=117964

# Then run with turbo3 for maximum context
llama-server -m Llama-70B-Q4_K_M.gguf --cache-type-k turbo3 --cache-type-v turbo3 -c 65536 -fa 1
```

### Recommended Configs by Scenario

| Scenario | K cache | V cache | Compression | PPL impact |
|----------|---------|---------|-------------|------------|
| **Best quality** | turbo4 | turbo4 | 3.8x | +0.23% |
| **Balanced** | turbo3 | turbo3 | 4.6-5.1x | +1.06% |
| **Max compression** | turbo2 | turbo2 | 6.4x | +6.48% |
| **Q4_K_M safe** | q8_0 | turbo4 | ~3.8x V | +1.0% |
| **Boundary V** | q8_0 | turbo2 | ~6x V | 37-91% quality recovered |

## Apple Silicon Benchmarks (M5 Max 128GB)

### Quality (wikitext-2)

| Cache | Compression | PPL | vs q8_0 |
|-------|-------------|-----|---------|
| q8_0 | 1.9x | 6.111 | baseline |
| **turbo4** | **3.8x** | **6.125** | **+0.23%** |
| turbo3 | 4.6x | 6.176 | +1.06% |
| turbo2 | 6.4x | 6.507 | +6.48% |

### Large Model Results

| Model | Config | PPL | Context | NIAH |
|-------|--------|-----|---------|------|
| Llama-70B Q4_K_M | turbo4/turbo4 | 3.461 | 48K | 30/30 |
| Command-R+ 104B Q4_K_M | turbo3/turbo3 | 6.415 | **128K** | 10/10 |

### Speed

- **Prefill**: turbo3 matches or exceeds q8_0 speed (1.0-1.1x)
- **Decode**: turbo4 at ~0.93x q8_0, turbo3 at ~0.78-0.90x q8_0
- **Sparse V**: +22.8% decode at 32K context, no quality loss

### M1 Max 64GB Results (Community)

| KV | Prefill t/s | Decode t/s | vs q8_0 |
|----|------------|-----------|---------|
| q8_0 | 399.0 | 12.4 | — |
| **turbo4** | **365.0** | **16.6** | **+33.9%** |

## Key Research Findings

1. **V compression is free** — Compressing V to 2-bit has zero measurable effect when K precision is maintained. Validated on Metal, CUDA RTX 4090, RTX 3090.
2. **All quality loss comes from K compression** — This is why asymmetric configs rescue quality.
3. **Boundary layers are sensitive** — Protecting first 2 + last 2 layers recovers 37-91% of quality gap.
4. **turbo4 beats q4_0 in quality** — Lower KL divergence, higher top-p agreement, at similar compression.

## References
- [Getting Started Guide](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/getting-started.md)
- [Configuration Recommendations](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/turboquant-recommendations.md)
- [TurboQuant Paper (Google Research)](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)
- [Asymmetric K/V Compression](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/asymmetric-kv-compression.md)
- [M5 Max Stress Test](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/m5-max-stress-test.md)
