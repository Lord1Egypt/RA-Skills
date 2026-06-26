#!/usr/bin/env python3
"""
微信视频号视频搜索器 - TikHub API
基于官方文档实现：支持关键词搜索，返回视频下载链接和分析数据
注意：中国大陆用户使用 api.tikhub.dev 域名（api.tikhub.io 被墙）
"""

import requests
import json
import os
import sys
import argparse
from urllib.parse import quote

# API 端点（中国大陆使用新域名）
TIKHUB_SEARCH_URL = "https://api.tikhub.dev/api/v1/wechat_channels/fetch_search_latest"


def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser("~/.openclaw/config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # 如果没有配置文件，尝试从环境变量读取（备用方案）
    token = os.environ.get("TIKHUB_API_TOKEN")
    # token="8LEpSlFo2n8F7AID3HW3i3YU1hkhrr/kgb1L4ynIqDR98nEZd7tj+zWoIg=="
    if token:
        return {"tikhub_api_token": token}
    # 如果都没有，返回空字典，后续会报错
    return {}


def get_token():
    """获取 TikHub Token"""
    config = load_config()
    token = config.get("tikhub_api_token")
    if not token:
        raise ValueError(
            "❌ 缺少 TikHub API Token\n\n"
            "请配置 Token：\n"
            "1. 在 ~/.openclaw/config.json 中添加：\n"
            "   {\"tikhub_api_token\": \"你的 Token\"}\n"
            "2. 或设置环境变量 TIKHUB_API_TOKEN"
        )
    return token


def search_videos(keyword, token=None):
    """
    调用视频号搜索 API
    参数：
    - keyword: 搜索关键词
    - token: TikHub API Token
    """
    if token is None:
        token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        'accept': 'application/json'
    }

    # URL 编码关键词
    encoded_keyword = quote(keyword)
    url = f"{TIKHUB_SEARCH_URL}?keywords={encoded_keyword}"
    print("token",token)
    print("DEBUG: url=", url)
    try:
        resp = requests.get(url, headers=headers, timeout=60)
        print(f"DEBUG: status_code={resp.status_code}", file=sys.stderr)
        print(f"DEBUG: response_text={resp.text[:500]}", file=sys.stderr)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API 请求失败：{e}")
    except json.JSONDecodeError:
        raise RuntimeError("API 返回非 JSON 格式")


def format_video_item(item, idx=0):
    if not item:
        return "（数据格式异常）"

    video_id = item.get("docID", "未知 ID")
    desc = item.get("title", "无描述")[:100]
    author = item.get("source", {})
    author_name = author.get("title", "未知作者") if author else "未知作者"

    # 统计信息（注意字段名）
    like_num = item.get("likeNum", 0)
    duration = item.get("duration", "0")
    date_time = item.get("dateTime", "")

    # 视频下载链接
    video_url = item.get("videoUrl", "")
    share_url = f"https://channels.weixin.qq.com/web/pages/feed?feedId={video_id}" if video_id != "未知 ID" else ""

    return (
        f"📹 ID: {video_id}\n"
        f"📝 标题：{desc}\n"
        f"👤 作者：{author_name}\n"
        f"👍 点赞：{like_num}  ⏱️ 时长：{duration}  🕒 发布时间：{date_time}\n"
        f"🔗 下载链接：{video_url}\n"
        f"🔗 分享链接：{share_url}\n"
    )


def format_search_result(data, show_raw=False):
    """格式化整个搜索结果"""
    if show_raw:
        return json.dumps(data, indent=2, ensure_ascii=False)
    # print("1111data",data)
    # 修正：正确提取 data.data.items
    data_content = data.get("data", {})
    items = data_content.get("items", []) if isinstance(data_content, dict) else []
    
    if not items:
        return "没有找到相关视频。"
    
    lines = [f"找到 {len(items)} 个视频号视频\n"]
    for idx, item in enumerate(items, 1):
        lines.append(f"--- 第 {idx} 个 ---")
        lines.append(format_video_item(item, idx))
    
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="微信视频号视频搜索（TikHub）")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON 数据")

    args = parser.parse_args()

    try:
        result = search_videos(keyword=args.keyword)
        output = format_search_result(result, show_raw=args.raw)
        # 强制 UTF-8 输出
        sys.stdout.reconfigure(encoding='utf-8')
        print(output)
    except Exception as e:
        sys.stderr.reconfigure(encoding='utf-8')
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)
