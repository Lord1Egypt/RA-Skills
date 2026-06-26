#!/usr/bin/env python3
"""
Memory Manager 首次使用引导脚本

用法:
    python memory_onboard.py              # 交互式引导
    python memory_onboard.py --silent     # 静默模式 (使用默认/参数)

首次运行会自动引导用户完成:
1. 配置用户名
2. 选择 Embedding 后端
3. 输入 API Key
4. 初始化记忆仓库
"""

import os
import sys
import json
import getpass
from pathlib import Path
from datetime import datetime

# 版本信息
VERSION = "3.5.0"

# ══════════════════════════════════════════════════════════════
#  颜色输出
# ══════════════════════════════════════════════════════════════

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
except ImportError:
    # Fallback: 无颜色
    RESET = BOLD = RED = GREEN = YELLOW = CYAN = MAGENTA = ""

def print_banner():
    """打印欢迎横幅"""
    print(f"""
{MAGENTA}╔════════════════════════════════════════════════════════════╗{RESET}
{MAGENTA}║                                                            ║{RESET}
{MAGENTA}║          🎉 Memory Manager 首次使用引导                    ║{RESET}
{MAGENTA}║                                                            ║{RESET}
{MAGENTA}║              版本: v{VERSION}{' ' * (37 - len(VERSION))}║{RESET}
{MAGENTA}║                                                            ║{RESET}
{MAGENTA}╚════════════════════════════════════════════════════════════╝{RESET}
    """)

def print_step(step, total, title):
    """打印步骤标题"""
    print(f"\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n{CYAN}[{step}/{total}] {title}{RESET}\n")

def print_success(msg):
    print(f"  {GREEN}✅ {msg}{RESET}")

def print_info(msg):
    print(f"  {CYAN}ℹ️  {msg}{RESET}")

def print_warn(msg):
    print(f"  {YELLOW}⚠️  {msg}{RESET}")

def print_error(msg):
    print(f"  {RED}❌ {msg}{RESET}")

def print_box(title, lines=None):
    """打印带边框的文本块"""
    print(f"\n{CYAN}┌{'─' * 58}┐{RESET}")
    print(f"{CYAN}│{RESET}  {BOLD}{title}{RESET}{' ' * (54 - len(title))}{CYAN}│{RESET}")
    if lines:
        for line in lines:
            print(f"{CYAN}│{RESET}  {line}{' ' * (54 - len(line))}{CYAN}│{RESET}")
    print(f"{CYAN}└{'─' * 58}┘{RESET}")

# ══════════════════════════════════════════════════════════════
#  用户输入
# ══════════════════════════════════════════════════════════════

def input_text(prompt, default=None, required=False, password=False):
    """安全的用户输入"""
    if default:
        prompt_full = f"{prompt} [{default}]: "
    else:
        prompt_full = f"{prompt}: "

    while True:
        try:
            if password:
                value = getpass.getpass(prompt_full)
            else:
                value = input(prompt_full).strip()

            if not value and default:
                value = default

            if required and not value:
                print_warn("此项为必填项")
                continue

            return value
        except (KeyboardInterrupt, EOFError):
            print("\n\n已取消")
            sys.exit(0)

def input_choice(prompt, options, default=0):
    """选择输入"""
    print(f"\n{prompt}")
    for i, (key, desc) in enumerate(options):
        marker = "(推荐)" if i == default else ""
        print(f"  {CYAN}[{i + 1}]{RESET} {desc} {YELLOW}{marker}{RESET}")

    while True:
        try:
            choice = input(f"\n请选择 [{default + 1}]: ").strip()
            if not choice:
                choice = str(default + 1)
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][0]
            print_warn(f"请输入 1-{len(options)} 之间的数字")
        except ValueError:
            print_warn("请输入有效数字")

def input_yes_no(prompt, default=True):
    """是/否输入"""
    default_str = "[Y/n]" if default else "[y/N]"
    while True:
        try:
            response = input(f"{prompt} {default_str}: ").strip().lower()
            if not response:
                return default
            if response in ('y', 'yes', '是'):
                return True
            if response in ('n', 'no', '否'):
                return False
            print_warn("请输入 y/n")
        except (KeyboardInterrupt, EOFError):
            print("\n已取消")
            sys.exit(0)

# ══════════════════════════════════════════════════════════════
#  配置步骤
# ══════════════════════════════════════════════════════════════

def step_user_info():
    """步骤 1: 用户信息"""
    print_step(1, 5, "配置用户信息")

    # 获取默认用户名
    default_user = os.environ.get("USER") or os.environ.get("USERNAME") or "user"

    user_name = input_text("👤 请输入用户名 (用于区分多用户)", default=default_user, required=True)
    print_success(f"用户 ID: {user_name}")

    return {"uid": user_name}

def step_backend():
    """步骤 2: 选择后端"""
    print_step(2, 5, "选择 Embedding 后端")

    backends = [
        ("openai", "OpenAI (推荐, 需要 API Key)"),
        ("siliconflow", "SiliconFlow (国内可用)"),
        ("zhipu", "Zhipu (国内可用)"),
    ]

    backend = input_choice("🌐 选择 Embedding 服务:", backends, default=0)
    print_success(f"后端: {backend}")

    return {"backend": backend}

def step_api_key(config):
    """步骤 3: 配置 API Key"""
    print_step(3, 5, "配置 API Key")

    backend = config["backend"]
    env_vars = {
        "openai": "OPENAI_API_KEY",
        "siliconflow": "SILICONFLOW_API_KEY",
        "zhipu": "ZHIPU_API_KEY",
    }
    prompts = {
        "openai": "OpenAI API Key (sk-...)",
        "siliconflow": "SiliconFlow API Key",
        "zhipu": "Zhipu API Key",
    }

    env_var = env_vars[backend]

    # 检查环境变量
    existing_key = os.environ.get(env_var, "")
    if existing_key and existing_key.startswith("sk-"):
        print_success(f"检测到已配置的环境变量 {env_var}")
        if input_yes_no("是否使用已保存的 Key?", default=True):
            return {"api_key": existing_key, "env_var": env_var}

    # 交互输入
    print_info(f"\n请前往以下网址获取 {backend} API Key:")
    urls = {
        "openai": "https://platform.openai.com/api-keys",
        "siliconflow": "https://siliconflow.cn/",
        "zhipu": "https://open.bigmodel.cn/",
    }
    print(f"  {CYAN}{urls.get(backend, '')}{RESET}\n")

    api_key = input_text(prompts[backend], password=True)

    if api_key:
        print_success("API Key 已记录")
        return {"api_key": api_key, "env_var": env_var}
    else:
        print_warn("未输入 API Key，尝试使用环境变量方式")
        return {"api_key": "", "env_var": env_var}

def step_memory_path():
    """步骤 4: 记忆仓库路径"""
    print_step(4, 5, "设置记忆仓库")

    script_dir = Path(__file__).parent.parent
    default_path = str(script_dir / "memory")

    memory_path = input_text("📁 记忆仓库路径", default=default_path)

    # 验证/创建目录
    path = Path(memory_path).resolve()
    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"目录已创建: {path}")
        except Exception as e:
            print_error(f"无法创建目录: {e}")
            sys.exit(1)

    print_success(f"记忆仓库: {path}")
    return {"base_dir": str(path)}

def step_git_sync(config):
    """步骤 5: GitHub 同步"""
    print_step(5, 5, "GitHub 同步 (可选)")

    if not input_yes_no("是否配置 GitHub 同步?", default=False):
        print_info("跳过 GitHub 配置")
        return {"git_sync": False}

    repo_url = input_text("🔗 GitHub 仓库 URL (git@github.com:user/repo.git)")
    if not repo_url:
        print_info("跳过 GitHub 配置")
        return {"git_sync": False}

    return {"git_sync": True, "repo_url": repo_url}

# ══════════════════════════════════════════════════════════════
#  保存配置
# ══════════════════════════════════════════════════════════════

def save_config(config):
    """保存配置到文件"""
    # 全局配置
    config_dir = Path.home() / ".memory-manager"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "config.json"

    # 移除敏感信息
    save_data = {k: v for k, v in config.items() if k != "api_key"}
    save_data["version"] = VERSION
    save_data["created"] = datetime.now().isoformat()

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=4, ensure_ascii=False)

    print_success(f"配置已保存: {config_path}")

    # 本地配置
    base_dir = config.get("base_dir", ".")
    local_config_path = Path(base_dir) / ".mm.json"

    local_config = {
        "default": {
            "uid": config.get("uid"),
            "base_dir": base_dir,
            "scope": "private"
        }
    }

    with open(local_config_path, "w", encoding="utf-8") as f:
        json.dump(local_config, f, indent=4, ensure_ascii=False)

    print_success(f"本地配置: {local_config_path}")

    # API Key 到环境变量
    if config.get("api_key") and config.get("env_var"):
        # 打印建议添加到 shell 配置
        print_info("\n建议将以下内容添加到 ~/.bashrc 或 ~/.zshrc:")
        print(f"  {CYAN}export {config['env_var']}='{config['api_key'][:10]}...'{RESET}")

def init_directories(config):
    """初始化目录结构"""
    base_dir = Path(config["base_dir"])
    uid = config["uid"]

    # 公共目录
    shared_dirs = [
        base_dir / "shared" / "daily",
        base_dir / "shared" / "weekly",
        base_dir / "shared" / "permanent",
    ]

    # 用户目录
    user_dirs = [
        base_dir / "users" / uid / "daily",
        base_dir / "users" / uid / "weekly",
        base_dir / "users" / uid / "permanent",
    ]

    for d in shared_dirs + user_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 创建 INDEX.md
    index_path = base_dir / "users" / uid / "INDEX.md"
    if not index_path.exists():
        index_content = f"""# 用户索引 - {uid}

## 基本信息
- 用户名: {uid}
- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- 版本: v{VERSION}

## 记忆层级
| 层级 | 位置 | 说明 |
|------|------|------|
| L1 临时 | `daily/` | 当天记录，自动清理 |
| L2 长期 | `weekly/` | 本周总结 |
| L3 永久 | `permanent/` | 重要记忆，长期保存 |

## 快速命令
```bash
mm log "记录内容"    # 快速记录
mm search "关键词"   # 搜索
mm insight           # AI 总结
mm stats             # 统计
```

## 使用提示
- 重要记忆标记 `[IMPORTANT]` 可自动升级到 L2
- 永久记忆标记 `[PERMANENT]` 可升级到 L3
- 运行 `mm --help` 查看所有命令
"""
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

    print_success("目录结构初始化完成")

# ══════════════════════════════════════════════════════════════
#  完成
# ══════════════════════════════════════════════════════════════

def show_completion(config):
    """显示完成信息"""
    print(f"""
{GREEN}╔════════════════════════════════════════════════════════════╗{RESET}
{GREEN}║                                                            ║{RESET}
{GREEN}║  ✅ Memory Manager 配置完成！                              ║{RESET}
{GREEN}║                                                            ║{RESET}
{GREEN}╚════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📖 快速开始:{RESET}

  {CYAN}mm log "这是我的第一条记忆"{RESET}   # 📝 记录记忆
  {CYAN}mm search "查找相关内容"{RESET}       # 🔍 语义搜索
  {CYAN}mm insight{RESET}                      # 🧠 AI 自我总结
  {CYAN}mm stats{RESET}                        # 📊 查看统计

{BOLD}📚 详细文档:{RESET}

  SKILL.md      - AI 使用的 Skill 文档
  README.md     - 完整使用说明
  reference.md  - 命令参考手册

{BOLD}⚠️  重要提示:{RESET}

  1. 请确保 API Key 已配置 (环境变量或 shell 配置)
  2. 运行 `mm embed` 生成向量索引
  3. 运行 `mm sync` 同步到 GitHub (如已配置)
  4. 查看 INDEX.md 了解记忆组织方式

""")

# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Memory Manager 首次使用引导",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--silent", action="store_true", help="静默模式")
    parser.add_argument("--uid", help="用户名")
    parser.add_argument("--backend", choices=["openai", "siliconflow", "zhipu"], help="Embedding 后端")
    parser.add_argument("--path", dest="base_dir", help="记忆仓库路径")
    parser.add_argument("--skip-git", action="store_true", help="跳过 Git 配置")

    args = parser.parse_args()

    print_banner()

    config = {}

    # 静默模式
    if args.silent or args.uid:
        config["uid"] = args.uid or os.environ.get("USER", "user")
        config["backend"] = args.backend or "openai"
        config["base_dir"] = args.base_dir or "./memory"
        config["git_sync"] = False

        # 尝试从环境变量获取 API Key
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "siliconflow": "SILICONFLOW_API_KEY",
            "zhipu": "ZHIPU_API_KEY",
        }
        config["api_key"] = os.environ.get(env_vars.get(config["backend"], ""), "")
        config["env_var"] = env_vars.get(config["backend"], "")
    else:
        # 交互模式
        config.update(step_user_info())
        config.update(step_backend())
        config.update(step_api_key(config))
        config.update(step_memory_path())

        if not args.skip_git:
            config.update(step_git_sync(config))
        else:
            config["git_sync"] = False

    # 保存配置
    print("\n" + "─" * 60)
    save_config(config)
    init_directories(config)

    # 完成
    show_completion(config)

if __name__ == "__main__":
    main()
