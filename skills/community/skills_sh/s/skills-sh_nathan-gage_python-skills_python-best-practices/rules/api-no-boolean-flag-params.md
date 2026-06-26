---
title: Avoid Boolean Flag Parameters in Public APIs
impact: MEDIUM
impactDescription: prevents call sites that read like "do_thing(thing, True, False)"
tags: api, parameters, booleans, literal, enum
references: https://docs.python.org/3/library/typing.html#typing.Literal, https://docs.python.org/3/library/enum.html
---

## Avoid Boolean Flag Parameters in Public APIs

A boolean parameter is a binary mode switch hiding behind a generic type. `download(url, True, False, True)` is unreadable, the body branches on the flag with near-duplicate paths, and adding a third mode later breaks the API. The function-level cousin of `data-explicit-variants`: when behavior meaningfully changes on a flag, prefer split functions or a `Literal`/`Enum` parameter.

**Incorrect (boolean flags — call sites lose meaning):**

```python
def export_report(rows: list[Row], to_csv: bool = True, compress: bool = False) -> bytes:
    data = render_csv(rows) if to_csv else render_json(rows)
    return gzip.compress(data) if compress else data

export_report(rows, False, True)   # JSON, compressed? CSV, compressed? Reader can't tell.
```

**Correct (`Literal` parameter when the modes share most of the body):**

```python
from typing import Literal

Format = Literal["csv", "json", "parquet"]

def export_report(rows: list[Row], format: Format, *, compress: bool = False) -> bytes:
    match format:
        case "csv":     data = render_csv(rows)
        case "json":    data = render_json(rows)
        case "parquet": data = render_parquet(rows)
    return gzip.compress(data) if compress else data

export_report(rows, format="csv", compress=True)
```

Adding a fourth format is a one-line change to the `Literal`; call sites read meaningfully. Use an `Enum` when modes carry behavior or constants (e.g. `CompressionLevel.BEST` with value `9`). Split into separate functions when bodies barely overlap and composition is orthogonal.

A single keyword-only `bool` is still fine when the name clearly answers "what does `True` mean?" (`include_archived=True`, `strict=True`, `dry_run=True`) and the body is a small filter rather than two near-duplicate paths. Read call sites out loud: `export_report(rows, True, False)` fails; `export_report(rows, format="csv", compress=True)` passes.
