---
name: virtual-cell-reasoner-1.0.0
description: Consult a virtual cell language model on single-cell tasks — cell generation, cell understanding, cell perturbation, and biology Q&A using cell token sequences.
metadata: {"clawdbot":{"emoji":"🧬","requires":{"bins":["python"]}}}
---

# Virtual Cell LLM

A language model for single-cell biology. Cells are encoded as token sequences:

```
A-126 B-090 C-058 D-133 E-074 F-053
```

## Quick start

```bash
# Generate a cell from features
python call_api.py "Given the following cell features:\n\n[CellType] neuron\n\nProvide a cell language token sequence.\nReturn ONLY the tokens.\nNo extra text."

# Understand a cell from tokens
python call_api.py "The following tokens encode a cell\n\nA-168 B-090 C-005 D-069 E-232 F-196\nConstruct a requested feature summary based on this encoding:\n\n[CellType][Identity-Associated TFs][General TFs][Ligands][Receptors][TopExpressedGene]\nReturn ONLY canonical feature entries.\nIf a feature cannot be inferred from the tokens, use \"NA\".\n\nDo not provide additional text."

# Ask biology questions
python call_api.py "What transcription factors are associated with T cell identity?"
```

## Useful flags

- `--max-tokens N`     Max new tokens to generate (default: 2048)
- `--temperature F`    Sampling temperature (default: 0.7; lower = more deterministic)
- `--url URL`          Override server base URL (default: ngrok endpoint)
