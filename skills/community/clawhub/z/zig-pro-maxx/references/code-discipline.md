# Code Discipline — Zig 0.16.0

Veteran rules. Every item here is something a senior Zig engineer would
block in review. Not style preferences — these are engineering decisions
that determine whether code survives contact with production.

---

## 1. Function discipline

### One function, one job

A function that needs a paragraph comment to explain what it does needs
to be split. The name should be the entire explanation.

```zig
// WRONG — does three unrelated things
fn processUser(allocator: std.mem.Allocator, raw: []const u8) !void {
    const user = try parseUser(raw);        // parse
    try validateEmail(user.email);          // validate
    try db.insertUser(user);               // persist
}

// RIGHT — each concern is named, testable, replaceable
fn parseUser(allocator: std.mem.Allocator, raw: []const u8) !User { ... }
fn validateUser(user: User) !void { ... }
fn persistUser(db: *Db, user: User) !void { ... }
```

### Function length

If a function doesn't fit on one screen (~50 lines), it's doing too much.
Split it. The Linux kernel enforces this. So do we.

### Parameter count

More than 4 parameters is a design smell. Group related parameters into
a struct:

```zig
// WRONG — too many positional parameters
fn renderTile(x: i32, y: i32, w: u32, h: u32, color: u32, alpha: u8) void { ... }

// RIGHT — grouped into a struct
const Tile = struct { x: i32, y: i32, w: u32, h: u32, color: u32, alpha: u8 };
fn renderTile(tile: Tile) void { ... }
```

---

## 2. Naming discipline

### Names are documentation

If you need a comment to explain a variable name, rename the variable.

```zig
// WRONG — cryptic
const n = buf.len;
const t = std.time.nanoTimestamp();
const r = try parseRecord(data);

// RIGHT — self-documenting
const byte_count     = buf.len;
const started_at_ns  = std.time.nanoTimestamp();
const record         = try parseRecord(data);
```

### Zig naming conventions (enforced by compiler in some contexts)

| Thing | Convention | Example |
|---|---|---|
| Types, structs, enums | `PascalCase` | `PacketHeader`, `ParseError` |
| Functions, variables | `camelCase` | `parseHeader`, `byte_count` |
| Constants (comptime) | `SCREAMING_SNAKE` or `camelCase` | `MAX_PACKET_SIZE` |
| Files | `snake_case.zig` | `packet_parser.zig` |

### Boolean names must be affirmative

```zig
// WRONG — double negation in conditionals is unreadable
const not_valid = !isValid(x);
if (!not_valid) { ... }

// RIGHT
const is_valid = isValid(x);
if (is_valid) { ... }
```

### Avoid noise words

`data`, `info`, `manager`, `handler`, `helper`, `utils` — these say nothing.
Name the thing by what it actually *is*.

```zig
const user_data    →   const user: User
const packet_info  →   const header: PacketHeader
fn handleError()   →   fn logAndAbort() or fn retryOrFail()
```

---

## 3. Memory discipline

### Stack first, heap as a last resort

Every heap allocation is a liability: it can fail, it can leak, it must
be freed. Ask before allocating:

1. Can this live on the stack? (fixed-size → yes)
2. Can an arena cover its lifetime? (request-scoped → yes)
3. Does it truly need dynamic lifetime? (then allocate)

```zig
// WRONG — heap for something that could be stack
fn formatPort(port: u16) ![]u8 {
    return std.fmt.allocPrint(allocator, "{d}", .{port});
}

// RIGHT — stack buffer, no allocator needed
fn formatPort(port: u16, buf: *[6]u8) []u8 {
    return std.fmt.bufPrint(buf, "{d}", .{port}) catch unreachable;
}
```

### Ownership must be explicit at the call site

Every function that allocates must say so in its signature and docs.
If a caller can't tell who owns memory by reading the call site, the
API is wrong.

```zig
/// Caller owns the returned slice. Free with `allocator.free`.
fn buildPath(allocator: std.mem.Allocator, dir: []const u8, file: []const u8) ![]u8 {
    return std.fmt.allocPrint(allocator, "{s}/{s}", .{ dir, file });
}
```

### Never store an allocator in a struct unless necessary

Storing an allocator couples the struct to an allocation strategy.
Pass it to the method that needs it instead:

```zig
// WRONG — couples struct to allocation strategy
const Parser = struct {
    allocator: std.mem.Allocator,
    fn parse(self: *Parser, input: []const u8) !Ast { ... }
};

// RIGHT — allocator is a parameter of the operation that needs it
const Parser = struct {
    fn parse(input: []const u8, allocator: std.mem.Allocator) !Ast { ... }
};
```

Exception: long-lived objects that allocate throughout their lifetime
(e.g. `ArrayList`) — storing the allocator is correct there.

### `errdefer` is not optional

Every fallible allocation must be protected by `errdefer` before the
next fallible operation. No exceptions.

```zig
// WRONG — leak on second alloc failure
const a = try allocator.alloc(u8, 64);
const b = try allocator.alloc(u8, 64); // if this fails, `a` leaks

// RIGHT
const a = try allocator.alloc(u8, 64);
errdefer allocator.free(a);
const b = try allocator.alloc(u8, 64);
errdefer allocator.free(b);
```

---

## 4. Error handling discipline

### Never discard errors silently

`_ = fallibleFn()` is almost always wrong. If you're discarding an error
you're making a decision — document it explicitly.

```zig
// WRONG — silent discard
_ = file.close();

// RIGHT — acknowledged decision
file.close() catch {}; // close errors are unrecoverable; ignore intentionally
```

### Error sets over `anyerror`

`anyerror` is a last resort. Use explicit error sets so callers know
exactly what can go wrong:

```zig
// WRONG — caller has no idea what errors to handle
fn readConfig(path: []const u8) anyerror!Config { ... }

// RIGHT — exhaustive, documentable, catchable
const ConfigError = error{ FileNotFound, ParseFailed, InvalidEncoding };
fn readConfig(path: []const u8) ConfigError!Config { ... }
```

### Handle errors at the right level

Don't propagate an error past the point where it can be meaningfully
handled. Don't handle it before you have enough context.

```zig
// WRONG — too low: file layer shouldn't log user-facing messages
fn readFile(path: []const u8) ![]u8 {
    return std.fs.cwd().readFileAlloc(...) catch |err| {
        std.debug.print("ERROR: cannot read config\n", .{});
        return err;
    };
}

// RIGHT — let it bubble; handle at the call site with context
fn loadConfig(path: []const u8) !Config {
    const raw = std.fs.cwd().readFileAlloc(...) catch |err| {
        std.debug.print("config file '{s}' unreadable: {s}\n",
            .{ path, @errorName(err) });
        return err;
    };
    ...
}
```

---

## 5. Type discipline

### Use the smallest correct integer type

Using `usize` or `u64` everywhere is lazy. Use the type that matches the
domain. It catches bugs at compile time:

```zig
const port:    u16  = 8080;   // ports are 0–65535
const fd:      i32  = -1;     // POSIX file descriptors are signed i32
const timeout: u32  = 5000;   // milliseconds fit in u32
```

### Prefer `comptime` over runtime branching for type logic

If a decision depends only on types, make it comptime:

```zig
// WRONG — runtime branch on type info
fn serialize(value: anytype) []u8 {
    if (@TypeOf(value) == u32) { ... }
    else if (@TypeOf(value) == []const u8) { ... }
}

// RIGHT — comptime dispatch
fn serialize(value: anytype) []u8 {
    return switch (@typeInfo(@TypeOf(value))) {
        .int  => serializeInt(value),
        .pointer => serializeBytes(value),
        else  => @compileError("unsupported type: " ++ @typeName(@TypeOf(value))),
    };
}
```

### Sentinel-terminated slices vs plain slices

Use `[:0]const u8` (null-terminated) only at C boundaries.
Everywhere else use `[]const u8`. Mixing them without reason creates
confusion and unnecessary casts.

---

## 6. Comment discipline

### Comments explain WHY, never WHAT

The code already says what. Comments that restate the code are noise.

```zig
// WRONG — restates the code
i += 1; // increment i

// WRONG — describes what is obvious
const mask: u8 = 0xFF; // a byte mask

// RIGHT — explains a non-obvious decision
// Align to 8 bytes: the hardware DMA engine requires 8-byte-aligned
// source buffers or it silently corrupts the transfer.
const aligned_size = (size + 7) & ~@as(usize, 7);
```

### Document contracts, not implementations

Public functions must document: what they require (preconditions), what
they guarantee (postconditions), and who owns returned memory.

```zig
/// Parse a RESP3 frame from `buf`.
///
/// Preconditions:
///   - `buf` must contain at least one complete frame (caller must buffer)
///   - `buf.len` must be > 0
///
/// Returns the parsed frame and the number of bytes consumed.
/// Caller owns `frame.data`; free with `allocator.free`.
///
/// Errors:
///   - `error.Incomplete` — frame is not yet complete; buffer more data
///   - `error.Malformed`  — protocol violation; close the connection
fn parseFrame(allocator: std.mem.Allocator, buf: []const u8) !struct {
    frame: Frame,
    consumed: usize,
} { ... }
```

### No commented-out code

Dead code belongs in git history, not in the file. Remove it.

---

## 7. Structure and layout discipline

### Structs: data first, methods second, tests last

Keep struct fields at the top. Methods below. Tests in a separate file
or at the very bottom of the same file.

```zig
const Connection = struct {
    // ── fields ──────────────────────────────────────────────────────────
    fd:       std.posix.fd_t,
    state:    State,
    buf:      [4096]u8,
    buf_len:  usize,

    // ── lifecycle ────────────────────────────────────────────────────────
    pub fn init(fd: std.posix.fd_t) Connection { ... }
    pub fn deinit(conn: *Connection) void { ... }

    // ── operations ───────────────────────────────────────────────────────
    pub fn read(conn: *Connection) !usize { ... }
    pub fn write(conn: *Connection, data: []const u8) !void { ... }
};
```

### Flat over nested

Deep nesting is a signal that logic should be extracted into a function
or that early returns should replace guard clauses:

```zig
// WRONG — pyramid of doom
fn process(input: ?[]const u8) !void {
    if (input) |data| {
        if (data.len > 0) {
            if (isValid(data)) {
                // ... actual work buried 3 levels deep
            }
        }
    }
}

// RIGHT — early returns flatten the logic
fn process(input: ?[]const u8) !void {
    const data = input orelse return error.NoInput;
    if (data.len == 0) return error.EmptyInput;
    if (!isValid(data)) return error.InvalidInput;
    // ... actual work at the top level
}
```

---

## 8. No unnecessary abstraction

### Don't abstract until you have two real users

Premature abstraction is worse than duplication. Write the concrete
code twice. The abstraction that fits both will be obvious. If it isn't,
you don't need one.

### Avoid wrapper types that add nothing

```zig
// WRONG — wrapping []const u8 in a struct with no added invariants
const Bytes = struct { inner: []const u8 };

// RIGHT — just use []const u8 directly
```

### Interfaces (comptime duck-typing) only when dispatch is genuinely needed

Zig's `anytype` is not free — it monomorphises at every call site.
Use it only when the generic behaviour is real, not to appear flexible.

---

## 9. Testability discipline

### Every exported function must have a test

If it's public, it's a contract. Contracts need tests.

### Tests must not depend on each other

Each test sets up its own state completely. Shared mutable state between
tests is a source of false positives and order-dependent failures.

### Test the error paths, not just the happy path

```zig
test "parseFrame returns Incomplete on short buffer" {
    const result = parseFrame(std.testing.allocator, "");
    try std.testing.expectError(error.Incomplete, result);
}

test "parseFrame returns Malformed on bad magic byte" {
    const result = parseFrame(std.testing.allocator, "\xFF\x00");
    try std.testing.expectError(error.Malformed, result);
}
```

### Name tests as sentences

`test "add"` tells you nothing when it fails.
`test "add returns overflow error when result exceeds u32 max"` tells you everything.

---

## 10. Performance discipline

### Measure before optimising

Never optimise code you haven't profiled. The bottleneck is almost never
where you think it is.

### Allocations inside hot loops are always wrong

```zig
// WRONG — allocates on every iteration
for (items) |item| {
    const label = try std.fmt.allocPrint(allocator, "item_{d}", .{item.id});
    defer allocator.free(label);
    render(label);
}

// RIGHT — stack buffer, zero allocations
var label_buf: [32]u8 = undefined;
for (items) |item| {
    const label = std.fmt.bufPrint(&label_buf, "item_{d}", .{item.id}) catch continue;
    render(label);
}
```

### Prefer data locality over pointer indirection

Arrays of structs (`[]Particle`) cache-miss on every field access when
you only need one field. Structs of arrays (`Particles{ .x: []f32, .y: []f32 }`)
let SIMD and prefetch work. Profile first; restructure when it matters.

---

## The one-line test

Before submitting any function, ask:

> "Could a new engineer, reading only this function and its signature,
>  understand what it does, what it requires, what it returns, and who
>  owns any allocated memory — without reading any other function?"

If the answer is no: rename, simplify, or document until it is.




# Code discipline and architecture

---

## Multi-file project layout

```
my-project/
├── build.zig             — build script (entry point for `zig build`)
├── src/
│   ├── main.zig          — program entry point; wires modules together
│   ├── parser.zig        — one concern per file
│   ├── types.zig         — shared type definitions (imported by many files)
│   └── util.zig          — pure helpers, no project-level imports
├── include/
│   └── mylib.h           — C header (if exposing a C API)
└── tests/
    └── parser_test.zig   — separate test files for complex modules
```

### Import graph rules

- The graph must be a **DAG** (directed acyclic graph) — no circular imports.
- `main.zig` imports everything; leaf modules import nothing from the project.
- `types.zig` only imports from `std`; other modules import `types.zig`.
- Library modules never import `main.zig`.

```zig
// src/parser.zig:
const types = @import("types.zig");   // ✅ imports a leaf module
const main  = @import("main.zig");    // ❌ would create a cycle
```

---

## Visibility — `pub` is opt-in

Default to **private** (no `pub`). Make something `pub` only when it is
explicitly part of the module's public API surface.

```zig
// Private implementation detail:
fn computeHash(data: []const u8) u64 { ... }

// Public contract:
pub fn lookup(map: *const Map, key: []const u8) ?Value {
    const h = computeHash(key);
    return map.buckets[h % map.capacity];
}
```

Fields of public structs are also private by default:

```zig
pub const Config = struct {
    max_connections: u32,       // private field
    pub timeout_ms: u32,        // public field (unusual — prefer accessor fns)
};
```

---

## Naming conventions

| Kind | Convention | Example |
|---|---|---|
| Functions | `camelCase` | `parseHeader`, `readByte` |
| Types (struct, enum, union, opaque) | `PascalCase` | `TokenKind`, `HttpClient` |
| Comptime-known constants | `SCREAMING_SNAKE` | `MAX_CONNECTIONS`, `VERSION` |
| Local variables / fields / params | `snake_case` | `byte_count`, `is_ready` |
| File names (modules) | `snake_case.zig` | `http_client.zig` |
| Error names | `PascalCase` (no suffix) | `error.InvalidToken` (not `error.EInvalidToken`) |

---

## Function design

```zig
// Good: allocator as first parameter when the function allocates
pub fn readAll(allocator: std.mem.Allocator, io: std.Io, path: []const u8) ![]u8 { ... }

// Good: receiver as first parameter for methods on a type
pub fn append(self: *List, allocator: std.mem.Allocator, item: Item) !void { ... }

// Bad: storing allocator in a struct that doesn't own the allocator lifetime
pub const Processor = struct {
    allocator: std.mem.Allocator, // fine ONLY if Processor truly owns all allocations
    // ...
};
```

---

## `const` by default

```zig
// const unless you need to mutate:
const result = try parse(input);

// var only when reassignment or mutation is required:
var total: u64 = 0;
for (items) |n| total += n;
```

---

## Error handling discipline

```zig
// Always handle errors explicitly — no `_ = try`:
const n = try std.fmt.parseInt(u32, input, 10);

// Discard only when you have a good reason (log it):
std.Io.Dir.cwd().deleteFile(io, "tmp.lock") catch |err| {
    std.log.warn("cleanup failed: {s}", .{@errorName(err)});
};

// errdefer for cleanup on error paths:
const buf = try allocator.alloc(u8, size);
errdefer allocator.free(buf);
try fill(buf);
return buf;  // errdefer does not fire here
```

---

## Hot-path discipline

```zig
// No allocations inside hot loops:
fn processAll(items: []const Item) void {
    var tmp: [256]u8 = undefined;  // stack buffer, declared once outside
    for (items) |item| {
        const label = std.fmt.bufPrint(&tmp, "item_{d}", .{item.id}) catch unreachable;
        render(label);
    }
}

// Prefer comptime constants over runtime computation:
const MAX_ITEMS = 1024;
comptime { std.debug.assert(MAX_ITEMS <= std.math.maxInt(u16)); }
```

---

## Comments — *why*, not *what*

```zig
// BAD — explains the what (code already says this):
// increment i by 1
i += 1;

// GOOD — explains the why (not obvious from code):
// Skip the BOM if present — Windows text editors often prepend it
if (std.mem.startsWith(u8, data, "\xEF\xBB\xBF")) data = data[3..];
```

---

## Struct design

```zig
// Group related data; avoid large flat parameter lists
pub const ConnectOptions = struct {
    host:           []const u8,
    port:           u16          = 443,
    timeout_ms:     u32          = 5000,
    tls:            bool         = true,

    // Provide a sensible default:
    pub const default: ConnectOptions = .{ .host = "localhost" };
};

pub fn connect(io: std.Io, opts: ConnectOptions) !Conn { ... }
```

---

## One file per concern

Avoid mega-files. Split when a file exceeds ~500 lines or contains
clearly separate concerns. Use `@import` to compose:

```zig
// parser.zig imports its own sub-concerns:
pub const Lexer  = @import("parser/lexer.zig").Lexer;
pub const Parser = @import("parser/parser.zig").Parser;
pub const Ast    = @import("parser/ast.zig").Ast;
```
