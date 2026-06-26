"""Check FastAPI route handlers for missing docstrings."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass

from pylinter_assist.checks.base import CheckResult, Severity

# Decorators that indicate a FastAPI route handler
_ROUTE_DECORATORS = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace", "route",
    "api_route",
})

_ROUTER_NAMES = re.compile(r'^(?:router|app|api|v\d+_router)', re.IGNORECASE)


def _is_route_decorator(decorator: ast.expr) -> bool:
    """Return True if decorator looks like a FastAPI route decorator."""
    # @router.get(...) / @app.post(...)
    if isinstance(decorator, ast.Call):
        func = decorator.func
        if isinstance(func, ast.Attribute):
            return func.attr in _ROUTE_DECORATORS
        if isinstance(func, ast.Name):
            return func.id in _ROUTE_DECORATORS
    # @router.get (no-call form, rare but valid)
    if isinstance(decorator, ast.Attribute):
        return decorator.attr in _ROUTE_DECORATORS
    return False


@dataclass
class FastAPIDocstringCheck:
    name: str = "fastapi-docstring"
    enabled: bool = True

    def check(self, file_path: str, source: str, config: dict) -> list[CheckResult]:
        if not self.enabled:
            return []

        cfg = config.get("fastapi_docstring", {})
        if cfg.get("enabled") is False:
            return []

        severity_str = cfg.get("severity", "warning")
        severity = Severity(severity_str)

        results: list[CheckResult] = []

        try:
            tree = ast.parse(source, filename=file_path)
        except SyntaxError:
            return results

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            has_route_decorator = any(_is_route_decorator(d) for d in node.decorator_list)
            if not has_route_decorator:
                continue

            has_docstring = (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            )

            if not has_docstring:
                results.append(
                    CheckResult(
                        file=file_path,
                        line=node.lineno,
                        col=node.col_offset + 1,
                        severity=severity,
                        code="FAD001",
                        message=f"FastAPI route handler '{node.name}' is missing a docstring",
                        check_name=self.name,
                        context=f"async def {node.name}(...)" if isinstance(node, ast.AsyncFunctionDef)
                        else f"def {node.name}(...)",
                    )
                )

        return results
