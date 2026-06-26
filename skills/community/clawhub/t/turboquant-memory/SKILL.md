---
name: turboquant-memory
description: >
  Compress and accelerate vector search in memory/RAG systems using TurboQuant
  (ICLR 2026) — near-optimal vector quantization with 5-8x compression and 98%+
  search accuracy. Uses blockwise Hadamard rotation + Lloyd-Max scalar quantization.
  Use when: (1) optimizing embedding storage size, (2) speeding up semantic search,
  (3) user mentions "compress embeddings", "quantize vectors", "memory optimization",
  "faster search", "TurboQuant", "vector compression", or "embedding compression",
  (4) reducing memory footprint of RAG systems. Works with any embedding model
  (Gemini, OpenAI, Cohere, local) and any dimension ≥ 128. No GPU required. numpy only.
---

# TurboQuant Memory

Compress embedding vectors 5-8x with 98%+ search accuracy using TurboQuant (Google, ICLR 2026).

## Quick Start

### 1. Run tests

```bash
python3 scripts/turboquant.py
```

15 built-in tests: FWHT correctness, MSE distortion, IP correlation, recall, compression ratio, determinism.

### 2. Validate on your data

```bash
python3 scripts/validate.py --db /path/to/memory.sqlite --auto-detect --bits 5
```

Auto-detects sqlite-vec `vec0` tables, analyzes distribution, reports quantization quality and recall.

### 3. Quantize a memory database

```bash
python3 scripts/memory_quantize.py --db /path/to/memory.db --bits 5 --benchmark
python3 scripts/memory_quantize.py --db /path/to/memory.db --bits 5 --migrate
```

### 4. Integrate into code

```python
from turboquant import TurboQuantMSE

# Initialize (deterministic — same seed = same quantization)
tq = TurboQuantMSE(dim=3072, bits=5)

# Quantize for storage
stored = tq.quantize(embedding_vector)  # float32 → compressed

# Reconstruct
reconstructed = tq.dequantize(stored)   # compressed → float32

# Search: query stays float32, database is quantized
q_rot = tq.rotation.apply(query)
for doc in database:
    score = doc['norm'] * doc['scale'] * np.dot(q_rot, tq.codebook[doc['indices']])
```

## Recommended Configuration

| Preset | Mode | Bits | R@1 | Compression | Use Case |
|--------|------|------|-----|-------------|----------|
| **Default** | MSE | **5** | **98%** | **6.4x** | Most memory/RAG search |
| Conservative | MSE | 6 | 98%+ | 5.3x | High-fidelity retrieval |
| Aggressive | MSE | 4 | 92% | 8.0x | Large-scale, storage-constrained |

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `dim` | auto-detect | Embedding dimension (768, 1536, 3072, etc.) |
| `bits` | 5 | Bits per coordinate. See table above. |
| `seed` | 42 | Rotation seed. Same seed = reproducible quantization. |

## Algorithm

**Blockwise Hadamard Rotation → Lloyd-Max Scalar Quantization**

1. Split vector into power-of-2 blocks (e.g., 3072 = 3 × 1024)
2. Per block: random sign flip + Fast Walsh-Hadamard Transform (fully invertible)
3. Per-vector scale normalization
4. Lloyd-Max optimal scalar quantizer per coordinate (precomputed codebook for N(0,1))
5. Pack indices into compact bit representation

Key properties:
- **Data-oblivious**: no training or calibration needed
- **Fully invertible**: zero information loss from rotation
- **Near-optimal**: within 2.7x of Shannon information-theoretic lower bound
- **Deterministic**: same seed = same output

See [references/algorithm.md](references/algorithm.md) for full details.

## Benchmark (Gemini embedding-001, 3072-dim, 112 vectors)

| Bits | MSE | Cosine | R@1 | R@5 | R@10 | Bytes/vec | Compression |
|------|-----|--------|-----|-----|------|-----------|-------------|
| 3 | 1.1e-5 | 0.982 | 88% | 90% | 91% | 1,160 | 10.6x |
| 4 | 3.2e-6 | 0.995 | 92% | 93% | 93% | 1,544 | 8.0x |
| **5** | **8.2e-7** | **0.999** | **98%** | **96%** | **96%** | **1,928** | **6.4x** |
| 6 | 2.2e-7 | 1.000 | 96% | 98% | 98% | 2,312 | 5.3x |
| 7 | 8e-8 | 1.000 | 100% | 98% | 99% | 2,696 | 4.6x |
| 8 | 3e-8 | 1.000 | 98% | 98% | 99% | 3,080 | 4.0x |

## Compatibility

- Python 3.9+, **numpy only** (no scipy, no GPU)
- Any embedding dimension ≥ 128
- Any embedding model (Gemini, OpenAI, Cohere, sentence-transformers, etc.)
- SQLite / sqlite-vec `vec0` tables (auto-detected)

## References

- TurboQuant paper: [arXiv:2504.19874](https://arxiv.org/abs/2504.19874) (ICLR 2026)
- PolarQuant paper: [arXiv:2502.02617](https://arxiv.org/abs/2502.02617) (AISTATS 2026)
