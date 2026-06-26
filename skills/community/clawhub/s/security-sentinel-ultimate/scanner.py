#!/usr/bin/env python3
"""Security Sentinel - AST-based scanner for Python skill directories."""

import ast
import os
import re
import sys
from pathlib import Path

# Patterns that resemble API keys or tokens
SECRET_PATTERNS = [
    re.compile(r"^sk-[a-zA-Z0-9]{20,}$"),           # OpenAI-style
    re.compile(r"^ghp_[a-zA-Z0-9]{36}$"),             # GitHub PAT
    re.compile(r"^AKIA[0-9A-Z]{16}$"),                 # AWS access key
    re.compile(r"^eyJ[a-zA-Z0-9._-]+$"),               # JWT
    re.compile(r"^[a-f0-9]{32,}$"),                    # Hex token
    re.compile(r"^[A-Za-z0-9+/]{40,}={0,2}$"),         # Base64 blob
]

VARIABLE_NAME_HINTS = re.compile(
    r"(api[_-]?key|secret|token|auth|password|credential|private[_-]?key)",
    re.IGNORECASE,
)

# Dangerous function calls to flag
DANGEROUS_CALLS = {
    ("os", "system"),
    ("os", "popen"),
    ("subprocess", "call"),
    ("subprocess", "run"),
    ("subprocess", "Popen"),
    ("subprocess", "check_output"),
    ("subprocess", "check_call"),
    ("subprocess", "getoutput"),
    ("subprocess", "getstatusoutput"),
}

# Bare function names (no module prefix)
DANGEROUS_BARE = {"eval", "exec"}

# Dangerous module names that should never be dynamically loaded
DANGEROUS_MODULES = {"os", "subprocess", "sys", "shutil", "ctypes"}

# Dangerous attribute names that indicate risky behaviour when used with getattr
DANGEROUS_ATTR_NAMES = {
    "system", "popen", "call", "run", "Popen", "check_output", "check_call",
    "getoutput", "getstatusoutput", "eval", "exec",
    "urlopen", "Request", "HTTPConnection", "HTTPSConnection",
}

# Dangerous string literals that hint at obfuscated calls
DANGEROUS_STRING_PARTS = {
    "system", "popen", "subprocess", "eval", "exec",
    "urlopen", "request", "socket", "connect",
}

# ── Severity classification ──────────────────────────────────────────────
RED_CALLS = {"eval", "exec"}          # bare names → critical
RED_MODULES = {"os"}                  # os.system, os.popen → critical
RED_ATTRS = {"system", "popen"}       # dangerous attrs → critical


def classify_severity(visitor):
    """Return overall severity for a scanned file: 'red', 'yellow', or 'green'."""
    has_red = False
    has_yellow = False

    # Hardcoded secrets are always red
    if visitor.hardcoded_secrets:
        has_red = True

    # Obfuscation is always red
    if visitor.obfuscation:
        has_red = True

    # Dangerous calls: use pre-tagged severity
    for _lineno, _call, sev in visitor.dangerous_calls:
        if sev == "red":
            has_red = True
        else:
            has_yellow = True

    # Network calls are yellow
    if visitor.network_calls:
        has_yellow = True

    if has_red:
        return "red"
    if has_yellow:
        return "yellow"
    return "green"

# Network-related calls
NETWORK_CALLS = {
    ("requests", "get"),
    ("requests", "post"),
    ("requests", "put"),
    ("requests", "delete"),
    ("requests", "patch"),
    ("requests", "head"),
    ("requests", "options"),
    ("requests", "request"),
    ("urllib", "request"),
    ("urllib", "urlopen"),
    ("urllib.request", "urlopen"),
    ("urllib.request", "Request"),
    ("http", "client"),
    ("http.client", "HTTPConnection"),
    ("http.client", "HTTPSConnection"),
}


def _get_attr_chain(node):
    """Resolve a chain of attribute accesses like 'urllib.request.urlopen'."""
    parts = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return tuple(reversed(parts))


def _looks_like_secret(variable_name, value):
    """Check if a variable assignment looks like a hardcoded secret."""
    if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
        return False
    raw = value.value.strip()
    if not raw or len(raw) < 12:
        return False
    name_match = VARIABLE_NAME_HINTS.search(variable_name)
    value_match = any(p.match(raw) for p in SECRET_PATTERNS)
    return name_match or value_match


class SecurityVisitor(ast.NodeVisitor):
    """Walk the AST and collect security findings."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.dangerous_calls = []
        self.hardcoded_secrets = []
        self.network_calls = []
        self.obfuscation = []

    def _resolve_string(self, node):
        """Best-effort resolution of string expressions, including concatenation and chr()."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            if 0x20 <= node.value <= 0x7E:
                return chr(node.value)
            return ""
        if isinstance(node, ast.JoinedStr):
            parts = []
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    parts.append(v.value)
                else:
                    parts.append("<?>")
            return "".join(parts)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._resolve_string(node.left) or ""
            right = self._resolve_string(node.right) or ""
            return left + right
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "chr" and node.args:
                inner = self._resolve_string(node.args[0])
                return inner if inner and len(inner) == 1 else ""
            if isinstance(func, ast.Name) and func.id == "bytes":
                return "<bytes>"
        return None

    def _line(self, node):
        return getattr(node, "lineno", "?")

    def visit_Call(self, node):
        func = node.func

        # Handle attribute-based calls: module.func or obj.attr.func
        if isinstance(func, ast.Attribute):
            chain = _get_attr_chain(func)
            # Check at most the last 3 parts (e.g. urllib.request.urlopen)
            for length in range(len(chain), 0, -1):
                segment = chain[-length:] if length <= len(chain) else chain
                # Use the tail segment for matching
                if len(chain) >= 2 and (chain[0], chain[1]) in DANGEROUS_CALLS:
                    sev = "red" if chain[0] in RED_MODULES and chain[1] in RED_ATTRS else "yellow"
                    self.dangerous_calls.append(
                        (self._line(node), f"{'.'.join(chain[:2])}({', '.join(self._arg_summary(node))})", sev)
                    )
                    break
                if len(chain) >= 2 and (chain[0], chain[1]) in NETWORK_CALLS:
                    self.network_calls.append(
                        (self._line(node), f"{'.'.join(chain[:2])}({', '.join(self._arg_summary(node))})", "yellow")
                    )
                    break
            # Also check bare attr name for single-part matches
            if chain in DANGEROUS_CALLS or (len(chain) >= 2 and (chain[0], chain[1]) in DANGEROUS_CALLS):
                pass  # already handled
            # Check for requests.<method> style
            if len(chain) >= 2:
                pair = (chain[0], chain[1])
                if pair in DANGEROUS_CALLS and not self.dangerous_calls:
                    sev = "red" if chain[0] in RED_MODULES and chain[1] in RED_ATTRS else "yellow"
                    self.dangerous_calls.append(
                        (self._line(node), f"{'.'.join(chain)}(...)", sev)
                    )
                if pair in NETWORK_CALLS and not self.network_calls:
                    self.network_calls.append(
                        (self._line(node), f"{'.'.join(chain)}(...)", "yellow")
                    )

        # Handle bare function names: eval(), exec()
        elif isinstance(func, ast.Name):
            if func.id in DANGEROUS_BARE:
                self.dangerous_calls.append(
                    (self._line(node), f"{func.id}({', '.join(self._arg_summary(node))})", "red")
                )

            # --- Bypass #1: getattr(obj, 'dangerous_name') ---
            if func.id == "getattr" and len(node.args) >= 2:
                attr_arg = self._resolve_string(node.args[1])
                if attr_arg and attr_arg in DANGEROUS_ATTR_NAMES:
                    self.obfuscation.append(
                        (self._line(node), "getattr-indirection",
                         f"getattr(..., '{attr_arg}') hides a call to a dangerous attribute", "red")
                    )
                    self.dangerous_calls.append(
                        (self._line(node), f"getattr(..., '{attr_arg}')", "red")
                    )

            # --- Bypass #2: __import__('module').func() ---
            if func.id == "__import__" and node.args:
                mod_arg = self._resolve_string(node.args[0])
                if mod_arg and mod_arg in DANGEROUS_MODULES:
                    self.obfuscation.append(
                        (self._line(node), "dynamic-import",
                         f"__import__('{mod_arg}') dynamically loads a dangerous module", "red")
                    )
                    self.dangerous_calls.append(
                        (self._line(node), f"__import__('{mod_arg}')", "red")
                    )

        # --- Bypass #2 alt: importlib.import_module('module') ---
        if isinstance(func, ast.Attribute):
            chain = _get_attr_chain(func)
            if (len(chain) >= 2 and chain[-1] == "import_module"
                    and chain[-2] in ("importlib",)):
                if node.args:
                    mod_arg = self._resolve_string(node.args[0])
                    if mod_arg and mod_arg in DANGEROUS_MODULES:
                        self.obfuscation.append(
                            (self._line(node), "dynamic-import",
                             f"importlib.import_module('{mod_arg}') dynamically loads a dangerous module", "red")
                        )
                        self.dangerous_calls.append(
                            (self._line(node), f"importlib.import_module('{mod_arg}')", "red")
                        )

        self.generic_visit(node)

    def visit_Assign(self, node):
        """Check assignments for hardcoded secrets, including concatenated strings."""
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id

            # Direct constant assignment
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if _looks_like_secret(name, node.value):
                    snippet = node.value.value
                    masked = snippet[:4] + "..." + snippet[-4:] if len(snippet) > 12 else snippet
                    self.hardcoded_secrets.append(
                        (self._line(node), name, masked, "red")
                    )

            # Concatenated / built-up strings: key = "sk-" + "abcd..."
            # Skip if the value is already a plain constant (handled above)
            if not isinstance(node.value, ast.Constant):
                resolved = self._resolve_string(node.value)
                if resolved and len(resolved) >= 12:
                    if VARIABLE_NAME_HINTS.search(name) or any(p.match(resolved) for p in SECRET_PATTERNS):
                        masked = resolved[:4] + "..." + resolved[-4:] if len(resolved) > 12 else resolved
                        self.hardcoded_secrets.append(
                            (self._line(node), name, masked, "red")
                        )
                        self.obfuscation.append(
                            (self._line(node), "string-concat",
                             f"Secret built via expression (resolved to {len(resolved)} chars)", "red")
                        )
        self.generic_visit(node)

    @staticmethod
    def _arg_summary(node):
        """Return a short representation of call arguments."""
        args = []
        for a in node.args[:2]:
            if isinstance(a, ast.Constant):
                val = str(a.value)
                args.append(val[:40])
            else:
                args.append("...")
        return args

    def _count_chr_calls(self, node):
        """Count chr() calls nested in an expression to detect encoding tricks."""
        count = 0
        for child in ast.walk(node):
            if (isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Name)
                    and child.func.id == "chr"):
                count += 1
        return count

    def _is_nested_binop(self, node):
        """Check if this BinOp is a child of a larger BinOp (to avoid duplicate reports)."""
        # We rely on the fact that generic_visit walks children after the parent.
        # If a parent BinOp already had >= 3 chr() calls, we mark children to skip.
        return getattr(node, "_skip_chr_report", False)

    def visit_BinOp(self, node):
        """Detect chr()-heavy string construction (bypass #3)."""
        if self._is_nested_binop(node):
            self.generic_visit(node)
            return
        chr_count = self._count_chr_calls(node)
        if chr_count >= 3:
            resolved = self._resolve_string(node)
            snippet = resolved[:60] if resolved else "<unresolvable>"
            hint = ""
            for part in DANGEROUS_STRING_PARTS:
                if resolved and part in resolved.lower():
                    hint = f" (contains '{part}')"
                    break
            self.obfuscation.append(
                (self._line(node), "chr-encoding",
                 f"{chr_count} chr() calls build string: \"{snippet}\"{hint}", "red")
            )
            if hint:
                self.dangerous_calls.append(
                    (self._line(node), f"<chr-encoded>{hint}", "red")
                )
            # Mark child BinOp nodes so they don't double-report
            for child in ast.walk(node):
                if child is not node and isinstance(child, ast.BinOp):
                    child._skip_chr_report = True
        self.generic_visit(node)


def scan_file(filepath):
    """Parse a single Python file and return findings."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, ValueError):
        return None

    visitor = SecurityVisitor(filepath)
    visitor.visit(tree)
    return visitor


def scan_directory(directory):
    """Walk a directory and scan all .py files."""
    findings = []
    for root, _, files in os.walk(directory):
        for fname in sorted(files):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            result = scan_file(fpath)
            if result is None:
                continue
            if result.dangerous_calls or result.hardcoded_secrets or result.network_calls or result.obfuscation:
                findings.append(result)
    return findings


def scan_hidden_files(directory):
    """Find files and directories whose names start with a dot."""
    hidden = []
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d.startswith("."):
                hidden.append(("dir", os.path.relpath(os.path.join(root, d), directory)))
        for f in files:
            if f.startswith("."):
                hidden.append(("file", os.path.relpath(os.path.join(root, f), directory)))
    return hidden


SEVERITY_LABEL = {
    "red": "CRITICAL",
    "yellow": "WARNING",
    "green": "OK",
}

SEVERITY_ICON = {
    "red": "🔴",
    "yellow": "🟡",
    "green": "🟢",
}


def _overall_status(findings, hidden_files):
    """Determine the overall scan status from all findings."""
    if not findings and not hidden_files:
        return "green"
    for v in findings:
        if classify_severity(v) == "red":
            return "red"
    # Hidden files bump overall to yellow
    if hidden_files:
        return "yellow"
    for v in findings:
        if classify_severity(v) == "yellow":
            return "yellow"
    return "green"


def format_report(findings, directory, hidden_files):
    """Render findings as a Markdown report with severity summary."""
    # Classify every file
    file_statuses = []
    for v in findings:
        sev = classify_severity(v)
        rel = os.path.relpath(v.filepath, directory)
        file_statuses.append((rel, sev))

    # Count all scanned files (including clean ones)
    total_py = sum(1 for _, _, files in os.walk(directory) for f in files if f.endswith(".py"))
    clean_count = total_py - len(findings)

    overall = _overall_status(findings, hidden_files)
    red_count = sum(1 for _, s in file_statuses if s == "red")
    yellow_count = sum(1 for _, s in file_statuses if s == "yellow")
    green_count = clean_count + sum(1 for _, s in file_statuses if s == "green" and s != "red")

    lines = [
        "# Security Sentinel Report",
        "",
        f"**Directory:** `{directory}`",
        f"**Overall Status:** {SEVERITY_ICON[overall]} **{SEVERITY_LABEL[overall]}**",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Python files scanned | {total_py} |",
        f"| {SEVERITY_ICON['red']} Critical (red) | {red_count} |",
        f"| {SEVERITY_ICON['yellow']} Warning (yellow) | {yellow_count} |",
        f"| {SEVERITY_ICON['green']} Clean (green) | {green_count} |",
        f"| Hidden items | {len(hidden_files)} |",
        "",
    ]

    # Per-file status table
    if file_statuses:
        lines.append("### File Status")
        lines.append("")
        lines.append("| File | Status |")
        lines.append("|------|--------|")
        for rel, sev in file_statuses:
            lines.append(f"| `{rel}` | {SEVERITY_ICON[sev]} {SEVERITY_LABEL[sev]} |")
        if clean_count:
            lines.append(f"| *{clean_count} clean file(s)* | {SEVERITY_ICON['green']} OK |")
        lines.append("")

    if hidden_files:
        lines.append("## Hidden Files and Directories")
        lines.append("")
        lines.append("| Type | Path | Status |")
        lines.append("|------|------|--------|")
        for kind, path in hidden_files:
            lines.append(f"| {kind} | `{path}` | {SEVERITY_ICON['yellow']} WARNING |")
        lines.append("")

    if not findings and not hidden_files:
        lines.append(f"> {SEVERITY_ICON['green']} No issues found. All files are clean.")
        return "\n".join(lines)

    # Detailed findings per file
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Findings")
    lines.append("")

    for v in findings:
        rel = os.path.relpath(v.filepath, directory)
        sev = classify_severity(v)
        lines.append(f"### {SEVERITY_ICON[sev]} `{rel}` — {SEVERITY_LABEL[sev]}")
        lines.append("")

        if v.obfuscation:
            lines.append("#### Obfuscation Detected")
            lines.append("")
            lines.append("| Line | Technique | Detail | Severity |")
            lines.append("|------|-----------|--------|----------|")
            for entry in v.obfuscation:
                lineno, technique, detail, sev = entry[0], entry[1], entry[2], entry[3]
                lines.append(f"| {lineno} | `{technique}` | {detail} | {SEVERITY_ICON[sev]} {SEVERITY_LABEL[sev]} |")
            lines.append("")

        if v.dangerous_calls:
            lines.append("#### Dangerous Calls")
            lines.append("")
            lines.append("| Line | Call | Severity |")
            lines.append("|------|------|----------|")
            for entry in v.dangerous_calls:
                lineno, call, sev = entry[0], entry[1], entry[2]
                lines.append(f"| {lineno} | `{call}` | {SEVERITY_ICON[sev]} {SEVERITY_LABEL[sev]} |")
            lines.append("")

        if v.hardcoded_secrets:
            lines.append("#### Hardcoded Secrets")
            lines.append("")
            lines.append("| Line | Variable | Value | Severity |")
            lines.append("|------|----------|-------|----------|")
            for entry in v.hardcoded_secrets:
                lineno, name, masked, sev = entry[0], entry[1], entry[2], entry[3]
                lines.append(f"| {lineno} | `{name}` | `{masked}` | {SEVERITY_ICON[sev]} {SEVERITY_LABEL[sev]} |")
            lines.append("")

        if v.network_calls:
            lines.append("#### Network Calls")
            lines.append("")
            lines.append("| Line | Call | Severity |")
            lines.append("|------|------|----------|")
            for entry in v.network_calls:
                lineno, call, sev = entry[0], entry[1], entry[2]
                lines.append(f"| {lineno} | `{call}` | {SEVERITY_ICON[sev]} {SEVERITY_LABEL[sev]} |")
            lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <skill_directory>", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: `{directory}` is not a directory.", file=sys.stderr)
        sys.exit(1)

    findings = scan_directory(directory)
    hidden = scan_hidden_files(directory)
    print(format_report(findings, directory, hidden))


if __name__ == "__main__":
    main()
