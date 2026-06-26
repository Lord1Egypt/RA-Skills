# std Collections — Verified API Reference (Zig 0.16.0)

Sources: `zig-0.16.0/lib/std/array_list.zig`,
`zig-0.16.0/lib/std/hash_map.zig`,
`zig-0.16.0/lib/std/std.zig`

---

## CRITICAL 0.16.0 BREAKING CHANGE — `std.ArrayList` is now unmanaged

In **0.15 and earlier**, `std.ArrayList` stored the allocator and methods
did not take one. In **0.16.0**, `std.ArrayList(T)` maps to
`array_list.Aligned(T, null)` — the **unmanaged** variant. Every mutating
method now takes an explicit `Allocator` parameter.

```zig
// BROKEN — 0.15 style, will NOT compile on 0.16.0
var list = std.ArrayList(u32).init(allocator);
defer list.deinit();
try list.append(42);            // no allocator arg → compile error

// CORRECT — 0.16.0 style
var list: std.ArrayList(u32) = .empty;
defer list.deinit(allocator);
try list.append(allocator, 42); // allocator is first arg
```

---

## `std.ArrayList(T)` — dynamic array

Source: `zig-0.16.0/lib/std/array_list.zig` (the `Aligned` type, line 570)

### Initialisation

```zig
// Empty list — no allocation until first append
var list: std.ArrayList(u32) = .empty;

// Pre-allocate capacity for n elements (avoids reallocations)
var list = try std.ArrayList(u32).initCapacity(allocator, 64);
```

### Cleanup

```zig
// Always: pass the same allocator used during mutations
defer list.deinit(allocator);

// Or take ownership of the slice (deinit is then unnecessary)
const owned: []u32 = try list.toOwnedSlice(allocator);
defer allocator.free(owned);
```

### Core methods — all mutating methods take `gpa: Allocator` first

```zig
// Append one element — may allocate
try list.append(allocator, value);         // Allocator.Error!void

// Append a slice of elements
try list.appendSlice(allocator, &.{1, 2, 3}); // Allocator.Error!void

// Insert at index (shifts elements right)
try list.insert(allocator, index, value);  // Allocator.Error!void

// Remove by index — preserves order, O(n)
const removed = list.orderedRemove(index); // returns T

// Remove by index — swaps with last, O(1)
const removed = list.swapRemove(index);    // returns T

// Pop last element (returns null if empty)
const last: ?u32 = list.pop();

// Ensure capacity without changing length
try list.ensureTotalCapacity(allocator, n);
try list.ensureUnusedCapacity(allocator, n);

// Resize (extends with undefined values or truncates)
try list.resize(allocator, new_len);

// Clear without freeing memory
list.clearRetainingCapacity();

// Clear and free memory
list.clearAndFree(allocator);
```

### Reading elements — NO allocator needed

```zig
// Direct slice access — the most common pattern
const items: []u32 = list.items;
const count = list.items.len;
const first = list.items[0];

// Iterate
for (list.items) |item| {
    std.debug.print("{d}\n", .{item});
}

// Indexed loop
for (list.items, 0..) |item, i| {
    std.debug.print("[{d}] = {d}\n", .{ i, item });
}

// Get last element (asserts non-empty)
const last = list.getLast();

// Get last element or null
const maybe_last: ?u32 = list.getLastOrNull();
```

### Assume-capacity variants (no allocator, no error)

Use after `ensureUnusedCapacity` when you know there is room:

```zig
try list.ensureUnusedCapacity(allocator, items.len);
for (items) |item| {
    list.appendAssumeCapacity(item); // no allocator, no try
}
```

### Ownership transfer

```zig
// Give the slice to the caller; list becomes empty
const slice: []u32 = try list.toOwnedSlice(allocator);
// Caller must free: allocator.free(slice)

// Build from an existing heap-allocated slice
var list = std.ArrayList(u32).fromOwnedSlice(slice);
```

### Complete usage example

```zig
const std = @import("std");

pub fn main() !void {
    var gpa: std.heap.DebugAllocator(.{}) = .init;
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var list: std.ArrayList([]const u8) = .empty;
    defer list.deinit(allocator);

    try list.append(allocator, "alpha");
    try list.append(allocator, "beta");
    try list.append(allocator, "gamma");

    for (list.items, 0..) |s, i| {
        std.debug.print("[{d}] {s}\n", .{ i, s });
    }
}
```

---

## `std.AutoHashMap(K, V)` — hash map with auto-derived hash/eql

Source: `zig-0.16.0/lib/std/hash_map.zig` line 46

Unlike ArrayList, `std.AutoHashMap` and `std.StringHashMap` are
**managed** — they store the allocator, so methods do NOT take one.

```zig
// K must be a type with derivable hash (integers, pointers, small structs)
// For []const u8 keys, use StringHashMap instead
var map = std.AutoHashMap(u32, []const u8).init(allocator);
defer map.deinit();
```

### Initialisation and cleanup

```zig
var map = std.AutoHashMap(u32, []const u8).init(allocator);
defer map.deinit(); // frees the backing array; does NOT free keys/values

// If keys or values are heap-allocated, free them first:
// var it = map.iterator();
// while (it.next()) |entry| allocator.free(entry.value_ptr.*);
```

### Core operations

```zig
// Insert or overwrite
try map.put(key, value);           // Allocator.Error!void

// Insert only if key is absent; error if already present
try map.putNoClobber(key, value);  // Allocator.Error!void

// Lookup — returns null if not found
const val: ?[]const u8 = map.get(key);

// Lookup — returns pointer to value (allows in-place mutation)
const ptr: ?*[]const u8 = map.getPtr(key);
if (ptr) |p| p.* = "new value";

// Check existence
const found: bool = map.contains(key);

// Remove by key — returns true if it existed
const existed: bool = map.remove(key);

// Remove and return the key-value pair
const kv: ?std.AutoHashMap(u32, []const u8).KV = map.fetchRemove(key);

// Get or insert
const gop = try map.getOrPut(key);
if (!gop.found_existing) {
    gop.value_ptr.* = "default";
}

// Count
const n: u32 = map.count();
```

### Iteration

```zig
var it = map.iterator();
while (it.next()) |entry| {
    std.debug.print("{d} → {s}\n", .{ entry.key_ptr.*, entry.value_ptr.* });
}

// Keys only
var kit = map.keyIterator();
while (kit.next()) |key_ptr| {
    std.debug.print("key: {d}\n", .{key_ptr.*});
}

// Values only
var vit = map.valueIterator();
while (vit.next()) |val_ptr| {
    std.debug.print("val: {s}\n", .{val_ptr.*});
}
```

### Capacity management

```zig
// Pre-allocate to avoid rehashing
try map.ensureTotalCapacity(expected_count);
try map.ensureUnusedCapacity(additional_count);

// Clear without freeing backing memory
map.clearRetainingCapacity();

// Clear and free backing memory
map.clearAndFree();
```

---

## `std.StringHashMap(V)` — hash map with `[]const u8` keys

Source: `zig-0.16.0/lib/std/hash_map.zig` line 64

Identical API to `AutoHashMap` but with string key hashing built in.

```zig
var map = std.StringHashMap(u32).init(allocator);
defer map.deinit();

try map.put("alpha", 1);
try map.put("beta",  2);

const val = map.get("alpha"); // ?u32 → 1
const n   = map.count();      // u32 → 2
```

**Key lifetime:** the map does NOT copy keys. You must ensure the
`[]const u8` slice outlives the map entry.

```zig
// WRONG — key is a local slice; may be freed before map.get
const key = try allocator.dupe(u8, input_key);
defer allocator.free(key);       // freed too early if map outlives scope
try map.put(key, 42);

// RIGHT — transfer ownership; free when map is done with it
const key = try allocator.dupe(u8, input_key);
// key lives until map.deinit or until explicitly freed after map.remove
try map.put(key, 42);
```

---

## Choosing the right map type

| Situation | Use |
|-----------|-----|
| Integer or pointer keys | `std.AutoHashMap(K, V)` |
| String (`[]const u8`) keys | `std.StringHashMap(V)` |
| Custom hash/eql logic | `std.HashMap(K, V, Context, max_load_percentage)` |
| Ordered by insertion | `std.array_hash_map` |
| No allocator stored (arena pattern) | `std.AutoHashMapUnmanaged` |

---

## Common mistakes

### Forgetting the allocator argument on ArrayList

```zig
// COMPILE ERROR — 0.16.0 ArrayList.append requires allocator
try list.append(item);

// CORRECT
try list.append(allocator, item);
```

### Using ArrayList.init (old managed API — removed)

```zig
// COMPILE ERROR — no `init` on Aligned (the unmanaged type)
var list = std.ArrayList(u32).init(allocator);

// CORRECT
var list: std.ArrayList(u32) = .empty;
```

### Mutating while iterating a HashMap

```zig
// RUNTIME PANIC / undefined behaviour — iterator is invalidated
var it = map.iterator();
while (it.next()) |entry| {
    _ = map.remove(entry.key_ptr.*); // WRONG: mutates during iteration
}

// RIGHT — collect keys first, then remove
var to_remove = std.ArrayList(u32).empty;
defer to_remove.deinit(allocator);
var it = map.iterator();
while (it.next()) |entry| {
    try to_remove.append(allocator, entry.key_ptr.*);
}
for (to_remove.items) |key| _ = map.remove(key);
```

### Holding a pointer across ArrayList mutations

```zig
const ptr = &list.items[0];  // INVALID after any append that reallocates
try list.append(allocator, new_value); // may realloc; ptr is now dangling

// RIGHT — use an index, not a pointer
const index: usize = 0;
try list.append(allocator, new_value);
const val = list.items[index]; // safe: index into the current slice
```
