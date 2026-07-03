"""
trends/api.py - Trending data fetching API
"""

import sys
from typing import Optional
from core import TrendingResult
from core.http_client import NoSNIClient

API_BASE_URL = "https://onetotenvip.com/skill/cozeSkill/getWxCozeSkillData"


def fetch_trending_data(
    keyword: str,
    start_date: Optional[str] = None,
    client: Optional[NoSNIClient] = None,
    debug: bool = False,
    max_retries: int = 3
) -> TrendingResult:
    """
    Fetch trending articles from the API.

    Args:
        keyword: Search keyword for trending articles
        start_date: Optional start date filter (YYYY-MM-DD format)
        client: Optional HTTP client (creates default if not provided)
        debug: Enable debug output
        max_retries: Maximum retry attempts

    Returns:
        TrendingResult containing raw categories and articles

    Raises:
        Exception: On API failure after retries
    """
    if client is None:
        client = NoSNIClient()

    params = {
        "keyword": keyword,
        "source": "公众号爆款文章洞察-ClawHub"
    }

    if start_date:
        params["startDate"] = start_date

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }

    last_error = None
    for attempt in range(max_retries):
        if debug:
            print(f"\n=== DEBUG: 第 {attempt + 1} 次尝试 ===", file=sys.stderr)

        try:
            response = client.fetch_json(API_BASE_URL, params, headers)

            if debug:
                print(f"状态码: 200", file=sys.stderr)
                print(f"响应长度: {len(str(response))} 字节", file=sys.stderr)

            if "data" not in response:
                raise Exception(f"API 错误: {response.get('msg', '未知错误')}")

            result_data = response.get("data", {})

            if debug:
                import json
                print("=== DEBUG: API 返回的 data 字段键 ===", file=sys.stderr)
                print(json.dumps(list(result_data.keys()), ensure_ascii=False, indent=2), file=sys.stderr)

            return TrendingResult(
                keyword=keyword,
                raw_categories={
                    "low_fan_explosive": result_data.get("lowPowderExplosiveArticle", []),
                    "ten_w_reading": result_data.get("tenWReadingRank", []),
                    "original_rank": result_data.get("originalRank", []),
                    "one_w_reading": result_data.get("oneWReadingRank", [])
                }
            )

        except Exception as e:
            last_error = str(e)
            if debug:
                print(f"  错误: {type(e).__name__}: {str(e)[:100]}", file=sys.stderr)
            import time
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            continue

    raise Exception(f"{last_error}（已尝试 {max_retries} 次）")