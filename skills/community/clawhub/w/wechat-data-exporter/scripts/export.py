#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信视频号数据导出技能 - V1 (Restored & Portable)
"""
import os
import sys
import json
import requests
import io
import argparse  # <-- 修正：补上这行导入
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import quote

# ==================== 配置区域 (Restored - 动态路径) ====================

def find_openclaw_root() -> Optional[Path]:
    """健壮地向上查找 .openclaw 根目录。"""
    current_path = Path(__file__).resolve().parent
    for _ in range(5):
        if (current_path / 'config.json').exists() and (current_path / 'skills').is_dir():
            return current_path
        if current_path.parent == current_path: break
        current_path = current_path.parent
    home_path = Path.home() / '.openclaw'
    return home_path if home_path.exists() else None

OPENCLAW_ROOT = find_openclaw_root()

if not OPENCLAW_ROOT:
    print("致命错误：无法定位 .openclaw 根目录。", file=sys.stderr)
    sys.exit(1)

# 安全地将输出指向 workspace
OUTPUT_DIR = OPENCLAW_ROOT / "workspace" / "data" / "wechat-data-exporter"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_BASE_URL = "https://boss-ip.da-mai.com/api/v1"
API_ENDPOINTS = {
    "短视频数据": "/lead/heating/short-video/export",
    "直播数据": "/lead/heating/live-video/export",
    "私信数据": "/lead/heating/private-message/export",
    "视频号加热数据": "/lead/heating/heating/export"
}

# ==================== 核心API函数 (已还原) ====================

def call_api(endpoint: str, author_name_encoded: str) -> Dict[str, Any]:
    """
    调用API (无签名版)，并返回响应内容。
    严格遵循 SKILL.md 的描述。
    """
    try:
        url = f"{API_BASE_URL}{endpoint}"
        params = {"author": author_name_encoded}
        print(f"[下载] 请求参数：{params}","https://boss-ip.da-mai.com/api/v1/lead/heating/short-video/export?author=%E5%B3%A1%E5%B7%9E%E5%9B%BD%E6%97%85")
        # 构建完整 URL 用于调试
        full_url = requests.Request('GET', url, params=params).prepare().url
        print(f"[DEBUG] 完整请求 URL: {full_url}")
        response = requests.get(url, params=params, timeout=60, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()

        if 'json' in content_type:
            return {"type": "json", "data": response.json()}
        elif 'excel' in content_type or 'spreadsheet' in content_type or 'octet-stream' in content_type:
            return {"type": "file", "data": response.content}
        else:
            return {"type": "text", "data": response.text}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"API 请求失败: {e}"
        if e.response is not None:
             error_msg += f" | Status: {e.response.status_code} | Body: {e.response.text}"
        return {"type": "error", "data": error_msg}

def save_file(data: bytes, filename: str) -> str:
    """将二进制数据保存到文件。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    filepath.write_bytes(data)
    return str(filepath)

# ==================== 主程序 ====================
def main(author_name: str):
    print("=" * 60)
    print(f"数据下载任务 (还原模式) - 客户：{author_name}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}
    # author_name_encoded = quote(author_name) # URL编码

    for data_type, endpoint in API_ENDPOINTS.items():
        print(f"\n[下载] 正在获取 [{data_type}]...")
        # result = call_api(endpoint, author_name_encoded)
        result = call_api(endpoint, author_name)
        if result["type"] == "error":
            print(f"  ❌ 失败：{result['data']}")
            results[data_type] = {"status": "failed", "error": result["data"]}
        elif result["type"] == "file":
            filename = f"{author_name}-{data_type}-{timestamp}.xlsx"
            filepath = save_file(result["data"], filename)
            print(f"  ✅ 成功！文件已保存：{filepath}")
            results[data_type] = {"status": "success", "file": filepath}
        else:
            print(f"  ⚠️ 收到非文件响应 ({result['type']})：{result['data']}")
            results[data_type] = {"status": "non-file", "data": result['data']}

    report_path = OUTPUT_DIR / f"{author_name}-下载汇总报告-{timestamp}.json"
    report_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print("\n" + "=" * 60)
    print(f"📊 汇总报告已生成: {report_path}")
    print(f"REPORT_PATH:{report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="微信视频号数据导出器 (还原模式)")
    parser.add_argument("client_name", help="客户的完整名称（视频号名称）")
    args = parser.parse_args()
    main(args.client_name)
