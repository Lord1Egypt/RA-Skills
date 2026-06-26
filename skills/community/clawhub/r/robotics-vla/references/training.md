# Training Pipeline Reference

## Table of Contents
1. [Pre-training Phase](#pre-training-phase)
2. [Fine-tuning Phase](#fine-tuning-phase)
3. [Data Mixture Strategy](#data-mixture-strategy)
4. [Key Lessons](#key-lessons)

---

## Pre-training Phase

**Goal:** Broad physical capabilities and generalization. Especially recovery behaviors.

**Scale:** ~10,000+ hours of robot data, 903M timesteps

**Data breakdown:**
| Source | Share | Notes |
|---|---|---|
| Open-source (OXE, Bridge v2, DROID) | 9.1% | Diverse objects/environments; 2–10Hz |
| Proprietary dexterous manipulation | 90.9% | 7 robot configs, 68 tasks |

**Language annotation:**
- Task-level: overall task name (e.g. "fold laundry")
- Segment-level: fine-grained ~2s sub-trajectory labels (e.g. "grasp left sleeve")
- Both levels used during training

**Sampling:**
- Task-robot combinations weighted by `n^0.43` (power-law to balance imbalanced distributions)

---

## Fine-tuning Phase

**Goal:** Fluent, task-specific execution on target task.

**Dataset size guidelines:**
| Task complexity | Fine-tuning data |
|---|---|
| Simpler tasks | ~5 hours |
| Complex tasks | 100+ hours |
| Example: laundry folding | ~100 hours |

**What pre-training adds to fine-tuning:**
- Recovery from failures (learned during pre-training, retained through fine-tuning)
- Broader visual generalization
- Stronger language following

**Rule:** Fine-tuning with only high-quality data → brittle model (no recovery). Pre-training alone → imprecise execution. Both combined → best results.

---

## Data Mixture Strategy

When mixing pre-training and fine-tuning data:
- Include pre-training data alongside fine-tuning data during the fine-tuning phase
- This prevents catastrophic forgetting of recovery behaviors
- Exact ratio depends on task; start with a small fraction of pre-training data mixed in

---

## Key Lessons

1. **Pre-training is most valuable for hard tasks** — the harder and longer the task, the bigger the pre-training benefit (laundry folding, multi-stage manipulation show largest gains)

2. **VLM initialization matters** — π0-small (no VLM pre-training, 470M params) consistently underperforms π0 despite similar architecture. VLM provides both visual representations AND language grounding.

3. **Intermediate language commands help** — π0 benefits significantly from fine-grained language commands during execution (from a high-level VLM). π0-small does NOT benefit, because its language understanding is too weak.

4. **1 hour of data is enough to outperform baselines** — when pre-trained π0 is fine-tuned with just 1 hour of target-task data, it significantly outperforms task-specific baselines trained from scratch with more data.

5. **Transfer is positive for similar domains** — pre-training helps most when fine-tuning tasks are similar to pre-training tasks. For highly novel domains, transfer benefit is smaller.

6. **Data composition is not fully understood** — open question: what is the optimal pre-training mixture? More research needed.
