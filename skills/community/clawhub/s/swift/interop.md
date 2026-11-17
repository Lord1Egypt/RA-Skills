# Interop — Objective-C, C, C++, and Unsafe Pointers

Everything here is a boundary where Swift's guarantees stop. The rule that prevents most of the damage: **convert at the edge**. Bridge once, into a Swift-native type, and never let a raw pointer, an unaudited optional, or an `Any` travel inward.

## Objective-C From Swift

- Nullability drives everything. An unaudited header imports every object pointer as an implicitly unwrapped optional, so a nil you never expected crashes at the use site (`optionals.md`). Annotate with `NS_ASSUME_NONNULL_BEGIN`/`END` plus `nullable` where it applies — one header edit removes a class of crashes.
- Lightweight generics (`NSArray<NSString *> *`) import as `[String]`; unparameterized collections import as `[Any]` and force casts at every use.
- `NS_ENUM` imports as a Swift enum (exhaustive); `NS_OPTIONS` as an `OptionSet`. `NS_CLOSED_ENUM` promises no new cases, letting you switch without `@unknown default`.
- Methods with an `NSError **` out-parameter import as `throws`. A bridged call that returns nil with no error still throws a generic error — check both.
- Objective-C blocks import as escaping closures. A block that captures `self` creates a cycle exactly as a Swift closure does.
- `NS_SWIFT_NAME`, `NS_SWIFT_UI_ACTOR`, and `NS_SWIFT_SENDABLE` shape the Swift-side API from the header, which is the cheapest way to make an old framework pleasant and concurrency-clean.

## Swift Exposed To Objective-C

- Only `@objc` members of `NSObject` subclasses are visible. Structs, enums with payloads, generics, tuples, and protocols with associated types cannot be exposed at all.
- `@objc dynamic` is required for KVO, method swizzling, and anything else that resolves through the runtime — plain `@objc` alone is not enough.
- `#selector` requires the target method be `@objc`, and the compiler checks the shape, so prefer it over `Selector("name:")` strings, which fail at runtime.
- `@objcMembers` exposes everything in a type; convenient, and it defeats dead-code stripping for the whole class.
- The generated header (`<Module>-Swift.h`) is what Objective-C sees; a symbol missing there means the annotation did not take.

## C From Swift

- SwiftPM: a C target with headers in `include/` and (for anything non-trivial) a `module.modulemap`. Xcode: a bridging header. Mixing both in one target is not supported.
- C types map predictably: `int` → `Int32`, `char *` → `UnsafeMutablePointer<CChar>`, `size_t` → `Int`. Never assume `Int` matches `int` — it is 64-bit on the platforms you care about.
- Fixed-size C arrays import as **tuples**, which is unusable; access them via `withUnsafeBytes` or wrap them in C accessor functions.
- `String(cString:)` copies into a Swift `String`. Passing a Swift string out: `str.withCString { ptr in }` — the pointer is valid only inside that closure.
- Memory ownership must be written down at the boundary: who allocates, who frees. A `strdup`ed buffer handed to Swift needs a matching `free`, and Swift will not do it for you.

## C Callbacks and Context

C function pointers cannot capture context. The universal pattern is a `void *` user-data slot:

```swift
let box = Unmanaged.passRetained(Context(handler: handler)).toOpaque()
c_register_callback({ userData in
    guard let userData else { return }
    let ctx = Unmanaged<Context>.fromOpaque(userData).takeUnretainedValue()
    ctx.handler()
}, box)
// on unregister:
Unmanaged<Context>.fromOpaque(box).release()
```

- `passRetained` + `takeUnretainedValue` for a long-lived registration, released explicitly at unregister. `passUnretained` only when something else provably owns the object for the whole window.
- Forgetting the `release` is a permanent leak that Leaks will not report as a cycle; calling it twice is an over-release crash.
- A closure that captures anything cannot be converted to a `@convention(c)` function pointer — the compiler says so, and the workaround is always the box above.

## Unsafe Pointers

- Scope is the whole game: `withUnsafeBytes`, `withUnsafeMutableBufferPointer`, and `withCString` guarantee validity **only inside the closure**. Storing or returning the pointer is undefined behavior that appears to work until an unrelated allocation moves (SKILL.md Crash Messages).
- `UnsafeMutablePointer.allocate(capacity:)` must be paired with `initialize`, `deinitialize`, and `deallocate`. Skipping `deinitialize` for a type with references leaks; skipping it for trivial types is harmless but still wrong to habitualize.
- Type punning must go through `withMemoryRebound(to:capacity:)`; casting pointer types directly breaks strict aliasing and produces optimizer-dependent bugs.
- Alignment matters: loading a `UInt32` from an unaligned address traps on some architectures. Use `loadUnaligned(fromByteOffset:as:)`.
- `Array.withUnsafeBufferPointer` is fine; `&array` as an inout-to-pointer conversion is only valid for the duration of that single call.
- Address Sanitizer is the tool for every bug in this section; guessing is not.

## C++ Interop

- Enabled per target (`.interoperabilityMode(.Cxx)`), and it is viral: a Swift target using C++ interop exports that requirement to its Swift consumers, so keep the C++ boundary in one leaf target.
- What maps cleanly: value types with copy constructors, `std::string`, `std::vector`, simple class hierarchies, functions and methods.
- What does not: templates the compiler cannot instantiate from Swift, exceptions (a C++ exception crossing into Swift terminates the process), and multiple inheritance.
- Lifetime is not checked across the boundary. A Swift value holding a C++ reference into a container that reallocates is a use-after-free with no diagnostic.

## Foundation and Platform Bridging

- `String`↔`NSString`, `Array`↔`NSArray`, `Dictionary`↔`NSDictionary` bridge automatically. Some bridges are lazy in one direction and copying in the other; per-element bridging in a loop is a visible profiler entry.
- `Data` and `NSData` bridge in O(1) in most cases; `Data(referencing:)` shares storage.
- `NSNull` is a non-nil object standing in for JSON null.
- Core Foundation types bridge with `as`, but `CF`-prefixed create/copy functions still follow the Create Rule: what you create, you release (`takeRetainedValue`); what you get, you do not (`takeUnretainedValue`).
- None of this exists on Linux: `@objc`, KVO, `NSSelectorFromString`, and CF bridging are Darwin-only (`linux.md`).
