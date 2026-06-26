# std.fmt — Verified API Reference (Zig 0.16.0)

Source: `zig-0.16.0/lib/std/fmt.zig`,
`zig-0.16.0/lib/std/Io/Writer.zig`

---

## Overview

`std.fmt` provides compile-time-verified format strings, number parsing,
and byte-encoding utilities. All format strings are checked at compile time —
a specifier mismatch is a **compile error**, never a runtime bug.

---

## Formatting into a fixed buffer — `std.fmt.bufPrint`

No allocator. Returns `error.NoSpaceLeft` if the buffer is too small.

```zig
pub fn bufPrint(buf: []u8, comptime fmt: []const u8, args: anytype) BufPrintError![]u8
```

`BufPrintError = error{ NoSpaceLeft }`.

```zig
var buf: [64]u8 = undefined;
const result: []u8 = try std.fmt.bufPrint(&buf, "port {d}", .{8080});
// result is a slice into buf — "port 8080"
// result.len == 9; buf itself is 64 bytes, only result.len bytes are valid

// Common pattern: fixed-size buffer for a known-bounded value
var port_buf: [6]u8 = undefined; // max port "65535" = 5 chars
const port_str = try std.fmt.bufPrint(&port_buf, "{d}", .{port});
```

### Null-terminated variant (`bufPrintSentinel`)

```zig
var buf: [64]u8 = undefined;
const result: [:0]u8 = try std.fmt.bufPrintSentinel(&buf, 0, "hello {s}", .{"world"});
// Use at C boundaries
```

---

## Formatting into heap memory — `std.fmt.allocPrint`

Allocates exactly the bytes needed. Caller owns the returned slice.

```zig
pub fn allocPrint(gpa: Allocator, comptime fmt: []const u8, args: anytype) Allocator.Error![]u8
```

```zig
const label = try std.fmt.allocPrint(allocator, "item_{d}", .{item.id});
defer allocator.free(label);

// errdefer pattern when label is returned to caller:
const label = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
errdefer allocator.free(label);
return label; // caller must free
```

### Null-terminated variant

```zig
const cstr: [:0]u8 = try std.fmt.allocPrintSentinel(allocator, 0, "{s}", .{name});
defer allocator.free(cstr);
```

---

## Counting output length — `std.fmt.count`

Returns the number of bytes the format string would produce, without
writing anywhere. Useful for pre-sizing buffers.

```zig
pub fn count(comptime fmt: []const u8, args: anytype) usize
```

```zig
const needed = std.fmt.count("item_{d}", .{item_id});
const buf = try allocator.alloc(u8, needed);
defer allocator.free(buf);
_ = try std.fmt.bufPrint(buf, "item_{d}", .{item_id});
```

---

## Parsing integers — `std.fmt.parseInt` / `parseUnsigned`

```zig
pub fn parseInt(comptime T: type, buf: []const u8, base: u8) ParseIntError!T
pub fn parseUnsigned(comptime T: type, buf: []const u8, base: u8) ParseIntError!T
```

`ParseIntError = error{ Overflow, InvalidCharacter }`.

```zig
// base 10
const n: i32  = try std.fmt.parseInt(i32, "−42", 10);
const n: u16  = try std.fmt.parseUnsigned(u16, "65535", 10);

// base 16 (no "0x" prefix needed when base is explicit)
const n: u8   = try std.fmt.parseUnsigned(u8, "FF", 16);

// base 0 — auto-detect from prefix (0b, 0o, 0x, else decimal)
const n: u32  = try std.fmt.parseInt(u32, "0xFF", 0);   // 255
const n: u32  = try std.fmt.parseInt(u32, "0b1010", 0); // 10
const n: u32  = try std.fmt.parseInt(u32, "0o17", 0);   // 15

// Error handling
const n = std.fmt.parseInt(u8, "999", 10) catch |err| switch (err) {
    error.Overflow        => return error.ValueTooLarge,
    error.InvalidCharacter => return error.BadInput,
};
```

`_` is allowed as a digit separator in the input string and is ignored.

---

## Parsing floats — `std.fmt.parseFloat`

```zig
pub fn parseFloat(comptime T: type, s: []const u8) ParseFloatError!T
```

`ParseFloatError = error{ InvalidCharacter }`.

```zig
const f: f64 = try std.fmt.parseFloat(f64, "3.14");
const f: f32 = try std.fmt.parseFloat(f32, "1e10");
const f: f64 = try std.fmt.parseFloat(f64, "-0.5");
```

---

## Parsing size suffixes — `std.fmt.parseIntSizeSuffix`

Accepts values like `"2G"`, `"4KiB"`, `"512MB"`.

```zig
pub fn parseIntSizeSuffix(buf: []const u8, digit_base: u8) ParseIntError!usize
```

```zig
const size: usize = try std.fmt.parseIntSizeSuffix("4KiB", 10); // 4096
const size: usize = try std.fmt.parseIntSizeSuffix("2G", 10);   // 2147483648
```

---

## Hex encoding / decoding

### `std.fmt.bytesToHex` — slice to hex string (comptime length)

```zig
pub fn bytesToHex(input: anytype, case: std.fmt.Case) [input.len * 2]u8
```

Input must be a comptime-known-length array (not a slice):

```zig
const bytes = [_]u8{ 0xDE, 0xAD, 0xBE, 0xEF };
const hex_str = std.fmt.bytesToHex(bytes, .lower); // "deadbeef"
const hex_str = std.fmt.bytesToHex(bytes, .upper); // "DEADBEEF"
// hex_str is [8]u8 — lives on the stack, no allocator
```

### `std.fmt.hexToBytes` — hex string to bytes

```zig
pub fn hexToBytes(out: []u8, input: []const u8) ![]u8
```

```zig
var buf: [4]u8 = undefined;
const decoded = try std.fmt.hexToBytes(&buf, "deadbeef");
// decoded is a slice of buf: [0xDE, 0xAD, 0xBE, 0xEF]
```

### `std.fmt.hex` — integer to hex bytes (little-endian)

```zig
pub fn hex(x: anytype) [@sizeOf(@TypeOf(x)) * 2]u8
```

```zig
const h = std.fmt.hex(@as(u32, 0xDEAD_BEEF));
// [8]u8 containing the little-endian hex representation
```

---

## Format specifier reference

All specifiers are verified at **compile time**. A mismatch → compile error.

### Integer specifiers

| Specifier | Output | Notes |
|-----------|--------|-------|
| `{d}` | decimal | works on all integer types |
| `{x}` | hex lowercase | `0xff` → `"ff"` |
| `{X}` | hex uppercase | `0xff` → `"FF"` |
| `{b}` | binary | `5` → `"101"` |
| `{o}` | octal | `8` → `"10"` |
| `{c}` | ASCII char | `u8` only |
| `{u}` | Unicode scalar | `u21` max |

### Float specifiers

| Specifier | Output |
|-----------|--------|
| `{d}` | decimal |
| `{e}` | scientific notation lowercase |
| `{E}` | scientific notation uppercase |

### String / bytes specifiers

| Specifier | Input type | Output |
|-----------|-----------|--------|
| `{s}` | `[]const u8` or `[*:0]const u8` | UTF-8 string |
| `{x}` | `[]const u8` | hex dump of bytes, lowercase |
| `{X}` | `[]const u8` | hex dump of bytes, uppercase |
| `{b64}` | `[]const u8` | base64 encoded *(new in 0.16.0)* |

### Special / type-aware specifiers

| Specifier | Output | Notes |
|-----------|--------|-------|
| `{}` | default | auto-selects per type |
| `{any}` | default | same as `{}` |
| `{?}` | optional | prints value or `null` |
| `{!}` | error union | prints value or error name |
| `{*}` | pointer address | hex address |
| `{t}` | tag name | enum/union/error tag *(new in 0.16.0)* |
| `{f}` | custom | calls `.format(writer)` on the value |
| `{D}` | duration | nanoseconds → human string *(new in 0.16.0)* |
| `{B}` | SI bytes | `1024` → `"1.024kB"` *(new in 0.16.0)* |
| `{Bi}` | IEC bytes | `1024` → `"1KiB"` *(new in 0.16.0)* |

### Width, precision, fill, alignment

```
{[specifier]:[fill][alignment][width].[precision]}
```

Alignment characters: `<` left · `>` right · `^` center

```zig
// Right-aligned, zero-filled, width 8
std.debug.print("{d:0>8}\n",  .{42});       // "00000042"

// Left-aligned, space-filled, width 10
std.debug.print("{s:<10}\n",  .{"hi"});     // "hi        "

// Center-aligned
std.debug.print("{d:^8}\n",   .{42});       // "   42   "

// Float precision: 3 decimal places
std.debug.print("{d:.3}\n",   .{3.14159}); // "3.142"

// Hex, zero-padded to 4 digits
std.debug.print("{x:0>4}\n",  .{0xFF});    // "00ff"

// Binary, zero-padded to 8 bits
std.debug.print("{b:0>8}\n",  .{@as(u8, 42)}); // "00101010"
```

### Named arguments

```zig
std.debug.print("{[name]s} is {[age]d}\n", .{ .name = "Alice", .age = 30 });
```

### Escaping braces

```zig
std.debug.print("use {{}} for braces\n", .{}); // prints: use {} for braces
```

---

## Custom `format` method on structs

Implement a `.format` method to control how your type prints with `{f}`:

```zig
const Point = struct {
    x: f32,
    y: f32,

    pub fn format(self: Point, writer: *std.Io.Writer) std.Io.Writer.Error!void {
        try writer.print("({d:.2}, {d:.2})", .{ self.x, self.y });
    }
};

const p = Point{ .x = 1.5, .y = -3.0 };
std.debug.print("point: {f}\n", .{p}); // "point: (1.50, -3.00)"
```

---

## Common mistakes

### Wrong specifier for type — compile error

```zig
std.debug.print("{d}\n", .{true});      // ERROR: {d} invalid for bool → use {}
std.debug.print("{d}\n", .{"hello"});   // ERROR: {d} invalid for []const u8 → use {s}
std.debug.print("{s}\n", .{42});        // ERROR: {s} invalid for integer → use {d}
```

### Argument count mismatch — compile error

```zig
std.debug.print("{d}\n",    .{ 1, 2 }); // ERROR: unused argument
std.debug.print("{d} {d}\n",.{1});      // ERROR: not enough arguments
```

### Using `allocPrint` in a hot loop — always wrong

```zig
// WRONG — heap allocation on every iteration
for (items) |item| {
    const label = try std.fmt.allocPrint(allocator, "item_{d}", .{item.id});
    defer allocator.free(label);
    render(label);
}

// RIGHT — stack buffer, zero allocations
var buf: [32]u8 = undefined;
for (items) |item| {
    const label = std.fmt.bufPrint(&buf, "item_{d}", .{item.id}) catch continue;
    render(label);
}
```

### Forgetting `errdefer` when `allocPrint` result is returned

```zig
// WRONG — leaks if subsequent code fails
fn buildPath(allocator: std.mem.Allocator, dir: []const u8, file: []const u8) ![]u8 {
    const path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
    try validatePath(path); // if this fails, path leaks
    return path;
}

// RIGHT
fn buildPath(allocator: std.mem.Allocator, dir: []const u8, file: []const u8) ![]u8 {
    const path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
    errdefer allocator.free(path);
    try validatePath(path);
    return path; // caller owns path; errdefer does NOT run
}
```
