#!/usr/bin/env python3
"""
save_config.py — 持久化 Key 配置到本地文件

用法:
    python save_config.py <phone> <key> <expire_time> [is_existing]

    expire_time 格式: "2027-07-17 19:59:59" 或 "2027-07-17"
    is_existing: "true" / "false"（可选，默认 false）

成功输出:
    {"is_new": true, "write_success": true}
    {"is_new": false, "write_success": true}   ← 同手机号同 key，视为复用

失败输出 (文件写入异常):
    {"is_new": true/false, "write_success": false, "msg": "<原因>"}

兼容旧记录: 读取旧版记录（无 is_existing 字段）时不报错，正常覆盖更新。
"""

import sys
import json
import os
import platform
from datetime import datetime


def get_config_path() -> str:
    if platform.system() == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return os.path.join(base, ".tencentmap", "tempkey.json")


def save_config(phone: str, key: str, expire_time: str, is_existing: bool = False) -> dict:
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # 读取现有记录（兼容旧版无 is_existing 字段的记录）
    records = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = {}

    # 判断新建 vs 复用
    existing = records.get(phone, {})
    is_new = not (existing.get("key") == key)

    # 构建新记录
    records[phone] = {
        "key": key,
        "expire_time": expire_time,
        "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "is_existing": is_existing,
        "quota": {
            "pv_per_day": 5000,
            "qps": 5,
        },
    }

    # 写入文件
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return {"is_new": is_new, "write_success": True}
    except Exception as e:
        return {"is_new": is_new, "write_success": False, "msg": str(e)}


def mark_expired(phone: str) -> dict:
    """将指定手机号的记录标记为 expired，并返回本地存储的 expire_time（如有）。"""
    config_path = get_config_path()
    if not os.path.exists(config_path):
        return {"found": False}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    except Exception:
        return {"found": False}

    if phone not in records:
        return {"found": False}

    expire_time = records[phone].get("expire_time", "")
    records[phone]["status"] = "expired"

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 标记失败不影响主流程

    return {"found": True, "expire_time": expire_time}


if __name__ == "__main__":
    # 正常写入模式: phone key expire_time [is_existing]
    if len(sys.argv) >= 4 and sys.argv[2] != "--mark-expired":
        is_existing = False
        if len(sys.argv) >= 5:
            is_existing = sys.argv[4].lower() == "true"
        result = save_config(sys.argv[1], sys.argv[2], sys.argv[3], is_existing)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result["write_success"] else 1)

    # 标记过期模式
    elif len(sys.argv) == 3 and sys.argv[2] == "--mark-expired":
        result = mark_expired(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    else:
        print(json.dumps(
            {"error": -1, "msg": "用法: save_config.py <phone> <key> <expire_time> [is_existing]  |  save_config.py <phone> --mark-expired"},
            ensure_ascii=False
        ))
        sys.exit(1)
