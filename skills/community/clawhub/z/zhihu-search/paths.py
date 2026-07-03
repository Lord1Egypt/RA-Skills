#!/usr/bin/env python3
"""
paths.py - 集中管理 zhihu-search skill 的所有路径
=================================================

路径解析优先级(从高到低):
1. 环境变量 ZHIHU_DATA_DIR (给 docker / CI 用)
2. 环境变量 ZHIHU_COOKIE_FILE (单独覆盖 cookie 路径)
3. 老的 /tmp/zhihu/(向后兼容,如果新路径不存在但老的在)
4. 默认 <skill 目录>/data/

这样 skill 可以:
- git clone 到任何位置都能用(自包含)
- 跨设备部署(每台机器只需导一次 cookies)
- 老的 /tmp/zhihu/ 数据自动迁移(无需手工)
"""
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
LEGACY_DIR = Path("/tmp/zhihu")


def _resolve_data_dir() -> Path:
    """解析 data 目录"""
    env = os.environ.get("ZHIHU_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    # 老的 /tmp/zhihu/ 兼容:存在就用老的
    if (LEGACY_DIR / "cookies.txt").exists():
        return LEGACY_DIR
    # 默认 skill 目录
    return SKILL_DIR / "data"


def _ensure_dir(p: Path) -> Path:
    """确保目录存在"""
    p.mkdir(parents=True, exist_ok=True)
    return p


def _resolve_cookie_file(data_dir: Path) -> Path:
    """解析 cookie 文件路径(支持独立覆盖)"""
    env = os.environ.get("ZHIHU_COOKIE_FILE")
    if env:
        return Path(env).expanduser().resolve()
    return data_dir / "cookies.txt"


# ===== 核心路径(其他模块用这些) =====
DATA_DIR    = _resolve_data_dir()
COOKIE_RAW  = DATA_DIR / "cookies-raw.txt"
COOKIE_FILE = _resolve_cookie_file(DATA_DIR)
STATE_DIR   = _ensure_dir(DATA_DIR / "state")
STATE_FILE  = STATE_DIR / "zhihu.state.json"
EXPORTS_DIR = _ensure_dir(DATA_DIR / "exports")
ANSWERS_DIR = _ensure_dir(DATA_DIR / "answers")
ARTICLES_DIR = _ensure_dir(DATA_DIR / "articles")
COLUMNS_DIR = _ensure_dir(DATA_DIR / "columns")
COMMENTS_DIR = _ensure_dir(DATA_DIR / "comments")

# 临时文件目录(过程中间文件,放系统 /tmp)
TMP_DIR = Path("/tmp/zhihu")
_ensure_dir(TMP_DIR)


def report() -> str:
    """返回当前路径配置(供 keepalive.py / zhihu-fetch.py 启动时打印)"""
    lines = [
        "📁 zhihu-search skill 路径配置:",
        f"  skill 目录:    {SKILL_DIR}",
        f"  data 目录:     {DATA_DIR}",
        f"  cookies:       {COOKIE_FILE}",
        f"  cookies-raw:   {COOKIE_RAW}",
        f"  state:         {STATE_FILE}",
        f"  默认导出:      {EXPORTS_DIR}",
    ]
    if DATA_DIR == LEGACY_DIR:
        lines.append("  ⚠️  使用老路径 /tmp/zhihu/ (向后兼容)")
        lines.append("     建议: 跑 setup 切到新路径;或设 ZHIHU_DATA_DIR 环境变量")
    return "\n".join(lines)
