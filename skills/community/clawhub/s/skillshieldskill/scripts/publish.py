#!/usr/bin/env python3
"""
SkillShield Publisher
Publish skill to the skill marketplace
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def publish_skill():
    """Publish skill to marketplace"""
    skill_dir = Path(__file__).parent.parent
    
    # Load metadata
    meta_file = skill_dir / "_meta.json"
    if not meta_file.exists():
        print("❌ 错误: 未找到 _meta.json 文件")
        sys.exit(1)
    
    with open(meta_file) as f:
        meta = json.load(f)
    
    print("🛡️ SkillShield 发布工具")
    print("=" * 50)
    print(f"\n技能名称: {meta.get('name')}")
    print(f"版本: {meta.get('version')}")
    print(f"作者: {meta.get('author')}")
    print(f"描述: {meta.get('description')[:50]}...")
    
    # Check required files
    required_files = ['SKILL.md', '_meta.json', 'README.md', 'LICENSE']
    missing = []
    for f in required_files:
        if not (skill_dir / f).exists():
            missing.append(f)
    
    if missing:
        print(f"\n❌ 缺少必要文件: {', '.join(missing)}")
        sys.exit(1)
    
    print("\n✅ 所有必要文件齐全")
    
    # Run self-scan
    print("\n🔍 正在执行自检扫描...")
    scan_result = subprocess.run(
        [sys.executable, str(skill_dir / 'scripts' / 'skillshield.py'), 
         'scan', str(skill_dir)],
        capture_output=True,
        text=True
    )
    
    if scan_result.returncode == 0:
        print("✅ 自检通过 - 技能安全")
    else:
        print("⚠️ 自检发现问题，请检查")
        print(scan_result.stdout)
    
    print("\n" + "=" * 50)
    print("📦 发布方式:")
    print()
    print("1. 通过 skills CLI 发布:")
    print(f"   npx skills publish {skill_dir}")
    print()
    print("2. 手动上传到 GitHub:")
    print("   - 创建仓库: https://github.com/new")
    print("   - 推送代码:")
    print(f"     cd {skill_dir}")
    print("     git init")
    print("     git add .")
    print('     git commit -m "Initial release v1.0.0"')
    print("     git remote add origin https://github.com/YOUR_USERNAME/skillshield.git")
    print("     git push -u origin main")
    print()
    print("3. 提交到 SkillHub:")
    print("   - 访问 https://clawhub.com")
    print("   - 注册账号并提交 skill")
    print()
    print("=" * 50)
    print("✨ SkillShield 准备就绪，等待发布!")

if __name__ == '__main__':
    publish_skill()
