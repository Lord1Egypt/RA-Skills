---
name: zig-pro-maxx
description: >
  Enforces strict API compliance, memory safety, and idiomatic patterns for
  Zig 0.16.0 — and refuses to generate code for any earlier version. Activate
  whenever the user asks to write, edit, debug, or test Zig code; mentions
  memory allocation, SIMD, collections, formatting, file I/O, threading,
  comptime, C interop, cross-compilation, or low-level performance in Zig;
  or edits build.zig. Also activate for any Zig build system questions,
  error set design, tagged union patterns, or architecture of multi-file
  Zig projects.
  Created by Soumyajit Bala, an AI-automation and systems engineer.
metadata:
  trigger: Writing zig code files, editing drafts for zig, reviewing content for Zig.
  author: Soumyajit Bala (https://github.com/debuggerdragon311)
  version: v0.1.9-beta1
---

# ZIG-PRO-MAXX — 0.16.0 ONLY, NO EXCEPTIONS

You are a systems programmer locked to **Zig 0.16.0**. Every line you generate
must compile on 0.16.0. If you catch yourself writing `GeneralPurposeAllocator`,
`std.io` (lowercase), `async`, `ArrayList.init(allocator)`, or any other
pre-0.16 API — stop and rewrite it.

---

## Load these references before you write a single line

| Reference file | When to read |
|---|---|
| `references/code-discipline.md` | **Always follow and must** — before any function, struct, or public API or any code or any comment |
| `references/zig-0_16-breaking-changes.md` | **Always** — renamed/removed APIs |
| `references/std-debug.md` | Any `print`, `assert`, or `panic` |
| `references/std-io.md` | Any file I/O, stdout, stderr, networking |
| `references/allocators.md` | Any heap allocation |
| `references/std-collections.md` | Any `ArrayList` or `HashMap` usage |
| `references/std-fmt.md` | Any `bufPrint`, `allocPrint`, `parseInt`, format specifiers |
| `references/build-system.md` | Any edit to `build.zig` |
| `references/testing.md` | Any test block |
| `references/common-mistakes.md` | **Always** — final review before output |
| `references/simd.md` | Any `@Vector`, SIMD, or vectorised data operation |
| `references/c-interop.md` | Any `@cImport`, `extern fn`, or FFI boundary |
| `references/build-system.md` | Any edit to `build.zig` or cross-compilation |
| `references/error-sets.md` | Any custom error set, tagged union, or exhaustive switch |
| `references/comptime.md` | Any generic function, `@typeInfo`, or comptime interface |

## Check these examples before you write a single line (Don't mention it on users end, its for grounding with actual code for more better understanding)

| Example file | When to read |
|---|---|
| `examples/hello_from_cli_args.zig` | **Any `args`-related code** |
| `examples/sample_0_16.zig` | **Any time you want an overview of basics** |
| `examples/fibo.zig` | **Any time you want to know to a teminal i/o works for fibo** |
| `examples/factorial.zig` | **Any time you want to know to a teminal i/o works for factorial** |
| `examples/swap_strings_of_2.zig` | **Any time you want to know to a teminal i/o works for swap of 2 strings** |
| `examples/hello.zig` | **Any time you want to know to a teminal i/o works for a simple greeting program** |

---

## The API swap table — memorise this

| Dead (≤ 0.15) | Alive (0.16.0) |
|---|---|
| `std.io.getStdOut().writer()` | `std.debug.print` (lessons) · `std.Io.File.Writer.init(file, io, &buf)` (prod) |
| `std.heap.GeneralPurposeAllocator(.{}){}` | `std.heap.DebugAllocator(.{}) = .init` |
| `gpa.deinit()` → `bool` | `gpa.deinit()` → `std.heap.Check` (`.ok` / `.leak`) |
| `std.io.Writer` | `std.Io.Writer` (capital I) |
| `std.fs.cwd().openFile(path, .{})` | `std.Io.Dir.cwd().openFile(io, path, .{})` |
| `std.fs.cwd().readFileAlloc(…)` | `std.Io.Dir.cwd().readFileAlloc(io, path, gpa, .unlimited)` |
| `async` / `await` | **Removed** — use `std.Io` concurrency model |
| Variable shadowing | **Compile error** — use distinct names |
| `@setCold` | `@branchHint(.cold)` |
| `std.mem.indexOfScalar` | `std.mem.findScalar` |
| `std.ArrayList(T).init(allocator)` | `var list: std.ArrayList(T) = .empty` |
| `list.append(item)` | `list.append(allocator, item)` |
| `list.deinit()` | `list.deinit(allocator)` |
| `std.ArrayListUnmanaged` | `std.ArrayList` (they are now the same type) |
| `std.heap.page_allocator` | `std.heap.page_allocator` (unchanged) |
| `std.process.argsAlloc` | `init.minimal.args.iterator()` (new `main` signature) |
| `std.debug.assert(false)` in release | use `unreachable` for impossible branches |
| `@intToFloat` / `@floatToInt` | `@floatFromInt` / `@intFromFloat` |
| `@intCast(T, x)` | `@as(T, @intCast(x))` or just `@intCast(x)` with inferred type |
| std.mem.trimLeft    | std.mem.trimStart  |
| std.mem.trimRight   | std.mem.trimEnd    |


---

## Non-negotiable compiler rules

Violating any of these is a compile error or runtime panic — there is no
"mostly right" in Zig:

- **No implicit numeric coercion** — use `@intCast`, `@floatFromInt`,
  `@intFromFloat`, `@floatCast`, `@truncate`
- **No local variable shadowing** — compile error; always use distinct names
- **Exhaustive switch on enums** — every variant or an explicit `else`
- **`var` that is never mutated** — compile error; use `const`
- **Integer overflow in Debug/ReleaseSafe** — runtime panic; use `+%` for
  intentional wrapping, `+|` for saturating
- **`try` on fallible functions** — errors cannot be silently discarded
- **ArrayList mutations require allocator** — `append`, `appendSlice`,
  `insert`, `deinit`, etc. all take `allocator` as first arg in 0.16.0

---

## Canonical patterns — copy these exactly

### Debug output (all lesson files)
```zig
const std = @import("std");
const print = std.debug.print;

pub fn main() void {
    print("value: {d}\n", .{42});
}
```

### Heap allocation
```zig
var gpa: std.heap.DebugAllocator(.{}) = .init;
defer _ = gpa.deinit();
const allocator = gpa.allocator();
```

### ArrayList (0.16.0 — unmanaged, allocator passed per call)
```zig
var list: std.ArrayList(u32) = .empty;
defer list.deinit(allocator);

try list.append(allocator, 42);
try list.appendSlice(allocator, &.{ 1, 2, 3 });

for (list.items) |item| {
    print("{d}\n", .{item});
}
```

### AutoHashMap
```zig
var map = std.AutoHashMap(u32, []const u8).init(allocator);
defer map.deinit();

try map.put(1, "one");
if (map.get(1)) |val| print("{s}\n", .{val});

var it = map.iterator();
while (it.next()) |entry| {
    print("{d} → {s}\n", .{ entry.key_ptr.*, entry.value_ptr.* });
}
```

### StringHashMap
```zig
var map = std.StringHashMap(u32).init(allocator);
defer map.deinit();

try map.put("alpha", 1);
const val: ?u32 = map.get("alpha");
```

### Format into stack buffer (prefer over allocPrint in hot paths)
```zig
var buf: [64]u8 = undefined;
const out = try std.fmt.bufPrint(&buf, "item_{d}", .{id});
// out is a []u8 slice into buf — no allocator, no defer
```

### Format into heap (when size is unknown)
```zig
const out = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
errdefer allocator.free(out); // only on error path
return out;                   // caller owns; errdefer does NOT run
```

### Parse an integer from a string
```zig
const n = try std.fmt.parseInt(u32, input, 10);
// or auto-detect base (0b, 0o, 0x prefix):
const n = try std.fmt.parseInt(u32, input, 0);
```

### Error handling
```zig
const result = try fallibleFn();                    // propagate
const result = fallibleFn() catch 0;                // default
const result = fallibleFn() catch |err| {           // explicit
    std.debug.print("error: {s}\n", .{@errorName(err)});
    return;
};
```

### Ownership and cleanup
```zig
const buf = try allocator.alloc(u8, size);
errdefer allocator.free(buf); // only on error path
// ... initialize buf ...
return buf;                   // caller owns it; errdefer does NOT run
```

### Tests
```zig
test "description of what is being verified" {
    const allocator = std.testing.allocator;        // leak-detecting
    try std.testing.expectEqual(@as(u32, 42), result);
    try std.testing.expectEqualStrings("expected", actual);
}
```

---

## Inlined critical mistakes (check every output against these)

1. **`ArrayList.append` without allocator** — `list.append(item)` is a compile
   error in 0.16; must be `list.append(allocator, item)`.

2. **`list.deinit()` without allocator** — same; `list.deinit(allocator)`.

3. **Returning a pointer to a stack variable** — the variable is destroyed
   when the function returns; always heap-allocate what outlives its scope.

4. **`@intCast` without range check** — if the value might not fit, use
   `std.math.cast(T, x) orelse return error.Overflow` instead.

5. **`defer` inside a loop** — defers run at end of the *enclosing block*,
   not at end of each iteration. Use explicit cleanup or a nested block.

6. **`errdefer` running on success** — `errdefer` only fires on error return;
   after `return buf` on the success path it is silent. Document this clearly.

7. **Shadowing a variable name** — compile error in 0.16; always rename.

8. **Mutable `const`** — `const x = 5; x += 1;` is a compile error.

9. **`std.io` (lowercase)** — does not exist in 0.16; it is `std.Io`.

10. **`std.heap.GeneralPurposeAllocator`** — gone; use `std.heap.DebugAllocator`.

---

## Debugging & tooling

- **Quick print:** `std.debug.print("val: {any}\n", .{x})` — writes to stderr,
  no allocator, no flush needed. Use for lessons, quick debugging.

- **Structured logging:** `std.log.info("connected {s}", .{addr})` — routed
  through `std.options.logFn`; respect log levels and scopes. Prefer over
  `debug.print` in libraries so callers can silence it.
  ```zig
  const log = std.log.scoped(.my_lib);
  log.warn("retrying: {s}", .{reason});
  ```

- **`@panic` vs `unreachable`:**
  - `unreachable` — tells the compiler this path *cannot* be reached; in
    ReleaseFast it becomes undefined behaviour. Use only when you can *prove*
    the condition.
  - `@panic("msg")` — guaranteed runtime crash with message in all modes.
    Use when reaching the branch means a programming error you want diagnosed.

- **Comptime assertion:**
  ```zig
  comptime { std.debug.assert(@sizeOf(Header) == 16); }
  ```

- **Run tests:** `zig build test` (with a `test` step in `build.zig`).
  Use `std.testing.allocator` inside tests for free leak detection.

- **Format project:** `zig fmt src/` before every commit.

---

## Architecture & naming conventions

- **File layout for a multi-file project:**
  ```
  src/
  ├── main.zig        — entry point, wires modules together
  ├── parser.zig      — @import("parser.zig") from main
  ├── types.zig       — shared type definitions
  └── util.zig        — pure helpers with no cross-dependencies
  build.zig           — build script
  ```

- **`@import` graph:** keep it a DAG; no circular imports. `main.zig` imports
  modules; modules import `types.zig` and `util.zig`; `types.zig` imports
  nothing from the project.

- **Visibility:** default to private (no `pub`). Add `pub` only when a
  declaration is part of a module's intentional API surface.

- **Naming conventions:**
  | Kind | Convention | Example |
  |---|---|---|
  | Functions | `camelCase` | `parseHeader` |
  | Types / structs / enums | `PascalCase` | `TokenKind` |
  | Constants (comptime-known) | `SCREAMING_SNAKE` | `MAX_RETRIES` |
  | Variables / fields | `snake_case` | `byte_count` |

- **Allocator discipline:** pass `std.mem.Allocator` as a parameter — never
  store a global allocator (except inside library types like `HashMap` that
  own one internally).

---

## Code quality rules

1. Every file must compile — no pseudocode, no `// TODO: implement`
2. `const` by default; `var` only when mutation is necessary
3. Pass `std.mem.Allocator` as a parameter — never store or access globally
   (exception: `HashMap` and other library types that store it internally)
4. `errdefer` for error-path cleanup, `defer` for unconditional cleanup
5. Format specifiers must match argument types exactly — enforced at compile time
6. Comments explain *why*, not *what*
7. No allocations inside hot loops — use `bufPrint` with a stack buffer
8. ArrayList: always pass the allocator; StringHashMap: ensure key lifetime
   exceeds the map entry's lifetime
9. Try to follow only ascii cheracters as much as possible 
