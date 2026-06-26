#!/usr/bin/env python3
"""
Skill 安全检查工具
扫描已安装的 skill 是否存在潜在风险
"""

import os
import re
import json
from pathlib import Path

class SkillSecurityScanner:
    """Skill 安全扫描器"""
    
    # 危险命令模式
    DANGEROUS_PATTERNS = [
        (r'rm\s+-rf\s+/', '危险: 递归删除根目录'),
        (r'rm\s+-rf\s+~', '危险: 递归删除用户目录'),
        (r'>\s*/dev/sda', '危险: 直接写入磁盘'),
        (r':\(\)\{\s*:\|:&\s*\};:', '危险: Fork 炸弹'),
        (r'curl\s+.*\s*\|\s*sh', '警告: 管道执行远程脚本'),
        (r'wget\s+.*\s*\|\s*sh', '警告: 管道执行远程脚本'),
        (r'eval\s*\(', '警告: 使用 eval'),
        (r'exec\s*\(', '警告: 使用 exec'),
        (r'system\s*\(', '警告: 使用 system 调用'),
        (r'os\.system\s*\(', '警告: 使用 os.system'),
        (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', '警告: subprocess 使用 shell=True'),
    ]
    
    # 敏感文件路径
    SENSITIVE_PATHS = [
        '/etc/passwd',
        '/etc/shadow',
        '/etc/hosts',
        '/.ssh/',
        '/.aws/',
        '/.config/',
        '/.openclaw/',
    ]
    
    def __init__(self, skills_dir='~/.openclaw/workspace/skills'):
        self.skills_dir = Path(skills_dir).expanduser()
        self.issues = []
        
    def scan_all_skills(self):
        """扫描所有 skill"""
        print("=" * 60)
        print("Skill 安全扫描")
        print("=" * 60)
        
        if not self.skills_dir.exists():
            print(f"错误: Skill 目录不存在: {self.skills_dir}")
            return
            
        skills = [d for d in self.skills_dir.iterdir() if d.is_dir()]
        print(f"\n发现 {len(skills)} 个 skill\n")
        
        for skill_path in skills:
            self.scan_skill(skill_path)
            
        self.print_summary()
        
    def scan_skill(self, skill_path):
        """扫描单个 skill"""
        skill_name = skill_path.name
        print(f"\n扫描: {skill_name}")
        print("-" * 40)
        
        skill_issues = []
        
        # 扫描所有文件
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # 跳过文档和示例文件
                if file_path.name in ['SKILL.md', 'README.md', 'CHANGELOG.md']:
                    continue
                if file_path.suffix in ['.md', '.txt', '.rst']:
                    continue
                issues = self.scan_file(file_path, skill_name)
                skill_issues.extend(issues)
                
        if skill_issues:
            for issue in skill_issues:
                print(f"  ! {issue['level']}: {issue['message']}")
                print(f"      文件: {issue['file']}")
                if issue.get('line'):
                    print(f"      行号: {issue['line']}")
        else:
            print("  [OK] 未发现明显风险")
            
        self.issues.extend(skill_issues)
        
    def scan_file(self, file_path, skill_name):
        """扫描单个文件"""
        issues = []
        
        try:
            # 跳过二进制文件
            if self.is_binary(file_path):
                return issues
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            # 检查危险模式
            for pattern, message in self.DANGEROUS_PATTERNS:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            'skill': skill_name,
                            'file': str(file_path.relative_to(self.skills_dir)),
                            'line': line_num,
                            'level': '高',
                            'message': message,
                            'content': line.strip()[:100]
                        })
                        
            # 检查敏感路径访问
            for sensitive_path in self.SENSITIVE_PATHS:
                if sensitive_path in content:
                    issues.append({
                        'skill': skill_name,
                        'file': str(file_path.relative_to(self.skills_dir)),
                        'level': '中',
                        'message': f'访问敏感路径: {sensitive_path}'
                    })
                    
            # 检查网络请求
            if re.search(r'(curl|wget|requests\.get|urllib\.request)', content, re.IGNORECASE):
                # 检查是否有验证
                if not re.search(r'(verify|cert|ssl|tls)', content, re.IGNORECASE):
                    issues.append({
                        'skill': skill_name,
                        'file': str(file_path.relative_to(self.skills_dir)),
                        'level': '低',
                        'message': '网络请求可能未验证 SSL/TLS'
                    })
                    
        except Exception as e:
            issues.append({
                'skill': skill_name,
                'file': str(file_path.relative_to(self.skills_dir)),
                'level': '信息',
                'message': f'扫描错误: {e}'
            })
            
        return issues
        
    def is_binary(self, file_path):
        """检查是否为二进制文件"""
        binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz'}
        return file_path.suffix.lower() in binary_extensions
        
    def print_summary(self):
        """打印扫描摘要"""
        print("\n" + "=" * 60)
        print("扫描摘要")
        print("=" * 60)
        
        if not self.issues:
            print("\n[OK] 所有 skill 扫描完成，未发现安全风险")
            return
            
        high = sum(1 for i in self.issues if i['level'] == '高')
        medium = sum(1 for i in self.issues if i['level'] == '中')
        low = sum(1 for i in self.issues if i['level'] == '低')
        
        print(f"\n发现 {len(self.issues)} 个问题:")
        print(f"  [HIGH] 高风险: {high}")
        print(f"  [MED] 中风险: {medium}")
        print(f"  [LOW] 低风险: {low}")
        
        if high > 0:
            print("\n[!] 发现高风险问题，建议立即检查！")
            
        print("\n建议:")
        print("  1. 仔细检查标记的文件和代码")
        print("  2. 确认 skill 来源可信")
        print("  3. 在隔离环境中测试新 skill")
        print("  4. 定期更新 skill 到最新版本")


if __name__ == '__main__':
    scanner = SkillSecurityScanner()
    scanner.scan_all_skills()
