---
name: python-typing-checker
description: Analyze Python type annotation coverage and quality — check mypy compliance, find untyped functions, review Protocol usage, Generic types, TypeVar constraints, and modern typing patterns. Use when auditing Python type safety, preparing for strict mypy, or enforcing type annotation standards.
metadata:
  tags: ["python", "typing", "mypy", "type-checking", "code-quality", "static-analysis"]
---

# Python Typing Checker

Deep analysis of type annotation coverage and quality across Python codebases. Finds untyped functions, incorrect annotations, missing generics, improper Protocol usage, and patterns that break type checker inference.

Use when: auditing type safety, preparing to enable strict mypy, reviewing annotation quality, or migrating from untyped to typed Python.

## Analysis Steps

### 1. Project Discovery

```bash
cat pyproject.toml 2>/dev/null | head -30
python3 --version 2>/dev/null

# Mypy config
cat pyproject.toml 2>/dev/null | grep -A30 '\[tool.mypy\]'
cat mypy.ini 2>/dev/null || cat setup.cfg 2>/dev/null | grep -A20 '\[mypy\]'

# py.typed marker (PEP 561)
find . -name "py.typed" -not -path '*/venv/*' 2>/dev/null
find . -name "*.pyi" -not -path '*/venv/*' 2>/dev/null | head -10
find . -name "*.py" -not -path '*/venv/*' -not -path '*/__pycache__/*' | wc -l
```

Determine: Python version, type checker config and strictness, whether package ships types (py.typed), project size.

### 2. Type Annotation Coverage

```bash
# Functions without return type annotation
grep -rn 'def [a-zA-Z_]\+(' --include="*.py" . 2>/dev/null \
  | grep -v 'venv/\|__pycache__\|_test\.py\|test_' | grep -v '\-> ' | head -30

# Completely untyped files
for f in $(find . -name "*.py" -not -path '*/venv/*' -not -path '*/__pycache__/*' \
  -not -name '*_test.py' 2>/dev/null); do
  if ! grep -q ':\s*[A-Z]\|-> \|: str\|: int\|: float\|: bool\|: list\|: dict' "$f" 2>/dev/null; then
    echo "UNTYPED: $f"
  fi
done | head -15

# Coverage estimate
total=$(grep -rc 'def ' --include="*.py" . 2>/dev/null | grep -v 'venv/' | awk -F: '{s+=$2} END {print s}')
typed=$(grep -rc '\-> ' --include="*.py" . 2>/dev/null | grep -v 'venv/' | awk -F: '{s+=$2} END {print s}')
echo "Coverage: $typed / $total functions have return type annotations"
```

### 3. Type Import Patterns

```bash
# Deprecated typing imports (use builtins in 3.9+)
grep -rn 'from typing import List\|from typing import Dict\|from typing import Tuple\|from typing import Set' \
  --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -15

# from __future__ import annotations (PEP 563)
grep -rn 'from __future__ import annotations' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10

# TYPE_CHECKING guard
grep -rn 'TYPE_CHECKING' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10
```

Flag:
- **Deprecated typing imports**: `typing.List/Dict/Tuple/Set` deprecated since 3.9 — use `list/dict/tuple/set`
- **Missing TYPE_CHECKING guard**: types imported only for annotations should be under `if TYPE_CHECKING:` to avoid runtime overhead and circular imports
- **Inconsistent style**: mixing `List[int]` and `list[int]` in same codebase

### 4. Any, Union, and Escape Hatches

```bash
# Any usage (excluding imports)
grep -rn '\bAny\b' --include="*.py" . 2>/dev/null | grep -v 'venv/\|_test\.py\|from typing' | head -20

# type: ignore comments
grep -rn 'type:\s*ignore' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -15

# cast() usage
grep -rn 'cast(' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10

# Optional without None check patterns
grep -rn 'Optional\[' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10
```

Flag:
- **Excessive Any**: each `Any` is a hole in type safety — each usage should be justified
- **Functions returning Any**: callers lose all type information
- **`type: ignore` without error code**: should specify like `# type: ignore[assignment]` for maintainability
- **`cast()` overuse**: runtime no-op that lies to the type checker — prefer `isinstance` narrowing
- **Optional without None handling**: annotating `Optional[X]` but never checking for `None`

### 5. Generics, TypeVar, and Protocol

```bash
# TypeVar definitions
grep -rn 'TypeVar(' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10

# ParamSpec (decorator typing, 3.10+)
grep -rn 'ParamSpec' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -5

# Protocol definitions
grep -rn 'class.*Protocol' --include="*.py" . 2>/dev/null | grep -v 'venv/\|from typing' | head -10

# ABC vs Protocol
grep -rn '@abstractmethod\|class.*ABC' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10

# Complex Callable types
grep -rn 'Callable\[' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10

# dict[str, Any] (could be TypedDict)
grep -rn 'dict\[str,\s*Any\]\|Dict\[str,\s*Any\]' --include="*.py" . 2>/dev/null | grep -v 'venv/' | head -10
```

Flag:
- **Unconstrained TypeVar**: `T = TypeVar('T')` accepts anything — add `bound=` if function needs specific capabilities
- **Missing ParamSpec for decorators**: decorators without `ParamSpec` lose the decorated function's signature
- **ABC where Protocol fits**: if base class has no shared implementation, Protocol gives structural subtyping without inheritance
- **Complex Callable types**: `Callable[[str, int, Optional[dict]], Awaitable[list[str]]]` — use Protocol with `__call__` instead
- **`dict[str, Any]` for structured data**: use `TypedDict` for type-safe key access

### 6. Dataclass & Async Patterns

```bash
# Dataclass issues
grep -A20 '@dataclass' --include="*.py" . 2>/dev/null | grep '^\s\+[a-z_]\+ =' | grep -v ':' | head -10

# TypedDict
grep -rn 'TypedDict' --include="*.py" . 2>/dev/null | grep -v 'venv/\|from typing' | head -10

# Async functions without return type
grep -rn 'async def' --include="*.py" . 2>/dev/null | grep -v 'venv/\|_test\.py' | grep -v '\->' | head -10
```

Flag:
- **Dataclass fields without types**: required in strict mode
- **Mutable default in dataclass**: `field: list = []` shared across instances — use `field(default_factory=list)`
- **Async functions without return annotation**: type checker infers `Coroutine[Any, Any, Any]`

### 7. Mypy Strictness Audit

```bash
grep -i 'strict\|disallow_untyped_defs\|disallow_any_generics\|warn_return_any\|check_untyped_defs' \
  pyproject.toml mypy.ini setup.cfg 2>/dev/null | head -15
```

Recommended strictness progression:
1. `check_untyped_defs = true` — type-check bodies even without annotations
2. `no_implicit_optional = true` — require explicit `Optional[X]` for `= None`
3. `warn_return_any = true` — flag functions returning `Any` via untyped calls
4. `disallow_untyped_defs = true` — require annotations on all functions
5. `disallow_any_generics = true` — require type params (`list[int]` not `list`)
6. `strict = true` — all strict flags (goal state)

## Output Template

```markdown
# Python Typing Analysis — [Project Name]

## Summary
- Files: N | Python: 3.XX | Type checker: mypy/pyright/none
- Functions with return types: N/M (XX%) | Any usages: N | type:ignore: N

## Coverage by Package
| Package | Functions | Typed | Coverage |
|---------|-----------|-------|----------|
| src/core/ | 30 | 12 | 40% |
| src/api/ | 45 | 40 | 89% |

## Critical Findings
### [C1] Function Returns Any, Callers Assume str
- **File**: src/utils/parser.py:34 — Fix: `def parse(data: bytes) -> ParseResult:`
### [C2] Optional Without None Check
- **File**: src/api/handlers.py:56 — Fix: add None guard before access

## Recommendations
1. Enable `check_untyped_defs = true` in mypy config
2. Add return types to N functions in highest-priority packages
3. Replace N deprecated `typing.List/Dict` imports with builtins
4. Add error codes to N `type: ignore` comments
5. Replace N `dict[str, Any]` with TypedDict, add `ParamSpec` to N decorators
6. Add `py.typed` marker if package is distributed as library
```

## Tips

- Run `mypy --strict --show-error-codes .` to see all strict violations
- Use `reveal_type(expr)` to debug inference, `typing.assert_type()` (3.11+) for tests
- Run `pyright --verifytypes <package>` to check exported API completeness
- Use `stubgen` for `.pyi` stubs, `monkeytype` for runtime-traced annotations
- For complex dict structures, use `datamodel-code-generator` to generate TypedDict from JSON
