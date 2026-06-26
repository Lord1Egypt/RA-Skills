#!/usr/bin/env python3
"""
报告生成器 - 支持多语言
"""

from datetime import datetime
from typing import List, Dict
from locale_loader import LocaleLoader

class ReportGenerator:
    """多语言报告生成器"""
    
    def __init__(self, i18n: LocaleLoader):
        self.i18n = i18n
    
    def generate(self, skills: List[Dict], conflicts: List[Dict], 
                 scan_dir: str = '') -> str:
        """生成审计报告"""
        report = f"# {self.i18n.get('report_title')}\n\n"
        report += f"**{self.i18n.get('scan_time')}:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        if scan_dir:
            report += f"**{self.i18n.get('scan_directory')}:** {scan_dir}\n"
        report += f"**{self.i18n.get('total_skills')}:** {len(skills)}\n\n"
        
        if not conflicts:
            report += f"## {self.i18n.get('no_conflicts')}\n\n"
            report += f"{self.i18n.get('no_conflicts_detail')}\n"
            
            # 列出所有技能
            report += f"\n### {self.i18n.get('safe_skills')}\n\n"
            for skill in skills:
                report += f"- `{skill['name']}` - {skill['description'][:50]}...\n"
            return report
        
        report += f"## {self.i18n.get('conflicts_found', count=len(conflicts))}\n\n"
        
        for i, conflict in enumerate(conflicts, 1):
            level_key = 'high_similarity' if conflict['level'] == 'high' else 'medium_similarity'
            report += f"### {i}. {self.i18n.get(level_key)}\n\n"
            report += f"**{self.i18n.get('skill_a')}:** `{conflict['skill1']['name']}`\n"
            report += f"   - Path: `{conflict['skill1']['path']}`\n"
            report += f"**{self.i18n.get('skill_b')}:** `{conflict['skill2']['name']}`\n"
            report += f"   - Path: `{conflict['skill2']['path']}`\n\n"
            report += f"**{self.i18n.get('similarity_score')}:** {conflict['overall_similarity']*100:.0f}%\n\n"
            report += f"**{self.i18n.get('analysis')}:**\n"
            report += f"- {self.i18n.get('name_similarity')}: {conflict['name_similarity']*100:.0f}%\n"
            report += f"- {self.i18n.get('description_similarity')}: {conflict['description_similarity']*100:.0f}%\n\n"
            report += f"**{self.i18n.get('recommendations')}:**\n"
            report += f"- {self.i18n.get('differentiate_suggestion')}\n"
            report += f"- {self.i18n.get('rename_suggestion')}\n\n"
        
        return report
    
    def generate_json(self, skills: List[Dict], conflicts: List[Dict]) -> Dict:
        """生成 JSON 格式报告"""
        return {
            'scan_time': datetime.now().isoformat(),
            'total_skills': len(skills),
            'conflicts': [
                {
                    'skill1': conflict['skill1']['name'],
                    'skill2': conflict['skill2']['name'],
                    'similarity': conflict['overall_similarity'],
                    'level': conflict['level']
                }
                for conflict in conflicts
            ]
        }
