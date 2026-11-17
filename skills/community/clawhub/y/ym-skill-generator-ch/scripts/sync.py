#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能版本自检（**只读**）：比对线上版本，落后就给出重装命令，绝不自己改写文件。

为什么每个技能都需要它
----------------------
技能装到本地后就是一份**文件快照**，平台不会替用户检查版本。版本落后时，
最常见的后果是「流程走完了但产物不对」——而且往往在用户已经投入时间之后才暴露。
所以每次动手前先跑一次自检。

为什么**不**自动更新
--------------------
一个能悄悄改写自己的技能，本身就是风险面：SkillHub 的下载接口不提供包摘要
（没有 sha256 / digest），脚本自己取包自己校验等于自证，「拿到的包被换成了什么」
无从校验。所以本脚本只读：只比对版本、只给结论与重装命令，**不下载、不解压、
不修改任何文件**。换版本只有一条路 —— 由用户明确重装。

用法
----
    python scripts/sync.py            # 人读
    python scripts/sync.py --json     # 机器读（推荐给智能体）

退出码（智能体据此决定怎么跟用户说）
------------------------------------
    0   已是最新（或本地比线上新）
    10  有新版，建议重装
    20  主版本号不同 = 协议不兼容，必须重装后才能继续
    30  联网核对失败 —— 按旧版继续，不阻断用户
    1   出错（本地连版本号都读不出来等）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
META_PATH = SKILL_DIR / "_meta.json"          # 老版本可能留下，只当版本号兜底读取源
CONFIG_PATH = SKILL_DIR / "config.json"

# 版本真相源：SkillHub 公开接口（免登录，由平台保障可用性）
SKILLHUB_API = "https://api.skillhub.cn/api/v1"

EXIT_OK = 0
EXIT_OUTDATED = 10
EXIT_HARD_REQUIRED = 20
EXIT_UNREACHABLE = 30
EXIT_ERROR = 1


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def read_frontmatter_value(key: str) -> str:
    """从 SKILL.md 的 frontmatter 里取一个单行字段的值。

    只认「key: 值」这一行（平台解析器也是这个口径），折叠块与块列表读不到。
    """
    try:
        text = SKILL_MD.read_text(encoding="utf-8")
    except OSError:
        return ""
    pattern = r"^" + re.escape(key) + r":[ \t]*(.+?)[ \t]*$"
    match = re.search(pattern, text, re.M)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def detect_skill_code() -> str:
    """技能标识：slug → name → 目录名。

    优先 slug（平台发布 CLI 的口径），目录名兜底 —— 手工复制的技能目录
    常常没写 frontmatter，但目录名一定在。
    """
    return (read_frontmatter_value("slug")
            or read_frontmatter_value("name")
            or SKILL_DIR.name)


def detect_skill_name(code: str) -> str:
    return (read_frontmatter_value("display_name")
            or read_frontmatter_value("displayName")
            or read_frontmatter_value("name")
            or code)


def parse_version(value: object) -> tuple:
    """把 ``1.4.0`` / ``v1.4.0`` 解析成可比较的元组。

    刻意不做字符串比较：``"1.10.0" < "1.9.0"`` 在字典序下成立，而那是错的。
    """
    text = str(value or "").strip()
    if text[:1] in ("v", "V"):
        text = text[1:]

    parts = []
    for chunk in text.split("."):
        digits = ""
        for char in chunk:
            if char.isdigit():
                digits += char
            else:
                break
        parts.append(int(digits) if digits else 0)

    return tuple(parts) if parts else (0,)


def is_newer(candidate: object, current: object) -> bool:
    return parse_version(candidate) > parse_version(current)


def major_of(value: object):
    match = re.match(r"^[vV]?(\d+)", str(value or "").strip())
    return int(match.group(1)) if match else None


def http_get(url: str, timeout: float) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "skill-version-check/1.0", "Accept": "application/json, */*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def read_local_version() -> str:
    """本地版本以 SKILL.md 的 frontmatter 为准，回落到 _meta.json。

    不看 _meta.json 优先是因为：用户也可能是直接 `skillhub install` 装的，
    那种情况下 _meta.json 由包携带甚至根本不存在。SKILL.md 随包更新，
    才是「我这一份技能是什么版本」的权威来源。
    """
    version = read_frontmatter_value("version")
    if version:
        return version
    return str(load_json(META_PATH).get("version") or "").strip()


def resolve_source(explicit_manifest: str, code: str) -> tuple:
    """决定去哪儿核对版本，返回 ``(kind, url)``。

    默认走 SkillHub（免登录、由平台保障）。只有显式给了清单地址才改道：
    ``--manifest-url`` → 环境变量 ``SKILL_UPDATE_MANIFEST_URL``
    → ``config.json`` 的 ``manifest_url``。
    """
    if explicit_manifest.strip():
        return "manifest", explicit_manifest.strip()

    env_url = os.environ.get("SKILL_UPDATE_MANIFEST_URL", "").strip()
    if env_url:
        return "manifest", env_url

    configured = str(load_json(CONFIG_PATH).get("manifest_url") or "").strip()
    if configured:
        return "manifest", configured

    return "skillhub", "%s/skills/%s" % (SKILLHUB_API, code)


def fetch_skillhub_manifest(url: str, timeout: float) -> dict:
    payload = json.loads(http_get(url, timeout).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SkillHub 返回的不是 JSON 对象")

    latest = payload.get("latestVersion") or {}
    if not isinstance(latest, dict):
        latest = {}
    return {
        "version": str(latest.get("version") or "").strip(),
        "notes": str(latest.get("changelog") or "").strip(),
        "min_supported_version": "",
    }


def fetch_server_manifest(url: str, timeout: float) -> dict:
    payload = json.loads(http_get(url, timeout).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("版本清单不是一个 JSON 对象")
    return payload


def infer_hard_required(current: str, latest: str) -> bool:
    """平台不声明「最低可用版本」，改由版本号语义推断。

    约定：**主版本号不同 = 协议不兼容**，必须更新。这样发布方控制硬阻断的方式
    就是「该 bump major 时 bump major」，既不依赖后端也不需要额外配置。
    """
    now_major, new_major = major_of(current), major_of(latest)
    if now_major is None or new_major is None:
        return False
    return now_major != new_major


def emit(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("技能 %s" % result["skill_code"])
    print("  版本来源  %s  %s" % (result["source"], result["source_url"]))
    print("  本地版本  %s" % (result["current_version"] or "(未知)"))
    if result["latest_version"]:
        print("  线上版本  %s" % result["latest_version"])
    if result["min_supported_version"]:
        print("  最低可用  %s" % result["min_supported_version"])
    print("  结论      %s" % result["message"])
    if result["notes"]:
        print("  更新说明  %s" % result["notes"])
    if result["reinstall_command"] and result["status"] in ("outdated", "hard-required"):
        print("  重装命令  %s" % result["reinstall_command"])
    print("  （本脚本只读：未下载、未修改任何文件）")


def main() -> int:
    parser = argparse.ArgumentParser(description="比对本技能与线上版本（只读，不修改任何文件）。")
    parser.add_argument("--json", dest="as_json", action="store_true", help="输出 JSON，便于智能体解析")
    parser.add_argument("--manifest-url", default="", help="改用自建版本清单（一般不用）")
    parser.add_argument("--timeout", type=float, default=20.0, help="网络超时（秒）")
    args = parser.parse_args()

    code = detect_skill_code()
    name = detect_skill_name(code)
    kind, url = resolve_source(args.manifest_url, code)
    current = read_local_version()

    result = {
        "skill_code": code,
        "skill_name": name,
        "skill_dir": str(SKILL_DIR),
        "source": kind,
        "source_url": url,
        "current_version": current,
        "latest_version": "",
        "min_supported_version": "",
        "status": "",
        "hard_required": False,
        "read_only": True,
        "reinstall_command": "skillhub install %s" % code,
        "notes": "",
        "message": "",
    }

    if not current:
        result["status"] = "unknown"
        result["message"] = "SKILL.md 里读不到 version 字段，无法判断版本，先补上 version 再自检。"
        emit(result, args.as_json)
        return EXIT_ERROR

    try:
        manifest = (fetch_skillhub_manifest(url, args.timeout)
                    if kind == "skillhub"
                    else fetch_server_manifest(url, args.timeout))
    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError) as exc:
        # 核对不上不等于用户做错了什么，因此不阻断，只提示。
        result["status"] = "unreachable"
        result["message"] = ("没能连上 %s 核对版本（%s）。已按本地 %s 版继续；"
                             "如果后续结果异常，先检查网络。" % (result["source"], exc, current))
        emit(result, args.as_json)
        return EXIT_UNREACHABLE

    latest = str(manifest.get("version") or "").strip()
    minimum = str(manifest.get("min_supported_version") or "").strip()
    result["latest_version"] = latest
    result["min_supported_version"] = minimum
    result["notes"] = str(manifest.get("notes") or "")

    if not latest:
        result["status"] = "up-to-date"
        result["message"] = "线上未声明版本号（可能尚未发布），按本地 %s 版继续。" % current
        emit(result, args.as_json)
        return EXIT_OK

    # 本地比线上还新：发布前的开发版，或线上被回滚。不动它，也不误导用户。
    if is_newer(current, latest):
        result["status"] = "ahead"
        result["message"] = "本地 %s 高于线上 %s（未发布的开发版，或线上被回滚），不做改动。" % (current, latest)
        emit(result, args.as_json)
        return EXIT_OK

    has_update = is_newer(latest, current)
    # 「低于最低可用版本」必须独立于「有没有新版」判定：否则一旦最低线抬高而 latest
    # 没动，会收到一句「已是最新」，然后继续用一个协议上不被支持的版本。
    hard_required = (bool(minimum) and is_newer(minimum, current)) or infer_hard_required(current, latest)
    result["hard_required"] = hard_required

    if not has_update and not hard_required:
        result["status"] = "up-to-date"
        result["message"] = "技能已是最新版本（%s）。" % current
        emit(result, args.as_json)
        return EXIT_OK

    if hard_required:
        result["status"] = "hard-required"
        result["message"] = ("技能版本过低（%s → 线上 %s，主版本号不同 = 协议不兼容），"
                             "必须重装后才能继续使用。重装：%s"
                             % (current, latest, result["reinstall_command"]))
        emit(result, args.as_json)
        return EXIT_HARD_REQUIRED

    result["status"] = "outdated"
    result["message"] = "技能有新版本 %s → %s。建议重装：%s" % (current, latest, result["reinstall_command"])
    emit(result, args.as_json)
    return EXIT_OUTDATED


if __name__ == "__main__":
    sys.exit(main())
