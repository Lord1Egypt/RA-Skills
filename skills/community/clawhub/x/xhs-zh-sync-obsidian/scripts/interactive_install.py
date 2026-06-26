#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from common import DEFAULT_CONFIG_PATH, SKILL_ROOT, expand_path, load_config


DEFAULT_TZ = "Asia/Shanghai"


DEFAULT_CLASSIFY_RULES = """rules:
  - level1: "技术"
    level2: "AI"
    keywords: ["AI", "LLM", "模型", "agent", "机器学习", "提示词"]
  - level1: "技术"
    level2: "开发"
    keywords: ["Python", "JavaScript", "代码", "架构", "数据库", "工程"]
  - level1: "知识"
    level2: "读书"
    keywords: ["读书", "书摘", "阅读", "作者", "出版"]
  - level1: "知识"
    level2: "商业"
    keywords: ["商业", "创业", "产品", "增长", "管理", "公司"]
  - level1: "生活"
    level2: "旅行"
    keywords: ["旅行", "城市", "路线", "酒店", "攻略"]
  - level1: "生活"
    level2: "健康"
    keywords: ["健康", "运动", "睡眠", "饮食", "医学"]
"""


def prompt(text: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{text}{suffix}: ").strip()
    return value if value else (default or "")


def yes_no(text: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    while True:
        value = input(f"{text} [{hint}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes", "是", "好"}:
            return True
        if value in {"n", "no", "否", "不"}:
            return False
        print("请输入 y 或 n。")


def choose(text: str, options: list[tuple[str, str]], default: str) -> str:
    print(text)
    for key, label in options:
        print(f"  {key}. {label}")
    valid = {key for key, _ in options}
    while True:
        value = prompt("请选择", default)
        if value in valid:
            return value
        print(f"请输入其中一个选项：{', '.join(sorted(valid))}")


def run(cmd: list[str], *, cwd: Path = SKILL_ROOT, check: bool = True) -> int:
    print("+ " + " ".join(str(x) for x in cmd))
    code = subprocess.call([str(x) for x in cmd], cwd=str(cwd))
    if check and code != 0:
        raise SystemExit(code)
    return code


def python_cmd() -> str:
    return sys.executable or "python"


def npm_cmd() -> str | None:
    return shutil.which("npm.cmd") or shutil.which("npm")


def ob_cmd() -> str | None:
    return shutil.which("ob.cmd") or shutil.which("ob")


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def read_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def update_env(path: Path, updates: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        if "=" not in line or line.strip().startswith("#"):
            out.append(line)
            continue
        key = line.split("=", 1)[0].strip()
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key, value in updates.items():
        if key not in seen:
            out.append(f"{key}={value}")
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def no_proxy_value(server_url: str) -> str:
    host = urlparse(server_url).hostname or ""
    values = [host, "127.0.0.1", "localhost"]
    return ",".join(x for x in values if x)


def config_cookie_env(config_path: Path) -> Path:
    try:
        config = load_config(config_path)
        return expand_path(config["cookiecloud_env"])
    except Exception:
        return expand_path("~/.config/social-favorites-to-obsidian/cookiecloud.env")


def classify_rules_path(config_path: Path) -> Path:
    try:
        config = load_config(config_path)
        return expand_path(config["classification"]["rules_file"])
    except Exception:
        return expand_path("~/.config/social-favorites-to-obsidian/classify_rules.yaml")


def local_ip_hint() -> str:
    return "http://<本机局域网IP>:8088"


def install_local_cookiecloud() -> str:
    compose_dir = expand_path("~/.config/social-favorites-to-obsidian/cookiecloud")
    compose_dir.mkdir(parents=True, exist_ok=True)
    compose_file = compose_dir / "docker-compose.yml"
    if not compose_file.exists():
        shutil.copyfile(SKILL_ROOT / "assets" / "docker-compose.cookiecloud.yml", compose_file)
    if not command_exists("docker"):
        print("[warn] 未找到 docker。已写入 compose 文件，但无法自动启动 CookieCloud。")
        print(f"       compose 文件: {compose_file}")
        return "http://127.0.0.1:8088"
    run(["docker", "compose", "-f", str(compose_file), "up", "-d", "cookiecloud"], check=False)
    return "http://127.0.0.1:8088"


def install_ob_headless() -> None:
    if ob_cmd():
        print("[ok] ob 命令已存在")
        return
    npm = npm_cmd()
    if not npm:
        raise SystemExit("未找到 npm。请先安装 Node.js 22+ 和 npm。")
    run([npm, "install", "-g", "obsidian-headless"])


def write_default_classification(config_path: Path) -> Path:
    path = classify_rules_path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DEFAULT_CLASSIFY_RULES, encoding="utf-8")
    return path


def detect_openclaw() -> bool:
    return command_exists("openclaw") or (Path.home() / ".openclaw").exists()


def write_cron_specs(config_path: Path, timezone: str) -> list[Path]:
    out_dir = expand_path("~/.config/social-favorites-to-obsidian")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for platform, default_time in (("xhs", "06:00"), ("zhihu", "05:00")):
        time_text = prompt(f"{platform} 每日同步时间 HH:MM", default_time)
        proc = subprocess.run(
            [
                python_cmd(),
                str(SKILL_ROOT / "scripts" / "install_cron.py"),
                "--platform",
                platform,
                "--time",
                time_text,
                "--timezone",
                timezone,
                "--config",
                str(config_path),
                "--print",
            ],
            cwd=str(SKILL_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        target = out_dir / f"openclaw-cron-{platform}.json"
        target.write_text(proc.stdout, encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactive installer for social-favorites-to-obsidian.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--non-interactive", action="store_true", help="Reserved for future automation; currently unsupported.")
    args = parser.parse_args()
    if args.non_interactive:
        raise SystemExit("--non-interactive 尚未实现；请使用交互模式。")

    config_path = expand_path(args.config)
    external_todos: list[str] = []

    print("\nSocial Favorites to Obsidian - 交互式安装\n")

    cookie_mode = choose(
        "CookieCloud 服务端部署方式",
        [("1", "本机 Docker 安装 CookieCloud 服务端"), ("2", "使用已有 CookieCloud 服务端")],
        "1",
    )
    cookie_server_url = "http://127.0.0.1:8088"
    browser_cookie_url = cookie_server_url
    remote_cookie_updates: dict[str, str] = {}
    if cookie_mode == "1":
        if yes_no("是否确认本机已有 Docker / Docker Compose 环境？", True):
            cookie_server_url = install_local_cookiecloud()
        else:
            print("[warn] 跳过 CookieCloud Docker 启动，只继续生成配置和凭据。")
        browser_cookie_url = prompt("Chrome 插件可访问的 CookieCloud 服务地址", local_ip_hint())
    else:
        cookie_server_url = prompt("CookieCloud 服务端地址，例如 http://172.28.102.127:8088")
        uuid = prompt("CookieCloud UUID")
        password = getpass.getpass("CookieCloud Password: ").strip()
        remote_cookie_updates = {
            "COOKIECLOUD_SERVER_URL": cookie_server_url,
            "COOKIECLOUD_UUID": uuid,
            "COOKIECLOUD_PASSWORD": password,
            "COOKIECLOUDUUID": uuid,
            "COOKIECLOUDPASSWORD": password,
        }
        browser_cookie_url = cookie_server_url

    vault_mode = choose(
        "Obsidian vault 与同步方式",
        [
            ("1", "自动创建本地 vault，并使用官方 Obsidian Sync"),
            ("2", "自动创建本地 vault，只本地导出，不自动同步"),
            ("3", "使用当前已有本地 vault 目录"),
        ],
        "2",
    )
    use_headless_sync = vault_mode == "1"
    obsidian_vault = None
    if vault_mode == "3":
        obsidian_vault = prompt("已有本地 vault 目录")
        use_headless_sync = yes_no("这个已有 vault 是否也要配置官方 Obsidian Sync？", False)

    remote_vault = ""
    obsidian_email = ""
    obsidian_password = ""
    sync_password = ""
    if use_headless_sync:
        obsidian_email = prompt("Obsidian 官方账号邮箱/用户名")
        if yes_no("是否现在输入 Obsidian 官方账号密码给 ob login 使用？否则稍后交互输入", False):
            obsidian_password = getpass.getpass("Obsidian 官方账号密码: ").strip()
        remote_vault = prompt("Obsidian Sync 远程 vault 名字或 ID")
        if yes_no("远程 vault 是否需要端到端加密密码？", False):
            sync_password = getpass.getpass("Obsidian Sync 端到端加密密码: ").strip()

    classify_mode = choose(
        "文章分类标准",
        [("1", "由默认 LLM 风格规则初始化分类"), ("2", "用户稍后自行编辑，先使用 其他/待整理")],
        "1",
    )

    init_cmd = [
        python_cmd(),
        str(SKILL_ROOT / "scripts" / "setup.py"),
        "--config",
        str(config_path),
        "--init",
        "--install-skill-deps",
        "--install-python-deps",
        "--install-playwright",
        "--cookiecloud-server-url",
        cookie_server_url,
        "--obsidian-mode",
        "headless-sync" if use_headless_sync else "local-only",
    ]
    if obsidian_vault:
        init_cmd.extend(["--obsidian-vault", obsidian_vault])
    run(init_cmd)

    cookie_env = config_cookie_env(config_path)
    if remote_cookie_updates:
        update_env(cookie_env, remote_cookie_updates)
    update_env(
        cookie_env,
        {
            "NO_PROXY": no_proxy_value(cookie_server_url),
            "no_proxy": no_proxy_value(cookie_server_url),
            "HTTP_PROXY": "",
            "HTTPS_PROXY": "",
            "ALL_PROXY": "",
            "http_proxy": "",
            "https_proxy": "",
            "all_proxy": "",
        },
    )
    env_values = read_env(cookie_env)

    run([python_cmd(), str(SKILL_ROOT / "scripts" / "patch_hctec_zhihu_format.py"), "--config", str(config_path)])

    if classify_mode == "1":
        rules_path = write_default_classification(config_path)
        print(f"[ok] 已写入默认分类规则: {rules_path}")

    if use_headless_sync:
        install_ob_headless()
        ob = ob_cmd()
        if not ob:
            raise SystemExit("obsidian-headless 安装后仍未找到 ob 命令，请检查 PATH。")
        if obsidian_password:
            run([ob, "login", "--email", obsidian_email, "--password", obsidian_password], check=False)
        else:
            print("即将运行 ob login；请按提示完成 Obsidian 登录。")
            run([ob, "login"], check=False)
        setup_cmd = [
            python_cmd(),
            str(SKILL_ROOT / "scripts" / "setup.py"),
            "--config",
            str(config_path),
            "--setup-ob-sync",
            "--obsidian-sync-vault",
            remote_vault,
        ]
        if sync_password:
            setup_cmd.extend(["--obsidian-sync-password", sync_password])
        run(setup_cmd)

    cron_files: list[Path] = []
    if detect_openclaw() and yes_no("检测到 OpenClaw 环境，是否生成 OpenClaw cron 定时任务配置？", False):
        timezone = prompt("cron 时区", DEFAULT_TZ)
        cron_files = write_cron_specs(config_path, timezone)

    run([python_cmd(), str(SKILL_ROOT / "scripts" / "setup.py"), "--config", str(config_path), "--doctor"], check=False)

    external_todos.append(
        "在自己常用 Chrome 浏览器安装 CookieCloud 插件，并填写："
        f"服务器地址 {browser_cookie_url}，UUID {env_values.get('COOKIECLOUD_UUID', '<cookiecloud.env 中的 COOKIECLOUD_UUID>')}，"
        f"Password {env_values.get('COOKIECLOUD_PASSWORD', '<cookiecloud.env 中的 COOKIECLOUD_PASSWORD>')}。"
    )
    external_todos.append("在该 Chrome 浏览器中登录 xiaohongshu.com 和 zhihu.com，然后执行 CookieCloud 插件同步。")
    if cookie_mode == "1" and browser_cookie_url.startswith("http://<"):
        external_todos.append("把 Chrome 插件里的服务器地址替换成运行 CookieCloud 服务端机器的真实局域网 IP 和 8088 端口。")
    if cron_files:
        external_todos.append("OpenClaw cron 配置已生成，请按你的 OpenClaw 环境导入或创建任务：" + ", ".join(str(p) for p in cron_files))
    else:
        external_todos.append("如需定时同步，稍后运行 scripts/install_cron.py 生成 OpenClaw cron 配置。")
    external_todos.append(f"小规模验证命令：python scripts/sync.py --config {config_path} --platform xhs")
    external_todos.append(f"小规模验证命令：python scripts/sync.py --config {config_path} --platform zhihu")
    external_todos.append(f"导出验证命令：python scripts/export_obsidian.py --config {config_path} --platform all --incremental")

    print("\n安装流程已完成。用户还需要在外部完成：")
    for index, item in enumerate(external_todos, start=1):
        print(f"{index}. {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
