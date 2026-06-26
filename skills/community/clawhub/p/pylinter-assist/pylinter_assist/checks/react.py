"""Check React useEffect hooks for missing or empty dependency arrays."""

from __future__ import annotations

import re
from dataclasses import dataclass

from pylinter_assist.checks.base import CheckResult, Severity

# Matches useEffect( ... ) calls — handles multi-line via DOTALL
_USE_EFFECT_PATTERN = re.compile(
    r'useEffect\s*\(\s*'           # useEffect(
    r'(?:async\s*)?\(?'            # optional async arrow
    r'(?:[^)]*)\)?\s*=>\s*'        # () =>  or  async () =>
    r'\{[^}]*\}[^,)]*'             # callback body (simplified)
    r'(?P<args>[^)]*)\)',           # remaining args before closing )
    re.DOTALL,
)

# Simpler heuristic: find useEffect calls and inspect trailing argument
_EFFECT_CALL = re.compile(r'\buseEffect\s*\(', re.MULTILINE)
_EMPTY_DEP_ARRAY = re.compile(r',\s*\[\s*\]\s*\)\s*;?')
_HAS_DEP_ARRAY = re.compile(r',\s*\[')


def _extract_useeffect_calls(source: str) -> list[tuple[int, str]]:
    """Return list of (line_number, snippet) for each useEffect call."""
    calls: list[tuple[int, str]] = []
    lines = source.splitlines()

    for match in _EFFECT_CALL.finditer(source):
        start = match.start()
        line_no = source[:start].count("\n") + 1

        # Grab the next 300 chars to inspect the full call
        snippet = source[start : start + 300]
        calls.append((line_no, snippet))

    return calls


@dataclass
class ReactUseEffectCheck:
    name: str = "react-useeffect-deps"
    enabled: bool = True

    def check(self, file_path: str, source: str, config: dict) -> list[CheckResult]:
        if not self.enabled:
            return []

        cfg = config.get("react_useeffect_deps", {})
        if cfg.get("enabled") is False:
            return []

        # Only run on JS/JSX/TS/TSX files
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext not in {"js", "jsx", "ts", "tsx"}:
            return []

        severity_str = cfg.get("severity", "warning")
        severity = Severity(severity_str)

        results: list[CheckResult] = []

        for line_no, snippet in _extract_useeffect_calls(source):
            has_dep = _HAS_DEP_ARRAY.search(snippet)

            if not has_dep:
                results.append(
                    CheckResult(
                        file=file_path,
                        line=line_no,
                        col=1,
                        severity=severity,
                        code="RUE001",
                        message=(
                            "useEffect is missing a dependency array — "
                            "this runs on every render. Add [] or list explicit deps."
                        ),
                        check_name=self.name,
                        context=snippet[:80].strip(),
                    )
                )
            elif _EMPTY_DEP_ARRAY.search(snippet):
                # Empty [] is valid (run-once) but flag if there are refs inside the callback
                # that look like state/props (heuristic: capital letter vars or hooks)
                inner = snippet[: snippet.find(",\n[") + 1] if ",\n[" in snippet else snippet
                if re.search(r'\b[a-z][A-Za-z]+\b', inner):
                    results.append(
                        CheckResult(
                            file=file_path,
                            line=line_no,
                            col=1,
                            severity=Severity.INFO,
                            code="RUE002",
                            message=(
                                "useEffect has empty dependency array [] but callback "
                                "references variables — verify deps are intentionally omitted."
                            ),
                            check_name=self.name,
                            context=snippet[:80].strip(),
                        )
                    )

        return results
