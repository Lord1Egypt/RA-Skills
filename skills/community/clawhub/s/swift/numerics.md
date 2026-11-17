# Numerics — Overflow, Conversion, Floating Point, Money

Swift does not wrap on integer overflow and does not return NaN for a bad conversion: it traps. Arithmetic is therefore a crash surface, not just a correctness surface, and the fix is almost always "pick the operator that says what you meant" rather than "make the type wider".

## Integer Overflow Traps

- `+`, `-`, `*`, `<<` on a result outside the type's range trap at runtime: "Fatal error: Arithmetic operation … resulted in an overflow". Release builds trap too — this is a language guarantee, not a debug check. `-Ounchecked` removes it and turns the trap into undefined behavior; never ship it to silence one.
- `&+`, `&-`, `&*` wrap two's-complement, `&<<`/`&>>` mask the shift amount. Legal only where wrapping is the intent: hashes, checksums, PRNGs, ring buffers, C-compatible counters. Reaching for `&+` to stop a crash converts a loud bug into a silent one.
- Recoverable arithmetic uses the reporting forms: `let (v, overflowed) = a.multipliedReportingOverflow(by: b)`; also `addingReportingOverflow`, `subtractingReportingOverflow`, `dividedReportingOverflow(by:)`. Widening instead: `a.multipliedFullWidth(by: b)` gives `(high, low)` with no loss.
- `abs(Int.min)` traps — the positive counterpart does not exist. Use `Int.min.magnitude` (a `UInt`) when you need the value.
- `(a + b) / 2` overflows on large operands. Midpoint without overflow: `a + (b - a) / 2` for `a <= b`.
- Accumulators inherit the element type: summing 10 000 `Int32` samples in an `Int32` overflows around 2.1e9. Widen the accumulator explicitly (`values.reduce(Int64(0)) { $0 + Int64($1) }`), not the storage.
- `UInt` subtraction underflows into astronomic numbers before it traps on the next operation. Any expression of the form `unsignedCount - 1` needs a guard, or should be `Int` in the first place.

## Division and Remainder

| Expression | Result |
|---|---|
| `7 / 2` | `3` — integer division truncates toward zero |
| `-7 / 2` | `-3`, not `-4`. Swift truncates; Python floors |
| `-7 % 2` | `-1`. The remainder takes the **dividend's** sign |
| `x % 2 == 1` for negative `x` | `false` — use `x.isMultiple(of: 2)` |
| `x / 0`, `x % 0` (integers) | Trap: "Fatal error: Division by zero" |
| `Int.min / -1` | Trap: the quotient is one past `Int.max` |
| `1.0 / 0.0` | `.infinity` — floating point does not trap |

- Floor division for negatives: `let q = Int((Double(a) / Double(b)).rounded(.down))` loses exactness above 2^53; do it in integers instead — `var q = a / b; if (a % b != 0) && ((a < 0) != (b < 0)) { q -= 1 }`.
- Guard the divisor at the boundary where it enters, not at the division: a zero divisor is almost always a validation failure upstream.

## Conversions That Trap, and Their Safe Forms

| Intent | Call | On failure |
|---|---|---|
| Must fit exactly, caller decides | `Int(exactly: x)` | Returns `nil` (also nil for `3.5` → `Int`) |
| Saturate at the bounds | `Int8(clamping: 300)` | Yields `127` |
| Reinterpret the bit pattern | `UInt8(truncatingIfNeeded: -1)` | Yields `255` |
| The value is provably in range | `Int(x)` | Traps |

- `Int(someDouble)` truncates toward zero (`Int(3.9) == 3`, `Int(-3.9) == -3`) and traps on NaN, on ±infinity, and on anything outside `Int.min...Int.max`: "Double value cannot be converted to Int because it is outside the representable range". `Int(exactly:)` is the only form safe on untrusted floats.
- `UInt(negativeInt)` traps with "Negative value is not representable". This is the standard crash when a signed count, index, or difference is handed to a C or unsigned API.
- Avoid `numericCast`: it hides which of the four behaviors above you got, and it traps. Spell the conversion out.
- `Int` is pointer-sized. Never persist or transmit `Int` in a binary format — use `Int64`/`UInt32` with an explicit endianness (`bigEndian`, `init(bigEndian:)`).

## Floating Point

- `Double` holds 53 significand bits: every integer up to 2^53 (9 007 199 254 740 992) is exact, above it they are not. `Float` gives out at 2^24 (16 777 216) — enough to break IDs and timestamps stored as `Float`.
- `0.1 + 0.2 != 0.3`. Never compare floats with `==` unless comparing against a value you produced by the identical computation. Compare with a tolerance scaled to the magnitude: `abs(a - b) <= max(abs(a), abs(b)) * .ulpOfOne * 4`, or an absolute epsilon when the values are known to be near zero.
- NaN is not equal to itself. Consequences that bite: `array.contains(.nan)` is always `false`; a `Set<Double>` can hold several NaNs; and sorting data containing NaN violates strict weak ordering and traps (SKILL.md Crash Messages). Filter with `isFinite` before sorting, comparing, or reducing (`collections.md`).
- `x.isNaN`, `x.isFinite`, `x.isSignalingNaN` are the tests; `x != x` is the old C idiom and reads as a bug.
- `rounded()` defaults to `.toNearestOrAwayFromZero`. IEEE and most financial rules want `.toNearestOrEven` (banker's rounding): `x.rounded(.toNearestOrEven)`. Also available: `.up`, `.down`, `.towardZero`, `.awayFromZero`.
- `stride(from: 0.0, to: 1.0, by: 0.1)` accumulates error and may or may not include the last step. Stride over integers and divide: `(0..<10).map { Double($0) / 10 }`.
- Summing many floats loses low bits in magnitude order. Sort by magnitude, or use pairwise/Kahan summation, when the sum spans several orders of magnitude.
- `Float80` is x86-only; it does not exist on arm64. Do not put it in cross-platform code.

## Money and Decimals

- Money is never a `Double`. Two representations are correct: **integer minor units** (`let cents: Int`) for a single currency with a fixed exponent, or `Decimal` (base-10, Foundation, available on Linux) when you need fractional rates, tax, or currency-agnostic math.
- Construct `Decimal` from a string or from integer parts — `Decimal(string: "0.1")!`, `Decimal(sign: .plus, exponent: -2, significand: 10)`. `Decimal(0.1)` and the float-literal path go through a `Double` first and inherit its binary error, which defeats the point of using `Decimal`.
- Round once, at the point of settlement, with the rule the domain specifies (`NSDecimalRound` with an explicit `NSDecimalNumber.RoundingMode`). Rounding intermediate results compounds; rounding at display time only, while storing full precision, is what makes an invoice total disagree with the sum of its lines.
- Split a total by rounding each share down and distributing the remainder in minor units: three ways on 100 cents is 34/33/33, never 33.33 three times.
- On the wire, money is an integer of minor units or a string. JSON has no decimal type and a JSON number round-trips through `Double` at both ends.

## Numeric Literals and Types

- Untyped integer literals default to `Int`, float literals to `Double`. A literal too large for its annotated type is a compile error, not a trap.
- Underscores group digits (`1_000_000`); `0b`, `0o`, `0x` prefixes and hex float literals (`0x1p-2`) are supported.
- Mixed-type arithmetic never converts implicitly: `Int + Double` does not compile, and long mixed expressions are a top cause of "unable to type-check this expression in reasonable time" (SKILL.md rule 8). Annotate one intermediate `let`.
- Generic numeric code constrains on `BinaryInteger`, `FixedWidthInteger` (bounds, overflow reporting, bit ops), or `FloatingPoint`/`BinaryFloatingPoint` — not on `Numeric`, which lacks division.
- `Int.random(in:)` traps on an empty range; check the bounds before calling. `SystemRandomNumberGenerator` is cryptographically secure on Apple platforms and Linux; a seeded generator for tests must be an explicit `RandomNumberGenerator` you pass in.
