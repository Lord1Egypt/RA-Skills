---
name: seismograph
version: 1.0.0
description: >
  Predicts the ripple effects of a proposed change before you make it.
  Maps how a modification propagates through the codebase — what breaks,
  what bends, what shifts — the way a seismograph maps how energy radiates
  from an epicenter through geological layers with different densities
  and fault lines.
author: J. DeVere Cooley
category: change-intelligence
tags:
  - impact-analysis
  - change-prediction
  - risk-assessment
  - pre-commit
metadata:
  openclaw:
    emoji: "📊"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - risk
---

# Seismograph

> "An earthquake's damage isn't determined at the epicenter. It's determined by the geology between the epicenter and everything else — the fault lines, the soil composition, the depth of the bedrock. Code changes work the same way."

## What It Does

Before you make a change, Seismograph maps the **propagation path** — every function, module, test, type, config, and downstream system that will feel the tremor. Not just "what calls this function" (your IDE does that), but:

- What **assumptions** about this code exist elsewhere?
- What **tests** validate the current behavior you're about to change?
- What **documentation** promises the behavior you're about to break?
- What **downstream systems** depend on the output shape you're about to modify?
- What **side effects** of this code have become relied upon, even though they weren't intended?

## The Seismic Model

### Earthquake Anatomy → Change Anatomy

| Seismic Concept | Code Equivalent |
|---|---|
| **Epicenter** | The line(s) of code you're modifying |
| **Fault line** | Interface boundaries, type contracts, API surfaces |
| **P-waves** (first, compression) | Direct callers/importers — feel the change immediately |
| **S-waves** (second, shear) | Indirect dependents — feel it through intermediaries |
| **Surface waves** (slowest, most destructive) | Side-effect dependents — feel it through emergent behavior |
| **Seismic velocity** | How fast the change propagates (tight coupling = faster) |
| **Liquefaction** | Loosely-defined interfaces that collapse under unexpected change |
| **Aftershocks** | Secondary bugs caused by fixing the primary change's breakage |
| **Magnitude** | Scope of the change × coupling density × downstream reach |
| **Intensity** (varies by location) | Impact varies by distance and intervening architecture |

## Wave Analysis

### P-Waves: Direct Impact
**Propagation:** Immediate callers, importers, and direct consumers.
**Speed:** Instant. These break at compile/import time.
**Damage:** Usually low — these are caught by static analysis.

```
ANALYSIS:
├── Every file that imports the changed module
├── Every function that calls the changed function
├── Every type that extends or implements the changed type
├── Every test that directly tests the changed behavior
└── Estimated: files affected, lines potentially impacted
```

### S-Waves: Indirect Impact
**Propagation:** Second-order dependents. Things that use things that use the changed code.
**Speed:** Slower. These break at runtime or during integration testing.
**Damage:** Medium — often caught by integration tests, if they exist.

```
ANALYSIS:
├── Transitive importers (A uses B uses Changed)
├── Functions that consume the output of changed functions
├── Systems that read data written by changed code
├── Configurations parsed by changed logic
└── Estimated: propagation depth, weakest intermediary
```

### Surface Waves: Side-Effect Impact
**Propagation:** Code that depends on the *behavior* of the changed code without explicitly calling it. Event listeners, database triggers, log parsers, monitoring alerts, cached values, file watchers.
**Speed:** Slowest. These break in production, days or weeks later.
**Damage:** Highest — invisible until they cause an incident.

```
ANALYSIS:
├── Event subscribers that react to events emitted by changed code
├── Monitoring/alerting rules that pattern-match on changed behavior
├── Cached values computed from changed code's output
├── Database triggers fired by changed code's queries
├── Log parsers/aggregators that expect changed code's log format
├── Downstream services that learned (not contracted) the output shape
└── Estimated: probability of surface-wave damage, detection difficulty
```

## Magnitude Scale

| Magnitude | Description | Typical Impact |
|---|---|---|
| **1.0 - 2.0** | Micro. Internal refactor, no interface change. | Self-contained. No propagation. |
| **2.0 - 3.0** | Minor. Implementation detail change, interface preserved. | P-waves only. Tests may need updates. |
| **3.0 - 4.0** | Moderate. Interface change, same semantics. | P and S-waves. Direct consumers affected. |
| **4.0 - 5.0** | Significant. Semantic change to public interface. | All wave types. Integration tests break. |
| **5.0 - 6.0** | Major. Behavioral change affecting downstream systems. | Cross-service impact. Deployment coordination needed. |
| **6.0 - 7.0** | Severe. Schema/contract breaking change. | Data migration required. Multi-team coordination. |
| **7.0+** | Catastrophic. Architectural assumption change. | System-wide impact. Staged rollout mandatory. |

## Geological Survey: Pre-Change Analysis

```
Phase 1: EPICENTER MAPPING
├── Identify exact lines being changed
├── Classify change type:
│   ├── Rename (lowest risk)
│   ├── Signature change (medium risk)
│   ├── Behavioral change (high risk)
│   ├── Removal (highest risk)
│   └── Addition (usually safe, unless overloading existing names)
└── Determine magnitude baseline

Phase 2: WAVE PROPAGATION
├── P-Wave analysis:
│   ├── Static dependency graph traversal
│   ├── Type system impact (what breaks at compile time?)
│   └── Direct test impact (what tests fail?)
├── S-Wave analysis:
│   ├── Transitive dependency traversal (2-3 hops)
│   ├── Data flow tracing (output consumed where?)
│   └── Integration test impact
└── Surface-Wave analysis:
    ├── Event/message subscribers
    ├── Database triggers and views
    ├── Monitoring and alerting rules
    ├── Cache invalidation implications
    └── Log format dependencies

Phase 3: FAULT LINE ASSESSMENT
├── For each wave path, assess intervening architecture:
│   ├── Strong boundaries (typed interfaces, contracts) → wave dampened
│   ├── Weak boundaries (duck typing, convention) → wave amplified
│   ├── No boundary (direct coupling) → wave passes through
│   └── Fault lines (known fragile points) → wave magnified
└── Adjust intensity at each affected location

Phase 4: AFTERSHOCK PREDICTION
├── If you fix the primary breakage, what secondary breaks occur?
├── Which fixes are "safe" (localized) vs "cascading" (cause more waves)?
├── Estimated total change set: original change + all required adaptations
└── Is the total change set larger than the original intention warrants?

Phase 5: SEISMOGRAPH REPORT
├── Magnitude and intensity map
├── Prioritized list of affected locations
├── Recommended change strategy (direct, staged, behind flag)
├── Aftershock forecast
└── Go / staged-rollout / reconsider recommendation
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                  SEISMOGRAPH ANALYSIS                       ║
║    Proposed: Rename User.email → User.emailAddress           ║
║    Magnitude: 4.7 (Significant)                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  EPICENTER: src/models/user.ts:24                            ║
║                                                              ║
║  P-WAVES (Direct Impact):                                    ║
║  ├── 14 files import User and access .email                  ║
║  ├── 8 tests assert on .email                                ║
║  ├── 2 API serializers include 'email' key                   ║
║  └── Compile-time breakage: YES (TypeScript will catch)      ║
║                                                              ║
║  S-WAVES (Indirect Impact):                                  ║
║  ├── 3 services consume User API response with 'email' field ║
║  ├── 1 webhook payload includes 'email' (external consumers) ║
║  ├── 1 CSV export uses 'email' as column header              ║
║  └── Runtime breakage: LIKELY in downstream services         ║
║                                                              ║
║  SURFACE WAVES (Side-Effect Impact):                         ║
║  ├── Elasticsearch index maps 'email' field → search breaks  ║
║  ├── Monitoring alert matches on "email" in log output       ║
║  ├── 2 Zapier integrations reference 'email' field           ║
║  └── Detection difficulty: HIGH (weeks before discovery)     ║
║                                                              ║
║  AFTERSHOCK FORECAST:                                        ║
║  ├── Fixing the 14 P-wave files triggers 0 new waves ✓      ║
║  ├── Fixing the API serializer triggers 3 client-side breaks ║
║  ├── Fixing the webhook requires partner notification        ║
║  └── Total change set: 24 files + 3 external systems        ║
║                                                              ║
║  FAULT LINES CROSSED: 2                                      ║
║  ├── API boundary (typed but externally consumed)            ║
║  └── Webhook contract (no versioning, external consumers)    ║
║                                                              ║
║  RECOMMENDATION: STAGED ROLLOUT                              ║
║  1. Add emailAddress as alias, keep email (backward compat)  ║
║  2. Migrate internal consumers to emailAddress               ║
║  3. Notify external consumers, add deprecation warning       ║
║  4. Remove email after deprecation period                    ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- Before **any** change to a public interface, API, or shared type
- Before renaming anything that crosses a module boundary
- Before modifying database schemas or wire formats
- Before removing any function, field, or parameter
- When someone says "this should be a simple change" (it never is)
- During PR review to assess whether the change accounts for its full impact

## Why It Matters

The #1 source of production incidents isn't bad code — it's **changes that propagated further than anyone expected**. A "simple rename" that broke a webhook. A "minor optimization" that changed a timing guarantee. A "cleanup refactor" that removed a field a downstream system needed.

Seismograph doesn't prevent changes. It prevents *surprises*. Because the question is never "should we make this change?" — it's "do we understand what this change will touch?"

Zero external dependencies. Zero API calls. Pure static and historical analysis.
