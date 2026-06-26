# std.debug — Verified API Reference (Zig 0.16.0)

Source: `zig-0.16.0/lib/std/debug.zig`

---

## `std.debug.print`

```zig
pub fn print(comptime fmt: []const u8, args: anytype) void
```

- Writes to **stderr**
- Never fails — ignores write errors
- Uses a 64-byte internal buffer; flushes before returning
- Does NOT require an `Io` instance
- Thread-safe: acquires stderr mutex internally

**This is the correct output function for all lesson files.**

### Usage

```zig
const std = @import("std");
const print = std.debug.print; // alias to save typing

pub fn main() void {
    print("Hello, {s}!\n", .{"world"});
    print("value: {d}\n", .{42});
    print("pi ≈ {d:.4}\n", .{3.14159});
}
```

---

## `std.debug.assert`

```zig
pub fn assert(ok: bool) void
```

- If `ok` is false → `unreachable` (detectable illegal behavior)
- In Debug/ReleaseSafe builds: triggers a panic with stack trace
- In ReleaseFast/ReleaseSmall: undefined behavior (optimized away)
- Use for invariants that **must never** be false

```zig
const x: u32 = compute();
std.debug.assert(x > 0); // crash if x is 0
```

---

## `std.debug.panic`

```zig
pub fn panic(comptime format: []const u8, args: anytype) noreturn
```

- Equivalent to `@panic` but with a formatted message
- Always crashes — use for unrecoverable programmer errors

```zig
std.debug.panic("unexpected state: {d}", .{state});
```

---

## Format specifiers — complete list

Verified from `zig-0.16.0/lib/std/Io/Writer.zig` `printValue` function.

### Integer specifiers

| Specifier | Output |
|-----------|--------|
| `{d}` | decimal (base 10) |
| `{x}` | hex lowercase |
| `{X}` | hex uppercase |
| `{b}` | binary |
| `{o}` | octal |
| `{c}` | ASCII character (u8 only) |
| `{u}` | UTF-8 codepoint (u21 max) |

### Float specifiers

| Specifier | Output |
|-----------|--------|
| `{d}` | decimal |
| `{e}` | scientific notation lowercase |
| `{E}` | scientific notation uppercase |

### String specifiers

| Specifier | Output |
|-----------|--------|
| `{s}` | `[]const u8` slice, or `[*:0]const u8` C string |
| `{x}` | hex dump of bytes |
| `{X}` | hex dump of bytes, uppercase |
| `{b64}` | base64 encoded (new in 0.16.0) |

### Special specifiers

| Specifier | Output |
|-----------|--------|
| `{}` | default format (auto) |
| `{any}` | any type, uses default formatter |
| `{?}` | optional — prints value or `null` |
| `{!}` | error union — prints value or error name |
| `{*}` | pointer address |
| `{t}` | tag name for enum/union/error (new in 0.16.0) |
| `{f}` | calls `.format(writer)` method on type |
| `{D}` | nanoseconds formatted as duration (new in 0.16.0) |
| `{B}` | bytes in SI units: kB, MB, GB (new in 0.16.0) |
| `{Bi}` | bytes in IEC units: KiB, MiB, GiB (new in 0.16.0) |

### Width, precision, fill, alignment

```zig
// {[specifier]:[fill][alignment][width].[precision]}
print("{d:0>8}\n",   .{42});    // "00000042"  (right-align, zero-fill, width 8)
print("{d:<8}\n",    .{42});    // "42      "  (left-align, space-fill, width 8)
print("{d:^8}\n",    .{42});    // "   42   "  (center, space-fill, width 8)
print("{d:.3}\n",    .{3.14159}); // "3.142"  (3 decimal places)
print("{x:0>4}\n",   .{0xFF}); // "00ff"      (hex, zero-padded to 4)
print("{b:0>8}\n",   .{@as(u8, 42)}); // "00101010"
```

### Named arguments

```zig
print("{[name]s} is {[age]d}\n", .{ .name = "Alice", .age = 30 });
```

### Escaping braces

```zig
print("use {{}} for braces\n", .{}); // prints: use {} for braces
```

---

## `std.debug.dumpHex`

```zig
pub fn dumpHex(bytes: []const u8) void
```

Prints a hex dump of bytes to stderr. Useful for debugging binary data.

```zig
const data = [_]u8{ 0xDE, 0xAD, 0xBE, 0xEF };
std.debug.dumpHex(&data);
```

---

## What NOT to use in lesson code

```zig
// Do not use any of these in lessons — they require an Io instance:
std.io.getStdOut()              // lowercase io — removed in 0.16.0
std.io.getStdErr()
const w = stdout.writer()       // old writer() API
w.print("...", .{})             // this is the OLD writer interface
```
