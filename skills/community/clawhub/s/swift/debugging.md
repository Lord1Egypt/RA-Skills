# Debugging — Symptom to Cause in Minutes

Work symptom-first. Swift failures split into four families and each has a different first move: **runtime trap** (Swift printed a message), **memory error** (no message, EXC_BAD_ACCESS), **hang** (no message, no CPU), **compile failure** (the error you see is often not the error you have).

## The Universal First Three

1. Read the LAST console line before the crash, not the backtrace — Swift traps print their reason to stderr. Message present → decode it in SKILL.md Crash Messages.
2. `bt all` in LLDB (or Xcode's thread list). Thread 1 parked on a lock while other threads idle = hang, not crash.
3. Rebuild with `-Onone` and reproduce. If it stops reproducing, suspect an exclusivity or lifetime bug the optimizer exposed, not a compiler bug.

## LLDB — the commands that actually save time

| Command | Use |
|---|---|
| `v foo` (`frame variable`) | Reads memory directly. Works in optimized builds and when `po` errors out; no code is run |
| `po foo` | Runs the expression evaluator — richer output, but fails on optimized frames and can have side effects |
| `bt all` | Every thread. The only way to see which thread holds the lock the crashed one wants |
| `breakpoint set -E swift` | Break the instant any Swift error is thrown, before anyone catches it |
| `breakpoint set -n "MyClass.deinit"` | Prove whether an object dies at all (leak triage, `arc.md`) |
| `watchpoint set variable self.count` | Catch "who mutated this?" — the classic answer to unexplained state |
| `image lookup -a 0x…` | Turn a raw address from a crash report into file and line |
| `expr -l objc -- …` | Evaluate against the Objective-C runtime when Swift's evaluator refuses |

`po` failing with "error: Couldn't realize type" usually means the frame is optimized: switch to `v`, or add a temporary `@inline(never)`.

## Crash: nil unwrap or index out of range

1. Symbolicate to the exact line. If the crash log's top frame is stdlib, the caller one frame down is yours.
2. Reproduce with a breakpoint one line above; inspect with `v`, not `po` (the object may be half-initialized).
3. The fix is almost never "add another `?`" — find which invariant broke upstream. A nil that arrives from JSON means the payload contract changed; a nil read through a `weak` reference means the owner already deallocated.
4. Prevent the reprise: turn the assumption into a `guard … else { fatalError("…") }` naming it (SKILL.md rule 1).

## Crash: EXC_BAD_ACCESS with no Swift message

Ordered by frequency in Swift code:

1. **`unowned` reference read after deallocation** — this one DOES usually print a message; if it did, you are in the previous section.
2. **Objective-C object over-released or accessed after dealloc** — enable Zombie Objects (scheme diagnostics); the console then names the class and selector instead of crashing at a garbage address.
3. **Unsafe pointer escaping its scope** — `withUnsafeBytes { ptr in }` guarantees validity only inside the closure; storing `ptr` is undefined behavior that "works" until it doesn't (`interop.md`).
4. **Buffer overrun in C interop** — Address Sanitizer names the allocation and both stacks. Run the failing test under ASan before guessing.
5. **Stack overflow from unbounded recursion** — backtrace is thousands of identical frames; the address is near the stack guard page.

Zombies first (cheap, no rebuild), ASan second (rebuild, ~2× slower), Malloc Scribble/Guard Malloc only when ASan is inconclusive.

## Hang: no error, no CPU

| Signature in `bt all` | Cause | Fix |
|---|---|---|
| Every cooperative worker parked on `DispatchSemaphore.wait` | Blocking inside `async` starved the pool (SKILL.md rule 4) | Move the blocking call off the pool |
| Main thread waiting on a lock a background thread holds while it awaits main | Classic deadlock via `DispatchQueue.main.sync` | Never `.sync` onto main from code that main can call |
| One task suspended forever, no thread parked | Continuation never resumed (SKILL.md rule 5) | Audit each resume path; add a timeout wrapper while diagnosing |
| Main thread deep in layout or `Data(contentsOf:)` | Synchronous I/O or heavy work on main | Move off main; Main Thread Checker flags the UI half automatically |
| Everything idle, actor never progresses | Two actors awaiting each other | Break the cycle: one side takes a snapshot instead of calling back |

Hang debugging on device: sample the process rather than pausing — a paused app hides which frames were spinning.

## Data race: it only fails sometimes

1. Turn on **Thread Sanitizer** and run the suite. TSan reports the two stacks that raced, which is the entire answer; it is ~5-15× slower, so run it on a subset.
2. TSan and Address Sanitizer cannot run together — alternate.
3. TSan cannot see races the compiler already proved impossible, so a Swift 6 language-mode build catches a different, larger set at compile time. Use both: compile-time for your code, TSan for the Objective-C and C you inherited.
4. Non-reproducible ordering bugs that TSan calls clean are often hash-order dependence, not races.

## Memory growth and leaks

1. Xcode **Debug Memory Graph** while the app is live: purple `!` badges mark leaked cycles, and the graph shows which reference keeps the object alive. This finds cycles faster than Instruments.
2. **Instruments → Leaks** finds unreachable allocations; **Allocations** with "Mark Generation" finds the reachable-but-growing case (a cache nobody evicts), which Leaks never reports.
3. `deinit` breakpoint on the suspect class: if it never fires when the screen closes, you have a cycle.
4. Growth with flat object counts = buffers: Substrings pinning parent strings, `Data` accumulating, image caches, unbounded `AsyncStream` buffering.

## Compile failures worth naming

| Error | Real cause | Move |
|---|---|---|
| "The compiler is unable to type-check this expression in reasonable time" | Combinatorial overload resolution, not expression length | Split into `let`s with explicit types; measure with the flags in SKILL.md rule 8 |
| "Type of expression is ambiguous without more context" | Same cause, smaller expression | Annotate the closure's parameter and return types first |
| "Command CompileSwift failed with a nonzero exit code" | The wrapper, never the cause | Scroll UP to the first real diagnostic; in SwiftPM add `-v` |
| "Cannot convert value of type 'X' to expected argument type 'Y'" pointing at an unrelated line | One wrong type earlier poisoned inference | Fix the FIRST error only, then rebuild |
| "Undefined symbol: …" at link time | Missing `@objc`, a target not linked, or a `#if` that excluded the definition on this platform | `nm -gU` the object file to confirm the symbol was ever emitted |
| Segmentation fault in the compiler itself | Genuine compiler bug, usually in generics or macros | Bisect by commenting; reduce and file it; work around with an explicit type or a `@inline(never)` boundary |

## Print debugging without lying to yourself

- `#file`, `#function`, `#line` are free and precise: `print("\(#function):\(#line)")`.
- `os.Logger` interpolation is lazy and privacy-aware; `print` builds the string always (SKILL.md Traps).
- `dump(x)` beats `print(x)` for nested structures — it walks children via reflection.
- SwiftUI redraw mystery: `let _ = Self._printChanges()` at the top of `body` names the property that invalidated the view.
- Never leave a `print` inside `body`, `deinit`, or a hot loop — the measurement changes the thing measured.

## When You Are Truly Stuck

Cut the program in half: delete features until it stops failing, then restore the last one. A Swift failure surviving reduction to 30 lines is either a compiler bug or an assumption you never tested — both are now easy to prove.
