# -*- coding: utf-8 -*-
"""
更新提醒 —— 让用户及时知道技能有新版本。

机制（不依赖联网 / 密钥，默认可用）：
  1. 读取技能包内版本（version.py 的 VERSION）。
  2. 与本机缓存的「已见版本」(installed_version.json) 比较。
  3. 若包内版本 > 已见版本 => 提醒用户更新，并缓存新版本号。

可选增强（默认关闭，需用户在 config 中填 update_manifest_url）：
  远程 manifest 主动探测（best-effort，拉取失败不影响本地判断）。
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime

from . import config
from .version import VERSION, DISPLAY_NAME


def get_packaged_version() -> str:
    return VERSION


def get_installed_version() -> str:
    try:
        if config.INSTALLED_VERSION_PATH.exists():
            with open(config.INSTALLED_VERSION_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("version", "")
    except Exception:
        pass
    return ""


def _save_installed(version: str) -> None:
    config.ensure_dirs()
    try:
        with open(config.INSTALLED_VERSION_PATH, "w", encoding="utf-8") as f:
            json.dump({"version": version,
                       "seen_at": datetime.now().isoformat(timespec="seconds")}, f,
                      ensure_ascii=False, indent=2)
    except Exception:
        pass


def _remote_latest(manifest_url: str) -> str | None:
    """best-effort 远程探测；失败返回 None。"""
    try:
        req = urllib.request.Request(manifest_url, headers={"User-Agent": "zwjh-skill"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return str(data.get("version", ""))
    except Exception:
        return None


def check(remote: bool = False) -> dict:
    """
    返回 {update_available, packaged, installed, remote_latest, reminder}
    """
    packaged = get_packaged_version()
    installed = get_installed_version()
    cfg = config.load_config()
    remote_latest = None
    if remote:
        url = cfg.get("update_manifest_url")
        if url:
            remote_latest = _remote_latest(url)

    update_available = False
    packaged_cmp = packaged
    if remote_latest and _is_newer(remote_latest, packaged):
        packaged_cmp = remote_latest
        update_available = True
    elif installed:
        # 仅在「已记录过旧版本」时才提醒；首次运行（installed 为空）不算有新版本
        if _is_newer(packaged, installed):
            update_available = True

    reminder = ""
    if update_available:
        reminder = (
            f"🔔 {DISPLAY_NAME} 有新版本可用（当前已见 {installed or '未知'} "
            f"→ 最新 {packaged_cmp}）。\n"
            f"   建议更新本技能以获得最新能力与修复。"
        )
    elif not installed:
        reminder = f"✅ 已是最新版本（{packaged}），已记录当前版本。"
    return {
        "update_available": update_available,
        "packaged_version": packaged,
        "installed_version": installed,
        "remote_latest": remote_latest,
        "reminder": reminder,
    }


def mark_seen() -> None:
    """运行后调用，缓存当前包内版本为「已见」。"""
    _save_installed(get_packaged_version())


def _is_newer(a: str, b: str) -> bool:
    """a 是否比 b 新（语义化版本比较）。b 为空视为需要提醒。"""
    if not b:
        return True

    def _parts(v: str):
        return [int(x) for x in v.split(".") if x.isdigit()]

    pa, pb = _parts(a), _parts(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    return pa > pb


if __name__ == "__main__":
    r = check()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    mark_seen()
