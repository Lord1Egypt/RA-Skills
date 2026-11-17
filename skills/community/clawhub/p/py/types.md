# Type Traps

## Identity vs equality
- CPython caches small ints (−5..256) and interns many string literals, so `x is y` on equal values often works by accident. Constant folding can even make `a = 257; b = 257; a is b` True in one file and False across modules — unreliable in BOTH directions. Rule: `is` only for `None`/`True`/`False`/sentinels.
- Sentinel pattern for "missing vs None": `_MISSING = object()` then `if x is _MISSING:` — the only object guaranteed distinct from every user value.
- `bool` subclasses `int`: `True == 1`, so `{1: "a", True: "b"}` has ONE key and `sum(flags)` counts Trues. When validating "is this an int", exclude bools explicitly: `isinstance(x, int) and not isinstance(x, bool)`.
- `id()` is unique only among LIVE objects — the number is reused after collection, so it is never a stable identifier to store.

## Floats and rounding
- Floats are IEEE-754 doubles: ~15-17 significant decimal digits; `0.1 + 0.2 == 0.30000000000000004`. Compare with `math.isclose(a, b)` (default `rel_tol=1e-09`); never `==` on computed floats.
- `round()` is banker's rounding (half to even): `round(0.5) == 0`, `round(1.5) == 2`, `round(2.5) == 2`. Invoices expecting half-up need `decimal` with `ROUND_HALF_UP`.
- `Decimal('0.1')` is exact; `Decimal(0.1)` is `0.1000000000000000055511151231257827...` — constructing from float imports the error. Same for `Fraction`.
- `float('nan') != float('nan')`, yet `nan in [nan]` is True — containers check identity before equality. NaN in data silently breaks sorting and deduplication; filter with `math.isnan` first.
- `sum()` over many floats accumulates error; `math.fsum` is exact to the last bit. For money it is `Decimal` either way (SKILL.md rule 7).

## Integer arithmetic
- `//` floors toward negative infinity and `%` takes the SIGN OF THE DIVISOR: `-7 // 2 == -4`, `-7 % 3 == 2`. C, Java, and JavaScript give `-3` and `-1`, so ported algorithms change behavior on negative inputs without any error.
- `int(-3.5)` truncates toward zero (`-3`) while `-7 // 2` floors (`-4`). Mixing both in one calculation is a classic off-by-one; `math.floor`/`math.ceil` return ints and state which you meant.
- `divmod(a, b)` returns quotient and remainder in one call, consistent with `//` and `%`.
- Integers never overflow, so the failure mode is slowness, not wrapping: multiplication of very large ints is superlinear, and conversion to text is capped (below).

## Truthiness
- Falsy: `False`, `None`, `0`, `0.0`, `Decimal("0")`, `""`, `[]`, `{}`, `set()`, and any object whose `__len__` returns 0. Everything else is truthy.
- `if x:` and `if x is not None:` answer different questions. Where `0`, `""`, or an empty list are legitimate values, the first takes the wrong branch — the same bug as `xs = xs or []` (SKILL.md rule 1).
- numpy arrays and pandas objects RAISE on truthiness ("truth value of an array is ambiguous"): a guard that works for lists breaks on arrays.

## Strings and bytes
- `"filename.txt".strip(".txt")` strips a CHARACTER SET, not a suffix — returns `"filename"` sometimes, `"filenam"` for `"format.txt"`. Use `removesuffix`/`removeprefix` (`python >=3.9`).
- Building strings with `+=` in a loop is O(n²); accumulate in a list and `''.join(parts)`.
- `"a b  c".split()` collapses whitespace runs and drops leading/trailing empties; `"a b  c".split(" ")` yields an empty string per extra space. Two behaviors, one name.
- Case-insensitive comparison is `casefold()`, not `lower()` (German `"ß".casefold() == "ss"`). Text from two different systems also needs Unicode normalization before comparison (`files.md`).
- `startswith`/`endswith` accept a TUPLE: `name.endswith((".yml", ".yaml"))` instead of an `or` chain.
- `bytes` and `str` never compare equal (`b"a" == "a"` is False) and never implicitly convert. Indexing bytes gives an int (`b"abc"[0] == 97`); slicing gives bytes. Encode and decode once, at the boundary (`files.md`).
- `f"{value=}"` (`python >=3.8`) prints the expression and its value — the fastest debug print available. f-strings do NOT belong in logging calls (`logging.md`) or in SQL and shell strings (`security.md`).

## Immutability edge cases
- `t = (1, [2]); t[1] += [3]` both mutates the inner list AND raises `TypeError`: the in-place add succeeds, then the tuple assignment fails. The data changed and the traceback says it did not.
- A tuple containing a list is unhashable — and you only find out at the moment you use it as a dict key or put it in a set.

## Hints and limits
- Type hints never enforce at runtime: `def f(x: int)` happily takes a string. Enforcement needs a checker in CI or runtime validation at the boundary (`type-checking.md`, `data-modeling.md`).
- `Any` vs `object`: `Any` silences the checker transitively (errors vanish downstream); `object` forces explicit narrowing before use. For "accepts anything, must be checked", annotate `object`.
- `Optional[X]` means `X | None` — nothing to do with the argument having a default. An arg can be optional without Optional, and required-but-nullable with it.
- `int` is arbitrary precision, but int↔str conversion beyond 4300 digits raises `ValueError` since `python >=3.11` (DoS fix, CVE-2020-10735); raise the limit with `sys.set_int_max_str_digits()` if you legitimately parse huge numbers.
- Chained comparisons bind as `and`: `a < b < c` is `(a < b) and (b < c)`. This also means `x == y in zs` chains — parenthesize anything mixing operators.
- Sorting mixed types raises `TypeError: '<' not supported between instances of 'NoneType' and 'int'`. A column with nulls needs a key that handles them: `key=lambda x: (x is None, x)`.
