#!/usr/bin/env python3
"""
Code Review - Core Analyzer

Analyzes code for quality, best practices, security, and style issues.
"""

import ast
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

# Import C support library
c_support_path = Path(__file__).parent.parent.parent / 'c-support' / 'lib'
if c_support_path.exists():
    sys.path.insert(0, str(c_support_path))
    try:
        from c_parser import CParser
        from c_security_rules import CSecurityChecker
        C_SUPPORT_AVAILABLE = True
    except ImportError:
        C_SUPPORT_AVAILABLE = False
else:
    C_SUPPORT_AVAILABLE = False


@dataclass
class Issue:
    """A code review issue"""
    rule: str                    # e.g., "complexity", "style", "security"
    severity: str                # "error", "warning", "info"
    message: str                 # Human-readable description
    file: str
    line: int = 0
    column: int = 0
    suggestion: str = ""         # Suggested fix
    code_snippet: str = ""       # Relevant code


@dataclass
class FileReview:
    """Review results for a single file"""
    file: str
    language: str
    issues: List[Issue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")


@dataclass
class ReviewReport:
    """Complete review report"""
    files: List[FileReview] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def add_file(self, review: FileReview):
        self.files.append(review)

    def generate_summary(self):
        """Generate summary statistics"""
        total_issues = sum(len(f.issues) for f in self.files)
        total_errors = sum(f.error_count for f in self.files)
        total_warnings = sum(f.warning_count for f in self.files)
        total_info = sum(f.info_count for f in self.files)

        self.summary = {
            'files_reviewed': len(self.files),
            'total_issues': total_issues,
            'errors': total_errors,
            'warnings': total_warnings,
            'info': total_info,
            'by_rule': {}
        }

        # Count by rule
        for file_review in self.files:
            for issue in file_review.issues:
                rule = issue.rule
                if rule not in self.summary['by_rule']:
                    self.summary['by_rule'][rule] = {'count': 0, 'severity': issue.severity}
                self.summary['by_rule'][rule]['count'] += 1


class BaseAnalyzer:
    """Base class for language-specific analyzers"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.max_complexity = self.config.get('max_complexity', 10)
        self.max_function_lines = self.config.get('max_function_lines', 50)
        self.max_file_lines = self.config.get('max_file_lines', 500)

    def analyze(self, filepath: Path, content: str) -> FileReview:
        """Analyze a file and return review"""
        raise NotImplementedError


class PythonAnalyzer(BaseAnalyzer):
    """Python code analyzer"""

    def analyze(self, filepath: Path, content: str) -> FileReview:
        review = FileReview(
            file=str(filepath),
            language='Python'
        )

        lines = content.split('\n')

        # File-level checks
        self._check_file_length(review, lines)
        self._check_trailing_whitespace(review, lines)
        self._check_line_length(review, lines)

        # AST-based checks
        try:
            tree = ast.parse(content)
            self._check_complexity(review, tree, lines)
            self._check_function_length(review, tree, lines)
            self._check_docstrings(review, tree, lines)
            self._check_imports(review, tree, lines)
            self._check_security(review, tree, lines, content)

            # Calculate metrics
            review.metrics['functions'] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            review.metrics['classes'] = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            review.metrics['complexity'] = self._calculate_complexity(tree)

        except SyntaxError as e:
            review.issues.append(Issue(
                rule='syntax',
                severity='error',
                message=f'Syntax error: {e.msg}',
                file=str(filepath),
                line=e.lineno or 0
            ))

        return review

    def _check_file_length(self, review: FileReview, lines: List[str]):
        """Check if file is too long"""
        if len(lines) > self.max_file_lines:
            review.issues.append(Issue(
                rule='file-too-long',
                severity='warning',
                message=f'File has {len(lines)} lines (max {self.max_file_lines})',
                file=review.file,
                suggestion='Consider splitting into smaller modules'
            ))

    def _check_trailing_whitespace(self, review: FileReview, lines: List[str]):
        """Check for trailing whitespace"""
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                review.issues.append(Issue(
                    rule='trailing-whitespace',
                    severity='info',
                    message='Line has trailing whitespace',
                    file=review.file,
                    line=i,
                    suggestion='Remove trailing spaces'
                ))

    def _check_line_length(self, review: FileReview, lines: List[str]):
        """Check line length (PEP 8: 79 chars)"""
        for i, line in enumerate(lines, 1):
            if len(line) > 100:  # Relaxed from 79
                review.issues.append(Issue(
                    rule='line-too-long',
                    severity='info',
                    message=f'Line is {len(line)} characters (max 100)',
                    file=review.file,
                    line=i,
                    suggestion='Break into multiple lines'
                ))

    def _check_complexity(self, review: FileReview, tree: ast.AST, lines: List[str]):
        """Check cyclomatic complexity of functions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_function_complexity(node)
                if complexity > self.max_complexity:
                    review.issues.append(Issue(
                        rule='high-complexity',
                        severity='warning',
                        message=f'Function "{node.name}" has complexity {complexity} (max {self.max_complexity})',
                        file=review.file,
                        line=node.lineno,
                        suggestion='Refactor into smaller functions'
                    ))

    def _check_function_length(self, review: FileReview, tree: ast.AST, lines: List[str]):
        """Check function length"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if node.end_lineno else 0
                if func_lines > self.max_function_lines:
                    review.issues.append(Issue(
                        rule='function-too-long',
                        severity='warning',
                        message=f'Function "{node.name}" is {func_lines} lines (max {self.max_function_lines})',
                        file=review.file,
                        line=node.lineno,
                        suggestion='Consider breaking into smaller functions'
                    ))

    def _check_docstrings(self, review: FileReview, tree: ast.AST, lines: List[str]):
        """Check for missing docstrings"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    # Skip private methods/functions
                    if not node.name.startswith('_'):
                        review.issues.append(Issue(
                            rule='missing-docstring',
                            severity='info',
                            message=f'{"Function" if isinstance(node, ast.FunctionDef) else "Class"} "{node.name}" lacks docstring',
                            file=review.file,
                            line=node.lineno,
                            suggestion='Add a docstring explaining what this does'
                        ))

    def _check_imports(self, review: FileReview, tree: ast.AST, lines: List[str]):
        """Check import issues"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append((f"{module}.{alias.name}", node.lineno))

        # Check for unused imports (simple check)
        imported_names = {name.split('.')[-1] for name, _ in imports}
        used_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)

        unused = imported_names - used_names - {'*'}
        for name, lineno in imports:
            if name.split('.')[-1] in unused and lineno:
                review.issues.append(Issue(
                    rule='unused-import',
                    severity='warning',
                    message=f'Import "{name}" may be unused',
                    file=review.file,
                    line=lineno,
                    suggestion='Remove unused import'
                ))

    def _check_security(self, review: FileReview, tree: ast.AST, lines: List[str], content: str):
        """Check for security issues"""
        # Check for hardcoded secrets (simple patterns)
        secret_patterns = [
            (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'hardcoded-password', 'Possible hardcoded password'),
            (r'secret\s*=\s*[\'"][^\'"]+[\'"]', 'hardcoded-secret', 'Possible hardcoded secret'),
            (r'api_key\s*=\s*[\'"][^\'"]+[\'"]', 'hardcoded-api-key', 'Possible hardcoded API key'),
            (r'token\s*=\s*[\'"][^\'"]+[\'"]', 'hardcoded-token', 'Possible hardcoded token'),
        ]

        for pattern, rule, message in secret_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                review.issues.append(Issue(
                    rule=rule,
                    severity='error',
                    message=message,
                    file=review.file,
                    line=line_num,
                    suggestion='Use environment variables or secret management'
                ))

        # Check for eval/exec
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ('eval', 'exec'):
                        review.issues.append(Issue(
                            rule='dangerous-function',
                            severity='error',
                            message=f'Use of {node.func.id}() is dangerous',
                            file=review.file,
                            line=node.lineno,
                            suggestion='Use ast.literal_eval for safe evaluation'
                        ))

        # Check for SQL injection patterns
        sql_patterns = [
            r'execute\s*\(\s*[f"\']',
            r'\.format\s*\(',
            r'%\s*\(',
        ]
        for pattern in sql_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                # Only flag if it looks like SQL
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""
                if any(sql in line_content.lower() for sql in ['select', 'insert', 'update', 'delete']):
                    review.issues.append(Issue(
                        rule='sql-injection-risk',
                        severity='warning',
                        message='Possible SQL injection vulnerability',
                        file=review.file,
                        line=line_num,
                        suggestion='Use parameterized queries'
                    ))

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate overall file complexity"""
        total = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total += self._calculate_function_complexity(node)
        return total

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity


class JavaScriptAnalyzer(BaseAnalyzer):
    """JavaScript/TypeScript code analyzer"""

    def analyze(self, filepath: Path, content: str) -> FileReview:
        review = FileReview(
            file=str(filepath),
            language='JavaScript'
        )

        lines = content.split('\n')

        # File-level checks
        self._check_file_length(review, lines)
        self._check_trailing_whitespace(review, lines)

        # Pattern-based checks
        self._check_console_logs(review, content, lines)
        self._check_var_usage(review, content, lines)
        self._check_security(review, content, lines)

        # Calculate metrics
        review.metrics['lines'] = len(lines)
        review.metrics['functions'] = len(re.findall(r'function\s+\w+', content))

        return review

    def _check_file_length(self, review: FileReview, lines: List[str]):
        if len(lines) > self.max_file_lines:
            review.issues.append(Issue(
                rule='file-too-long',
                severity='warning',
                message=f'File has {len(lines)} lines (max {self.max_file_lines})',
                file=review.file
            ))

    def _check_trailing_whitespace(self, review: FileReview, lines: List[str]):
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                review.issues.append(Issue(
                    rule='trailing-whitespace',
                    severity='info',
                    message='Line has trailing whitespace',
                    file=review.file,
                    line=i
                ))

    def _check_console_logs(self, review: FileReview, content: str, lines: List[str]):
        """Check for leftover console.log statements"""
        for i, line in enumerate(lines, 1):
            if 'console.log' in line and not line.strip().startswith('//'):
                review.issues.append(Issue(
                    rule='console-log',
                    severity='info',
                    message='Found console.log statement',
                    file=review.file,
                    line=i,
                    suggestion='Remove debug logging before committing'
                ))

    def _check_var_usage(self, review: FileReview, content: str, lines: List[str]):
        """Check for var usage (should use let/const)"""
        for i, line in enumerate(lines, 1):
            if re.search(r'\bvar\s+', line):
                review.issues.append(Issue(
                    rule='prefer-let-const',
                    severity='info',
                    message='Use let or const instead of var',
                    file=review.file,
                    line=i
                ))

    def _check_security(self, review: FileReview, content: str, lines: List[str]):
        """Check for security issues"""
        # Check for eval
        for i, line in enumerate(lines, 1):
            if 'eval(' in line and not line.strip().startswith('//'):
                review.issues.append(Issue(
                    rule='dangerous-eval',
                    severity='error',
                    message='Use of eval() is dangerous',
                    file=review.file,
                    line=i
                ))

        # Check for innerHTML
        for i, line in enumerate(lines, 1):
            if 'innerHTML' in line:
                review.issues.append(Issue(
                    rule='xss-risk',
                    severity='warning',
                    message='innerHTML can lead to XSS vulnerabilities',
                    file=review.file,
                    line=i,
                    suggestion='Use textContent or sanitized HTML'
                ))


class CAnalyzer(BaseAnalyzer):
    """C/C++ code analyzer"""

    DANGEROUS_FUNCTIONS = {
        'strcpy': ('Use strncpy or strlcpy', 'Buffer overflow risk'),
        'strcat': ('Use strncat or strlcat', 'Buffer overflow risk'),
        'sprintf': ('Use snprintf', 'Buffer overflow risk'),
        'vsprintf': ('Use vsnprintf', 'Buffer overflow risk'),
        'gets': ('Use fgets', 'Removed in C11, buffer overflow'),
        'scanf': ('Use with width limit', 'Buffer overflow risk'),
    }

    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config)
        self.c_parser = CParser() if C_SUPPORT_AVAILABLE else None
        self.security_checker = CSecurityChecker() if C_SUPPORT_AVAILABLE else None

    def analyze(self, filepath: Path, content: str) -> FileReview:
        review = FileReview(
            file=str(filepath),
            language='C'
        )

        lines = content.split('\n')

        # File-level checks
        self._check_file_length(review, lines)
        self._check_trailing_whitespace(review, lines)
        self._check_line_length(review, lines)

        # C-specific checks
        self._check_dangerous_functions(review, content, lines)
        self._check_goto_usage(review, content, lines)
        self._check_magic_numbers(review, content, lines)
        self._check_function_length_c(review, content, lines)
        self._check_header_guards(review, filepath, content, lines)
        self._check_malloc_null_check(review, content, lines)
        self._check_buffer_size(review, content, lines)

        # Use C parser for deeper analysis if available
        if self.c_parser:
            try:
                info = self.c_parser.parse_file(str(filepath))
                review.metrics['functions'] = len(info.functions)
                review.metrics['macros'] = len(info.macros)
                review.metrics['types'] = len(info.types)
                review.metrics['includes'] = len(info.includes)
            except Exception:
                pass

        # Security checks
        if self.security_checker:
            try:
                sec_issues = self.security_checker.check_file(str(filepath), content)
                for issue in sec_issues:
                    review.issues.append(Issue(
                        rule=f'security-{issue.cwe_id.lower()}',
                        severity=issue.severity.value,
                        message=issue.title,
                        file=review.file,
                        line=issue.line,
                        suggestion=issue.fix,
                        code_snippet=issue.description
                    ))
            except Exception:
                pass

        return review

    def _check_file_length(self, review: FileReview, lines: List[str]):
        if len(lines) > self.max_file_lines:
            review.issues.append(Issue(
                rule='file-too-long',
                severity='warning',
                message=f'File has {len(lines)} lines (max {self.max_file_lines})',
                file=review.file,
                suggestion='Consider splitting into smaller modules'
            ))

    def _check_trailing_whitespace(self, review: FileReview, lines: List[str]):
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                review.issues.append(Issue(
                    rule='trailing-whitespace',
                    severity='info',
                    message='Line has trailing whitespace',
                    file=review.file,
                    line=i,
                    suggestion='Remove trailing spaces'
                ))

    def _check_line_length(self, review: FileReview, lines: List[str]):
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                review.issues.append(Issue(
                    rule='line-too-long',
                    severity='info',
                    message=f'Line is {len(line)} characters (max 100)',
                    file=review.file,
                    line=i,
                    suggestion='Break into multiple lines'
                ))

    def _check_dangerous_functions(self, review: FileReview, content: str, lines: List[str]):
        """Check for dangerous C functions"""
        for func, (replacement, reason) in self.DANGEROUS_FUNCTIONS.items():
            pattern = rf'\b{func}\s*\('
            for i, line in enumerate(lines, 1):
                code = line.split('//')[0]  # Skip comments
                if re.search(pattern, code):
                    review.issues.append(Issue(
                        rule='dangerous-function',
                        severity='error',
                        message=f'Use of {func}(): {reason}',
                        file=review.file,
                        line=i,
                        suggestion=f'Replace with {replacement}',
                        code_snippet=line.strip()
                    ))

    def _check_goto_usage(self, review: FileReview, content: str, lines: List[str]):
        """Check for goto statements"""
        for i, line in enumerate(lines, 1):
            code = line.split('//')[0]
            if re.search(r'\bgoto\s+\w+', code):
                review.issues.append(Issue(
                    rule='goto-used',
                    severity='warning',
                    message='goto statement used',
                    file=review.file,
                    line=i,
                    suggestion='Consider using structured control flow (if/else, loops, functions)'
                ))

    def _check_magic_numbers(self, review: FileReview, content: str, lines: List[str]):
        """Check for magic numbers"""
        # Pattern to match numbers (but not in comments or certain contexts)
        magic_pattern = r'(?<![\w\d_])(\d{2,})(?!\s*\*)'

        for i, line in enumerate(lines, 1):
            code = line.split('//')[0]
            # Skip certain contexts
            if any(skip in code for skip in ['#define', '#include', 'case ', '/*', '*/']):
                continue

            matches = re.findall(magic_pattern, code)
            for match in matches:
                num = int(match)
                # Skip common numbers
                if num in [0, 1, 2, 8, 10, 16, 32, 64, 100, 1000, 1024, 255]:
                    continue
                if num >= 2000 and num <= 2100:  # Likely year
                    continue

                review.issues.append(Issue(
                    rule='magic-number',
                    severity='info',
                    message=f'Magic number {match} detected',
                    file=review.file,
                    line=i,
                    suggestion='Consider using a named constant'
                ))

    def _check_function_length_c(self, review: FileReview, content: str, lines: List[str]):
        """Check function length for C"""
        # Simple regex-based function detection
        func_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'

        for match in re.finditer(func_pattern, content):
            func_name = match.group(2)
            start_pos = match.end() - 1

            # Find closing brace
            brace_count = 1
            pos = start_pos + 1
            while brace_count > 0 and pos < len(content):
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1

            if brace_count == 0:
                func_lines = content[start_pos:pos].count('\n')
                if func_lines > self.max_function_lines:
                    line_num = content[:match.start()].count('\n') + 1
                    review.issues.append(Issue(
                        rule='function-too-long',
                        severity='warning',
                        message=f'Function "{func_name}" is {func_lines} lines (max {self.max_function_lines})',
                        file=review.file,
                        line=line_num,
                        suggestion='Consider breaking into smaller functions'
                    ))

    def _check_header_guards(self, review: FileReview, filepath: Path, content: str, lines: List[str]):
        """Check for header include guards in .h files"""
        if not filepath.suffix == '.h':
            return

        has_ifndef = re.search(r'#ifndef\s+\w+', content)
        has_define = re.search(r'#define\s+\w+', content)
        has_endif = re.search(r'#endif', content)

        if not (has_ifndef and has_define and has_endif):
            review.issues.append(Issue(
                rule='missing-header-guard',
                severity='warning',
                message='Header file lacks include guard',
                file=review.file,
                suggestion='Add #ifndef/#define/#endif guard or #pragma once'
            ))

    def _check_malloc_null_check(self, review: FileReview, content: str, lines: List[str]):
        """Check for malloc return value checks"""
        malloc_pattern = r'(\w+)\s*=\s*malloc\s*\('

        for match in re.finditer(malloc_pattern, content):
            var_name = match.group(1)
            match_end = match.end()
            line_num = content[:match.start()].count('\n') + 1

            # Check next few lines for NULL check
            after_malloc = content[match_end:match_end + 200]
            has_null_check = re.search(rf'{var_name}\s*==\s*NULL|!\s*{var_name}', after_malloc)

            if not has_null_check:
                review.issues.append(Issue(
                    rule='malloc-no-null-check',
                    severity='warning',
                    message=f'malloc() return value not checked for NULL',
                    file=review.file,
                    line=line_num,
                    suggestion=f'Add NULL check: if ({var_name} == NULL) {{ handle_error(); }}'
                ))

    def _check_buffer_size(self, review: FileReview, content: str, lines: List[str]):
        """Check for buffer size issues in declarations"""
        # Check for small stack buffers that might be problematic
        small_buffer_pattern = r'char\s+(\w+)\s*\[\s*(\d+)\s*\]'

        for i, line in enumerate(lines, 1):
            code = line.split('//')[0]
            match = re.search(small_buffer_pattern, code)
            if match:
                size = int(match.group(2))
                if size < 16:
                    review.issues.append(Issue(
                        rule='small-buffer',
                        severity='info',
                        message=f'Small buffer ({size} bytes) declared',
                        file=review.file,
                        line=i,
                        suggestion='Consider if buffer size is sufficient for all use cases'
                    ))


class ReviewEngine:
    """Main review engine"""

    ANALYZERS = {
        '.py': PythonAnalyzer,
        '.js': JavaScriptAnalyzer,
        '.ts': JavaScriptAnalyzer,
        '.jsx': JavaScriptAnalyzer,
        '.tsx': JavaScriptAnalyzer,
        '.c': CAnalyzer,
        '.h': CAnalyzer,
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.analyzers: Dict[str, BaseAnalyzer] = {}

    def get_analyzer(self, filepath: Path) -> Optional[BaseAnalyzer]:
        """Get appropriate analyzer for file type"""
        ext = filepath.suffix.lower()
        if ext not in self.analyzers:
            analyzer_class = self.ANALYZERS.get(ext)
            if analyzer_class:
                self.analyzers[ext] = analyzer_class(self.config)
        return self.analyzers.get(ext)

    def review_file(self, filepath: Path) -> Optional[FileReview]:
        """Review a single file"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return FileReview(
                file=str(filepath),
                language='unknown',
                issues=[Issue(
                    rule='read-error',
                    severity='error',
                    message=f'Could not read file: {e}',
                    file=str(filepath)
                )]
            )

        analyzer = self.get_analyzer(filepath)
        if not analyzer:
            return None  # Skip unsupported files

        return analyzer.analyze(filepath, content)

    def review_files(self, filepaths: List[Path]) -> ReviewReport:
        """Review multiple files"""
        report = ReviewReport()

        for filepath in filepaths:
            review = self.review_file(filepath)
            if review:
                report.add_file(review)

        report.generate_summary()
        return report

    def format_report(self, report: ReviewReport, format: str = 'md') -> str:
        """Format report for output"""
        if format == 'json':
            return json.dumps({
                'summary': report.summary,
                'files': [
                    {
                        'file': f.file,
                        'language': f.language,
                        'metrics': f.metrics,
                        'issues': [asdict(i) for i in f.issues]
                    }
                    for f in report.files
                ]
            }, indent=2)

        # Markdown format
        lines = [
            "# Code Review Report",
            "",
            "## Summary",
            "",
            f"- **Files Reviewed**: {report.summary.get('files_reviewed', 0)}",
            f"- **Total Issues**: {report.summary.get('total_issues', 0)}",
            f"- **Errors**: {report.summary.get('errors', 0)} 🔴",
            f"- **Warnings**: {report.summary.get('warnings', 0)} ⚠️",
            f"- **Info**: {report.summary.get('info', 0)} ℹ️",
            "",
        ]

        # Issues by rule
        by_rule = report.summary.get('by_rule', {})
        if by_rule:
            lines.append("## Issues by Type")
            lines.append("")
            lines.append("| Rule | Count | Severity |")
            lines.append("|------|-------|----------|")
            for rule, data in sorted(by_rule.items(), key=lambda x: x[1]['count'], reverse=True):
                emoji = "🔴" if data['severity'] == 'error' else ("⚠️" if data['severity'] == 'warning' else "ℹ️")
                lines.append(f"| {rule} | {data['count']} | {emoji} {data['severity']} |")
            lines.append("")

        # File details
        if report.files:
            lines.append("## File Details")
            lines.append("")

            for file_review in report.files:
                lines.append(f"### {file_review.file}")
                lines.append("")

                if file_review.metrics:
                    lines.append("**Metrics:**")
                    for key, value in file_review.metrics.items():
                        lines.append(f"- {key}: {value}")
                    lines.append("")

                if file_review.issues:
                    lines.append("**Issues:**")
                    lines.append("")
                    for issue in file_review.issues:
                        emoji = "🔴" if issue.severity == 'error' else ("⚠️" if issue.severity == 'warning' else "ℹ️")
                        lines.append(f"{emoji} **{issue.rule}** (line {issue.line})")
                        lines.append(f"   {issue.message}")
                        if issue.suggestion:
                            lines.append(f"   💡 {issue.suggestion}")
                        lines.append("")
                else:
                    lines.append("✅ No issues found")
                    lines.append("")

        return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Code Review Analyzer')
    parser.add_argument('files', nargs='+', help='Files to review')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--max-complexity', type=int, default=10)
    parser.add_argument('--max-function-lines', type=int, default=50)
    parser.add_argument('--max-file-lines', type=int, default=500)

    args = parser.parse_args()

    config = {
        'max_complexity': args.max_complexity,
        'max_function_lines': args.max_function_lines,
        'max_file_lines': args.max_file_lines,
    }

    engine = ReviewEngine(config)
    filepaths = [Path(f) for f in args.files]
    report = engine.review_files(filepaths)

    output = engine.format_report(report, args.format)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
