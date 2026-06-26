---
name: tidal-lock
version: 1.0.0
description: >
  Detects unhealthy coupling between components — when two modules, services,
  or layers have become gravitationally locked, unable to change independently.
  Like the Moon always showing Earth the same face, tidally-locked code can
  only rotate together. This skill maps coupling health across the entire
  system and identifies where independence has been silently surrendered.
author: J. DeVere Cooley
category: architecture-health
tags:
  - coupling
  - architecture
  - dependency-analysis
  - modularity
metadata:
  openclaw:
    emoji: "🌗"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - architecture
---

# Tidal Lock

> "In orbital mechanics, tidal locking occurs when a body's orbital period matches its rotational period — it can only face one direction. In software, tidal locking occurs when two components can only change together. They've lost the ability to face any other direction."

## What It Does

Every software architecture diagram shows clean boxes with clean arrows. Reality is messier. Over time, components develop **gravitational relationships** — shared assumptions, implicit contracts, synchronized change requirements — that make them unable to evolve independently.

Tidal Lock detects these gravitational bonds before they become permanent.

## The Physics of Code Coupling

In astrophysics, tidal locking is caused by gravitational gradient forces. In codebases, it's caused by **coupling gradient forces**:

| Physical Force | Code Equivalent | Example |
|---|---|---|
| Gravitational pull | Shared data structures | Two services reading the same DB table |
| Tidal friction | Synchronized deploys | Service A fails if Service B isn't deployed first |
| Orbital resonance | Matching change frequency | Every commit to module X requires a commit to module Y |
| Roche limit | Merger threat | Components so coupled they should just be one module |
| Lagrange points | Stable mediators | A third component that exists only to translate between two locked ones |

## The Five Degrees of Lock

### Degree 0: Independent Orbit
Components are genuinely independent. Changing one has zero effect on the other. This is the ideal for components that shouldn't be related.

### Degree 1: Gravitational Awareness
Components know about each other through well-defined interfaces. Changes to internals are isolated. Changes to the interface require coordination. This is healthy coupling.

### Degree 2: Orbital Resonance
Components change at correlated frequencies. Not every change to A requires a change to B, but many do. The interface between them has become too wide or too leaky.

```
SYMPTOMS:
├── PRs frequently touch both components
├── "Don't forget to update the other side" appears in code reviews
├── Integration tests between them break more than unit tests
└── Deploy ordering matters sometimes
```

### Degree 3: Synchronous Rotation
Components MUST change together. Every modification to A requires a corresponding modification to B. They share data structures, timing assumptions, or implicit contracts that make independent evolution impossible.

```
SYMPTOMS:
├── Cannot deploy A without deploying B
├── Changing A's internals breaks B's tests
├── Shared mutable state (database tables, global configs)
├── Copy-pasted type definitions kept "in sync" manually
└── Integration bugs outnumber all other bug types
```

### Degree 4: Tidal Lock (Critical)
Components have lost their individual identity. They are one system pretending to be two. The boundary between them is a fiction maintained by the directory structure but violated by every data flow.

```
SYMPTOMS:
├── Circular dependencies (A imports B, B imports A)
├── Shared internal state (not just shared interfaces)
├── Cannot reason about one without fully understanding the other
├── "We should really merge these" has been said multiple times
└── New developers can't tell where one ends and the other begins
```

### Degree 5: Roche Limit (Structural Failure)
The coupling is so severe that the components are actively tearing each other apart. Bugs in one appear as symptoms in the other. Changes cascade unpredictably. The architecture is in structural failure.

## Detection Methodology

```
Phase 1: GRAVITATIONAL SURVEY
├── Map all explicit dependencies (imports, API calls, DB access)
├── Map all implicit dependencies (shared configs, env vars, timing)
├── Map change correlation (git co-change analysis)
├── Map deploy dependencies (must X deploy before/after Y?)
└── Map failure correlation (when X fails, does Y fail too?)

Phase 2: ORBITAL ANALYSIS
├── For each component pair, calculate:
│   ├── Change Coupling Score: How often do they change together?
│   ├── Interface Width: How much surface area connects them?
│   ├── Data Gravity: How much shared state exists?
│   ├── Temporal Coupling: Do they depend on ordering?
│   └── Failure Coupling: Do they fail together?
├── Composite score → Degree of Lock (0-5)
└── Trend analysis: Is coupling increasing or decreasing?

Phase 3: LOCK CARTOGRAPHY
├── Generate coupling map of the full system
├── Identify lock clusters (groups of mutually locked components)
├── Identify lock chains (A→B→C cascading coupling)
├── Calculate system-wide coupling health score
└── Flag components approaching the Roche limit

Phase 4: ORBITAL MECHANICS REPORT
├── For each locked pair, explain:
│   ├── What force is causing the lock
│   ├── How long the lock has existed (git history analysis)
│   ├── Whether the lock is increasing or stable
│   └── Decoupling strategy (if decoupling is warranted)
├── System-wide coupling topology
└── Priority ranking: which locks to break first
```

## Decoupling Strategies by Force Type

| Coupling Force | Decoupling Strategy |
|---|---|
| **Shared DB tables** | Introduce owned views or dedicated read models per service |
| **Shared data types** | Define contracts at the boundary, allow internal divergence |
| **Deploy ordering** | Add graceful degradation and version negotiation |
| **Change correlation** | Extract the shared concern into its own module |
| **Circular imports** | Introduce an interface/protocol layer; invert one dependency |
| **Shared mutable state** | Event-driven communication; each component owns its state |
| **Timing assumptions** | Explicit synchronization; remove implicit ordering |

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                    TIDAL LOCK ANALYSIS                      ║
║            System Coupling Health: 64/100                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  LOCK SEVERITY DISTRIBUTION:                                 ║
║  ├── Degree 0 (Independent): 12 pairs  ████████████  ✓      ║
║  ├── Degree 1 (Aware):        8 pairs  ████████      ✓      ║
║  ├── Degree 2 (Resonant):     5 pairs  █████         ⚠      ║
║  ├── Degree 3 (Synchronous):  2 pairs  ██            ⚠⚠     ║
║  ├── Degree 4 (Locked):       1 pair   █             🔴     ║
║  └── Degree 5 (Roche):        0 pairs                ✓      ║
║                                                              ║
║  CRITICAL LOCK:                                              ║
║  ┌─────────────────────────────────────────────────────┐     ║
║  │  UserService ←→ BillingService                      │     ║
║  │  Degree: 4 (Tidal Lock)                             │     ║
║  │  Force: Shared DB (users table), circular imports   │     ║
║  │  Duration: 14 months (increasing)                   │     ║
║  │  Co-change rate: 89% of commits touch both          │     ║
║  │  Strategy: Extract UserProfile as shared contract;  │     ║
║  │            give Billing its own customer table       │     ║
║  └─────────────────────────────────────────────────────┘     ║
║                                                              ║
║  LOCK CHAINS:                                                ║
║  Auth → Users → Billing → Invoicing (4-component chain)     ║
║  Any change to Auth cascades through 3 downstream services   ║
║                                                              ║
║  TREND: System coupling increased 12% in last quarter        ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- Before splitting a monolith into services (find out what's *actually* independent)
- After microservice adoption (verify you didn't build a distributed monolith)
- When deploys keep breaking unrelated services
- When "simple changes" take weeks because of cascading modifications
- During architecture reviews to assess modularity health

## Why It Matters

The promise of modularity is **independent evolution**. When components become tidally locked, that promise is broken — you have the overhead of multiple components with the rigidity of a monolith. The worst of both worlds.

Tidal Lock shows you where independence has been surrendered, so you can decide: decouple them, or honestly merge them. Either is better than the fiction of modularity with the reality of lock.

Zero external dependencies. Zero API calls. Pure structural and historical analysis.
