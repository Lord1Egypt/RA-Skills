---
name: synaptic-pruning
version: 1.0.0
description: >
  Identifies vestigial code — not just unused imports, but dead feature branches
  still compiled, zombie configurations nobody reads, orphaned tests that validate
  nothing, and architectural fossils from three rewrites ago. Prunes what the
  codebase has outgrown, the way a brain prunes unused neural pathways.
author: J. DeVere Cooley
category: cognitive-diagnostics
tags:
  - dead-code
  - code-health
  - pruning
  - evolution
metadata:
  openclaw:
    emoji: "🧠"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - maintenance
---

# Synaptic Pruning

> "A brain that never prunes becomes a brain that can't think. A codebase that never prunes becomes a codebase that can't change."

## What It Does

Your linter finds unused imports. Your compiler finds unreachable code. Synaptic Pruning finds **vestigial organs** — code that is technically reachable, technically used, technically valid — but serves no living purpose.

In neuroscience, synaptic pruning eliminates neural connections the brain no longer needs. It's not destruction — it's *maturation*. A child's brain has more synapses than an adult's. The adult brain is more capable because it has fewer.

Your codebase needs the same process.

## The Seven Vestigial Classes

### 1. Zombie Features
Features that are fully implemented, fully compiled, fully deployed — and fully unused. No user path reaches them. No button triggers them. They exist because nobody was confident enough to delete them.

```
Detection: Trace every UI element and API endpoint to user-reachable paths.
Flag features with zero invocations in the last N deployment cycles.
```

### 2. Fossil Configurations
Config keys, feature flags, and environment settings that are read by code but never influence behavior. The `if` branch they gate is always true (or always false). They're the appendix of your architecture.

```yaml
# This flag has been 'true' in every environment for 2 years
feature_flags:
  enable_new_checkout: true  # "new" checkout is the only checkout
  use_v2_api: true           # v1 was decommissioned 18 months ago
  experimental_search: true  # shipped to 100% of users last March
```

**Detection:** Evaluate every config-gated branch. If the gate has been in the same state across all environments for > N days, the gate is a fossil.

### 3. Orphaned Tests
Tests that pass, appear in coverage reports, and validate... nothing that matters. They test functions that were refactored away, mock interfaces that no longer exist, or assert behavior that was intentionally changed (and the test was updated to match the new behavior, making it a tautology).

```python
def test_calculate_discount():
    # This test was updated when discounts were removed.
    # It now tests that the function returns 0. Always.
    # It will never fail. It validates nothing.
    assert calculate_discount(any_input) == 0
```

**Detection:** Identify tests where every assertion is trivially true, where mocks replace 100% of real behavior, or where the tested function's actual callsites have all been removed.

### 4. Compatibility Shims
Adapters, wrappers, and translation layers that were added for a migration that completed. The old system is gone. The shim remains, adding a layer of indirection that obscures the actual architecture.

```javascript
// Added during the Angular → React migration (2023)
// Angular was fully removed in 2024
// This wrapper still wraps every React component for no reason
export function withAngularCompat(Component) {
  return Component; // literally returns its input unchanged
}
```

**Detection:** Find wrapper/adapter functions where input === output, translation layers where source and target are the same format, and abstraction layers with exactly one implementation.

### 5. Defensive Fossils
Error handling, validation, and guard clauses that protect against conditions that the current architecture makes impossible. They were necessary under a previous design. Now they're scar tissue.

```go
// This nil check was necessary when getUser() could return nil
// After the auth rewrite, getUser() always returns a valid user or panics
// This branch is unreachable but looks important
if user == nil {
    return ErrUserNotFound // this line has never executed in production
}
```

**Detection:** Analyze guard clauses against current control flow. If a predecessor guarantees the condition can never be true, the guard is a fossil.

### 6. Documentation Ghosts
README sections, API docs, and inline comments that describe systems, processes, or architectures that no longer exist. They don't cause bugs — they cause *wrong mental models*, which is worse.

```markdown
## Deployment Process
1. SSH into the staging server        ← We use Kubernetes now
2. Run the deploy script              ← Replaced by GitHub Actions
3. Verify the health check endpoint   ← Endpoint was renamed
4. Update the load balancer config    ← Handled automatically by Istio
```

**Detection:** Cross-reference documentation commands, paths, and process descriptions against actual project tooling, CI/CD configs, and infrastructure definitions.

### 7. Evolutionary Dead Ends
Entire modules or subsystems that represent an architectural direction the team tried and abandoned — but the code was never fully removed. Partial implementations, experimental branches merged to main, or V2 rewrites that were started but never finished.

```
src/
├── search/           ← Current search (Elasticsearch)
├── search-v2/        ← Started migrating to Meilisearch. Stopped.
│   ├── index.ts      ← 40% implemented
│   ├── client.ts     ← Works but unused
│   └── README.md     ← "TODO: finish migration"
```

**Detection:** Find directories/modules with high internal cohesion but zero external references. Flag modules where >50% of exports are unused outside the module.

## The Pruning Process

```
Phase 1: CENSUS
├── Catalog every function, class, config, test, and doc section
├── Build a full reachability graph from user-facing entry points
├── Map every feature flag and its historical states
└── Timestamp: when was each unit last meaningfully modified?

Phase 2: VITALITY CHECK
├── For each unit, determine: is it alive, dormant, or dead?
│   ├── Alive: reachable, executed, behavior matters
│   ├── Dormant: reachable but behavior is constant/trivial
│   └── Dead: unreachable, untriggered, or tautological
├── Score confidence (how certain is the classification)
└── Flag borderline cases for human review

Phase 3: PRUNING PLAN
├── Group vestigial code by class (1-7 above)
├── Calculate removal safety (what could break)
├── Estimate cognitive load reduction (lines × complexity × frequency-of-reading)
├── Generate ordered removal plan (safest-first)
└── Produce before/after complexity metrics

Phase 4: MATURATION REPORT
├── Total vestigial burden (lines, files, cognitive weight)
├── Recommended pruning order with safety scores
├── Estimated improvement in onboarding time
└── Codebase age distribution (living vs. fossil)
```

## Vitality Scoring

| Score | State | Action |
|---|---|---|
| **100** | Fully alive | No action |
| **75-99** | Alive but calcifying | Monitor for drift |
| **50-74** | Dormant | Review for removal |
| **25-49** | Effectively dead | Schedule removal |
| **1-24** | Dead weight | Remove immediately |
| **0** | Never lived | Delete with prejudice |

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                  SYNAPTIC PRUNING REPORT                    ║
║              Codebase Maturity: 67% (Growing)               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  VESTIGIAL BURDEN: 4,217 lines across 38 files              ║
║  COGNITIVE WEIGHT: ~12% of total codebase complexity         ║
║  ESTIMATED ONBOARDING REDUCTION: 1.5 days                   ║
║                                                              ║
║  BY CLASS:                                                   ║
║  ├── Zombie Features ......... 2 features, 890 lines        ║
║  ├── Fossil Configurations ... 14 flags, 3 always-true      ║
║  ├── Orphaned Tests .......... 7 tests, 340 lines           ║
║  ├── Compatibility Shims ..... 4 wrappers, identity funcs   ║
║  ├── Defensive Fossils ....... 23 unreachable guards        ║
║  ├── Documentation Ghosts .... 3 sections, 2 READMEs       ║
║  └── Evolutionary Dead Ends .. 1 module (search-v2/)        ║
║                                                              ║
║  SAFE TO PRUNE NOW: 2,841 lines (0 risk)                    ║
║  PRUNE WITH REVIEW: 1,376 lines (low risk)                  ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- After a major version release (prune the migration artifacts)
- Before onboarding new team members (reduce noise)
- Quarterly codebase health reviews
- After any "why does this exist?" question in code review

## Why It Matters

Dead code doesn't just waste disk space. It wastes **attention**. Every vestigial function a developer reads, every fossil config they try to understand, every zombie feature they accidentally modify — that's cognitive load stolen from productive work.

The leanest codebases aren't the ones that added the least. They're the ones that **pruned the most**.

Zero external dependencies. Zero API calls. Pure evolutionary analysis.
