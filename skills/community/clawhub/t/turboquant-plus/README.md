# TurboQuant+ Skill

OpenClaw skill for configuring TurboQuant+ KV cache compression with llama.cpp on Apple Silicon.

## Quick Start

```bash
# Install the llama.cpp TurboQuant fork
git clone https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant
cmake -B build -DGGML_METAL=ON && cmake --build build --config Release

# Run with turbo4 (best quality/compression balance)
./build/bin/llama-server -m model.gguf --cache-type-k turbo4 --cache-type-v turbo4 -fa 1
```

## Compression Levels

| Format | Bits | Compression | PPL vs q8_0 | Best For |
|--------|------|-------------|-------------|----------|
| turbo4 | 4-bit | 3.8x | +0.23% | Default choice, best quality |
| turbo3 | 3-bit | 4.6-5.1x | +1.06% | Maximum memory savings |
| turbo2 | 2-bit | 6.4x | +6.48% | Extreme compression, asymmetric V |

## Tips

- **Start with turbo4** — closest to q8_0 quality at 2x the compression
- **Use asymmetric K/V for Q4_K_M models** — `--cache-type-k q8_0 --cache-type-v turbo4`
- **Enable Flash Attention** — always add `-fa 1`
- **104B models run on a MacBook** — turbo3 + 128GB Mac + raised GPU memory cap

## Project

- Repository: [turboquant_plus](../turboquant_plus/)
- llama.cpp Fork: [TheTom/llama-cpp-turboquant](https://github.com/TheTom/llama-cpp-turboquant)
