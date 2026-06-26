"""
utils.py — 工具函数集
包含：Cookie 健康检查 / 路径常量 / 输出工具
"""
import json
import os
import time
from typing import Dict, Any

_BASE = os.path.dirname(__file__)

# ── 路径常量 ──────────────────────────────────────────────────

COOKIES_PRIMARY = os.path.join(
    _BASE, "..", "..", "..", "shopify-marketing", "xhs_cookies.json"
)
COOKIES_ALT = os.path.join(_BASE, "..", "xhs_cookies.json")

DATA_DIR      = os.path.join(_BASE, "data")
ARCHETYPES_DB = os.path.join(DATA_DIR, "archetypes.json")
BLOGGERS_DB   = os.path.join(DATA_DIR, "bloggers.json")

HSWORD_DIR = os.path.join(
    _BASE, "..", "..", "..", "..", "openclaw_cosmo", "afa", "hsword"
)


# ── Cookie 健康检查 ───────────────────────────────────────────

def check_cookies(cookies_file: str = None) -> Dict[str, Any]:
    """
    检查 Cookie 文件的有效性

    返回：
        {
            "valid": bool,
            "file": str,
            "total": int,
            "expired": list[str],
            "expiring_soon": list[str],  # 24小时内过期
            "message": str
        }
    """
    path = cookies_file or _find_cookies()
    if not path or not os.path.exists(path):
        return {"valid": False, "file": path, "message": "Cookie 文件不存在"}

    try:
        with open(path, encoding="utf-8") as f:
            cookies = json.load(f)
    except Exception as e:
        return {"valid": False, "file": path, "message": f"读取失败: {e}"}

    now     = int(time.time())
    expired = []
    soon    = []

    for c in cookies:
        exp = c.get("expiry") or c.get("expires", 0)
        if not exp:
            continue
        diff = exp - now
        if diff <= 0:
            expired.append(c["name"])
        elif diff < 86400:
            soon.append(c["name"])

    valid = len(expired) == 0
    parts = []
    if expired:
        parts.append(f"❌ 已过期：{', '.join(expired)}")
    if soon:
        parts.append(f"⚠️  即将过期（24h内）：{', '.join(soon)}")
    if valid and not soon:
        parts.append("✅ 全部有效")

    return {
        "valid":          valid,
        "file":           path,
        "total":          len(cookies),
        "expired":        expired,
        "expiring_soon":  soon,
        "message":        " | ".join(parts),
    }


def _find_cookies() -> str:
    """自动查找最新 Cookie 文件"""
    candidates = [
        os.path.abspath(COOKIES_PRIMARY),
        os.path.abspath(COOKIES_ALT),
    ]
    # 返回最近修改的有效文件
    valid = [p for p in candidates if os.path.exists(p)]
    if not valid:
        return ""
    return max(valid, key=os.path.getmtime)


def get_best_cookies() -> str:
    """获取当前最佳 Cookie 路径（优先使用最新且有效的）"""
    for path in [os.path.abspath(COOKIES_PRIMARY), os.path.abspath(COOKIES_ALT)]:
        if os.path.exists(path):
            status = check_cookies(path)
            if status["valid"]:
                return path
    # 如果都过期，返回最新修改的（并给出警告）
    return _find_cookies()


# ── 输出工具 ──────────────────────────────────────────────────

def print_cookie_status(cookies_file: str = None):
    """打印 Cookie 状态（带颜色提示）"""
    status = check_cookies(cookies_file)
    print(f"Cookie 文件: {status['file']}")
    print(f"状态: {status['message']}")
    if not status["valid"]:
        print("⚡ 请重新运行：python3 xhs_login.py")
    return status["valid"]


def save_md(content: str, path: str):
    """保存 Markdown 文件"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Markdown 已保存：{path}")


def parse_likes(v) -> int:
    """解析点赞数（支持'万'格式）"""
    if not v:
        return 0
    s = str(v).replace(",", "").strip()
    if "万" in s:
        return int(float(s.replace("万", "")) * 10000)
    try:
        return int(s)
    except ValueError:
        return 0
