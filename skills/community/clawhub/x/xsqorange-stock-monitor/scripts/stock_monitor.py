#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

"""
Stock Monitor - 股票监控分析脚本
功能：获取实时行情、K线数据、技术指标分析、信号提醒
支持：新浪财经API + 腾讯财经API
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 配置文件路径
CONFIG_FILE = os.path.expanduser("~/.openclaw/stock-pool.json")
POSITIONS_FILE = os.path.expanduser("~/.openclaw/stock-positions.json")
TRADES_FILE = os.path.expanduser("~/.openclaw/stock-trades.json")

# ============ 资讯新闻获取 ============

def get_stock_news(code: str, limit: int = 10) -> List[Dict]:
    """获取股票最新资讯（东方财富+新浪，多来源合并）"""
    news_results = []
    seen_titles = set()
    
    # 判断是否为港股（4-5位数字，以0开头）
    is_hk = len(code) >= 4 and len(code) <= 5 and code.startswith("0")
    
    if is_hk:
        # 港股新闻源：东方财富 + 新浪财经港股
        sources = [
            # 东方财富港股资讯 (JSONP)
            (f"https://search-api-web.eastmoney.com/search/jsonp?param={{\"uid\":\"\",\"keyword\":\"{code}\",\"type\":[\"stockNote\"],\"client\":\"web\",\"clientType\":\"pc\",\"clientVersion\":\"curr\",\"param\":{{\"market\":\"hk\",\"start\":\"0\",\"count\":\"{limit}\"}}}}", "eastmoney_hk", "https://www.eastmoney.com/"),
            # 新浪财经港股公司新闻 (HTML，需解析)
            (f"https://finance.sina.com.cn/realstock/company/hk{code}/nc.shtml", "sina_hk", "https://finance.sina.com.cn/"),
        ]
    else:
        sources = [
            # 东方财富公告
            ("https://np-anotice-stock.eastmoney.com/api/security/ann?cb=&sr=-1&page_size={limit}&page_index=1&ann_type=SHA%2CSZA&client_source=web&stock_list=" + code, "eastmoney", "https://www.eastmoney.com/"),
            # 东方财富资讯新闻
            ("https://np-listapi.eastmoney.com/comm/web/getNewsByColumn?cb=&client=web&bType=1&start=0&pageSize=" + str(limit) + "&keyword=" + code, "eastmoney_news", "https://www.eastmoney.com/"),
        ]
    
    for url, src, ref in sources:
        try:
            import urllib.request
            if "{limit}" in url:
                url = url.format(limit=limit)
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': ref,
                'Accept': 'application/json, text/html'
            })
            with urllib.request.urlopen(req, timeout=10) as r:
                raw = r.read().decode('utf-8', errors='ignore')
                
                # 解析JSON或类JSON
                try:
                    if src == "eastmoney_hk":
                        # 东方财富港股返回格式:callback([...])
                        raw = raw.strip()
                        if raw.startswith('jQuery') or raw.startswith('callback'):
                            start = raw.find('[')
                            end = raw.rfind(']') + 1
                            if start >= 0 and end > start:
                                raw = raw[start:end]
                        data = json.loads(raw)
                        if isinstance(data, list):
                            for item in data[:limit]:
                                title = item.get("title", item.get("t", "")).strip()
                                if title and title not in seen_titles:
                                    seen_titles.add(title)
                                    news_results.append({
                                        "title": title,
                                        "date": item.get("datetime", item.get("time", "")),
                                        "source": item.get("src", "东方财富港股"),
                                        "importance": _calc_news_importance(title),
                                        "url": item.get("url", ref)
                                    })
                    elif src == "sina_hk":
                        # 新浪港股返回HTML，提取新闻标题
                        import re
                        titles = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', raw)
                        for url_path, title_text in titles[:limit]:
                            title = title_text.strip()
                            if title and len(title) > 5 and title not in seen_titles:
                                seen_titles.add(title)
                                news_results.append({
                                    "title": title,
                                    "date": "",
                                    "source": "新浪财经港股",
                                    "importance": _calc_news_importance(title),
                                    "url": url_path if url_path.startswith('http') else f"https://finance.sina.com.cn{url_path}"
                                })
                    elif src == "eastmoney" and isinstance(json.loads(raw) if raw.startswith('{') else {}, dict):
                        json_data = json.loads(raw)
                        if json_data.get("data"):
                            for item in json_data["data"].get("list", [])[:limit]:
                                title = item.get("title", "").strip()
                                if title and title not in seen_titles:
                                    seen_titles.add(title)
                                    news_results.append({
                                        "title": title,
                                        "date": item.get("notice_date", ""),
                                        "source": item.get("src", "东方财富"),
                                        "importance": _calc_news_importance(title),
                                        "url": f"https://www.eastmoney.com/"
                                    })
                    elif src == "eastmoney_news":
                        json_data = json.loads(raw)
                        if isinstance(json_data, dict) and json_data.get("data"):
                            items = json_data["data"].get("news", json_data["data"].get("list", []))
                            for item in items[:limit]:
                                title = item.get("title", item.get("s", "")).strip()
                                if title and title not in seen_titles:
                                    seen_titles.add(title)
                                    news_results.append({
                                        "title": title,
                                        "date": item.get("datetime", item.get("time", "")),
                                        "source": item.get("src", "东方财富资讯"),
                                        "importance": _calc_news_importance(title),
                                        "url": item.get("url", "https://www.eastmoney.com/")
                                    })
                except json.JSONDecodeError:
                    # HTML页面，降级处理
                    if src == "sina_hk":
                        import re
                        titles = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', raw)
                        for url_path, title_text in titles[:limit]:
                            title = title_text.strip()
                            if title and len(title) > 5 and title not in seen_titles:
                                seen_titles.add(title)
                                news_results.append({
                                    "title": title,
                                    "date": "",
                                    "source": "新浪财经港股",
                                    "importance": _calc_news_importance(title),
                                    "url": url_path if url_path.startswith('http') else f"https://finance.sina.com.cn{url_path}"
                                })
                    pass
        except Exception as e:
            pass
    
    return news_results[:limit]

def _calc_news_importance(title: str) -> int:
    """计算新闻重要程度 1-5"""
    important_keywords = [
        (5, ["重组", "收购", "并购", "定增", "发行", "上市", "退市", "暂停上市"]),
        (4, ["业绩", "盈利", "亏损", "增长", "下降", "超预期", "不及预期", "下调", "上调"]),
        (3, ["增持", "减持", "回购", "分红", "送转", "摘帽", "ST"]),
        (2, ["合作", "签约", "中标", "订单", "投资", "扩建", "投产"]),
        (1, ["调研", "会议", "公告", "说明"]),
    ]
    for score, keywords in important_keywords:
        for kw in keywords:
            if kw in title:
                return score
    return 1

# 情感分析词典
POSITIVE_WORDS = [
    # 核心利好
    "增持", "买入", "推荐", "看好", "超预期", "突破", "上涨", "利好",
    "业绩增长", "盈利", "增长", "创新高", "景气", "复苏", "布局",
    "机会", "低估", "价值", "成长", "景气上行", "订单", "签约", "合作",
    "中标", "景气提升", "需求旺盛", "产能扩张", "市场份额",
    # 财务表现
    "净利润增长", "营收增长", "毛利率提升", "扭亏为盈", "大幅增长",
    "业绩翻倍", "净利润翻番", "营收创纪录", "利润创历史",
    # 业务发展
    "新签订单", "中标大单", "市场份额扩大", "行业领先地位",
    "技术突破", "研发成功", "产品发布", "上市申请获批",
    "产能扩张完成", "新产能投产", "满产", "扩产",
    # 资本运作
    "回购", "增持计划", "员工持股", "股权激励",
    "高分红", "派息增加", "送转股份", "定向增发获批",
    "战略投资", "引入战投", "混改", "分拆上市",
    # 政策利好
    "政策支持", "补贴", "税收优惠", "产业政策利好",
    # 评级上调
    "评级上调", "买入评级", "强烈推荐", "目标价上调",
    "上调盈利预测", "业绩指引上调",
]

NEGATIVE_WORDS = [
    # 核心利空
    "减持", "卖出", "看空", "下调", "不及预期", "下跌", "利空", "亏损",
    "业绩下降", "风险", "警示", "调查", "处罚", "诉讼", "债务", "违约",
    "商誉", "减值", "库存", "积压", "竞争加剧", "价格战", "需求疲软",
    "终止", "失败", "违规", "造假", "退市", "ST", "*ST",
    # 财务风险
    "净利润下降", "营收下滑", "亏损扩大", "大幅下跌",
    "业绩变脸", "盈利预警", "商誉暴雷", "资产减值",
    "债务逾期", "流动性紧张", "资金链断裂", "无法偿还债务",
    # 监管调查
    "立案调查", "监管函", "行政处罚", "市场禁入",
    "涉嫌信息披露违规", "涉嫌操纵股价", "内幕交易",
    "财务造假", "虚假陈述", "欺诈发行",
    # 业务风险
    "订单减少", "合同终止", "合作破裂", "被索赔",
    "产品召回", "安全事故", "环保问题", "停产整顿",
    "产能过剩", "库存积压", "销售下滑", "竞争失势",
    # 资本运作负面
    "回购取消", "增持终止", "减持计划", "定增失败",
    "收购终止", "重组失败", "分拆终止",
    # 政策风险
    "政策收紧", "监管趋严", "行业整顿", "整改",
    # 评级下调
    "评级下调", "卖出评级", "目标价下调", "下调盈利预测",
    "下调评级", "审慎推荐", "减持评级",
]

def analyze_sentiment(news_list: List[Dict]) -> Dict:
    """分析资讯情感倾向（带重要程度权重）"""
    if not news_list:
        return {
            "sentiment": "无资讯",
            "positive_count": 0,
            "negative_count": 0,
            "news_titles": [],
            "weighted_score": 0,
            "impact_level": "无"
        }
    
    positive_score = 0
    negative_score = 0
    news_summary = []
    impact_details = []
    
    for news in news_list:
        title = news.get("title", "")
        importance = news.get("importance", 1)  # 1-5级
        combined = title
        
        pos_found = []
        neg_found = []
        
        for word in POSITIVE_WORDS:
            if word in combined:
                pos_found.append(word)
        
        for word in NEGATIVE_WORDS:
            if word in combined:
                neg_found.append(word)
        
        # 带权重计分
        if len(pos_found) > len(neg_found):
            positive_score += importance * len(pos_found)
        elif len(neg_found) > len(pos_found):
            negative_score += importance * len(neg_found)
        
        if pos_found or neg_found:
            sentiment_icon = "🟢" if len(pos_found) > len(neg_found) else "🔴"
            impact_icon = "🔴" * importance if len(neg_found) > len(pos_found) else "🟢" * importance
            short_title = title[:35] + "..." if len(title) > 35 else title
            news_summary.append(f"{sentiment_icon}{impact_icon} {short_title}")
            impact_details.append({
                "title": short_title,
                "impact": importance,
                "sentiment": "positive" if len(pos_found) > len(neg_found) else "negative"
            })
    
    total = positive_score + negative_score
    # 计算加权情感比
    if total > 0:
        ratio = positive_score / total
        if ratio >= 0.7:
            sentiment = "偏多 🟢"
        elif ratio <= 0.3:
            sentiment = "偏空 🔴"
        else:
            sentiment = "中性 📊"
    else:
        sentiment = "中性 📊"
    
    # 影响级别：高权重利空/利好数量
    high_impact_neg = sum(1 for d in impact_details if d["impact"] >= 4 and d["sentiment"] == "negative")
    high_impact_pos = sum(1 for d in impact_details if d["impact"] >= 4 and d["sentiment"] == "positive")
    
    if high_impact_neg >= 2:
        impact_level = "⚠️ 高度警惕"
    elif high_impact_pos >= 2:
        impact_level = "✨ 高度关注"
    elif positive_score > negative_score * 2:
        impact_level = "📈 偏多"
    elif negative_score > positive_score * 2:
        impact_level = "📉 偏空"
    else:
        impact_level = "➡️ 中性"
    
    return {
        "sentiment": sentiment,
        "positive_count": positive_score,
        "negative_count": negative_score,
        "news_titles": news_summary[:6],
        "weighted_score": positive_score - negative_score,
        "impact_level": impact_level,
        "high_impact_count": high_impact_neg + high_impact_pos
    }

# ============ K线数据获取 ============

def get_kline_eastmoney(code: str, days: int = 60) -> List[Dict]:
    """使用东方财富获取K线数据（仅支持A股）"""
    import urllib.request
    
    try:
        if code.startswith("6"):
            secid = f"1.{code}"
        else:
            secid = f"0.{code}"
        
        end_date = datetime.now().strftime("%Y%m%d")
        url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&beg=20250101&end={end_date}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.add_header('Referer', 'https://www.eastmoney.com/')
        
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
            data = json.loads(content)
            
            if 'data' not in data or not data.get('data'):
                return None
            
            klines = data['data']['klines']
            result = []
            
            for kline in klines[-days:]:
                parts = kline.split(',')
                if len(parts) >= 6:
                    result.append({
                        "date": parts[0],
                        "open": float(parts[1]),
                        "close": float(parts[2]),
                        "high": float(parts[3]),
                        "low": float(parts[4]),
                        "volume": int(parts[5])
                    })
            
            return result if result else None
            
    except Exception as e:
        print(f"东方财富K线获取失败: {code}, {e}")
        return None

def get_kline_tencent_hk(code: str, days: int = 60) -> List[Dict]:
    """使用腾讯API获取港股K线数据"""
    import urllib.request
    
    try:
        # 港股代码：如果已带hk前缀则直接使用，否则补齐
        if code.startswith("hk"):
            full_code = code
        else:
            full_code = f"hk{code.zfill(5)}"
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={full_code},day,,,{days},qfq"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
            data = json.loads(content)
            
            # 腾讯返回格式: data -> hkXXXXX -> day
            if 'data' not in data:
                return None
            
            stock_data = data['data']
            if full_code not in stock_data:
                return None
            
            # K线数据直接在 day 字段
            kline_data = stock_data[full_code].get('day')
            if not kline_data:
                return None
            
            result = []
            for kline in kline_data[-days:]:
                if len(kline) >= 6:
                    result.append({
                        "date": kline[0],
                        "open": float(kline[1]),
                        "close": float(kline[2]),
                        "high": float(kline[3]),
                        "low": float(kline[4]),
                        "volume": int(float(kline[5])) if kline[5] else 0
                    })
            
            return result if result else None
            
    except Exception as e:
        print(f"腾讯港股K线获取失败: {code}, {e}")
        return None

def get_kline_sina(code: str, days: int = 60) -> List[Dict]:
    """使用新浪财经获取K线数据"""
    import requests
    
    try:
        if code.startswith("6"):
            symbol = f"sh{code}"
        elif code.startswith(("0", "3")):
            symbol = f"sz{code}"
        else:
            symbol = code
        
        url = f"https://quotes.sina.cn/cn/api/jsonp.php/var%20_{symbol}=/CN_MarketDataService.getKLineData?symbol={symbol}&scale=240&ma=no&datalen=1024"
        
        resp = requests.get(url, timeout=10)
        resp.encoding = 'utf-8'
        
        text = resp.text
        start = text.find('[')
        end = text.rfind(']') + 1
        
        if start < 0 or end <= 0:
            return get_kline_simulated(code, days)
        
        json_str = text[start:end]
        data = json.loads(json_str)
        
        klines = []
        for item in data[-days:]:
            klines.append({
                "date": item.get("day", ""),
                "open": float(item.get("open", 0)),
                "close": float(item.get("close", 0)),
                "high": float(item.get("high", 0)),
                "low": float(item.get("low", 0)),
                "volume": int(item.get("volume", 0))
            })
        
        return klines
        
    except Exception as e:
        print(f"新浪K线获取失败: {code}, {e}")
        return get_kline_simulated(code, days)

def get_kline_simulated(code: str, days: int = 60) -> List[Dict]:
    """模拟K线数据 (当无法获取真实数据时)"""
    import random
    quotes = []
    base_price = 50.0
    
    for i in range(days):
        date = (datetime.now().date()).strftime("%Y-%m-%d")
        open_p = base_price + random.uniform(-2, 2)
        close_p = open_p + random.uniform(-1.5, 1.5)
        high_p = max(open_p, close_p) + random.uniform(0, 1)
        low_p = min(open_p, close_p) - random.uniform(0, 1)
        volume = random.randint(1000000, 10000000)
        
        quotes.append({
            "date": date,
            "open": round(open_p, 2),
            "close": round(close_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "volume": volume
        })
        base_price = close_p
    
    return quotes

def get_stock_quote(code: str) -> Optional[Dict]:
    """获取股票实时行情 - 腾讯API"""
    import urllib.request
    import re
    
    try:
        # 判断股票市场
        if code.startswith("6") and len(code) == 6:
            full_code = f"sh{code}"
        elif code.startswith(("0", "3")) and len(code) == 6:
            full_code = f"sz{code}"
        elif code.startswith("8") and len(code) == 6:
            full_code = f"sh{code}"
        elif code.startswith(("sh", "sz")):
            full_code = code
        elif code.startswith("hk"):
            # 港股已带前缀，直接使用
            full_code = code
        else:
            # 港股：补齐5位（处理纯数字如 00981）
            full_code = f"hk{code.zfill(5)}"
        
        url = f"https://qt.gtimg.cn/q={full_code}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('gbk', errors='ignore')
            
            if 'none_match' in content or not content:
                return None
            
            match = re.search(r'="([^"]+)"', content)
            if not match:
                return None
            
            parts = match.group(1).split('~')
            
            if len(parts) < 33:
                return None
            
            # 腾讯字段: parts[3]=当前价, parts[31]=涨跌, parts[32]=涨跌幅
            price = float(parts[3]) if parts[3] and parts[3] != '-' else 0
            change = float(parts[31]) if parts[31] and parts[31] != '-' else 0
            pct = float(parts[32]) if parts[32] and parts[32] != '-' else 0
            
            # 安全转换volume
            try:
                volume = int(float(parts[6])) if parts[6] and parts[6] != '-' else 0
            except:
                volume = 0
            
            try:
                amount = float(parts[7]) if parts[7] and parts[7] != '-' else 0
            except:
                amount = 0
            
            return {
                "code": code,
                "name": parts[1] if parts[1] else code,
                "price": price,
                "change": change,
                "change_pct": pct,
                "volume": volume,
                "amount": amount,
                "open": price - change if price > 0 else 0,
                "high": float(parts[11]) if len(parts) > 11 and parts[11] and parts[11] != '-' else 0,
                "low": float(parts[12]) if len(parts) > 12 and parts[12] and parts[12] != '-' else 0,
            }
            
    except Exception as e:
        print(f"获取行情失败: {code}, {e}")
        return None

def get_market_index() -> List[Dict]:
    """获取大盘指数实时行情 - 腾讯API"""
    import urllib.request
    import re

    indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000300', '沪深300'),
        ('sh000016', '上证50'),
        ('sz399905', '中证500'),
        # 港股指数
        ('hkHSI', '恒生指数'),
        ('hkHSTECH', '恒生科技'),
        ('hkHSCEI', '恒生国企'),
    ]

    results = []
    for code, name in indices:
        try:
            url = f'https://qt.gtimg.cn/q={code}'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read().decode('gbk', errors='ignore')
                match = re.search(r'="([^"]+)"', content)
                if not match:
                    continue
                parts = match.group(1).split('~')
                if len(parts) < 33:
                    continue
                price = float(parts[3]) if parts[3] and parts[3] != '-' else 0
                change = float(parts[31]) if parts[31] and parts[31] != '-' else 0
                pct = float(parts[32]) if parts[32] and parts[32] != '-' else 0
                results.append({
                    'name': name,
                    'code': code,
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'pct': round(pct, 2)
                })
        except Exception as e:
            print(f"获取指数失败: {code}, {e}")
    return results

# ============ 技术指标计算函数 ============

def calculate_ma(prices: List[float], period: int) -> float:
    """计算移动平均线"""
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    return sum(prices[-period:]) / period

def calculate_ema(prices: List[float], period: int) -> float:
    """计算指数移动平均线"""
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    
    ema = prices[0]
    multiplier = 2 / (period + 1)
    
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_macd(prices: List[float]) -> Dict:
    """计算MACD指标"""
    if len(prices) < 26:
        return {"dif": 0, "dea": 0, "macd": 0, "signal": "数据不足"}
    
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    
    dif = ema12 - ema26
    dea = dif * 0.9
    macd = (dif - dea) * 2
    
    if dif > dea:
        signal = "金叉 ✓ 买入"
    else:
        signal = "死叉 ✗ 卖出"
    
    return {"dif": round(dif, 4), "dea": round(dea, 4), "macd": round(macd, 4), "signal": signal}

def calculate_kdj(prices: List[float], high: List[float], low: List[float], period: int = 9) -> Dict:
    """计算KDJ指标"""
    if len(prices) < period + 1:
        return {"k": 50, "d": 50, "j": 50, "signal": "数据不足"}
    
    rsv = []
    for i in range(period, len(prices)):
        window_high = max(high[i-period:i])
        window_low = min(low[i-period:i])
        
        if window_high == window_low:
            rsv.append(50)
        else:
            rsv.append((prices[i-1] - window_low) / (window_high - window_low) * 100)
    
    if not rsv:
        return {"k": 50, "d": 50, "j": 50, "signal": "数据不足"}
    
    k = sum(rsv[-period:]) / period
    d = k * 0.9 + 50 * 0.1
    j = 3 * k - 2 * d
    
    if k > 80:
        signal = "超买 ⚠️"
    elif k < 20:
        signal = "超卖 ✓"
    elif k > d:
        signal = "金叉 ✓"
    else:
        signal = "死叉 ✗"
    
    return {"k": round(k, 2), "d": round(d, 2), "j": round(j, 2), "signal": signal}

def calculate_rsi(prices: List[float], period: int = 14) -> Dict:
    """计算RSI指标"""
    if len(prices) < period + 1:
        return {"rsi6": 50, "rsi12": 50, "rsi24": 50, "signal": "数据不足"}
    
    def rsi_single(p, per):
        if len(p) < per + 1:
            return 50
        gains = []
        losses = []
        for i in range(1, len(p)):
            change = p[i] - p[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-per:]) / per
        avg_loss = sum(losses[-per:]) / per
        
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    rsi6 = rsi_single(prices, 6)
    rsi12 = rsi_single(prices, 12)
    rsi24 = rsi_single(prices, 24)
    
    if rsi6 > 70:
        signal = "超买 ⚠️"
    elif rsi6 < 30:
        signal = "超卖 ✓"
    else:
        signal = "正常"
    
    return {"rsi6": round(rsi6, 2), "rsi12": round(rsi12, 2), "rsi24": round(rsi24, 2), "signal": signal}

def calculate_boll(prices: List[float], period: int = 20) -> Dict:
    """计算布林带指标"""
    if len(prices) < period:
        return {"upper": 0, "middle": 0, "lower": 0, "signal": "数据不足"}
    
    recent = prices[-period:]
    middle = sum(recent) / period
    
    variance = sum((x - middle) ** 2 for x in recent) / period
    std = variance ** 0.5
    
    upper = middle + 2 * std
    lower = middle - 2 * std
    
    current_price = prices[-1]
    
    if current_price > upper:
        signal = "突破上轨 ⚠️"
    elif current_price < lower:
        signal = "突破下轨 ✓"
    elif current_price > middle:
        signal = "中轨上方"
    else:
        signal = "中轨下方"
    
    return {"upper": round(upper, 2), "middle": round(middle, 2), "lower": round(lower, 2), "signal": signal}

def calculate_obv(closes: List[float], volumes: List[int]) -> Dict:
    """计算OBV (能量潮指标)"""
    if len(closes) < 2 or len(volumes) < 2:
        return {"obv": 0, "signal": "数据不足"}
    
    obv = 0
    obv_history = []
    
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]:
            obv += volumes[i]
        elif closes[i] < closes[i-1]:
            obv -= volumes[i]
        obv_history.append(obv)
    
    if len(obv_history) < 10:
        return {"obv": obv, "signal": "数据不足"}
    
    # OBV均线
    obv_ma = sum(obv_history[-10:]) / 10
    
    current_obv = obv_history[-1]
    
    if current_obv > obv_ma:
        signal = "OBV上行 ✓"
    else:
        signal = "OBV下行 ✗"
    
    # 检查OBV背离
    price_trend = closes[-1] - closes[-10]
    obv_trend = obv_history[-1] - obv_history[-10]
    
    if price_trend > 0 and obv_trend < 0:
        signal = "顶背离 ⚠️ 卖出"
    elif price_trend < 0 and obv_trend > 0:
        signal = "底背离 ✓ 买入"
    
    return {"obv": round(obv, 2), "obv_ma10": round(obv_ma, 2), "signal": signal}

def calculate_dmi(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict:
    """计算DMI (动向指标) / ADX"""
    if len(closes) < period + 1:
        return {"plus_di": 0, "minus_di": 0, "adx": 0, "signal": "数据不足"}
    
    # 计算真实波幅TR
    tr_list = []
    plus_dm_list = []
    minus_dm_list = []
    
    for i in range(1, len(closes)):
        high = highs[i]
        low = lows[i]
        prev_close = closes[i-1]
        
        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        tr_list.append(tr)
        
        plus_dm = max(high - highs[i-1], 0) if i > 0 else 0
        minus_dm = max(lows[i-1] - low, 0) if i > 0 else 0
        
        # 避免DM为负
        plus_dm = max(plus_dm - minus_dm, 0) if i > 0 else 0
        minus_dm = max(minus_dm - plus_dm, 0) if i > 0 else 0
        
        plus_dm_list.append(plus_dm)
        minus_dm_list.append(minus_dm)
    
    if len(tr_list) < period:
        return {"plus_di": 0, "minus_di": 0, "adx": 0, "signal": "数据不足"}
    
    # 计算平滑值
    smooth_tr = sum(tr_list[:period])
    smooth_plus_dm = sum(plus_dm_list[:period])
    smooth_minus_dm = sum(minus_dm_list[:period])
    
    for i in range(period, len(tr_list)):
        smooth_tr = smooth_tr - smooth_tr / period + tr_list[i]
        smooth_plus_dm = smooth_plus_dm - smooth_plus_dm / period + plus_dm_list[i]
        smooth_minus_dm = smooth_minus_dm - smooth_minus_dm / period + minus_dm_list[i]
    
    # 计算DI
    plus_di = (smooth_plus_dm / smooth_tr * 100) if smooth_tr > 0 else 0
    minus_di = (smooth_minus_dm / smooth_tr * 100) if smooth_tr > 0 else 0
    
    # 计算ADX
    dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
    
    adx_list = [dx]
    for i in range(period, min(len(tr_list), 50)):
        adx_val = sum(adx_list[-period:]) / period
        adx_list.append(adx_val)
    
    adx = adx_list[-1] if adx_list else 0
    
    # 信号判断
    if plus_di > minus_di and adx > 25:
        signal = "多头趋势 ✓"
    elif minus_di > plus_di and adx > 25:
        signal = "空头趋势 ✗"
    elif adx < 20:
        signal = "震荡整理"
    else:
        signal = "趋势不明"
    
    return {
        "plus_di": round(plus_di, 2),
        "minus_di": round(minus_di, 2),
        "adx": round(adx, 2),
        "signal": signal
    }

def calculate_wr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict:
    """计算威廉指标 (Williams %R)"""
    if len(closes) < period:
        return {"wr": 50, "signal": "数据不足"}
    
    highest = max(highs[-period:])
    lowest = min(lows[-period:])
    current = closes[-1]
    
    if highest == lowest:
        wr = 50
    else:
        wr = (highest - current) / (highest - lowest) * 100
    
    if wr < 20:
        signal = "超买 ⚠️"
    elif wr > 80:
        signal = "超卖 ✓"
    else:
        signal = "正常"
    
    return {"wr": round(wr, 2), "signal": signal}

def analyze_stock(code: str) -> Dict:
    """分析股票并返回技术指标"""
    quote = get_stock_quote(code)
    if not quote:
        return {"error": f"无法获取 {code} 的行情"}
    
    # 校验代码/名称映射是否一致
    validation_warning = validate_stock_mapping(code, quote)
    if validation_warning:
        print(validation_warning)
    
    # 判断是否为港股（使用更新后的函数）
    is_hk = is_hk_stock(code)
    
    # 尝试获取真实K线数据
    if is_hk:
        # 港股使用腾讯API
        klines = get_kline_tencent_hk(code, 60)
    else:
        # A股使用东方财富优先，新浪备用
        klines = get_kline_eastmoney(code, 60)
        if not klines or len(klines) < 10:
            klines = get_kline_sina(code, 60)
    
    if not klines or len(klines) < 10:
        return {"error": f"无法获取 {code} 的K线数据"}
    
    # 获取资讯并分析情感
    sentiment = {"sentiment": "暂无", "positive_count": 0, "negative_count": 0, "news_titles": []}
    news = get_stock_news(code, 10)
    sentiment = analyze_sentiment(news)
    
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    volumes = [k['volume'] for k in klines]
    latest_kline = klines[-1]
    
    # 基础均线
    ma5 = calculate_ma(closes, 5)
    ma10 = calculate_ma(closes, 10)
    ma20 = calculate_ma(closes, 20)
    ma60 = calculate_ma(closes, 60) if len(closes) >= 60 else None
    
    # 技术指标
    macd = calculate_macd(closes)
    kdj = calculate_kdj(closes, highs, lows)
    rsi = calculate_rsi(closes)
    boll = calculate_boll(closes)
    obv = calculate_obv(closes, volumes)
    dmi = calculate_dmi(highs, lows, closes)
    wr = calculate_wr(highs, lows, closes)
    
    # 生成信号
    signals = []
    buy_score = 0
    sell_score = 0
    
    # MA信号
    if ma5 > ma10:
        signals.append(f"MA5({ma5:.2})>MA10({ma10:.2}) 金叉 ✓")
        buy_score += 1
    else:
        signals.append(f"MA5({ma5:.2})<MA10({ma10:.2}) 死叉 ✗")
        sell_score += 1
    
    if ma10 > ma20:
        signals.append("短期均线多头排列 ✓")
        buy_score += 1
    else:
        signals.append("短期均线空头排列 ✗")
        sell_score += 1
    
    # MACD信号
    if "金叉" in macd["signal"]:
        buy_score += 2
    else:
        sell_score += 2
    signals.append(f"MACD: {macd['signal']}")
    
    # KDJ信号
    if "超卖" in kdj["signal"] or "金叉" in kdj["signal"]:
        buy_score += 1
    elif "超买" in kdj["signal"] or "死叉" in kdj["signal"]:
        sell_score += 1
    signals.append(f"KDJ: {kdj['signal']}")
    
    # RSI信号
    signals.append(f"RSI: {rsi['signal']}")
    if rsi["rsi6"] < 30:
        buy_score += 1
    elif rsi["rsi6"] > 70:
        sell_score += 1
    
    # BOLL信号
    signals.append(f"BOLL: {boll['signal']}")
    
    # OBV信号
    signals.append(f"OBV: {obv['signal']}")
    if "底背离" in obv["signal"]:
        buy_score += 2
    elif "顶背离" in obv["signal"]:
        sell_score += 2
    
    # DMI信号
    signals.append(f"DMI: {dmi['signal']}")
    if "多头" in dmi["signal"]:
        buy_score += 2
    elif "空头" in dmi["signal"]:
        sell_score += 2
    
    # WR信号
    signals.append(f"WR: {wr['signal']}")
    if wr["signal"] == "超卖 ✓":
        buy_score += 1
    elif wr["signal"] == "超买 ⚠️":
        sell_score += 1
    
    # 资讯情感信号 (消息面权重)
    impact = sentiment.get("impact_level", "中性")
    signals.append(f"📰 资讯情感: {sentiment['sentiment']} | 影响:{impact} | 积极{sentiment['positive_count']}分/消极{sentiment['negative_count']}分")
    if sentiment["positive_count"] > sentiment["negative_count"] + 2:
        buy_score += 3
    elif sentiment["negative_count"] > sentiment["positive_count"] + 2:
        sell_score += 3
    elif sentiment["positive_count"] > sentiment["negative_count"]:
        buy_score += 1
    elif sentiment["negative_count"] > sentiment["positive_count"]:
        sell_score += 1
    
    # 综合判断
    if buy_score > sell_score + 3:
        overall = "强烈买入 ✓✓"
    elif buy_score > sell_score:
        overall = "建议买入 ✓"
    elif sell_score > buy_score + 3:
        overall = "强烈卖出 ✗✗"
    elif sell_score > buy_score:
        overall = "建议卖出 ✗"
    else:
        overall = "观望"
    
    return {
        "code": code,
        "name": quote["name"],
        "price": quote["price"],
        "change": quote["change"],
        "change_pct": quote["change_pct"],
        "kline_date": latest_kline["date"],
        "indicators": {
            "ma": {
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "ma60": round(ma60, 2) if ma60 else None
            },
            "macd": macd,
            "kdj": kdj,
            "rsi": rsi,
            "boll": boll,
            "obv": obv,
            "dmi": dmi,
            "wr": wr
        },
        "signals": signals,
        "overall": overall,
        "score": {"buy": buy_score, "sell": sell_score},
        "sentiment": sentiment,
        "klines": klines
    }

# ============ 持仓管理（智能成本计算） ============

def load_positions() -> Dict:
    """加载持仓"""
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("positions", {})
    return {}

def save_positions(positions: Dict):
    """保存持仓"""
    with open(POSITIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump({"positions": positions, "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

def recalculate_position_from_trades(code: str) -> Optional[Dict]:
    """
    根据交易记录重新计算持仓成本（纯FIFO批次计算法）
    - 维护买入批次队列，按时间顺序处理
    - 卖出时从最早买入批次开始扣除
    - 持仓成本 = 剩余批次总成本 / 剩余股数
    返回：{quantity, cost_price} 或 None（无持仓）
    """
    trades = load_trades()
    code_trades = [t for t in trades if str(t.get("code")) == str(code)]
    # 按时间顺序排序
    code_trades.sort(key=lambda x: x.get("date", ""))

    # 买入批次队列：[{qty, price, date}]
    buy_lots = []

    for t in code_trades:
        qty = float(t.get("quantity", 0))
        price = float(t.get("price", 0))
        action = t.get("action", "")

        if action in ("买入", "buy", "Buy", "BUY"):
            # 入队列
            buy_lots.append({"qty": qty, "price": price, "date": t.get("date", "")})
        elif action in ("卖出", "sell", "Sell", "SELL"):
            # FIFO：出队列
            remaining_to_sell = qty
            while remaining_to_sell > 0 and buy_lots:
                lot = buy_lots[0]
                if lot["qty"] <= remaining_to_sell:
                    # 批次全部卖出
                    remaining_to_sell -= lot["qty"]
                    buy_lots.pop(0)
                else:
                    # 批次部分卖出
                    lot["qty"] -= remaining_to_sell
                    remaining_to_sell = 0

    # 计算剩余持仓
    total_qty = sum(lot["qty"] for lot in buy_lots)
    total_cost = sum(lot["qty"] * lot["price"] for lot in buy_lots)

    if total_qty <= 0:
        return None

    avg_cost = total_cost / total_qty if total_qty > 0 else 0
    return {
        "quantity": total_qty,
        "cost_price": round(avg_cost, 4),
        "updated": datetime.now().isoformat()
    }

def sync_position_from_trades(code: str):
    """
    根据交易记录重新计算并同步持仓到文件
    """
    position = recalculate_position_from_trades(code)
    positions = load_positions()
    if position:
        positions[code] = position
    elif code in positions:
        del positions[code]
    save_positions(positions)
    return position

def add_position(code: str, quantity: float, cost_price: float):
    """
    添加或覆盖持仓（手动指定时使用）
    注意：智能方式推荐用 record_trade_and_sync()
    """
    positions = load_positions()
    positions[code] = {
        "quantity": quantity,
        "cost_price": cost_price,
        "updated": datetime.now().isoformat()
    }
    save_positions(positions)

def record_trade_and_sync(code: str, action: str, quantity: float, price: float, note: str = ""):
    """
    记录交易并智能同步持仓（核心智能函数）
    - 买入：自动计算新的加权平均持仓成本
    - 卖出：自动减少持仓数量，成本不变
    """
    # 1. 记录交易
    trades = load_trades()
    trades.append({
        "code": code,
        "action": action,
        "quantity": quantity,
        "price": price,
        "note": note,
        "date": datetime.now().isoformat()
    })
    save_trades(trades)
    # 2. 重新计算并同步持仓
    sync_position_from_trades(code)

def remove_position(code: str):
    """清除持仓"""
    positions = load_positions()
    if code in positions:
        del positions[code]
        save_positions(positions)

def get_position(code: str) -> Optional[Dict]:
    """获取单只股票持仓"""
    positions = load_positions()
    return positions.get(code)

def get_all_positions() -> Dict:
    """获取所有持仓（自动从交易记录同步后返回）"""
    return load_positions()

# ============ 交易记录 ============

def load_trades() -> List[Dict]:
    """加载交易记录"""
    if os.path.exists(TRADES_FILE):
        with open(TRADES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("trades", [])
    return []

def save_trades(trades: List[Dict]):
    """保存交易记录"""
    with open(TRADES_FILE, 'w', encoding='utf-8') as f:
        json.dump({"trades": trades, "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

def add_trade(code: str, action: str, quantity: float, price: float, note: str = ""):
    """添加交易记录"""
    trades = load_trades()
    trades.append({
        "code": code,
        "action": action,  # "买入" 或 "卖出"
        "quantity": quantity,
        "price": price,
        "note": note,
        "date": datetime.now().isoformat()
    })
    save_trades(trades)

def get_trades(code: str = None) -> List[Dict]:
    """获取交易记录"""
    trades = load_trades()
    if code:
        return [t for t in trades if t.get("code") == code]
    return trades

# ============ 持仓分析 ============

def analyze_position(code: str) -> Dict:
    """分析持仓情况"""
    quote = get_stock_quote(code)
    if not quote:
        return {"error": f"无法获取 {code} 的行情"}
    
    position = get_position(code)
    if not position:
        return {"error": f"未找到 {code} 的持仓记录"}
    
    current_price = quote["price"]
    quantity = position["quantity"]
    cost_price = position["cost_price"]
    
    # 计算盈亏
    profit = (current_price - cost_price) * quantity
    profit_pct = (current_price - cost_price) / cost_price * 100 if cost_price > 0 else 0
    market_value = current_price * quantity
    cost_value = cost_price * quantity
    
    # 获取技术分析
    tech = analyze_stock(code)
    
    # 生成操作建议
    suggestions = []
    
    # 基于技术面和持仓情况给出建议
    if "error" not in tech:
        score = tech.get("score", {})
        buy_score = score.get("buy", 0)
        sell_score = score.get("sell", 0)
        
        # 盈利且技术面偏空 -> 考虑止盈
        if profit > 0 and sell_score > buy_score + 2:
            suggestions.append("⚠️ 技术面偏弱，盈利可观，建议部分止盈")
        elif profit > 0 and sell_score > buy_score:
            suggestions.append("建议关注，可考虑分批卖出")
        
        # 亏损且技术面偏多 -> 考虑加仓
        elif profit < 0 and buy_score > sell_score + 2:
            suggestions.append("📈 技术面转好，可考虑加仓摊低成本")
        elif profit < 0 and buy_score > sell_score:
            suggestions.append("建议持有，等待反弹")
        
        # 强势买入信号
        elif buy_score > sell_score + 3:
            suggestions.append("🚀 技术面强烈看涨，可继续持有或加仓")
        
        # 强势卖出信号
        elif sell_score > buy_score + 3:
            suggestions.append("🔴 技术面强烈看跌，建议止损或减仓")
        
        # 震荡整理
        else:
            suggestions.append("📊 震荡整理中，建议观望")
    
    # 计算盈亏平衡点
    return {
        "code": code,
        "name": quote["name"],
        "current_price": current_price,
        "position": {
            "quantity": quantity,
            "cost_price": cost_price,
            "cost_value": round(cost_value, 2),
            "market_value": round(market_value, 2),
            "profit": round(profit, 2),
            "profit_pct": round(profit_pct, 2)
        },
        "suggestions": suggestions,
        "tech_summary": tech.get("overall", "分析中") if "error" not in tech else "分析失败"
    }

def format_position_report(results: List[Dict]) -> str:
    """格式化持仓报告"""
    if not results:
        return "没有持仓记录"
    
    lines = ["💰 持仓分析报告", "=" * 50, ""]
    
    total_profit = 0
    total_value = 0
    
    for r in results:
        if "error" in r:
            continue
            
        pos = r["position"]
        profit_emoji = "🟢" if pos["profit"] >= 0 else "🔴"
        
        lines.append(f"{profit_emoji} {r['name']} ({r['code']})")
        lines.append(f"   持仓: {pos['quantity']}股 @ 成本{pos['cost_price']:.2f}")
        lines.append(f"   当前: {r['current_price']:.2f}")
        lines.append(f"   市值: {pos['market_value']:.2f} | 盈亏: {pos['profit']:+.2f} ({pos['profit_pct']:+.2f}%)")
        
        if r["suggestions"]:
            lines.append(f"   💡 {r['suggestions'][0]}")
        
        lines.append(f"   📈 技术面: {r['tech_summary']}")
        lines.append("")
        
        total_profit += pos["profit"]
        total_value += pos["market_value"]
    
    if total_value > 0:
        lines.append("=" * 50)
        lines.append(f"📊 总市值: {total_value:.2f} | 总盈亏: {total_profit:+.2f}")
    
    return "\n".join(lines)

# ============ 股票池管理 ============

def load_stock_pool() -> List[str]:
    """加载股票池"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("stocks", [])
    return []

def save_stock_pool(stocks: List[str]):
    """保存股票池"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({"stocks": stocks, "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

def add_to_pool(code: str):
    """添加股票到监控池"""
    stocks = load_stock_pool()
    if code not in stocks:
        stocks.append(code)
        save_stock_pool(stocks)
        return True
    return False

def remove_from_pool(code: str):
    """从监控池移除"""
    stocks = load_stock_pool()
    if code in stocks:
        stocks.remove(code)
        save_stock_pool(stocks)
        return True
    return False

def monitor_all() -> List[Dict]:
    """监控所有股票"""
    stocks = load_stock_pool()
    results = []
    for code in stocks:
        result = analyze_stock(code)
        if "error" not in result:
            results.append(result)
        time.sleep(1)
    return results

def is_hk_stock(code: str) -> bool:
    """判断是否为港股"""
    # 方式1：4-5位数字，以0开头（老格式如 00981）
    if len(code) >= 4 and len(code) <= 5 and code.startswith("0"):
        return True
    # 方式2：已带hk前缀（hk00981）
    if code.startswith("hk"):
        return True
    return False

def is_a_stock(code: str) -> bool:
    """判断是否为A股（sz/sh前缀 + 6位数字）"""
    if len(code) == 8 and (code.startswith("sz") or code.startswith("sh")):
        return code[2:].isdigit()
    if len(code) == 6 and code.isdigit():
        return True
    return False

def validate_stock_mapping(code: str, quote: Dict) -> str:
    """
    校验股票代码和名称映射是否一致
    返回空字符串表示正常，否则返回警告信息
    """
    if not quote or "name" not in quote:
        return ""
    
    name = quote.get("name", "")
    stock_type = "unknown"
    
    # 根据代码判断应该是什么市场的股票
    if code.startswith("hk"):
        stock_type = "HK"
    elif len(code) == 6 and code.isdigit():
        stock_type = "A"
    elif code.startswith(("sh", "sz")):
        stock_type = "A"
    
    # 常见港股名称关键词（如果名称包含这些，认为是港股）
    hk_keywords = ["集团", "控股", "国际", "银行", "保险", "证券", "地产", "酒店", "娱乐", "技术", "健康", "医疗", "药业", "能源", "石油", "煤炭", "电力", "燃气", "水务", "公路", "铁路", "航空", "航运", "物流", "制造", "科技", "网络", "软件", "电子", "Semiconductor", "Holdings", "International", "Corp", "Ltd", "Co."]
    
    # 常见A股名称关键词（如果名称包含这些，认为是A股）
    a_keywords = ["股份", "有限", "公司", "集团", "实业", "投资", "发展", "控股", "国", "中"]
    
    # 检查名称是否包含市场特征
    is_likely_hk = any(kw in name for kw in hk_keywords)
    
    # 如果代码说应该是港股，但名称看起来像A股，警告
    if stock_type == "HK" and not is_likely_hk and len(name) < 10 and name.isdigit() == False:
        # 进一步检查：A股名称通常是中文，港股可能是英文或混合
        # 如果名称全是中文字符且不包含任何港股关键词，可能是错误
        if all('\u4e00' <= c <= '\u9fff' for c in name) and "集" not in name and "控" not in name:
            return f"[警告] 代码{code}被识别为港股，但返回名称'{name}'可能是A股Stock"
    
    return ""

def monitor_a() -> List[Dict]:
    """仅监控A股"""
    stocks = load_stock_pool()
    results = []
    for code in stocks:
        if is_a_stock(code):
            result = analyze_stock(code)
            if "error" not in result:
                results.append(result)
            time.sleep(1)
    return results

def monitor_hk() -> List[Dict]:
    """仅监控港股"""
    stocks = load_stock_pool()
    results = []
    for code in stocks:
        if is_hk_stock(code):
            result = analyze_stock(code)
            if "error" not in result:
                results.append(result)
            time.sleep(1)
    return results

def format_report(results: List[Dict]) -> str:
    """格式化报告"""
    if not results:
        return "监控池为空，请先添加股票"
    
    lines = ["📊 股票监控报告", "=" * 50, ""]
    
    for r in results:
        score_emoji = "🟢" if "买入" in r["overall"] else "🔴" if "卖出" in r["overall"] else "🟡"
        
        lines.append(f"{score_emoji} {r['name']} ({r['code']})")
        lines.append(f"   价格: {r['price']:.2f} ({r['change']:+.2f}, {r['change_pct']:+.2f}%)")
        lines.append(f"   📈 MA: 5日={r['indicators']['ma']['ma5']} | 10日={r['indicators']['ma']['ma10']} | 20日={r['indicators']['ma']['ma20']}")
        lines.append(f"   📊 MACD: DIF={r['indicators']['macd']['dif']:.4f} DEA={r['indicators']['macd']['dea']:.4f}")
        lines.append(f"   📉 KDJ: K={r['indicators']['kdj']['k']} D={r['indicators']['kdj']['d']} J={r['indicators']['kdj']['j']}")
        lines.append(f"   📊 RSI: {r['indicators']['rsi']['rsi6']}")
        lines.append(f"   🎯 BOLL: {r['indicators']['boll']['signal']}")
        lines.append(f"   📊 OBV: {r['indicators']['obv']['signal']}")
        lines.append(f"   📊 DMI: {r['indicators']['dmi']['signal']}")
        
        # 资讯情感（增强版）
        sent = r.get("sentiment", {})
        if sent and sent.get("sentiment") != "暂无":
            impact = sent.get("impact_level", "中性")
            lines.append(f"   📰 资讯情感: {sent['sentiment']} | 影响:{impact} | 积极{sent['positive_count']}分/消极{sent['negative_count']}分")
            if sent.get("news_titles"):
                for nt in sent["news_titles"][:3]:
                    lines.append(f"      {nt}")
            if sent.get("high_impact_count", 0) >= 1:
                lines.append(f"   🚨 高影响新闻: {sent['high_impact_count']}条")
        
        lines.append(f"   🎯 综合判断: {r['overall']}")
        lines.append("")
    
    return "\n".join(lines)

def calc_support_resistance(klines: List[Dict]) -> Dict:
    """
    计算支撑位和阻力位
    基于近30日高低点 + BOLL + 成交密集区
    """
    if not klines or len(klines) < 5:
        return {"support": None, "resistance": None, "pivot": None}
    
    closes = [k['close'] for k in klines]
    highs  = [k['high']  for k in klines]
    lows   = [k['low']   for k in klines]
    
    # 近30日（或全部）高低价
    recent_high  = max(highs[-30:]) if len(highs) >= 30 else max(highs)
    recent_low   = min(lows[-30:])  if len(lows)  >= 30 else min(lows)
    
    # BOLL
    boll = calculate_boll(closes[-20:]) if len(closes) >= 20 else None
    boll_upper = boll["upper"]  if boll else None
    boll_mid   = boll["middle"] if boll else None
    boll_lower = boll["lower"]  if boll else None
    
    # 近5日高低点（短线参考）
    short_high = max(highs[-5:])
    short_low  = min(lows[-5:])
    
    # 阻力位：优先用近30日高点，其次BOLL上轨
    resistance = recent_high if recent_high > closes[-1] * 1.02 else (boll_upper if boll_upper and boll_upper > closes[-1] else short_high)
    
    # 支撑位：优先用近30日低点，其次BOLL下轨
    support = recent_low if recent_low < closes[-1] * 0.98 else (boll_lower if boll_lower and boll_lower < closes[-1] else short_low)
    
    # 枢轴点（三价平均）
    pivot = (recent_high + recent_low + closes[-1]) / 3 if recent_high and recent_low else None
    
    return {
        "support":     round(support, 2) if support else None,
        "resistance":  round(resistance, 2) if resistance else None,
        "pivot":       round(pivot, 2) if pivot else None,
        "boll_upper":  round(boll_upper, 2) if boll_upper else None,
        "boll_lower":  round(boll_lower, 2) if boll_lower else None,
        "short_high":  round(short_high, 2),
        "short_low":   round(short_low, 2),
    }

def assess_trend_strength(dmi: Dict, macd: Dict, ma: Dict) -> Dict:
    """
    多维度评估趋势强度
    返回：短期/中期/长期趋势评分 + 综合趋势方向
    """
    adx = dmi.get("adx", 0)
    plus_di = dmi.get("plus_di", 0)
    minus_di = dmi.get("minus_di", 0)
    
    # ADX趋势强度：<20无趋势，20-25弱，25-40中，>40强
    if adx < 20:
        adx_strength = "⚪ 无明显趋势"
        adx_score = 0
    elif adx < 25:
        adx_strength = "🟡 趋势偏弱"
        adx_score = 1
    elif adx < 40:
        adx_strength = "🟢 趋势确认"
        adx_score = 2
    else:
        adx_strength = "🔴 趋势强劲"
        adx_score = 3
    
    # 多空力量对比
    di_diff = plus_di - minus_di
    if di_diff > 10:
        trend_dir = "多头主导"
        dir_score = 1
    elif di_diff < -10:
        trend_dir = "空头主导"
        dir_score = -1
    else:
        trend_dir = "多空均衡"
        dir_score = 0
    
    # MACD状态
    macd_signal = macd.get("signal", "")
    if "金叉" in macd_signal:
        macd_trend = "上升"
        macd_score = 1
    elif "死叉" in macd_signal:
        macd_trend = "下降"
        macd_score = -1
    else:
        macd_trend = "收敛"
        macd_score = 0
    
    # 均线多空排列
    ma5  = ma.get("ma5", 0)
    ma10 = ma.get("ma10", 0)
    ma20 = ma.get("ma20", 0)
    price = ma.get("price", 0)
    
    if ma5 > ma10 > ma20 and price > ma5:
        ma_status = "多头排列（强势）"
        ma_score = 2
    elif ma5 < ma10 < ma20 and price < ma5:
        ma_status = "空头排列（弱势）"
        ma_score = -2
    elif ma5 > ma10:
        ma_status = "短多中空"
        ma_score = 0.5
    elif ma5 < ma10:
        ma_status = "短空中多"
        ma_score = -0.5
    else:
        ma_status = "均线纠缠"
        ma_score = 0
    
    # 综合评分
    total_score = adx_score + dir_score + macd_score + ma_score
    if total_score >= 4:
        overall_trend = "📈 上升趋势"
    elif total_score >= 2:
        overall_trend = "↗️ 震荡偏多"
    elif total_score <= -4:
        overall_trend = "📉 下降趋势"
    elif total_score <= -2:
        overall_trend = "↘️ 震荡偏空"
    else:
        overall_trend = "↔️ 区间震荡"
    
    return {
        "adx":         round(adx, 2),
        "adx_strength": adx_strength,
        "trend_dir":   trend_dir,
        "macd_trend":  macd_trend,
        "ma_status":   ma_status,
        "overall_trend": overall_trend,
        "total_score": total_score
    }

def format_single_stock_analysis(r: Dict, position: Dict = None) -> List[str]:
    """
    格式化单只股票分析（用于综合报告）
    返回多行字符串列表
    """
    lines = []
    code  = r.get("code", "")
    name  = r.get("name", code)
    price = r.get("price", 0)
    chg   = r.get("change", 0)
    pct   = r.get("change_pct", 0)
    ind   = r.get("indicators", {})
    ma    = ind.get("ma", {})
    macd  = ind.get("macd", {})
    kdj   = ind.get("kdj", {})
    rsi   = ind.get("rsi", {})
    boll  = ind.get("boll", {})
    dmi   = ind.get("dmi", {})
    obv   = ind.get("obv", {})
    wr    = ind.get("wr", {})
    sent  = r.get("sentiment", {})
    score = r.get("score", {})
    klines = r.get("klines", [])
    
    # 价格颜色
    price_emoji = "🟢" if pct >= 0 else "🔴"
    
    # === 1. 基础行情 ===
    lines.append(f"{'─'*56}")
    lines.append(f"  {price_emoji} {name}({code})  ¥{price} {chg:+.2f}({pct:+.2f}%)")
    
    # === 2. 持仓信息（如果有）===
    if position:
        qty   = position.get("quantity", 0)
        cost  = position.get("cost_price", 0)
        mkt_val = price * qty
        pnl   = (price - cost) * qty
        pnl_pct = (price - cost) / cost * 100 if cost > 0 else 0
        pnl_emoji = "🟢" if pnl >= 0 else "🔴"
        lines.append(f"  📦 持仓: {qty}股 @ 成本{cost:.2f} | 市值{mkt_val:.0f} | {pnl_emoji}盈亏{pnl:+.0f}({pnl_pct:+.1f}%)")
    
    # === 3. 支撑/阻力 ===
    sr = calc_support_resistance(klines) if klines else {}
    if sr.get("support") and sr.get("resistance"):
        lines.append(f"  📍 支撑/阻力: {sr['support']} / {sr['resistance']} | 枢轴 {sr.get('pivot','N/A')}")
        if sr.get("boll_upper"):
            lines.append(f"  📊 BOLL: 上轨{boll.get('upper',0):.2f} 中轨{boll.get('middle',0):.2f} 下轨{boll.get('lower',0):.2f} → {boll.get('signal','')}")
    
    # === 4. 趋势评估 ===
    trend_info = assess_trend_strength(dmi, macd, {**ma, "price": price})
    lines.append(f"  📈 趋势: {trend_info['overall_trend']} | ADX{trend_info['adx']} {trend_info['adx_strength']}")
    lines.append(f"  ↔️  均线: {trend_info['ma_status']} | MACD: {trend_info['macd_trend']} | DMI: {trend_info['trend_dir']}")
    
    # === 5. 关键指标（分三行）===
    lines.append(f"  📊 MACD: DIF={macd.get('dif',0):.4f} DEA={macd.get('dea',0):.4f} | {macd.get('signal','')}")
    lines.append(f"  📊 KDJ:  K={kdj.get('k',0):.1f} D={kdj.get('d',0):.1f} J={kdj.get('j',0):.1f} | {kdj.get('signal','')}")
    lines.append(f"  📊 RSI:  6日={rsi.get('rsi6',0):.1f} 12日={rsi.get('rsi12',0):.1f} 24日={rsi.get('rsi24',0):.1f} | {rsi.get('signal','')}")
    lines.append(f"  📊 OBV:  {obv.get('signal','')} | WR: {wr.get('signal','')}")
    
    # === 6. 资讯情感 ===
    sentiment_val = sent.get("sentiment", "暂无")
    sentiment_weighted = sent.get("weighted_score", 0)
    sentiment_impact = sent.get("impact_level", "无")
    if sentiment_val != "暂无":
        lines.append(f"  📰 资讯: {sentiment_val} | 影响:{sentiment_impact} | 积极{sent.get('positive_count',0)}分/消极{sent.get('negative_count',0)}分")
        news_titles = sent.get("news_titles", [])
        if news_titles:
            for nt in news_titles[:2]:
                lines.append(f"      • {nt}")
    else:
        lines.append(f"  📰 资讯: 暂无新闻数据")
    
    # === 7. 综合信号与建议 ===
    buy_s  = score.get("buy", 0)
    sell_s = score.get("sell", 0)
    overall = r.get("overall", "观望")
    
    # 评分条
    bar_len = 10
    buy_bar  = "█" * min(int(buy_s), bar_len)
    sell_bar = "▓" * min(int(sell_s), bar_len)
    lines.append(f"  🎯 信号: {overall} | 买入{buy_s}:{sell_s}卖出 | [{buy_bar}{sell_bar}]")
    
    # 操作建议（结合趋势+信号+持仓）
    suggestions = _generate_suggestion(r, trend_info, position)
    if suggestions:
        lines.append(f"  💡 建议: {suggestions}")
    
    return lines

def _generate_suggestion(r: Dict, trend_info: Dict, position: Dict = None) -> str:
    """生成操作建议"""
    score = r.get("score", {})
    buy_s  = score.get("buy", 0)
    sell_s = score.get("sell", 0)
    trend_score = trend_info.get("total_score", 0)
    overall = r.get("overall", "")
    price = r.get("price", 0)
    pct   = r.get("change_pct", 0)
    kdj   = r.get("indicators", {}).get("kdj", {})
    rsi_v = r.get("indicators", {}).get("rsi", {}).get("rsi6", 50)
    sr    = calc_support_resistance(r.get("klines", [])) if r.get("klines") else {}
    
    suggestions = []
    
    # 1. 趋势为基础
    if trend_score >= 3 and buy_s > sell_s:
        suggestions.append("🚀 上升趋势确认，多头信号共振，可持仓或加仓")
    elif trend_score <= -3 and sell_s > buy_s:
        suggestions.append("🔴 下降趋势确认，空头信号共振，建议减仓止损")
    elif buy_s >= 6:
        suggestions.append("✅ 技术面偏多，高概率向上")
    elif sell_s >= 6:
        suggestions.append("⚠️ 技术面偏空，高概率向下，谨慎")
    elif "超卖" in kdj.get("signal", "") or rsi_v < 30:
        suggestions.append("⚡ RSI/KDJ超卖，短线反弹概率大")
    elif "超买" in kdj.get("signal", "") or rsi_v > 70:
        suggestions.append("⚡ RSI/KDJ超买，短线调整风险")
    else:
        suggestions.append("📊 方向不明，保持观望")
    
    # 2. 支撑/阻力提示
    if sr.get("support") and price <= sr["support"] * 1.02:
        suggestions.append(f"⚠️ 接近支撑位{sr['support']}，注意跌破风险")
    if sr.get("resistance") and price >= sr["resistance"] * 0.98:
        suggestions.append(f"⚠️ 接近阻力位{sr['resistance']}，突破可加仓")
    
    # 3. 持仓用户专属建议
    if position:
        cost  = position.get("cost_price", 0)
        qty   = position.get("quantity", 0)
        pnl_pct = (price - cost) / cost * 100 if cost > 0 else 0
        pnl   = (price - cost) * qty
        
        if pnl > 0 and sell_s > buy_s + 2:
            suggestions.append(f"🟢 盈利{pnl_pct:.1f}%但技术面转弱，建议部分止盈")
        elif pnl < 0 and buy_s > sell_s + 2:
            suggestions.append(f"🔵 亏损{pnl_pct:.1f}%但技术面转强，可加仓摊低成本")
        elif pnl_pct > 15:
            suggestions.append(f"🟢 盈利{pnl_pct:.1f}%，建议设动态止盈")
    
    return " | ".join(suggestions[:2])

def generate_full_report(market_indices: List[Dict], stock_results: List[Dict], period_label: str = "盘中") -> str:
    """
    生成综合分析报告（增强版）
    整合大盘技术面 + 个股多维度分析 + 持仓 + 资讯
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    
    # ========== 1. 报告头 ==========
    lines.append(f"{'📊'*25}")
    lines.append(f"  🔍 股票综合分析报告 {period_label}")
    lines.append(f"  🕐 更新时间: {now_str}")
    lines.append("")
    
    # ========== 2. 大盘指数 ==========
    if market_indices:
        lines.append("【大盘指数】")
        for idx in market_indices:
            emoji = "🟢" if idx['pct'] > 0 else "🔴" if idx['pct'] < 0 else "🟡"
            lines.append(f"  {emoji} {idx['name']}: {idx['price']} {idx['change']:+.2f}({idx['pct']:+.2f}%)")
        lines.append("")
    
    # ========== 3. 市场情绪总览 ==========
    all_sentiments = [r.get("sentiment", {}) for r in stock_results if r.get("sentiment")]
    pos_total = sum(s.get("positive_count", 0) for s in all_sentiments)
    neg_total = sum(s.get("negative_count", 0) for s in all_sentiments)
    
    # 涨跌统计
    up_count   = sum(1 for r in stock_results if r.get("change_pct", 0) > 0)
    down_count = sum(1 for r in stock_results if r.get("change_pct", 0) < 0)
    flat_count = len(stock_results) - up_count - down_count
    
    if pos_total > neg_total * 1.5:
        market_mood = "📈 偏多（资讯积极）"
    elif neg_total > pos_total * 1.5:
        market_mood = "📉 偏空（资讯消极）"
    else:
        market_mood = "↔️ 中性（多空均衡）"
    
    lines.append("【市场情绪】")
    lines.append(f"  股票涨跌: ↑{up_count} ↓{down_count} →{flat_count}")
    lines.append(f"  资讯情感: 积极{pos_total}分 / 消极{neg_total}分 | {market_mood}")
    lines.append("")
    
    # ========== 4. 分持仓/关注股 ==========
    positions_all = load_positions()
    
    # 4a. 持仓股
    held = [r for r in stock_results if r.get("code") in positions_all]
    watch = [r for r in stock_results if r.get("code") not in positions_all]
    
    if held:
        lines.append("【📦 持仓股分析】")
        # 汇总持仓盈亏
        total_mkt = 0.0
        total_pnl = 0.0
        for r in held:
            code  = r.get("code")
            price = r.get("price", 0)
            pos   = positions_all.get(code, {})
            qty   = pos.get("quantity", 0)
            cost  = pos.get("cost_price", 0)
            mkt   = price * qty
            pnl   = (price - cost) * qty if cost else 0
            total_mkt += mkt
            total_pnl  += pnl
        
        total_pnl_pct = total_pnl / (total_mkt - total_pnl) * 100 if total_mkt > total_pnl else 0
        pnl_emoji = "🟢" if total_pnl >= 0 else "🔴"
        lines.append(f"  {'─'*52}")
        lines.append(f"  💼 总持仓市值: ¥{total_mkt:,.0f} | {pnl_emoji}总盈亏: {total_pnl:+,.0f}({total_pnl_pct:+.1f}%)")
        lines.append("")
        
        for r in held:
            code  = r.get("code")
            pos   = positions_all.get(code, {})
            for l in format_single_stock_analysis(r, pos):
                lines.append(f"  {l}")
            lines.append("")
    
    # 4b. 关注股
    if watch:
        lines.append("【👁️ 关注股分析】")
        for r in watch:
            for l in format_single_stock_analysis(r):
                lines.append(f"  {l}")
            lines.append("")
    
    # ========== 5. 综合评级排序 ==========
    lines.append("【📋 综合评级】")
    sorted_stocks = sorted(stock_results, key=lambda x: x.get("score", {}).get("buy", 0) - x.get("score", {}).get("sell", 0), reverse=True)
    for i, r in enumerate(sorted_stocks, 1):
        score  = r.get("score", {})
        buy_s  = score.get("buy", 0)
        sell_s = score.get("sell", 0)
        diff   = buy_s - sell_s
        overall = r.get("overall", "观望")
        price  = r.get("price", 0)
        pct    = r.get("change_pct", 0)
        emoji  = "🟢" if pct >= 0 else "🔴"
        sign   = "+" if diff >= 0 else ""
        lines.append(f"  {i}. {emoji}{r.get('name','')}({r.get('code','')}) {emoji}{price}({pct:+.2f}%) | 信号{overall} | 差值:{sign}{diff}")
    
    lines.append("")
    lines.append(f"{'📊'*25}")
    lines.append(f"  ⚠️ 仅供参考，不构成投资建议")
    
    return "\n".join(lines)

# 命令行入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Stock Monitor CLI")
        print("Usage: python stock_monitor.py <command> [args]")
        print("Commands:")
        print("  quote <code>        - 查询股票行情")
        print("  index               - 查询大盘指数")
        print("  analyze <code>      - 分析股票技术指标")
        print("  add <code>          - 添加股票到监控池")
        print("  remove <code>       - 从监控池移除")
        print("  list                - 查看监控池")
        print("  monitor             - 监控所有股票")
        print("  monitor-a           - 仅监控A股")
        print("  monitor-hk          - 仅监控港股")
        print("  report [标签]       - 生成综合分析报告（含大盘+持仓+资讯+趋势）")
        print("  report-a [标签]     - 生成A股综合分析报告")
        print("  report-hk [标签]    - 生成港股综合分析报告")
        print("  position add <code> <quantity> <cost_price>  - 添加持仓")
        print("  position remove <code> - 清除持仓")
        print("  position list       - 查看持仓")
        print("  position <code>     - 分析单只持仓")
        print("  trade buy <code> <quantity> <price> - 记录买入")
        print("  trade sell <code> <quantity> <price> - 记录卖出")
        print("  trades [code]       - 查看交易记录")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    # 持仓管理命令
    if cmd == "position" and len(sys.argv) >= 2:
        subcmd = sys.argv[2] if len(sys.argv) > 2 else "list"
        
        if subcmd == "list":
            positions = load_positions()
            if not positions:
                print("暂无持仓")
            else:
                for code, pos in positions.items():
                    quote = get_stock_quote(code)
                    name = quote["name"] if quote else code
                    print(f"{code} {name}: {pos['quantity']}股 @ {pos['cost_price']}")
        
        elif subcmd == "add" and len(sys.argv) >= 5:
            code = sys.argv[3]
            quantity = float(sys.argv[4])
            cost_price = float(sys.argv[5])
            add_position(code, quantity, cost_price)
            print(f"已添加持仓: {code} {quantity}股 @ {cost_price}")
        
        elif subcmd == "remove" and len(sys.argv) >= 4:
            code = sys.argv[3]
            remove_position(code)
            print(f"已清除持仓: {code}")
        
        elif len(sys.argv) >= 3:
            # 分析单只持仓
            code = sys.argv[2]
            result = analyze_position(code)
            if "error" in result:
                print(result["error"])
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("用法: position <add|remove|list|code>")
    
    # 交易记录命令
    elif cmd == "trade" and len(sys.argv) >= 3:
        subcmd = sys.argv[2]
        
        if subcmd == "buy" and len(sys.argv) >= 6:
            code = sys.argv[3]
            quantity = float(sys.argv[4])
            price = float(sys.argv[5])
            add_trade(code, "买入", quantity, price)
            add_position(code, quantity, price)  # 同时更新持仓
            print(f"已记录买入: {code} {quantity}股 @ {price}")
        
        elif subcmd == "sell" and len(sys.argv) >= 6:
            code = sys.argv[3]
            quantity = float(sys.argv[4])
            price = float(sys.argv[5])
            add_trade(code, "卖出", quantity, price)
            
            # 更新持仓
            pos = get_position(code)
            if pos:
                new_qty = pos["quantity"] - quantity
                if new_qty <= 0:
                    remove_position(code)
                    print(f"已清仓: {code}")
                else:
                    add_position(code, new_qty, pos["cost_price"])
                    print(f"已记录卖出并更新持仓: {code} 剩余{new_qty}股")
            else:
                print(f"已记录卖出: {code} (无持仓记录)")
        
        else:
            print("用法: trade <buy|sell> <code> <quantity> <price>")
    
    elif cmd == "trades":
        code = sys.argv[2] if len(sys.argv) > 2 else None
        trades = get_trades(code)
        if not trades:
            print("暂无交易记录")
        else:
            for t in trades:
                print(f"{t['date'][:10]} {t['action']} {t['code']} {t['quantity']}股 @ {t['price']}")
    
    elif cmd == "quote" and len(sys.argv) > 2:
        quote = get_stock_quote(sys.argv[2])
        print(json.dumps(quote, ensure_ascii=False, indent=2))

    elif cmd == "index":
        indices = get_market_index()
        for idx in indices:
            emoji = "🟢" if idx['pct'] > 0 else "🔴" if idx['pct'] < 0 else "🟡"
            print(f"{emoji} {idx['name']}: {idx['price']} {idx['change']:+.2f} ({idx['pct']:+.2f}%)")
        print("\n--- JSON ---")
        print(json.dumps(indices, ensure_ascii=False, indent=2))
    
    elif cmd == "analyze" and len(sys.argv) > 2:
        result = analyze_stock(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "add" and len(sys.argv) > 2:
        if add_to_pool(sys.argv[2]):
            print(f"已添加 {sys.argv[2]} 到监控池")
        else:
            print(f"{sys.argv[2]} 已在监控池中")
    
    elif cmd == "remove" and len(sys.argv) > 2:
        if remove_from_pool(sys.argv[2]):
            print(f"已从监控池移除 {sys.argv[2]}")
        else:
            print(f"{sys.argv[2]} 不在监控池中")
    
    elif cmd == "list":
        stocks = load_stock_pool()
        print(f"监控池: {stocks}")
    
    elif cmd == "monitor":
        results = monitor_all()
        print(format_report(results))
    
    elif cmd == "monitor-a":
        results = monitor_a()
        print(format_report(results))
    
    elif cmd == "monitor-hk":
        results = monitor_hk()
        print(format_report(results))
    
    elif cmd == "report":
        # 综合报告（所有股票）
        indices = get_market_index()
        results = monitor_all()
        period_label = "综合报告"
        if len(sys.argv) > 2:
            period_label = sys.argv[2]
        print(generate_full_report(indices, results, period_label))
    
    elif cmd == "report-a":
        # A股综合报告
        indices = get_market_index()
        results = monitor_a()
        period_label = "A股综合报告"
        if len(sys.argv) > 2:
            period_label = sys.argv[2]
        print(generate_full_report(indices, results, period_label))
    
    elif cmd == "report-hk":
        # 港股综合报告
        indices = get_market_index()
        results = monitor_hk()
        period_label = "港股综合报告"
        if len(sys.argv) > 2:
            period_label = sys.argv[2]
        print(generate_full_report(indices, results, period_label))
    
    else:
        print("未知命令")
