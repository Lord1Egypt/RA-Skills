#!/usr/bin/env python3
"""
技能扫描器 - 扫描所有技能的 SKILL.md 文件
"""

import os
import yaml
from pathlib import Path
from typing import List, Dict, Optional

class SkillScanner:
    """技能扫描器"""
    
    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.skills: List[Dict] = []
    
    def scan(self) -> List[Dict]:
        """扫描所有技能"""
        if not self.skills_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.skills_dir}")
        
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_md = item / 'SKILL.md'
                if skill_md.exists():
                    skill_info = self.parse_skill(skill_md)
                    if skill_info:
                        self.skills.append(skill_info)
        
        return self.skills
    
    def parse_skill(self, skill_path: Path) -> Optional[Dict]:
        """解析 SKILL.md 文件"""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 frontmatter
            frontmatter = {}
            body = content
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        body = parts[2] if len(parts) > 2 else ''
                    except yaml.YAMLError:
                        pass
            
            return {
                'name': frontmatter.get('name', ''),
                'description': frontmatter.get('description', ''),
                'path': str(skill_path.parent),
                'file_path': str(skill_path),
                'full_content': content,
                'body': body
            }
        except Exception as e:
            print(f"Error parsing {skill_path}: {e}")
            return None
