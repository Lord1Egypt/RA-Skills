---
title: No Duplicate Imports
impact: LOW
impactDescription: prevents confusion and redundant work
tags: imports, duplicates, cleanup
references: https://docs.astral.sh/ruff/rules/duplicate-bindings/
---

## No Duplicate Imports

Two imports of the same name are either redundant (if they're identical) or a sign that a refactor left both in place. Either way, delete one. Tools flag this, but agents sometimes add a new import on top of an existing one without checking.

**Incorrect (same name imported twice):**

```python
import json
from typing import Any
from pathlib import Path

# ... later in the file, after a later edit ...
from pathlib import Path       # duplicate
from pathlib import Path as P  # different alias, same underlying import
```

The first duplicate is pure redundancy. The second is worse — now `Path` and `P` both exist in the namespace, pointing to the same class.

**Correct (one import per name):**

```python
import json
from typing import Any
from pathlib import Path
```

If two aliases are genuinely needed (very rare — usually a code-smell), pick one:

```python
from pathlib import Path  # use this name everywhere
```

**When "duplicates" are actually distinct:**

```python
from foo import bar
from foo.baz import bar as baz_bar  # different bar, aliased to avoid collision
```

These are different objects with the same name in different namespaces. Aliasing one disambiguates. This is fine — but it's *not* a duplicate; the names differ.

**Detection:**

- `ruff check --select F811` flags redefinitions
- `pyflakes` also catches these

Add to pre-commit or CI.

**Root cause:** duplicate imports usually appear after:

- Merging branches that both added the same import
- An IDE auto-import on top of an existing import
- Refactoring that copied a block without cleaning up the imports

Reviewing the imports block after any merge or mass edit catches these before they land.
