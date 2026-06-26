"""新闻情绪分析 Skill

数据获取策略：
- 硬数据（AKShare 新闻接口）：本地关键词统计，快速但覆盖弱
- 软数据（AI 搜索）：当 AKShare 新闻不足时，提示 AI Agent 自行搜索补充
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional

from core.core_engine import AnalysisResult


def run(
    symbol: str,
    news_list: Optional[List[Dict[str, Any]]] = None,
    news_provider: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    result = AnalysisResult(skill_name="news_analysis")

    try:
        import pandas as pd

        indicators = {}
        indicators["provider"] = "akshare"
        indicators["quality"] = "unknown"

        if news_list and isinstance(news_list, list) and len(news_list) > 0:
            df_news = pd.DataFrame(news_list)

            bullish_words = [
                "利多", "利好", "上涨", "看涨", "增产", "需求强劲", "供不应求", "去库存", "反弹", "企稳",
                "回暖", "回升", "走强", "偏强", "上行", "突破", "创新高", "供应偏紧", "现货紧张",
                "开工率提升", "采购增加", "成交活跃", "升水", "去库", "降库",
            ]
            bearish_words = [
                "利空", "利淡", "下跌", "看跌", "减产", "需求疲软", "供过于求", "累库存", "承压", "回落",
                "走弱", "偏弱", "下行", "跌破", "创新低", "供应过剩", "库存高企",
                "开工率下降", "采购清淡", "成交低迷", "贴水", "累库", "增库",
            ]

            bullish_count = 0
            bearish_count = 0
            neutral_count = 0

            for _, row in df_news.iterrows():
                title = str(row.get("title", ""))
                content = str(row.get("content", ""))
                text = title + content

                has_bullish = any(w in text for w in bullish_words)
                has_bearish = any(w in text for w in bearish_words)

                if has_bullish and not has_bearish:
                    bullish_count += 1
                elif has_bearish and not has_bullish:
                    bearish_count += 1
                else:
                    neutral_count += 1

            total = len(df_news)
            indicators["total_news_count"] = total
            indicators["bullish_news_count"] = bullish_count
            indicators["bearish_news_count"] = bearish_count
            indicators["neutral_news_count"] = neutral_count

            if total > 0:
                indicators["sentiment_ratio"] = round((bullish_count - bearish_count) / total, 4)

            if total >= 5:
                # 检查是否全部中性（关键词匹配失败）
                if bullish_count == 0 and bearish_count == 0:
                    indicators["quality"] = "all_neutral"
                    indicators["note"] = f"{total} 条新闻均为中性（关键词匹配未检出多空倾向），建议 AI Agent 搜索补全真实情绪"
                    indicators["soft_data_hint"] = (
                        f"AKShare 新闻关键词匹配判定全部中性。请 AI Agent 自行搜索 "
                        f"'{symbol} 期货 {_get_today_hint()} 行情 政策 供需 情绪'，"
                        f"补充真实的利多/利空判断。"
                    )
                    indicators["search_actions"] = [
                        {"query": f"{symbol} 期货 {_get_today_hint()} 行情 政策 供需 利多 利空", "source": "web", "priority": "high"},
                        {"query": f"site:finance.sina.com.cn OR site:eastmoney.com {symbol} 期货", "source": "finance_portal", "priority": "medium"},
                    ]
                else:
                    indicators["quality"] = "acceptable"
            else:
                indicators["quality"] = "insufficient"
                indicators["note"] = f"仅 {total} 条新闻（来自上海金属网），信号可能不具代表性"
                indicators["soft_data_hint"] = (
                    f"建议 AI Agent 自行搜索 '{symbol} 期货 {_get_today_hint()} 新闻 政策 事件'，"
                    f"交叉验证 48 小时内信息，优先关注交易所公告和产业数据。"
                )
                indicators["search_actions"] = [
                    {"query": f"{symbol} 期货 {_get_today_hint()} 新闻 政策 事件 公告", "source": "web", "priority": "high"},
                    {"query": f"site:shfe.com.cn OR site:dce.com.cn OR site:czce.com.cn {symbol} 公告", "source": "exchange", "priority": "medium"},
                ]
        else:
            indicators["total_news_count"] = 0
            indicators["quality"] = "unavailable"
            indicators["note"] = "AKShare 未返回新闻数据（部分品种无新闻接口覆盖）"
            indicators["soft_data_hint"] = (
                f"AKShare 无 {symbol} 新闻数据。请 AI Agent 自行搜索补全，参考 SKILL.md「软数据补充指南」。"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 {_get_today_hint()} 新闻 政策 事件 公告", "source": "web", "priority": "high"},
                {"query": f"site:finance.sina.com.cn OR site:eastmoney.com {symbol} 期货 新闻", "source": "finance_portal", "priority": "medium"},
            ]

        result.add_data("indicators", indicators)
        if news_list and len(news_list) > 0:
            result.add_data("data_date", news_list[0].get("date", ""))

        quality = indicators.get("quality", "unknown")
        total = indicators.get("total_news_count", 0)
        if quality in ("insufficient", "unavailable") or total < 5:
            reason = "样本不足" if total < 5 else "数据不可用"
            if total > 0:
                result.bullets.append(f"⚖️ 新闻样本仅{total}条（不足5条），该维度不纳入计分")
            result.add_warning(f"新闻{reason}，建议 AI Agent 补充搜索")
            result.set_signal("neutral", 0.0)
        elif quality == "all_neutral":
            result.bullets.append(f"⚖️ {total}条新闻均被判定为中性（关键词匹配局限），AI Agent 应自行搜索补充真实情绪")
            result.add_warning(f"新闻全部中性，建议 AI Agent 搜索 '{symbol} 期货' 获取真实多空信息")
            result.set_signal("neutral", 0.0)
        else:
            signal = _rule_based_news_signal(indicators)
            result.add_data("rule_based_signal", signal)
            result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
            result.bullets.extend(signal.get("signals", []) + signal.get("details", []))

    except Exception as e:
        result.add_error(f"新闻情绪分析出错: {e}")

    return result


def _get_today_hint() -> str:
    from datetime import datetime
    now = datetime.now()
    return f"{now.year}年{now.month}月"


def _rule_based_news_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    signals = []
    details = []

    sentiment_ratio = indicators.get("sentiment_ratio")
    bullish_count = indicators.get("bullish_news_count", 0)
    bearish_count = indicators.get("bearish_news_count", 0)
    neutral_count = indicators.get("neutral_news_count", 0)
    total_news = bullish_count + bearish_count + neutral_count

    if sentiment_ratio is not None:
        if sentiment_ratio > 0.5:
            score += 2
            details.append(f"[情绪] 比率={sentiment_ratio:.2f}，利多新闻占比远超利空")
        elif sentiment_ratio > 0.2:
            score += 1
        elif sentiment_ratio > 0:
            score += 0.5
        elif sentiment_ratio < -0.5:
            score -= 2
        elif sentiment_ratio < -0.2:
            score -= 1
        elif sentiment_ratio < 0:
            score -= 0.5

    if total_news > 0:
        details.append(f"[多空比] 利多{bullish_count}篇 vs 利空{bearish_count}篇 vs 中性{neutral_count}篇")
        if bullish_count == 0 and bearish_count == 0:
            details.append("⚖️ 当日无显著多空新闻，该维度不纳入计分")
            return {
                "direction": "neutral", "confidence": 0.0, "score": 0,
                "signals": signals, "details": details,
            }
        if neutral_count > total_news * 0.6:
            details.append("[活跃度] 市场以中性消息为主，情绪偏观望")

    if score > 1:
        direction = "bullish"
        confidence = min(0.55, 0.3 + score * 0.06)
    elif score > 0:
        direction = "bullish"
        confidence = 0.4
    elif score < -1:
        direction = "bearish"
        confidence = min(0.55, 0.3 + abs(score) * 0.06)
    elif score < 0:
        direction = "bearish"
        confidence = 0.4
    else:
        direction = "neutral"
        confidence = 0.25

    return {"direction": direction, "confidence": confidence, "score": score, "signals": signals + details}
