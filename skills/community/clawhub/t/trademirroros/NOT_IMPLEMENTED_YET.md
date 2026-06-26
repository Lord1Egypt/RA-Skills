# Not Implemented Yet

Updated: 2026-04-15

## Memory Retrieval Depth

The current memory stack already supports local hybrid retrieval, but it does not yet provide:
- a production embedding provider
- learned vector reranking
- true cross-runtime memory merge tooling
- stronger automatic scene consolidation across multiple users
- graph-aware retrieval learned from accumulated usage feedback

## Trajectory Modeling Depth

The project still does not provide:
- full intraday state-action-reward trajectories
- offline RL policy learning
- strategy-line specific regime-switch detection
- tick-level replay or chart memory archiving

## Community Layer

Not implemented yet:
- anonymized cross-user memory exchange
- moderation and provenance services for public memory cards
- a shared registry for reusable community skill cards
- federation between multiple local runtimes
- community-side cross-validation for high-risk patterns and wrong-thesis warnings

## Research and Publication Packaging

Partially implemented:
- a first retrieval benchmark harness now exists for `fts_only`, `structured_only`, `hybrid_cell_only`, and `graph_hybrid`
- a paper-style architecture note now exists in `TRADE_MEMORY_SYSTEM_PAPER.md`

Still open:
- larger-scale quantitative ablations for FTS / hyperedge / bandit stages
- a reproducible paper build pipeline such as Pandoc, Quarto, or LaTeX export scripts
- automated dataset sanitization for private-to-public artifact release
- a formal evaluation harness for memory skill-card precision and recall

## Why These Gaps Remain

The project is intentionally prioritizing:
1. truthful journaling
2. durable long-term memory
3. retrieval that scales with growing history
4. memory-backed review skills before any automation layer
