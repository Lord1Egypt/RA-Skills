#!/usr/bin/env python3
"""
Ultimate Agent System 发布脚本
"""

import subprocess
import sys
from pathlib import Path

def check_requirements():
    """检查发布要求"""
    print("检查发布要求...")
    
    # 检查clawhub
    try:
        result = subprocess.run(["clawhub", "--version"], 
                              capture_output=True, text=True)
        if "ClawHub CLI" in result.stdout or "ClawHub CLI" in result.stderr:
            print("✅ ClawHub CLI 已安装")
        else:
            print("❌ ClawHub CLI 未找到")
            return False
    except FileNotFoundError:
        print("❌ ClawHub CLI 未安装")
        return False
    
    # 检查当前目录
    current_dir = Path.cwd()
    skill_files = ["SKILL.md", "README.md", "LICENSE"]
    
    for file in skill_files:
        if not (current_dir / file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    print("✅ 所有要求满足")
    return True

def validate_skill():
    """验证skill完整性"""
    print("\n验证skill完整性...")
    
    # 检查SKILL.md格式
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    required_sections = ["name:", "description:", "version:"]
    missing = []
    
    for section in required_sections:
        if section not in content.lower():
            missing.append(section)
    
    if missing:
        print(f"❌ SKILL.md缺少部分: {missing}")
        return False
    
    print("✅ SKILL.md格式正确")
    
    # 检查脚本可执行性
    scripts = ["ultimate_system.py"]
    for script in scripts:
        script_path = Path("scripts") / script
        if script_path.exists():
            print(f"✅ 脚本存在: {script}")
        else:
            print(f"⚠️  脚本不存在: {script}")
    
    return True

def run_tests():
    """运行测试"""
    print("\n运行测试...")
    
    try:
        # 运行主脚本
        result = subprocess.run([sys.executable, "scripts/ultimate_system.py"],
                              capture_output=True, text=True, timeout=10)
        
        if "ULTIMATE SYSTEM REPORT" in result.stdout:
            print("✅ 主脚本测试通过")
            return True
        else:
            print("❌ 主脚本测试失败")
            print("输出:", result.stdout[:200])
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def publish_to_clawhub():
    """发布到ClawHub"""
    print("\n发布到ClawHub...")
    
    # 获取版本信息
    with open("SKILL.md", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("version:"):
                version = line.split(":")[1].strip()
                break
        else:
            version = "1.0.0"
    
    # 构建发布命令
    cmd = [
        "clawhub", "publish", ".",
        "--slug", "ultimate-agent",
        "--name", "Ultimate Agent System",
        "--version", version,
        "--changelog", "初始发布：整合主动工作、自我改进、代理创建三大核心能力"
    ]
    
    print(f"发布命令: {' '.join(cmd)}")
    
    # 询问确认
    response = input("\n确认发布? (y/N): ")
    if response.lower() != 'y':
        print("发布取消")
        return False
    
    # 执行发布
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 发布成功!")
            print("输出:", result.stdout)
            return True
        else:
            print("❌ 发布失败")
            print("错误:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 发布过程出错: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("ULTIMATE AGENT SYSTEM 发布流程")
    print("="*60)
    
    # 步骤1: 检查要求
    if not check_requirements():
        print("\n❌ 发布要求不满足，请先安装ClawHub CLI")
        return 1
    
    # 步骤2: 验证skill
    if not validate_skill():
        print("\n❌ Skill验证失败")
        return 1
    
    # 步骤3: 运行测试
    if not run_tests():
        print("\n❌ 测试失败")
        response = input("继续发布? (y/N): ")
        if response.lower() != 'y':
            return 1
    
    # 步骤4: 发布
    if not publish_to_clawhub():
        return 1
    
    print("\n" + "="*60)
    print("发布流程完成!")
    print("="*60)
    print("\n安装命令:")
    print("  clawhub install ultimate-agent")
    print("\n使用命令:")
    print("  python -m ultimate_system")
    print("\n感谢发布 Ultimate Agent System!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())