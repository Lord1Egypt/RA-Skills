#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector 安装脚本
简化安装流程，支持 ClawHub 安装方式
"""

import os
import sys
import json
import shutil
from pathlib import Path

def get_openclaw_skill_dir():
    """获取 OpenClaw 技能目录"""
    # 尝试不同平台的路径
    possible_paths = [
        # Linux/Mac
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".config" / "openclaw" / "skills",
        # Windows
        Path.home() / "AppData" / "Roaming" / "OpenClaw" / "skills",
        Path.home() / ".openclaw" / "skills",
        # 备用路径
        Path("/usr/local/share/openclaw/skills"),
        Path("/opt/openclaw/skills"),
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✅ 找到技能目录: {path}")
            return path
    
    # 询问用户
    print("❓ 未找到 OpenClaw 技能目录。")
    user_input = input("请输入技能安装目录（默认: ~/.openclaw/workspace/skills）: ").strip()
    
    if user_input:
        skill_dir = Path(user_input).expanduser()
    else:
        skill_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    
    skill_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 使用技能目录: {skill_dir}")
    return skill_dir

def copy_skill_files(source_dir, target_dir):
    """复制技能文件到目标目录"""
    print(f"📦 复制技能文件到: {target_dir}")
    
    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制所有文件
    files_to_copy = [
        "skill.json",
        "skill_optimized.json",
        "SKILL.md",
        "SKILL_OPTIMIZED.md",
        "README.md",
        "README_EN.md",
        "README_ZH.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "RELEASE.md",
        "LICENSE",
        "package.json",
        "verify_optimization.py",
        ".gitignore"
    ]
    
    directories_to_copy = [
        "scripts",
        "tests",
        "examples"
    ]
    
    # 复制文件
    copied_files = []
    for filename in files_to_copy:
        src = source_dir / filename
        if src.exists():
            shutil.copy2(src, target_dir / filename)
            copied_files.append(filename)
            print(f"  ✓ {filename}")
        else:
            print(f"  ⚠ 警告: {filename} 不存在")
    
    # 复制目录
    for dirname in directories_to_copy:
        src = source_dir / dirname
        if src.exists() and src.is_dir():
            shutil.copytree(src, target_dir / dirname, dirs_exist_ok=True)
            copied_files.append(f"{dirname}/")
            print(f"  ✓ {dirname}/")
        else:
            print(f"  ⚠ 警告: {dirname}/ 不存在")
    
    # 创建配置模板
    config_template = {
        "initialized": False,
        "csv_path": "",
        "db_path": "C:\\Users\\Administrator\\AppData\\Local\\Quicker\\data\\quicker.db",
        "starter_path": "C:\\Program Files\\Quicker\\QuickerStarter.exe",
        "default_source": "csv",
        "auto_select_threshold": 0.8,
        "max_results": 10
    }
    
    config_path = target_dir / "config.json"
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_template, f, indent=2, ensure_ascii=False)
        print(f"  ✓ 创建配置模板: config.json")
    
    print(f"✅ 共复制 {len(copied_files)} 个文件/目录")
    return True

def verify_installation(target_dir):
    """验证安装是否成功"""
    print("\n🔍 验证安装...")
    
    required_files = [
        "skill.json",
        "SKILL.md",
        "scripts/quicker_connector.py",
        "scripts/init_quicker.py"
    ]
    
    for filepath in required_files:
        full_path = target_dir / filepath
        if not full_path.exists():
            print(f"  ❌ 缺失必要文件: {filepath}")
            return False
    
    # 验证技能配置
    skill_json_path = target_dir / "skill.json"
    try:
        with open(skill_json_path, 'r', encoding='utf-8') as f:
            skill_data = json.load(f)
        
        if skill_data.get('name') != 'quicker-connector':
            print(f"  ❌ 技能名称不匹配: {skill_data.get('name')}")
            return False
        
        print(f"  ✓ 技能配置正确: {skill_data.get('name')} v{skill_data.get('version')}")
        
    except Exception as e:
        print(f"  ❌ 无法解析 skill.json: {e}")
        return False
    
    print("✅ 安装验证通过!")
    return True

def run_initialization_wizard(target_dir):
    """运行初始化向导"""
    print("\n🎯 启动初始化向导...")
    
    init_script = target_dir / "scripts" / "init_quicker.py"
    if init_script.exists():
        print("📝 运行初始化脚本...")
        
        # 添加脚本目录到路径
        sys.path.insert(0, str(target_dir / "scripts"))
        
        try:
            import init_quicker
            init_quicker.main()
            print("✅ 初始化完成!")
            return True
        except Exception as e:
            print(f"⚠ 初始化脚本运行失败: {e}")
            print("  你可以稍后手动运行: python scripts/init_quicker.py")
            return False
    else:
        print("⚠ 初始化脚本不存在，跳过向导。")
        return True

def display_usage_instructions(target_dir):
    """显示使用说明"""
    print("\n" + "=" * 70)
    print("🎉 Quicker Connector 安装完成!")
    print("=" * 70)
    print()
    
    print("📋 使用说明:")
    print("1. 配置 Quicker 连接:")
    print(f"   运行: cd '{target_dir}' && python scripts/init_quicker.py")
    print()
    
    print("2. 验证安装:")
    print(f"   运行: cd '{target_dir}' && python verify_optimization.py")
    print()
    
    print("3. 重启 OpenClaw Gateway:")
    print("   openclaw gateway restart")
    print()
    
    print("4. 使用技能:")
    print("   • 用 quicker 截图")
    print("   • 帮我翻译这段文字")
    print("   • 列出所有 quicker 动作")
    print("   • quicker 搜索包含'截图'的动作")
    print()
    
    print("📖 更多文档:")
    print(f"   • README: {target_dir}/README.md")
    print(f"   • 中文文档: {target_dir}/README_ZH.md")
    print("   • GitHub: https://github.com/awamwang/quicker-connector")
    print()
    
    print("🔄 更新技能:")
    print("   通过 ClawHub: clawhub update quicker-connector")
    print("   手动更新: 重新运行此安装脚本")
    print()
    
    print("🆘 获取帮助:")
    print("   • 问题反馈: https://github.com/awamwang/quicker-connector/issues")
    print("   • ClawHub 社区: https://clawhub.ai/community")
    print()

def main():
    """主安装函数"""
    print("\n" + "=" * 70)
    print("🦀 Quicker Connector 安装程序 v1.2.0")
    print("=" * 70)
    print()
    
    try:
        # 获取当前脚本目录（技能源代码目录）
        script_dir = Path(__file__).parent
        source_dir = script_dir.parent
        
        print(f"📁 源代码目录: {source_dir}")
        
        # 获取安装目录
        skill_dir = get_openclaw_skill_dir()
        target_dir = skill_dir / "quicker-connector"
        
        print(f"📁 目标目录: {target_dir}")
        
        # 确认安装
        if target_dir.exists():
            print(f"⚠ 警告: 技能已存在于 {target_dir}")
            response = input("是否覆盖安装? (y/N): ").strip().lower()
            if response != 'y':
                print("安装取消。")
                return 0
            shutil.rmtree(target_dir)
        
        # 复制文件
        if not copy_skill_files(source_dir, target_dir):
            print("❌ 文件复制失败。")
            return 1
        
        # 验证安装
        if not verify_installation(target_dir):
            print("❌ 安装验证失败。")
            return 1
        
        # 可选：运行初始化向导
        response = input("\n是否运行初始化向导? (y/N): ").strip().lower()
        if response == 'y':
            run_initialization_wizard(target_dir)
        
        # 显示使用说明
        display_usage_instructions(target_dir)
        
        print("✅ 安装完成!")
        return 0
        
    except Exception as e:
        print(f"\n❌ 安装失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())