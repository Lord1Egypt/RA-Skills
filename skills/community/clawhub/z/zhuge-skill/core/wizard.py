"""引导式安装 wizard"""
import os
import sys
import json
from pathlib import Path

from core.welcome import (GOLD, NEON_CYAN as CYAN, HOT_RED as RED,
                          NEON_GREEN as GREEN, GRAY, DIM, BOLD,
                          NEON_PURPLE as PURPLE, RESET)

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"


# === 工具函数 ===

def step(num, total, title):
    print(f"\n{BOLD}{CYAN}[{num}/{total}]{RESET} {BOLD}{title}{RESET}")
    print(f"  {DIM}{'─' * 45}{RESET}")


def ask(prompt, default=None, choices=None):
    """问用户问题，支持默认值和选项"""
    if choices:
        opts = "/".join([c.upper() if c == default else c for c in choices])
        prompt = f"  {prompt} [{opts}]: "
    elif default:
        prompt = f"  {prompt} [{DIM}{default}{RESET}]: "
    else:
        prompt = f"  {prompt}: "
    try:
        ans = input(prompt).strip()
    except EOFError:
        ans = ""
    if not ans and default is not None:
        return default
    if choices:
        return ans.lower() if ans.lower() in choices else default
    return ans


def confirm(prompt, default=True):
    """y/n 确认"""
    d = "Y/n" if default else "y/N"
    try:
        ans = input(f"  {prompt} [{d}]: ").strip().lower()
    except EOFError:
        ans = ""
    if not ans:
        return default
    return ans in ("y", "yes")


def write_env(values):
    """写 .env 文件"""
    lines = ["# 诸葛亮 · AI 推演军师 — 自动生成的配置\n"]
    for k, v in values.items():
        if v:
            lines.append(f"{k}={v}\n")
    ENV_FILE.write_text("".join(lines), encoding="utf-8")


# === Wizard 主流程 ===

def run_wizard():
    """引导式设置 + demo 演示"""
    print(f"\n  {BOLD}30 秒上手指引{RESET}")
    print(f"  {DIM}（按 Ctrl+C 随时退出）{RESET}\n")

    # === Step 1: 环境检查 ===
    step(1, 4, "环境检查")

    # Python 版本
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    py_ok = sys.version_info >= (3, 9)
    print(f"  {'✓' if py_ok else '✗'} Python {py_ver} {'(OK)' if py_ok else '(需要 3.9+)'}")
    if not py_ok:
        print(f"  {RED}请升级 Python 后重试{RESET}")
        return

    # 依赖
    deps_ok = True
    try:
        import requests  # noqa
        print(f"  {GREEN}✓{RESET} requests 已安装")
    except ImportError:
        print(f"  {RED}✗{RESET} requests 未安装")
        deps_ok = False

    if not deps_ok:
        print()
        if confirm("现在自动安装依赖？", default=True):
            os.system(f"{sys.executable} -m pip install -q requests python-dotenv")
            print(f"  {GREEN}✓{RESET} 依赖已安装")
        else:
            print(f"  {GRAY}跳过依赖安装。手动跑: pip install -r requirements.txt{RESET}")

    # === Step 2: API Key 配置 ===
    step(2, 4, "API Key 配置（可跳过 → demo 模式）")

    print(f"  {DIM}本工具支持 3 个数据源 + 12 个 LLM 供应商。{RESET}")
    print(f"  {DIM}全部跳过也能跑 demo（用内置样本数据）。{RESET}\n")

    env_values = {}

    # API-Football（核心）
    if confirm("配置 API-Football？(免费 100 次/日，赔率+H2H+近期状态)", default=False):
        print(f"  {DIM}申请地址: https://www.api-football.com/{RESET}")
        key = ask("  粘贴 API-Football Key", default="")
        if key:
            env_values["API_FOOTBALL_KEY"] = key

    # The Odds API（增强）
    if confirm("配置 The Odds API？(免费 500 次/月，49 家博彩交叉验证)", default=False):
        print(f"  {DIM}申请地址: https://the-odds-api.com/{RESET}")
        key = ask("  粘贴 The Odds API Key", default="")
        if key:
            env_values["THE_ODDS_API_KEY"] = key

    # === Step 3: LLM 供应商 ===
    step(3, 4, "选择 LLM 供应商（可选 → 用于自然语言「丞相评语」）")

    providers = ["none", "deepseek", "doubao", "kimi", "qwen", "zhipu", "claude", "openai"]
    print(f"  {DIM}选项: {' / '.join(providers)}{RESET}")
    p = ask("LLM 供应商", default="none", choices=providers)

    if p != "none":
        env_values["LLM_PROVIDER"] = p
        key_name = f"{p.upper()}_API_KEY"
        key = ask(f"  粘贴 {key_name}", default="")
        if key:
            env_values[key_name] = key

    # 写入 .env
    if env_values:
        write_env(env_values)
        print(f"\n  {GREEN}✓ 配置已写入 .env{RESET}")
    else:
        print(f"\n  {GRAY}跳过配置。后续可编辑 .env.example → .env 启用{RESET}")

    # === Step 4: Demo 演示 ===
    step(4, 4, "演示一次预测（Napoli vs Lazio · 履卦案例）")

    if confirm("现在跑一次 demo 看效果？", default=True):
        print()
        try:
            from scripts.predict import run_demo
            run_demo()
        except Exception as e:
            print(f"  {RED}demo 报错: {e}{RESET}")
            import traceback
            traceback.print_exc()

    # === 完成 ===
    print(f"\n  {DIM}═══════════════════════════════════════════════{RESET}")
    print(f"  {BOLD}{GREEN}✓ 设置完成！{RESET}\n")
    print(f"  {BOLD}下一步可以做的事：{RESET}\n")
    print(f"    {CYAN}python start.py demo{RESET}                    再看一次 demo")
    print(f"    {CYAN}python start.py predict \"Chelsea vs Man Utd\"{RESET}  预测一场")
    print(f"    {CYAN}python start.py stats{RESET}                   看历史命中率")
    print()
    print(f"    {DIM}详细文档：cat README.md{RESET}")
    print(f"    {DIM}经验库：data/seed_experience.jsonl ({_count_seed()} 条种子){RESET}")
    print()


def _count_seed():
    p = ROOT / "data" / "seed_experience.jsonl"
    if not p.exists():
        return 0
    with open(p, encoding="utf-8") as f:
        return sum(1 for _ in f)
