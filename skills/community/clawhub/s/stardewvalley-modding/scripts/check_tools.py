#!/usr/bin/env python3
"""
检查星露谷 Mod 制作所需工具
"""
import subprocess
import shutil
import sys

def check_command(cmd, name):
    """检查命令是否存在"""
    if shutil.which(cmd):
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=5)
            version = result.stdout.split('\n')[0] if result.stdout else "已安装"
            return True, version
        except:
            return True, "已安装"
    return False, None

def main():
    print("=" * 50)
    print("🔧 星露谷 Mod 制作工具检查")
    print("=" * 50)
    
    errors = []
    warnings = []
    
    # 检查 Python
    print("\n📦 检查 Python...")
    ok, info = check_command('python3', 'Python')
    if ok:
        print(f"   ✅ Python: {info}")
    else:
        errors.append("❌ Python 未安装（必需）")
        print("   ❌ Python 未安装（必需）")
    
    # 检查 .NET
    print("\n📦 检查 .NET SDK...")
    ok, info = check_command('dotnet', 'dotnet')
    if ok:
        print(f"   ✅ .NET SDK: {info}")
        print("   ℹ️  可以编译 SMAPI Mod")
    else:
        warnings.append("⚠️ .NET SDK 未安装（仅 SMAPI Mod 需要）")
        print("   ⚠️ .NET SDK 未安装")
        print("   ℹ️  仅 Content Patcher Mod 不需要")
    
    # 检查星露谷目录
    print("\n📁 检查星露谷游戏目录...")
    import os
    paths = [
        os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Stardew Valley"),
        "/Users/geyize/Library/Application Support/Steam/steamapps/common/Stardew Valley"
    ]
    
    game_path = None
    for p in paths:
        if os.path.exists(p):
            game_path = p
            print(f"   ✅ 找到游戏目录: {p}")
            break
    
    if not game_path:
        warnings.append("⚠️ 未找到星露谷游戏目录")
        print("   ⚠️ 未找到星露谷游戏目录")
    
    # 总结
    print("\n" + "=" * 50)
    if errors:
        print("❌ 错误:")
        for e in errors:
            print(f"   {e}")
        print("\n请安装缺失的工具后重试。")
        sys.exit(1)
    
    if warnings:
        print("⚠️ 警告:")
        for w in warnings:
            print(f"   {w}")
    
    if not errors and not warnings:
        print("✅ 所有工具就绪！可以开始制作 Mod。")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
