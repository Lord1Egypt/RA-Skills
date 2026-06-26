# π0 Architecture Reference

## Table of Contents
1. [Model Overview](#model-overview)
2. [Input/Output Structure](#inputoutput-structure)
3. [Flow Matching](#flow-matching)
4. [Mixture-of-Experts Design](#mixture-of-experts-design)
5. [Attention Masking](#attention-masking)
6. [Inference Details](#inference-details)

---

## Model Overview

π0 is a **Vision-Language-Action (VLA) flow model** combining:
- **PaliGemma** (3B params) as the VLM backbone — initialized from internet-scale pre-training
- **Action expert** (~300M params, width=1024, mlp_dim=4096) — initialized from scratch
- **Flow matching** for continuous action generation

Total: ~3.3B parameters.

---

## Input/Output Structure

**Observations at timestep t:**
```
o_t = [I¹_t, ..., Iⁿ_t,  ℓ_t,  q_t]
       ──────────────────  ────  ────
       RGB images (2-3)    lang  proprioception (joint angles)
```

**Output — Action chunk:**
```
A_t = [a_t, a_{t+1}, ..., a_{t+H-1}]     H = 50
```

Action dimensions vary by robot (7–17); smaller robots zero-padded.

---

## Flow Matching

Flow matching generates continuous action distributions without discretization.

**Training:**
1. Sample noise: `ε ~ N(0, I)`
2. Create noisy actions: `A^τ_t = τ·A_t + (1-τ)·ε`  where `τ ∈ [0,1]`
3. Train network to predict vector field: `u(A^τ_t | A_t) = ε - A_t`
4. Loss: `L^τ(θ) = E[‖v_θ(A^τ_t, o_t) − u(A^τ_t | A_t)‖²]`

**Inference:**
- Integrate learned vector field from τ=0 → τ=1
- Forward Euler integration, δ=0.1, 10 steps total
- Start from pure noise, denoise into action chunk

**Timestep sampling:**
- Shifted beta distribution emphasizing lower (noisier) τ values
- Cutoff at s=0.999
- Rationale: observations are highly informative → action distribution is tighter than image synthesis → emphasis on harder denoising steps less critical

---

## Mixture-of-Experts Design

Inspired by Transfusion paper. Two experts share the same transformer layers but have **separate weight sets**:

| Expert | Processes | Initialization |
|---|---|---|
| VLM backbone | Images + language tokens | PaliGemma weights |
| Action expert | Robot state (q_t) + noisy actions (A^τ_t) | Random |

- Experts interact **only through self-attention** layers
- Action expert uses reduced dimensions for faster inference
- This design lets the VLM backbone preserve its pre-trained representations while the action expert learns robot-specific dynamics

---

## Attention Masking

**Blockwise causal attention** with 3 blocks:

```
Block 1: [images, language]   ← full self-attention within block
Block 2: [state]              ← attends to Block 1 + Block 2
Block 3: [noisy actions]      ← attends to Block 1 + Block 2 + Block 3
```

- Block 1 tokens do NOT attend to Block 2 or Block 3
- This enables **KV caching** of Block 1 during flow matching integration (10 inference steps reuse the same visual+language KV cache)

---

## Inference Details

- **Total inference time:** ~73ms on RTX 4090
- **Execution mode:** Open-loop action chunks
  - 50Hz robots: new chunk every 0.5s
  - 20Hz robots: new chunk every 0.8s
- **No temporal ensembling** — found to hurt performance (contradicts some prior work)
- KV cache for Block 1 (images + language) across all 10 denoising steps saves significant compute
