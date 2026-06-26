#!/usr/bin/env python3
"""
Trade Arena runtime helper

这是 Skill 包内的手动辅助入口，用于本地辅助、自更新和少量 API 调试。
设置引导、策略整理、定时任务建议和启动守门都应由 Skill 对话完成。
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.parse import urljoin

import requests

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_ROOT / "config.json"
SKILL_MD_FILE = SKILL_ROOT / "SKILL.md"
STRATEGY_FILE = SKILL_ROOT / "strategy.md"
LEGACY_STRATEGY_FILE = SKILL_ROOT / "strategy.MD"
CLAW_HUB_SKILL_PAGE_URL = "https://clawhub.ai/catrefuse/trade-arena"

InputFunc = Callable[[str], str]

HANDOFF_LINES = [
    "Trade Arena 的设置引导、策略整理、定时任务建议和启动守门都由 Skill 对话负责。",
    "如果你是普通使用者，请直接在宿主里说：配置 trade arena / 修改我的投资策略 / 重新生成定时任务建议。",
    "这个脚本现在只保留手动辅助能力，例如检查更新、注册、刷新账户信息和查看单只股票行情。",
]


def _default_setup_state() -> dict:
    return {"last_update_error": ""}



def default_config() -> dict:
    return {
        "api_url": "stock.cocoloop.cn",
        "token": "",
        "agent_id": "",
        "account_id_us": "",
        "account_id_cn": "",
        "account_id_hk": "",
        "skill_version": "",
        "last_update_check_at": "",
        "latest_remote_skill_version": "",
        "setup_state": _default_setup_state(),
    }



def _merge_setup_state(raw_setup: dict | None) -> dict:
    merged: dict[str, str] = {}
    if isinstance(raw_setup, dict):
        for key, value in raw_setup.items():
            if isinstance(key, str) and isinstance(value, str):
                merged[key] = value
    merged.setdefault("last_update_error", "")
    return merged



def _normalize_config_payload(raw: object) -> dict:
    config = default_config()
    if not isinstance(raw, dict):
        return config

    if raw.get("$schema") and raw.get("properties") and "api_url" not in raw:
        return config

    for key in config:
        if key == "setup_state":
            continue
        value = raw.get(key)
        if isinstance(value, str):
            config[key] = value
    config["setup_state"] = _merge_setup_state(raw.get("setup_state"))
    return config



def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return default_config()
    try:
        raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default_config()
    return _normalize_config_payload(raw)



def save_config(config: dict, announce: bool = True) -> None:
    normalized = _normalize_config_payload(config)
    CONFIG_FILE.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if announce:
        print(f"✅ 配置已保存到 {CONFIG_FILE}")



def _normalize_api_url(api_url: str) -> str:
    normalized = (api_url or "").rstrip("/")
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized}"
    return normalized



def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")



def _version_to_tuple(version: str) -> tuple[int, ...]:
    parts = []
    for piece in (version or "").strip().split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)



def _is_remote_newer(remote_version: str, local_version: str) -> bool:
    if not remote_version:
        return False
    if not local_version:
        return True
    return _version_to_tuple(remote_version) > _version_to_tuple(local_version)



def _get_local_skill_version() -> str:
    if not SKILL_MD_FILE.exists():
        return ""
    try:
        content = SKILL_MD_FILE.read_text(encoding="utf-8")
    except OSError:
        return ""

    in_front_matter = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "---":
            if not in_front_matter:
                in_front_matter = True
                continue
            break
        if in_front_matter and stripped.startswith("version:"):
            return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return ""



def _safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    destination_resolved = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if not str(target).startswith(str(destination_resolved)):
            raise ValueError("检测到不安全的压缩包路径，已中止更新")
    archive.extractall(destination)



def _normalize_download_url(url: str, api_url: str) -> str:
    if not url:
        return ""
    if url.startswith("/"):
        return f"{_normalize_api_url(api_url)}{url}"
    return _normalize_api_url(url)



def _extract_clawhub_download_url(page_html: str) -> str:
    if not page_html:
        return ""

    labeled = re.search(r'href="([^"]+)"[^>]*>\s*Download zip\s*<', page_html, flags=re.IGNORECASE)
    if labeled:
        return urljoin(CLAW_HUB_SKILL_PAGE_URL, labeled.group(1))

    fallback = re.search(r'href="([^"]*api/v1/download\?slug=trade-arena[^"]*)"', page_html, flags=re.IGNORECASE)
    if fallback:
        return urljoin(CLAW_HUB_SKILL_PAGE_URL, fallback.group(1))
    return ""


def _extract_clawhub_version(page_html: str) -> str:
    if not page_html:
        return ""

    og_match = re.search(r'og/skill\.png[^"]*version=([0-9]+(?:\.[0-9]+)+)', page_html, flags=re.IGNORECASE)
    if og_match:
        return og_match.group(1)

    badge_match = re.search(r'>\s*v(?:<!-- -->)?\s*([0-9]+(?:\.[0-9]+)+)\s*<', page_html, flags=re.IGNORECASE)
    if badge_match:
        return badge_match.group(1)

    script_match = re.search(r'"version"\s*:\s*"([0-9]+(?:\.[0-9]+)+)"', page_html, flags=re.IGNORECASE)
    if script_match:
        return script_match.group(1)
    return ""


def _extract_version_from_content_disposition(content_disposition: str) -> str:
    if not content_disposition:
        return ""
    match = re.search(
        r'filename\*?=(?:"[^"]*?([0-9]+(?:\.[0-9]+)+)\.zip"|\S*?([0-9]+(?:\.[0-9]+)+)\.zip)',
        content_disposition,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    return match.group(1) or match.group(2) or ""


def _resolve_version_from_download(download_url: str) -> str:
    if not download_url:
        return ""

    try:
        response = requests.head(download_url, allow_redirects=True, timeout=30)
    except requests.RequestException:
        response = requests.get(download_url, allow_redirects=True, stream=True, timeout=30)

    version = _extract_version_from_content_disposition(response.headers.get("content-disposition", ""))
    try:
        response.close()
    except Exception:
        pass
    return version


def fetch_clawhub_release_metadata() -> dict:
    response = requests.get(CLAW_HUB_SKILL_PAGE_URL, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"http_{response.status_code}")

    page_html = response.text
    remote_version = _extract_clawhub_version(page_html)
    hosted_url = _extract_clawhub_download_url(page_html)

    if not hosted_url:
        raise RuntimeError("missing_download_url")
    if not remote_version:
        remote_version = _resolve_version_from_download(hosted_url)
    if not remote_version:
        raise RuntimeError("missing_version")

    return {"version": remote_version, "hosted_url": hosted_url}


def api_request(method, endpoint, data=None, token=None):
    config = load_config()
    api_url = _normalize_api_url(config["api_url"])
    url = f"{api_url}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.request(method, url, json=data, headers=headers, timeout=30)



def apply_skill_update(hosted_url: str, target_version: str, silent: bool = False) -> bool:
    """通过托管链接下载并覆盖本地 skill 文件（保留本地 config.json 与 strategy.md）"""
    local_config = load_config()
    download_url = _normalize_download_url(hosted_url, local_config.get("api_url", ""))
    if not download_url:
        if not silent:
            print("❌ 缺少托管下载链接，无法更新")
        return False

    if not silent:
        print(f"⬇️  正在下载新版本 skill: {download_url}")
    response = requests.get(download_url, timeout=90)
    if response.status_code != 200:
        if not silent:
            print(f"❌ 下载更新包失败: HTTP {response.status_code}")
        return False

    with tempfile.TemporaryDirectory(prefix="trade_arena_update_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
                _safe_extract(archive, tmp_path)
        except Exception as exc:
            if not silent:
                print(f"❌ 解压更新包失败: {exc}")
            return False

        copied = 0
        protected = {"config.json", "strategy.md", "strategy.MD"}
        for source in tmp_path.rglob("*"):
            if not source.is_file():
                continue
            relative = source.relative_to(tmp_path)
            if str(relative).replace("\\", "/") in protected:
                continue
            destination = SKILL_ROOT / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied += 1

    updated_config = load_config()
    updated_config["skill_version"] = target_version
    updated_config["last_update_check_at"] = _now_utc_iso()
    updated_config["latest_remote_skill_version"] = target_version
    updated_config["setup_state"]["last_update_error"] = ""
    save_config(updated_config, announce=False)
    if not silent:
        print(f"✅ 已自动更新到最新版 {target_version}（更新文件 {copied} 个）")
    return True



def check_and_update_skill(force: bool = False, auto_apply: bool = True, silent: bool = False) -> dict:
    """手动检查 skill 更新。正常启动守门应由 Skill 对话负责。"""
    config = load_config()
    local_version = config.get("skill_version") or _get_local_skill_version()
    config["skill_version"] = local_version
    config["last_update_check_at"] = _now_utc_iso()

    try:
        payload = fetch_clawhub_release_metadata()
    except requests.RequestException as exc:
        config["setup_state"]["last_update_error"] = f"clawhub_{exc.__class__.__name__}"
        save_config(config, announce=False)
        if force and not silent:
            print(f"⚠️  检查更新失败: {exc}")
        return {
            "checked": True,
            "updated": False,
            "error": f"clawhub_{exc.__class__.__name__}",
            "local_version": local_version,
        }
    except RuntimeError as exc:
        error_code = f"clawhub_{exc}"
        config["setup_state"]["last_update_error"] = error_code
        save_config(config, announce=False)
        if force and not silent:
            print(f"⚠️  检查更新失败: {error_code}")
        return {
            "checked": True,
            "updated": False,
            "error": error_code,
            "local_version": local_version,
        }

    remote_version = payload.get("version", "")
    hosted_url = payload.get("hosted_url", "")
    has_update = _is_remote_newer(remote_version, local_version)

    config["latest_remote_skill_version"] = remote_version
    config["setup_state"]["last_update_error"] = ""
    save_config(config, announce=False)

    if has_update:
        updated = False
        if auto_apply:
            updated = apply_skill_update(hosted_url, remote_version, silent=silent)
        elif not silent:
            print(f"🔔 发现新版本: 本地 {local_version or 'unknown'} -> 远端 {remote_version}")
        return {
            "checked": True,
            "updated": updated,
            "has_update": True,
            "local_version": local_version,
            "remote_version": remote_version,
            "hosted_url": hosted_url,
        }

    if force and not silent:
        print(f"✅ Skill 已是最新版本: {remote_version or local_version or 'unknown'}")
    return {
        "checked": True,
        "updated": False,
        "has_update": False,
        "local_version": local_version,
        "remote_version": remote_version or local_version,
        "hosted_url": hosted_url,
    }



def read_strategy_document() -> tuple[bool, Path | None, str]:
    for path in (STRATEGY_FILE, LEGACY_STRATEGY_FILE):
        if not path.exists():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            return False, path, ""
        return bool(content.strip()), path, content
    return False, None, ""



def prompt_text(prompt: str, input_fn: InputFunc = input) -> str:
    while True:
        raw = input_fn(prompt).strip()
        if raw:
            return raw
        print("这一项先别留空。")



def register(name, email, model, avatar, style):
    local_config = load_config()
    if local_config.get("token"):
        print("⛔ 检测到本地已存在 token，注册流程已中断。")
        print("   如需重新注册，请先清空 config.json 中的 token。")
        return None

    print(f"📝 正在注册队伍 {name}...")
    response = api_request(
        "POST",
        "/api/agents/register",
        {
            "name": name,
            "email": email,
            "model": model,
            "avatar": avatar,
            "style": style,
        },
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ 注册成功！")
        print(f"   Agent ID: {data['agent']['id']}")
        print(f"   Token: {data['token'][:20]}...")
        print("⚠️  请立即保存完整 token；关闭后将无法再次查看。")
        return data

    print(f"❌ 注册失败: {response.json()}")
    return None



def get_my_info(token):
    response = api_request("GET", "/api/agents/me", token=token)

    if response.status_code == 200:
        data = response.json()
        print("📊 队伍信息:")
        print(f"   名称: {data['name']}")
        print(f"   模型: {data['model']}")
        print(f"   人民币现金余额: {data.get('wallet_cash_cny', '0')} CNY")
        print(f"   总资产: {data.get('total_asset_cny', '0')} CNY")
        accounts = data.get("accounts", {})
        holdings = {item.get("market"): item for item in data.get("market_holdings", [])}
        for market in ("us", "cn", "hk"):
            account = accounts.get(market, {})
            market_holding = holdings.get(market, {})
            print(f"   {market.upper()} 账户: {account.get('id', 'N/A')}")
            print(
                "      持仓: "
                f"{market_holding.get('holdings_count', 0)} 只, "
                f"持仓市值 {market_holding.get('position_value_cny', '0')} CNY"
            )
        return data

    print(f"❌ 获取信息失败: {response.json()}")
    return None



def get_portfolio(account_id, token):
    response = api_request("GET", f"/api/accounts/{account_id}/portfolio", token=token)

    if response.status_code == 200:
        data = response.json()
        print("💼 持仓信息:")
        print(f"   人民币现金: {data['cash']}")
        for pos in data["positions"]:
            pnl_str = f"盈亏: {pos['pnl']}" if pos["pnl"] else ""
            print(f"   {pos['ticker']}: {pos['shares']} 股 @ {pos['avg_cost']} {pnl_str}")
        return data

    print(f"❌ 获取持仓失败: {response.json()}")
    return None



def get_agent_portfolio_summary(agent_id):
    response = api_request("GET", f"/api/agents/{agent_id}/portfolio-summary")

    if response.status_code == 200:
        data = response.json()
        print("💰 当前持仓状态")
        print(f"   共享现金池: ¥{data.get('wallet_cash_cny', '0')}")
        print(f"   总资产: ¥{data.get('total_asset_cny', '0')}")
        for market in data.get("markets", []):
            market_name = {"us": "美股", "cn": "A股", "hk": "港股"}.get(market.get("market"), market.get("market"))
            holdings_count = market.get("holdings_count", 0)
            position_value = market.get("position_value_cny", "0")
            account_id = market.get("account_id")
            if not account_id:
                print(f"   {market_name}: 未开通")
                continue
            print(f"   {market_name}: 持仓 {holdings_count} 只, 持仓市值 ¥{position_value}")
        return data

    print(f"❌ 获取公开持仓汇总失败: {response.json()}")
    return None



def get_quote(ticker):
    response = api_request("GET", f"/api/market/quote/{ticker}")

    if response.status_code == 200:
        data = response.json()
        change = "+" if data["change_pct"] >= 0 else ""
        print(f"📊 {data['ticker']} ({data.get('name', 'N/A')})")
        print(f"   价格: {data['price']}")
        print(f"   涨跌: {change}{data['change_pct']}%")
        print(f"   状态: {data['market_status']}")
        return data

    print(f"❌ 获取行情失败: {response.json()}")
    return None



def register_interactively(input_fn: InputFunc = input) -> dict:
    config = load_config()
    if config.get("token"):
        print("⛳ 已检测到现有参赛身份，跳过注册。")
        print(f"   当前 Token: {config['token'][:20]}...")
        return config

    print("\n📌 手动注册辅助")
    print("正式的参赛设置请直接在 Skill 对话里完成。")
    email = prompt_text("请输入邮箱: ", input_fn=input_fn)
    name = prompt_text("请输入队伍名称: ", input_fn=input_fn)
    avatar = prompt_text("请输入头像 emoji: ", input_fn=input_fn)
    model = prompt_text("请输入模型名称 (如 gpt-5.4): ", input_fn=input_fn)
    style = prompt_text("请输入投资风格: ", input_fn=input_fn)

    result = register(name, email, model, avatar, style)
    if not result:
        return config

    config["token"] = result["token"]
    config["agent_id"] = result["agent"]["id"]
    save_config(config)
    return config



def refresh_account_info(config: dict) -> dict:
    if not config.get("token"):
        print("⚠️  当前还没有 token。请先在 Skill 对话里完成注册，或用 --register 做手动辅助注册。")
        return config

    info = get_my_info(config["token"])
    if not info:
        return config

    config["agent_id"] = info["agent_id"]
    config["account_id_us"] = info["accounts"]["us"]["id"]
    config["account_id_cn"] = info["accounts"]["cn"]["id"]
    if info["accounts"].get("hk"):
        config["account_id_hk"] = info["accounts"]["hk"]["id"]
    save_config(config)
    return config



def print_helper_intro() -> None:
    print("=" * 50)
    print("🛠️  Trade Arena Helper")
    print("=" * 50)
    for line in HANDOFF_LINES:
        print(line)
    has_strategy, path, _content = read_strategy_document()
    if path:
        status = "可用" if has_strategy else "存在但不可读或为空"
        print(f"当前策略文件: {path.name} ({status})")
    else:
        print("当前策略文件: 未找到，请回到 Skill 对话完成参赛设置。")



def parse_args():
    parser = argparse.ArgumentParser(description="Trade Arena helper")
    parser.add_argument("--check-update", action="store_true", help="手动检查更新；发现新版本后自动下载并更新")
    parser.add_argument("--check-update-only", action="store_true", help="手动检查更新；仅检查不更新")
    parser.add_argument("--register", action="store_true", help="手动辅助注册，不触发设置对话")
    parser.add_argument("--refresh-info", action="store_true", help="刷新并回写账户与市场账户信息")
    parser.add_argument("--quote", metavar="TICKER", help="查看单只股票行情")
    parser.add_argument("--portfolio-summary", action="store_true", help="查看当前 agent 的三地持仓汇总")
    return parser.parse_args()



def main(input_fn: InputFunc = input):
    args = parse_args()
    if args.check_update and args.check_update_only:
        raise SystemExit("--check-update 与 --check-update-only 不能同时使用")

    print_helper_intro()

    if args.check_update:
        check_and_update_skill(force=True, auto_apply=True, silent=False)
    elif args.check_update_only:
        check_and_update_skill(force=True, auto_apply=False, silent=False)

    config = load_config()
    if args.register:
        config = register_interactively(input_fn=input_fn)
    if args.refresh_info:
        config = refresh_account_info(config)
    if args.quote:
        get_quote(args.quote)
    if args.portfolio_summary:
        if config.get("agent_id"):
            get_agent_portfolio_summary(config["agent_id"])
        else:
            print("⚠️  当前没有 agent_id。先刷新账户信息，或在 Skill 对话里完成注册。")

    if not any([args.check_update, args.check_update_only, args.register, args.refresh_info, args.quote, args.portfolio_summary]):
        print("\n没有执行额外动作。请优先回到 Skill 对话完成设置和日常使用。")


if __name__ == "__main__":
    main()
