---
title: Place Imports at the Top of the File
impact: LOW
impactDescription: makes dependencies visible at a glance
tags: imports, structure, conventions
references: https://peps.python.org/pep-0008/#imports
---

## Place Imports at the Top of the File

Imports belong at the top of the module, grouped (stdlib, third-party, local) with blank lines between groups. Inline imports inside functions hide dependencies from readers, confuse static analysis, and surprise anyone debugging a `ModuleNotFoundError` raised in the middle of a call. `ruff` / `isort` automate the grouping.

**Incorrect (imports scattered through function bodies):**

```python
def fetch_user(user_id: str) -> User:
    import requests  # hidden dependency
    response = requests.get(f"/users/{user_id}")
    return User(**response.json())

def process():
    from .helpers import validate  # easily missed
    import json                    # another one
    data = json.dumps(result)
```

**Correct (all imports at the top, PEP 8 ordering):**

```python
import json
from typing import Any

import requests

from .helpers import validate


def fetch_user(user_id: str) -> User:
    response = requests.get(f"/users/{user_id}")
    return User(**response.json())
```

Inline imports are legitimate only for: breaking circular imports (add a comment so readers don't "fix" it), deferring truly optional/heavy deps behind a runtime gate (see `imports-optional-dependencies`), or avoiding module-load-time side effects. Outside those cases, top-of-file is the rule.
