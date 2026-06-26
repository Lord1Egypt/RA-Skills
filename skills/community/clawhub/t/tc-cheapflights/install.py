#!/usr/bin/env python3
"""
同程特价机票查询技能安装脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    dependencies = [
        'requests',
        'dateparser',
        'beautifulsoup4',
    ]
    
    for dep in dependencies:
        print(f"  安装 {dep}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"  ✅ {dep} 安装成功")
        except subprocess.CalledProcessError:
            print(f"  ⚠️  {dep} 安装失败，请手动安装: pip install {dep}")
    
    print("✅ 依赖安装完成")

def register_skill():
    """注册技能到EasyClaw"""
    print("📝 注册技能到EasyClaw...")
    
    skill_dir = Path(__file__).parent
    register_script = skill_dir / "scripts" / "easyclaw_register_skill.py"
    
    if not register_script.exists():
        print(f"❌ 注册脚本不存在: {register_script}")
        return False
    
    try:
        subprocess.check_call([sys.executable, str(register_script), str(skill_dir)])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 注册失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("同程特价机票查询技能安装程序")
    print("=" * 60)
    print()
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        sys.exit(1)
    
    # 安装依赖
    install_dependencies()
    print()
    
    # 注册技能
    if register_skill():
        print()
        print("=" * 60)
        print("✅ 技能安装完成!")
        print()
        print("使用方法:")
        print("  1. 在EasyClaw会话中，助手会自动识别技能")
        print("  2. 尝试查询: '帮我查一下北京到上海的机票'")
        print("  3. 创建监控: '监控北京到广州的机票价格'")
        print()
        print("配置说明:")
        print("  - 技能配置文件: ~/.easyclaw/skills/tongcheng-cheap-flights/config.json")
        print("  - 飞书推送: 配置webhook地址到配置文件")
        print("=" * 60)
    else:
        print("❌ 技能安装失败")
        sys.exit(1)

if __name__ == '__main__':
    main()