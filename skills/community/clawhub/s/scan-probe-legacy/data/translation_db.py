# -*- coding: utf-8 -*-
"""离线翻译数据库（V1.0.5 新增）

存储模组翻译条目，支持按 mod_id + target_lang 查询。
AI Agent 翻译完成后调用 store_batch 写入，下次离线模式可直接命中。

存储格式（data/translation_entries.json）:
{
    "version": 1,
    "entries": {
        "<mod_id>": {
            "<target_lang>": {
                "<lang_key>": "<translation>"
            }
        }
    }
}
"""

import json
import os
import threading
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

# 数据文件路径
_DB_DIR = Path(__file__).resolve().parent
_DB_FILE = _DB_DIR / "translation_entries.json"

# 线程锁（防止并发写入冲突）
_lock = threading.Lock()


def _ensure_db() -> Dict[str, Any]:
    """确保数据库文件存在，返回数据内容"""
    if not _DB_FILE.exists():
        return {"version": 1, "entries": {}, "last_updated": ""}
    try:
        with open(_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "entries": {}, "last_updated": ""}


def _save_db(data: Dict[str, Any]) -> None:
    """原子写入数据库（临时文件 → os.replace）"""
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmp_file = _DB_FILE.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(str(tmp_file), str(_DB_FILE))


class TranslationDB:
    """离线翻译数据库"""

    def __init__(self):
        self._db_path = _DB_FILE

    def lookup(self, mod_id: str, lang_key: str, target_lang: str) -> Optional[str]:
        """查询单条翻译

        Args:
            mod_id: 模组 ID（如 "create"）
            lang_key: 语言文件键名（如 "block.create.cogwheel"）
            target_lang: 目标语言（如 "zh_cn"）

        Returns:
            翻译文本，未命中返回 None
        """
        with _lock:
            data = _ensure_db()
            entries = data.get("entries", {})
            mod_entry = entries.get(mod_id, {})
            lang_entry = mod_entry.get(target_lang, {})
            return lang_entry.get(lang_key)

    def lookup_batch(self, mod_id: str, target_lang: str) -> Dict[str, str]:
        """批量查询某模组某语言的所有翻译

        Args:
            mod_id: 模组 ID
            target_lang: 目标语言

        Returns:
            {key: translation} 字典，未命中返回空字典
        """
        with _lock:
            data = _ensure_db()
            entries = data.get("entries", {})
            mod_entry = entries.get(mod_id, {})
            return mod_entry.get(target_lang, {})

    def store_batch(self, mod_id: str, target_lang: str, entries: Dict[str, str]) -> None:
        """批量存储翻译条目（AI 翻译完成后调用）

        Args:
            mod_id: 模组 ID
            target_lang: 目标语言
            entries: {key: translation} 字典
        """
        with _lock:
            data = _ensure_db()
            db_entries = data.setdefault("entries", {})
            mod_entry = db_entries.setdefault(mod_id, {})
            lang_entry = mod_entry.setdefault(target_lang, {})
            # 合并新条目（覆盖旧值）
            lang_entry.update(entries)
            _save_db(data)

    def stats(self) -> Dict[str, Any]:
        """返回数据库统计信息

        Returns:
            {mods, languages, total_entries, last_updated}
        """
        with _lock:
            data = _ensure_db()
            entries = data.get("entries", {})
            mod_count = len(entries)
            total = 0
            languages = set()
            for mod_id, langs in entries.items():
                for lang, kv in langs.items():
                    languages.add(lang)
                    total += len(kv)
            return {
                "mods": mod_count,
                "languages": sorted(languages),
                "total_entries": total,
                "last_updated": data.get("last_updated", ""),
            }

    def clear_mod(self, mod_id: str) -> int:
        """清除某模组的所有翻译条目

        Returns:
            被删除的条目数
        """
        with _lock:
            data = _ensure_db()
            entries = data.get("entries", {})
            if mod_id not in entries:
                return 0
            removed = 0
            for lang, kv in entries[mod_id].items():
                removed += len(kv)
            del entries[mod_id]
            _save_db(data)
            return removed


# 单例
_db_instance = TranslationDB()


def get_db() -> TranslationDB:
    """获取 TranslationDB 单例"""
    return _db_instance


# === 命令行入口 ===
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python -m data.translation_db <stats|lookup|clear>")
        print("  stats                    - 查看统计")
        print("  lookup <mod_id> <lang>   - 查询某模组翻译")
        print("  clear <mod_id>           - 清除某模组翻译")
        sys.exit(0)

    cmd = sys.argv[1]
    db = get_db()

    if cmd == "stats":
        s = db.stats()
        print(f"模组数: {s['mods']}")
        print(f"语言: {', '.join(s['languages']) or '无'}")
        print(f"总条目: {s['total_entries']}")
        print(f"最后更新: {s['last_updated'] or '无'}")

    elif cmd == "lookup" and len(sys.argv) >= 4:
        mod_id = sys.argv[2]
        lang = sys.argv[3]
        entries = db.lookup_batch(mod_id, lang)
        if not entries:
            print(f"无 {mod_id} 的 {lang} 翻译")
        else:
            for k, v in entries.items():
                print(f"  {k} = {v}")

    elif cmd == "clear" and len(sys.argv) >= 3:
        mod_id = sys.argv[2]
        n = db.clear_mod(mod_id)
        print(f"已清除 {mod_id} 的 {n} 条翻译")

    else:
        print(f"未知命令: {cmd}")
