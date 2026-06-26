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
    
    def __init__(self):
        """初始化敏感信息检查器"""
        # 硬编码密钥的常见模式
        self.key_patterns = [
            re.compile(r'(?i)(api[_-]?key|secret|token|password|pwd|auth)[\'"]?\s*[=:]\s*[\'"][A-Za-z0-9_\-+=/]{10,}[\'"]'),
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
            'auth-token', 'authtoken'
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
        findings = []
        
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
                    if re.search(rf'[\'"]?\w*[\'"]?\s*[=:].*[{keyword}]', lower_line) or \
                       re.search(rf'{keyword}\s*[=:].*[\'"][^\'"]{{10,}}[\'"]', lower_line):
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
        if not path.is_dir():
            return []
        
        findings = []
        
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


def main():
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