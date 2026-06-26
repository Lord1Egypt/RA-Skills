#!/usr/bin/env python3
"""
vitest_config_validator.py — Validate vitest.config.ts/js configurations.

Commands:
  validate  Full validation (all 22 rules)
  check     Quick syntax-only check (structure rules only)
  explain   Human-readable explanation of the config
  suggest   Suggest improvements

Flags:
  --format text|json|summary   Output format (default: text)
  --strict                     Treat warnings as errors

Exit codes:
  0  No errors
  1  Errors found (or warnings in --strict mode)
  2  File not found or parse error
"""

import re
import sys
import os
import json
import argparse
from typing import List, Tuple, Dict, Optional, Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_ENVIRONMENTS = {"jsdom", "happy-dom", "node", "edge-runtime"}
VALID_COVERAGE_PROVIDERS = {"c8", "v8", "istanbul"}
VALID_POOLS = {"threads", "forks", "vmThreads", "vmForks"}

KNOWN_TOP_LEVEL_KEYS = {
    "test",
    "plugins",
    "resolve",
    "define",
    "root",
    "mode",
    "build",
    "server",
    "optimizeDeps",
    "css",
    "publicDir",
    "assetsInclude",
    "esbuild",
    "worker",
    "logLevel",
    "clearScreen",
    "envDir",
    "envPrefix",
    "appType",
    "experimental",
    "ssr",
    "base",
    "cacheDir",
    "configFile",
}

KNOWN_TEST_KEYS = {
    "include",
    "exclude",
    "includeSource",
    "name",
    "environment",
    "globals",
    "setupFiles",
    "globalSetup",
    "reporters",
    "reporter",
    "outputFile",
    "coverage",
    "testTimeout",
    "hookTimeout",
    "teardownTimeout",
    "silent",
    "open",
    "api",
    "bail",
    "isolate",
    "pool",
    "poolOptions",
    "singleThread",
    "maxConcurrency",
    "watch",
    "watchExclude",
    "forceRerunTriggers",
    "update",
    "snapshotFormat",
    "resolveSnapshotPath",
    "allowOnly",
    "passWithNoTests",
    "logHeapUsage",
    "deps",
    "css",
    "sequence",
    "typecheck",
    "benchmark",
    "alias",
    "threads",
    "minThreads",
    "maxThreads",
    "cache",
    "clearMocks",
    "resetMocks",
    "restoreMocks",
    "mockReset",
    "unstubEnvs",
    "unstubGlobals",
    "diff",
    "chaiConfig",
    "fakeTimers",
    "retry",
    "dangerouslyIgnoreUnhandledErrors",
    "slowTestThreshold",
    "inspect",
    "inspectBrk",
    "fileParallelism",
    "projects",
    "workspace",
    "server",
    "browser",
    "runner",
    "testNamePattern",
    "disableConsoleIntercept",
    "printConsoleTrace",
    "onConsoleLog",
    "onStackTrace",
    "onTestFailed",
    "onTestFinished",
}

# Deprecated options (vitest < 1.0 names that were renamed)
DEPRECATED_OPTIONS: Dict[str, str] = {
    r"\bthreads\s*:\s*false\b": "threads:false is deprecated; use pool:'forks' or singleThread instead",
    r"\bthreads\s*:\s*true\b": "threads:true is deprecated; use pool:'threads' instead",
    r"\bminThreads\b": "minThreads is deprecated; use poolOptions.threads.minThreads",
    r"\bmaxThreads\b": "maxThreads is deprecated; use poolOptions.threads.maxThreads",
    r"\bdeps\.registerNodeLoader\b": "deps.registerNodeLoader is removed in Vitest 1.x",
    r"\bdeps\.experimentalOptimizer\b": "deps.experimentalOptimizer is deprecated; use deps.optimizer",
    r"\bsuite\b\s*:": "suite: key is not a valid Vitest option",
    r"\bspecs\b\s*:": "specs: is not valid; use include: instead",
    r"\btestFiles\b\s*:": "testFiles: is not valid; use include: instead",
}

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, rule_id: str, severity: str, message: str, line: Optional[int] = None):
        self.rule_id = rule_id
        self.severity = severity  # E, W, I
        self.message = message
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "rule": self.rule_id,
            "severity": self.severity,
            "message": self.message,
        }
        if self.line is not None:
            d["line"] = self.line
        return d

    def __str__(self) -> str:
        loc = f" (line {self.line})" if self.line is not None else ""
        return f"[{self.severity}] {self.rule_id}{loc}: {self.message}"


# ---------------------------------------------------------------------------
# Config parser
# ---------------------------------------------------------------------------

def read_file(path: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (content, error_message)."""
    if not os.path.exists(path):
        return None, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), None
    except OSError as e:
        return None, f"Cannot read file: {e}"


def strip_comments(text: str) -> str:
    """Remove // and /* */ comments outside of string literals, preserving line structure."""
    result = []
    i = 0
    n = len(text)
    while i < n:
        # String literals — pass through unchanged
        if text[i] in ('"', "'", '`'):
            quote = text[i]
            result.append(text[i])
            i += 1
            while i < n:
                c = text[i]
                result.append(c)
                if c == '\\' and i + 1 < n:
                    i += 1
                    result.append(text[i])
                elif c == quote:
                    break
                i += 1
            i += 1
            continue
        # Block comment /* ... */
        if text[i] == '/' and i + 1 < n and text[i + 1] == '*':
            j = i + 2
            while j < n - 1:
                if text[j] == '*' and text[j + 1] == '/':
                    j += 2
                    break
                if text[j] == '\n':
                    result.append('\n')
                j += 1
            i = j
            continue
        # Line comment // ...
        if text[i] == '/' and i + 1 < n and text[i + 1] == '/':
            while i < n and text[i] != '\n':
                i += 1
            continue
        result.append(text[i])
        i += 1
    return ''.join(result)


def extract_test_block(content: str) -> Optional[str]:
    """Extract the content of the test: { ... } block (best-effort)."""
    # Find 'test:' or '"test":' key
    match = re.search(r'\btest\s*:\s*\{', content)
    if not match:
        return None

    start = match.end() - 1  # position of opening {
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[start:i+1]
        i += 1
    return None


def extract_string_value(content: str, key: str) -> Optional[str]:
    """Extract string value for a given key like environment: "jsdom"."""
    pattern = rf'\b{re.escape(key)}\s*:\s*["\']([^"\']+)["\']'
    m = re.search(pattern, content)
    return m.group(1) if m else None


def extract_number_value(content: str, key: str) -> Optional[int]:
    """Extract numeric value for a key."""
    pattern = rf'\b{re.escape(key)}\s*:\s*(\d+)'
    m = re.search(pattern, content)
    return int(m.group(1)) if m else None


def extract_bool_value(content: str, key: str) -> Optional[bool]:
    """Extract boolean value for a key."""
    pattern = rf'\b{re.escape(key)}\s*:\s*(true|false)\b'
    m = re.search(pattern, content)
    if m:
        return m.group(1) == "true"
    return None


def find_line(content: str, pattern: str) -> Optional[int]:
    """Return 1-based line number of first match of pattern in content."""
    lines = content.splitlines()
    compiled = re.compile(pattern)
    for i, line in enumerate(lines, 1):
        if compiled.search(line):
            return i
    return None


def extract_array_strings(content: str, key: str) -> List[str]:
    """Extract string items from an array value like include: ["a", "b"]."""
    pattern = rf'\b{re.escape(key)}\s*:\s*\[([^\]]*)\]'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        # might be a single string
        sv = extract_string_value(content, key)
        return [sv] if sv else []
    items_str = m.group(1)
    return re.findall(r'["\']([^"\']+)["\']', items_str)


def extract_top_level_keys(content: str) -> List[str]:
    """Heuristically extract top-level keys from defineConfig({...})."""
    # Find the outer defineConfig block
    m = re.search(r'defineConfig\s*\(?\s*\{', content)
    if not m:
        # try export default { ...
        m = re.search(r'export\s+default\s*\{', content)
    if not m:
        return []

    start = content.find('{', m.start())
    if start == -1:
        return []

    # Extract top-level keys (depth=1)
    keys = []
    depth = 0
    i = start
    buf = []
    while i < len(content):
        c = content[i]
        if c in ('{', '[', '('):
            depth += 1
        elif c in ('}', ']', ')'):
            depth -= 1
            if depth == 0:
                break
        elif depth == 1 and c not in (' ', '\t', '\n', '\r', ','):
            buf.append(c)
        elif depth == 1 and (c == '\n' or c == ','):
            text = ''.join(buf).strip()
            m2 = re.match(r'^([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', text)
            if m2:
                keys.append(m2.group(1))
            buf = []
        i += 1

    # Flush last buffer
    text = ''.join(buf).strip()
    m2 = re.match(r'^([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', text)
    if m2:
        keys.append(m2.group(1))

    return keys


def validate_glob(pattern: str) -> bool:
    """Basic glob pattern sanity check."""
    # Unbalanced braces
    opens = pattern.count('{')
    closes = pattern.count('}')
    if opens != closes:
        return False
    # Double slashes (common mistake)
    if '//' in pattern:
        return False
    # Starts with / but not a rooted glob
    return True


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def check_structure(content: str, stripped: str, path: str) -> List[Issue]:
    """S1-S5: Structure checks."""
    issues: List[Issue] = []

    # S2: Empty / no defineConfig
    if not stripped.strip():
        issues.append(Issue("S2", "E", "Config file is empty"))
        return issues

    has_define_config = bool(re.search(r'\bdefineConfig\b', stripped))
    has_export_default = bool(re.search(r'\bexport\s+default\b', stripped))

    if not has_define_config and not has_export_default:
        issues.append(Issue("S2", "E", "No defineConfig call found — config may not be loaded by Vitest"))

    # S3: No default export
    if not has_export_default:
        issues.append(Issue("S3", "W", "No default export found — Vitest requires 'export default defineConfig(...)'"))

    # S4: Both vitest.config and vite.config with test section
    base = os.path.basename(path)
    if "vitest.config" in base:
        dirname = os.path.dirname(os.path.abspath(path))
        for name in ("vite.config.ts", "vite.config.js", "vite.config.mts", "vite.config.mjs"):
            sibling = os.path.join(dirname, name)
            if os.path.exists(sibling):
                try:
                    with open(sibling, "r", encoding="utf-8") as f:
                        vite_content = f.read()
                    if re.search(r'\btest\s*:', vite_content):
                        issues.append(Issue(
                            "S4", "W",
                            f"Both {base} and {name} define a 'test' section — Vitest may pick up conflicting config"
                        ))
                except OSError:
                    pass

    # S5: Unknown top-level keys
    top_keys = extract_top_level_keys(stripped)
    unknown = [k for k in top_keys if k not in KNOWN_TOP_LEVEL_KEYS]
    for k in unknown:
        line = find_line(content, rf'^\s*{re.escape(k)}\s*:')
        issues.append(Issue("S5", "W", f"Unknown top-level config key: '{k}'", line))

    return issues


def check_test_settings(content: str, stripped: str) -> List[Issue]:
    """T1-T5: Test settings checks."""
    issues: List[Issue] = []
    test_block = extract_test_block(stripped) or stripped

    # T1: environment
    env_val = extract_string_value(test_block, "environment")
    if env_val is not None:
        if env_val not in VALID_ENVIRONMENTS:
            line = find_line(content, r'\benvironment\s*:')
            issues.append(Issue(
                "T1", "E",
                f"Invalid test environment: '{env_val}'. Must be one of: {', '.join(sorted(VALID_ENVIRONMENTS))}",
                line
            ))

    # T2: Empty include/exclude
    for key in ("include", "exclude"):
        vals = extract_array_strings(test_block, key)
        # Detect explicit empty array
        empty_arr = re.search(rf'\b{key}\s*:\s*\[\s*\]', test_block)
        if empty_arr:
            line = find_line(content, rf'\b{key}\s*:')
            issues.append(Issue("T2", "W", f"'{key}' is an empty array — no test files will match", line))

    # T3: Invalid glob patterns
    for key in ("include", "exclude"):
        patterns = extract_array_strings(test_block, key)
        for pat in patterns:
            if not validate_glob(pat):
                line = find_line(content, re.escape(pat))
                issues.append(Issue("T3", "E", f"Invalid glob pattern in '{key}': '{pat}'", line))

    # T4: Coverage provider not set
    has_coverage = bool(re.search(r'\bcoverage\s*:', test_block))
    if has_coverage:
        cov_provider = extract_string_value(test_block, "provider")
        if cov_provider is None:
            line = find_line(content, r'\bcoverage\s*:')
            issues.append(Issue(
                "T4", "I",
                "Coverage is configured but 'provider' is not set — recommend setting provider: 'v8' or 'istanbul'",
                line
            ))
        elif cov_provider not in VALID_COVERAGE_PROVIDERS:
            line = find_line(content, r'\bprovider\s*:')
            issues.append(Issue(
                "T4", "E",
                f"Invalid coverage provider: '{cov_provider}'. Must be one of: {', '.join(sorted(VALID_COVERAGE_PROVIDERS))}",
                line
            ))

    # T5: testTimeout
    timeout_val = extract_number_value(test_block, "testTimeout")
    if timeout_val is not None:
        if timeout_val > 60000:
            line = find_line(content, r'\btestTimeout\s*:')
            issues.append(Issue(
                "T5", "W",
                f"testTimeout is {timeout_val}ms — unreasonably high (>60000ms). Tests should be fast; use per-test overrides instead",
                line
            ))
        elif timeout_val < 100:
            line = find_line(content, r'\btestTimeout\s*:')
            issues.append(Issue(
                "T5", "W",
                f"testTimeout is {timeout_val}ms — unreasonably low (<100ms). Tests may flake due to setup overhead",
                line
            ))

    return issues


def check_performance(content: str, stripped: str) -> List[Issue]:
    """P1-P4: Performance checks."""
    issues: List[Issue] = []
    test_block = extract_test_block(stripped) or stripped

    # P1: singleThread with forks
    single_thread = extract_bool_value(test_block, "singleThread")
    pool_val = extract_string_value(test_block, "pool")
    if single_thread is True and pool_val == "forks":
        line = find_line(content, r'\bsingleThread\s*:')
        issues.append(Issue(
            "P1", "W",
            "singleThread: true with pool: 'forks' disables parallelism entirely — tests run sequentially",
            line
        ))

    # Also catch legacy threads: false pattern
    threads_false = re.search(r'\bthreads\s*:\s*false\b', test_block)
    if threads_false:
        line = find_line(content, r'\bthreads\s*:\s*false\b')
        issues.append(Issue(
            "P1", "W",
            "threads: false disables parallel test execution — use pool: 'forks' with singleFork for clarity",
            line
        ))

    # P2: isolate: false
    isolate_val = extract_bool_value(test_block, "isolate")
    if isolate_val is False:
        line = find_line(content, r'\bisolate\s*:\s*false\b')
        # Check if there's a comment nearby
        if line is not None:
            lines = content.splitlines()
            context_lines = lines[max(0, line-2):line+1]
            has_comment = any('//' in l or '/*' in l for l in context_lines)
        else:
            has_comment = False

        if not has_comment:
            issues.append(Issue(
                "P2", "W",
                "isolate: false can cause test pollution (shared module state between test files). Add a comment explaining why",
                line
            ))

    # P3: No pool configuration
    has_pool = bool(re.search(r'\bpool\s*:', test_block))
    has_pool_options = bool(re.search(r'\bpoolOptions\s*:', test_block))
    if not has_pool and not has_pool_options:
        issues.append(Issue(
            "P3", "I",
            "No pool configuration found — consider setting pool: 'threads' (default) or 'forks' for explicit parallelism control"
        ))

    # P4: globals: true without triple-slash reference or tsconfig types
    globals_val = extract_bool_value(test_block, "globals")
    if globals_val is True:
        # Check for /// <reference types="vitest/globals" /> or vitest/globals in tsconfig
        has_ref = bool(re.search(r'<reference\s+types=["\']vitest', content))
        # Check tsconfig.json in same dir (best effort — just flag it)
        line = find_line(content, r'\bglobals\s*:\s*true\b')
        if not has_ref:
            issues.append(Issue(
                "P4", "W",
                "globals: true requires TypeScript types to be registered. Add '/// <reference types=\"vitest/globals\" />' or add 'vitest/globals' to tsconfig compilerOptions.types",
                line
            ))

    return issues


def check_compatibility(content: str, stripped: str) -> List[Issue]:
    """C1-C3: Compatibility checks."""
    issues: List[Issue] = []
    test_block = extract_test_block(stripped) or stripped

    # C1: Deprecated options
    for pattern, message in DEPRECATED_OPTIONS.items():
        if re.search(pattern, test_block):
            line = find_line(content, pattern)
            issues.append(Issue("C1", "W", message, line))

    # C2: css.modules without css.include
    has_css_modules = bool(re.search(r'\bmodules\s*:', test_block))
    has_css_include = bool(re.search(r'\bcss\s*:.*include\s*:', test_block, re.DOTALL))
    # More targeted: look for css block
    css_match = re.search(r'\bcss\s*:\s*\{([^}]*)\}', test_block, re.DOTALL)
    if css_match:
        css_block = css_match.group(1)
        if re.search(r'\bmodules\s*:', css_block) and not re.search(r'\binclude\s*:', css_block):
            line = find_line(content, r'\bmodules\s*:')
            issues.append(Issue(
                "C2", "W",
                "css.modules is set but css.include is not — CSS transforms may be skipped for non-matched files",
                line
            ))

    # C3: deps.inline and deps.external conflict
    deps_match = re.search(r'\bdeps\s*:\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', test_block, re.DOTALL)
    if deps_match:
        deps_block = deps_match.group(1)
        has_inline = re.search(r'\binline\s*:', deps_block)
        has_external = re.search(r'\bexternal\s*:', deps_block)
        if has_inline and has_external:
            line = find_line(content, r'\bdeps\s*:')
            issues.append(Issue(
                "C3", "W",
                "Both deps.inline and deps.external are set — overlapping entries will cause unpredictable module resolution",
                line
            ))

    return issues


def check_best_practices(content: str, stripped: str) -> List[Issue]:
    """B1-B5: Best practice checks."""
    issues: List[Issue] = []
    test_block = extract_test_block(stripped) or stripped

    # B1: No reporter configured
    has_reporters = bool(re.search(r'\breporters?\s*:', test_block))
    if not has_reporters:
        issues.append(Issue(
            "B1", "I",
            "No reporter configured — consider adding reporters: ['verbose'] for local dev or ['junit'] for CI"
        ))

    # B2: Missing coverage configuration
    has_coverage = bool(re.search(r'\bcoverage\s*:', test_block))
    if not has_coverage:
        issues.append(Issue(
            "B2", "I",
            "No coverage configuration found — add coverage: { provider: 'v8', reporter: ['text', 'lcov'] } to track test coverage"
        ))

    # B3: setupFiles references
    setup_files = extract_array_strings(test_block, "setupFiles")
    if not setup_files:
        sv = extract_string_value(test_block, "setupFiles")
        if sv:
            setup_files = [sv]
    for sf in setup_files:
        # Warn about glob patterns in setupFiles (not supported)
        if '*' in sf or '?' in sf or '[' in sf:
            line = find_line(content, re.escape(sf))
            issues.append(Issue(
                "B3", "W",
                f"setupFiles entry '{sf}' contains glob characters — setupFiles does not support globs, use explicit paths",
                line
            ))

    # B4: snapshotFormat not configured
    has_snapshot = bool(re.search(r'\bsnapshotFormat\s*:', test_block))
    if not has_snapshot:
        issues.append(Issue(
            "B4", "I",
            "snapshotFormat not configured — defaults may differ from Jest. Set snapshotFormat: { escapeString: false } for Jest compatibility"
        ))

    # B5: passWithNoTests
    has_pass_with_no_tests = bool(re.search(r'\bpassWithNoTests\s*:', test_block))
    if not has_pass_with_no_tests:
        issues.append(Issue(
            "B5", "I",
            "passWithNoTests is not set — in CI, Vitest will exit with error code 1 if no test files are found. Set passWithNoTests: true if intentional"
        ))

    return issues


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def run_validate(content: str, stripped: str, path: str, strict: bool) -> List[Issue]:
    """Run all 22 rules."""
    issues: List[Issue] = []
    issues.extend(check_structure(content, stripped, path))
    issues.extend(check_test_settings(content, stripped))
    issues.extend(check_performance(content, stripped))
    issues.extend(check_compatibility(content, stripped))
    issues.extend(check_best_practices(content, stripped))
    return issues


def run_check(content: str, stripped: str, path: str) -> List[Issue]:
    """Structure-only quick check (S rules)."""
    return check_structure(content, stripped, path)


def run_explain(content: str, stripped: str) -> str:
    """Return a human-readable explanation of the config."""
    test_block = extract_test_block(stripped) or stripped
    lines_out = ["=== Vitest Config Explanation ===", ""]

    env = extract_string_value(test_block, "environment")
    lines_out.append(f"Environment     : {env or '(not set, defaults to node)'}")

    include_pats = extract_array_strings(test_block, "include")
    lines_out.append(f"Include patterns: {', '.join(include_pats) if include_pats else '(defaults: **/*.{{test,spec}}.{{js,ts,jsx,tsx}})'}")

    exclude_pats = extract_array_strings(test_block, "exclude")
    lines_out.append(f"Exclude patterns: {', '.join(exclude_pats) if exclude_pats else '(defaults: node_modules, dist)'}")

    timeout = extract_number_value(test_block, "testTimeout")
    lines_out.append(f"Test timeout    : {timeout}ms" if timeout else "Test timeout    : (default: 5000ms)")

    globals_val = extract_bool_value(test_block, "globals")
    lines_out.append(f"Globals         : {'enabled' if globals_val else 'disabled (default)'}")

    isolate_val = extract_bool_value(test_block, "isolate")
    lines_out.append(f"Isolation       : {'disabled (risky)' if isolate_val is False else 'enabled (default)'}")

    pool = extract_string_value(test_block, "pool")
    lines_out.append(f"Pool            : {pool or '(default: threads)'}")

    has_coverage = bool(re.search(r'\bcoverage\s*:', test_block))
    if has_coverage:
        cov_provider = extract_string_value(test_block, "provider")
        lines_out.append(f"Coverage        : enabled (provider: {cov_provider or 'not set'})")
    else:
        lines_out.append("Coverage        : not configured")

    reporters = extract_array_strings(test_block, "reporters")
    if not reporters:
        reporters = extract_array_strings(test_block, "reporter")
    lines_out.append(f"Reporters       : {', '.join(reporters) if reporters else '(default: verbose)'}")

    setup_files = extract_array_strings(test_block, "setupFiles")
    if setup_files:
        lines_out.append(f"Setup files     : {', '.join(setup_files)}")

    pass_no_tests = extract_bool_value(test_block, "passWithNoTests")
    lines_out.append(f"passWithNoTests : {'true' if pass_no_tests else 'false (may fail CI on empty test suite)'}")

    return "\n".join(lines_out)


def run_suggest(issues: List[Issue]) -> str:
    """Generate improvement suggestions from issues."""
    suggestions = []
    severity_order = {"E": 0, "W": 1, "I": 2}
    sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.severity, 3))

    for i, issue in enumerate(sorted_issues, 1):
        if issue.severity == "E":
            prefix = "CRITICAL"
        elif issue.severity == "W":
            prefix = "Recommend"
        else:
            prefix = "Consider"
        suggestions.append(f"{i}. [{prefix}] ({issue.rule_id}) {issue.message}")

    if not suggestions:
        return "No suggestions — config looks good!"
    return "\n".join(["=== Improvement Suggestions ===", ""] + suggestions)


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(issues: List[Issue], path: str, command: str, strict: bool) -> str:
    errors = [i for i in issues if i.severity == "E"]
    warnings = [i for i in issues if i.severity == "W"]
    infos = [i for i in issues if i.severity == "I"]

    lines = [f"Validating: {path}", ""]
    if not issues:
        lines.append("No issues found.")
    else:
        for issue in issues:
            lines.append(str(issue))

    lines.append("")
    effective_errors = len(errors) + (len(warnings) if strict else 0)
    lines.append(
        f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)"
        + (" [strict mode: warnings counted as errors]" if strict else "")
    )

    if effective_errors > 0:
        lines.append("Result: FAIL")
    elif warnings:
        lines.append("Result: WARN")
    else:
        lines.append("Result: PASS")

    return "\n".join(lines)


def format_json(issues: List[Issue], path: str, command: str, strict: bool) -> str:
    errors = [i for i in issues if i.severity == "E"]
    warnings = [i for i in issues if i.severity == "W"]
    infos = [i for i in issues if i.severity == "I"]
    effective_errors = len(errors) + (len(warnings) if strict else 0)

    result = {
        "file": path,
        "command": command,
        "strict": strict,
        "issues": [i.to_dict() for i in issues],
        "summary": {
            "errors": len(errors),
            "warnings": len(warnings),
            "infos": len(infos),
        },
        "result": "FAIL" if effective_errors > 0 else ("WARN" if warnings else "PASS"),
    }
    return json.dumps(result, indent=2)


def format_summary(issues: List[Issue], path: str, strict: bool) -> str:
    errors = [i for i in issues if i.severity == "E"]
    warnings = [i for i in issues if i.severity == "W"]
    effective_errors = len(errors) + (len(warnings) if strict else 0)

    if effective_errors > 0:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    return (
        f"{status} {path} — "
        f"{len(errors)}E {len(warnings)}W {len([i for i in issues if i.severity == 'I'])}I"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="vitest_config_validator",
        description="Validate vitest.config.ts/js configurations",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd, help_text in [
        ("validate", "Full validation (all 22 rules)"),
        ("check", "Quick syntax-only check (structure rules only)"),
        ("explain", "Explain config in human-readable form"),
        ("suggest", "Suggest improvements based on all rules"),
    ]:
        sp = subparsers.add_parser(cmd, help=help_text)
        sp.add_argument("file", help="Path to vitest.config.ts or vitest.config.js")
        sp.add_argument(
            "--format", choices=["text", "json", "summary"], default="text",
            help="Output format (default: text)"
        )
        sp.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    # S1: Read file
    content, error = read_file(args.file)
    if error:
        if args.format == "json":
            print(json.dumps({"error": error, "result": "FAIL", "issues": [
                {"rule": "S1", "severity": "E", "message": error}
            ]}, indent=2))
        elif args.format == "summary":
            print(f"FAIL {args.file} — file error")
        else:
            print(f"[E] S1: {error}")
        return 2

    stripped = strip_comments(content)

    if args.command == "validate":
        issues = run_validate(content, stripped, args.file, args.strict)
    elif args.command == "check":
        issues = run_check(content, stripped, args.file)
    elif args.command == "explain":
        print(run_explain(content, stripped))
        return 0
    elif args.command == "suggest":
        issues = run_validate(content, stripped, args.file, args.strict)
        if args.format == "json":
            suggestions = [
                {"rule": i.rule_id, "severity": i.severity, "message": i.message}
                for i in sorted(issues, key=lambda x: {"E": 0, "W": 1, "I": 2}.get(x.severity, 3))
            ]
            print(json.dumps({"file": args.file, "suggestions": suggestions}, indent=2))
        else:
            print(run_suggest(issues))
        return 0

    # Format and print output
    if args.format == "json":
        print(format_json(issues, args.file, args.command, args.strict))
    elif args.format == "summary":
        print(format_summary(issues, args.file, args.strict))
    else:
        print(format_text(issues, args.file, args.command, args.strict))

    # Exit code
    errors = [i for i in issues if i.severity == "E"]
    warnings = [i for i in issues if i.severity == "W"]
    effective_errors = len(errors) + (len(warnings) if args.strict else 0)
    return 1 if effective_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
