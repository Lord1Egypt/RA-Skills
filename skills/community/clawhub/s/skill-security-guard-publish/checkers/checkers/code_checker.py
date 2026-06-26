"""
代码检查模块

该模块提供源代码安全性检查功能，包括漏洞扫描、代码质量评估、
安全编码规范检查等。
"""

import ast
import re
from typing import List, Dict, Any, Optional
from pathlib import Path


class CodeChecker:
    """
    代码安全检查器
    
    提供多种代码相关的安全检查功能，包括静态代码分析、
    安全漏洞检测、编码规范检查等。
    """
    
    def __init__(self):
        """初始化代码检查器"""
        # 常见的安全漏洞模式
        self.vulnerability_patterns = {
            'sql_injection': [
                r'cursor\.execute\(.*[\+\%]\s*.*\)',
                r'execute\([^)]*\+[^)]*\)',
                r'".*"\s*\+\s*.*',
                r'%s.*%'  # String formatting with % operator
            ],
            'command_injection': [
                r'os\.system\(',
                r'subprocess\.(call|run|Popen)\([^)]*(shell=True|executable=)[^)]*\)',
                r'exec\(',
                r'eval\(',
                r'compile\([^)]*input[^)]*\)'
            ],
            'path_traversal': [
                r'os\.path\.join\(.*\.\..*\)',
                r'open\([^)]*\+\s*"../"[^)]*\)',
                r'request\.args\[.*\].*os\.path\.join'
            ],
            'xss_vulnerability': [
                r'return.*request\.args\[.*\]',
                r'render_template.*request\.form\[.*\]',
                r'return.*request\.values\[.*\]'
            ],
            'hardcoded_credentials': [
                r'(password|secret|key|token|auth)\s*=\s*["\'][^"\']+["\']',
                r'(PASSWORD|SECRET|KEY|TOKEN|AUTH).*["\'][^"\']+["\']'
            ]
        }
        
        # 危险函数列表
        self.dangerous_functions = [
            'eval', 'exec', 'compile', 'execfile', 'input',
            'open', 'file', 'os.system', 'os.popen', 'subprocess.call',
            'subprocess.Popen', 'subprocess.run', 'pickle.load',
            'pickle.loads', 'yaml.load', 'xml.etree.ElementTree.parse'
        ]
    
    def check_syntax_errors(self, code: str) -> List[Dict[str, Any]]:
        """
        检查代码语法错误
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            List[Dict[str, Any]]: 语法错误列表
        """
        errors = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                'type': 'SyntaxError',
                'line': e.lineno,
                'column': e.offset,
                'message': e.msg,
                'text': e.text
            })
        except Exception as e:
            errors.append({
                'type': 'ParseError',
                'message': str(e)
            })
            
        return errors
    
    def scan_security_vulnerabilities(self, code: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        扫描代码中的安全漏洞
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: 漏洞扫描结果
        """
        vulnerabilities = {vuln_type: [] for vuln_type in self.vulnerability_patterns.keys()}
        
        lines = code.split('\n')
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for i, line in enumerate(lines, 1):
                for pattern in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        vulnerabilities[vuln_type].append({
                            'line_number': i,
                            'code_snippet': line.strip(),
                            'matched_pattern': match.group(),
                            'pattern_type': pattern
                        })
        
        # 过滤掉空的结果
        return {k: v for k, v in vulnerabilities.items() if v}
    
    def find_dangerous_functions(self, code: str) -> List[Dict[str, Any]]:
        """
        查找代码中的危险函数调用
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            List[Dict[str, Any]]: 危险函数调用列表
        """
        dangerous_calls = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = self._get_function_name(node.func)
                    if func_name and any(danger in func_name for danger in self.dangerous_functions):
                        line_no = node.lineno
                        # 获取包含该节点的代码行
                        lines = code.split('\n')
                        if line_no <= len(lines):
                            code_line = lines[line_no - 1].strip()
                        else:
                            code_line = "Line not available"
                            
                        dangerous_calls.append({
                            'function': func_name,
                            'line_number': line_no,
                            'code_snippet': code_line,
                            'node_type': type(node).__name__
                        })
        except SyntaxError:
            # 如果语法错误，使用正则表达式查找
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                for func in self.dangerous_functions:
                    if re.search(r'\b' + re.escape(func) + r'\s*\(', line):
                        dangerous_calls.append({
                            'function': func,
                            'line_number': i,
                            'code_snippet': line.strip(),
                            'node_type': 'RegexMatch'
                        })
        
        return dangerous_calls
    
    def _get_function_name(self, func_node) -> Optional[str]:
        """
        从AST节点获取函数名
        
        Args:
            func_node: AST函数节点
            
        Returns:
            Optional[str]: 函数名
        """
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            attr_chain = []
            current = func_node
            while isinstance(current, ast.Attribute):
                attr_chain.insert(0, current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                attr_chain.insert(0, current.id)
            elif isinstance(current, ast.Constant) and isinstance(current.value, str):
                attr_chain.insert(0, current.value)
            else:
                # 处理更复杂的情况
                return self._get_attribute_name_recursive(func_node)
            return '.'.join(attr_chain)
        return None
    
    def _get_attribute_name_recursive(self, node) -> Optional[str]:
        """
        递归获取属性名
        
        Args:
            node: AST节点
            
        Returns:
            Optional[str]: 属性名
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            left = self._get_attribute_name_recursive(node.value)
            if left:
                return f"{left}.{node.attr}"
        return None
    
    def check_code_quality(self, code: str) -> Dict[str, Any]:
        """
        检查代码质量
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            Dict[str, Any]: 代码质量检查结果
        """
        quality_issues = {
            'line_count': 0,
            'long_lines': [],  # 超过80字符的行
            'complexity_score': 0,  # 复杂度评分
            'missing_docstrings': [],  # 缺少文档字符串的函数/类
            'naming_issues': [],  # 命名规范问题
            'unused_imports': []  # 未使用的导入
        }
        
        lines = code.split('\n')
        quality_issues['line_count'] = len([line for line in lines if line.strip()])
        
        # 检查过长的行
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                quality_issues['long_lines'].append({
                    'line_number': i,
                    'length': len(line),
                    'content': line.strip()
                })
        
        try:
            tree = ast.parse(code)
            
            # 计算复杂度（简单版本：基于控制流语句数量）
            complexity_counter = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, 
                                   ast.FunctionDef, ast.ClassDef)):
                    complexity_counter += 1
            quality_issues['complexity_score'] = complexity_counter
            
            # 检查缺少文档字符串
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        quality_issues['missing_docstrings'].append({
                            'type': type(node).__name__,
                            'name': getattr(node, 'name', 'module'),
                            'line_number': node.lineno
                        })
            
            # 检查命名规范问题
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    name = node.id
                    if not self._is_valid_naming(name):
                        quality_issues['naming_issues'].append({
                            'name': name,
                            'line_number': node.lineno,
                            'issue': 'Invalid naming convention'
                        })
                elif isinstance(node, ast.FunctionDef):
                    if not self._is_valid_naming(node.name):
                        quality_issues['naming_issues'].append({
                            'name': node.name,
                            'line_number': node.lineno,
                            'issue': 'Function name does not follow convention'
                        })
                elif isinstance(node, ast.ClassDef):
                    if not self._is_valid_class_naming(node.name):
                        quality_issues['naming_issues'].append({
                            'name': node.name,
                            'line_number': node.lineno,
                            'issue': 'Class name does not follow convention'
                        })
                        
        except SyntaxError:
            pass  # 如果语法错误，则跳过AST分析
        
        return quality_issues
    
    def _is_valid_naming(self, name: str) -> bool:
        """
        检查变量/函数命名是否符合规范
        
        Args:
            name (str): 名称
            
        Returns:
            bool: 是否符合规范
        """
        # 检查是否符合snake_case或单个小写字母
        import keyword
        if keyword.iskeyword(name):
            return False
        return re.match(r'^[a-z_][a-z0-9_]*$', name) is not None
    
    def _is_valid_class_naming(self, name: str) -> bool:
        """
        检查类命名是否符合规范
        
        Args:
            name (str): 名称
            
        Returns:
            bool: 是否符合规范
        """
        # 检查是否符合PascalCase
        import keyword
        if keyword.iskeyword(name):
            return False
        return re.match(r'^[A-Z][a-zA-Z0-9]*$', name) is not None
    
    def analyze_imports(self, code: str) -> Dict[str, List[str]]:
        """
        分析代码导入情况
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            Dict[str, List[str]]: 导入分析结果
        """
        imports = {
            'standard_library': [],
            'third_party': [],
            'local': [],
            'suspicious': []  # 潜在危险的导入
        }
        
        suspicious_packages = [
            'os', 'subprocess', 'sys', 'importlib', 'imp', 
            'compileall', 'py_compile', 'pickle', 'marshal',
            'shelve', 'dbm', 'sqlite3', 'mysql', 'psycopg2'
        ]
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name
                        if any(susp in module_name for susp in suspicious_packages):
                            imports['suspicious'].append(module_name)
                        else:
                            imports['third_party'].append(module_name)
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module or ''
                    if any(susp in module_name for susp in suspicious_packages):
                        imports['suspicious'].append(module_name)
                    elif module_name and not module_name.startswith('.'):
                        imports['third_party'].append(module_name)
                    elif module_name and module_name.startswith('.'):
                        imports['local'].append(module_name)
        except SyntaxError:
            # 如果语法错误，使用正则表达式查找导入
            import_lines = re.findall(r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)', code)
            from_imports = re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import', code)
            
            for imp in import_lines + from_imports:
                if any(susp in imp for susp in suspicious_packages):
                    imports['suspicious'].append(imp)
                else:
                    imports['third_party'].append(imp)
        
        # 去重
        for key in imports:
            imports[key] = list(set(imports[key]))
            
        return imports
    
    def check_hardcoded_secrets(self, code: str) -> List[Dict[str, Any]]:
        """
        检查代码中硬编码的敏感信息
        
        Args:
            code (str): 源代码字符串
            
        Returns:
            List[Dict[str, Any]]: 硬编码敏感信息列表
        """
        secrets = []
        
        lines = code.split('\n')
        
        # 正则模式匹配各种敏感信息
        patterns = [
            (r'(?:password|secret|key|token|auth|api_key|client_secret)\s*[:=]\s*[\'"][^\'"]{5,}[\'"]', 'Potential password/api key'),
            (r'(?:password|secret|key|token|auth|api_key|client_secret)\s*[:=]\s*["\'][A-Za-z0-9+/]{20,}["\']', 'Base64 encoded secret'),
            (r'Authorization\s*:\s*Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', 'Hardcoded auth token'),
            (r'"[A-Za-z0-9]{32,}"', 'Long string that might be a key'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, description in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    secrets.append({
                        'line_number': i,
                        'type': description,
                        'value': match.group(),
                        'context': line.strip()
                    })
        
        return secrets
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """
        扫描整个文件
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            Dict[str, Any]: 扫描结果
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
                
            return {
                'syntax_errors': self.check_syntax_errors(code),
                'vulnerabilities': self.scan_security_vulnerabilities(code),
                'dangerous_functions': self.find_dangerous_functions(code),
                'code_quality': self.check_code_quality(code),
                'imports': self.analyze_imports(code),
                'hardcoded_secrets': self.check_hardcoded_secrets(code)
            }
        except Exception as e:
            return {'error': str(e)}