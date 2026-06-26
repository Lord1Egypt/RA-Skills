#!/usr/bin/env python3
"""
EasyClaw技能注册脚本
将技能文件夹注册到EasyClaw系统
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def register_skill(source_folder_path: str):
    """
    注册技能到EasyClaw
    
    Args:
        source_folder_path: 技能文件夹路径
    """
    try:
        # 检查源文件夹是否存在
        source_path = Path(source_folder_path).resolve()
        if not source_path.exists():
            logger.error(f"源文件夹不存在: {source_path}")
            return False
        
        # 检查SKILL.md文件
        skill_md = source_path / "SKILL.md"
        if not skill_md.exists():
            logger.error(f"SKILL.md文件不存在: {skill_md}")
            return False
        
        # 读取SKILL.md获取技能名称
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析YAML frontmatter
        import re
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        
        if not frontmatter_match:
            logger.error("SKILL.md中没有找到YAML frontmatter")
            return False
        
        frontmatter = frontmatter_match.group(1)
        
        # 解析技能名称
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if not name_match:
            logger.error("SKILL.md中没有找到name字段")
            return False
        
        skill_name = name_match.group(1).strip()
        
        # EasyClaw技能目录
        easyclaw_skills_dir = Path.home() / ".easyclaw" / "skills"
        easyclaw_skills_dir.mkdir(parents=True, exist_ok=True)
        
        # 目标路径
        target_path = easyclaw_skills_dir / skill_name
        
        # 如果目标已存在，先备份
        if target_path.exists():
            backup_path = target_path.with_suffix('.bak')
            logger.info(f"技能已存在，备份到: {backup_path}")
            if backup_path.exists():
                shutil.rmtree(backup_path)
            shutil.move(target_path, backup_path)
        
        # 复制技能文件夹
        logger.info(f"复制技能文件夹: {source_path} -> {target_path}")
        shutil.copytree(source_path, target_path)
        
        # 检查复制结果
        if (target_path / "SKILL.md").exists():
            logger.info(f"技能注册成功: {skill_name}")
            logger.info(f"技能路径: {target_path}")
            
            # 显示技能信息
            print(f"\n✅ 技能注册成功!")
            print(f"   名称: {skill_name}")
            print(f"   路径: {target_path}")
            print(f"   下次启动EasyClaw时自动加载")
            
            return True
        else:
            logger.error(f"技能复制失败: SKILL.md不存在于目标路径")
            return False
            
    except Exception as e:
        logger.error(f"注册技能时发生错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python easyclaw_register_skill.py <skill_folder_path>")
        print("示例: python easyclaw_register_skill.py ./tongcheng-cheap-flights")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    
    # 注册技能
    success = register_skill(source_folder)
    
    if not success:
        print("❌ 技能注册失败")
        sys.exit(1)

if __name__ == '__main__':
    main()