#!/usr/bin/env python3
"""Skill 使用次数记录脚本（无需鉴权，调用失败不影响主流程）"""

import json
import urllib.request
import urllib.error

API_URL = "https://redfox.hk/story/api/skill/record/save"
SOURCE = "qoder-skill映射文件生成"


def record_usage():
    """调用记录接口上报使用次数"""
    payload = json.dumps({"source": SOURCE}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"✅ 记录成功: {result}")
    except Exception:
        pass


if __name__ == "__main__":
    record_usage()
