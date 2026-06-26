#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillPilot 技能验证脚本

Usage:
    python scripts/validate.py <skill-directory>

Validates:
- YAML frontmatter format and required fields
- Skill naming conventions and directory structure
- Description completeness and quality
- File organization and resource references
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import List, Tuple


class SkillValidator:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> bool:
        """运行所有验证"""
        print(f"Validating skill: {self.skill_path}")
        print("=" * 60)
        
        self._check_directory_structure()
        self._check_skill_md_exists()
        self._check_yaml_frontmatter()
        self._check_description_quality()
        self._check_naming_conventions()
        self._check_file_organization()
        
        # 输出结果
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ Validation passed!")
        
        print("=" * 60)
        return len(self.errors) == 0
    
    def _check_directory_structure(self):
        """检查目录结构"""
        required_dirs = ["scripts", "references"]
        
        for dir_name in required_dirs:
            dir_path = self.skill_path / dir_name
            if not dir_path.exists():
                self.warnings.append(f"Missing recommended directory: {dir_name}/")
    
    def _check_skill_md_exists(self):
        """检查 SKILL.md 是否存在"""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("Missing required file: SKILL.md")
    
    def _check_yaml_frontmatter(self):
        """检查 YAML frontmatter"""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return
        
        content = skill_md.read_text()
        
        # 检查是否以 --- 开头
        if not content.startswith("---"):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return
        
        # 提取 YAML
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            self.errors.append("Invalid YAML frontmatter format")
            return
        
        yaml_content = match.group(1)
        
        try:
            frontmatter = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return
        
        # 检查必需字段
        if "name" not in frontmatter:
            self.errors.append("Missing required field: name")
        
        if "description" not in frontmatter:
            self.errors.append("Missing required field: description")
        
        # 检查是否有多余字段
        allowed_fields = {"name", "description"}
        extra_fields = set(frontmatter.keys()) - allowed_fields
        if extra_fields:
            self.warnings.append(f"Extra fields in frontmatter (only name/description allowed): {extra_fields}")
    
    def _check_description_quality(self):
        """检查 description 质量"""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return
        
        content = skill_md.read_text()
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return
        
        frontmatter = yaml.safe_load(match.group(1))
        description = frontmatter.get("description", "")
        
        # 处理 YAML 多行字符串 (可能是 dict 或列表)
        if isinstance(description, dict):
            # YAML > 格式会解析为 dict
            description = " ".join(str(v) for v in description.values())
        elif isinstance(description, list):
            description = " ".join(str(item) for item in description)
        elif not isinstance(description, str):
            description = str(description)
        
        # 检查长度
        if len(description) < 50:
            self.warnings.append("Description is too short (< 50 chars)")
        
        # 检查是否包含"when to use"
        if "use when" not in description.lower() and "use for" not in description.lower():
            self.warnings.append("Description should include when to use the skill")
        
        # 检查是否以小写开头
        first_word = description.split()[0] if description else ""
        if first_word and first_word[0].isupper() and not first_word.endswith('s'):
            self.warnings.append("Description should start with lowercase (it continues the prompt)")
    
    def _check_naming_conventions(self):
        """检查命名规范"""
        skill_name = self.skill_path.name
        
        # 检查是否使用小写和连字符
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', skill_name):
            self.warnings.append(f"Skill name should use lowercase and hyphens: {skill_name}")
    
    def _check_file_organization(self):
        """检查文件组织"""
        # 检查是否有 assets 目录（如果有，应该包含实际文件）
        assets_dir = self.skill_path / "assets"
        if assets_dir.exists():
            files = list(assets_dir.iterdir())
            if not files:
                self.warnings.append("Empty assets/ directory (remove if not needed)")
        
        # 检查 scripts 目录
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            py_files = list(scripts_dir.glob("*.py"))
            if py_files:
                # 检查是否有执行权限
                for py_file in py_files:
                    if not os.access(py_file, os.X_OK):
                        self.warnings.append(f"Script without execute permission: {py_file.name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <skill-directory>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    if not os.path.isdir(skill_path):
        print(f"Error: {skill_path} is not a directory")
        sys.exit(1)
    
    validator = SkillValidator(skill_path)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
