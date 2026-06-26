# π0 Related & Complementary Research (2025)

## Table of Contents
1. [π0 Direct Successors](#π0-direct-successors)
2. [Solving π0's Weaknesses](#solving-π0s-weaknesses)
3. [Parallel Approaches (Big Labs)](#parallel-approaches-big-labs)
4. [Practical Takeaways](#practical-takeaways)

---

## π0 Direct Successors

| Model | Date | Key Improvement |
|---|---|---|
| **π0** | 2024.10 | Original: VLM + Flow Matching + Action Chunking (H=50) |
| **π0-FAST** | 2025.02 | New tokenizer → 5× faster training; better generalization across embodiments |
| **π0.5** | 2025.04 | Open-world generalization; works in unseen environments via heterogeneous data co-training |
| **π0.6** | 2025.11 | RL fine-tuning — learns from experience to improve real-world success rate |

---

## Solving π0's Weaknesses

### 1. Inference Latency
**Real-Time Chunking (RTC)** — NeurIPS 2025
- Asynchronously generates the next action chunk *while* the current chunk executes
- No retraining required — plug-in compatible with any diffusion/flow VLA
- Eliminates motion pauses between chunks

### 2. Action Smoothness
**Streaming Flow Policy** (2025.05)
- Treats the action trajectory directly as a flow trajectory — simpler and cleaner formulation

**ManiFlow** (2025.09)
- Flow Matching + Consistency Training
- Faster, more accurate for high-dimensional action spaces

### 3. Training Efficiency / Data Cost
**UniVLA** (2025.05)
- Extracts latent actions from **unannotated video** via unsupervised methods
- No explicit action labels required — dramatically reduces data collection cost
- Key insight: recorded video of robot behavior can be used directly for training without manual annotation

---

## Parallel Approaches (Big Labs)

| Model | Lab | Architecture |
|---|---|---|
| **GR00T N1** | NVIDIA (2025.03) | Dual-system: System 1 (fast reflexes) + System 2 (slow VLM planning) |
| **Helix** | Figure AI (2025.02) | Whole-upper-body control; on-device GPU inference; multi-robot coordination |
| **OpenVLA-OFT** | Open Source | 7B params; 97.1% on LIBERO; optimized fine-tuning recipe |
| **DiVLA** | Academic | Autoregressive reasoning + Diffusion Policy; +20.9% zero-shot bin picking |
| **RDT-1B** | Academic | 1B params; specialized for bimanual manipulation |

---

## Practical Takeaways

### When to use which approach:

**For training efficiency with limited data:**
→ π0-FAST (faster convergence) + UniVLA (use raw video without action labels)

**For smooth real-time execution:**
→ RTC (async chunk generation) to eliminate motion pauses
→ ManiFlow or Streaming Flow Policy for smoother trajectories

**For long-horizon / semantic tasks:**
→ GR00T dual-system pattern: high-level VLM planner → low-level fast policy
→ π0 high-level policy decomposition (see SKILL.md)

**For fine-tuning on new tasks:**
→ π0 pre-train + fine-tune recipe
→ OpenVLA-OFT for open-source 7B baseline

### The three gaps π0 left open — all addressed by 2025:
1. **Training cost** → UniVLA (no action labels needed)
2. **Inference latency** → RTC (async chunk execution)
3. **Action smoothness** → ManiFlow / Streaming Flow Policy
