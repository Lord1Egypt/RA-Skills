---
title: Remove Unused Imports
impact: LOW
impactDescription: prevents accidental dependencies and reduces noise
tags: imports, dead-code, cleanup
references: https://docs.astral.sh/ruff/rules/unused-import/
---

## Remove Unused Imports

Every import is a declaration of "this module depends on X." Unused imports lie about dependencies, add reading noise, risk circular imports, and mask refactoring errors — the import survives long after the only call site was deleted.

**Incorrect (imports for names that aren't used):**

```python
import json
import re
from typing import Any, Optional, Union

from .helpers import validate, format_date  # format_date never used

def compact(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"))
```

**Correct (just what's needed):**

```python
import json
from typing import Any

def compact(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"))
```

`ruff check --select F401` flags unused imports — wire it into pre-commit or CI. If a module intentionally re-exports names (common in `__init__.py`), use the `from .client import Client as Client` form or list them in `__all__`; both signal "intentional, not forgotten." If an import is used only in annotations, move it under `if TYPE_CHECKING:` (see `types-type-checking-imports`). Keep an otherwise-unused import only when importing it has a required side effect (plugin self-registration) — and comment it: `# noqa: F401 — registers handlers at import time`.
