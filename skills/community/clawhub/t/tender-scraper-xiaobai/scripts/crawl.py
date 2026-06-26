#!/usr/bin/env python3
"""
招投标信息爬取脚本

数据来源：https://ygcg.nbcqjy.org

用法：
    python scripts/crawl.py
"""

import requests
import json
import argparse
from datetime import datetime

# 配置
BASE_URL = "https://ygcg.nbcqjy.org"
API_URL = "https://ygcg.nbcqjy.org/api/Portal/GetBulletinList"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://ygcg.nbcqjy.org/",
    "Origin": "https://ygcg.nbcqjy.org"
}


def crawl_tender_list(limit: int = 50) -> list:
    """爬取招标公告列表"""
    data = []
    page_size = 15  # 每页最多15条
    page_index = 1

    while len(data) < limit:
        try:
            payload = {
                "pageIndex": page_index,
                "pageSize": page_size,
                "deptId": "",
                "classID": "21",
                "ZtbTypeId": None,
                "InfoTypeId": None
            }

            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            result = response.json()

            if result.get("header", {}).get("resultType") != 1:
                break

            bulletin_list = result.get("body", {}).get("data", {}).get("bulletinList", [])

            if not bulletin_list:
                break

            for item in bulletin_list:
                if len(data) >= limit:
                    break

                title = item.get("bulletinTitle", "")
                auto_id = item.get("autoId", "")
                url = f"{BASE_URL}/detail?bulletinId={auto_id}" if auto_id else ""

                publish_time = item.get("publishDate", "")
                if publish_time and isinstance(publish_time, str):
                    if "T" in publish_time:
                        publish_time = publish_time.split("T")[0]

                # 根据infoTypeId获取类型
                info_type_id = item.get("infoTypeId", "")
                type_map = {
                    "D01": "非工程类货物",
                    "D02": "工程",
                    "D03": "非工程类服务",
                    "D04": "其他",
                    "D05": "工程类货物",
                    "D06": "工程类服务",
                    "D07": "中介超市服务"
                }
                tags = type_map.get(info_type_id, "其他")

                data.append({
                    "title": item.get("bulletinTitle", ""),
                    "url": url,
                    "publish_time": publish_time,
                    "tags": tags,
                    "tender_type": item.get("ztbtype", "")
                })

            page_index += 1

        except Exception as e:
            print(f"请求失败: {e}")
            break

    return data


def crawl_and_return_json(limit: int = 50) -> dict:
    """
    爬取招投标信息

    参数:
        limit: 获取数量

    返回:
        dict: 包含data列表的字典
    """
    data = crawl_tender_list(limit)

    return {
        "fetch_time": datetime.now().isoformat(),
        "total_count": len(data),
        "data": data
    }


if __name__ == "__main__":
    result = crawl_and_return_json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
