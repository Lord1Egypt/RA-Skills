#!/usr/bin/env python3
"""
Code Analyzer - Python 代码分析与优化工具
"""

import ast
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from enum import Enum


class Severity(Enum):
    """问题严重性等级"""
    P0 = "P0"  # 必须修复 - 安全/稳定性问题
    P1 = "P1"  # 重要 - 可靠性问题
    P2 = "P2"  # 建议 - 质量问题
    P3 = "P3"  # 可选 - 风格问题


@dataclass
class Issue:
    """代码问题"""
    severity: Severity
    line: int
    message: str
    rule: str
    suggestion: str = ""


@dataclass
class AnalysisResult:
    """分析结果"""
    file_path: str
    issues: List[Issue] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)
    
    def get_by_severity(self, severity: Severity) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]
    
    @property
    def has_critical(self) -> bool:
        return any(i.severity == Severity.P0 for i in self.issues)


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.rules = {
            # P0 - 安全
            'bare_except': self._check_bare_except,
            'hardcoded_secrets': self._check_hardcoded_secrets,
            'sql_injection': self._check_sql_injection,
            'command_injection': self._check_command_injection,
            'dangerous_functions': self._check_dangerous_functions,
            
            # P1 - 可靠性
            'missing_timeout': self._check_missing_timeout,
            'resource_leaks': self._check_resource_leaks,
            'unclosed_files': self._check_unclosed_files,
            
            # P2 - 质量
            'inline_imports': self._check_inline_imports,
            'missing_type_hints': self._check_type_hints,
            'long_functions': self._check_long_functions,
            'unused_variables': self._check_unused_variables,
            'debug_code': self._check_debug_code,
            'hardcoded_urls': self._check_hardcoded_urls,
        }
    
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """分析单个文件"""
        result = AnalysisResult(file_path=file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            result.issues.append(Issue(
                severity=Severity.P0,
                line=0,
                message=f"无法读取文件: {e}",
                rule="file_read"
            ))
            return result
        
        # 语法检查
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            result.issues.append(Issue(
                severity=Severity.P0,
                line=e.lineno or 0,
                message=f"语法错误: {e.msg}",
                rule="syntax_error"
            ))
            return result
        
        # 统计信息
        result.stats = self._gather_stats(tree)
        
        # 运行所有规则检查
        for rule_name, rule_func in self.rules.items():
            issues = rule_func(tree, code)
            result.issues.extend(issues)
        
        return result
    
    def _gather_stats(self, tree: ast.AST) -> Dict:
        """收集代码统计信息"""
        stats = {
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'lines': 0,
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stats['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                stats['classes'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                stats['imports'] += 1
        
        return stats
    
    def _check_bare_except(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查裸 except 语句"""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(Issue(
                        severity=Severity.P0,
                        line=node.lineno,
                        message="使用裸 'except:' 会捕获所有异常，包括 KeyboardInterrupt",
                        rule="bare_except",
                        suggestion="使用具体的异常类型，如 'except ValueError:' 或 'except Exception:'"
                    ))
        return issues
    
    def _check_hardcoded_secrets(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查硬编码密钥"""
        issues = []
        secret_patterns = [
            (r'API_KEY\s*=\s*[\'"]([\w-]+)[\'"]', "API_KEY"),
            (r'API_SECRET\s*=\s*[\'"]([\w-]+)[\'"]', "API_SECRET"),
            (r'PASSWORD\s*=\s*[\'"]([^\'"]+)[\'"]', "PASSWORD"),
            (r'SECRET\s*=\s*[\'"]([\w-]+)[\'"]', "SECRET"),
            (r'TOKEN\s*=\s*[\'"]([\w-]+)[\'"]', "TOKEN"),
        ]
        
        for pattern, name in secret_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append(Issue(
                    severity=Severity.P0,
                    line=line_num,
                    message=f"发现硬编码 {name}，存在安全风险",
                    rule="hardcoded_secrets",
                    suggestion=f"使用环境变量: {name} = os.getenv('{name}')"
                ))
        return issues
    
    def _check_missing_timeout(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查缺少超时设置的 HTTP 请求"""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'urlopen':
                        # 检查是否有 timeout 参数
                        has_timeout = any(
                            kw.arg == 'timeout' for kw in node.keywords
                        )
                        if not has_timeout:
                            issues.append(Issue(
                                severity=Severity.P1,
                                line=node.lineno,
                                message="urllib.request.urlopen 缺少 timeout 参数",
                                rule="missing_timeout",
                                suggestion="添加 timeout 参数，如 timeout=15"
                            ))
        return issues
    
    def _check_inline_imports(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查函数内导入"""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # 检查是否在函数内
                parent = getattr(node, 'parent', None)
                if isinstance(parent, ast.FunctionDef):
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message=f"导入语句在函数 '{parent.name}' 内部",
                        rule="inline_imports",
                        suggestion="将导入语句移到文件顶部"
                    ))
        return issues
    
    def _check_type_hints(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查类型提示"""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查参数类型提示
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != 'self':
                        issues.append(Issue(
                            severity=Severity.P2,
                            line=node.lineno,
                            message=f"函数 '{node.name}' 的参数 '{arg.arg}' 缺少类型提示",
                            rule="missing_type_hints",
                            suggestion=f"添加类型提示，如 {arg.arg}: str"
                        ))
                # 检查返回值类型提示
                if node.returns is None:
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message=f"函数 '{node.name}' 缺少返回值类型提示",
                        rule="missing_type_hints",
                        suggestion="添加返回类型，如 -> Optional[Dict]"
                    ))
        return issues
    
    def _check_long_functions(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查过长函数"""
        issues = []
        lines = code.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno
                if func_lines > 50:
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message=f"函数 '{node.name}' 过长 ({func_lines} 行)",
                        rule="long_functions",
                        suggestion="考虑将函数拆分为多个小函数"
                    ))
        return issues
    
    # ========== P0 安全规则 - 新增 ==========
    
    def _check_sql_injection(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查 SQL 注入风险"""
        issues = []
        
        # 查找字符串格式化或拼接后执行 SQL 的模式
        sql_methods = ['execute', 'executemany', 'executescript']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # 检查是否是 SQL 执行方法
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in sql_methods:
                        # 检查第一个参数
                        if node.args:
                            first_arg = node.args[0]
                            # 检查是否是格式化字符串
                            if isinstance(first_arg, (ast.BinOp, ast.JoinedStr)):
                                issues.append(Issue(
                                    severity=Severity.P0,
                                    line=node.lineno,
                                    message=f"检测到潜在的 SQL 注入风险: {node.func.attr} 使用了字符串拼接",
                                    rule="sql_injection",
                                    suggestion="使用参数化查询，如 cursor.execute('SELECT * FROM t WHERE id = ?', (user_id,))"
                                ))
                            elif isinstance(first_arg, ast.Call):
                                # 检查 .format() 或 % 格式化
                                if (isinstance(first_arg.func, ast.Attribute) and 
                                    first_arg.func.attr in ['format', '__mod__']):
                                    issues.append(Issue(
                                        severity=Severity.P0,
                                        line=node.lineno,
                                        message=f"检测到潜在的 SQL 注入风险: {node.func.attr} 使用了字符串格式化",
                                        rule="sql_injection",
                                        suggestion="使用参数化查询代替字符串格式化"
                                    ))
                            # 检查 f-string
                            elif isinstance(first_arg, ast.JoinedStr):
                                issues.append(Issue(
                                    severity=Severity.P0,
                                    line=node.lineno,
                                    message=f"检测到潜在的 SQL 注入风险: {node.func.attr} 使用了 f-string",
                                    rule="sql_injection",
                                    suggestion="使用参数化查询，避免在 SQL 中使用 f-string"
                                ))
        return issues
    
    def _check_command_injection(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查命令注入风险"""
        issues = []
        
        dangerous_funcs = ['os.system', 'os.popen', 'subprocess.call', 
                          'subprocess.run', 'subprocess.Popen']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Attribute):
                    # 获取完整的函数名
                    if isinstance(node.func.value, ast.Name):
                        func_name = f"{node.func.value.id}.{node.func.attr}"
                elif isinstance(node.func, ast.Name):
                    func_name = node.func.id
                
                if func_name in dangerous_funcs or func_name in ['system', 'popen']:
                    # 检查参数是否包含用户输入
                    if node.args:
                        first_arg = node.args[0]
                        # 检查是否是格式化字符串或拼接
                        if isinstance(first_arg, (ast.BinOp, ast.JoinedStr, ast.Call)):
                            issues.append(Issue(
                                severity=Severity.P0,
                                line=node.lineno,
                                message=f"检测到潜在的命令注入风险: {func_name} 使用了动态字符串",
                                rule="command_injection",
                                suggestion="使用列表传参代替字符串，如 subprocess.run(['ls', '-la'], capture_output=True)"
                            ))
        return issues
    
    def _check_dangerous_functions(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查危险函数使用"""
        issues = []
        
        dangerous = {
            'eval': "eval() 存在任意代码执行风险",
            'exec': "exec() 存在任意代码执行风险",
            'compile': "compile() 可能被用于代码注入",
            '__import__': "__import__() 可能导致不安全的模块加载",
            'pickle.loads': "pickle 反序列化存在远程代码执行风险",
            'pickle.load': "pickle 反序列化存在远程代码执行风险",
            'yaml.load': "yaml.load() 存在代码执行风险，请使用 yaml.safe_load()",
            'marshal.loads': "marshal 反序列化存在安全风险",
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        func_name = f"{node.func.value.id}.{node.func.attr}"
                
                if func_name in dangerous:
                    issues.append(Issue(
                        severity=Severity.P0,
                        line=node.lineno,
                        message=dangerous[func_name],
                        rule="dangerous_functions",
                        suggestion=f"避免使用 {func_name}()，寻找安全的替代方案"
                    ))
        return issues
    
    # ========== P1 可靠性规则 - 新增 ==========
    
    def _check_resource_leaks(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查资源泄漏（数据库连接、锁等）"""
        issues = []
        
        # 检查 acquire 没有对应 release
        acquired_locks = []
        released_locks = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'acquire':
                        acquired_locks.append(node)
                    elif node.func.attr == 'release':
                        released_locks.append(node)
        
        # 简单检查：acquire 数量是否匹配 release 数量
        if len(acquired_locks) > len(released_locks):
            for lock in acquired_locks[len(released_locks):]:
                issues.append(Issue(
                    severity=Severity.P1,
                    line=lock.lineno,
                    message="检测到锁 acquire() 可能没有对应的 release()",
                    rule="resource_leaks",
                    suggestion="使用上下文管理器: with lock:"
                ))
        
        return issues
    
    def _check_unclosed_files(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查未关闭的文件"""
        issues = []
        
        opened_files = []
        closed_files = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # 检查 open() 调用
                if isinstance(node.func, ast.Name) and node.func.id == 'open':
                    opened_files.append(node)
                # 检查 .close() 调用
                elif isinstance(node.func, ast.Attribute) and node.func.attr == 'close':
                    closed_files.append(node)
        
        # 简单检查
        if len(opened_files) > len(closed_files):
            for f in opened_files[len(closed_files):]:
                issues.append(Issue(
                    severity=Severity.P1,
                    line=f.lineno,
                    message="文件打开后可能没有关闭",
                    rule="unclosed_files",
                    suggestion="使用上下文管理器: with open(...) as f:"
                ))
        
        return issues
    
    # ========== P2 质量规则 - 新增 ==========
    
    def _check_unused_variables(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查未使用的变量"""
        issues = []
        
        # 收集所有赋值
        assigned = {}  # name -> node
        used = set()
        
        for node in ast.walk(tree):
            # 赋值
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned[target.id] = target
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    assigned[node.target.id] = node.target
            # 使用
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used.add(node.id)
        
        # 检查未使用的变量（排除 _ 开头的）
        for name, node in assigned.items():
            if name not in used and not name.startswith('_'):
                issues.append(Issue(
                    severity=Severity.P2,
                    line=getattr(node, 'lineno', 0),
                    message=f"变量 '{name}' 被赋值但从未使用",
                    rule="unused_variables",
                    suggestion=f"删除未使用的变量，或使用 '_' 前缀表明有意忽略"
                ))
        
        return issues
    
    def _check_debug_code(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查调试代码"""
        issues = []
        
        # 检查 print 语句
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message="发现 print() 语句，可能是调试代码",
                        rule="debug_code",
                        suggestion="使用 logging 模块代替 print，或在生产代码中移除"
                    ))
            # 检查 pdb
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'pdb':
                        issues.append(Issue(
                            severity=Severity.P1,
                            line=node.lineno,
                            message="发现 pdb 导入，可能是调试代码",
                            rule="debug_code",
                            suggestion="在提交前移除调试代码"
                        ))
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'pdb':
                    issues.append(Issue(
                        severity=Severity.P1,
                        line=node.lineno,
                        message="发现 pdb 导入，可能是调试代码",
                        rule="debug_code",
                        suggestion="在提交前移除调试代码"
                    ))
        
        return issues
    
    def _check_hardcoded_urls(self, tree: ast.AST, code: str) -> List[Issue]:
        """检查硬编码 URL/IP"""
        issues = []
        
        url_pattern = r'https?://[^\s\'"]+'
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = node.value
                # 检查 URL
                if re.search(url_pattern, value):
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message=f"发现硬编码 URL: {value[:50]}...",
                        rule="hardcoded_urls",
                        suggestion="将 URL 提取到配置文件或环境变量"
                    ))
                # 检查 IP
                elif re.match(ip_pattern, value):
                    issues.append(Issue(
                        severity=Severity.P2,
                        line=node.lineno,
                        message=f"发现硬编码 IP 地址: {value}",
                        rule="hardcoded_urls",
                        suggestion="将 IP 地址提取到配置文件"
                    ))
        
        return issues
    
    def generate_report(self, result: AnalysisResult) -> str:
        """生成分析报告"""
        lines = [
            "📊 代码分析报告",
            "=" * 50,
            f"文件: {result.file_path}",
            "",
            "📈 统计信息:",
            f"  函数数量: {result.stats.get('functions', 0)}",
            f"  类数量: {result.stats.get('classes', 0)}",
            f"  导入数量: {result.stats.get('imports', 0)}",
            "",
        ]
        
        if result.issues:
            lines.append("🔍 发现的问题:")
            for severity in [Severity.P0, Severity.P1, Severity.P2, Severity.P3]:
                issues = result.get_by_severity(severity)
                for issue in issues:
                    lines.append(f"  [{severity.value}] 第{issue.line}行: {issue.message}")
                    if issue.suggestion:
                        lines.append(f"      💡 建议: {issue.suggestion}")
        else:
            lines.append("✅ 未发现明显问题")
        
        return '\n'.join(lines)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Analyzer')
    parser.add_argument('file', help='要分析的 Python 文件')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='输出格式')
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(args.file)
    
    if args.format == 'json':
        import json
        data = {
            'file': result.file_path,
            'stats': result.stats,
            'issues': [
                {
                    'severity': i.severity.value,
                    'line': i.line,
                    'message': i.message,
                    'rule': i.rule,
                    'suggestion': i.suggestion
                }
                for i in result.issues
            ]
        }
        print(json.dumps(data, indent=2))
    else:
        print(analyzer.generate_report(result))


if __name__ == '__main__':
    main()
