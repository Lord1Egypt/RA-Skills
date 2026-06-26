#!/usr/bin/env python3
"""
fetch_images.py — 根据文章主题自动配图（Unsplash / Pexels）

用法：
    python fetch_images.py --topic "AI大模型" --count 3 --key YOUR_UNSPLASH_KEY

返回：
    JSON 格式的图片列表，含 url, alt, credit 字段
"""

import json
import argparse
import urllib.request
import urllib.parse


# IT科技话题 → 英文搜索词映射（Unsplash 英文搜索效果更好）
TOPIC_EN_MAP = {
    "AI": "artificial intelligence technology",
    "人工智能": "artificial intelligence neural network",
    "大模型": "machine learning deep learning",
    "LLM": "language model technology",
    "芯片": "computer chip semiconductor",
    "半导体": "semiconductor microchip",
    "GPU": "graphics card computer hardware",
    "手机": "smartphone technology",
    "苹果": "apple technology macbook",
    "编程": "programming code developer",
    "代码": "code programming laptop",
    "开源": "open source software collaboration",
    "云计算": "cloud computing server data center",
    "自动驾驶": "autonomous driving car technology",
    "机器人": "robot technology automation",
    "量子": "quantum computing future technology",
    "网络安全": "cybersecurity network security hacker",
    "数据": "data analytics visualization",
    "互联网": "internet technology network",
    "区块链": "blockchain cryptocurrency technology",
}

DEFAULT_TECH_QUERY = "technology innovation future digital"


def translate_topic_to_query(topic: str) -> str:
    """将中文话题转换为适合 Unsplash 搜索的英文关键词"""
    for zh, en in TOPIC_EN_MAP.items():
        if zh in topic:
            return en
    return DEFAULT_TECH_QUERY


def fetch_unsplash(query: str, count: int, access_key: str) -> list[dict]:
    """从 Unsplash 搜索图片"""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": "landscape",  # 横版图，适合公众号
        "content_filter": "high",    # 过滤低质量图片
    })
    url = f"https://api.unsplash.com/search/photos?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {access_key}",
        "Accept-Version": "v1",
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Unsplash 请求失败: {e}") from e

    results = []
    for photo in data.get("results", []):
        results.append({
            "url": photo["urls"]["regular"],          # 1080px 宽
            "url_thumb": photo["urls"]["thumb"],      # 缩略图
            "url_full": photo["urls"]["full"],        # 原图
            "alt": photo.get("alt_description", query),
            "credit": f"Photo by {photo['user']['name']} on Unsplash",
            "credit_url": photo["links"]["html"],
            "width": photo["width"],
            "height": photo["height"],
            "source": "unsplash",
        })
    return results


def fetch_pexels(query: str, count: int, api_key: str) -> list[dict]:
    """从 Pexels 搜索图片（Unsplash 的备选方案）"""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": count,
        "orientation": "landscape",
    })
    url = f"https://api.pexels.com/v1/search?{params}"
    req = urllib.request.Request(url, headers={"Authorization": api_key})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Pexels 请求失败: {e}") from e

    results = []
    for photo in data.get("photos", []):
        results.append({
            "url": photo["src"]["large"],
            "url_thumb": photo["src"]["medium"],
            "url_full": photo["src"]["original"],
            "alt": photo.get("alt", query),
            "credit": f"Photo by {photo['photographer']} on Pexels",
            "credit_url": photo["url"],
            "width": photo["width"],
            "height": photo["height"],
            "source": "pexels",
        })
    return results


def get_article_images(
    topic: str,
    count: int = 3,
    unsplash_key: str = None,
    pexels_key: str = None,
) -> dict:
    """
    为文章获取配图套装：
    - images[0]: 封面图（宽幅，科技感强）
    - images[1]: 正文配图1（技术细节）
    - images[2]: 正文配图2（数据/趋势）
    """
    query = translate_topic_to_query(topic)
    images = []
    error_msg = None

    # 优先 Unsplash
    if unsplash_key:
        try:
            images = fetch_unsplash(query, count, unsplash_key)
        except Exception as e:
            error_msg = str(e)

    # 备选 Pexels
    if not images and pexels_key:
        try:
            images = fetch_pexels(query, count, pexels_key)
        except Exception as e:
            error_msg = str(e)

    # 都失败时，返回占位提示
    if not images:
        images = [
            {
                "url": f"https://picsum.photos/seed/{i}/1200/630",
                "alt": f"{topic} 配图{i+1}",
                "credit": "占位图，请手动替换",
                "source": "placeholder",
            }
            for i in range(count)
        ]
        error_msg = f"图片API请求失败（{error_msg}），已使用占位图。"

    return {
        "topic": topic,
        "query_en": query,
        "cover": images[0] if images else None,
        "inline": images[1:] if len(images) > 1 else [],
        "error": error_msg,
    }


def main():
    parser = argparse.ArgumentParser(description="为公众号文章自动配图")
    parser.add_argument("--topic", required=True, help="文章主题，如'AI大模型'")
    parser.add_argument("--count", type=int, default=3, help="图片数量，默认3")
    parser.add_argument("--unsplash-key", help="Unsplash API Access Key")
    parser.add_argument("--pexels-key", help="Pexels API Key（备选）")
    args = parser.parse_args()

    result = get_article_images(
        topic=args.topic,
        count=args.count,
        unsplash_key=args.unsplash_key,
        pexels_key=args.pexels_key,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
