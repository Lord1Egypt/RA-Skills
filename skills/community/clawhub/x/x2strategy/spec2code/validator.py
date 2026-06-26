"""Code validator — AST syntax check + Backtrader structural & indicator validation.

Validates generated strategy code before execution. Catches:
  - Python syntax errors (via ast.parse)
  - Missing Backtrader imports
  - Missing Strategy class
  - Missing cerebro runner block
  - Non-existent bt.indicators references (dynamic check against installed backtrader)
"""

import ast
import re
from typing import List, Set, Tuple

from spec2code.models import ValidationResult

# ── Indicator registry (built once at import time) ──────────────
_VALID_INDICATORS: Set[str] = set()


def _build_indicator_registry() -> Set[str]:
    """Dynamically inspect backtrader to get all valid indicator names.

    Ported from QSA stage4_validation.py — uses inspect.getmembers to
    reflect bt.indicators so the check stays in sync with the installed
    backtrader version.  Returns empty set if backtrader is not installed.
    """
    try:
        import backtrader as bt
        import inspect

        indicators = set()
        for name, obj in inspect.getmembers(bt.indicators):
            if inspect.isclass(obj) and issubclass(obj, bt.Indicator):
                indicators.add(name)
        return indicators
    except ImportError:
        return set()


_VALID_INDICATORS = _build_indicator_registry()


def validate_code(code: str) -> ValidationResult:
    """Validate strategy code and return a ValidationResult.

    Performs three levels of checking:
      1. AST syntax validation (hard errors)
      2. Structural checks for Backtrader patterns (warnings)
      3. Indicator existence check (errors — if backtrader is available)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # ── Level 1: Syntax check ──
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"SyntaxError at line {e.lineno}: {e.msg}")
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    # ── Level 2: Structural checks ──
    tree = ast.parse(code)

    # Check for backtrader import
    has_bt_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "backtrader" or (alias.asname and alias.asname == "bt"):
                    has_bt_import = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and "backtrader" in node.module:
                has_bt_import = True

    if not has_bt_import:
        warnings.append("No 'import backtrader' found — strategy may not run")

    # Check for Strategy class
    has_strategy_class = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = ""
                if isinstance(base, ast.Attribute):
                    base_name = f"{_get_name(base.value)}.{base.attr}"
                elif isinstance(base, ast.Name):
                    base_name = base.id
                if "Strategy" in base_name:
                    has_strategy_class = True

    if not has_strategy_class:
        warnings.append("No class inheriting from bt.Strategy found")

    # Check for cerebro / runner
    has_cerebro = "cerebro" in code.lower() or "Cerebro" in code
    if not has_cerebro:
        warnings.append("No Cerebro runner found — code may not be self-executable")

    # Check for if __name__ == "__main__"
    has_main_guard = '__name__' in code and '__main__' in code
    if not has_main_guard:
        warnings.append("No if __name__ == '__main__' guard")

    # ── Level 3: Indicator existence check ──
    # Only runs when backtrader is installed (codegen extra).
    # Detects bt.indicators.XXX, bt.ind.XXX, btind.XXX patterns in AST.
    if _VALID_INDICATORS:
        invalid = _check_indicators(tree)
        errors.extend(invalid)

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def _check_indicators(tree: ast.AST) -> List[str]:
    """Check all bt.indicators references against the installed registry.

    Detects three access patterns:
      - bt.indicators.SMA  (standard)
      - bt.ind.SMA         (shorthand)
      - btind.SMA          (alias import)
    """
    errors: List[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue

        indicator_name = None
        full_path = ""

        # Pattern 1: bt.indicators.SMA or bt.ind.SMA
        if (isinstance(node.value, ast.Attribute)
                and node.value.attr in ('indicators', 'ind')
                and isinstance(node.value.value, ast.Name)
                and node.value.value.id == 'bt'):
            indicator_name = node.attr
            full_path = f"bt.{node.value.attr}.{indicator_name}"

        # Pattern 2: btind.SMA
        elif (isinstance(node.value, ast.Name)
              and node.value.id == 'btind'):
            indicator_name = node.attr
            full_path = f"btind.{indicator_name}"

        if indicator_name and indicator_name not in _VALID_INDICATORS:
            # Show a few valid alternatives to help the agent fix it
            sample = sorted(list(_VALID_INDICATORS))[:10]
            errors.append(
                f"Invalid indicator: '{full_path}' does not exist in backtrader. "
                f"Valid examples: {', '.join(sample)}, ... "
                f"({len(_VALID_INDICATORS)} total)"
            )

    return errors


def _get_name(node: ast.AST) -> str:
    """Extract name from an AST node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_get_name(node.value)}.{node.attr}"
    return ""
