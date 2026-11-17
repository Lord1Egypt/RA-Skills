# Clean Code Audit Sample · aggregate.py → `main()` (synthetic example)

> Target: `main()` of `demo-skill/scripts/aggregate.py` (lines 15–55 below, ~41 lines)
> Criteria: A. Comprehension cost / B. Change risk. Red = dirty on sight, fix first; Amber = intentional debt (comment + scoped); Green = clean on sight.
> Note: this sample is a **synthetic example script**, maps to no real project; line numbers start at 1, audit evidence can be checked directly.

## Audited snippet (`demo-skill/scripts/aggregate.py`)

```python
 1 │ """Daily usage report aggregator.
 2 │ Builds the daily usage report and writes a summary JSON.
 3 │ """
 4 │ from config import *                      # implicit import: symbol origin unknown
 5 │ import sqlite3, requests
 6 │
 7 │ DB_PATH = "data/usage.db"                 # module-level global
 8 │ TZ = "Asia/Shanghai"
 9 │ _PRICING = {}                             # module-level [mutable] global
10 │
11 │ """Daily usage report aggregator.
12 │ This module collects token usage and emits a per-source summary.
13 │ (legacy header kept for compatibility)"""   # duplicates / contradicts the top docstring
14 │
15 │ def main(argv=None):
16 │     args = _parse_args(argv)
17 │     # T-12: fall back to empty db when missing
18 │     # F-3: skip pricing meta if unavailable
19 │     # T-18: reorder sources after incident review
20 │     rows = _fetch_rows(args.start, args.end, DB_PATH, gap_min=15)  # magic number 15
21 │     if not rows:
22 │         print("[WARN] no rows in range")   # hidden side effect (print)
23 │         rows = []
24 │     if args.source == "claude":            # switch-on-type
25 │         try:
26 │             raw = _query(rows, "claude")
27 │         except (sqlite3.Error, OSError):    # precise except
28 │             raw = []
29 │         sid_map = _build_sid_map(rows, "claude")
30 │         total = 0
31 │         for r in raw:                       # duplicates the codex branch
32 │             total += r["tokens"]
33 │         usage = {"source": "claude", "total": total, "rows": len(raw)}
34 │         _write_outputs(usage, "claude")
35 │     elif args.source == "codex":           # nearly line-by-line identical to claude branch
36 │         try:
37 │             raw = _query(rows, "codex")
38 │         except (sqlite3.Error, OSError):
39 │             raw = []
40 │         sid_map = _build_sid_map(rows, "codex")
41 │         total = 0
42 │         for r in raw:                       # duplicated logic (DRY violation)
43 │             total += r["tokens"]
44 │         usage = {"source": "codex", "total": total, "rows": len(raw)}
45 │         _write_outputs(usage, "codex")
46 │     summary = {
47 │         "generated_at": _now(TZ),
48 │         "period": f"{args.start}..{args.end}",
49 │         "source": usage["source"],
50 │         "total_tokens": usage["total"],
51 │         "row_count": usage["rows"],
52 │     }
53 │     _attach_pricing(summary, _PRICING)      # mutates module-level mutable global
54 │     print(f"report ready: {len(summary)}")  # main looks like a query but secretly prints
55 │     return summary
```

## A. Comprehension cost

| # | Checklist item | Hit | Evidence (line) | Note |
|---|--------|------|-----------|------|
| A1 | 🔴 Implicit symbol origin (`import *`) | ✅ Red | 4 + call sites 7/8/9/20/46/53 | `DB_PATH`/`TZ`/`_PRICING`/`_now`/`_query`/`_fetch_rows` all come from `from config import *`. Seeing a call, you can't tell which file defines it — needs a global search. |
| A2 | 🔴 Same explanation duplicated and contradictory | ✅ Red | 1–3 vs 11–13 | The top docstring is duplicated by the bare string literal at line 11; the latter is a dead string (discarded at runtime), and "legacy header kept" hints it's meaningless yet undeleted. |
| A3 | 🔴 Comments read like a changelog (issue IDs everywhere) | ✅ Red | 17/18/19 | `T-12`/`F-3`/`T-18` issue-tracker labels scattered inside `main`. A new reader must mentally decode this internal numbering scheme before understanding "who owns this code now". |
| A4 | 🟡 Long function >40 lines but cohesive, hard to split | ✅ Amber | 15–55 (~41 lines) | Truly long. But the "hard to split" defense is weak: it is essentially sequential orchestration (parse args → collect by source → aggregate → attach pricing meta → output), splittable into `parse_args`/`collect_by_source`/`build_summary`/`attach_pricing`/`write_output`. Amber = temporarily acceptable, but schedule the split. |
| A5 | 🟡 Unnamed magic number / string | ✅ Amber | 20/24/35 (`"claude"`/`"codex"`), 20 (`gap_min=15`) | Cost-scope strings `"claude"`/`"codex"` appear in 2 places; `gap_min=15` in default + call = 2 places. Name constants (`SOURCE_CLAUDE`, etc., `GAP_MIN_DEFAULT`) to eliminate. |
| A6 | 🟢 Naming is documentation | ✅ Green (mostly) | `_parse_args`(16)/`_build_sid_map`(29)/`raw`(26)/`total`(30) | Most local names reveal intent at a glance; this item is met. |
| A7 | 🟢 Explicit beats implicit | ❌ Not met | see A1/B1 | Behavior mixes in imported module-level globals (`DB_PATH`/`TZ`/`_PRICING`…); preconditions and boundaries unclear, so this is not green. |

## B. Change risk

| # | Checklist item | Hit | Evidence (line) | Note |
|---|--------|------|-----------|------|
| B1 | 🔴 Module-level mutable global controls behavior | ✅ Red | 9 + 53 | `main` reads and mutates the module global `_PRICING` poured in by `import *` (`_attach_pricing(summary, _PRICING)`). Set at import time by config, not mutated at runtime, so one notch lower risk than runtime mutation — but by the checklist definition still "depends on non-local state"; marked red. |
| B2 | 🔴 Duplicated logic (DRY violation) | ✅ Red | 24–34 vs 35–45 | The `claude` and `codex` branches are nearly line-by-line identical (collect → build sid_map → accumulate tokens → write output), differing only in adapter name and print label. ~20 lines duplicated; fix one place must sync two. |
| B3 | 🔴 Bare `except` swallows errors silently | ⬜ Not hit (good) | 25–28/37–39 | Every `except` is precise: `(sqlite3.Error, OSError)`(27)(38). No bare `except`. Item met. |
| B4 | 🟡 Intentional best-effort `except` | ✅ Amber | 25–28/37–39 (single-source fetch fails → fall back `raw = []`) | A single-source query failure only falls back to an empty list without breaking the whole pipeline. Already precise except + scoped, so "temporarily acceptable debt". |
| B5 | 🟡 Premature abstraction of an unused interface | ⬜ Not hit | — | Splitting `_parse_args`/`_build_sid_map` is deliberate refactoring, not premature abstraction; not counted. |
| B6 | 🟢 Behavior depends only on inputs | ⚠️ Partially met | parsed from `argv`(16) | A CLI tool necessarily reads argv, but mixes in imported globals (see B1), so not pure input-driven; only partially met, not full green. |
| B7 | 🟢 Test coverage | ❓ Unverified | — | Not confirmed in this audit; left blank. |

## Extra findings (outside the checklist, still comprehension cost)

**The `if args.source == "claude": ... elif args.source == "codex":` at line 24 is switch-on-type:** every new data source forces copying a whole branch inside `main` (see B2), and needs syncing in 2 places. Equivalent to Uncle Bob smell **Rigidity/Fragility** — a small change (add a source) is forced to touch many places. Extract a `COLLECTORS = {"claude": collect_claude, "codex": collect_codex}` registry; adding a source then touches only one place.

## Audit score

- 🔴 Red (must fix): **5** — A1 import* / A2 duplicate docstring / A3 changelog comments / B1 global state / B2 DRY duplicate branch
- 🟡 Amber (controlled debt): **3** — A4 long function / A5 magic values / B4 best-effort except
- 🟢 Green (already met): **1** (A6 naming) + B3 bare except not hit (good)
- Unverified / not hit: A7, B5, B6, B7

## Conclusion (by first principles)

`main()`'s "dirt" concentrates on the **comprehension cost** side: implicit origin (A1), self-contradictory docs (A2), comments degraded into an issue tracker (A3), over-long function (A4).
The **change risk** side is actually restrained — no bare except (B3 good), duplication only across the claude/codex branches (B2), global dependency is import-time not runtime mutation (B1).
Priority suggestion: clear A1/A2/A3 first (near-zero behavior risk, pure readability), then schedule B2 to merge the two branches and A4 to split the function; amber items like A5/B4 can be handled along the way when you naturally touch the code.

> This sample is read-only, not modified. To apply fixes, open a separate pass following the priority above, one PR at a time.
