#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import json
import secrets
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import uuid
import zipfile
from pathlib import Path

from common import DEFAULT_CONFIG_PATH, SKILL_ROOT, command_exists, expand_path, load_config, skill_dir, write_json, write_yaml


HCTEC_REPO = "https://github.com/hc-tec/my-collection-skills.git"
HCTEC_REPO_ZIP = "https://github.com/hc-tec/my-collection-skills/archive/refs/heads/main.zip"
HCTEC_SKILLS = [
    {"source": "xiaohongshu-favorites", "target": "hctec-xiaohongshu-favorites"},
    {"source": "zhihu-favorites", "target": "hctec-zhihu-favorites"},
    {"source": "favorites-harvester", "target": "hctec-favorites-harvester"},
]


def copy_if_missing(src: Path, dst: Path) -> bool:
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return True


def run(cmd: list[str]) -> int:
    print("+ " + " ".join(cmd))
    return subprocess.call(cmd)


def command_path(name: str) -> str | None:
    if sys.platform.startswith("win"):
        return shutil.which(f"{name}.cmd") or shutil.which(f"{name}.exe") or shutil.which(name)
    return shutil.which(name)


def render_cookiecloud_env(server_url: str) -> tuple[str, str, str]:
    cc_uuid = str(uuid.uuid4())
    cc_password = secrets.token_urlsafe(24)
    text = (
        "# CookieCloud 服务端地址。Docker 默认部署在本机时无需修改。\n"
        f"COOKIECLOUD_SERVER_URL={server_url}\n"
        f"COOKIECLOUD_UUID={cc_uuid}\n"
        f"COOKIECLOUD_PASSWORD={cc_password}\n"
        "\n"
        "# 兼容旧脚本变量名，保持与上面相同。\n"
        f"COOKIECLOUDUUID={cc_uuid}\n"
        f"COOKIECLOUDPASSWORD={cc_password}\n"
        "\n"
        "# 可选：如果不用 CookieCloud，可手动填原始 Cookie。\n"
        "# XIAOHONGSHU_COOKIE=\n"
        "# ZHIHU_COOKIE=\n"
        "# ZHIHU_COOKIES=\n"
    )
    return text, cc_uuid, cc_password


def state_path_for(config_path: Path) -> Path:
    return config_path.parent / "install_state.json"


def update_install_state(config_path: Path, **updates) -> None:
    state_path = state_path_for(config_path)
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    state.update(updates)
    state["schema_version"] = 1
    state["skill"] = "social-favorites-to-obsidian"
    state["config_path"] = str(config_path)
    write_json(state_path, state)


def default_random_vault_path() -> str:
    suffix = secrets.token_hex(4)
    return f"~/.local/share/social-favorites-to-obsidian/obsidian-vault-{suffix}"


def default_config_text(vault_path: str, obsidian_mode: str) -> str:
    run_ob_sync = "true" if obsidian_mode == "headless-sync" else "false"
    return f"""config_dir: "~/.config/social-favorites-to-obsidian"
data_dir: "~/.local/share/social-favorites-to-obsidian"
cookiecloud_env: "~/.config/social-favorites-to-obsidian/cookiecloud.env"

obsidian:
  vault: "{vault_path}"
  base_dir: "互联网笔记"
  run_ob_sync: {run_ob_sync}
  asset_dirname: "_assets"
  sync:
    mode: "{obsidian_mode}"
    headless_config_dir: "social-favorites-to-obsidian"
    device_name: "social-favorites-to-obsidian"

install:
  state_file: "~/.config/social-favorites-to-obsidian/install_state.json"

hctec:
  skills_root: "~/.openclaw/workspace/skills"
  xhs_skill: "hctec-xiaohongshu-favorites"
  zhihu_skill: "hctec-zhihu-favorites"
  harvester_skill: "hctec-favorites-harvester"
  python: ""

platforms:
  xhs:
    enabled: true
    max_per_run: 50
    max_new_per_run: 50
    max_scan_per_run: 50
    detail_delay_seconds: 8
    no_headless: false
  zhihu:
    enabled: true
    collection_ids: []
    collection_list_limit: 50
    max_per_collection: 100
    max_per_run: 100
    max_new_per_run: 100
    max_scan_per_run: 100

classification:
  rules_file: "~/.config/social-favorites-to-obsidian/classify_rules.yaml"
  default_level1: "其他"
  default_level2: "待整理"
"""


def init_files(config_path: Path, cookiecloud_server_url: str, obsidian_vault: str | None, obsidian_mode: str) -> None:
    created = []
    generated_vault_path = obsidian_vault or default_random_vault_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(default_config_text(generated_vault_path, obsidian_mode), encoding="utf-8")
        created.append(str(config_path))
    try:
        config = load_config(config_path)
    except Exception:
        # PyYAML may not be installed during first init. Use the generated defaults
        # so setup can still create env/rules/vault before --install-python-deps.
        config = {
            "config_dir": "~/.config/social-favorites-to-obsidian",
            "data_dir": "~/.local/share/social-favorites-to-obsidian",
            "cookiecloud_env": "~/.config/social-favorites-to-obsidian/cookiecloud.env",
            "obsidian": {
                "vault": generated_vault_path,
                "base_dir": "互联网笔记",
                "sync": {"mode": obsidian_mode},
            },
            "classification": {"rules_file": "~/.config/social-favorites-to-obsidian/classify_rules.yaml"},
        }
    cookie_env = expand_path(config["cookiecloud_env"])
    if not cookie_env.exists():
        env_text, cc_uuid, cc_password = render_cookiecloud_env(cookiecloud_server_url)
        cookie_env.parent.mkdir(parents=True, exist_ok=True)
        cookie_env.write_text(env_text, encoding="utf-8")
        created.append(str(cookie_env))
        print("")
        print("CookieCloud 浏览器插件需要填写下面这组值：")
        print(f"  服务端地址: {cookiecloud_server_url}")
        print(f"  UUID: {cc_uuid}")
        print(f"  Password: {cc_password}")
        print("")
        print("如果浏览器插件不在本机安装，请把服务端地址里的 127.0.0.1 换成运行 CookieCloud 的机器 IP。")
    rules = expand_path(config["classification"]["rules_file"])
    if copy_if_missing(SKILL_ROOT / "assets" / "classify_rules.example.yaml", rules):
        created.append(str(rules))
    for path in [
        expand_path(config["data_dir"]),
        expand_path(config["obsidian"]["vault"]) / config["obsidian"]["base_dir"],
    ]:
        path.mkdir(parents=True, exist_ok=True)
    update_install_state(
        config_path,
        initialized=True,
        obsidian_mode=config["obsidian"]["sync"].get("mode", obsidian_mode),
        obsidian_vault=str(expand_path(config["obsidian"]["vault"])),
        obsidian_local_ready=True,
        ob_sync_configured=False,
    )
    if created:
        print("已创建:")
        for item in created:
            print(f"  - {item}")
    else:
        print("配置文件已存在，未覆盖。")


def copy_skill_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        print(f"[ok] 已存在: {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    print(f"[ok] 已安装: {src.name} -> {dst}")


def checkout_hctec_repo(repo_url: str, workdir: Path) -> Path:
    if shutil.which("git"):
        checkout = workdir / "my-collection-skills"
        code = run(["git", "clone", "--depth", "1", repo_url, str(checkout)])
        if code == 0:
            return checkout
        print("[warn] git clone 失败，尝试下载 main.zip")

    archive = workdir / "my-collection-skills-main.zip"
    urllib.request.urlretrieve(HCTEC_REPO_ZIP, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(workdir)
    return workdir / "my-collection-skills-main"


def install_hctec_deps(repo_url: str, skills_root: Path) -> int:
    print(f"从 GitHub 安装 hctec 相关技能: {repo_url}")
    print(f"目标目录: {skills_root}")
    failed = 0
    with tempfile.TemporaryDirectory(prefix="sfto-hctec-") as tmp:
        repo = checkout_hctec_repo(repo_url, Path(tmp))
        for item in HCTEC_SKILLS:
            src = repo / "skills" / item["source"]
            dst = skills_root / item["target"]
            if not src.exists():
                print(f"[fail] 仓库中缺少: {src}")
                failed += 1
                continue
            try:
                copy_skill_tree(src, dst)
            except Exception as exc:
                print(f"[fail] 安装 {item['source']} 失败: {exc}")
                failed += 1
    return 1 if failed else 0


def install_ob_headless() -> int:
    if command_path("ob"):
        print("[ok] ob 命令已存在")
        return 0
    npm = command_path("npm")
    if not npm:
        print("[fail] 未找到 npm，无法自动安装 obsidian-headless。请先安装 Node.js/npm。")
        return 1
    return run([npm, "install", "-g", "obsidian-headless"])


def setup_ob_sync(config_path: Path, vault_name: str | None, device_name: str | None, config_dir: str | None, password: str | None) -> int:
    config = load_config(config_path)
    vault_path = expand_path(config["obsidian"]["vault"])
    vault_path.mkdir(parents=True, exist_ok=True)
    ob = command_path("ob")
    if not ob:
        print("[fail] 未找到 ob 命令。先运行: python scripts/setup.py --install-ob")
        return 1

    remote_vault = vault_name or input("Obsidian Sync 远程仓库名或 ID: ").strip()
    if not remote_vault:
        print("[fail] 远程仓库名不能为空")
        return 1
    username = input("Obsidian 账号用户名/邮箱（如果 ob 稍后提示登录，请输入同一个账号；这里只用于引导，不会保存）: ").strip()
    if username:
        print(f"账号: {username}")
    sync_password = password
    if sync_password is None:
        sync_password = getpass.getpass("Obsidian Sync 端到端加密密码（没有则直接回车，让 ob 交互处理）: ")

    cmd = [ob, "sync-setup", "--vault", remote_vault, "--path", str(vault_path)]
    if sync_password:
        cmd.extend(["--password", sync_password])
    if device_name:
        cmd.extend(["--device-name", device_name])
    else:
        cmd.extend(["--device-name", "social-favorites-to-obsidian"])
    if config_dir:
        cmd.extend(["--config-dir", config_dir])
    elif config["obsidian"].get("sync", {}).get("headless_config_dir"):
        cmd.extend(["--config-dir", str(config["obsidian"]["sync"]["headless_config_dir"])])

    code = run(cmd)
    if code == 0:
        config["obsidian"]["run_ob_sync"] = True
        config["obsidian"]["sync"]["mode"] = "headless-sync"
        write_yaml(config_path, {k: v for k, v in config.items() if not k.startswith("_")})
        update_install_state(
            config_path,
            initialized=True,
            obsidian_mode="headless-sync",
            obsidian_vault=str(vault_path),
            ob_sync_configured=True,
            ob_command="ob",
        )
    return code


def status(config_path: Path, as_json: bool) -> int:
    state_path = state_path_for(config_path)
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as exc:
            state = {"state_read_error": str(exc)}
    config_exists = config_path.exists()
    result = {
        "first_install": not (config_exists and state.get("initialized")),
        "config_exists": config_exists,
        "state_exists": state_path.exists(),
        "config_path": str(config_path),
        "state_path": str(state_path),
        "state": state,
    }
    if config_exists:
        try:
            config = load_config(config_path)
            result["cookiecloud_env_exists"] = expand_path(config["cookiecloud_env"]).exists()
            result["obsidian_vault_exists"] = expand_path(config["obsidian"]["vault"]).exists()
            result["obsidian_mode"] = config["obsidian"].get("sync", {}).get("mode")
            result["run_ob_sync"] = bool(config["obsidian"].get("run_ob_sync"))
            result["ob_command_exists"] = bool(command_path("ob"))
        except Exception as exc:
            result["config_error"] = str(exc)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"first_install: {result['first_install']}")
        print(f"config: {config_path} ({'exists' if config_exists else 'missing'})")
        print(f"state: {state_path} ({'exists' if state_path.exists() else 'missing'})")
        if "obsidian_mode" in result:
            print(f"obsidian_mode: {result['obsidian_mode']}")
            print(f"run_ob_sync: {result['run_ob_sync']}")
    return 0


def install_python_deps() -> int:
    return run([sys.executable, "-m", "pip", "install", "-r", str(SKILL_ROOT / "requirements.txt")])


def install_playwright() -> int:
    return run([sys.executable, "-m", "playwright", "install", "chromium"])


def doctor(config_path: Path) -> int:
    try:
        config = load_config(config_path)
    except Exception as exc:
        print(f"[fail] config load: {exc}")
        return 1

    failures = 0
    print(f"config: {config['_config_path']}")
    print(f"data_dir: {expand_path(config['data_dir'])}")

    checks = []
    for key, label in [
        ("xhs_skill", "hctec-xiaohongshu-favorites"),
        ("zhihu_skill", "hctec-zhihu-favorites"),
        ("harvester_skill", "hctec-favorites-harvester"),
    ]:
        d = skill_dir(config, key)
        ok = d.exists()
        checks.append((ok, label, str(d)))

    cookie_env = expand_path(config["cookiecloud_env"])
    checks.append((cookie_env.exists(), "cookiecloud.env", str(cookie_env)))
    checks.append((expand_path(config["obsidian"]["vault"]).exists(), "Obsidian vault", str(expand_path(config["obsidian"]["vault"]))))
    checks.append((bool(command_path("ob")) or not config["obsidian"].get("run_ob_sync"), "ob sync command", "run --install-ob or set run_ob_sync=false"))

    try:
        import yaml  # noqa: F401
        checks.append((True, "PyYAML", "installed"))
    except Exception:
        checks.append((False, "PyYAML", "运行 --install-python-deps"))
    try:
        import playwright  # noqa: F401
        checks.append((True, "Playwright", "installed"))
    except Exception:
        checks.append((False, "Playwright", "运行 --install-python-deps --install-playwright"))

    for ok, name, detail in checks:
        print(f"[{'ok' if ok else 'fail'}] {name}: {detail}")
        failures += int(not ok)
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="首次安装、依赖安装和诊断")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--init", action="store_true", help="创建配置/env/分类规则和运行目录")
    parser.add_argument("--status", action="store_true", help="输出安装状态，供其它 agent 判断是否首次安装")
    parser.add_argument("--json", action="store_true", help="配合 --status 输出 JSON")
    parser.add_argument("--doctor", action="store_true", help="检查依赖和配置")
    parser.add_argument("--install-skill-deps", action="store_true", help="从 GitHub 安装 hctec 相关技能")
    parser.add_argument("--install-python-deps", action="store_true", help="安装 Python 依赖")
    parser.add_argument("--install-playwright", action="store_true", help="安装 Playwright Chromium 浏览器")
    parser.add_argument("--install-ob", action="store_true", help="通过 npm 安装 obsidian-headless，提供 ob sync 命令")
    parser.add_argument("--setup-ob-sync", action="store_true", help="运行 ob sync-setup 初始化官方 Obsidian Sync")
    parser.add_argument("--cookiecloud-server-url", default="http://127.0.0.1:8088", help="写入 cookiecloud.env 的 CookieCloud 服务端地址")
    parser.add_argument("--obsidian-mode", choices=["local-only", "headless-sync"], default="local-only", help="Obsidian 同步模式")
    parser.add_argument("--obsidian-vault", help="本地 Obsidian 存储目录；不传则首次初始化随机创建")
    parser.add_argument("--obsidian-sync-vault", help="Obsidian Sync 远程仓库名或 ID")
    parser.add_argument("--obsidian-sync-password", help="Obsidian Sync 端到端加密密码；不传则交互输入")
    parser.add_argument("--obsidian-device-name", help="ob sync-setup 的设备名")
    parser.add_argument("--obsidian-config-dir", help="ob sync-setup 的 config-dir")
    parser.add_argument("--hctec-repo", default=HCTEC_REPO, help="hctec 技能 GitHub 仓库地址")
    parser.add_argument("--skills-root", default="~/.openclaw/workspace/skills", help="hctec 技能安装目标目录")
    args = parser.parse_args()

    config_path = expand_path(args.config)
    status = 0
    if args.status:
        return globals()["status"](config_path, args.json)
    if args.init:
        init_files(config_path, args.cookiecloud_server_url, args.obsidian_vault, args.obsidian_mode)
    if args.install_skill_deps:
        status |= install_hctec_deps(args.hctec_repo, expand_path(args.skills_root))
    if args.install_python_deps:
        status |= install_python_deps()
    if args.install_playwright:
        status |= install_playwright()
    if args.install_ob:
        status |= install_ob_headless()
    if args.setup_ob_sync:
        status |= setup_ob_sync(config_path, args.obsidian_sync_vault, args.obsidian_device_name, args.obsidian_config_dir, args.obsidian_sync_password)
    if args.doctor or not any([args.init, args.install_skill_deps, args.install_python_deps, args.install_playwright, args.install_ob, args.setup_ob_sync]):
        status |= doctor(config_path)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
