# Reference: System Evolution — Stable States, Ultra-Stability, Catastrophe

Book anchor: 金观涛《控制论与科学方法论》第三章 §3.3–§3.9, 第四章 §4 (系统及其演化, 质变的数学模型).

## Stability is a structure property, not just a trajectory property (§3.3)

(§3.3) A system of mutually-coupled subsystems tends toward a **stable-state structure**
(稳态结构): a configuration where each subsystem's value is held in place by the feedback of the
others. Small perturbations return to the stable state; large ones may push the system past a
separatrix into a *different* stable state, or into collapse.

This is a stronger claim than "the trajectory is stable" (see `references/stability.md`). It
says: **the system as a whole has attractors**, and the behavior you observe is the system
sitting in one of them. If you don't like the behavior, you cannot fix it by tweaking inputs
alone — the structure will keep pulling the system back to the same attractor.

### Three things a coupled system can do (§3.3)

1. Sit in a stable-state structure (returns after small kicks).
2. Oscillate or collapse (no restoring force, or a runaway positive feedback).
3. Move from one stable-state structure to another (the old structure lost stability and the
   system fell into a new attractor).

Most debugging focuses on case 2 (kill the oscillation). The harder skill is recognizing case
3: the system was stable, your change broke the stability, and the system has now settled into
a *different* stable state that you didn't intend. Reverting your change may not be enough —
the system may be stuck in the new attractor.

## LLM behavior pattern: Recognize which case you are in

> "Before trying to fix a behavior, ask: is the system oscillating (case 2), or has it moved to
> a different stable state (case 3)? The fixes are different."

- Case 2 (oscillation / leak / divergence): add damping, clamp the actuator, fix the feedback
  sign. See `references/stability.md`.
- Case 3 (moved to a new attractor): the *structure* changed. You must change the structure
  back — restore the invariant, re-establish the coordination relation, remove the input that
  broke the old attractor. Tweaking gains will not move the system between attractors.

Example: a service that was stable at 1000 QPS suddenly runs at 3000 QPS after a marketing
push. The cache hit rate dropped, the DB is now the bottleneck, latency is up, autoscaler is
thrashing. This is *not* an oscillation — the system has moved to a new stable state
("overloaded"). Adding retries (case 2 fix) makes it worse; you must change the structure
(bigger cache, read replica, rate-limit at the edge) to move it back.

## Ultra-stable systems (§3.7)

(§3.7) Some systems maintain long-term stability **by going through instability**. The pattern:

1. The system sits in a stable state.
2. Internal or external change erodes the stability; the system enters an unstable phase.
3. A repair mechanism activates, searches, and *returns the system to the original stable
   state* (not a new one).
4. Repeat.

Ashby's *homeostat* is the canonical example. The book's example: the Chinese feudal system,
which cycled through centuries of stability punctuated by centuries of upheaval that ultimately
restored the same structure. The pattern is **stable → unstable → repair → stable**, and the
repair targets the *original* attractor, not a new one.

The key signal: the instability is **part of the design**, not a failure. The system uses the
unstable phase to flush accumulated disturbance and reconverge.

## LLM behavior pattern: Don't patch over the repair cycle

> "Before patching an instability, ask: is this a failure, or is it a repair mechanism trying
> to run? Patching over a repair cycle converts a self-healing system into a brittle one."

Examples of ultra-stability in software:
- A cache that periodically evicts everything and rebuilds from source. The "instability" (cold
  cache, slow responses for a few minutes) is the repair mechanism that prevents unbounded
  growth. Do not "fix" it by disabling eviction.
- A GC pause that periodically stops the world to reclaim memory. The pause is the repair.
  Disabling GC converts a stable system into a leaky one.
- A circuit breaker that trips and lets traffic through again after a timeout. The trip is the
  unstable phase; the reset is the reconvergence.
- An autoscaler that scales down at night and up at dawn. The scaling events look like
  instability on a graph, but they are the system returning to its setpoint.
- A test suite that occasionally flakes and forces a re-run. The flake may be revealing a real
  race; "fixing" it by retrying suppresses the signal.

The anti-pattern: the LLM sees the unstable phase, treats it as a bug, and patches it (disable
eviction, disable GC, pin the autoscaler, hide the flake). The system *appears* more stable
in the short term, but has lost its ability to recover from real disturbance. When the next
real disturbance hits, the system fails catastrophically because the repair mechanism was
disabled.

## Bifurcation and convergence (§3.8)

(§3.8) When a stable-state structure loses stability, the system may move to a *new* stable
state. The new state may be unique (convergence: many starting points lead to the same outcome)
or multiple (bifurcation: small differences in initial conditions lock in very different
outcomes).

- **Bifurcation**: at the critical point, the system can fall into attractor B or attractor C.
  Tiny differences in initial conditions decide which. After the bifurcation, B and C diverge
  sharply. You cannot treat a bifurcation as a continuous tradeoff — it is a discrete choice
  disguised as a continuous parameter.
- **Convergence**: many different starting points flow to the same attractor. You can be sloppy
  about initial conditions because the system corrects itself.

## LLM behavior pattern: Identify bifurcation points

> "At a bifurcation, small choices lock in large differences. Examine initial conditions
> carefully; do not treat a bifurcation as a continuous tradeoff."

Architecture decisions are full of bifurcations:
- Sync vs async I/O: once chosen, the entire codebase forms around it. Moving from sync to
  async later is not a parameter tweak — it is a rewrite.
- Single-process vs distributed: once you assume you can share memory, every component does.
  Removing that assumption is a structural change, not a config change.
- Mutable shared state vs immutable messages: same shape. The choice locks in a stable-state
  structure that resists change.
- Schema-first vs schema-less: once data is in production without a schema, adding one is a
  bifurcation, not a migration.

At these points, the LLM must *not* default to "the smaller change". The smaller change at a
bifurcation is the one that locks in the existing attractor, which may be the wrong one. The
LLM must explicitly name the bifurcation, the candidate attractors, and the initial conditions
that decide between them.

## Self-reproduction and critical thresholds (§3.9)

(§3.9) Some variables have **positive feedback on their own growth rate**: the larger the
value, the faster it grows. Nuclear chain reactions, viral spread, cancer, laser amplification,
cache stampedes, bank runs, retry storms. The book calls these **self-reproducing systems**
(自繁殖系统).

Every self-reproducing loop has a **critical threshold** (临界值):
- Below the threshold, the loop dies out (sub-critical: each generation is smaller than the
  last).
- Above the threshold, the loop explodes (super-critical: each generation is larger, until
  saturation or collapse).

The threshold depends on the system's stability: more stable systems have higher thresholds.
A well-damped retry system tolerates a high error rate before storming; a tightly-coupled one
storms at a low error rate.

## LLM behavior pattern: Test near the threshold, not just at typical load

> "Positive-feedback loops look safe at typical load and explode at the threshold. If you
> haven't tested near the threshold, you don't know where it is."

Concrete practices:
- Retries: what error rate triggers a retry storm? Test at 2×, 5×, 10× typical.
- Cache: what miss rate triggers a stampede? Test at the TTL boundary with N concurrent
  misses.
- Auto-scaling: what load triggers thrashing? Test at the scale-up threshold and beyond.
- Queue depth: what depth triggers OOM? Test with the producer running 2× the consumer rate.

If the threshold is below your worst realistic load, you must add damping *now* — not when the
storm hits. By the time the loop is super-critical, you cannot control it from inside the loop.

## Catastrophe theory: leap vs gradual (§4.2)

(§4.2) The same qualitative change can happen **by leap** (sudden, discontinuous) or **by
gradual** (continuous), depending on conditions. The book's example: water → steam.
- At 1 atm, heating water to 100 °C produces a sudden phase change (boiling = leap).
- Above the critical point (374 °C, 218 atm), water turns to steam continuously, with no
  boiling point at all.

The implication for software: **the same change can be safe or catastrophic depending on
conditions**. Adding a new feature to a stable, well-tested codebase is gradual. Adding the
same feature to a system near its stability boundary is a leap — the system jumps to a new
attractor without passing through intermediate states.

## LLM behavior pattern: Know whether you're near a fold

> "Before a change, ask: am I on the smooth part of the surface, or near the fold where small
> changes cause leaps? Near a fold, the same change that was safe yesterday is catastrophic
> today."

Signs you're near a fold:
- The system is already at a resource boundary (memory, CPU, queue depth, context window).
- Small perturbations already produce disproportionate responses.
- There is no headroom — utilization is consistently > 80%.
- Multiple subsystems are tightly coupled with no decoupling margin.

Near a fold, you must either (a) move away from the fold first (add headroom), or (b) accept
that the change is a leap and prepare for the new stable state on the other side. You cannot
pretend the change is gradual.

## Worked example: cache eviction as ultra-stability + threshold

**System:** a CDN edge cache with a 10 GB limit. Daily traffic is 8 GB. Occasionally a viral
event pushes traffic to 30 GB.

- **Normal day**: cache is at 80% utilization. Stable state A: high hit rate, low origin load.
- **Viral day, no eviction**: cache fills, origin load spikes, latency rises, autoscaler
  thrashes. The system has moved to stable state B ("overloaded"). Reverting viral traffic
  alone may not return to A, because the autoscaler is now in a thrashing attractor.
- **Viral day, with LRU eviction**: the cache enters its unstable phase (eviction storm),
  hit rate drops temporarily, origin load rises briefly, then the cache reconverges to a
  new working set for the viral content. This is **ultra-stability**: the instability is the
  repair mechanism.
- **Disabling eviction to "fix" the instability**: removes the repair mechanism. The cache
  OOMs at 30 GB. Catastrophic failure.

The LLM must recognize: the eviction storm is not a bug. The bug would be *not having*
eviction. The fix is to ensure the threshold (eviction rate that triggers the storm) is above
the realistic peak, by tuning the eviction policy or increasing the cache size — not by
disabling eviction.

---

## Decision rule

- Is the system oscillating, or has it moved to a new attractor? The fixes differ.
- Is the instability a failure, or a repair mechanism (ultra-stability)? Don't patch over
  repairs.
- At a bifurcation, small choices lock in large differences. Name the candidate attractors
  explicitly.
- For positive-feedback loops, find the critical threshold. Test near it.
- Near a resource boundary, the same change is a leap, not a gradient. Add headroom first.
