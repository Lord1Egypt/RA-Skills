#!/usr/bin/env python3
"""
研林 · 新闻过滤脚本
从公开财经资讯获取当日新闻，过滤筛选重要事件
"""
import json, sys, re, urllib.request, html as html_mod, time

def fetch_url(url, headers=None):
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except:
        return None

# 重要性关键词
HIGH_IMPACT_KW = [
    "央行", "降息", "降准", "加息", "证监会", "国务院", "政治局", 
    "严重短缺", "涨价", "暴跌", "暴涨", "突破", "创历史", 
    "特朗普", "美联储", "制裁", "关税", "战争", 
    "业绩预告", "并购", "重大合同", "IPO", "上市",
    "产能", "供需", "供不应求", "扩产", "减产"
]

SECTOR_MAP = {
    "芯片": "半导体", "存储": "存储芯片", "光伏": "光伏", 
    "新能源": "新能源", "锂": "锂电", "黄金": "贵金属",
    "茅台": "白酒", "汽车": "汽车", "医药": "医药",
    "AI": "人工智能", "机器人": "机器人", "军工": "军工",
    "消费": "消费", "地产": "房地产", "银行": "银行",
    "券商": "券商", "保险": "保险", "石油": "石油石化",
    "煤炭": "煤炭", "钢铁": "钢铁", "通信": "通信"
}

def get_news_from_sina():
    """从新浪财经获取最新新闻"""
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=30&page=1&r=0.1"
    data = fetch_url(url)
    if not data:
        return []
    
    news_list = []
    try:
        obj = json.loads(data)
        for item in obj.get('result', {}).get('data', []):
            title = html_mod.unescape(item.get('title', ''))
            ctime = item.get('ctime', '')
            news_list.append({"title": title, "time": ctime})
    except:
        pass
    return news_list

def score_importance(title):
    """评估新闻重要性"""
    score = 1
    matched_kw = []
    for kw in HIGH_IMPACT_KW:
        if kw in title:
            score += 1
            matched_kw.append(kw)
    # 长标题通常信息量更大
    if len(title) > 20:
        score += 0.5
    return min(round(score), 5), matched_kw

def map_sectors(title):
    """将新闻映射到行业赛道"""
    sectors = []
    for kw, sector in SECTOR_MAP.items():
        if kw in title:
            sectors.append(sector)
    return sectors if sectors else ["综合"]

def main():
    output_format = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--output' else 'text'
    
    raw_news = get_news_from_sina()
    
    events = []
    for news in raw_news:
        title = news['title']
        importance, matched_kw = score_importance(title)
        sectors = map_sectors(title)
        
        if importance >= 2:  # 筛选重要性≥2的
            event = {
                "title": title,
                "source": "新浪财经",
                "importance": importance,
                "category": "综合",
                "related_sectors": sectors,
                "is_marginal": importance >= 3
            }
            events.append(event)
    
    # 按重要性排序
    events.sort(key=lambda x: x['importance'], reverse=True)
    
    result = {
        "date": time.strftime("%Y-%m-%d"),
        "total_raw": len(raw_news),
        "total_filtered": len(events),
        "events": events[:8]  # 保留前8条最重要事件
    }
    
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 关键事件筛选 ({result['date']}) ===")
        print(f"原始{result['total_raw']}条 → 筛选出{result['total_filtered']}条重要事件\n")
        for e in result['events']:
            stars = "⭐" * e['importance']
            sectors_str = "/".join(e['related_sectors'])
            print(f"  {stars} [{sectors_str}] {e['title']}")

if __name__ == '__main__':
    main()
