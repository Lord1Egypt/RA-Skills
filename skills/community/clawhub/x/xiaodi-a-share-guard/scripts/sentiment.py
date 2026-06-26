#!/usr/bin/env python3
"""
A股避雷针 - 第一层：研报语义分析（Sensing）

任务：
1. 抓取全网关于该股的最新研报和新闻
2. 利用 DuckDuckGo 过滤公关软文
3. 只抓利空隐患关键词

利空关键词库：
- 库存积压、质押、商誉减值、现金流恶化
- 亏损、减持、诉讼、监管处罚
- 应收账款堆积、存货周转下降

输出：
- 语义风险评分（0-100）
- 关键利空词频统计
- 研报情绪偏差检测
"""

import argparse
import datetime as dt
import json
import re


# ========== 利空关键词库 ==========
NEGATIVE_KEYWORDS = {
    "财务风险": [
        "商誉减值", "现金流恶化", "经营性现金流负",
        "应收账款堆积", "存货周转下降", "库存积压",
        "负债率上升", "亏损扩大", "净利润下滑"
    ],
    "股权风险": [
        "质押", "减持", "股权冻结", "控制权不稳",
        "大股东质押率", "质押平仓"
    ],
    "经营风险": [
        "停产", "裁员", "业务收缩", "订单取消",
        "客户流失", "合同纠纷", "诉讼"
    ],
    "监管风险": [
        "监管处罚", "行政处罚", "立案调查",
        "警示函", "整改", "违规"
    ],
    "市场风险": [
        "价格战", "竞争加剧", "市场份额下滑",
        "行业衰退", "需求萎缩"
    ]
}

# ========== 利好关键词库（用于对比）==========
POSITIVE_KEYWORDS = [
    "增长", "盈利", "扩张", "创新", "突破",
    "订单增加", "市场份额提升", "新产品",
    "业绩向好", "超预期"
]


# ========== 词频分析 ==========
def count_keywords(text, keywords):
    """统计关键词出现次数"""
    counts = {}
    for kw in keywords:
        # 不区分大小写
        pattern = re.compile(kw, re.IGNORECASE)
        matches = pattern.findall(text)
        counts[kw] = len(matches)
    return counts


def analyze_sentiment(texts):
    """
    分析研报情绪
    
    输入: 研报/新闻文本列表
    输出: 情绪评分 + 词频统计
    """
    all_text = " ".join(texts)
    
    # 统计利空关键词
    negative_counts = {}
    for category, keywords in NEGATIVE_KEYWORDS.items():
        counts = count_keywords(all_text, keywords)
        for kw, cnt in counts.items():
            if cnt > 0:
                negative_counts[kw] = {
                    "count": cnt,
                    "category": category
                }
    
    # 统计利好关键词
    positive_counts = count_keywords(all_text, POSITIVE_KEYWORDS)
    positive_total = sum(positive_counts.values())
    
    # 计算情绪偏差
    negative_total = sum(c["count"] for c in negative_counts.values())
    
    if positive_total + negative_total == 0:
        bias = 0  # 无明显情绪
    else:
        # 利空占比
        bias = negative_total / (positive_total + negative_total)
    
    # 风险评分（利空越多，分数越高）
    # 基础分 = 利空词频总和 * 5
    # 最高 100 分
    score = min(100, negative_total * 5)
    
    # 如果情绪偏差 > 70%（利空占主导），额外加分
    if bias > 0.7:
        score = min(100, score + 20)
    
    return {
        "negative_counts": negative_counts,
        "positive_counts": {k: v for k, v in positive_counts.items() if v > 0},
        "negative_total": negative_total,
        "positive_total": positive_total,
        "bias": round(bias * 100, 1),
        "sentiment": "偏空" if bias > 0.6 else ("偏多" if bias < 0.4 else "中性"),
        "score": score,
    }


# ========== 研报来源可信度评估 ==========
def evaluate_source_credibility(source_type, source_name):
    """
    评估研报来源可信度
    
    来源等级：
    - 官方：交易所公告、公司公告（最可信）
    - 主流媒体：东方财富、同花顺、新浪财经
    - 券商研报：中信、国泰君安等大券商
    - 社区：雪球、股吧（可信度低）
    """
    credibility_map = {
        "官方": ["cninfo", "sse", "szse", "公司公告"],
        "主流媒体": ["eastmoney", "同花顺", "sina", "腾讯财经"],
        "券商研报": ["中信证券", "国泰君安", "华泰证券", "中金公司"],
        "社区": ["雪球", "股吧", "东方财富股吧"],
    }
    
    level = "社区"  # 默认最低
    for lvl, sources in credibility_map.items():
        for s in sources:
            if s.lower() in source_name.lower():
                level = lvl
                break
    
    # 可信度评分
    score_map = {
        "官方": 100,
        "主流媒体": 80,
        "券商研报": 70,
        "社区": 30,
    }
    
    return {
        "level": level,
        "score": score_map[level],
    }


# ========== 主分析函数 ==========
def analyze_stock_sentiment(code6, texts=None):
    """
    分析个股研报情绪
    
    如果 texts 未提供，返回占位数据（实际需要 web_search 获取）
    """
    result = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": code6,
    }
    
    if texts:
        # 实际分析
        sentiment_data = analyze_sentiment(texts)
        result["sentiment"] = sentiment_data
        result["status"] = "analyzed"
    else:
        # 占位数据（需要 web_search 获取研报）
        result["sentiment"] = {
            "negative_counts": {},
            "positive_counts": {},
            "negative_total": 0,
            "positive_total": 0,
            "bias": 0,
            "sentiment": "pending",
            "score": 0,
        }
        result["status"] = "pending"
        result["message"] = "需要 web_search 获取研报数据"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="A股避雷针 - 研报语义分析")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--texts", nargs="+", help="研报文本（可选）")
    parser.add_argument("--pretty", action="store_true", help="美化输出")
    args = parser.parse_args()
    
    result = analyze_stock_sentiment(args.code, args.texts)
    
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())