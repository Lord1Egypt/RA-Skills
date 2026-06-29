#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Install — 一键安装 triphasic-execution 技能（v4.1：双模式 + 跨平台）
=============================================
v4.1 重大更新：【双模式设计】+ 【安装路径由调用方决定】
  - 安装路径不再硬编码，通过 --target 参数或 TRIPHASIC_SKILL_DIR 环境变量指定
  - 各家智能体/平台自行决定技能安装位置
  - 🟢 按需调用模式（默认）| 🔵 全局自动模式（可选）

用法:
  python install.py                          # 安装（按需调用模式）
  python install.py --mode global            # 全局自动模式
  python install.py --target /path/to/skills # 指定安装路径
  python install.py --register-exec          # 安装 + 注册 exec wrapper
  python install.py --uninstall              # 卸载
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

# 脚本所在目录即技能根目录
SKILL_SOURCE = Path(__file__).parent.parent
SKILL_NAME = "triphasic-execution"


def get_target_dir(args) -> Path:
    """获取安装目标路径（优先级：--target > 环境变量 > 默认值）

    默认值仅为兼容性保留，实际应由调用方（Agent/平台）通过 --target 明确指定。
    """
    if args.target:
        return Path(args.target).expanduser().resolve() / SKILL_NAME
    env_dir = os.environ.get("TRIPHASIC_SKILL_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve() / SKILL_NAME
    # 兼容性默认值（不推荐依赖）
    return Path.home() / ".workbuddy" / "skills" / SKILL_NAME


def get_triphasic_home(args) -> Path:
    """获取数据目录路径（优先级：--home > 环境变量 > 默认值）"""
    if args.home:
        return Path(args.home).expanduser().resolve()
    env_home = os.environ.get("TRIPHASIC_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()
    return Path.home() / ".workbuddy" / "triphasic"


def install_skill(args):
    """安装技能（v4.1：支持双模式 + 可自定义安装路径）

    Args:
        args: argparse 命名空间，包含 mode/target/home 等字段
    """
    mode = args.mode
    target_dir = get_target_dir(args)
    triphasic_home = get_triphasic_home(args)

    print(f"📦 安装 {SKILL_NAME} 技能...")
    print(f"   🎯 模式：{'🟢 按需调用' if mode == 'on_demand' else '🔵 全局自动'}")
    print(f"   📂 安装到：{target_dir}")
    print(f"   📁 数据目录：{triphasic_home}")

    if target_dir.exists():
        print(f"   ⚠️  目标已存在：{target_dir}")
        overwrite = input("   是否覆盖？(y/N): ").strip().lower()
        if overwrite != "y":
            print("   取消安装")
            return False
        shutil.rmtree(target_dir)

    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_SOURCE, target_dir)
    print(f"   ✅ 已安装到：{target_dir}")

    # 初始化数据目录
    logger = target_dir / "scripts" / "problem_logger.py"
    if logger.exists():
        import subprocess
        env = os.environ.copy()
        env["TRIPHASIC_HOME"] = str(triphasic_home)
        result = subprocess.run(
            [sys.executable, str(logger), "init"],
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode == 0:
            print(f"   ✅ 数据目录已初始化：{triphasic_home}")
        else:
            print(f"   ⚠️  数据目录初始化失败：{result.stderr}")

    # v4.1：根据 mode 参数配置 config.json
    config_file = triphasic_home / "config.json"
    default_config = SKILL_SOURCE / "assets" / "default_config.json"
    if config_file.exists() and default_config.exists():
        try:
            with open(default_config, "r", encoding="utf-8") as f:
                default_cfg = json.load(f)
            with open(config_file, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            merged = {
                **default_cfg,
                **user_cfg,
                "mode": mode,
                "daemon": {
                    "enabled": mode == "global",
                    "start_on_boot": False,
                },
            }
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2, ensure_ascii=False)
            print(f"   ✅ 配置文件已更新（mode={mode}）")
        except Exception as e:
            print(f"   ⚠️  配置合并失败：{e}")

    return True


def register_exec(args):
    """注册 exec 全局管理（v4.1：仅在全局模式下推荐）"""
    target_dir = get_target_dir(args)
    triphasic_home = get_triphasic_home(args)
    mode = args.mode

    print(f"\n🔧 注册 exec 全局管理...")

    wrapper = target_dir / "scripts" / "exec_wrapper.py"

    if sys.platform == "win32":
        ps_profile = Path.home() / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
        if not ps_profile.parent.exists():
            ps_profile = Path.home() / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"

        func_code = f'''
# Triphasic Execution - exec wrapper
$env:TRIPHASIC_HOME = "{triphasic_home}"
function exec {{ python "{wrapper}" @args }}
'''
        print(f"   请将以下内容添加到 PowerShell Profile：")
        print(f"   Profile 位置：{ps_profile}")
        print(f"   ---")
        print(func_code.strip())
        print(f"   ---")
        print(f"   或运行：")
        print(f'   Add-Content -Path "{ps_profile}" -Value @\'')
        print(func_code.strip())
        print(f'\'@')

    else:
        func_code = f'''
# Triphasic Execution - exec wrapper
export TRIPHASIC_HOME="{triphasic_home}"
exec() {{
    python3 "{wrapper}" "$@"
}}
'''
        print(f"   请将以下内容添加到 ~/.bashrc 或 ~/.zshrc：")
        print(f"   ---")
        print(func_code.strip())
        print(f"   ---")

    print(f"\n   注册后重启终端即可使用 `exec` 命令")
    if mode == "global":
        print(f"\n💡 全局自动模式提示：启动守护进程以开启后台监控")
        print(f"   python problem_daemon.py start")
    else:
        print(f"\n💡 按需调用模式提示：无需 daemon，手动调用 CLI 即可")
    return True


def uninstall(args):
    """卸载技能"""
    target_dir = get_target_dir(args)
    triphasic_home = get_triphasic_home(args)

    print(f"🗑️  卸载 {SKILL_NAME}...")

    if not target_dir.exists():
        print(f"   ⚠️  技能未安装（{target_dir}）")
        return

    shutil.rmtree(target_dir)
    print(f"   ✅ 已删除：{target_dir}")
    print(f"\n   以下数据目录保留未删除（如需清理请手动删除）：")
    print(f"   {triphasic_home}")


def main():
    parser = argparse.ArgumentParser(description=f"安装 {SKILL_NAME} 技能（v4.1：双模式 + 跨平台）")
    parser.add_argument("--mode", choices=["on_demand", "global"], default="on_demand",
                       help="🟢 on_demand:按需调用（默认）| 🔵 global:全局自动（daemon 后台监控）")
    parser.add_argument("--target", type=str, default=None,
                       help="安装目标路径（由 Agent/平台决定，如 ~/.workbuddy/skills/）")
    parser.add_argument("--home", type=str, default=None,
                       help="数据目录路径（默认 ~/.workbuddy/triphasic/）")
    parser.add_argument("--register-exec", action="store_true", help="安装后注册 exec wrapper")
    parser.add_argument("--uninstall", action="store_true", help="卸载技能")

    args = parser.parse_args()

    if args.uninstall:
        uninstall(args)
    else:
        mode = args.mode
        installed = install_skill(args)
        if installed and args.register_exec:
            register_exec(args)
        elif installed:
            print(f"\n💡 提示：")
            if mode == "global":
                print(f"   🔵 全局自动模式已启用")
                print(f"   → 启动守护进程：python problem_daemon.py start")
                print(f"   → 注册 exec wrapper: python install.py --register-exec")
            else:
                print(f"   🟢 按需调用模式已启用（默认）")
                print(f"   → 需要三步框架时，手动加载技能即可")


if __name__ == "__main__":
    main()
