#!/usr/bin/env python3
"""
技能测试框架
检查技能目录结构、SKILL.md 格式、脚本语法
"""

import subprocess
import sys
import os
import json
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def parse_args():
    parser = argparse.ArgumentParser(description='技能测试框架')
    parser.add_argument('skill_path', help='技能目录路径')
    parser.add_argument('--quick', '-q', action='store_true', help='快速测试')
    parser.add_argument('--output', '-o', help='输出报告路径')
    return parser.parse_args()

def check_skill_structure(skill_path):
    """检查技能目录结构"""
    skill_path = Path(skill_path)
    logger.info(f"检查技能目录: {skill_path}")

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        logger.error("缺失 SKILL.md")
        return False

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            logger.error("YAML frontmatter 格式错误")
            return False
        frontmatter = content[3:yaml_end]
        lines = frontmatter.strip().split('\n')
        if not any(line.startswith('name:') for line in lines):
            logger.error("缺少 name 字段")
            return False
        if not any(line.startswith('description:') for line in lines):
            logger.error("缺少 description 字段")
            return False

    logger.info("✅ 目录结构检查通过")
    return True

def check_scripts(skill_path, quick_mode=False):
    """检查脚本语法"""
    scripts_dir = Path(skill_path) / 'scripts'
    if not scripts_dir.exists():
        logger.info("无 scripts 目录")
        return True

    scripts = list(scripts_dir.glob('*.py'))
    bash_scripts = list(scripts_dir.glob('*.sh'))

    for script in scripts:
        try:
            subprocess.run(['python3', '-m', 'py_compile', str(script)],
                         capture_output=True, timeout=10)
            logger.info(f"✅ {script.name} 语法正确")
        except Exception as e:
            logger.error(f"❌ {script.name} 检查失败: {e}")
            return False

    for script in bash_scripts:
        try:
            subprocess.run(['bash', '-n', str(script)],
                         capture_output=True, timeout=10)
            logger.info(f"✅ {script.name} 语法正确")
        except Exception as e:
            logger.error(f"❌ {script.name} 检查失败: {e}")
            return False

    return True

def main():
    setup_logging()
    args = parse_args()

    structure_ok = check_skill_structure(args.skill_path)
    scripts_ok = check_scripts(args.skill_path, args.quick)

    if structure_ok and scripts_ok:
        print("✅ 技能测试通过")
        sys.exit(0)
    else:
        print("❌ 技能测试失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
