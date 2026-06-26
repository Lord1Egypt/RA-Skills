# comptime — Zig's superpower

Read this whenever you write a generic function, use `@typeInfo`, build a
comptime interface, or need to do type-level computation.

---

## What `comptime` means

`comptime` forces an expression to be evaluated at compile time. The compiler
runs the expression, the result is embedded in the binary. No runtime cost.

```zig
const N = 1024;                          // implicitly comptime (integer literal)
comptime var idx: usize = 0;            // explicit comptime variable — rare
const T = comptime computeType();       // function result baked in at compile time
```

---

## Generic functions — `comptime T: type`

The canonical pattern. `T` is resolved at each call site; the compiler
monomorphises the function (like C++ templates, but no header hell).

```zig
fn sum(comptime T: type, slice: []const T) T {
    var total: T = 0;
    for (slice) |v| total += v;
    return total;
}

const s = sum(u32, &.{ 1, 2, 3 }); // T = u32 at compile time
```

`anytype` is shorthand — the compiler infers `T` from the argument:

```zig
fn printAny(val: anytype) void {
    std.debug.print("{any}\n", .{val});
}
```

---

## `@typeInfo` — type reflection

`@typeInfo(T)` returns a `std.builtin.Type` tagged union. Switch on it to
branch on the actual kind of type.

```zig
fn isSlice(comptime T: type) bool {
    return switch (@typeInfo(T)) {
        .pointer => |p| p.size == .slice,
        else => false,
    };
}

fn isOptional(comptime T: type) bool {
    return @typeInfo(T) == .optional;
}
```

### Iterating struct fields at comptime

```zig
fn printFields(val: anytype) void {
    const T = @TypeOf(val);
    inline for (@typeInfo(T).@"struct".fields) |field| {
        std.debug.print("{s} = {any}\n", .{
            field.name,
            @field(val, field.name),
        });
    }
}
```

### Iterating enum variants at comptime

```zig
fn enumNames(comptime E: type) []const []const u8 {
    const fields = @typeInfo(E).@"enum".fields;
    var names: [fields.len][]const u8 = undefined;
    for (fields, 0..) |f, i| names[i] = f.name;
    return &names;
}
```

---

## Comptime interfaces — duck typing via `anytype`

Zig has no interfaces keyword. Instead, pass `anytype` and rely on the
compiler to reject callers that don't have the required declarations.

```zig
/// Anything passed here must have a `.write([]const u8) !void` method.
fn writeAll(writer: anytype, data: []const u8) !void {
    try writer.write(data);
}
```

For richer contracts, use a comptime check to emit a clear error:

```zig
fn assertHasWrite(comptime T: type) void {
    if (!@hasDecl(T, "write")) {
        @compileError(@typeName(T) ++ " must declare pub fn write([]const u8) !void");
    }
}

fn writeAll2(writer: anytype, data: []const u8) !void {
    comptime assertHasWrite(@TypeOf(writer));
    try writer.write(data);
}
```

---

## Comptime-known values in data structures

```zig
// A type-indexed lookup table built entirely at compile time:
fn StaticMap(comptime K: type, comptime V: type, comptime entries: []const struct { K, V }) type {
    return struct {
        pub fn get(key: K) ?V {
            inline for (entries) |entry| {
                if (entry[0] == key) return entry[1];
            }
            return null;
        }
    };
}

const ColorMap = StaticMap([]const u8, u32, &.{
    .{ "red",   0xFF0000 },
    .{ "green", 0x00FF00 },
    .{ "blue",  0x0000FF },
});
```

---

## `inline for` vs `for` at comptime

`inline for` unrolls the loop at compile time. Required when the loop body
contains `comptime`-dependent expressions (e.g. field access by name).

```zig
inline for (0..8) |i| {
    std.debug.print("{d}\n", .{i}); // i is comptime-known each iteration
}
```

---

## Comptime branches with `if`

`if (comptime condition)` prunes dead branches from the binary:

```zig
fn debugOnly(comptime enable: bool, msg: []const u8) void {
    if (comptime enable) {
        std.debug.print("[debug] {s}\n", .{msg});
    }
}
```

---

## `@compileError` — user-friendly compile errors

```zig
fn mustBeUnsigned(comptime T: type) void {
    if (@typeInfo(T) != .int or @typeInfo(T).int.signedness != .unsigned) {
        @compileError("expected unsigned integer, got " ++ @typeName(T));
    }
}
```

---

## `comptime` assertions (not just in tests)

```zig
comptime {
    std.debug.assert(@sizeOf(Header) == 16);
    std.debug.assert(@alignOf(Packet) == 8);
}
```

These run at compile time, produce a compile error if they fail, and
disappear entirely from the final binary.

---

## `@Vector` comptime length

Vector lengths must be comptime-known. Use `std.simd.suggestVectorLength`:

```zig
const vec_len = std.simd.suggestVectorLength(f32) orelse 4;
const V = @Vector(vec_len, f32);
```

See `references/simd.md` for full SIMD patterns.

---

## `packed struct` and `extern struct`

```zig
// packed: bit-layout guaranteed, used for hardware registers / network headers
const Flags = packed struct(u8) {
    carry:    bool,
    zero:     bool,
    overflow: bool,
    _pad:     u5 = 0,
};

// extern: C-compatible layout (fields in declaration order, C alignment rules)
const Point = extern struct {
    x: f32,
    y: f32,
};

// Verify size at comptime:
comptime { std.debug.assert(@sizeOf(Flags) == 1); }
```

`packed struct` fields can be read and written with normal field access;
Zig handles the bit-masking. The integer backing type is in parentheses
after `packed struct`.
