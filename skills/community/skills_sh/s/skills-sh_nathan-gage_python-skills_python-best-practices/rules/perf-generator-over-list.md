---
title: Stream with Generators When Memory or First-Result Latency Matters
impact: LOW-MEDIUM
impactDescription: bounded memory and lazy evaluation for large or infinite sequences
tags: perf, generators, memory, streaming
references: https://docs.python.org/3/glossary.html#term-generator, https://docs.python.org/3/library/itertools.html
---

## Stream with Generators When Memory or First-Result Latency Matters

Generators trade materialization for laziness: one value at a time, no intermediate list, caller can stop early. This is a memory and streaming rule, not "generators are categorically better." When you need every result, re-iterate, want random access, or will sort anyway, a list comprehension is often clearer and sometimes faster.

**Incorrect (materializes a multi-GB file three times for a count):**

```python
def count_errors(path: Path) -> int:
    lines = path.read_text().splitlines()                    # full file in memory
    parsed = [parse_line(line) for line in lines]            # second full copy
    matching = [p for p in parsed if p.level == "ERROR"]     # third full copy
    return len(matching)
```

**Correct (streaming — constant memory regardless of file size):**

```python
def count_errors(path: Path) -> int:
    with path.open() as f:
        return sum(1 for line in f if parse_line(line).level == "ERROR")
```

Reach for a generator when the input is large, unbounded, or the consumer can stop early (`any()`, `next()`, `break`). Reach for a list when you need `len()`, iterate more than once, need random access, or will sort the whole sequence. A generator exhausted by the first loop reading zero on the second is a real bug, not a perf issue. `itertools` (`chain`, `islice`, `takewhile`, `groupby`) yields lazily for pipelines that stay streaming.
