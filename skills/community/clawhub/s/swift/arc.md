# ARC — Retain Cycles, Lifetime, and Objects That Never Die

ARC is deterministic: an object dies the instant its last strong reference goes. So "it leaked" always means *something still points at it*, and the job is to name that something. There is no garbage collector to blame and no delay to wait out.

## Prove It Leaked Before You Fix Anything

1. Put a breakpoint (or a `print`) in `deinit`. Navigate away. Silence = leak; noise = you were chasing a cached object, which is not a leak.
2. Xcode's Debug Memory Graph shows the retaining chain — read it backwards from the leaked node to the root. Purple `!` marks cycles specifically.
3. Instruments → Leaks finds unreachable allocations; it will NOT report a growing cache, an array nobody empties, or a Substring pinning a huge parent (`debugging.md`).
4. Only then edit. A `[weak self]` added on suspicion usually moves the bug rather than fixing it.

## The Five Cycles That Cause Most Leaks

| Cycle | Signature | Fix |
|---|---|---|
| Closure ↔ self | Object stores a closure that mentions `self` | `[weak self]` on stored/escaping closures only (SKILL.md rule 2) |
| Delegate ↔ owner | `var delegate: FooDelegate` declared strong | `weak var delegate: (any FooDelegate)?` — requires the protocol be `AnyObject`-constrained |
| Timer ↔ target | `Timer.scheduledTimer(target: self, …)` never fires `deinit` | The timer retains the target and the runloop retains the timer; invalidate from `viewWillDisappear`-style teardown, never from `deinit` (it will never run), or use the block API with `[weak self]` |
| NotificationCenter ↔ observer | Block-based `addObserver(forName:object:queue:using:)` | The center retains the block; store the returned token and `removeObserver(token)` — the selector-based API auto-removes on modern OSes, the block one does not |
| Parent ↔ child | Two objects each holding the other strongly | The child's back-reference is `weak` or `unowned` (rule 2) |

## Capture Lists, Precisely

- Capture lists evaluate at closure *creation*, not at call. `[value = self.count]` freezes the value then; `[weak self]` takes a weak reference then.
- `[weak self] in guard let self else { return }` pins `self` alive for the rest of that closure body — after the guard you are back to strong semantics, deliberately.
- `[unowned self]` is a bet that `self` outlives the closure. Losing the bet is a crash, not a nil (SKILL.md Crash Messages).
- Non-escaping closures cannot create a cycle: no capture list needed for `map`, `filter`, `forEach`, `withLock`, `sorted(by:)` (SKILL.md Traps).
- Capturing a property (`[count]`) instead of `self` is often the cleanest fix — no weakness, no cycle, no optional.
- Nested closures each need their own treatment: an inner closure that captures `self` strongly recreates the cycle even when the outer one is weak.

## `Task`, `async`, and Lifetime

- `Task { await self.load() }` retains `self` until the task finishes. That is usually correct — you want the work to complete — but a task that never finishes (an unbounded `for await`) keeps the object alive forever.
- Store long-lived tasks and cancel them in teardown. `.task` in SwiftUI does this for you.
- `[weak self]` inside a `Task` is only useful when the task can outlive the object legitimately; otherwise it turns a completed operation into a silently skipped one.
- An actor holding a `Task` that references the same actor is a cycle like any other; clear the handle in a `defer`.

## Weak, Unowned, and Their Costs

- `weak` requires a side table entry and a nil check on every read; `unowned` has neither but crashes on a dead target. On hot paths this is measurable; everywhere else, prefer safety.
- `unowned(unsafe)` removes even the crash check — a dangling read becomes EXC_BAD_ACCESS at some later, unrelated point. Only with a measured reason.
- `weak` cannot be used with non-class types, and cannot be `let`.
- A weak reference becomes nil *during* the target's deinit, so code in `deinit` cannot observe itself through someone else's weak reference.
- Collections do not hold weakly: `[Delegate]` retains everything. Use `NSHashTable.weakObjects()` on Apple platforms or a small `struct WeakBox<T: AnyObject> { weak var value: T? }` wrapper elsewhere, and prune nils on access.

## Growth That Is Not A Cycle

- **Caches without eviction.** `NSCache` evicts under pressure; a `[Key: Value]` dictionary does not. Anything called "cache" needs a bound.
- **Substrings and Data slices** keep their parent buffer alive (SKILL.md Traps). Copy at the boundary.
- **Unbounded streams**: an `AsyncStream` with default buffering holds every unconsumed element — give the stream an explicit `bufferingPolicy` or a slow consumer becomes a leak.
- **Autorelease growth on Darwin**: a tight loop creating Objective-C objects (image decoding, `NSString` bridging) accumulates until the runloop drains. Wrap the loop body in `autoreleasepool { }`.
- **Retain of the whole view hierarchy** via one captured closure — the leaked node is small, the graph behind it is not. Fix the edge, not the node.

## Deinit Discipline

- `deinit` runs on whichever thread released the last reference — not necessarily main. UIKit/AppKit teardown from `deinit` must hop, and hopping means the work happens after the object is gone: do teardown explicitly instead.
- `deinit` cannot access actor-isolated state (`concurrency.md`) and cannot be `async`.
- Never resurrect: passing `self` out of `deinit` is undefined behavior.
- A class that needs `deinit` for correctness (file handles, C resources, observers) is a signal the resource should own its own small wrapper type rather than living on a large object.
