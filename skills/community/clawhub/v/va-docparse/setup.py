#!/usr/bin/env python3
"""
Docparse MCP Skill — 自动安装与配置注入脚本

功能：
  1. 自动识别 OpenClaw 安装路径与 workspace 位置
  2. 安装 Python 依赖（fastmcp, mcp）
  3. 创建 .env 配置文件（如不存在）
  4. 将 MCP Server 配置注入 openclaw.json
  5. 检测并修复 docparse.py 中硬编码的路径，使其自适应

用法：
  python setup.py                          # 交互式安装
  python setup.py --mcp-url URL            # 非交互式，指定 MCP 地址
  python setup.py --mcp-url URL --api-key KEY  # 完整配置
  python setup.py --dry-run                # 预览操作
  python setup.py --uninstall              # 卸载 MCP 配置

"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ── 路径发现 ──────────────────────────────────────────────

def find_openclaw_dir() -> Path:
    """查找 ~/.openclaw 目录"""
    home = Path.home()
    oclaw = home / ".openclaw"
    if oclaw.is_dir():
        return oclaw
    # 尝试从环境变量
    env_path = os.environ.get("OPENCLAW_DIR")
    if env_path:
        p = Path(env_path)
        if p.is_dir():
            return p
    print(f"[!] 未找到 ~/.openclaw 目录，请确认 OpenClaw 已安装。")
    sys.exit(1)


def find_workspace_dir(oclaw_dir: Path) -> Path:
    """从 openclaw.json 或默认位置找到 workspace"""
    config_path = oclaw_dir / "openclaw.json"
    if config_path.is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            ws = config.get("agents", {}).get("defaults", {}).get("workspace")
            if ws and Path(ws).is_dir():
                return Path(ws)
        except Exception:
            pass
    # 默认
    return oclaw_dir / "workspace"


def find_skill_dir(workspace: Path) -> Path:
    """当前脚本所在的 skill 目录（docparse/）"""
    script = Path(__file__).resolve()
    # setup.py 在 skills/docparse/ 下
    return script.parent


# ── 配置文件操作 ──────────────────────────────────────────

def load_openclaw_config(oclaw_dir: Path) -> dict:
    """加载 openclaw.json"""
    config_path = oclaw_dir / "openclaw.json"
    if not config_path.is_file():
        print(f"[!] 未找到配置文件: {config_path}")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_openclaw_config(config: dict, oclaw_dir: Path):
    """保存 openclaw.json（备份原件）"""
    config_path = oclaw_dir / "openclaw.json"
    backup = config_path.with_suffix(".json.bak")
    import shutil
    shutil.copy2(config_path, backup)
    print(f"  ✅ 已备份原配置 → {backup}")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  ✅ 已更新配置   → {config_path}")


def ensure_env_file(skill_dir: Path, mcp_url: str, api_key: str, timeout: str, dry_run: bool):
    """创建 .env 文件（如不存在）"""
    env_path = skill_dir / ".env"

    lines = [
        "# 文档解析 MCP 服务配置",
        f"DOCPARSE_MCP_URL={mcp_url}",
        f"DOCPARSE_API_KEY={api_key if api_key else 'your-api-key'}",
        f"DOCPARSE_TIMEOUT={timeout}",
    ]
    content = "\n".join(lines) + "\n"

    if env_path.is_file():
        print(f"  ℹ️  .env 已存在: {env_path}")
        # 检查是否需要更新
        with open(env_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if f"DOCPARSE_MCP_URL={mcp_url}" in existing:
            print(f"  ✅ .env 配置已是最新")
            return
        print(f"  🔄 .env 内容需要更新...")

    if not dry_run:
        env_path.parent.mkdir(parents=True, exist_ok=True)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ 已写入 .env → {env_path}")
    else:
        print(f"  [dry-run] 将写入 .env → {env_path}")
        print(f"  [dry-run] 内容:\n{content}")


def inject_mcp_config(config: dict, skill_dir: Path, mcp_url: str, api_key: str, timeout: str, dry_run: bool):
    """将 docparse MCP Server 注入 openclaw.json"""
    mcp_script = skill_dir / "mcp" / "docparse.py"
    if not mcp_script.is_file():
        print(f"  [!] 未找到 MCP 脚本: {mcp_script}")
        return

    mcp_section = config.setdefault("mcp", {}).setdefault("servers", {})

    existing = mcp_section.get("docparse", {})
    current_url = existing.get("env", {}).get("DOCPARSE_MCP_URL", "")

    if current_url == mcp_url and existing.get("args") == [str(mcp_script)]:
        print(f"  ✅ openclaw.json 中 docparse MCP 配置已是最新")
        return

    mcp_section["docparse"] = {
        "command": "python",
        "args": [str(mcp_script)],
        "env": {
            "DOCPARSE_MCP_URL": mcp_url,
            "DOCPARSE_API_KEY": api_key,
            "DOCPARSE_TIMEOUT": timeout,
        }
    }

    if dry_run:
        print(f"  [dry-run] 将注入 mcp.servers.docparse:")
        print(f"  [dry-run] {json.dumps(mcp_section['docparse'], indent=4)}")
    else:
        print(f"  ✅ 已注入 mcp.servers.docparse → openclaw.json")


def fix_hardcoded_paths(skill_dir: Path, dry_run: bool):
    """检查 docparse.py 是否有硬编码路径问题"""
    mcp_script = skill_dir / "mcp" / "docparse.py"
    if not mcp_script.is_file():
        return

    with open(mcp_script, "r", encoding="utf-8") as f:
        content = f.read()

    issues = []

    # 检查是否使用 _SCRIPT_DIR = Path(__file__).resolve().parent
    if "_SCRIPT_DIR = Path(__file__)" in content:
        print("  ✅ docparse.py 已使用 __file__ 自适应路径")
    elif "_OPENCLAW_CONFIG_PATH = Path.home() / '.openclaw'" in content:
        print("  ✅ docparse.py 已使用 Path.home() 定位 openclaw.json")
    else:
        issues.append("docparse.py 可能包含硬编码路径")

    if issues and not dry_run:
        print(f"  ⚠️  路径检查发现问题: {'; '.join(issues)}")
    elif issues and dry_run:
        print(f"  [dry-run] 路径检查发现问题: {'; '.join(issues)}")


# ── 依赖安装 ──────────────────────────────────────────────

def install_dependencies(skill_dir: Path, dry_run: bool):
    """安装 Python 依赖"""
    req_file = skill_dir / "requirements.txt"

    # 先检查是否已安装
    try:
        import fastmcp  # noqa: F401
        import mcp      # noqa: F401
        print("  ✅ Python 依赖已安装 (fastmcp, mcp)")
        return
    except ImportError:
        pass

    if not req_file.is_file():
        print("  ℹ️  requirements.txt 不存在，直接安装已知依赖")
        packages = ["fastmcp>=3.0.0", "mcp>=1.0.0"]
    else:
        packages = None

    cmd = None
    if packages:
        cmd = [sys.executable, "-m", "pip", "install"] + packages
    elif req_file.is_file():
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file)]

    if cmd is None:
        print("  [!] 无法确定安装命令")
        return

    if dry_run:
        print(f"  [dry-run] 将执行: {' '.join(cmd)}")
        return

    print(f"  🔄 安装依赖: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("  ✅ 依赖安装成功")
        else:
            print(f"  ⚠️  依赖安装可能有问题:\n{result.stderr[-500:] if result.stderr else ''}")
            print("  💡 请手动运行: pip install fastmcp>=3.0.0 mcp>=1.0.0")
    except subprocess.TimeoutExpired:
        print("  ⚠️  安装超时，请手动运行 pip install")


# ── 卸载 ──────────────────────────────────────────────────

def uninstall(oclaw_dir: Path, dry_run: bool):
    """从 openclaw.json 中移除 docparse MCP 配置"""
    config = load_openclaw_config(oclaw_dir)

    if "mcp" not in config or "servers" not in config.get("mcp", {}):
        print("  ℹ️  openclaw.json 中不存在 MCP 配置")
        return

    if "docparse" not in config["mcp"]["servers"]:
        print("  ℹ️  openclaw.json 中不存在 docparse MCP 配置")
        return

    if dry_run:
        print("  [dry-run] 将从 mcp.servers 中移除 docparse")
        return

    removed = config["mcp"]["servers"].pop("docparse")
    print("  ✅ 已移除 docparse MCP 配置:")
    print(f"     {json.dumps(removed, indent=6)}")
    save_openclaw_config(config, oclaw_dir)


# ── 主流程 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Docparse MCP Skill 自动安装与配置注入",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --mcp-url http://10.24.9.2:8097/mcp
  %(prog)s --mcp-url http://10.24.9.2:8097/mcp --api-key my-secret-key
  %(prog)s --dry-run --mcp-url http://10.24.9.2:8097/mcp
        """
    )
    parser.add_argument("--mcp-url", type=str, help="文档解析 MCP 服务地址")
    parser.add_argument("--api-key", type=str, default="", help="API 密钥")
    parser.add_argument("--timeout", type=str, default="7200", help="超时时间（秒，默认 7200）")
    parser.add_argument("--dry-run", action="store_true", help="预览操作，不实际修改")
    parser.add_argument("--uninstall", action="store_true", help="卸载 MCP 配置")
    parser.add_argument("--skip-deps", action="store_true", help="跳过依赖安装")
    parser.add_argument("--oclaw-dir", type=str, help="自定义 .openclaw 目录路径")

    args = parser.parse_args()

    # 卸载模式
    if args.uninstall:
        print("=" * 60)
        print("🔧 Docparse MCP Skill — 卸载模式")
        print("=" * 60)
        oclaw_dir = Path(args.oclaw_dir) if args.oclaw_dir else find_openclaw_dir()
        uninstall(oclaw_dir, args.dry_run)
        return

    print("=" * 60)
    print("🔧 Docparse MCP Skill — 自动安装与配置")
    print("=" * 60)

    # 交互式获取参数
    interactive_mode = not args.mcp_url  # 无 --mcp-url 则走交互式引导

    mcp_url = args.mcp_url
    if not mcp_url:
        if args.dry_run:
            print("[dry-run] 使用示例 URL")
            mcp_url = "http://example.com:8097/mcp"
        else:
            mcp_url = input(
                "\n请输入文档解析 MCP 服务地址:\n"
                "  格式示例: http://10.24.9.2:8097/mcp\n"
                "  格式示例: http://your-server.local:8097/mcp\n"
                "> ").strip()
            if not mcp_url:
                print("[!] MCP 地址不能为空")
                sys.exit(1)

    api_key = args.api_key
    if not api_key and interactive_mode and not args.dry_run:
        key_input = input(
            "\n请输入 API Key（可选，直接回车跳过）:\n"
            "  格式示例: sk-xxxxxxxxxxxxxxxxxxxxxxxx\n"
            "  格式示例: your-secret-key-here\n"
            "> ").strip()
        api_key = key_input if key_input else ""

    timeout = args.timeout
    if interactive_mode and not args.dry_run:
        t_input = input(
            f"\n请输入超时时间（秒，默认 {timeout}）:\n"
            "  格式示例: 7200 (2小时)\n"
            "  格式示例: 3600 (1小时)\n"
            "> ").strip()
        timeout = t_input if t_input else timeout

    # 路径发现
    oclaw_dir = Path(args.oclaw_dir) if args.oclaw_dir else find_openclaw_dir()
    workspace = find_workspace_dir(oclaw_dir)
    skill_dir = find_skill_dir(workspace)

    print(f"\n📂 路径信息:")
    print(f"  OpenClaw 目录 : {oclaw_dir}")
    print(f"  Workspace    : {workspace}")
    print(f"  Skill 目录    : {skill_dir}")
    print(f"  MCP 脚本      : {skill_dir / 'mcp' / 'docparse.py'}")
    print(f"\n⚙️  配置参数:")
    print(f"  MCP URL      : {mcp_url}")
    print(f"  API Key      : {'***' + api_key[-4:] if len(api_key) > 4 else api_key or '(空)'}")
    print(f"  Timeout      : {timeout}s")

    if args.dry_run:
        print(f"\n  🔍 DRY-RUN 模式 — 不会实际修改任何文件")

    print()

    # Step 1: 安装依赖
    if not args.skip_deps:
        print("📦 Step 1: 安装 Python 依赖")
        install_dependencies(skill_dir, args.dry_run)
        print()

    # Step 2: 创建 .env
    print("📝 Step 2: 配置 .env 文件")
    ensure_env_file(skill_dir, mcp_url, api_key, timeout, args.dry_run)
    print()

    # Step 3: 检查路径自适应
    print("🔍 Step 3: 检查 docparse.py 路径配置")
    fix_hardcoded_paths(skill_dir, args.dry_run)
    print()

    # Step 4: 注入 openclaw.json
    print("💉 Step 4: 注入 MCP Server 配置到 openclaw.json")
    config = load_openclaw_config(oclaw_dir)
    inject_mcp_config(config, skill_dir, mcp_url, api_key, timeout, args.dry_run)

    if not args.dry_run:
        save_openclaw_config(config, oclaw_dir)
    print()

    # 完成
    print("=" * 60)
    if args.dry_run:
        print("🔍 DRY-RUN 完成 — 以上为预览，未实际修改任何文件")
    else:
        print("✅ 安装完成！")
        print()
        print("后续操作:")
        print("  1. 重启 OpenClaw Gateway 使配置生效:")
        print("     openclaw gateway restart")
        print("  2. 测试 MCP 连接:")
        print("     python mcp/docparse.py <your-pdf-file>")
    print("=" * 60)


if __name__ == "__main__":
    main()
