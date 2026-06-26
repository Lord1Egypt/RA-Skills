#!/usr/bin/env python3
"""
Skill Performance Auditor
检查 AgentSkill 的性能和优化建议
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

class PerformanceAuditor:
    """性能审计器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues = []

    def count_tokens(self, text: str) -> int:
        """估算 token 数量（粗略估算：1 token ≈ 4 字符）"""
        return len(text) // 4

    def audit_skill_md(self, file_path: Path) -> Dict[str, Any]:
        """审计 SKILL.md 文件"""
        content = file_path.read_text(encoding='utf-8')

        # 分离 frontmatter 和 body
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not frontmatter_match:
            return {'error': 'Invalid SKILL.md format'}

        frontmatter = frontmatter_match.group(1)
        body = frontmatter_match.group(2)

        issues = []
        stats = {
            'frontmatter_tokens': self.count_tokens(frontmatter),
            'body_tokens': self.count_tokens(body),
            'total_tokens': self.count_tokens(content),
            'line_count': len(content.split('\n')),
        }

        # 检查 frontmatter 大小（应该 < 100 tokens）
        if stats['frontmatter_tokens'] > 100:
            issues.append({
                'severity': 'medium',
                'category': 'frontmatter_too_long',
                'message': f'Frontmatter is too long ({stats["frontmatter_tokens"]} tokens, should be < 100)',
                'suggestion': 'Move detailed descriptions to body, keep frontmatter concise',
            })

        # 检查 body 大小（应该 < 5000 tokens）
        if stats['body_tokens'] > 5000:
            issues.append({
                'severity': 'high',
                'category': 'body_too_long',
                'message': f'Body is too long ({stats["body_tokens"]} tokens, should be < 5000)',
                'suggestion': 'Split content into references/ files and link from SKILL.md',
            })

        # 检查行数（应该 < 500 行）
        if stats['line_count'] > 500:
            issues.append({
                'severity': 'medium',
                'category': 'too_many_lines',
                'message': f'Too many lines ({stats["line_count"]} lines, should be < 500)',
                'suggestion': 'Split content into references/ files to reduce bloat',
            })

        # 检查是否有重复内容
        duplicate_sections = re.findall(r'##\s+(.+)', body)
        if len(duplicate_sections) != len(set(duplicate_sections)):
            issues.append({
                'severity': 'low',
                'category': 'duplicate_sections',
                'message': 'Duplicate section headers found',
                'suggestion': 'Remove or merge duplicate sections',
            })

        # 检查是否有未使用的资源引用
        refs_dir = self.skill_path / 'references'
        if refs_dir.exists():
            referenced_files = set(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body))
            referenced_files.update(re.findall(r'\[([^\]]+)\]\[([^\]]+)\]', body))

            existing_files = {f.name for f in refs_dir.glob('*.md')}
            unreferenced = existing_files - {Path(r[1]).name for r in referenced_files}

            if unreferenced:
                issues.append({
                    'severity': 'low',
                    'category': 'unreferenced_files',
                    'message': f'Unreferenced files in references/: {", ".join(unreferenced)}',
                    'suggestion': 'Either link them in SKILL.md or remove if not needed',
                })

        return {
            'stats': stats,
            'issues': issues,
        }

    def audit_scripts(self, scripts_dir: Path) -> List[Dict[str, Any]]:
        """审计脚本目录"""
        issues = []

        if not scripts_dir.exists():
            return issues

        # 检查脚本是否有执行权限
        for script_file in scripts_dir.glob('*'):
            if script_file.is_file():
                if not os.access(script_file, os.X_OK):
                    issues.append({
                        'severity': 'low',
                        'category': 'no_execute_permission',
                        'file': str(script_file.relative_to(self.skill_path)),
                        'message': f'Script lacks execute permission',
                        'suggestion': f'Run: chmod +x {script_file.name}',
                    })

        return issues

    def audit_references(self, refs_dir: Path) -> List[Dict[str, Any]]:
        """审计 references 目录"""
        issues = []

        if not refs_dir.exists():
            return issues

        # 检查是否有超大文件
        for ref_file in refs_dir.glob('*.md'):
            content = ref_file.read_text(encoding='utf-8')
            tokens = self.count_tokens(content)

            if tokens > 10000:
                issues.append({
                    'severity': 'medium',
                    'category': 'large_reference_file',
                    'file': str(ref_file.relative_to(self.skill_path)),
                    'message': f'Large reference file ({tokens} tokens)',
                    'suggestion': 'Consider splitting into smaller files or adding grep patterns',
                })

        return issues

    def audit_skill(self) -> Dict[str, Any]:
        """审计整个技能"""
        all_issues = []

        # 审计 SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            skill_md_result = self.audit_skill_md(skill_md)
            all_issues.extend(skill_md_result.get('issues', []))
            skill_md_stats = skill_md_result.get('stats', {})
        else:
            all_issues.append({
                'severity': 'high',
                'category': 'missing_skill_md',
                'message': 'SKILL.md not found',
                'suggestion': 'Create SKILL.md with proper frontmatter and body',
            })
            skill_md_stats = {}

        # 审计 scripts/
        scripts_dir = self.skill_path / 'scripts'
        all_issues.extend(self.audit_scripts(scripts_dir))

        # 审计 references/
        refs_dir = self.skill_path / 'references'
        all_issues.extend(self.audit_references(refs_dir))

        # 检查是否有 README.md 等不应该存在的文件
        for unwanted in ['README.md', 'INSTALLATION_GUIDE.md', 'QUICK_REFERENCE.md', 'CHANGELOG.md']:
            unwanted_file = self.skill_path / unwanted
            if unwanted_file.exists():
                all_issues.append({
                    'severity': 'low',
                    'category': 'unnecessary_file',
                    'file': unwanted,
                    'message': f'Unnecessary file: {unwanted}',
                    'suggestion': f'Remove {unwanted} - skills should only contain essential files',
                })

        # 按严重程度排序
        all_issues.sort(key=lambda x: (
            {'high': 0, 'medium': 1, 'low': 2}[x.get('severity', 'low')],
            x.get('file', ''),
        ))

        return {
            'skill_path': str(self.skill_path),
            'skill_md_stats': skill_md_stats,
            'total_issues': len(all_issues),
            'high_severity': len([i for i in all_issues if i.get('severity') == 'high']),
            'medium_severity': len([i for i in all_issues if i.get('severity') == 'medium']),
            'low_severity': len([i for i in all_issues if i.get('severity') == 'low']),
            'issues': all_issues,
        }

def main():
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 performance_audit.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    auditor = PerformanceAuditor(skill_path)
    result = auditor.audit_skill()

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
