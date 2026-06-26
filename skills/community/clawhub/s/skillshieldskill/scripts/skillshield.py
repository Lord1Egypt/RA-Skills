#!/usr/bin/env python3
"""
SkillShield - AI Agent Skill Security Scanner
Detects malicious skills, analyzes permissions, and provides trust ratings

Version: 1.0.0
Author: OpenClaw Community
License: MIT
"""

import sys
import os
import re
import json
import argparse
import hashlib
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class SkillScanner:
    """Main skill scanner class with enhanced security detection"""
    
    # Sensitive file patterns
    SENSITIVE_FILES = [
        (r'\.env', '读取 .env 文件', 'high'),
        (r'\.bashrc', '读取 .bashrc', 'medium'),
        (r'\.zshrc', '读取 .zshrc', 'medium'),
        (r'\.ssh[/\\]', '访问 SSH 目录', 'critical'),
        (r'\.aws[/\\]', '访问 AWS 凭证', 'critical'),
        (r'\.config[/\\]', '读取配置文件', 'low'),
        (r'password', '访问密码相关文件', 'high'),
        (r'credential', '访问凭证文件', 'critical'),
        (r'token', '访问 token 文件', 'critical'),
        (r'api_key', '访问 API key', 'critical'),
        (r'secret', '访问密钥文件', 'critical'),
        (r'cookie', '访问 cookie 文件', 'high'),
        (r'\.gitconfig', '读取 git 配置', 'medium'),
        (r'\.docker', '访问 Docker 配置', 'medium'),
    ]
    
    # System command patterns
    DANGEROUS_COMMANDS = [
        (r'os\.system\s*\(', '执行系统命令 (os.system)', 'critical'),
        (r'subprocess\.(call|run|Popen)', '执行子进程 (subprocess)', 'high'),
        (r'subprocess\.check_output', '执行子进程并获取输出', 'high'),
        (r'exec\s*\(', '动态执行代码 (exec)', 'critical'),
        (r'eval\s*\(', '动态执行代码 (eval)', 'critical'),
        (r'__import__\s*\(', '动态导入模块', 'medium'),
        (r'compile\s*\(', '编译代码', 'medium'),
        (r'importlib', '动态导入模块', 'medium'),
    ]
    
    # Suspicious patterns
    SUSPICIOUS_PATTERNS = [
        (r'base64\.(b64encode|b64decode)', 'Base64 编码/解码', 'medium'),
        (r'encrypt|decrypt', '加密/解密操作', 'low'),
        (r'keylogger|keyboard|input', '键盘记录相关', 'critical'),
        (r'screenshot', '屏幕截图', 'high'),
        (r'webhook', 'Webhook 调用', 'low'),
        (r'socket\.', '网络 socket 操作', 'medium'),
        (r'ftplib|smtplib', 'FTP/SMTP 协议', 'medium'),
        (r'tempfile\.(mkdtemp|mkstemp)', '创建临时文件', 'low'),
    ]
    
    # Suspicious domains
    SUSPICIOUS_DOMAINS = [
        'webhook', 'pastebin', 'requestbin', 'hook', 
        'ngrok', 'burpcollaborator', 'interactsh'
    ]
    
    def __init__(self, rules_dir: str = None):
        self.rules_dir = rules_dir or os.path.join(os.path.dirname(__file__), '..', 'rules')
        self.warnings = []
        self.permissions = {
            'files': {'read': set(), 'write': set(), 'delete': set()},
            'network': {'urls': set(), 'domains': set()},
            'system': {'commands': set(), 'imports': set()},
            'data': {'env_vars': set(), 'credentials': set()}
        }
        self.file_hashes = {}
    
    def scan(self, skill_path: str, deep_scan: bool = False) -> Dict:
        """Scan a skill directory or file with enhanced detection"""
        self.warnings = []
        self.permissions = {
            'files': {'read': set(), 'write': set(), 'delete': set()},
            'network': {'urls': set(), 'domains': set()},
            'system': {'commands': set(), 'imports': set()},
            'data': {'env_vars': set(), 'credentials': set()}
        }
        self.file_hashes = {}
        
        if not os.path.exists(skill_path):
            return {'error': f'Path not found: {skill_path}'}
        
        # Get all files to scan
        files_to_scan = self._get_files(skill_path)
        
        if not files_to_scan:
            return {'error': f'No scannable files found in: {skill_path}'}
        
        # Scan each file
        for filepath in files_to_scan:
            self._scan_file(filepath, deep_scan)
        
        # Check for hidden malicious files
        if deep_scan:
            self._deep_scan(skill_path)
        
        # Calculate trust rating
        rating = self._calculate_rating()
        
        return {
            'skill_path': skill_path,
            'scan_time': datetime.now().isoformat(),
            'trust_rating': rating['grade'],
            'score': rating['score'],
            'risk_level': rating['risk_level'],
            'warnings': self.warnings,
            'permissions': self._serialize_permissions(),
            'files_scanned': len(files_to_scan),
            'file_hashes': self.file_hashes,
            'summary': self._generate_summary(),
            'recommendations': self._generate_recommendations()
        }
    
    def _get_files(self, path: str) -> List[str]:
        """Get all relevant files to scan"""
        files = []
        scannable_extensions = ('.py', '.js', '.ts', '.md', '.sh', 
                                '.json', '.yaml', '.yml', '.toml', '.txt')
        
        if os.path.isfile(path):
            if path.endswith(scannable_extensions):
                files.append(path)
        else:
            for root, dirs, filenames in os.walk(path):
                # Skip hidden directories and common non-source directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d not in ['node_modules', '__pycache__', 'venv', '.git']]
                
                for filename in filenames:
                    if filename.endswith(scannable_extensions):
                        files.append(os.path.join(root, filename))
        
        return files
    
    def _scan_file(self, filepath: str, deep_scan: bool = False):
        """Scan a single file with comprehensive checks"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.warnings.append({
                'type': 'file_error',
                'severity': 'low',
                'description': f'无法读取文件: {str(e)}',
                'file': os.path.basename(filepath)
            })
            return
        
        filename = os.path.basename(filepath)
        
        # Calculate file hash for integrity checking
        self.file_hashes[filename] = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Run all security checks
        self._check_sensitive_files(content, filename)
        self._check_network_requests(content, filename)
        self._check_system_commands(content, filename)
        self._check_suspicious_patterns(content, filename)
        self._check_data_exfiltration(content, filename)
        self._check_imports(content, filename)
        
        if deep_scan:
            self._check_obfuscation(content, filename)
    
    def _check_sensitive_files(self, content: str, filename: str):
        """Check for access to sensitive files"""
        for pattern, desc, severity in self.SENSITIVE_FILES:
            if re.search(pattern, content, re.IGNORECASE):
                self._add_warning('sensitive_file', severity, desc, filename)
                self.permissions['files']['read'].add(pattern)
    
    def _check_network_requests(self, content: str, filename: str):
        """Check for network requests with enhanced detection"""
        # Find all URLs
        url_pattern = r'https?://[^\s\'"\)\>]+'
        matches = re.findall(url_pattern, content)
        
        for url in matches:
            self.permissions['network']['urls'].add(url)
            
            # Extract domain
            domain_match = re.search(r'https?://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1)
                self.permissions['network']['domains'].add(domain)
                
                # Check for suspicious domains
                for susp in self.SUSPICIOUS_DOMAINS:
                    if susp in domain.lower():
                        self._add_warning('suspicious_network', 'high', 
                                        f'数据可能发送到外部服务: {domain}', filename)
        
        # Check for request libraries
        request_patterns = [
            r'requests\.(get|post|put|delete|patch)',
            r'urllib\.(request|urlopen)',
            r'http\.client',
            r'fetch\(',
            r'axios\.(get|post)',
            r'curl\s',
            r'wget\s',
        ]
        
        for pattern in request_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.permissions['system']['commands'].add(pattern)
    
    def _check_system_commands(self, content: str, filename: str):
        """Check for system command execution"""
        for pattern, desc, severity in self.DANGEROUS_COMMANDS:
            if re.search(pattern, content):
                self._add_warning('system_command', severity, desc, filename)
    
    def _check_suspicious_patterns(self, content: str, filename: str):
        """Check for other suspicious patterns"""
        for pattern, desc, severity in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                self._add_warning('suspicious_pattern', severity, desc, filename)
    
    def _check_data_exfiltration(self, content: str, filename: str):
        """Check for data exfiltration patterns"""
        # Check for reading env vars and sending them
        has_env_read = re.search(r'os\.environ|getenv|os\.getenv', content)
        has_http_send = re.search(r'requests\.(post|put|patch)|urllib', content)
        has_json_encode = re.search(r'json\.dumps', content)
        
        if has_env_read and has_http_send:
            severity = 'critical' if has_json_encode else 'high'
            self._add_warning('data_exfiltration', severity, 
                            '可能读取环境变量并发送到外部', filename)
    
    def _check_imports(self, content: str, filename: str):
        """Check imported modules"""
        import_patterns = [
            r'^import\s+(\w+)',
            r'^from\s+(\w+)',
            r'require\([\'"]([^\'"]+)[\'"]',
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                self.permissions['system']['imports'].add(match)
    
    def _check_obfuscation(self, content: str, filename: str):
        """Check for code obfuscation techniques"""
        # Check for excessive base64
        base64_count = len(re.findall(r'base64', content, re.IGNORECASE))
        if base64_count > 5:
            self._add_warning('obfuscation', 'medium',
                            f'检测到多次 Base64 编码 ({base64_count} 次)', filename)
        
        # Check for hex encoding
        hex_pattern = r'\\x[0-9a-fA-F]{2}'
        hex_matches = len(re.findall(hex_pattern, content))
        if hex_matches > 20:
            self._add_warning('obfuscation', 'medium',
                            f'检测到十六进制编码 ({hex_matches} 处)', filename)
    
    def _deep_scan(self, skill_path: str):
        """Perform deep scan for hidden threats"""
        # Check for hidden files
        for root, dirs, files in os.walk(skill_path):
            for filename in files:
                if filename.startswith('.'):
                    self._add_warning('hidden_file', 'low',
                                    f'发现隐藏文件: {filename}', '')
    
    def _add_warning(self, warning_type: str, severity: str, 
                    description: str, filename: str):
        """Add a warning with deduplication"""
        warning = {
            'type': warning_type,
            'severity': severity,
            'description': description,
            'file': filename
        }
        
        # Simple deduplication
        if warning not in self.warnings:
            self.warnings.append(warning)
    
    def _calculate_rating(self) -> Dict:
        """Calculate trust rating with enhanced algorithm"""
        score = 100
        
        severity_weights = {
            'critical': 25,
            'high': 10,
            'medium': 5,
            'low': 2,
            'info': 0
        }
        
        critical_count = 0
        high_count = 0
        
        for warning in self.warnings:
            severity = warning.get('severity', 'medium')
            score -= severity_weights.get(severity, 5)
            
            if severity == 'critical':
                critical_count += 1
            elif severity == 'high':
                high_count += 1
        
        # Additional penalties
        if critical_count >= 2:
            score -= 20  # Multiple critical issues
        if high_count >= 3:
            score -= 10  # Multiple high issues
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        # Convert to letter grade
        if score >= 95:
            grade = 'A+'
            risk_level = '极低'
        elif score >= 90:
            grade = 'A'
            risk_level = '低'
        elif score >= 80:
            grade = 'B'
            risk_level = '中低'
        elif score >= 70:
            grade = 'C'
            risk_level = '中等'
        elif score >= 60:
            grade = 'D'
            risk_level = '高'
        else:
            grade = 'F'
            risk_level = '极高'
        
        return {
            'score': score, 
            'grade': grade,
            'risk_level': risk_level,
            'critical_count': critical_count,
            'high_count': high_count
        }
    
    def _serialize_permissions(self) -> Dict:
        """Convert sets to lists for JSON serialization"""
        return {
            'files': {
                'read': list(self.permissions['files']['read'])[:10],
                'write': list(self.permissions['files']['write'])[:5],
                'delete': list(self.permissions['files']['delete'])[:5]
            },
            'network': {
                'urls': list(self.permissions['network']['urls'])[:10],
                'domains': list(self.permissions['network']['domains'])[:10]
            },
            'system': {
                'commands': list(self.permissions['system']['commands'])[:10],
                'imports': list(self.permissions['system']['imports'])[:20]
            },
            'data': {
                'env_vars': list(self.permissions['data']['env_vars']),
                'credentials': list(self.permissions['data']['credentials'])
            }
        }
    
    def _generate_summary(self) -> str:
        """Generate human-readable summary"""
        rating = self._calculate_rating()
        
        if rating['grade'] in ['A+', 'A']:
            return "此 skill 看起来非常安全，没有发现明显风险，可以放心使用。"
        elif rating['grade'] == 'B':
            return "此 skill 总体可信，有一些需要注意的权限请求，建议审查后使用。"
        elif rating['grade'] == 'C':
            return "此 skill 有中等风险，请仔细审查权限和警告，确认安全后再安装。"
        elif rating['grade'] == 'D':
            return "此 skill 有高风险，建议谨慎使用或避免安装，除非完全理解其行为。"
        else:
            return "此 skill 检测到严重安全风险，强烈建议不要安装！"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        rating = self._calculate_rating()
        
        if rating['critical_count'] > 0:
            recommendations.append("立即审查所有 CRITICAL 级别的警告")
        
        if rating['high_count'] > 0:
            recommendations.append("仔细评估 HIGH 级别的安全风险")
        
        if self.permissions['network']['domains']:
            domains = list(self.permissions['network']['domains'])
            if len(domains) > 5:
                recommendations.append(f"技能需要访问 {len(domains)} 个外部域名，确认都是必需的")
        
        if 'subprocess' in str(self.permissions['system']['commands']):
            recommendations.append("技能使用系统命令执行，确认来源可信")
        
        if not recommendations:
            recommendations.append("没有发现特别的安全问题")
        
        return recommendations


def format_report(result: Dict, verbose: bool = False) -> str:
    """Format scan result as human-readable report"""
    lines = []
    
    # Header
    lines.append("\n" + "═" * 65)
    lines.append("🛡️ SkillShield 安全扫描报告")
    lines.append("═" * 65)
    
    # Basic info
    lines.append(f"\n📦 Skill 路径: {result.get('skill_path', 'Unknown')}")
    lines.append(f"📅 扫描时间: {result.get('scan_time', 'Unknown')[:19]}")
    lines.append(f"📁 扫描文件: {result.get('files_scanned', 0)} 个")
    
    # Rating
    rating = result.get('trust_rating', 'N/A')
    score = result.get('score', 0)
    risk_level = result.get('risk_level', '未知')
    
    rating_emoji = {
        'A+': '🟢', 'A': '🟢',
        'B': '🟡',
        'C': '🟠',
        'D': '🔴',
        'F': '⛔'
    }.get(rating, '⚪')
    
    lines.append(f"\n📊 信任评级: {rating_emoji} {rating} (得分: {score}/100)")
    lines.append(f"⚡ 风险等级: {risk_level}")
    
    # Warnings
    warnings = result.get('warnings', [])
    if warnings:
        lines.append(f"\n⚠️  警告 ({len(warnings)} 个):")
        
        severity_order = ['critical', 'high', 'medium', 'low', 'info']
        severity_emoji = {
            'critical': '⛔', 'high': '🔴',
            'medium': '🟠', 'low': '🟡', 'info': '🔵'
        }
        
        for severity in severity_order:
            severity_warnings = [w for w in warnings if w.get('severity') == severity]
            for warning in severity_warnings:
                emoji = severity_emoji.get(severity, '⚪')
                desc = warning.get('description', 'Unknown')
                file = warning.get('file', 'Unknown')
                lines.append(f"   {emoji} [{severity.upper()}] {desc}")
                if verbose and file:
                    lines.append(f"      📄 文件: {file}")
    else:
        lines.append("\n✅ 无警告 - 未发现明显安全问题")
    
    # Permissions
    permissions = result.get('permissions', {})
    lines.append("\n📋 权限清单:")
    
    network_domains = permissions.get('network', {}).get('domains', [])
    if network_domains:
        lines.append("   🌐 网络访问:")
        for domain in network_domains[:5]:
            lines.append(f"      - {domain}")
        if len(network_domains) > 5:
            lines.append(f"      ... 还有 {len(network_domains) - 5} 个域名")
    
    files_read = permissions.get('files', {}).get('read', [])
    if files_read:
        lines.append("   📁 文件访问:")
        for pattern in files_read[:5]:
            lines.append(f"      - {pattern}")
    
    imports = permissions.get('system', {}).get('imports', [])
    if imports:
        lines.append("   📦 导入模块:")
        import_list = ', '.join(imports[:10])
        lines.append(f"      {import_list}")
        if len(imports) > 10:
            lines.append(f"      ... 还有 {len(imports) - 10} 个")
    
    # Recommendations
    recommendations = result.get('recommendations', [])
    if recommendations:
        lines.append(f"\n💡 建议:")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"   {i}. {rec}")
    
    # Summary
    lines.append(f"\n📝 总结:")
    lines.append(f"   {result.get('summary', '无法生成建议')}")
    
    lines.append("\n" + "═" * 65)
    lines.append("🛡️ SkillShield - 保护 Agent 生态安全")
    lines.append("═" * 65)
    
    return "\n".join(lines)


def verify_signature(skill_path: str) -> Dict:
    """Verify skill signature (placeholder for future implementation)"""
    # This would integrate with GPG or similar signing system
    return {
        'verified': False,
        'message': '签名验证功能需要额外的加密库支持，将在后续版本实现',
        'suggestion': '目前请通过 GitHub 等可信渠道下载 skill，并检查作者身份'
    }


def main():
    parser = argparse.ArgumentParser(
        description='SkillShield - AI Agent Skill Security Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 skillshield.py scan ./skill/           # 扫描 skill
  python3 skillshield.py scan ./skill -v         # 详细输出
  python3 skillshield.py scan ./skill --deep     # 深度扫描
  python3 skillshield.py scan ./skill -f json    # JSON 格式
  python3 skillshield.py verify ./skill/         # 验证签名
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='扫描 skill')
    scan_parser.add_argument('path', help='Skill 路径或 GitHub URL')
    scan_parser.add_argument('-v', '--verbose', action='store_true',
                            help='详细输出')
    scan_parser.add_argument('-f', '--format', choices=['text', 'json'],
                            default='text', help='输出格式')
    scan_parser.add_argument('--deep', action='store_true',
                            help='深度扫描（较慢但更彻底）')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='验证签名')
    verify_parser.add_argument('path', help='Skill 路径')
    verify_parser.add_argument('--check-author', action='store_true',
                              help='检查作者身份')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='显示版本')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'version':
        print("SkillShield v1.0.0")
        print("AI Agent Skill Security Scanner")
        print("https://github.com/openclaw/skillshield")
        sys.exit(0)
    
    scanner = SkillScanner()
    
    if args.command == 'scan':
        # Handle GitHub URLs
        path = args.path
        if path.startswith('https://github.com/'):
            print(f"📥 正在从 GitHub 下载: {path}")
            print("   (注意: 从 URL 下载功能开发中，请先手动克隆)")
            print(f"   建议运行: git clone {path} /tmp/skill && python3 skillshield.py scan /tmp/skill")
            sys.exit(1)
        
        result = scanner.scan(path, deep_scan=args.deep)
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
            sys.exit(1)
        
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_report(result, args.verbose))
        
        # Exit with error code for malicious skills
        if result['trust_rating'] == 'F':
            sys.exit(2)
    
    elif args.command == 'verify':
        result = verify_signature(args.path)
        print(f"\n🔍 签名验证")
        print(f"   状态: {'✅ 已验证' if result['verified'] else '❌ 未验证'}")
        print(f"   信息: {result['message']}")
        if 'suggestion' in result:
            print(f"\n💡 {result['suggestion']}")


if __name__ == '__main__':
    main()
