#!/usr/bin/env python3
"""
模块化安装脚本 - yaoyao-memory

用法：
    python3 install_modules.py              # 交互式安装
    python3 install_modules.py --list      # 列出所有模块
    python3 install_modules.py --install cloud_backup  # 安装指定模块
    python3 install_modules.py --remove stats         # 卸载指定模块
    python3 install_modules.py --status    # 查看已安装模块
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
MODULES_FILE = SKILL_DIR / "MODULES.json"
INSTALLED_FILE = SKILL_DIR / ".installed_modules.json"
CORE_MARKER = SKILL_DIR / ".core_installed"

# 安全：允许的模块ID格式
MODULE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')


def is_safe_module_id(module_id):
    """检查模块ID是否安全（防止路径遍历）"""
    if not module_id:
        return False
    if not MODULE_ID_PATTERN.match(module_id):
        return False
    # 禁止常见的路径遍历模式
    dangerous = ['..', '~', '$', '|', ';', '&', '`', '<', '>', '\n', '\r', '\x00']
    for d in dangerous:
        if d in module_id:
            return False
    return True


def load_modules():
    """加载模块配置"""
    if not MODULES_FILE.exists():
        print(f"❌ 模块配置文件不存在: {MODULES_FILE}")
        sys.exit(1)
    try:
        data = json.loads(MODULES_FILE.read_text())
        # 验证配置结构
        if "modules" not in data:
            print(f"❌ 模块配置格式错误：缺少 modules 字段")
            sys.exit(1)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ 模块配置文件格式错误: {e}")
        sys.exit(1)


def _detect_auto_modules():
    """自动检测可启用的模块"""
    auto_modules = []
    
    # 检测 IMA 凭证
    ima_client = Path.home() / ".config" / "ima" / "client_id"
    ima_api = Path.home() / ".config" / "ima" / "api_key"
    if ima_client.exists() and ima_api.exists():
        auto_modules.append("cloud_backup")
    
    # 检测 secrets.env 中的 IMA 配置
    secrets = Path.home() / ".openclaw" / "credentials" / "secrets.env"
    if secrets.exists():
        content = secrets.read_text()
        if "IMA_CLIENT_ID" in content and "IMA_API_KEY" in content:
            if "cloud_backup" not in auto_modules:
                auto_modules.append("cloud_backup")
    
    return auto_modules


def load_installed():
    """加载已安装模块"""
    if INSTALLED_FILE.exists():
        try:
            data = json.loads(INSTALLED_FILE.read_text())
            # 自动检测：添加检测到凭证的模块
            auto_modules = _detect_auto_modules()
            for mod in auto_modules:
                if mod not in data["modules"]:
                    data["modules"].append(mod)
                    data["installed_at"][mod] = "auto"
            return data
        except json.JSONDecodeError:
            # 配置文件损坏，恢复默认
            pass
    
    # 默认：自动检测
    auto_modules = _detect_auto_modules()
    return {
        "modules": auto_modules,
        "installed_at": {mod: "auto" for mod in auto_modules}
    }


def save_installed(installed):
    """安全保存已安装模块"""
    INSTALLED_FILE.write_text(json.dumps(installed, indent=2, ensure_ascii=False))


def list_modules(modules, installed):
    """列出所有模块"""
    print()
    print("📦 可用模块")
    print("=" * 50)
    print()
    
    for module_id, module in modules["modules"].items():
        status = "✅ 已安装" if module_id in installed["modules"] else "○ 未安装"
        required = " [必装]" if module.get("required") else ""
        
        print(f"  {module_id}: {module['name']}{required}")
        print(f"         {module['description']}")
        print(f"         脚本数: {len(module['scripts'])} | 大小: {module.get('size_estimate', 'unknown')}")
        print(f"         状态: {status}")
        print()


def status(modules, installed):
    """查看已安装状态"""
    print()
    print("📊 安装状态")
    print("=" * 50)
    print()
    
    core_ok = CORE_MARKER.exists()
    print(f"  核心模块: {'✅ 已安装' if core_ok else '❌ 未安装'}")
    print()
    
    if installed["modules"]:
        print("  已安装模块:")
        for module_id in installed["modules"]:
            if module_id in modules["modules"]:
                module = modules["modules"][module_id]
                print(f"    ✅ {module['name']} ({module_id})")
    else:
        print("  未安装可选模块")
    
    print()
    
    # 依赖检查
    print("  依赖关系:")
    for module_id, module in modules["modules"].items():
        if module_id != "core":
            deps = module.get("dependencies", [])
            if deps:
                print(f"    {module_id} → {', '.join(deps)}")


def check_core():
    """检查核心模块"""
    if not CORE_MARKER.exists():
        print("❌ 核心模块未安装！")
        print()
        print("请先运行完整安装：")
        print("  python3 install_modules.py --full-install")
        return False
    return True


def verify_script_safety(script_path):
    """验证脚本安全性"""
    if not script_path.exists():
        return False
    
    # 读取脚本内容检查危险模式
    try:
        content = script_path.read_text(encoding='utf-8')
        
        # 检查危险模式（这些用于检测脚本安全性，非执行代码）
        dangerous_patterns = [
            # 代码执行模式 - 检测而非使用
            'eval(', 'exec(', 'compile(', '__import__(',
            # Shell 执行模式 - 检测而非使用
            'subprocess.call', 'subprocess.run', 'os.system', 'os.popen',
            # 反序列化风险 - 检测而非使用
            'pickle.load', 'marshal.load',
        ]
        
        for pattern in dangerous_patterns:
            if pattern in content:
                print(f"  ⚠️  警告: 脚本包含潜在危险模式: {pattern}")
        
        return True
    except Exception:
        return False


def verify_installation():
    """验证安装完整性"""
    print()
    print("🔍 验证安装...")
    print()
    
    issues = []
    
    # 检查核心标记
    core_marker = SKILL_DIR / ".core_installed"
    if not core_marker.exists():
        issues.append("❌ 核心模块未安装")
    else:
        print("  ✅ 核心模块已安装")
    
    # 检查配置文件
    config_dir = SKILL_DIR / "config"
    if not config_dir.exists():
        issues.append("⚠️  配置目录不存在")
    else:
        print("  ✅ 配置目录存在")
    
    # 检查脚本目录
    scripts_dir = SKILL_DIR / "scripts"
    if not scripts_dir.exists():
        issues.append("❌ 脚本目录不存在")
    else:
        script_count = len(list(scripts_dir.glob("*.py")))
        print(f"  ✅ 脚本目录: {script_count} 个脚本")
    
    # 检查记忆目录
    memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    if memory_dir.exists():
        memory_count = len(list(memory_dir.glob("*.md")))
        print(f"  ✅ 记忆文件: {memory_count} 个")
    else:
        issues.append("⚠️  记忆目录不存在")
    
    # 检查数据库
    db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
    if db_path.exists():
        size_mb = db_path.stat().st_size / 1024 / 1024
        print(f"  ✅ 数据库: {size_mb:.1f} MB")
    else:
        print("  ℹ️  数据库不存在（首次运行会自动创建）")
    
    print()
    if issues:
        for issue in issues:
            print(f"  {issue}")
        print()
        return False
    else:
        print("  ✅ 安装验证通过！")
        return True


def complete_initialization():
    """完成初始化，删除 BOOTSTRAP.md"""
    bootstrap = SKILL_DIR / "BOOTSTRAP.md"
    if bootstrap.exists():
        bootstrap.unlink()
        print("  ✅ BOOTSTRAP.md 已删除（初始化完成）")
        return True
    return False


def install_module(module_id, modules, installed, verbose=True):
    """安装单个模块"""
    # 安全检查：模块ID格式
    if not is_safe_module_id(module_id):
        print(f"❌ 无效的模块ID: {module_id}")
        return False
    
    if module_id not in modules["modules"]:
        print(f"❌ 未知模块: {module_id}")
        return False
    
    module = modules["modules"][module_id]
    
    # 检查依赖
    deps = module.get("dependencies", [])
    for dep in deps:
        if dep == "core":
            if not CORE_MARKER.exists():
                print(f"❌ 模块 {module_id} 需要核心模块")
                return False
        elif dep not in installed["modules"]:
            print(f"❌ 模块 {module_id} 需要先安装 {dep}")
            return False
    
    # 检查是否已安装
    if module_id in installed["modules"]:
        if verbose:
            print(f"ℹ️  模块 {module_id} 已安装")
        return True
    
    # 创建模块目录（安全：使用 skill 目录下的固定位置）
    module_dir = SCRIPTS_DIR / module_id
    if not module_dir.exists():
        module_dir.mkdir(exist_ok=True)
    
    # 安全验证：确保在 scripts 目录下
    if not str(module_dir).startswith(str(SCRIPTS_DIR)):
        print(f"❌ 路径不安全: {module_dir}")
        return False
    
    # 复制脚本
    scripts = module.get("scripts", [])
    for script_name in scripts:
        src = SCRIPTS_DIR / f"{script_name}.py"
        
        # 安全检查：脚本必须在 scripts 目录
        if not str(src).startswith(str(SCRIPTS_DIR)):
            print(f"❌ 脚本路径不安全: {src}")
            continue
        
        if src.exists():
            # 验证脚本安全性
            if not verify_script_safety(src):
                print(f"⚠️  脚本安全性验证失败: {script_name}")
            
            # 如果脚本已在 scripts 目录，不移动（核心模块已安装）
            if module_id != "core":
                dst = module_dir / f"{script_name}.py"
                # 安全检查：目标路径必须在 scripts 目录下
                if not str(dst).startswith(str(SCRIPTS_DIR)):
                    print(f"❌ 目标路径不安全: {dst}")
                    continue
                shutil.copy2(src, dst)
    
    # 标记安装
    installed["modules"].append(module_id)
    installed["installed_at"][module_id] = datetime.now().isoformat()
    save_installed(installed)
    
    if verbose:
        print(f"✅ 模块已安装: {module['name']} ({module_id})")
    
    return True


def remove_module(module_id, modules, installed, verbose=True):
    """卸载模块"""
    # 安全检查：模块ID格式
    if not is_safe_module_id(module_id):
        print(f"❌ 无效的模块ID: {module_id}")
        return False
    
    if module_id not in modules["modules"]:
        print(f"❌ 未知模块: {module_id}")
        return False
    
    module = modules["modules"][module_id]
    
    if module.get("required"):
        print(f"❌ 必选模块不能卸载: {module_id}")
        return False
    
    if module_id not in installed["modules"]:
        if verbose:
            print(f"ℹ️  模块 {module_id} 未安装")
        return True
    
    # 检查依赖
    for other_id, other_module in modules["modules"].items():
        if other_id != module_id and other_id in installed["modules"]:
            if module_id in other_module.get("dependencies", []):
                print(f"❌ 模块 {other_id} 依赖 {module_id}，无法卸载")
                return False
    
    # 安全删除：确保在 scripts 目录下
    module_dir = SCRIPTS_DIR / module_id
    if str(module_dir).startswith(str(SCRIPTS_DIR)) and module_dir.exists():
        shutil.rmtree(module_dir)
    
    # 移除标记
    installed["modules"].remove(module_id)
    if module_id in installed["installed_at"]:
        del installed["installed_at"][module_id]
    save_installed(installed)
    
    if verbose:
        print(f"✅ 模块已卸载: {module['name']} ({module_id})")
    
    return True


def full_install(modules, installed):
    """完整安装（核心模块 + 基础模块）"""
    print()
    print("🚀 开始完整安装...")
    print()
    
    # 安装核心模块
    print("📦 安装核心模块...")
    if not CORE_MARKER.exists():
        CORE_MARKER.write_text(datetime.now().isoformat())
    print("  ✅ 核心模块")
    
    # 安装基础可选模块（security + health_check 必装）
    basic_modules = ["security", "health_check", "stats", "summary"]
    for module_id in basic_modules:
        if module_id in modules["modules"]:
            install_module(module_id, modules, installed, verbose=False)
            module = modules["modules"][module_id]
            print(f"  ✅ {module['name']}")
    
    print()
    print("🎉 完整安装完成！")
    print()
    print("可选模块：")
    print("  python3 install_modules.py --list    # 查看所有模块")
    print("  python3 install_modules.py --install cloud_backup  # 安装云备份")


def interactive_install(modules, installed):
    """交互式安装"""
    print()
    print("🦞 yaoyao-memory 模块化安装向导")
    print("=" * 50)
    print()
    
    # 检查核心
    if not CORE_MARKER.exists():
        print("🔍 检测到核心模块未安装...")
        print()
        print("是否安装核心模块？")
        print("  1. 安装核心（必选）")
        print("  2. 退出")
        print()
        
        while True:
            choice = input("请选择 [1]: ").strip() or "1"
            if choice == "1":
                CORE_MARKER.write_text(datetime.now().isoformat())
                print("  ✅ 核心模块已安装")
                break
            elif choice == "2":
                return
            else:
                print("请输入 1 或 2")
    
    print()
    print("📦 可选模块")
    print()
    
    available = []
    for module_id, module in modules["modules"].items():
        if module_id == "core":
            continue
        if module_id not in installed["modules"]:
            available.append((module_id, module))
            size = module.get("size_estimate", "unknown")
            print(f"  {len(available)}. {module['name']}")
            print(f"     {module['description']}")
            print(f"     大小: {size}")
            print()
    
    if not available:
        print("  所有可选模块已安装完成！")
        print()
        return
    
    print("  0. 完成安装")
    print()
    
    selected = []
    while True:
        choice = input(f"请选择要安装的模块 [多选如 1,2 或 0 完成]: ").strip()
        
        if choice == "0" or choice == "":
            break
        
        # 解析多选
        try:
            nums = [int(c.strip()) for c in choice.split(",")]
            for n in nums:
                if 1 <= n <= len(available):
                    if n not in selected:
                        selected.append(n)
            print(f"  已选择: {', '.join([available[i-1][1]['name'] for i in selected])}")
        except:
            print("请输入正确的选项")
    
    print()
    
    # 安装选中的模块
    for n in selected:
        module_id, module = available[n - 1]
        install_module(module_id, modules, installed, verbose=False)
        print(f"  ✅ {module['name']}")
    
    print()
    print("🎉 安装完成！")
    print()
    print("后续可以：")
    print("  python3 install_modules.py --status   # 查看安装状态")
    print("  python3 install_modules.py --list    # 查看所有模块")


def main():
    parser = argparse.ArgumentParser(description="yaoyao-memory 模块化安装")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有模块")
    parser.add_argument("--status", "-s", action="store_true", help="查看安装状态")
    parser.add_argument("--verify", "-v", action="store_true", help="验证安装完整性")
    parser.add_argument("--install", "-i", metavar="MODULE", help="安装指定模块")
    parser.add_argument("--remove", "-r", metavar="MODULE", help="卸载指定模块")
    parser.add_argument("--full-install", "-f", action="store_true", help="完整安装")
    parser.add_argument("--interactive", "-I", action="store_true", help="交互式安装")
    parser.add_argument("--complete", "-c", action="store_true", help="完成初始化并删除引导文件")
    
    args = parser.parse_args()
    
    modules = load_modules()
    installed = load_installed()
    
    # 无参数时显示状态
    if len(sys.argv) == 1:
        status(modules, installed)
        print("用法: python3 install_modules.py --help")
        return
    
    if args.verify:
        if verify_installation():
            sys.exit(0)
        else:
            sys.exit(1)
    
    if args.complete:
        if complete_initialization():
            print("  ✅ 初始化完成！")
        else:
            print("  ℹ️  BOOTSTRAP.md 不存在，无需删除")
        return
    
    if args.list:
        list_modules(modules, installed)
        return
    
    if args.status:
        status(modules, installed)
        return
    
    if args.full_install:
        full_install(modules, installed)
        return
    
    if args.interactive:
        interactive_install(modules, installed)
        return
    
    if args.install:
        if install_module(args.install, modules, installed):
            return
        sys.exit(1)
    
    if args.remove:
        if remove_module(args.remove, modules, installed):
            return
        sys.exit(1)


if __name__ == "__main__":
    main()
