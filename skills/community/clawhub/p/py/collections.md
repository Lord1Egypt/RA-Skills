# Collection Traps

## Aliasing and copies
- `[[]] * 3` creates 3 references to the SAME list — `m[0].append(1)` changes all rows. Build with `[[] for _ in range(3)]`.
- `dict.fromkeys(keys, [])` has the identical bug: every key shares ONE list. Build with `{k: [] for k in keys}`.
- `a[:]`, `list(a)`, `dict(d)`, `.copy()` are all SHALLOW — nested objects stay shared. Nested structures need `copy.deepcopy`, but it is slow and follows every reference; for a known shape like dict-of-lists, `{k: v[:] for k, v in d.items()}` is the fast targeted copy.
- Mutating a dict key object after insertion (possible with custom `__hash__` on mutable state) makes the entry unfindable — lookup hashes the new state, the bucket holds the old. Keys must be effectively immutable.
- A function that mutates a list it was passed changes the caller's data. Either say so in the name and docstring, or copy on entry — silent argument mutation is the hardest class of bug to locate later (`debugging.md`).

## Ordering
- Dict preserves insertion order (guaranteed since `python >=3.7`). Sets do NOT, and str hashing is salted per process (`PYTHONHASHSEED`) — set iteration order changes between runs. Never serialize set iteration order into golden files; `sorted()` first.
- `list.sort`/`sorted` are stable: for multi-key mixed-direction sorts, sort by the secondary key first, then the primary — or negate numeric keys in a single tuple key.
- `itertools.groupby` groups only CONSECUTIVE equal keys — on unsorted input it silently yields fragmented groups. Sort by the same key first, or use a dict accumulator.
- `Counter.most_common()` breaks ties by insertion order: stable within a run, meaningless across runs whose input arrived in a different order. Sort explicitly when ties matter.
- In-place methods return None: `xs = xs.sort()` sets `xs` to None, and so do `append`, `extend`, `update`, and `reverse`. This is where a large share of `AttributeError: 'NoneType' object has no attribute` comes from (`debugging.md`).

## Lookup and mutation
- `d[k]` on a `defaultdict` INSERTS the key — logging `d[k]` or checking `if d[k]:` pollutes the dict. Membership tests must use `k in d`.
- `d.setdefault(k, expensive())` evaluates the default on every call, hit or miss. If the default is costly, use `defaultdict` or an explicit `in` check.
- `d.get(k)` returning None is ambiguous when None is a legal value — use a sentinel: `_MISSING = object()`, then `d.get(k, _MISSING) is _MISSING` distinguishes missing from None.
- `k in d` tests KEYS. `v in d.values()` is a full O(n) scan; needing it usually means you want a second dict indexed the other way.
- Mutating while iterating: dicts raise `RuntimeError: dictionary changed size`, lists silently skip (removing index i shifts i+1 into i, loop moves to i+1). Iterate `list(xs)` or build a new collection.
- `.keys()`, `.values()`, `.items()` are LIVE views, not snapshots: they see later changes and cannot be indexed. `list(d.items())` when you need a frozen copy or positional access.
- Slices never raise: `xs[10:20]` on a 3-element list returns `[]` — off-by-one bugs surface as empty results downstream, not as IndexError at the fault.
- `list.remove(x)` removes the FIRST match and raises `ValueError` when absent; `del xs[i]` and `xs.pop(i)` work by index. Removing by value while looping over the same list is both bugs at once.

## Comprehensions
- The loop variable does not leak out (unlike Python 2), but the FIRST iterable is evaluated in the ENCLOSING scope — which is why a comprehension in a class body cannot see other class attributes and raises `NameError`. Use a plain loop in class bodies.
- Clause order matches the equivalent nested loops read left to right: `[y for row in m for y in row]` flattens; swapping the clauses is a `NameError`.
- A generator expression is lazy and single-use: `sum(x*x for x in xs)` never builds a list, and a generator stored in a variable is exhausted after one pass (`functions.md`).
- `dict(pairs)` and `{k: v for k, v in pairs}` both keep the LAST value for a duplicated key, silently. If duplicates are an error, count them first.

## Sets
- Elements must be hashable: a set of lists raises `TypeError`, a set of tuples is fine, a `frozenset` can itself be a dict key.
- `set.discard(x)` never raises, `set.remove(x)` raises `KeyError` — pick the one that states your assumption.
- Set algebra replaces nested loops: `a & b`, `a | b`, `a - b`, `a ^ b`. "What changed between these two collections" is two differences, not an O(n²) comparison.
- Order-preserving deduplication is `list(dict.fromkeys(xs))`, not `set(xs)`.

## Cost
- `x in list` is O(n). If you test membership against the same collection more than once, build a `set` once — the O(n) build amortizes immediately and each lookup drops to O(1).
- `list.pop(0)` and `list.insert(0, x)` are O(n) because every element shifts; `collections.deque` is O(1) at both ends (`stdlib.md`).
- Top-k from n items when k << n: `heapq.nlargest(k, xs)` is O(n log k) vs full sort O(n log n) — matters from thousands of items up.
- `zip` silently truncates to the shortest input — misaligned data disappears instead of erroring. Pass `strict=True` (`python >=3.10`) whenever inputs must be equal length.
- A list of a million small objects costs far more than the objects themselves (a pointer per slot plus over-allocation); `array.array` or numpy is an order of magnitude smaller for homogeneous numbers (`performance.md`).
