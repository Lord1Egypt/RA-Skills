# X Thread 示例输出

> 以下是基于一篇假设的技术报告 "SparseFormer: Efficient Sparse Attention for Long-Context LLMs" 生成的示例

## Tweet 1/8
[IMAGE: x_cover.png]

SparseFormer achieves 97.2% of full attention quality while using only 12% of compute on sequences up to 128K tokens.

We introduce a dynamic sparse attention mechanism that adapts sparsity patterns per-layer. Key findings:

---

## Tweet 2/8

The problem: Full self-attention scales O(n^2) with sequence length. At 128K tokens, this becomes prohibitively expensive even on H100s.

Existing sparse methods (Longformer, BigBird) use fixed patterns that miss important cross-document dependencies.

---

## Tweet 3/8

Core idea: Instead of fixed sparsity patterns, SparseFormer learns which tokens to attend to using a lightweight "routing" module.

Each layer gets a different sparsity pattern, allowing early layers to be broad and later layers to be focused.

---

## Tweet 4/8

The routing module adds only 0.3% extra parameters but determines attention patterns in O(n log n) time.

Key insight: Information flow in transformers follows predictable pathways — you can identify the critical paths cheaply.

---

## Tweet 5/8

Training trick: We use a two-stage approach.
- Stage 1: Train with full attention (short sequences)
- Stage 2: Fine-tune with learned sparse patterns (long sequences)

This avoids the cold-start problem of training sparse attention from scratch.

---

## Tweet 6/8

Results on RULER-128K benchmark:

- SparseFormer-7B: 94.1 (12% compute)
- Full Attention-7B: 96.8 (100% compute)
- Longformer-7B: 81.3 (15% compute)
- BigBird-7B: 79.6 (14% compute)

Significantly closes the gap to full attention with comparable efficiency to fixed patterns.

---

## Tweet 7/8

On real-world tasks:
- Multi-doc QA (MuSiQue): +8.3 points over Longformer
- Code understanding (RepoQA): +12.1 points
- Summarization (GovReport): ROUGE-L 47.2 vs 43.8

The adaptive patterns particularly shine on tasks requiring cross-document reasoning.

---

## Tweet 8/8

Weights and code available at [GitHub link placeholder]

Paper: [arXiv link placeholder]

What's interesting: the learned sparsity patterns are highly interpretable — they reveal how information actually flows through the model.

#MachineLearning #NLP #EfficientAI #LLM
