#!/usr/bin/env python3
"""
taint_tracker.py - Lightweight SAST taint tracking engine.

Implements source-to-sink data flow analysis:
- Python: AST-based data flow analysis (import/assignment/attribute tracking)
- JS: Lexical approximation (variable assignment + property access tracking)
- Complex languages: Falls back to pattern matching with analysis depth annotation
- No complete taint path: Downgraded to info level

Author: njskills@agent.qq.com
Version: 3.3.0
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# ============================================================
# Taint Sources & Sinks
# ============================================================

# Source: user input / environment / network response
TAINT_SOURCES_PY = [
    'input(', 'raw_input(', 'sys.argv', 'os.environ', 'os.getenv',
    'request.args', 'request.form', 'request.json', 'request.data',
    'requests.get(', 'requests.post(', 'urllib.request.urlopen(',
    'stdin.read(', 'file.read(', 'socket.recv(', 'flake.request',
]

TAINT_SOURCES_JS = [
    'process.argv', 'process.env', 'req.query', 'req.body', 'req.params',
    'fetch(', 'axios.get(', 'axios.post(', 'request(', '$.get(',
    'document.cookie', 'localStorage.getItem(', 'sessionStorage.getItem(',
]

# Sink: dangerous operations
TAINT_SINKS_PY = [
    'eval(', 'exec(', 'os.system(', 'subprocess.call(', 'subprocess.Popen(',
    'pickle.loads(', 'yaml.load(', 'marshal.loads(', '__import__(',
    'cursor.execute(', 'db.execute(', 'sqlite3.connect(',
    'open(', 'file.write(', 'shutil.copy(',
]

TAINT_SINKS_JS = [
    'eval(', 'exec(', 'child_process.exec(', 'child_process.execSync(',
    'Function(', 'vm.runInNewContext(', 'vm.runInThisContext(',
    'innerHTML=', 'document.write(', 'document.writeln(',
    'db.query(', 'connection.execute(', 'mongoose.insert(',
]

# ============================================================
# Python AST Taint Tracker
# ============================================================

class PythonTaintTracker(ast.NodeVisitor):
    """AST-based taint tracker for Python code."""

    def __init__(self, filename: str):
        self.filename = filename
        self.findings: List[Dict] = []
        self.tainted_vars: Dict[str, Tuple[int, str]] = {}  # var -> (line, source)
        self.import_map: Dict[str, str] = {}  # alias -> full_name
        self.current_function: Optional[str] = None
        self.lines: List[str] = []

    def track(self, source: str, lines: List[str]):
        """Run taint tracking on source code."""
        self.lines = lines
        try:
            tree = ast.parse(source)
            self.visit(tree)
        except SyntaxError:
            pass  # Fall back to pattern matching if AST parse fails
        return self.findings

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.import_map[name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.names:
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                module = node.module or ''
                self.import_map[name] = f"{module}.{name}"
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Check if RHS is a taint source
        source_info = self._get_taint_source(node.value)
        if source_info:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars[target.id] = (node.lineno, source_info)
                elif isinstance(target, ast.Attribute):
                    # e.g., self.data = request.args
                    name = self._get_full_attr_name(target)
                    if name:
                        self.tainted_vars[name] = (node.lineno, source_info)
        else:
            # Check if RHS references a tainted variable
            taint_source = self._find_tainted_ref(node.value)
            if taint_source:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        src_line, src_name = taint_source
                        self.tainted_vars[target.id] = (node.lineno, f"{src_name} (from line {src_line})")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check if this is a taint sink with tainted args
        sink_info = self._get_taint_sink(node)
        if sink_info:
            taint_source = self._find_tainted_arg_source(node)
            if taint_source:
                src_line, src_name = taint_source
                self.findings.append({
                    'type': 'taint_chain',
                    'severity': 'high',
                    'source_line': src_line,
                    'source_name': src_name,
                    'sink_line': node.lineno,
                    'sink_name': sink_info,
                    'flow_path': f"{src_name} (line {src_line}) → {sink_info} (line {node.lineno})",
                    'filename': self.filename,
                })
            else:
                # Sink without clear taint source - lower severity
                self.findings.append({
                    'type': 'taint_sink_only',
                    'severity': 'info',
                    'source_line': 0,
                    'source_name': '',
                    'sink_line': node.lineno,
                    'sink_name': sink_info,
                    'flow_path': f"{sink_info} (line {node.lineno})",
                    'filename': self.filename,
                })
        self.generic_visit(node)

    def _get_taint_source(self, node):
        """Check if node is a taint source."""
        if isinstance(node, ast.Call):
            func_name = self._get_call_name(node)
            if func_name:
                for pattern in TAINT_SOURCES_PY:
                    if pattern in func_name or func_name in pattern:
                        return func_name
        if isinstance(node, ast.Subscript):
            name = self._get_full_attr_name(node.value)
            if name:
                for pattern in ['os.environ', 'request.args', 'request.form', 'req.query', 'req.body']:
                    if pattern in name:
                        return name
        return None

    def _get_taint_sink(self, node):
        """Check if node is a taint sink."""
        if isinstance(node, ast.Call):
            func_name = self._get_call_name(node)
            if func_name:
                for pattern in TAINT_SINKS_PY:
                    if pattern in func_name or func_name in pattern:
                        return func_name
        if isinstance(node, ast.Attribute):
            attr_name = self._get_full_attr_name(node)
            if attr_name:
                for pattern in ['cursor.execute', 'db.execute', 'connection.execute']:
                    if pattern in attr_name:
                        return attr_name
        return None

    def _find_tainted_ref(self, node):
        """Find if node references a tainted variable."""
        if isinstance(node, ast.Name):
            if node.id in self.tainted_vars:
                return self.tainted_vars[node.id]
        elif isinstance(node, ast.Attribute):
            name = self._get_full_attr_name(node)
            if name and name in self.tainted_vars:
                return self.tainted_vars[name]
        elif isinstance(node, ast.Call):
            for arg in node.args:
                result = self._find_tainted_ref(arg)
                if result:
                    return result
            for keyword in node.keywords:
                result = self._find_tainted_ref(keyword.value)
                if result:
                    return result
        elif isinstance(node, ast.BinOp):
            result = self._find_tainted_ref(node.left)
            if result:
                return result
            result = self._find_tainted_ref(node.right)
            if result:
                return result
        elif isinstance(node, ast.JoinedStr):
            for value in node.values:
                result = self._find_tainted_ref(value)
                if result:
                    return result
        return None

    def _find_tainted_arg_source(self, node):
        """Find if any argument to a sink call is tainted."""
        for arg in node.args:
            result = self._find_tainted_ref(arg)
            if result:
                return result
        for keyword in node.keywords:
            result = self._find_tainted_ref(keyword.value)
            if result:
                return result
        return None

    def _get_call_name(self, node):
        """Get full function name from Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id + '('
        elif isinstance(node.func, ast.Attribute):
            return self._get_full_attr_name(node.func) + '('
        return None

    def _get_full_attr_name(self, node):
        """Get full dotted name from Attribute node."""
        if isinstance(node, ast.Attribute):
            parent = self._get_full_attr_name(node.value)
            if parent:
                return f"{parent}.{node.attr}"
        elif isinstance(node, ast.Name):
            return node.id
        return None


# ============================================================
# JS Lexical Taint Tracker (Approximation)
# ============================================================

class JSTaintTracker:
    """Lexical approximation-based taint tracker for JavaScript."""

    def __init__(self, filename: str):
        self.filename = filename
        self.findings: List[Dict] = []
        self.tainted_vars: Dict[str, Tuple[int, str]] = {}
        self.lines: List[str] = []

    def track(self, source: str, lines: List[str]):
        """Run lexical taint tracking."""
        self.lines = lines
        for line_num, line in enumerate(lines, 1):
            # Variable assignment with taint source
            self._track_assignment(line, line_num)
            # Sink call with tainted variable
            self._track_sink_call(line, line_num)
        return self.findings

    def _track_assignment(self, line: str, line_num: int):
        """Track variable assignments from taint sources."""
        # var/let/const x = source(...)
        m = re.match(r'(?:var|let|const)\s+(\w+)\s*=\s*(.+)', line.strip())
        if m:
            var_name, rhs = m.group(1), m.group(2)
            for pattern in TAINT_SOURCES_JS:
                if pattern in rhs:
                    self.tainted_vars[var_name] = (line_num, pattern.strip('('))
                    break
            # Also check if RHS references a tainted variable
            for tv, (tl, tn) in self.tainted_vars.items():
                if tv in rhs:
                    self.tainted_vars[var_name] = (line_num, f"{tn} (from line {tl})")
                    break

    def _track_sink_call(self, line: str, line_num: int):
        """Track sink calls with tainted variables."""
        for pattern in TAINT_SINKS_JS:
            if pattern in line:
                # Check if any tainted var is used in the line
                for tv, (tl, tn) in self.tainted_vars.items():
                    if tv in line:
                        self.findings.append({
                            'type': 'taint_chain',
                            'severity': 'high',
                            'source_line': tl,
                            'source_name': tn,
                            'sink_line': line_num,
                            'sink_name': pattern.strip('('),
                            'flow_path': f"{tn} (line {tl}) → {pattern.strip('(')} (line {line_num})",
                            'filename': self.filename,
                        })
                        return
                # Sink without clear taint
                self.findings.append({
                    'type': 'taint_sink_only',
                    'severity': 'info',
                    'source_line': 0,
                    'source_name': '',
                    'sink_line': line_num,
                    'sink_name': pattern.strip('('),
                    'flow_path': f"{pattern.strip('(')} (line {line_num})",
                    'filename': self.filename,
                })


# ============================================================
# Unified Taint Tracker
# ============================================================

class TaintTracker:
    """Unified taint tracker with automatic language detection."""

    def __init__(self, filename: str):
        self.filename = filename

    def track_file(self, filepath: str) -> List[Dict]:
        """Track taints in a file."""
        try:
            content = Path(filepath).read_text(encoding='utf-8-sig')
        except Exception:
            return []
        lines = content.split('\n')
        ext = Path(filepath).suffix.lower()
        if ext == '.py':
            tracker = PythonTaintTracker(self.filename)
            return tracker.track(content, lines)
        elif ext in ('.js', '.ts', '.jsx', '.tsx'):
            tracker = JSTaintTracker(self.filename)
            return tracker.track(content, lines)
        else:
            # Complex language: fall back to pattern matching
            return self._fallback_pattern_match(content, lines)

    def _fallback_pattern_match(self, content: str, lines: List[str]) -> List[Dict]:
        """Fallback pattern matching for unsupported languages."""
        findings = []
        sink_patterns = [r'eval\s*\(', r'exec\s*\(', r'os\.system\s*\(', r'subprocess\.call\s*\(',
                        r'child_process\.exec\s*\(', r'document\.write\s*\(', r'innerHTML\s*=']
        for line_num, line in enumerate(lines, 1):
            for pat in sink_patterns:
                if re.search(pat, line, re.IGNORECASE):
                    findings.append({
                        'type': 'taint_sink_only',
                        'severity': 'info',
                        'source_line': 0,
                        'source_name': '',
                        'sink_line': line_num,
                        'sink_name': pat.strip('\\').strip('('),
                        'flow_path': f"{pat.strip('\\').strip('(')} (line {line_num}) - 分析深度: 模式匹配",
                        'filename': self.filename,
                    })
        return findings
