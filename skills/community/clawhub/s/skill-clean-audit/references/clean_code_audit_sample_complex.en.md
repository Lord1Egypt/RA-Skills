# Audit Sample · Complex Scenario (synthetic)

> This sample uses **synthetic** code (not a real project), to demonstrate how to express findings with the "comprehension cost A / change risk B" two axes + red/amber/green when the target contains **classes / inheritance / async / global state / sync-async boundary** issues. Structure mirrors `clean_code_audit_sample.en.md`, but the sample is more complex.

## Code under audit

`demo_service.py` (synthetic illustration; line numbers are checkable and map to no real project):

```python
# demo_service.py
from typing import Dict, Any
import asyncio

_CONFIG: Dict[str, Any] = {}                 # L5  module-level mutable global

class BaseHandler:
    def handle(self, req):                    # L9
        return self._process(req)

    def _process(self, req):                  # L12
        raise NotImplementedError

class OrderHandler(BaseHandler):
    def __init__(self):
        self._cache: Dict[int, Any] = {}      # L17  instance cache, unbounded

    def _process(self, req):                  # L19  too long + deep nesting
        if req:
            if "id" in req:
                if req["id"] > 0:
                    if self._validate(req):
                    # L23
                        if req.get("vip"):
                            self._cache[req["id"]] = req
                            return self._save(req)   # L26  returns coroutine, not awaited
                        else:
                            return self._save(req)   # L28  same issue
                    else:
                        return None
        return None

    def _validate(self, req):                 # L33
        global _CONFIG
        _CONFIG.update(req)                   # L35  side effect: mutates global
        return bool(req.get("id"))

    async def _save(self, req):               # L38
        await asyncio.sleep(0.01)
        return {"ok": True, "id": req["id"]}
```

## Audit Report

**target**: `demo_service.py` (synthetic)　**lang**: en　**mode**: auto→en

### Red · Amber · Green

| Severity | Location | Signal | A comprehension | B change risk | Fix |
|---|---|---|---|---|---|
| 🔴 Red | L5, L33–L35 | module-level mutable global `_CONFIG`, silently `update`d by `_validate` | Med: caller can't see who mutates global | **High**: any handler call quietly rewrites shared state; dangerous for debugging & concurrency | pass config as explicit param / immutable snapshot; if shared state is required, use a read-only singleton and document it |
| 🔴 Red | L26, L28 | `_process` calls async `_save` but **does not `await`** — returns a coroutine, not a result | High: looks like it saved | **High**: never persisted; unawaited coroutine warns/gets dropped | `return await self._save(req)`; make `_process` `async def` too |
| 🟡 Amber | L19–L31 | `_process` 5-level `if` nesting + duplicated branch (`vip` or not both hit `_save`) | Med: branches hard to read at a glance | Med: adding a branch easily breaks indentation | early `return` to flatten; merge the `vip`/non-`vip` paths into one `_save` |
| 🟡 Amber | L17 | `_cache` unbounded dict holding request refs | Low | Med: memory grows with requests; cache key coupled to global state | add TTL / cap, or store only `id` not the whole `req` |
| 🟢 Green | L38–L40 | `async _save` boundary clear (I/O vs pure compute separated) | Low | Low | keep; ensure callers await |

### Cross-segment summary (if file > 500 lines)

This sample is small, so segmentation did not trigger. For a very large file, after scoring each ~500-line segment independently, this line gives one global verdict: this module's **change risk** is clearly higher than its **comprehension cost** — the problems cluster around "implicit global side effects + sync/async boundary misuse", both of which quietly break on edit. Fix the Red items first.

### Intentional debt (if any)

None. All Red/Amber items here lack a "commented + scoped" exemption, so by the method they all count.

---

**Mapping to this skill's method**: this sample deliberately stacks class inheritance + async + global state, to show how axis B (change risk) can flash red *before* axis A (comprehension cost) — deep nesting is readable (A med), but global side effects and the missing `await` are the real edit-time traps (B high). That is also what sets it apart from `clean_code_audit_sample.en.md` (pure functional aggregation).
