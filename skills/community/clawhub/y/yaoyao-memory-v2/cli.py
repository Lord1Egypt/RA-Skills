#!/usr/bin/env python3
"""
yaoyao-memory 统一命令行入口

用法：
    python3 cli.py                    # 显示帮助
    python3 cli.py install             # 安装模块
    python3 cli.py status             # 查看状态
    python3 cli.py verify             # 验证安装
    python3 cli.py migrate            # 迁移数据
    python3 cli.py list              # 列出模块
    python3 cli.py health             # 健康检查
    python3 cli.py dashboard         # 启动面板
"""

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent


def cmd_install(args):
    """安装模块"""
    from install_modules import interactive_install, load_modules, load_installed
    
    modules = load_modules()
    installed = load_installed()
    interactive_install(modules, installed)


def cmd_status(args):
    """查看状态"""
    from install_modules import status, load_modules, load_installed
    
    modules = load_modules()
    installed = load_installed()
    status(modules, installed)


def cmd_verify(args):
    """验证安装"""
    from install_modules import verify_installation
    
    if verify_installation():
        print("\n✅ 安装验证通过！")
        sys.exit(0)
    else:
        print("\n❌ 安装验证失败！")
        sys.exit(1)


def cmd_migrate(args):
    """迁移数据"""
    print("请使用：python3 migrate.py --dry")
    print("或：python3 migrate.py --force")


def cmd_list(args):
    """列出模块"""
    from install_modules import list_modules, load_modules, load_installed
    
    modules = load_modules()
    installed = load_installed()
    list_modules(modules, installed)


def cmd_health(args):
    """健康检查"""
    print("运行健康检查...")
    
    try:
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from health_check import main as health_main
        health_main()
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        sys.exit(1)


def cmd_dashboard(args):
    """启动面板"""
    print("启动控制面板...")
    print("按 Ctrl+C 停止")
    
    try:
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from api_server import main as server_main
        server_main()
    except KeyboardInterrupt:
        print("\n\n✅ 面板已停止")
    except Exception as e:
        print(f"❌ 面板启动失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="yaoyao-memory 统一命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 cli.py install      # 交互式安装
  python3 cli.py status       # 查看状态
  python3 cli.py verify       # 验证安装
  python3 cli.py health       # 健康检查
  python3 cli.py dashboard    # 启动面板
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # install
    subparsers.add_parser("install", help="交互式安装模块")
    
    # status
    subparsers.add_parser("status", help="查看安装状态")
    
    # verify
    subparsers.add_parser("verify", help="验证安装完整性")
    
    # migrate
    subparsers.add_parser("migrate", help="迁移数据")
    
    # list
    subparsers.add_parser("list", help="列出所有模块")
    
    # health
    subparsers.add_parser("health", help="运行健康检查")
    
    # dashboard
    subparsers.add_parser("dashboard", help="启动控制面板")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    # 执行对应命令
    commands = {
        "install": cmd_install,
        "status": cmd_status,
        "verify": cmd_verify,
        "migrate": cmd_migrate,
        "list": cmd_list,
        "health": cmd_health,
        "dashboard": cmd_dashboard,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
