# Allocators — Verified API Reference (Zig 0.16.0)

Sources: `zig-0.16.0/lib/std/heap.zig`,
`zig-0.16.0/lib/std/heap/debug_allocator.zig`,
`zig-0.16.0/lib/std/heap/ArenaAllocator.zig`,
`zig-0.16.0/lib/std/heap/FixedBufferAllocator.zig`,
`zig-0.16.0/lib/std/mem/Allocator.zig`

---

## The Allocator interface

All allocators expose `std.mem.Allocator`. Code that allocates accepts this
interface, not a concrete type. This is the idiomatic pattern:

```zig
// CORRECT — accept the interface
fn createBuffer(allocator: std.mem.Allocator, size: usize) ![]u8 {
    return allocator.alloc(u8, size);
}

// WRONG — accept a concrete type (couples to implementation)
fn createBuffer(gpa: *std.heap.DebugAllocator(.{}), size: usize) ![]u8 {
    return gpa.allocator().alloc(u8, size);
}
```

### Core Allocator methods

```zig
const Allocator = std.mem.Allocator;

// Allocate slice of T with count elements
const slice = try allocator.alloc(T, count);   // returns []T
defer allocator.free(slice);

// Allocate a single item of type T
const ptr = try allocator.create(T);  // returns *T
defer allocator.destroy(ptr);

// Resize a slice (may fail if backing allocator can't resize in place)
// Returns new slice — old slice is invalid after this
slice = try allocator.realloc(slice, new_count);

// Free a slice
allocator.free(slice);

// Free a single item
allocator.destroy(ptr);
```

---

## `std.heap.DebugAllocator` (was `GeneralPurposeAllocator`)

**Name changed in 0.16.0.**

Source: `zig-0.16.0/lib/std/heap/debug_allocator.zig` line 163

```zig
pub fn DebugAllocator(comptime config: Config) type
```

### Correct usage pattern

```zig
var gpa: std.heap.DebugAllocator(.{}) = .init;
defer {
    const check = gpa.deinit();
    if (check == .leak) @panic("memory leak");
}
const allocator = gpa.allocator();
```

- `.init` is a comptime constant — no `{}` initializer needed
- `deinit()` returns `std.heap.Check` — either `.ok` or `.leak`
- To discard the leak result: `defer _ = gpa.deinit();`

### Config options (most commonly used)

```zig
// Default config (zero overhead in ReleaseFast)
var gpa: std.heap.DebugAllocator(.{}) = .init;

// With memory limit
var gpa: std.heap.DebugAllocator(.{ .enable_memory_limit = true }) = .init;
gpa.requested_memory_limit = 1024 * 1024; // 1MB

// Retain metadata after free (catches use-after-free in debug)
var gpa: std.heap.DebugAllocator(.{ .retain_metadata = true }) = .init;
```

### When to use

- Default choice for development and testing
- Shows leak locations with stack traces in Debug mode
- In ReleaseFast/ReleaseSmall the safety overhead is removed

---

## `std.heap.ArenaAllocator`

Frees all allocations at once when `deinit()` is called.
Individual `free()` calls are no-ops.

Source: `zig-0.16.0/lib/std/heap/ArenaAllocator.zig` lines 46–53

```zig
pub fn init(child_allocator: Allocator) ArenaAllocator
pub fn deinit(arena: ArenaAllocator) void
pub fn allocator(arena: *ArenaAllocator) Allocator
```

### Usage pattern

```zig
var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
defer arena.deinit(); // frees everything allocated from this arena

const allocator = arena.allocator();

const buf1 = try allocator.alloc(u8, 100);
const buf2 = try allocator.alloc(u8, 200);
// No need to free buf1 or buf2 individually
// arena.deinit() frees it all
```

### When to use

- Request/response cycles (web server handler)
- Parse then discard (parse JSON, process, arena.deinit)
- Any scope where all allocations have the same lifetime
- Avoids fragmentation and per-allocation overhead

---

## `std.heap.FixedBufferAllocator`

Allocates from a fixed-size buffer on the stack. No heap involvement.
Returns `error.OutOfMemory` when the buffer is exhausted.

```zig
var buffer: [4096]u8 = undefined;
var fba = std.heap.FixedBufferAllocator.init(&buffer);
const allocator = fba.allocator();

const data = try allocator.alloc(u8, 100);
// `data` lives inside `buffer`
// fba goes out of scope — no deinit needed
```

### When to use

- Embedded/no-std targets with no heap
- Hot paths where allocation latency must be zero
- Small, predictable allocations in a tight loop

---

## `std.heap.page_allocator`

Allocates directly from OS pages (mmap/VirtualAlloc).
No bookkeeping overhead. Frees entire pages.

```zig
const allocator = std.heap.page_allocator;
const buf = try allocator.alloc(u8, 4096);
defer allocator.free(buf);
```

Use as backing allocator for ArenaAllocator in production. Don't use
directly for small allocations (wastes page-sized chunks).

---

## `std.heap.smp_allocator` (new in 0.16.0)

Lock-free scalable allocator for multi-threaded programs.

Source: `zig-0.16.0/lib/std/heap.zig` line 353

```zig
const allocator = std.heap.smp_allocator; // already an Allocator
```

Only available on non-WASM, non-single-threaded targets.
`start.zig` uses this by default when not linking libc.

### When to use

- Production multi-threaded servers
- High contention allocators where DebugAllocator would bottleneck
- Replace DebugAllocator in `ReleaseFast` builds

---

## Explicit allocator passing pattern

The idiomatic Zig pattern: never use a global allocator.
Pass the allocator as a parameter everywhere.

```zig
const std = @import("std");

// All functions that allocate take an allocator
pub fn parseConfig(allocator: std.mem.Allocator, input: []const u8) !Config {
    const result = try allocator.create(Config);
    errdefer allocator.destroy(result);
    // ... parse input into result ...
    return result.*;
}

pub fn main() !void {
    var gpa: std.heap.DebugAllocator(.{}) = .init;
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Pass down, never store globally
    const config = try parseConfig(allocator, "...");
    _ = config;
}
```

---

## Allocator choice guide

| Situation | Use |
|-----------|-----|
| Development / testing | `DebugAllocator` |
| Single-owner, same-lifetime data | `ArenaAllocator` |
| Stack-only, bounded size | `FixedBufferAllocator` |
| Production multi-threaded | `smp_allocator` |
| Backing arena with OS pages | `page_allocator` |
| Linking C runtime | `std.heap.c_allocator` |
