# Trade Memory Architecture

Updated: 2026-04-15

This note explains how Finance Journal adapts ideas from EverOS / EverMemOS / HyperMem into a trading-memory architecture.

## Why The Architecture Changed

The old framework could store plans, trades, reviews, and bandit-style evolution outputs.
But as trading memory grows, plain notes plus tag overlap are not enough.

We now need:
- atomic memory units
- scene-level organization
- graph / hypergraph relations across memories
- scalable retrieval before reminder generation
- a way to solidify stable trajectories into reusable skill cards

## Finance Journal Memory Stack

### 1. Memory Cells

`memory_cells` are the atomic units.
Each cell comes from a plan, trade, or review and stores:
- source entity identity
- trade date / symbol / strategy line / market stage
- searchable text body
- structured summary
- quality metadata
- provenance

### 2. Memory Scenes

`memory_scenes` aggregate cells into reusable contexts, such as:
- symbol scenes
- setup scenes
- stage scenes
- strategy-line scenes

This gives us a stable middle layer between raw memories and top-level reminders.

### 3. Hypergraph Relations

`memory_hyperedges` link cells and scenes through shared setup / risk / strategy / symbol / regime dimensions.
This is our local adaptation of relation-aware memory organization for trading memory retrieval.

### 4. Skill Cards

`memory_skill_cards` are distilled from high-value historical paths.
They are not execution rules.
They are reusable review skills with:
- trigger conditions
- do-not-use conditions
- evidence trades
- sample size
- bandit snapshot
- optional community-share flag

## Retrieval Pipeline

Finance Journal now uses coarse-to-fine retrieval:

1. SQLite FTS5 full-text recall
2. structured filters by symbol / stage / strategy / tags
3. scene and hyperedge expansion
4. bandit-aware reranking in `evolution remind`

This keeps the original bandit layer, but moves candidate recall onto a memory system that can scale.

## Relationship To EverOS / EverMemOS / HyperMem

The following sources informed the redesign:

1. EverOS repository
   - https://github.com/EverMind-AI/EverOS
   - practical reference for treating memory as an operating layer rather than a single prompt cache

2. EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning
   - https://arxiv.org/abs/2601.02163
   - inspired the separation between atomic memory units, scene organization, and self-organized long-horizon memory management

3. HyperMem: Hypergraph Memory for Long-Term Conversations
   - https://arxiv.org/abs/2604.08256
   - inspired the relation-aware retrieval design and the use of hypergraph-style linkage instead of only flat vector recall

## What Is Directly Borrowed vs Adapted

Borrowed at the architecture level:
- memory should be an explicit system layer
- long-horizon recall needs more than flat history
- relation-aware retrieval matters
- stable trajectories can become reusable capabilities

Adapted for trading memory:
- memory units are built from plans / trades / reviews, not general dialogue turns alone
- scene design is symbol / setup / stage / strategy-line oriented
- bandit remains the top-layer prioritizer because our current data is still trade-level and sparse
- skill cards are closer to reusable trading know-how than to standardized quant strategies

## Current Boundary

The system still does not do:
- broker execution
- copy trading
- automatic strategy deployment
- full RL policy learning

The current output remains a memory-backed review and decision-support layer.
