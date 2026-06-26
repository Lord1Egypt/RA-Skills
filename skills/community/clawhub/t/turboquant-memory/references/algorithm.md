# TurboQuant Algorithm Reference

## Overview

TurboQuant (ICLR 2026, Google Research) is a near-optimal vector quantization algorithm that compresses high-dimensional vectors to 3-8 bits per coordinate with provably minimal distortion. It is **data-oblivious** (no training/calibration needed) and works **online** (each vector quantized independently).

Paper: [arXiv:2504.19874](https://arxiv.org/abs/2504.19874)

## How It Works

**Blockwise Hadamard Rotation → Predictable Distribution → Optimal Scalar Quantization**

1. **Blockwise rotation**: Split the vector into power-of-2 blocks (e.g., 3072 = 3 × 1024). Per block, multiply by random ±1 signs, then apply the Fast Walsh-Hadamard Transform. This is fully invertible and makes coordinates approximately independent with a known distribution ≈ N(0, 1/d).

2. **Lloyd-Max quantization**: Since coordinates now follow a predictable distribution, apply a precomputed optimal scalar quantizer to each coordinate independently. Codebooks are precomputed for standard normal and hardcoded for 4-8 bit widths.

3. **Per-vector scale**: Store a single scale factor (the std of rotated coordinates) to adapt the global codebook to each vector's dynamic range.

### Why Blockwise Hadamard?

The original TurboQuant paper uses a full random orthogonal matrix (QR decomposition). We use blockwise Hadamard instead because:

- **O(d log d)** computation vs O(d³) for QR
- **O(d)** memory (just sign vectors) vs O(d²) for full matrix
- **Fully invertible** — no information loss
- **Identical quality** on real embeddings (verified via ablation)

Important: Subsampled Randomized Hadamard Transform (SRHT) — where you pad to a larger power of 2 then subsample back — introduces **irreversible information loss** and should NOT be used. Our ablation showed it creates a hard MSE floor that makes bit-width increases ineffective.

## Two Modes

### TurboQuantMSE (Recommended)
- Uses all b bits for MSE-optimal quantization
- Best for: cosine similarity search, retrieval, RAG, memory search
- **Recommended as default** for most use cases

### TurboQuantProd
- Uses (b-1) bits for MSE + 1 bit for QJL residual correction
- Theoretically provides unbiased inner product estimation
- In practice: only beneficial for very large databases (10k+) or ultra-low bit (2-3 bit)
- Not recommended as default for small/medium collections

## Choosing Bit-Width

| Bits | Compression | Cosine Similarity | Recall@1 | Recommended For |
|------|-------------|-------------------|----------|-----------------|
| 3 | ~10.6x | 0.982 | ~88% | Maximum compression, approximate search |
| 4 | ~8.0x | 0.995 | ~92% | Large-scale, storage-constrained |
| **5** | **~6.4x** | **0.999** | **~98%** | **Default — best quality/compression tradeoff** |
| 6 | ~5.3x | 1.000 | ~98% | Conservative, high-fidelity |
| 7 | ~4.6x | 1.000 | ~100% | Near-lossless |
| 8 | ~4.0x | 1.000 | ~100% | Maximum quality |

## Dimension Considerations

- **d ≥ 128**: Algorithm works well
- **d = 768** (many sentence transformers): Good
- **d = 1536** (OpenAI text-embedding-3-large): Very good
- **d = 3072** (Gemini embedding-001): Excellent — higher dimensions improve quantization quality

Higher dimensions → better quantization quality (concentration of measure).

The blockwise decomposition automatically handles any dimension by splitting into the largest possible power-of-2 blocks. For example:
- 3072 = 3 × 1024
- 1536 = 1024 + 512
- 768 = 512 + 256

## Theoretical Guarantees

- MSE within **2.7x** of information-theoretic lower bound (Shannon)
- **Zero indexing time** — no offline training, no codebook learning
- **Deterministic** — same seed produces identical quantization
- Provably near-optimal across all bit-widths and dimensions
