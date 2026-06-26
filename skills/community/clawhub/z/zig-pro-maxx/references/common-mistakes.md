# Common Mistakes — Zig 0.16.0

These are bugs and compile errors that will appear when writing lesson code.
Each entry was verified against the actual 0.16.0 source and compiler behavior.

---

## 1. Variable shadowing — compile error

```zig
// ERROR: local constant 'x' shadows local constant from outer scope
const x: u32 = 10;
{
    const x: u32 = 20; // COMPILE ERROR
}
```

**Fix:** use distinct names.

```zig
const base: u32 = 10;
{
    const inner: u32 = 20;
    _ = inner;
}
```

---

## 2. Using old allocator name

```zig
// ERROR: no field or member function named 'GeneralPurposeAllocator' in 'heap'
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
```

**Fix:**

```zig
var gpa: std.heap.DebugAllocator(.{}) = .init;
defer _ = gpa.deinit();
const allocator = gpa.allocator();
```

---

## 3. Using old std.io (lowercase)

```zig
// ERROR: no field 'io' in package 'std' (lowercase io was removed)
const stdout = std.io.getStdOut().writer();
```

**Fix for lessons:** use `std.debug.print`.
**Fix for production:** use `std.Io.File.stdout().writer(io, &buf)`.

---

## 4. Comparing strings with `==`

```zig
// WRONG — compares pointers, not content
if (name == "Alice") { ... }
```

**Fix:**

```zig
if (std.mem.eql(u8, name, "Alice")) { ... }
```

---

## 5. Implicit numeric coercion

```zig
// ERROR: expected type 'u64', found 'u8'
const small: u8 = 10;
const big: u64 = small;
```

**Fix:**

```zig
const big: u64 = @intCast(small);
```

Cast reference:
- `@intCast` — integer to integer (checked: panics if value doesn't fit)
- `@truncate` — integer to integer (unchecked: takes low bits)
- `@floatFromInt` — integer to float
- `@intFromFloat` — float to integer (truncates toward zero)
- `@floatCast` — float to different float type

---

## 6. Integer overflow in Debug mode

```zig
// RUNTIME PANIC in Debug/ReleaseSafe: integer overflow
const x: u8 = 255;
const y = x + 1; // panics
```

**Fix — use wrapping operator if intentional:**

```zig
const y = x +% 1; // wraps to 0
```

**Fix — use saturating operator if clamping is desired:**

```zig
const y = x +| 1; // saturates at 255
```

---

## 7. Non-exhaustive switch on enum

```zig
const Color = enum { red, green, blue };
const c = Color.red;
// ERROR: switch must handle all values
const name = switch (c) {
    .red   => "red",
    .green => "green",
    // missing .blue — compile error
};
```

**Fix — handle all cases:**

```zig
const name = switch (c) {
    .red   => "red",
    .green => "green",
    .blue  => "blue",
};
```

**Or use else for a catch-all:**

```zig
const name = switch (c) {
    .red => "red",
    else => "other",
};
```

---

## 8. `var` never mutated — compile error

```zig
// ERROR: variable is never mutated; consider using 'const'
var x: u32 = 10;
std.debug.print("{d}\n", .{x});
```

**Fix:** use `const` if you never reassign.

---

## 9. Accessing optional without unwrapping

```zig
const maybe: ?u32 = 42;
// ERROR: expected type 'u32', found '?u32'
const val: u32 = maybe;
```

**Fix — use orelse:**

```zig
const val = maybe orelse 0;
```

**Fix — use if capture:**

```zig
if (maybe) |val| {
    std.debug.print("{d}\n", .{val});
}
```

---

## 10. Forgetting `try` on fallible functions

```zig
// ERROR: error is discarded — must be handled with `try` or `catch`
const buf = allocator.alloc(u8, 100);
```

**Fix:**

```zig
const buf = try allocator.alloc(u8, 100);
// or
const buf = allocator.alloc(u8, 100) catch |err| {
    std.debug.print("alloc failed: {}\n", .{err});
    return;
};
```

---

## 11. Using `defer` return value incorrectly

```zig
// WRONG — defer runs LIFO (last in, first out)
// This frees buf BEFORE using it
const buf = try allocator.alloc(u8, 100);
defer allocator.free(buf);
defer std.debug.print("{d}\n", .{buf.len}); // runs SECOND — buf already freed
```

**Fix — defers run in reverse order. Be aware of ordering:**

```zig
const buf = try allocator.alloc(u8, 100);
defer std.debug.print("len: {d}\n", .{buf.len}); // runs SECOND (first deferred)
defer allocator.free(buf);                         // runs FIRST (last deferred)
```

---

## 12. `errdefer` vs `defer` confusion

```zig
// WRONG — defer always runs, even on success
// This frees the buffer even when you want to return it
fn createBuffer(allocator: std.mem.Allocator) ![]u8 {
    const buf = try allocator.alloc(u8, 100);
    defer allocator.free(buf); // frees on success too!
    return buf; // returns freed memory
}
```

**Fix — use `errdefer` to free only on error:**

```zig
fn createBuffer(allocator: std.mem.Allocator) ![]u8 {
    const buf = try allocator.alloc(u8, 100);
    errdefer allocator.free(buf); // only runs if we return an error
    // ... initialize buf ...
    return buf; // caller owns buf, errdefer does NOT run
}
```

---

## 13. Slice out of bounds

```zig
const arr = [_]u32{ 1, 2, 3 };
// RUNTIME PANIC: index out of bounds
const val = arr[5];
```

Zig checks slice bounds in Debug and ReleaseSafe builds.
Always validate indices before indexing, or use slice iteration.

---

## 14. `@sizeOf` vs `.len` confusion

```zig
const arr = [5]u32{ 1, 2, 3, 4, 5 };
const byte_size  = @sizeOf(@TypeOf(arr)); // 20 bytes (5 * 4)
const elem_count = arr.len;               // 5 elements
```

`arr.len` gives element count. `@sizeOf` gives byte count.
For slices: `slice.len` is element count, not bytes.

---

## 15. Wrong type for `std.testing.expectEqual`

```zig
// Sometimes needs explicit type annotation to resolve ambiguity
try std.testing.expectEqual(5, result); // may error if types differ

// Fix — annotate expected value
try std.testing.expectEqual(@as(u32, 5), result);
```

---

## 15b. Format specifier mismatches (compile errors)

```zig
// ERROR: invalid format string 'd' for type 'bool'
std.debug.print("{d}\n", .{true});     // use {} or {any} for bool

// ERROR: invalid format string 'd' for type '[]const u8'
std.debug.print("{d}\n", .{"hello"}); // use {s} for strings

// ERROR: unused argument in format string
std.debug.print("{d}\n", .{ 1, 2 });  // too many args

// ERROR: not enough arguments
std.debug.print("{d} {d}\n", .{1});   // too few args
```

---

## 16. Calling `.next()` directly on `std.process.Args` instead of `Args.Iterator`

`std.process.Args` is a **wrapper struct**, not an iterator. It has no `.next()` method and no `.len` field. Both guesses compile-fail with confusing errors.

```zig
// WRONG — Args has no .next()
const arg = init.args.next();   // compile error

// WRONG — Args has no .len
if (init.args.len == 0) { ... } // compile error
```

You must call `.iterate()` (Posix, no alloc) or `.iterateAllocator(alloc)` (cross-platform) first:

```zig
// RIGHT — Posix path
var it = init.args.iterate();
_ = it.next(); // skip program name
while (it.next()) |arg| { ... }

// RIGHT — cross-platform path (remember defer it.deinit())
var it = try init.args.iterateAllocator(allocator);
defer it.deinit();
_ = it.next(); // skip program name
while (it.next()) |arg| { ... }
```

The iterator's `.next()` returns `?[:0]const u8` — a null-terminated slice. The first call always yields the program name (argv[0]); call it once and discard before processing user arguments.

---

## 17. `ArrayList.init(allocator)` — compile error in 0.16.0

`std.ArrayList` is the **unmanaged** type in 0.16.0. It has no `init` method
that takes an allocator. Using the 0.15 pattern produces a confusing compile
error because `init` simply doesn't exist on this type.

```zig
// COMPILE ERROR — `init` does not exist on the Aligned (unmanaged) type
var list = std.ArrayList(u32).init(allocator);
```

**Fix — use the `.empty` sentinel:**

```zig
var list: std.ArrayList(u32) = .empty;
defer list.deinit(allocator);
```

---

## 18. `list.append(item)` without allocator — compile error in 0.16.0

Every mutating `ArrayList` method now takes `Allocator` as its first argument.
Omitting it produces a type-mismatch compile error that doesn't immediately
point to the missing allocator.

```zig
// COMPILE ERROR — expected Allocator as first argument
try list.append(42);
try list.appendSlice(&.{ 1, 2, 3 });
list.deinit();
```

**Fix — pass the allocator:**

```zig
try list.append(allocator, 42);
try list.appendSlice(allocator, &.{ 1, 2, 3 });
list.deinit(allocator);
```

Read-only methods (`list.items`, `list.items.len`, `pop`, `getLast`,
`swapRemove`, `orderedRemove`, iteration) do **not** take an allocator.

---

## 19. Holding a pointer into ArrayList across mutations

`ArrayList` may reallocate its backing buffer on any `append`,
`appendSlice`, `insert`, or `resize` that exceeds capacity. Any pointer
or reference into `list.items` taken before such a call becomes a
dangling pointer the moment reallocation happens.

```zig
// WRONG — ptr may dangle after append
const ptr = &list.items[0];
try list.append(allocator, new_value); // may reallocate; ptr is now dangling
std.debug.print("{d}\n", .{ptr.*});   // undefined behaviour

// RIGHT — use an index; re-derive the pointer after mutations
const index: usize = 0;
try list.append(allocator, new_value);
std.debug.print("{d}\n", .{list.items[index]}); // always valid
```

---

## 20. Mutating a HashMap while iterating it — undefined behaviour

Any call to `put`, `remove`, `fetchRemove`, or `getOrPut` during iteration
invalidates the iterator. The bug is silent in many cases — it may
silently skip entries or visit entries twice before crashing.

```zig
// WRONG — remove inside iterator loop
var it = map.iterator();
while (it.next()) |entry| {
    if (shouldDelete(entry.key_ptr.*)) {
        _ = map.remove(entry.key_ptr.*); // invalidates iterator
    }
}

// RIGHT — collect first, then remove
var to_delete: std.ArrayList(K) = .empty;
defer to_delete.deinit(allocator);

var it = map.iterator();
while (it.next()) |entry| {
    if (shouldDelete(entry.key_ptr.*)) {
        try to_delete.append(allocator, entry.key_ptr.*);
    }
}
for (to_delete.items) |key| _ = map.remove(key);
```

---

## 21. `allocPrint` inside a hot loop — always wrong

`std.fmt.allocPrint` performs a heap allocation on every call. Inside a
loop this turns an O(1) format into O(n) allocations, each of which can
fail and each of which must be freed.

```zig
// WRONG — allocation + free on every iteration
for (items) |item| {
    const label = try std.fmt.allocPrint(allocator, "item_{d}", .{item.id});
    defer allocator.free(label);
    render(label);
}

// RIGHT — stack buffer, zero allocations per iteration
var buf: [32]u8 = undefined;
for (items) |item| {
    const label = std.fmt.bufPrint(&buf, "item_{d}", .{item.id}) catch continue;
    render(label);
}
```

---

## 22. Forgetting `errdefer` after `allocPrint` when returning the result

`allocPrint` allocates memory the caller must free. If any fallible
operation between `allocPrint` and the `return` fails, the allocation
leaks unless guarded by `errdefer`.

```zig
// WRONG — leaks if validatePath fails
fn buildPath(allocator: std.mem.Allocator, dir: []const u8, file: []const u8) ![]u8 {
    const path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
    try validatePath(path); // if this errors, path leaks
    return path;
}

// RIGHT
fn buildPath(allocator: std.mem.Allocator, dir: []const u8, file: []const u8) ![]u8 {
    const path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
    errdefer allocator.free(path); // runs only if we return an error below
    try validatePath(path);
    return path; // caller owns path; errdefer does NOT run on success
}
```

---

## 23. `bufPrint` error name — `error.NoSpaceLeft`, not `error.BufferTooSmall`

The error returned when the buffer is too small for `bufPrint` is
`error.NoSpaceLeft`. Matching on `error.BufferTooSmall` compiles but
the branch is unreachable, so the actual overflow silently propagates.

```zig
// WRONG — wrong error name; the branch never fires
const out = std.fmt.bufPrint(&buf, "{s}", .{long_str}) catch |err| switch (err) {
    error.BufferTooSmall => return error.Overflow, // unreachable in 0.16.0
};

// CORRECT
const out = std.fmt.bufPrint(&buf, "{s}", .{long_str}) catch |err| switch (err) {
    error.NoSpaceLeft => return error.Overflow,
};
```

Verified: `BufPrintError = error{ NoSpaceLeft }` in `fmt.zig` line 591.
