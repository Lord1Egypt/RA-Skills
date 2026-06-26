# Design Rationale

Use this file when you need the architectural thesis behind the skill, not just the mechanics.

## Problem statement

Many local RAG setups fail long before retrieval quality becomes the main problem.

The first failures are often:
- unclear data boundaries
- over-broad indexing
- agent overreach
- private notes mixed with reusable workspace knowledge
- expensive rebuild habits
- fragile interfaces that expose backend details to every caller

This skill exists to package a better default.

## Thesis

A reusable retrieval system for multi-agent workspaces should optimize for **boundary quality, operational reliability, and controlled access** before it optimizes for maximal ingestion.

In practice, that means:
- separate personal memory from workspace retrieval
- index only allowlisted corpora
- give agents explicit, deny-by-default access rules
- keep one stable search wrapper
- treat maintenance and refresh strategy as part of the architecture

## Why memory is not the same as retrieval

Personal memory and workspace knowledge have different jobs.

### Personal memory
Used for continuity, preferences, prior decisions, and user-specific context.

Typical examples:
- long-term preferences
- daily notes
- recurring personal workflows
- durable user context

### Workspace retrieval
Used for reusable project knowledge and operational docs.

Typical examples:
- skill docs
- agent rules
- plans
- schemas
- reference material
- domain-scoped documentation

Mixing both into one retrieval pool creates two problems at once:
- privacy boundaries get weaker
- retrieval quality gets noisier

This is why the architecture treats them as separate layers.

## Why allowlisted corpora instead of indexing everything

Index-everything setups look convenient in demos, but they age badly.

Common failure modes:
- accidental inclusion of secrets or private notes
- noisy recall from irrelevant files
- no clear ownership of what belongs in the index
- difficulty explaining why an agent surfaced a result

Allowlisted corpora create explicit ownership and better reasoning surfaces.

Instead of asking:
- "What can we index?"

ask:
- "What should this agent be allowed to know?"
- "What knowledge belongs together operationally?"
- "What should never enter retrieval at all?"

## Why deny-by-default for agent access

Retrieval is an access-expanding capability.

If an agent can search a corpus, the barrier to surfacing that corpus is lower. That makes access policy part of the safety model, not just configuration hygiene.

Deny-by-default is useful because it:
- makes intent explicit
- reduces accidental cross-domain leakage
- keeps specialist agents specialist
- makes policy review easier

## Why one stable wrapper matters

Agents should not need to understand indexing internals, embedding model changes, rank fusion, or backend migrations.

A stable wrapper helps because it:
- centralizes allowlist enforcement
- keeps error handling consistent
- reduces coupling between callers and the backend
- makes it easier to swap search internals later

## Why maintenance belongs in the design

A retrieval system is not done when indexing succeeds once.

Long-running workspaces need an operational model for:
- status checks
- freshness tracking
- selective refresh
- full rebuild fallback
- smoke tests after changes

If maintenance is treated as an afterthought, the system will drift into stale or unexplainable behavior.

## Tradeoffs

This skill does **not** try to maximize ingestion speed or abstraction depth.

Intentional tradeoffs:
- prefer explicit corpora over magical auto-discovery
- prefer safe starter templates over aggressive automation
- prefer architectural clarity over one-command convenience
- prefer boundary discipline over broader default recall

These choices make the skill less flashy, but more trustworthy and easier to evolve.

## What this skill is, and is not

This skill **is**:
- a reusable retrieval architecture pattern
- a safety-conscious starter kit
- a packaging of local-first retrieval design decisions
- a practical bridge between governance and implementation

This skill is **not**:
- a hosted vector database
- a full turnkey search platform
- a benchmark-driven ranking package
- a substitute for careful corpus design

## Why this matters for multi-agent systems

As soon as multiple agents exist, retrieval quality is no longer only about ranking. It becomes a question of:
- who can know what
- how broad shared context should be
- what must stay isolated
- how boundary mistakes compound across agents

That is why this skill treats retrieval as part of system architecture and governance, not just search plumbing.
