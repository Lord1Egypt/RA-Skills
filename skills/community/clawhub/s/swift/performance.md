# Performance — Build Time, Runtime, Binary Size

Three separate budgets with different tools. Never optimize any of them from a debug build: `-Onone` disables inlining, specialization, and ARC optimization, so debug measurements describe a program you do not ship.

## Measure First, In This Order

1. **Time Profiler** (Instruments) on a release build for CPU. Read the heaviest stack, not the flat list.
2. **Allocations** with Mark Generation for memory growth; **Leaks** only for cycles.
3. **`os_signpost`** intervals around your own phases — the profiler shows the machine's view, signposts show yours.
4. For a micro-question, a release-mode loop with `ContinuousClock().measure { }` and a `blackHole`-style sink beats intuition, but beware the optimizer deleting work whose result is unused.

## Runtime: The Costs Specific To Swift

- **ARC traffic.** Every pass of a class reference across a function boundary can retain and release, and those are atomic. In hot loops this dominates. Remedies in order: use value types; make classes `final`; hoist the reference out of the loop; last, `Unmanaged` (measured, documented).
- **Existential boxing.** A value stored in `any P` larger than three words is heap-allocated on each conversion. An array of `any P` in a hot path is the classic hidden allocator (`types.md`).
- **Dynamic dispatch.** Class methods go through a vtable, protocol requirements through a witness table, `@objc dynamic` through `objc_msgSend`. `final`, `private`, and whole-module optimization let the compiler devirtualize; a non-final public class method in a resilient library cannot be.
- **Generic specialization** turns generic code into concrete code and is where most of the speed comes from — but it only happens when the compiler can see the body: same module with WMO, or `@inlinable` across modules. Unspecialized generics run through witness tables and boxed values.
- **Copy-on-write** copies on the first write to a shared buffer. Passing a large array into a function that appends to it, while another reference exists, copies the whole array.
- **Bridging.** Crossing to Objective-C converts `String`/`Array`/`Dictionary`. A loop that calls a Foundation API per element can spend most of its time in bridging.
- **`Character`/`String` work** is Unicode-correct and therefore not free; byte-level algorithms should run on `utf8`.
- **Dynamic casts** (`as?`) hit runtime metadata; hoist them out of loops.
- **`Mirror`** walks metadata reflectively — fine for logging, never on a hot path.

## Allocation Discipline

- Value types can still allocate: any type holding a heap buffer (`String` above 15 UTF-8 bytes, `Array`, `Dictionary`, `Data`) allocates on creation and on COW copies.
- `reserveCapacity` before a known-size build; append-in-a-loop otherwise reallocates on a geometric schedule.
- `reduce(into:)` instead of `reduce` for anything with a buffer.
- `lazy` chains skip intermediate arrays; measure, because the closure indirection can outweigh the saving on small collections.
- On Darwin, tight loops creating Objective-C objects need `autoreleasepool { }` inside the loop body.
- `Data` slices and `Substring`s pin their parents — retained memory is not the same as allocated memory (SKILL.md Traps).

## Concurrency Performance

- The cooperative pool runs one thread per active core; oversubscribing it with blocking work is a correctness bug before it is a performance one (SKILL.md rule 4).
- Actor hops cost a context switch on the executor. Batch calls rather than awaiting per element.
- Task creation is an allocation: bound the width of a task group rather than spawning one task per item.
- Parallelism below roughly a millisecond of work per task is usually a loss; measure the serial version first.

## Build Time

| Symptom | Cause | Fix |
|---|---|---|
| One file takes minutes | Type-checker blowup | `-Xfrontend -warn-long-expression-type-checking=500` and split what it flags (SKILL.md rule 8) |
| Whole module rebuilds on any change | Debug builds default to incremental, but a change to a widely imported file invalidates its dependents | Narrow the public surface; split god-modules |
| Clean build slow after adding a package | swift-syntax compiled from source for a macro or plugin | Fewer macro dependencies, or accept it and cache `.build` in CI |
| Release build much slower than debug | WMO plus specialization across a large module | Split the module, or use `-Osize` where speed is not critical |
| Xcode fast, `swift build` slow (or vice versa) | Different settings and derived paths | Compare the actual flags before changing code |

- Explicit types on non-trivial `let`s reduce inference work. Blanket annotation everywhere is noise; annotate what the compiler complained about.
- Large `Codable` models and long SwiftUI `body` chains are the two heaviest generated-code sources in most apps.

## Binary Size

- Generic specialization duplicates code per concrete type; `@inline(never)` on a large generic body keeps one copy at the cost of a call.
- `-Osize` trades a few percent of speed for meaningful size reduction; a good default for large apps outside hot modules.
- Dead code stripping needs no dynamic reachability: `@objc`, `@_cdecl`, and reflection-driven lookups keep symbols alive that would otherwise be stripped.
- Fewer, larger modules link smaller than many small dynamic frameworks, and start faster (each dynamic library costs load time).
- `swift-demangle` over the largest symbols in the link map tells you which generic instantiations are actually costing you.

## The Rules That Survive Every Profile

- Algorithmic complexity first: an O(n²) `contains` in a loop dwarfs every micro-optimization on this page (`collections.md`).
- Optimize the measured 5%, and re-measure after every change; Swift's optimizer regularly makes the "obviously faster" version slower.
- Never trade correctness for speed silently: an `unowned(unsafe)` or `-Ounchecked` win must be documented where the next reader will see it.
