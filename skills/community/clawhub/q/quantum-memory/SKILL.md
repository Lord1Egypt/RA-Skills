---
name: quantum-memory-graph
title: Quantum Memory Graph
description: "Quantum-enhanced long-term memory for AI agents — #1 on LongMemEval (98.6% R@5, 99.4% R@10, 0.9426 NDCG). Chunked gte-large retrieval with QAOA+CVaR subgraph optimization for agents."
tags: [memory, retrieval, quantum, rag, embeddings, long-memory, AI-agents, agent-memory]
---

# Quantum Memory Graph (QMG)

Quantum-enhanced long-term memory for AI agents. Uses **chunked gte-large embeddings** for state-of-the-art semantic retrieval with **QAOA+CVaR** quantum subgraph optimization for graph-based reasoning.

## Features

- **#1 on LongMemEval** — 98.6% R@5, 99.4% R@10, 0.9426 NDCG
- **Chunked retrieval** — 500-char blocks with 100-char overlap, mean-of-top-3 per session
- **QAOA+CVaR optimization** — 12.8% edge over greedy on graph/PCE tasks
- **GPU accelerated** — runs on NVIDIA GB10 (DGX Spark)
- **Cascade recall** — personal graph → historical archive fallback
- **Per-agent isolation** — each agent gets their own isolated memory graph

## How It Works

1. **Session chunking** — Conversations split into overlapping 500-char chunks
2. **Embedding** — Chunks encoded with gte-large (1024-dim sentence transformer)
3. **Scoring** — Per-session score = mean of top-3 chunk cosine similarities
4. **Refinement** — Top-N candidates optionally refined via QAOA+CVaR subgraph optimizer
5. **Cascade** — Personal graph first, historical archive fallback if relevance < 0.4

## Performance

| Metric | Score |
|--------|:-----:|
| R@1 | 90.6% |
| **R@5** | **98.6%** |
| R@10 | 99.4% |
| NDCG@10 | 0.9426 |

*Benchmark: LongMemEval-S (500 questions, 18,464 sessions), May 28 2026*

## Usage

```python
from quantum_memory_graph import MemoryGraph

mg = MemoryGraph()
mg.store("Project Alpha uses React frontend with TypeScript.")
mg.store("Project Alpha backend is FastAPI with PostgreSQL.")

# Recall — chunked semantic retrieval + optional QAOA refinement
results = mg.retrieve("What is Project Alpha's tech stack?", top_k=5)
```

Or as a FastAPI server for agent integration:

```bash
pip install quantum-memory-graph
quantum-memory-graph serve  # serves /store, /recall, /stats endpoints
```

## Requirements

- Python 3.10+
- sentence-transformers
- numpy
- (optional) qiskit for QAOA optimization on real hardware

## Links

- GitHub: [https://github.com/Dustin-a11y/quantum-memory-graph](https://github.com/Dustin-a11y/quantum-memory-graph)
- PyPI: [https://pypi.org/project/quantum-memory-graph/](https://pypi.org/project/quantum-memory-graph/)

## License

MIT
