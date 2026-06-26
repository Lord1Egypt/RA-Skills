"""
Futu 搜索层桥接器

封装 Futu 三个 HTTP API 为 Python 类：
- news_search: 新闻搜索 / 个股摘要
- stock_feed: 社区评论/情绪

Base URL: https://ai-news-search.futunn.com
"""

import re
import time
import logging
from typing import Optional, List, Dict
from datetime import datetime

import httpx
import pandas as pd

logger = logging.getLogger(__name__)

BASE_URL = "https://ai-news-search.futunn.com"

# ============== 情绪关键词 ==============

BULLISH_KEYWORDS = [
    "看涨", "利好", "大涨", "突破", "买入", "增持", "看好",
    "反弹", "抄底", "牛市", "做多", "强势", "放量上涨",
    "涨停", "创新高", "业绩大增", "超预期", "拐点",
    "bullish", "buy", "long", "moon", "pump",
]

BEARISH_KEYWORDS = [
    "看跌", "利空", "大跌", "暴跌", "卖出", "减持", "看空",
    "回调", "出货", "熊市", "做空", "弱势", "放量下跌",
    "跌停", "创新低", "业绩暴雷", "不及预期", "风险",
    "bearish", "sell", "short", "dump", "crash",
]

NEUTRAL_KEYWORDS = [
    "震荡", "观望", "持有", "中性", "横盘", "整理",
    "neutral", "hold", "wait",
]


class FutuBridge:
    """Futu 搜索 API 桥接器"""

    def __init__(self, timeout: float = 10.0):
        self.client = httpx.Client(timeout=timeout, follow_redirects=True)
        self.base_url = BASE_URL

    # ──────────────────────────────────────────
    # API 1: 新闻搜索
    # ──────────────────────────────────────────

    def search_news(
        self,
        keyword: str,
        size: int = 10,
        news_type: int = 1,
        sort_type: int = 2,
    ) -> pd.DataFrame:
        """
        搜索个股新闻

        Args:
            keyword: 搜索关键词（股票代码或名称）
            size: 返回条数
            news_type: 1=全部, 2=公告, 3=研报
            sort_type: 2=时间倒序, 1=相关度

        Returns:
            pd.DataFrame with columns: [news_id, news_type, title, publish_time, url, img_url, publish_date]
        """
        url = f"{self.base_url}/news_search"
        params = {
            "keyword": keyword,
            "size": size,
            "news_type": news_type,
            "sort_type": sort_type,
        }

        try:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.warning(f"[FutuBridge] search_news failed for '{keyword}': {e}")
            return pd.DataFrame()

        if data.get("code") != 0 or not data.get("data"):
            logger.warning(f"[FutuBridge] search_news empty for '{keyword}': {data}")
            return pd.DataFrame()

        records = []
        for item in data["data"]:
            pub_ts = item.get("publish_time", 0)
            pub_dt = self._parse_timestamp(pub_ts)
            records.append({
                "news_id": item.get("news_id", ""),
                "news_type": item.get("news_type", 0),
                "title": self._strip_html(str(item.get("title", ""))),
                "publish_time": pub_ts,
                "publish_date": pub_dt,
                "url": item.get("url", ""),
                "img_url": item.get("img_url", ""),
            })

        df = pd.DataFrame(records)
        return df

    # ──────────────────────────────────────────
    # API 2: 社区评论 / Feed
    # ──────────────────────────────────────────

    def get_stock_feed(self, keyword: str, size: int = 30) -> pd.DataFrame:
        """
        获取个股社区评论

        Args:
            keyword: 搜索关键词
            size: 返回条数（越大情绪越准确，建议 >= 20）

        Returns:
            pd.DataFrame with columns: [id, title, publish_time, desc, clean_text, sentiment_label]
        """
        url = f"{self.base_url}/stock_feed"
        params = {"keyword": keyword, "size": size}

        try:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.warning(f"[FutuBridge] get_stock_feed failed for '{keyword}': {e}")
            return pd.DataFrame()

        if data.get("code") != 0 or not data.get("data"):
            logger.warning(f"[FutuBridge] get_stock_feed empty for '{keyword}'")
            return pd.DataFrame()

        records = []
        for item in data["data"]:
            raw_title = str(item.get("title", ""))
            raw_desc = str(item.get("desc", ""))
            clean_text = self._strip_html(raw_title + " " + raw_desc)
            sentiment_label = self._classify_sentiment(clean_text)

            pub_ts = item.get("publish_time", 0)
            pub_dt = self._parse_timestamp(pub_ts)

            records.append({
                "id": item.get("id", ""),
                "title": self._strip_html(raw_title),
                "publish_time": pub_ts,
                "publish_date": pub_dt,
                "desc": self._strip_html(raw_desc),
                "clean_text": clean_text,
                "sentiment_label": sentiment_label,
            })

        df = pd.DataFrame(records)
        return df

    # ──────────────────────────────────────────
    # API 3: 个股摘要（同 news_search）
    # ──────────────────────────────────────────

    def get_stock_digest(self, symbol: str) -> dict:
        """
        获取个股摘要：结合新闻 + 社区评论

        Returns:
            dict: {conclusion, signals, evidence}
        """
        news_df = self.search_news(symbol, size=5, news_type=1, sort_type=2)
        feed_df = self.get_stock_feed(symbol, size=20)

        signals = []
        evidence = []

        # 新闻摘要
        if not news_df.empty:
            titles = news_df["title"].tolist()
            evidence.append({"type": "news", "count": len(titles), "titles": titles[:3]})
            # 检测关键词信号
            all_titles = " ".join(titles).lower()
            if any(kw in all_titles for kw in ["利好", "突破", "增长", "中标"]):
                signals.append("利好新闻信号")
            if any(kw in all_titles for kw in ["利空", "风险", "下跌", "减持"]):
                signals.append("利空新闻信号")

        # 社区情绪
        if not feed_df.empty:
            sentiment_counts = feed_df["sentiment_label"].value_counts()
            total = len(feed_df)
            bullish_pct = int(sentiment_counts.get("bullish", 0) / total * 100)
            bearish_pct = int(sentiment_counts.get("bearish", 0) / total * 100)
            evidence.append({
                "type": "feed_sentiment",
                "total": total,
                "bullish_pct": bullish_pct,
                "bearish_pct": bearish_pct,
            })
            if bullish_pct > bearish_pct + 20:
                signals.append(f"社区情绪看多 ({bullish_pct}%看涨)")
            elif bearish_pct > bullish_pct + 20:
                signals.append(f"社区情绪看空 ({bearish_pct}%看跌)")

        # Conclusion
        if not signals:
            conclusion = "暂无明显信号"
        elif len(signals) >= 2 and all("看多" in s or "利好" in s for s in signals):
            conclusion = "综合偏多"
        elif len(signals) >= 2 and all("看空" in s or "利空" in s for s in signals):
            conclusion = "综合偏空"
        else:
            conclusion = "多空交织"

        return {
            "conclusion": conclusion,
            "signals": signals,
            "evidence": evidence,
        }

    # ──────────────────────────────────────────
    # 情绪评分
    # ──────────────────────────────────────────

    def get_sentiment(self, symbol: str) -> dict:
        """
        基于社区评论计算个股情绪评分

        Returns:
            dict: {bullish_pct, bearish_pct, neutral_pct, label, summary}
        """
        feed_df = self.get_stock_feed(symbol, size=30)

        if feed_df.empty:
            return {
                "bullish_pct": 50,
                "bearish_pct": 50,
                "neutral_pct": 0,
                "label": "unknown",
                "summary": "无社区数据",
            }

        total = len(feed_df)
        sentiment_counts = feed_df["sentiment_label"].value_counts()

        bullish_pct = int(sentiment_counts.get("bullish", 0) / total * 100)
        bearish_pct = int(sentiment_counts.get("bearish", 0) / total * 100)
        neutral_pct = 100 - bullish_pct - bearish_pct

        # 情绪标签判定
        if abs(bullish_pct - bearish_pct) < 15 and bullish_pct >= 25 and bearish_pct >= 25:
            label = "mixed"
        elif bullish_pct > bearish_pct + 15:
            label = "bullish"
        elif bearish_pct > bullish_pct + 15:
            label = "bearish"
        else:
            label = "neutral"

        summary = (
            f"Futu社区情绪：看涨{bullish_pct}%，看跌{bearish_pct}%，中性{neutral_pct}%"
        )

        return {
            "bullish_pct": bullish_pct,
            "bearish_pct": bearish_pct,
            "neutral_pct": neutral_pct,
            "label": label,
            "summary": summary,
        }

    def batch_sentiment(self, symbols: list) -> dict:
        """
        批量获取情绪评分

        Returns:
            dict: {symbol: {bullish_pct, bearish_pct, neutral_pct, label, summary}}
        """
        result = {}
        for sym in symbols:
            try:
                result[sym] = self.get_sentiment(sym)
            except Exception as e:
                logger.warning(f"[FutuBridge] batch_sentiment failed for '{sym}': {e}")
                result[sym] = {
                    "bullish_pct": 50,
                    "bearish_pct": 50,
                    "neutral_pct": 0,
                    "label": "error",
                    "summary": f"分析异常: {e}",
                }
        return result

    def get_sentiment_score(self, symbol: str) -> float:
        """
        返回 0~1 的情绪评分（供 ScoringEngine 使用）
        """
        sentiment = self.get_sentiment(symbol)
        bullish = sentiment.get("bullish_pct", 50)
        bearish = sentiment.get("bearish_pct", 50)
        # bullish_pct 越高 → score 越高
        # bearish_pct 越高 → score 越低
        net = (bullish - bearish) / 100.0  # -1.0 ~ 1.0
        return max(0.0, min(1.0, 0.5 + net / 2.0))

    # ──────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────

    @staticmethod
    def _strip_html(text: str) -> str:
        """去除 HTML 标签"""
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _parse_timestamp(ts) -> str:
        """
        兼容 unix 秒 (10位) 和 毫秒 (13位)
        返回格式: YYYY-MM-DD HH:MM:SS
        """
        try:
            ts = int(ts)
            if ts > 1e12:  # 毫秒
                ts = ts // 1000
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError, OverflowError):
            return ""

    @staticmethod
    def _classify_sentiment(text: str) -> str:
        """
        基于关键词判断单条评论情绪

        Returns:
            "bullish" / "bearish" / "neutral"
        """
        if not text.strip():
            return "neutral"

        text_lower = text.lower()

        # 看涨关键词计数
        bullish_score = sum(1 for kw in BULLISH_KEYWORDS if kw.lower() in text_lower)
        bearish_score = sum(1 for kw in BEARISH_KEYWORDS if kw.lower() in text_lower)
        neutral_score = sum(1 for kw in NEUTRAL_KEYWORDS if kw.lower() in text_lower)

        # 带价格目标的正向表达
        if re.search(r"目标.*\d+", text) and not any(kw in text_lower for kw in ["看空", "卖出"]):
            bullish_score += 1

        # 看多/看空互斥
        if bullish_score > bearish_score and bullish_score > neutral_score:
            return "bullish"
        elif bearish_score > bullish_score and bearish_score > neutral_score:
            return "bearish"
        else:
            return "neutral"


# ============== 快捷函数 ==============

def create_bridge() -> FutuBridge:
    return FutuBridge()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bridge = FutuBridge()

    # 测试新闻搜索
    print("=== News Search (600036) ===")
    news = bridge.search_news("600036", size=5)
    print(news.to_string(max_colwidth=60))

    print("\n=== Stock Feed (600036) ===")
    feed = bridge.get_stock_feed("600036", size=10)
    print(feed.to_string(max_colwidth=60))

    print("\n=== Sentiment (600036) ===")
    sent = bridge.get_sentiment("600036")
    print(sent)

    print("\n=== Digest (600036) ===")
    digest = bridge.get_stock_digest("600036")
    print(digest)
