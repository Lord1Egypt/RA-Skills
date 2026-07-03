#!/usr/bin/env python3
"""
save_config.py — 持久化临时 Key 配置到本地文件

用法:
    python save_config.py <phone> <key> <expire_time>

    expire_time 格式: "2026-06-25 19:54:54" 或 "2026-06-25"

成功输出:
    {"is_new": true, "write_success": true}
    {"is_new": false, "write_success": true}   ← 同手机号同 key，视为复用

失败输出 (文件写入异常):
    {"is_new": true/false, "write_success": false, "msg": "<原因>"}
"""

import sys
import json
import os
import platform
from datetime import datetime

APIS = [
    {"id": 1,   "name": "坐标转换"},
    {"id": 2,   "name": "行政区划列表"},
    {"id": 3,   "name": "子级查询"},
    {"id": 4,   "name": "逆地址解析"},
    {"id": 5,   "name": "IP定位"},
    {"id": 6,   "name": "地点搜索"},
    {"id": 7,   "name": "关键词输入提示"},
    {"id": 10,  "name": "静态图"},
    {"id": 11,  "name": "场景点吸附"},
    {"id": 38,  "name": "行政区划搜索"},
    {"id": 78,  "name": "驾车路线规划"},
    {"id": 79,  "name": "步行路线规划"},
    {"id": 80,  "name": "公交路线规划"},
    {"id": 83,  "name": "地址解析"},
    {"id": 84,  "name": "步行距离计算"},
    {"id": 85,  "name": "驾车距离计算"},
    {"id": 93,  "name": "POI详情"},
    {"id": 96,  "name": "距离矩阵驾车"},
    {"id": 100, "name": "骑行路线规划"},
    {"id": 118, "name": "距离矩阵骑行"},
    {"id": 123, "name": "沿途搜索"},
    {"id": 124, "name": "周边POI推荐"},
    {"id": 132, "name": "步行距离矩阵"},
    {"id": 204, "name": "电动车路线规划"},
    {"id": 238, "name": "智能硬件定位"},
    {"id": 264, "name": "危险区域查询"},
    {"id": 275, "name": "多边形区域搜索"},
    {"id": 290, "name": "未来驾车ETA"},
    {"id": 303, "name": "天气"},
    {"id": 323, "name": "直线距离矩阵"},
]


def get_config_path() -> str:
    if platform.system() == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return os.path.join(base, ".tencentmap", "tempkey.json")


def save_config(phone: str, key: str, expire_time: str) -> dict:
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    # 读取现有记录
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
        "quota": {
            "pv_per_day": 5000,
            "qps": 5,
            "valid_days": 14,
        },
        "apis": APIS,
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
    if len(sys.argv) == 4:
        # 正常写入模式
        result = save_config(sys.argv[1], sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result["write_success"] else 1)

    elif len(sys.argv) == 3 and sys.argv[2] == "--mark-expired":
        # 标记过期模式
        result = mark_expired(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    else:
        print(json.dumps(
            {"error": -1, "msg": "用法: save_config.py <phone> <key> <expire_time>  |  save_config.py <phone> --mark-expired"},
            ensure_ascii=False
        ))
        sys.exit(1)
