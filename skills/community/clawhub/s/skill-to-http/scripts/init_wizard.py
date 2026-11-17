#!/usr/bin/env python3
"""skill-to-http 初始化向导（v2，对齐 HTTP skill TLS+鉴权统一规范）

引导用户完成 8 步配置：
1. Skill 扫描目录
2. Skill 暴露范围（默认全开放 + 反向黑名单）
3. 监听地址和端口
4. API Key（外部调用方鉴权，自动生成 + 持久化到 ~/.http/secrets/）
5. TLS 证书（自动 / 导入 / 不启用）
6. 执行器（auto / openclaw / cc / claude_cli / codex / llm）
7. 并发限制
8. LLM Fallback（可选）

非 TTY 环境：复制默认模板退出
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 导入同级 tls_auth 模块
sys.path.insert(0, str(Path(__file__).parent))
from tls_auth import (  # noqa: E402
    ensure_dirs,
    generate_api_key,
    save_api_key,
    load_api_key,
    DEFAULT_CERT_PATH,
    DEFAULT_KEY_PATH,
    API_KEYS_DIR,
)

SKILL_NAME = "skill-to-http"
from _paths import CONFIG_PATH
TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "config.example.json"

# 推荐拒绝清单（有副作用 / 改系统 / 发外部消息）
# 示例名单：外发消息 / 部署上线 / 发布分发类技能建议默认不暴露，
# 请按你环境中的实际技能名增删。
RECOMMENDED_DENY = [
    "im-send",
    "group-message",
    "site-deploy",
    "app-publish",
    "skill-release",
    "skill-creator",
    "skill-creator-plus",
    "collective-memory",
]


BANNER = """
╔══════════════════════════════════════════════════════════╗
║       🚀 skill-to-http 初始化向导                        ║
║       本向导会引导你配置 HTTPS / API Key / 暴露范围      ║
║       全程可按 Ctrl+C 取消                               ║
╚══════════════════════════════════════════════════════════╝
"""


def _ask(prompt: str, default: str = "", required: bool = False) -> str:
    display = f"{prompt}"
    if default:
        display += f" [{default}]"
    display += ": "
    while True:
        try:
            val = input(display).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已取消。")
            sys.exit(0)
        if val:
            return val
        if default:
            return default
        if not required:
            return ""
        print("  此项必填，请重新输入。")


def _ask_yes_no(prompt: str, default: bool = False) -> bool:
    hint = "(Y/n)" if default else "(y/N)"
    while True:
        try:
            val = input(f"{prompt} {hint}: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n已取消。")
            sys.exit(0)
        if not val:
            return default
        if val in ("y", "yes", "1"):
            return True
        if val in ("n", "no", "0"):
            return False
        print("  请输入 y 或 n。")


def _banner(text: str) -> None:
    print()
    print("─" * 60)
    print(f"  {text}")
    print("─" * 60)


def _detect_workspace() -> str:
    openclaw_ws = os.environ.get("OPENCLAW_WORKSPACE")
    if openclaw_ws:
        return str(Path(openclaw_ws) / "skills")
    candidate = Path.home() / ".openclaw" / "workspace" / "skills"
    return str(candidate)


def _list_installed_skills() -> list[str]:
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    skills_dir = Path(workspace) / "skills"
    if not skills_dir.exists():
        return []
    return sorted([
        entry.name for entry in skills_dir.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").exists()
    ])


def _run_gen_cert():
    """调用同级 gen_cert.py。"""
    script = Path(__file__).parent / "gen_cert.py"
    try:
        subprocess.run([sys.executable, str(script), "--san", "auto", "--force"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  证书生成失败，可稍后手动跑 python3 scripts/gen_cert.py")


def run_interactive() -> dict:
    """TTY 环境：交互式问答生成配置。"""
    print(BANNER)
    config: dict = {}

    # ── 1. Skill 目录 ──────────────────────────────────────────────
    _banner("Step 1/8: Skill 扫描目录")
    default_skill_dir = _detect_workspace()
    print("指定要对外暴露哪些目录下的 Skill")
    skill_dir = _ask("Skill 目录路径", default=default_skill_dir)
    config["skill_dirs"] = [skill_dir, "/app/skills"]

    # ── 2. 暴露范围 ────────────────────────────────────────────────
    _banner("Step 2/8: Skill 暴露范围")
    installed = _list_installed_skills()
    print(f"📦 本机已装 {len(installed)} 个 skill")
    print()
    print("暴露模式：")
    print("  [a] 全开放（默认）— 所有 skill 都可通过 API 执行，配合反向黑名单")
    print("  [b] 白名单 — 只暴露指定 skill（更严格）")
    print("  [n] 不暴露任何 skill（最安全，稍后在 config.json 中调整）")
    mode = _ask("选择 [a/b/n]", default="a").lower()
    if mode == "n":
        config["expose_skills"] = []
        config["deny_skills"] = []
    elif mode == "b":
        names = _ask("输入要暴露的 skill（逗号分隔）", required=True)
        config["expose_skills"] = [s.strip() for s in names.split(",") if s.strip()]
        config["deny_skills"] = []
    else:
        config["expose_skills"] = ["*"]
        suggested = [s for s in RECOMMENDED_DENY if s in installed]
        if suggested:
            print()
            print("推荐拒绝的 skill（有副作用 / 改系统 / 发外部消息）：")
            for s in suggested:
                print(f"  - {s}")
            print()
            deny_choice = _ask("采用推荐清单 [y]，全部允许 [n]，自定义 [c]", default="y").lower()
            if deny_choice == "y":
                config["deny_skills"] = suggested
            elif deny_choice == "c":
                user_deny = _ask("请输入要拒绝的 skill（逗号分隔）", default=",".join(suggested))
                config["deny_skills"] = [s.strip() for s in user_deny.split(",") if s.strip()]
            else:
                config["deny_skills"] = []
                print("⚠️  所有 skill 都将被允许执行，仅靠 API Key 把关")
        else:
            config["deny_skills"] = []

    # ── 3. 监听地址和端口 ───────────────────────────────────────────
    _banner("Step 3/8: 监听地址和端口")
    print("监听地址：")
    print("  0.0.0.0    = 允许内网/外部访问（默认，供其它系统调用）")
    print("  127.0.0.1  = 仅本机访问（最安全，但失去 HTTP 服务意义）")
    config["listen_host"] = _ask("监听地址", default="0.0.0.0")
    config["port"] = int(_ask("监听端口", default="8080"))

    # ── 4. API Key ─────────────────────────────────────────────────
    _banner("Step 4/8: API Key（外部调用方鉴权）")
    existing_api_key = load_api_key(SKILL_NAME)
    if existing_api_key and _ask_yes_no(
        f"已有 API Key（{existing_api_key[:8]}...），继续使用？", default=True
    ):
        config["api_key"] = existing_api_key
    else:
        new_key = generate_api_key()
        path = save_api_key(SKILL_NAME, new_key)
        config["api_key"] = new_key
        print(f"✅ 已生成新 API Key 并保存到：{path}")
    config["api_key_header"] = "X-API-Key"
    print(f"   预览：{config['api_key'][:8]}...{config['api_key'][-4:]}")
    print(f"   💡 调用方需在请求头带 X-API-Key: <key>")

    # ── 5. TLS 证书 ────────────────────────────────────────────────
    _banner("Step 5/8: TLS 证书（HTTPS）")
    print("HTTPS 提供传输层加密，但需要生成自签证书 + 客户端导入，有一定门槛。")
    print()
    print("证书模式：")
    print("  [none]        ★ 默认 - 先用 HTTP 跑通（零门槛，调用方直接 curl 即可）")
    print("  [self-signed] 自动生成自签证书（调用方需 --cacert 或导入信任库）")
    print("  [imported]    导入已有证书（如公司颁发的）")
    if config.get("listen_host") == "0.0.0.0":
        print()
        print("  ⚠️  当前监听 0.0.0.0（局域网可达），如有跨机器调用强烈建议开 HTTPS")
    cert_mode = _ask("证书模式", default="none").lower()

    if cert_mode in ("none", "n"):
        config["tls_enabled"] = False
        # 保留默认 cert/key 路径，用户后续切回 HTTPS 时改一行 tls_enabled 即可
        config["cert_path"] = str(DEFAULT_CERT_PATH)
        config["key_path"] = str(DEFAULT_KEY_PATH)
        print("ℹ️  HTTP 模式（推荐先跑通）。需要切回 HTTPS 时：")
        print("     1. python3 scripts/gen_cert.py --san auto")
        print("     2. 编辑 config.json 把 tls_enabled 改 true")
        print("     3. python3 scripts/server.py restart")
    elif cert_mode in ("imported", "i"):
        config["tls_enabled"] = True
        config["cert_path"] = _ask("证书文件路径（.pem/.crt）", required=True)
        config["key_path"] = _ask("私钥文件路径（.key/.pem）", required=True)
        # 调 gen_cert.py 的 import 流程
        try:
            subprocess.run([
                sys.executable,
                str(Path(__file__).parent / "gen_cert.py"),
                "import",
                "--cert", config["cert_path"],
                "--key", config["key_path"],
            ], check=True)
            # 导入后路径切到统一目录
            config["cert_path"] = str(DEFAULT_CERT_PATH)
            config["key_path"] = str(DEFAULT_KEY_PATH)
        except subprocess.CalledProcessError:
            print("⚠️  证书导入失败，请检查路径")
    else:
        # self-signed（默认）
        config["tls_enabled"] = True
        config["cert_path"] = str(DEFAULT_CERT_PATH)
        config["key_path"] = str(DEFAULT_KEY_PATH)
        if DEFAULT_CERT_PATH.exists():
            print(f"✅ 已有证书：{DEFAULT_CERT_PATH}")
            if _ask_yes_no("是否重新生成（用当前本机 IP 覆盖 SAN）？", default=False):
                _run_gen_cert()
        else:
            print("生成自签证书（含本机 IP 自动嗅探）...")
            _run_gen_cert()

    # ── 6. 执行器 ──────────────────────────────────────────────────
    _banner("Step 6/8: 执行器")
    print("可选：auto（自动检测，推荐） / openclaw / cc / claude_cli / codex / llm")
    executor = _ask("执行器", default="auto")
    config["executor"] = executor

    # ── 7. 并发限制 ────────────────────────────────────────────────
    _banner("Step 7/8: 并发限制")
    concurrent_raw = _ask("最大并发数（0 = 不限制）", default="10")
    try:
        config["max_concurrent"] = int(concurrent_raw)
    except ValueError:
        config["max_concurrent"] = 10

    # ── 8. LLM Fallback ────────────────────────────────────────────
    _banner("Step 8/8: LLM Fallback（可选，仅 executor=llm 时使用）")
    setup_llm = _ask_yes_no("是否配置 LLM API？（不配则 llm executor 不可用）", default=False)
    if setup_llm:
        llm_base = _ask("LLM API 地址", default="https://api.openai.com/v1")
        llm_key = _ask("LLM API Key（或使用 ${ENV_VAR} 引用环境变量）", default="${OPENAI_API_KEY}")
        llm_model = _ask("模型名称", default="gpt-4o")
        config["llm"] = {
            "base_url": llm_base,
            "api_key": llm_key,
            "model": llm_model,
        }
    else:
        config["llm"] = {
            "base_url": "https://api.openai.com/v1",
            "api_key": "${OPENAI_API_KEY}",
            "model": "gpt-4o",
        }

    # ── 其他默认值 ─────────────────────────────────────────────────
    config.setdefault("max_request_size_mb", 1)
    config.setdefault("data_dir", "")
    config.setdefault("disable_docs_without_auth", False)
    config.setdefault("cors", {
        "allow_origins": ["*"],
        "_comment": "默认允许任何源（配合 API Key 已挡 CSRF）；如需 0 信任部署改为 ['https://your-tool.com']",
    })

    return config


def run_non_interactive() -> None:
    """非 TTY 环境：复制模板并退出。"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 优先从 secrets 加载已有 api_key，没有则自动生成（禁止留空）
    existing_key = load_api_key(SKILL_NAME)
    if not existing_key:
        existing_key = generate_api_key()
        save_api_key(SKILL_NAME, existing_key)
        print(f"[skill-to-http] API Key auto-generated (non-interactive): {len(existing_key)} chars, see <HTTP_ROOT>/secrets/api-keys/")

    if TEMPLATE_PATH.exists():
        shutil.copy(TEMPLATE_PATH, CONFIG_PATH)
        # 把自动生成的 api_key 写进模板 copy（模板里可能是空值）
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            if not cfg.get("api_key"):
                cfg["api_key"] = existing_key
                CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
        except Exception:
            pass
        print(f"[skill-to-http] Config template copied to {CONFIG_PATH}")
    else:
        default_cfg = {
            "executor": "auto",
            "expose_skills": ["*"],
            "deny_skills": [],
            "listen_host": "0.0.0.0",
            "port": 8080,
            "tls_enabled": False,
            "cert_path": str(DEFAULT_CERT_PATH),
            "key_path": str(DEFAULT_KEY_PATH),
            "api_key": existing_key,  # 修复：不再留空
            "api_key_header": "X-API-Key",
            "max_concurrent": 10,
            "max_request_size_mb": 1,
            "skill_dirs": [str(Path.home() / ".openclaw" / "workspace" / "skills"), "/app/skills"],
            "data_dir": "",
            "cors": {"allow_origins": ["*"]},
            "llm": {"base_url": "https://api.openai.com/v1", "api_key": "${OPENAI_API_KEY}", "model": "gpt-4o"},
        }
        CONFIG_PATH.write_text(json.dumps(default_cfg, ensure_ascii=False, indent=2))
        print(f"[skill-to-http] Default config created at {CONFIG_PATH}")

    print(f"""
请编辑配置文件后重新启动：

  {CONFIG_PATH}

关键配置项：
  skill_dirs     - 要扫描的 Skill 目录列表
  expose_skills  - 对外暴露的 Skill（["*"] = 全部）
  deny_skills    - 反向黑名单（拒绝执行的 skill）
  api_key        - API Key 认证（必须非空，建议跑 init wizard 自动生成）
  tls_enabled    - 是否启用 HTTPS（默认 false；需要时跑 gen_cert.py + 改 true）

编辑完成后运行：
  cd /path/to/skill-to-http/scripts && python server.py
""")
    sys.exit(1)


def save_config(config: dict) -> None:
    """将配置写入文件。"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except OSError:
        pass


def maybe_run_wizard() -> None:
    """检查 config.json 是否存在，不存在则触发向导。"""
    if CONFIG_PATH.exists():
        return

    if sys.stdin.isatty():
        ensure_dirs()
        config = run_interactive()

        print()
        print("─" * 60)
        print("📋 配置预览（已脱敏）：")
        preview = dict(config)
        if preview.get("api_key"):
            preview["api_key"] = preview["api_key"][:8] + "..." + preview["api_key"][-4:]
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        print("─" * 60)

        confirm = _ask_yes_no("\n保存并启动服务？", default=True)
        if not confirm:
            print("已取消。请手动创建配置文件：")
            print(f"  {CONFIG_PATH}")
            sys.exit(0)

        save_config(config)
        print(f"\n✓ 配置已保存到 {CONFIG_PATH}")
        print(f"  API Key  : {API_KEYS_DIR / (SKILL_NAME + '.key')}")
        if config.get("tls_enabled"):
            print(f"  TLS 证书 : {config.get('cert_path')}")
        print("\n🚀 正在启动服务...\n")
    else:
        run_non_interactive()


if __name__ == "__main__":
    maybe_run_wizard()
    print("Config already exists, nothing to do.")
