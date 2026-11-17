# Reference: Multivariable — Decouple What Hurts, Coordinate What Helps

Book anchors: §6.2–§6.3 (multi-variable control, non-interaction / diagonalization),
§6.7 (coordination control: coordination error, internal setpoint, disturbance compensation).

## Codebases are multivariable

Real systems have many modules and concerns coupled through shared state, APIs, and data.
The control question (§6.3) is: *which cross-terms must be zero, and which may stay?*

### Decoupling (§6.3, "non-interacting control")

- When two concerns must not interfere, drive the cross-terms to zero: isolate, single
  responsibility, pure functions, no shared mutable state, explicit interfaces.
- Once diagonalized, each subsystem can be designed as its own single-variable system —
  dramatically simpler (§6.3). This is the control-theory justification for modular design.

## LLM behavior pattern: Evaluate coupling before changing structure

> "Decouple harmful coupling; keep beneficial coupling. Do not default to 'isolate everything'."

When proposing a refactor or architecture change, the LLM **must** distinguish:
- **Harmful coupling**: cross-terms that cause instability, race conditions, or incorrect results
  under perturbation. These must be driven to zero.
- **Beneficial coupling**: synchronization, shared invariants, backpressure that keeps the
  system coherent. Removing these creates residual coupling elsewhere.

Blindly removing all coupling: complicates the system (more sensors/actuators to fake the
lost natural coupling); leaves residual coupling that *worsens* quality because the real plant
is uncertain.

## Coordination (§6.7) — do NOT over-decouple

> Non-interacting control is not the only design principle. Often subsystems must *cooperate*
> and stay in a coordination relation, not be independent.

- Some coupling is **beneficial**: forced synchronization, shared invariants, mechanical
  coupling that keeps things in lockstep.
- Keep helpful coupling; cancel only the **harmful** cross-talk (§6.7: use controller coupling
  to offset harmful plant coupling, preserve beneficial plant coupling).

## Coordination error (协调偏差) — control the relation, not just absolutes

- For coupled subsystems, regulate the **relation** between variables (e.g. "these two must
  stay consistent / proportional / in sync"), not only each variable's absolute value.
- Use an **internal setpoint**: when one subsystem moves, re-derive the others' targets from
  the *actual* state, so the whole returns to coordination. External fixed setpoints alone
  cannot hold a coordination relation under disturbance.
- Example mappings: distributed cache + DB (consistency relation); producer/consumer queues
  (backpressure relation); replicated services (quorum/sync relation).

## Worked example: shared mutable state → harmful coupling / beneficial coupling

**Harmful coupling (before):**
```python
# module_a.py
_counter = 0

def increment():
    global _counter
    _counter += 1

# module_b.py  
from module_a import _counter

def report():
    return _counter        # reads mutable state module_a owns
```
`module_b.report()` correctness depends on `module_a` execution order. Under concurrency
this is a race condition — the cross-term is nonzero and causes instability. Decouple with
explicit interface:

**After (decoupled):**
```python
# module_a.py
_state = {"count": 0}

def increment(state):
    state["count"] += 1
    return state

# module_b.py — no knowledge of module_a internals
def report(state):
    return state["count"]
```

**Beneficial coupling (preserved):**
```python
# Producer/consumer with backpressure (keep this coupling)
queue = asyncio.Queue(maxsize=100)

async def producer():
    for item in source():
        await queue.put(item)     # natural back pressure

async def consumer():
    while True:
        item = await queue.get()  # consumption rate regulates production rate
```
Removing the queue and calling producer/consumer independently destroys the natural
coordination. Regulate the *relation* (producer rate ≤ consumer rate), not just each
absolute.

---

## Decision rule

- Will interference cause incorrectness or instability? → **decouple** (diagonalize).
- Must subsystems move together or hold a ratio/invariant? → **coordinate** (internal
  setpoint + relation feedback), keep beneficial coupling.
- Uncertain which? Prefer the simpler structure, then *test the coupling* under disturbance
  before adding decoupling machinery.
