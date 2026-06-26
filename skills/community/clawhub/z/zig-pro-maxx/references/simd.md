# SIMD — @Vector and std.simd

SIMD (Single Instruction, Multiple Data) lets a single CPU instruction
operate on multiple values simultaneously. Zig exposes this via the
`@Vector` builtin and helpers in `std.simd`.

---

## The `@Vector` type

```zig
// @Vector(length, element_type)
const V4f32 = @Vector(4, f32);
const V8u8  = @Vector(8, u8);
```

Length must be a comptime-known power of two (hardware may emulate other sizes).

---

## Creating vectors

```zig
// Literal (scalar broadcast):
const zeros: @Vector(4, f32) = @splat(0.0);
const ones:  @Vector(4, i32) = @splat(1);

// From an array:
const arr: [4]f32 = .{ 1.0, 2.0, 3.0, 4.0 };
const v: @Vector(4, f32) = arr;   // implicit coercion

// Back to array:
const out: [4]f32 = v;
```

---

## Arithmetic — element-wise

All standard operators work element-wise on `@Vector`:

```zig
const a: @Vector(4, f32) = .{ 1, 2, 3, 4 };
const b: @Vector(4, f32) = .{ 5, 6, 7, 8 };

const sum  = a + b;   // .{ 6, 8, 10, 12 }
const diff = a - b;
const prod = a * b;
const quot = b / a;
```

---

## Reduction with `@reduce`

Collapse a vector to a scalar:

```zig
const v: @Vector(4, i32) = .{ 1, 2, 3, 4 };

const total = @reduce(.Add, v);   // 10
const min   = @reduce(.Min, v);   // 1
const max   = @reduce(.Max, v);   // 4
const all   = @reduce(.And, @Vector(4, bool){ true, true, false, true }); // false
const any   = @reduce(.Or,  @Vector(4, bool){ false, false, true, false }); // true
```

Available ops: `.Add`, `.Mul`, `.Min`, `.Max`, `.And`, `.Or`, `.Xor`.

---

## Comparisons — element-wise, returns `@Vector(N, bool)`

```zig
const a: @Vector(4, i32) = .{ 1, 2, 3, 4 };
const b: @Vector(4, i32) = .{ 2, 2, 2, 2 };

const lt: @Vector(4, bool) = a < b;   // .{ true, false, false, false }
const eq: @Vector(4, bool) = a == b;  // .{ false, true, false, false }
```

---

## Shuffle and permutation

```zig
const v: @Vector(4, u8) = .{ 10, 20, 30, 40 };
// Reverse the vector:
const r = @shuffle(u8, v, undefined, [4]i32{ 3, 2, 1, 0 });
// r == .{ 40, 30, 20, 10 }
```

---

## Auto-detect optimal vector length

```zig
const std = @import("std");

// Let std pick the best SIMD width for f32 on this CPU:
const vec_len: comptime_int = std.simd.suggestVectorLength(f32) orelse 4;
const V = @Vector(vec_len, f32);
```

`suggestVectorLength` returns `null` for targets without SIMD — the `orelse 4`
fallback keeps the code correct on any target.

---

## Processing a slice with SIMD

```zig
fn sumSlice(data: []const f32) f32 {
    const vec_len = std.simd.suggestVectorLength(f32) orelse 4;
    const V = @Vector(vec_len, f32);

    var acc: V = @splat(0.0);
    var i: usize = 0;

    // Vector loop — processes `vec_len` elements per iteration
    while (i + vec_len <= data.len) : (i += vec_len) {
        const chunk: V = data[i..][0..vec_len].*;
        acc += chunk;
    }

    // Scalar tail — handles remaining elements
    var tail: f32 = @reduce(.Add, acc);
    while (i < data.len) : (i += 1) tail += data[i];

    return tail;
}
```

---

## std.simd helper functions

All take `@Vector` arguments and return `@Vector` or scalar results.

| Function | What it does |
|---|---|
| `std.simd.suggestVectorLength(T)` | Best vector length for T on this CPU |
| `std.simd.repeat(len, vec)` | Extend vec to length len by repeating |
| `std.simd.join(a, b)` | Concatenate two vectors |
| `std.simd.extract(v, first, last)` | Sub-slice of a vector |
| `std.simd.reverseOrder(v)` | Reverse element order |
| `std.simd.shiftElementsLeft(v, n, fill)` | Shift left, fill right |
| `std.simd.shiftElementsRight(v, n, fill)` | Shift right, fill left |
| `std.simd.prefixScan(.Add, 1, v)` | Prefix sum |
| `std.simd.firstTrue(v)` | Index of first `true` in bool vector |
| `std.simd.countTrues(v)` | Count `true` elements |

---

## Alignment for SIMD loads

SIMD loads are fastest when the pointer is aligned to the vector width.
Use `std.mem.Alignment` or over-align your allocations:

```zig
const VEC_ALIGN = @alignOf(@Vector(vec_len, f32));
const buf = try allocator.alignedAlloc(f32, VEC_ALIGN, n);
defer allocator.free(buf);
```

---

## Pitfalls

- Vector length must be comptime-known and > 0.
- `@shuffle` mask indices use negative values to select from the second vector.
- Overflow in integer vectors wraps in ReleaseFast; use `+%` if intentional.
- Not all operations map to a single SIMD instruction on every architecture;
  LLVM will emit scalar fallback code where needed.
