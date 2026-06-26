"""
敏感信息检查器
用于检测代码中的硬编码密钥、密码、Token等敏感信息
以及环境变量读取相关的安全问题
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path


class SensitiveChecker:
    """
    敏感信息检查器类
    检测代码中可能存在的安全风险，如硬编码密钥、密码、Token等
    """
    
    def __init__(self) -> None:
        """初始化敏感信息检查器"""
        # 硬编码密钥的常见模式
        self.key_patterns = [
            re.compile(r'(?i)(api[_-]?key|secret|token|password|pwd|auth|api_key|client_secret)[\'"]?\s*[=:]\s*[\'"][A-Za-z0-9_\-+=/]{10,}[\'"]'),
            re.compile(r'(?i)(access[_-]?key|client[_-]?secret|private[_-]?key)[\'"]?\s*[=:]\s*[\'"][^\'"]{10,}[\'"]'),
            re.compile(r'[\'"][A-Za-z0-9]{32,}[\'"].*(?i)(key|token|secret)'),
        ]
        
        # 常见的敏感词
        self.sensitive_keywords = [
            'password', 'passwd', 'pwd', 'secret', 'token', 
            'api_key', 'api-key', 'apikey', 'access_key', 
            'access-key', 'accesskey', 'client_secret',
            'client-secret', 'clientsecret', 'private_key',
            'private-key', 'privatekey', 'auth_token',
            'auth-token', 'authtoken', 'username', 'user',
            'login', 'credential', 'cert', 'certificate'
        ]
        
        # 环境变量读取模式
        self.env_read_patterns = [
            re.compile(r'os\.getenv\([\'"][A-Z_][A-Z0-9_]*[\'"]\)'),
            re.compile(r'os\.environ\.get\([\'"][A-Z_][A-Z0-9_]*[\'"]\)'),
            re.compile(r'os\.environ\[["\'][A-Z_][A-Z0-9_]*["\']\]'),
            re.compile(r'config\.[a-zA-Z_][a-zA-Z0-9_]*'),
            re.compile(r'env\([\'"][A-Z_][A-Z0-9_]*[\'"]\)')  # 如 Rust 的 env! 宏
        ]

    def check_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        检查单个文件中的敏感信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            检测到的敏感信息列表
        """
        path = Path(file_path)
        if not path.exists():
            error_msg = f"错误：找不到文件 {file_path}\n"
            error_msg += "请检查文件路径是否正确，确保文件存在且可访问。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认文件路径拼写正确\n"
            error_msg += "- 检查文件是否确实存在于指定位置\n"
            error_msg += "- 验证是否有足够的权限访问该文件\n"
            print(error_msg)
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except UnicodeDecodeError:
                error_msg = f"错误：无法解码文件 {file_path}，可能是二进制文件或编码问题\n"
                error_msg += "解决方案：\n"
                error_msg += "- 确认文件是文本文件而非二进制文件\n"
                error_msg += "- 检查文件编码格式是否支持\n"
                error_msg += "- 验证文件是否损坏\n"
                print(error_msg)
                return []
        except FileNotFoundError:
            error_msg = f"错误：找不到文件 {file_path}\n"
            error_msg += "请检查文件路径是否正确，确保文件存在且可访问。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认文件路径拼写正确\n"
            error_msg += "- 检查文件是否确实存在于指定位置\n"
            error_msg += "- 验证是否有足够的权限访问该文件\n"
            print(error_msg)
            return []
        except PermissionError:
            error_msg = f"错误：没有权限读取文件 {file_path}\n"
            error_msg += "请检查文件权限设置。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认对文件具有读取权限\n"
            error_msg += "- 联系管理员获取相应权限\n"
            print(error_msg)
            return []
        except Exception as e:
            error_msg = f"读取文件时发生错误: {str(e)}\n"
            error_msg += f"文件路径: {file_path}\n"
            error_msg += "这可能是因为文件损坏、权限问题或其他I/O错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查文件是否损坏\n"
            error_msg += "- 验证磁盘空间是否充足\n"
            error_msg += "- 确认文件编码格式是否为UTF-8\n"
            print(error_msg)
            return []
                
        return self.check_content(content, file_path)

    def check_content(self, content: str, file_path: str = "") -> List[Dict[str, str]]:
        """
        检查内容中的敏感信息
        
        Args:
            content: 要检查的内容
            file_path: 文件路径（可选，用于报告）
            
        Returns:
            检测到的敏感信息列表
        """
        findings: List[Dict[str, str]] = []
        
        # 按行分割内容以便定位
        lines = content.split('\n')
        
        # 检查硬编码密钥模式
        for i, line in enumerate(lines, 1):
            for pattern in self.key_patterns:
                matches = pattern.finditer(line)
                for match in matches:
                    findings.append({
                        'type': 'hardcoded_credential',
                        'line': str(i),
                        'column': str(match.start() + 1),
                        'message': f'发现硬编码的敏感信息: {match.group(0)[:50]}...',
                        'severity': 'high',
                        'file': file_path
                    })
            
            # 检查敏感关键词
            lower_line = line.lower()
            for keyword in self.sensitive_keywords:
                if keyword in lower_line:
                    # 检查是否是赋值操作
                    if re.search(rf'[\'"]?\w*[\'"]?\s*[=:].*{re.escape(keyword)}', lower_line) or \
                       re.search(rf'{re.escape(keyword)}\s*[=:].*[\'"][^\'"]{{10,}}[\'"]', lower_line):
                        findings.append({
                            'type': 'potential_hardcoded_credential',
                            'line': str(i),
                            'column': str(lower_line.find(keyword) + 1),
                            'message': f'发现潜在的硬编码敏感信息: {keyword}',
                            'severity': 'medium',
                            'file': file_path
                        })
        
        # 检查环境变量读取
        for i, line in enumerate(lines, 1):
            for pattern in self.env_read_patterns:
                matches = pattern.finditer(line)
                for match in matches:
                    findings.append({
                        'type': 'environment_variable_access',
                        'line': str(i),
                        'column': str(match.start() + 1),
                        'message': f'发现环境变量读取: {match.group(0)}',
                        'severity': 'low',  # 环境变量读取本身不一定有害，但需要检查
                        'file': file_path
                    })
        
        return findings

    def check_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """
        检查目录下所有文件的敏感信息
        
        Args:
            directory_path: 目录路径
            
        Returns:
            检测到的敏感信息列表
        """
        path = Path(directory_path)
        if not path.exists():
            error_msg = f"错误：找不到目录 {directory_path}\n"
            error_msg += "请检查目录路径是否正确，确保目录存在且可访问。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认目录路径拼写正确\n"
            error_msg += "- 检查目录是否确实存在于指定位置\n"
            error_msg += "- 验证是否有足够的权限访问该目录\n"
            print(error_msg)
            return []
        
        if not path.is_dir():
            error_msg = f"错误：{directory_path} 不是一个目录\n"
            error_msg += "请确保提供的是一个有效的目录路径。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认提供的路径是一个目录而不是文件\n"
            error_msg += "- 检查路径是否正确\n"
            print(error_msg)
            return []
        
        findings: List[Dict[str, str]] = []
        
        try:
            # 检查常见的源代码文件扩展名
            extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb', '.php', '.html', '.css', '.yaml', '.yml', '.json', '.xml']
            
            for ext in extensions:
                for file_path in path.rglob(f'*{ext}'):
                    findings.extend(self.check_file(str(file_path)))
            
            # 检查配置文件
            config_files = ['*.env', '*.ini', '*.cfg', '*.conf', 'config.*']
            for pattern in config_files:
                for file_path in path.rglob(pattern):
                    findings.extend(self.check_file(str(file_path)))
        except PermissionError:
            error_msg = f"警告：没有权限访问目录 {directory_path} 中的部分文件\n"
            error_msg += "这可能会影响扫描的完整性。\n"
            print(error_msg)
        except Exception as e:
            error_msg = f"扫描目录时发生错误: {str(e)}\n"
            error_msg += f"目录路径: {directory_path}\n"
            error_msg += "这可能是因为目录损坏、权限问题或其他I/O错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查目录是否损坏\n"
            error_msg += "- 验证是否有足够的权限访问该目录\n"
            error_msg += "- 确认磁盘空间是否充足\n"
            print(error_msg)
        
        return findings

    def generate_report(self, findings: List[Dict[str, str]]) -> str:
        """
        生成检查报告
        
        Args:
            findings: 检测结果列表
            
        Returns:
            格式化的报告字符串
        """
        if not findings:
            return "✅ 未发现敏感信息"
        
        report = "⚠️ 检测到潜在的安全风险:\n\n"
        
        severity_order = {'high': 1, 'medium': 2, 'low': 3}
        
        # 按严重程度排序
        sorted_findings = sorted(findings, key=lambda x: severity_order.get(x['severity'], 99))
        
        for finding in sorted_findings:
            report += f"📁 文件: {finding['file']}\n"
            report += f";line {finding['line']}, col {finding['column']}\n"
            report += f"🔍 类型: {finding['type']}\n"
            report += f"⚠️ 信息: {finding['message']}\n"
            report += f"🔴 严重程度: {finding['severity']}\n"
            report += "-" * 50 + "\n"
        
        return report


def main() -> None:
    """
    主函数，用于测试敏感信息检查器
    """
    checker = SensitiveChecker()
    
    # 示例用法
    test_code = '''
    api_key = "sk-1234567890abcdef"
    password = "mySecretPassword123"
    secret_token = "ghp_AbcDefGhiJklMnoPqrStuVwxYz"
    db_password = os.getenv('DB_PASSWORD')
    '''
    
    findings = checker.check_content(test_code, "test.py")
    print(checker.generate_report(findings))


if __name__ == "__main__":
    main()