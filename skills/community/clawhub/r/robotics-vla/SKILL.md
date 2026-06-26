---
name: robotics-vla
description: >
  Expert guidance for Vision-Language-Action (VLA) robot foundation models — covering architecture design, training pipelines, data strategy, deployment, and evaluation. Use when (1) designing or implementing a generalist robot policy (VLA model), (2) setting up pre-training or fine-tuning pipelines for robot manipulation, (3) choosing action representations (flow matching vs. diffusion vs. autoregressive), (4) structuring multi-embodiment robot datasets, (5) evaluating dexterous manipulation tasks, (6) implementing action chunking or high-level policy decomposition. Based on the pi0 architecture (Physical Intelligence, 2024).
---

# Robotics VLA Skill

Expert guidance for building generalist robot policies using Vision-Language-Action (VLA) flow models, based on the π0 architecture.

## Core Architecture

**π0 model = VLM backbone + action expert + flow matching**

| Component | Detail |
|---|---|
| VLM backbone | PaliGemma (3B) — provides visual + language understanding |
| Action expert | Separate transformer weights (~300M) for robot state + actions |
| Total params | ~3.3B |
| Action output | Chunks of H=50 actions; 50Hz or 20Hz robots |
| Inference speed | ~73ms on RTX 4090 |

See `references/architecture.md` for full technical details (attention masks, flow matching math, MoE design).

## Training Pipeline

**Two-phase approach (mirrors LLM training):**

1. **Pre-training** → broad physical capabilities + recovery behaviors across many tasks/robots
2. **Fine-tuning** → fluent, task-specific execution on target task

Key rule: combining both phases outperforms either alone. Pre-training gives robustness; fine-tuning gives precision.

See `references/training.md` for data mixture ratios, loss functions, and fine-tuning dataset sizing.

## Action Representation

**Use flow matching, not autoregressive discretization.**

- Flow matching models continuous action distributions → essential for high-frequency dexterous control
- Autoregressive token prediction (e.g. RT-2 style) cannot produce action chunks efficiently
- Action chunks allow open-loop execution at 50Hz without temporal ensembling

## Multi-Embodiment Support

Single model handles 7+ robot configurations via:
- Zero-padding smaller action spaces to match the largest (17-dim)
- Shared VLM backbone; embodiment-specific behavior learned via data
- Weighted task sampling: n^0.43 to handle imbalanced data across robot types

See `references/embodiments.md` for robot platform specs and action space details.

## High-Level Policy Integration

For long-horizon tasks, use a two-tier approach:
- **High-level VLM**: decomposes task ("bus the table") → subtasks ("pick up napkin")
- **Low-level π0**: executes each subtask as a language-conditioned action sequence

Analogous to SayCan. Intermediate language commands significantly boost performance vs. flat task descriptions.

## Related & Complementary Research (2025)

π0 has been extended and complemented by several key works. See `references/related-work.md` for the full landscape, including:
- **π0-FAST / π0.5 / π0.6** — direct successors with faster training, open-world generalization, and RL fine-tuning
- **RTC** — async action chunking to eliminate inference pauses (plug-in, no retraining)
- **UniVLA** — unsupervised action extraction from raw video (no action labels needed)
- **ManiFlow / Streaming Flow** — smoother action generation
- **GR00T N1, Helix, OpenVLA-OFT, DiVLA, RDT-1B** — parallel approaches from NVIDIA, Figure AI, and academia

## Evaluation Checklist

When evaluating a robot manipulation policy:
- [ ] Out-of-box generalization (no fine-tuning) vs. baselines
- [ ] Language following accuracy with flat / human-guided / HL commands
- [ ] Fine-tuning efficiency (success rate vs. hours of data)
- [ ] Complex multi-stage tasks (5–20 min, recovery from failure)
- [ ] Compare: OpenVLA, Octo, ACT, Diffusion Policy as baselines
