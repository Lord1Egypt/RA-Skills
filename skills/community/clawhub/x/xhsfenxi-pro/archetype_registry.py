"""
archetype_registry.py — 可迭代博主类型注册表
随分析案例积累，自动更新类型数据库，支持添加新类型
"""
from __future__ import annotations
import json
import os
from datetime import date
from typing import Dict, Any, Optional

_BASE = os.path.dirname(__file__)
ARCHETYPES_FILE = os.path.join(_BASE, "data", "archetypes.json")
BLOGGERS_FILE = os.path.join(_BASE, "data", "bloggers.json")


# ── 读写工具 ──────────────────────────────────────────────────

def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _save(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 类型注册表操作 ────────────────────────────────────────────

def load_archetypes() -> Dict[str, Any]:
    """加载当前所有类型（内置 + 自定义）"""
    db = _load(ARCHETYPES_FILE)
    merged = {**db["archetypes"], **db.get("custom_archetypes", {})}
    return merged


def add_archetype(key: str, name: str, desc: str, formula: str,
                  title_signals: list, content_signals: list,
                  commercial: str, difficulty: str = "中") -> str:
    """
    添加新博主类型（当现有三型无法覆盖时）

    参数:
        key    — 类型代码，如 "D"、"E" 或自定义字符串
        name   — 类型名，如 "知识科普型"
        ...
    返回: 成功提示
    """
    db = _load(ARCHETYPES_FILE)
    if key in db["archetypes"]:
        return f"⚠️ 类型 {key} 已存在于内置类型，请用其他 key"

    db["custom_archetypes"][key] = {
        "name": name,
        "desc": desc,
        "formula": formula,
        "title_signals": title_signals,
        "content_signals": content_signals,
        "commercial": commercial,
        "difficulty": difficulty,
        "examples": [],
        "confirmed_by": 0,
    }
    db["_meta"]["last_updated"] = str(date.today())
    _save(ARCHETYPES_FILE, db)
    return f"✅ 新增类型 {key}「{name}」"


def update_archetype_signals(key: str, new_title_signals: list = None,
                              new_content_signals: list = None) -> str:
    """从新分析的博主身上迭代更新信号词"""
    db = _load(ARCHETYPES_FILE)
    target = db["archetypes"].get(key) or db["custom_archetypes"].get(key)
    if not target:
        return f"❌ 类型 {key} 不存在"

    if new_title_signals:
        existing = set(target["title_signals"])
        added = [s for s in new_title_signals if s not in existing]
        target["title_signals"].extend(added)

    if new_content_signals:
        existing = set(target["content_signals"])
        added = [s for s in new_content_signals if s not in existing]
        target["content_signals"].extend(added)

    target["confirmed_by"] = target.get("confirmed_by", 0) + 1
    db["_meta"]["last_updated"] = str(date.today())
    _save(ARCHETYPES_FILE, db)
    return f"✅ 类型 {key} 信号词已更新"


def list_archetypes() -> str:
    """打印当前所有类型（用于 /xhsfx 开头展示）"""
    db = _load(ARCHETYPES_FILE)
    lines = [f"📊 当前博主类型库（{db['_meta']['last_updated']} 更新）\n"]

    for key, cfg in db["archetypes"].items():
        ex = f" — 案例: {', '.join(cfg['examples'][:2])}" if cfg["examples"] else ""
        lines.append(f"  **{key}** {cfg['name']} × {cfg['confirmed_by']}个案例{ex}")

    custom = db.get("custom_archetypes", {})
    if custom:
        lines.append("\n  **自定义类型：**")
        for key, cfg in custom.items():
            lines.append(f"  **{key}** {cfg['name']} × {cfg['confirmed_by']}个案例")

    return "\n".join(lines)


# ── 博主数据库操作 ────────────────────────────────────────────

def save_blogger(creator_name: str, user_id: str, archetype: dict,
                 stats: dict, best_topic: str, best_topic_avg: int,
                 tags: list = None, formula: str = "") -> str:
    """
    分析完成后写入博主数据库，并更新对应类型的案例数
    """
    db = _load(BLOGGERS_FILE)

    # 检查是否已存在
    existing = next((b for b in db["bloggers"] if b["user_id"] == user_id), None)
    if existing:
        existing.update({
            "analyzed_at": str(date.today()),
            "archetype": archetype["type"],
            "archetype_name": archetype["name"],
            "stats": stats,
            "best_topic": best_topic,
            "best_topic_avg": best_topic_avg,
        })
        action = "更新"
    else:
        db["bloggers"].append({
            "creator_name": creator_name,
            "user_id": user_id,
            "analyzed_at": str(date.today()),
            "archetype": archetype["type"],
            "archetype_name": archetype["name"],
            "stats": stats,
            "best_topic": best_topic,
            "best_topic_avg": best_topic_avg,
            "tags": tags or [],
            "formula": formula,
        })
        db["_meta"]["total"] = len(db["bloggers"])
        action = "新增"

    _save(BLOGGERS_FILE, db)

    # 同步更新类型案例
    _update_archetype_example(archetype["type"][0], creator_name)

    return f"✅ 博主「{creator_name}」已{action}到数据库（共 {db['_meta']['total']} 位）"


def _update_archetype_example(type_key: str, creator_name: str):
    """把博主名写入对应类型的 examples 列表"""
    db = _load(ARCHETYPES_FILE)
    target = db["archetypes"].get(type_key) or db["custom_archetypes"].get(type_key)
    if target and creator_name not in target["examples"]:
        target["examples"].append(creator_name)
        target["confirmed_by"] = len(target["examples"])
        db["_meta"]["total_analyzed"] = sum(
            len(v["examples"]) for v in {**db["archetypes"], **db.get("custom_archetypes", {})}.values()
        )
        _save(ARCHETYPES_FILE, db)


def list_bloggers(archetype_filter: str = None) -> str:
    """列出已分析博主，可按类型过滤"""
    db = _load(BLOGGERS_FILE)
    bloggers = db["bloggers"]
    if archetype_filter:
        bloggers = [b for b in bloggers if archetype_filter in b["archetype"]]

    lines = [f"📋 已分析博主（共 {len(bloggers)} 位）\n"]
    for b in bloggers:
        lines.append(
            f"  · **{b['creator_name']}** [{b['archetype_name']}] "
            f"均赞{b['stats'].get('avg_likes',0):,} 最高{b['stats'].get('max_likes',0):,} "
            f"| {b['analyzed_at']}"
        )
    return "\n".join(lines)


def get_blogger(creator_name: str) -> Optional[dict]:
    """按名称查找已分析博主记录"""
    db = _load(BLOGGERS_FILE)
    return next((b for b in db["bloggers"] if b["creator_name"] == creator_name), None)
