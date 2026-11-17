# -*- coding: utf-8 -*-
"""
备份 / 恢复 —— 导出、备份、恢复。

默认目标：本地文件（零密钥、零联网、立即可用）。
可插拔目标：百度网盘（baidunetdisk）。该适配器仅在「用户已配置本地 token」时启用；
未配置则给出明确指引，绝不偷偷联网或要求密钥。

设计原则：
  - 备份是「可恢复」的：snapshot(JSON) + 每日日志原文一并打包到备份目录。
  - 保留最近 N 份（config.BACKUP_KEEP），自动清理过旧备份。
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime

from . import config, health, store, embeddings


def export_local(backup_dir: str | None = None) -> dict:
    """
    导出到本地备份目录：快照 + 每日日志原文。
    返回 {backup_path, snapshot, logs_copied}。
    """
    config.ensure_dirs()
    if backup_dir is None:
        backup_dir = str(config.ZWJH_DIR / "backups")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"zwjh_backup_{stamp}")
    os.makedirs(dest, exist_ok=True)

    # 1) 快照（图谱 + 事实 + 配置）
    snap = health.snapshot(os.path.join(dest, "snapshot.json"))

    # 2) 每日日志原文
    logs_copied = 0
    logs_src = config.MEMORY_DIR
    logs_dst = os.path.join(dest, "daily_logs")
    os.makedirs(logs_dst, exist_ok=True)
    for fp in sorted(logs_src.glob("20??-??-??.md")):
        try:
            shutil.copy2(fp, os.path.join(logs_dst, fp.name))
            logs_copied += 1
        except Exception:
            pass

    # 3) 清理旧备份（保留最近 BACKUP_KEEP 份）
    _prune_backups(backup_dir)

    return {"backup_path": dest, "snapshot": snap, "logs_copied": logs_copied}


def _prune_backups(backup_dir: str) -> None:
    try:
        items = sorted(
            [d for d in os.listdir(backup_dir) if d.startswith("zwjh_backup_")],
            reverse=True,
        )
        for old in items[config.BACKUP_KEEP:]:
            shutil.rmtree(os.path.join(backup_dir, old), ignore_errors=True)
    except Exception:
        pass


def restore_local(backup_path: str, include_logs: bool = True) -> dict:
    """从本地备份恢复（快照写回库；可选覆盖每日日志）。"""
    snap_file = os.path.join(backup_path, "snapshot.json")
    if not os.path.exists(snap_file):
        return {"status": "error", "reason": "no_snapshot"}
    with open(snap_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 写回实体/关系/事实
    conn = store.get_conn()
    # 清空派生索引（保留每日日志原文）
    store.wipe_memories_only()
    ent_id_map = {}
    for e in data.get("entities", []):
        new_id = store.upsert_entity(e["type"], e["name"],
                                     json.loads(e.get("aliases_json", "[]")),
                                     e.get("importance", 0.5))
        ent_id_map[e["id"]] = new_id
    for r in data.get("relations", []):
        frm = ent_id_map.get(r["from_id"])
        to = ent_id_map.get(r["to_id"])
        if frm and to:
            store.add_relation(frm, to, r["relation"], r.get("weight", 1.0),
                               r.get("confidence", 1.0))
    # 事实写回
    for fct in data.get("facts", []):
        eid = ent_id_map.get(fct["entity_id"])
        if eid:
            conn.execute(
                "INSERT INTO facts(entity_id, predicate, value, valid_from, valid_to, "
                "superseded, source_memory_id, created_at) VALUES(?,?,?,?,?,?,?,?)",
                (eid, fct["predicate"], fct["value"], fct.get("valid_from"),
                 fct.get("valid_to"), fct.get("superseded", 0),
                 None, fct.get("created_at")),
            )

    # 记忆写回（快照含记忆，避免恢复后记忆表为空导致数据丢失）
    for m in data.get("memories", []):
        try:
            toks = json.loads(m.get("tokens_json", "[]"))
        except Exception:
            toks = embeddings.tokenize(m.get("raw_text", ""))
        store.add_memory(
            m.get("day", config.today_str()),
            m.get("source", "conversation"),
            m.get("raw_text", ""),
            m.get("norm_hash", ""),
            toks,
            importance=float(m.get("importance", 0.5)),
        )
    conn.commit()

    logs_restored = 0
    if include_logs:
        logs_src = os.path.join(backup_path, "daily_logs")
        if os.path.isdir(logs_src):
            for fp in os.listdir(logs_src):
                if fp.endswith(".md"):
                    try:
                        shutil.copy2(os.path.join(logs_src, fp),
                                     os.path.join(str(config.MEMORY_DIR), fp))
                        logs_restored += 1
                    except Exception:
                        pass
    return {"status": "ok", "entities": len(ent_id_map),
            "logs_restored": logs_restored}


# ── 百度网盘适配器（可插拔，零密钥默认不可用） ──────────────────────────────
def backup_baidunetdisk(backup_dir: str | None = None) -> dict:
    """
    备份到百度网盘。

    仅在用户本地已配置百度网盘访问凭证时可用（凭证存于本地 config，不进技能包）。
    未配置时返回明确指引，不报错、不联网试探。
    """
    cfg = config.load_config()
    token = cfg.get("baidunetdisk", {}).get("access_token")
    if not token:
        return {
            "status": "unavailable",
            "reason": "未配置百度网盘凭证",
            "hint": "在 config.json 写入 baidunetdisk.access_token 即可启用；"
                    "或先运行「本地备份」再做手动上传。",
        }
    # 已配置：本地先导出，再调用上传适配器（mixin 接口，便于替换实现）
    local = export_local(backup_dir)
    return _upload_to_baidu(local["backup_path"], token)


def _upload_to_baidu(local_path: str, token: str) -> dict:
    """
    上传适配器占位实现：优先使用已安装的 `bypy` CLI（需用户自行授权）。
    不内置任何密钥；这里只负责调用已授权的本地客户端。
    """
    import subprocess

    try:
        proc = subprocess.run(
            ["bypy", "upload", local_path, "/zwjh_backup/"],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode == 0:
            return {"status": "ok", "via": "bypy", "path": local_path}
        return {"status": "error", "reason": proc.stderr[:200]}
    except FileNotFoundError:
        return {
            "status": "unavailable",
            "reason": "未找到 bypy 客户端",
            "hint": "pip install bypy 并完成授权后可启用百度网盘自动备份。",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)[:200]}


if __name__ == "__main__":
    print(export_local())
