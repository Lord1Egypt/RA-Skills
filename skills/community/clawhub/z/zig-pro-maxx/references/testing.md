# std.testing — Verified API Reference (Zig 0.16.0)

Source: `zig-0.16.0/lib/std/testing.zig`

---

## Running tests

```bash
zig test my_file.zig         # run all tests in a file
zig build test               # run via build.zig
```

All test functions are `fn() !void`. Failures propagate via `try`.

---

## Test allocator

```zig
// Verified from testing.zig line 21
pub const allocator: Allocator = allocator_instance.allocator();
```

Use `std.testing.allocator` in tests. It detects leaks automatically.

```zig
test "no leaks" {
    const buf = try std.testing.allocator.alloc(u8, 100);
    defer std.testing.allocator.free(buf);
    // If defer is removed, test fails with leak report
}
```

---

## `std.testing.expectEqual`

Verified signature from `testing.zig` line 81:
```zig
pub inline fn expectEqual(expected: anytype, actual: anytype) !void
```

Both arguments are coerced to a common type. `expected` comes first.

```zig
test "basic equality" {
    try std.testing.expectEqual(42, someFunction());
    try std.testing.expectEqual(true, 1 == 1);
    try std.testing.expectEqual(@as(u32, 100), count);
}
```

---

## `std.testing.expectError`

Verified from `testing.zig` line 62:
```zig
pub fn expectError(expected_error: anyerror, actual_error_union: anytype) !void
```

```zig
test "error handling" {
    try std.testing.expectError(
        error.OutOfMemory,
        failingFunction(),
    );
}
```

---

## `std.testing.expectEqualStrings`

Verified from `testing.zig` line 657:
```zig
pub fn expectEqualStrings(expected: []const u8, actual: []const u8) !void
```

```zig
test "string content" {
    const result = try buildString(std.testing.allocator);
    defer std.testing.allocator.free(result);
    try std.testing.expectEqualStrings("hello world", result);
}
```

---

## `std.testing.expectEqualSlices`

Verified from `testing.zig` line 364:
```zig
pub fn expectEqualSlices(comptime T: type, expected: []const T, actual: []const T) !void
```

```zig
test "slice equality" {
    const expected = [_]u32{ 1, 2, 3 };
    const actual   = [_]u32{ 1, 2, 3 };
    try std.testing.expectEqualSlices(u32, &expected, &actual);
}
```

---

## `std.testing.expect`

Verified from `testing.zig` line 614:
```zig
pub fn expect(ok: bool) !void
```

```zig
test "boolean assertion" {
    try std.testing.expect(someValue > 0);
    try std.testing.expect(str.len > 0);
}
```

---

## `std.testing.expectFmt`

Verified from `testing.zig` line 275:
```zig
pub fn expectFmt(expected: []const u8, comptime template: []const u8, args: anytype) !void
```

Tests that format output matches expected string:

```zig
test "formatting" {
    try std.testing.expectFmt("x = 42", "x = {d}", .{42});
    try std.testing.expectFmt("hello world", "{s} {s}", .{ "hello", "world" });
}
```

---

## Test structure patterns

### Basic test

```zig
const std = @import("std");

pub fn add(a: i32, b: i32) i32 {
    return a + b;
}

test "add function" {
    try std.testing.expectEqual(5, add(2, 3));
    try std.testing.expectEqual(0, add(-1, 1));
}
```

### Test with allocator

```zig
test "allocation test" {
    const allocator = std.testing.allocator;
    const result = try myAllocatingFunction(allocator);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("expected output", result);
}
```

### Comptime test (enforce invariants at compile time)

```zig
// Runs at compile time — fails compilation if false
comptime {
    std.debug.assert(@sizeOf(MyStruct) == 16);
    std.debug.assert(@alignOf(MyStruct) == 8);
}
```

### Test error cases

```zig
test "returns error on invalid input" {
    try std.testing.expectError(
        error.InvalidInput,
        parseValue("not-a-number"),
    );
}
```

---

## Testing with `std.testing.io`

For tests that need an `Io` instance (file I/O tests):

```zig
test "file operations" {
    const io = std.testing.io;
    var tmp = std.testing.tmpDir(.{});
    defer tmp.cleanup();

    const file = try tmp.dir.createFile(io, "test.txt", .{});
    defer file.close(io);
    // ...
}
```

---

## Quick reference

| Function | Purpose |
|----------|---------|
| `expectEqual(expected, actual)` | deep equality check |
| `expectEqualStrings(expected, actual)` | string content equality |
| `expectEqualSlices(T, expected, actual)` | slice content equality |
| `expectError(err, expr)` | assert expression returns error |
| `expect(bool)` | assert boolean is true |
| `expectFmt(expected, fmt, args)` | assert format output |
| `std.testing.allocator` | leak-detecting allocator |
| `std.testing.io` | test Io instance |
