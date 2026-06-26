# Error sets, tagged unions, and exhaustive switch

---

## Defining an error set

```zig
const ParseError = error{
    InvalidToken,
    UnexpectedEof,
    Overflow,
};
```

Error sets are types. Use them in return types:

```zig
fn parseInt(s: []const u8) ParseError!i64 {
    if (s.len == 0) return error.UnexpectedEof;
    return std.fmt.parseInt(i64, s, 10) catch return error.InvalidToken;
}
```

---

## Inferred error sets (the `!T` shorthand)

When you write `!T` without a named error set, Zig infers the set from
all `return error.X` statements and `try` calls in the function body.
This is convenient but makes the public API less explicit — for library
functions, name your error set.

```zig
// Inferred (fine for private helpers):
fn readByte(file: std.Io.File, io: std.Io) !u8 { ... }

// Named (better for public API):
pub fn readByte(file: std.Io.File, io: std.Io) ReadError!u8 { ... }
```

---

## Merging error sets

Use `||` to union two error sets:

```zig
const ParseError = error{ InvalidToken, UnexpectedEof };
const IoError    = error{ FileNotFound, PermissionDenied };

const AppError = ParseError || IoError;

fn run(path: []const u8, io: std.Io) AppError!void {
    const data = try std.Io.Dir.cwd().readFileAlloc(io, path, allocator, .unlimited);
    defer allocator.free(data);
    _ = try parseInt(data);
}
```

---

## `catch` patterns

```zig
// Propagate:
const n = try parseInt(s);

// Default value:
const n = parseInt(s) catch 0;

// Switch on error:
const n = parseInt(s) catch |err| switch (err) {
    error.InvalidToken  => return error.BadInput,
    error.UnexpectedEof => 0,
    error.Overflow      => return error.TooBig,
};

// Log and return:
const n = parseInt(s) catch |err| {
    std.log.err("parse failed: {s}", .{@errorName(err)});
    return err;
};
```

---

## Tagged unions

A tagged union associates a type tag (enum) with a payload. The active
variant is the only safe field to read.

```zig
const Value = union(enum) {
    int:    i64,
    float:  f64,
    string: []const u8,
    null_val,          // zero-payload variant
};
```

### Creating a tagged union value

```zig
const v1: Value = .{ .int = 42 };
const v2: Value = .{ .string = "hello" };
const v3: Value = .null_val;
```

### Exhaustive switch on a tagged union

```zig
fn display(v: Value) void {
    switch (v) {
        .int      => |n| std.debug.print("int: {d}\n",    .{n}),
        .float    => |f| std.debug.print("float: {d}\n",  .{f}),
        .string   => |s| std.debug.print("string: {s}\n", .{s}),
        .null_val =>     std.debug.print("null\n",        .{}),
        // No `else` — compiler will catch unhandled variants
    }
}
```

If you add a variant later without updating all switch statements, the
compiler rejects the code. This is the main advantage over bare integers.

### `std.meta.activeTag` — reading the tag without data

```zig
const tag = std.meta.activeTag(v);
if (tag == .int) { ... }
```

---

## Enums (not unions)

```zig
const Direction = enum { north, south, east, west };

fn opposite(d: Direction) Direction {
    return switch (d) {
        .north => .south,
        .south => .north,
        .east  => .west,
        .west  => .east,
    };
}
```

Enum with explicit integer values:

```zig
const Status = enum(u8) {
    ok       = 200,
    not_found = 404,
    error_    = 500,
};

const code: u8 = @intFromEnum(Status.ok); // 200
```

---

## Error union type syntax recap

| Syntax | Meaning |
|---|---|
| `T` | value, cannot fail |
| `!T` | inferred error set + T |
| `E!T` | named error set E + T |
| `anyerror!T` | any possible error + T (avoid in library code) |
| `error{}!T` | empty error set — function can never fail (unusual) |

---

## Common pitfall: shadowing error names

Zig error names are global; `error.Overflow` from `std` and your own
`error.Overflow` are the same error value. If a function catches
`error.Overflow` it catches all sources of that error name. Use distinct,
specific names for domain errors (`error.IntegerOverflow`, `error.BufferFull`).
