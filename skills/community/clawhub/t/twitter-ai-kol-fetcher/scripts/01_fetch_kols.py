#!/usr/bin/env python3
"""
Twitter KOL Fetcher - Data Fetcher
抓取 KOL 推文数据
"""

import requests
import json
import time
import os
from datetime import datetime

# 读取配置（优先从配置文件，否则用默认）
def load_config():
    """从配置文件加载 API Key"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

CONFIG = load_config()

# 配置
API_KEY = CONFIG.get("twitter_api_key", "new1_7590bc837c4d4104ada0ef3419ab7d6c")  # 默认值供本地使用
BASE_URL = "https://api.twitterapi.io/twitter/user/last_tweets"

# [优化] 每 KOL 抓取数量（最新 N 条）
# 扩大信源后，每 KOL 少抓，降低成本
MAX_RESULTS_PER_KOL = 1

# KOL 列表（从 references/kol_list.json 加载）
# 默认列表，可以后续在 kol_list.json 中扩展
DEFAULT_KOL_LIST = [
    # AI 公司官方
    "OpenAI", "AnthropicAI", "GoogleAI", "MetaAI", "xAI", "MistralAI",
    "CohereAI", "PerplexityAI", "RunwayAI", "StabilityAI",
    # CEO/创始人
    "sama", "elonmusk", "DarioAmodei", "AndrewYNg", "ylecun",
    "JeffDean", "pmarca", "cdixon", "michaelnieera",
    # 投资人
    "a16z", "sequoia", "greylock", "genecenter",
    # 顶流博主
    "hwchase17", "sherwinwu", "swyx", "sx", "heyBarsee",
    "thefireship", "mgsiegler", "emollick", "benhylak",
    # 研究员
    "polynoamial", "goodfellow_ian", "sarah_ocker", "rohanvarma",
    "mitchellh", "Steve0x2A"
]

def fetch_user_tweets(username, max_results=MAX_RESULTS_PER_KOL):
    """获取用户最新推文"""
    url = f"{BASE_URL}?userName={username}&max_results={max_results}"
    headers = {"x-api-key": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if data.get("status") == "success":
            tweets = data.get("data", {}).get("tweets", [])
            return tweets
        else:
            print(f"[{username}] API error: {data.get('msg', 'unknown')}")
            return []
    except Exception as e:
        print(f"[{username}] Error: {e}")
        return []

def process_tweet(tweet):
    """提取关键信息"""
    return {
        "id": tweet.get("id"),
        "text": tweet.get("text", ""),
        "url": tweet.get("url", ""),
        "created_at": tweet.get("createdAt", ""),
        "likes": tweet.get("likeCount", 0),
        "retweets": tweet.get("retweetCount", 0),
        "views": tweet.get("viewCount", 0),
        "author": tweet.get("author", {}).get("userName", ""),
        "author_name": tweet.get("author", {}).get("name", "")
    }

def load_kol_list():
    """[新增] 从 JSON 加载 KOL 列表"""
    import os
    json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "..", "references", "kol_list.json"
    )
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 支持多种格式：{"kols": [...]} 或 [...]
                if isinstance(data, dict) and "kols" in data:
                    return data["kols"]
                elif isinstance(data, list):
                    return data
        except Exception as e:
            print(f"[警告] 加载 kol_list.json 失败: {e}")
    
    # 返回默认列表
    return DEFAULT_KOL_LIST

def main(kol_list=None):
    """主函数：抓取所有 KOL 推文"""
    all_tweets = []
    
    # 优先使用传入的 KOL 列表，否则从 JSON 加载，否则用默认
    if kol_list is None:
        kol_list = load_kol_list()
    
    print(f"开始抓取 {len(kol_list)} 个 KOL 的推文（每 KOL {MAX_RESULTS_PER_KOL} 条）...")
    start_time = time.time()

    for i, username in enumerate(kol_list):
        print(f"[{i+1}/{len(KOL_LIST)}] 抓取 @{username}...")

        tweets = fetch_user_tweets(username, max_results=5)

        for tweet in tweets:
            processed = process_tweet(tweet)
            processed["username"] = username
            all_tweets.append(processed)

        # 避免请求过快
        time.sleep(0.2)

    elapsed = time.time() - start_time
    print(f"\n抓取完成！共获取 {len(all_tweets)} 条推文，耗时 {elapsed:.1f}秒")

    # 保存到临时文件（供下一步使用）
    output_file = f"/tmp/kol_tweets_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    main()
