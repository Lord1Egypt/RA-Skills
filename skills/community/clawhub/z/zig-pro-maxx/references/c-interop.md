# C interop — @cImport, extern fn, and FFI boundaries

---

## `@cImport` — include a C header

```zig
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("string.h");
    @cDefine("MY_MACRO", "1");
});

pub fn main() void {
    _ = c.printf("hello from C\n");
    const len = c.strlen("hello");
    std.debug.print("len: {d}\n", .{len});
}
```

`@cImport` translates C headers to Zig types at compile time.
All C types and functions are accessible through the returned namespace.

---

## `extern fn` — declare without including a header

When you only need a few C symbols and don't want to pull in a full header:

```zig
extern fn malloc(size: usize) ?*anyopaque;
extern fn free(ptr: ?*anyopaque) void;
extern fn strlen(s: [*:0]const u8) usize;
```

For calling conventions other than the platform default:

```zig
extern "kernel32" fn ExitProcess(exit_code: u32) callconv(.winapi) noreturn;
```

---

## Linking a C library in build.zig

```zig
// In build.zig:
const exe = b.addExecutable(.{
    .name = "myapp",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
exe.linkSystemLibrary("z");        // link libz (zlib)
exe.linkLibC();                    // always needed when using @cImport or extern
b.installArtifact(exe);
```

---

## Type mapping — C to Zig

| C type | Zig type |
|---|---|
| `int` | `c_int` |
| `unsigned int` | `c_uint` |
| `long` | `c_long` |
| `size_t` | `usize` |
| `void *` | `?*anyopaque` |
| `char *` (mutable) | `[*:0]u8` or `[*]u8` |
| `const char *` | `[*:0]const u8` |
| `uint8_t` | `u8` |
| `int32_t` | `i32` |
| `bool` (_Bool) | `bool` |
| struct (by value) | `extern struct { ... }` |
| pointer to struct | `*C_Struct` |
| `NULL` | `null` (optional pointer) |

---

## Passing Zig strings to C

C strings are null-terminated (`[*:0]const u8`). Zig string literals are
already `[:0]const u8`, so they can be coerced:

```zig
const msg: [:0]const u8 = "hello";
_ = c.puts(msg.ptr);               // .ptr gives [*:0]const u8
```

For runtime strings, allocate with sentinel:

```zig
const cstr = try allocator.dupeZ(u8, my_slice);
defer allocator.free(cstr);
_ = c.puts(cstr.ptr);
```

---

## Receiving C strings in Zig

```zig
// C returns: const char *getVersion(void);
extern fn getVersion() [*:0]const u8;

const ver_ptr = getVersion();
const ver: []const u8 = std.mem.span(ver_ptr); // convert to Zig slice
std.debug.print("version: {s}\n", .{ver});
```

`std.mem.span` walks the sentinel to build a slice length.

---

## Callbacks — passing Zig functions to C

```zig
const c = @cImport({ @cInclude("stdlib.h"); });

fn cmp(a: ?*const anyopaque, b: ?*const anyopaque) callconv(.c) c_int {
    const ia: *const c_int = @ptrCast(@alignCast(a));
    const ib: *const c_int = @ptrCast(@alignCast(b));
    return ia.* - ib.*;
}

var arr: [5]c_int = .{ 5, 3, 1, 4, 2 };
c.qsort(&arr, arr.len, @sizeOf(c_int), cmp);
```

Callbacks must use `callconv(.c)` to match C's ABI expectations.

---

## `extern struct` for C structs

```zig
// matches: struct Point { float x; float y; };
const Point = extern struct {
    x: f32,
    y: f32,
};

comptime { std.debug.assert(@sizeOf(Point) == 8); }
```

Use `extern struct` (not `packed struct`) for C interop — C uses its own
alignment rules which `extern struct` replicates.

---

## `@ptrCast` and `@alignCast`

When C gives you `void *` and you know the real type:

```zig
fn handleEvent(userdata: ?*anyopaque) callconv(.c) void {
    const ctx: *MyContext = @ptrCast(@alignCast(userdata));
    ctx.handleEvent();
}
```

`@alignCast` inserts a runtime alignment check in safe modes.
Use it whenever you cast from a pointer with lower or unknown alignment.

---

## Common pitfalls

1. **Forgetting `linkLibC()`** — any `@cImport` or `extern fn` needs
   `exe.linkLibC()` in build.zig or you'll get undefined symbol errors.

2. **Null-terminator confusion** — `[]const u8` has no null terminator;
   `[*:0]const u8` does. Use `allocator.dupeZ` or `std.mem.span` at the
   boundary.

3. **Struct layout mismatch** — use `extern struct`, not a bare `struct`,
   for types shared with C code.

4. **Passing Zig allocator through `void *` userdata** — box the allocator
   in a heap-allocated wrapper struct rather than passing the interface directly.

5. **`callconv(.c)` on callbacks** — without this, the function may use the
   wrong calling convention and corrupt the stack.
