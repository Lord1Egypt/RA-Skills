#!/usr/bin/env python3
"""
Skill Security Auditor
检查 AgentSkill 中的潜在安全风险和危险操作
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

class SecurityAuditor:
    """安全审计器"""

    # 危险操作模式
    DANGEROUS_PATTERNS = {
        'file_deletion': [
            r'\brm\s+-rf?\b',
            r'\brmdir\b',
            r'\bunlink\b',
            r'\bdelete\s+.*\s+file',
        ],
        'system_commands': [
            r'\beval\s*\(',
            r'\bexec\s*\(',
            r'\bsubprocess\s*\.\s*call\s*\(',
            r'\bos\s*\.\s*system\s*\(',
            r'\bbash\s+-c',
            r'\bsh\s+-c',
        ],
        'network_requests': [
            r'\brequests\.\w+\s*\(',
            r'\burllib\.\w+\s*\(',
            r'\bhttpx\.\w+\s*\(',
            r'\bfetch\s*\(',
        ],
        'credential_leaks': [
            r'api[_-]?key\s*=\s*["\'][\w-]+["\']',
            r'secret\s*=\s*["\'][\w-]+["\']',
            r'token\s*=\s*["\'][\w-]+["\']',
            r'password\s*=\s*["\'][\w-]+["\']',
            r'bearer\s+[\w-]+',
        ],
        'suspicious_urls': [
            r'https?://[^\s]*\.tk\b',
            r'https?://[^\s]*\.ml\b',
            r'https?://[^\s]*pastebin\.com',
            r'https?://[^\s]*bit\.ly',
        ],
        'file_write': [
            r'\bopen\s*\([^)]*["\']w["\']',
            r'\bPath\.write_text',
            r'\bPath\.write_bytes',
        ],
        'code_execution': [
            r'\b__import__\s*\(',
            r'\bimportlib\s*\.\s*import_module\s*\(',
            r'\bcompile\s*\(',
        ],
    }

    # 高风险文件路径
    RISKY_PATHS = [
        '~/.ssh/',
        '/etc/',
        '/root/',
        '/home/',
        '~/.config/',
        '~/.aws/',
    ]

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues = []

    def audit_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """审计单个文件"""
        issues = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            for category, patterns in self.DANGEROUS_PATTERNS.items():
                for pattern in patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        # 找到匹配的行号
                        line_num = content[:match.start()].count('\n') + 1
                        line_text = lines[line_num - 1].strip()

                        # 检查是否在注释中或文档示例中
                        if (line_text.startswith('#') or 
                            '"""' in line_text or 
                            "'''" in line_text or
                            line_text.startswith('-') or  # Markdown list
                            line_text.startswith('**') or  # Markdown bold
                            '```' in line_text):  # Code block
                            continue

                        issues.append({
                            'category': category,
                            'severity': self._get_severity(category),
                            'file': str(file_path.relative_to(self.skill_path)),
                            'line': line_num,
                            'pattern': pattern,
                            'matched_text': match.group(),
                            'context': line_text,
                        })

            # 检查高风险路径
            for risky_path in self.RISKY_PATHS:
                if risky_path in content:
                    matches = [i for i, line in enumerate(lines, 1) if risky_path in line]
                    for line_num in matches:
                        line_text = lines[line_num - 1].strip()
                        if line_text.startswith('#'):
                            continue
                        issues.append({
                            'category': 'risky_path',
                            'severity': 'high',
                            'file': str(file_path.relative_to(self.skill_path)),
                            'line': line_num,
                            'pattern': risky_path,
                            'matched_text': risky_path,
                            'context': line_text,
                        })

        except Exception as e:
            self.issues.append({
                'category': 'read_error',
                'severity': 'low',
                'file': str(file_path.relative_to(self.skill_path)),
                'line': 0,
                'error': str(e),
            })

        return issues

    def _get_severity(self, category: str) -> str:
        """获取风险等级"""
        high_risk = ['file_deletion', 'system_commands', 'credential_leaks']
        medium_risk = ['network_requests', 'code_execution', 'risky_path']

        if category in high_risk:
            return 'high'
        elif category in medium_risk:
            return 'medium'
        else:
            return 'low'

    def audit_skill(self) -> Dict[str, Any]:
        """审计整个技能"""
        all_issues = []

        # 检查 SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            all_issues.extend(self.audit_file(skill_md))

        # 检查 scripts/
        scripts_dir = self.skill_path / 'scripts'
        if scripts_dir.exists():
            for script_file in scripts_dir.glob('*.py'):
                all_issues.extend(self.audit_file(script_file))
            for script_file in scripts_dir.glob('*.sh'):
                all_issues.extend(self.audit_file(script_file))

        # 检查 references/
        refs_dir = self.skill_path / 'references'
        if refs_dir.exists():
            for ref_file in refs_dir.glob('*.md'):
                all_issues.extend(self.audit_file(ref_file))

        # 按严重程度排序
        all_issues.sort(key=lambda x: (
            {'high': 0, 'medium': 1, 'low': 2}[x.get('severity', 'low')],
            x['file'],
            x['line']
        ))

        return {
            'skill_path': str(self.skill_path),
            'total_issues': len(all_issues),
            'high_severity': len([i for i in all_issues if i.get('severity') == 'high']),
            'medium_severity': len([i for i in all_issues if i.get('severity') == 'medium']),
            'low_severity': len([i for i in all_issues if i.get('severity') == 'low']),
            'issues': all_issues,
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 security_audit.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    auditor = SecurityAuditor(skill_path)
    result = auditor.audit_skill()

    # 输出 JSON 格式
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
