#!/usr/bin/env python3
"""
研林 · 公司公告采集脚本（V2 — 多源接入）
接入新浪财经 + 上交所/深交所公开披露 + 新闻API 自动采集公告数据

数据源架构：
  Tier 1 [主]: 新浪财经新闻API — 实时市场新闻（含公司公告覆盖）
  Tier 2 [主]: 新浪个股信息地雷页 — 逐股提取近期公告事件
  Tier 3 [辅]: 上交所/深交所公开披露PDF链接索引
  Tier 4 [备]: 直接公告摘要匹配（公司公告分类关键词）

输出格式：按重要性排序的结构化JSON表格
"""
import json, sys, re, urllib.request, urllib.error, html as html_mod, time, os

# ========================================
# 核心股票池
# ========================================
CORE_STOCKS = [
    {"code":"sh600519","name":"贵州茅台","sector":"白酒"},
    {"code":"sz300750","name":"宁德时代","sector":"新能源"},
    {"code":"sh600036","name":"招商银行","sector":"银行"},
    {"code":"sh601318","name":"中国平安","sector":"保险"},
    {"code":"sh600030","name":"中信证券","sector":"券商"},
    {"code":"sh600900","name":"长江电力","sector":"电力"},
    {"code":"sh601899","name":"紫金矿业","sector":"贵金属"},
    {"code":"sh600276","name":"恒瑞医药","sector":"医药"},
    {"code":"sh600585","name":"海螺水泥","sector":"建材"},
    {"code":"sz000858","name":"五粮液","sector":"白酒"},
    {"code":"sz002475","name":"立讯精密","sector":"消费电子"},
    {"code":"sz000333","name":"美的集团","sector":"家电"},
    {"code":"sz000651","name":"格力电器","sector":"家电"},
    {"code":"sz002594","name":"比亚迪","sector":"新能源汽车"},
    {"code":"sz300059","name":"东方财富","sector":"券商"},
    {"code":"sz002230","name":"科大讯飞","sector":"人工智能"},
    {"code":"sz002415","name":"海康威视","sector":"安防"},
    {"code":"sh601012","name":"隆基绿能","sector":"光伏"},
    {"code":"sz002129","name":"TCL中环","sector":"光伏"},
    {"code":"sz002466","name":"天齐锂业","sector":"锂电"},
    {"code":"sz002714","name":"牧原股份","sector":"养殖"},
    {"code":"sh600703","name":"三安光电","sector":"半导体"},
    {"code":"sh600887","name":"伊利股份","sector":"食品饮料"},
    {"code":"sz300124","name":"汇川技术","sector":"自动化"},
    {"code":"sh600690","name":"海尔智家","sector":"家电"},
    {"code":"sh601857","name":"中国石油","sector":"石油石化"},
    {"code":"sh600010","name":"包钢股份","sector":"钢铁"},
    {"code":"sh600171","name":"上海贝岭","sector":"半导体"},
    {"code":"sh601127","name":"赛力斯","sector":"新能源汽车"},
    {"code":"sh688981","name":"中芯国际","sector":"半导体"},
]

# ========================================
# 公告影响关键词体系
# ========================================
KEYWORD_CATEGORIES = {
    "业绩": ["业绩预告","业绩快报","业绩预增","业绩预减","业绩预亏","净利润","扭亏为盈",
             "大幅增长","营收","利润总额","扣非","EPS","每股收益"],
    "资本运作": ["增发","配股","回购","减持","增持","股权激励","并购","重组","收购",
               "出售资产","借壳","要约收购","私有化"],
    "业务订单": ["中标","重大合同","战略合作","框架协议","订单","新客户","供货"],
    "产能项目": ["扩产","投产","新产线","产能","开工","竣工","投资建设"],
    "分红融资": ["分红","送转","派息","可转债","债券发行","融资"],
    "监管风险": ["立案","处罚","问询","监管措施","调查","风险提示","ST","退市","警示"],
    "人事治理": ["董事长变更","总经理变更","董事会换届","独立董事","高管变动"],
    "IPO上市": ["IPO","首发","上市","科创板","注册制","过会"],
}

# 公告类型 → 影响分值映射
TYPE_IMPORTANCE = {
    "业绩": 4.5, "资本运作": 4.0, "业务订单": 3.5, "产能项目": 3.0,
    "分红融资": 2.5, "监管风险": 4.0, "人事治理": 2.0, "IPO上市": 3.5,
}

def fetch_url_text(url, timeout=10):
    """通用URL文本获取，自动编码检测"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            ct = resp.headers.get('Content-Type', '')
            if 'json' in ct:
                return raw.decode('utf-8')
            for enc in ['utf-8', 'gb2312', 'gbk']:
                try:
                    return raw.decode(enc)
                except:
                    continue
            return raw.decode('utf-8', errors='replace')
    except Exception as e:
        return None

def classify_announcement(title):
    """对公告标题进行类型分类"""
    for cat, keywords in KEYWORD_CATEGORIES.items():
        for kw in keywords:
            if kw in title:
                return cat
    return None

def calc_importance(title):
    """基于公告类型+关键词密度计算重要性（1-5）"""
    cat = classify_announcement(title)
    base = TYPE_IMPORTANCE.get(cat, 1.5)
    
    # 加分：含具体数字（金额/比例）
    if re.search(r'[亿万千百]\d+', title) or re.search(r'\d+[%％]', title):
        base += 0.5
    # 加分：超级关键词
    if any(kw in title for kw in ["大幅增长","扭亏","中标","重大","历史新高"]):
        base += 0.5
    
    return min(max(round(base), 1), 5)

# ========================================
# Tier 1: 新浪财经新闻API
# ========================================
def tier1_news_api():
    """从新浪财经新闻API获取含公告的新闻"""
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.1"
    data = fetch_url_text(url, timeout=8)
    if not data:
        return []
    
    items = []
    try:
        obj = json.loads(data)
        for item in obj.get('result', {}).get('data', []):
            title = html_mod.unescape(item.get('title', ''))
            ctime = item.get('ctime', '')
            items.append({"title": title, "time": ctime})
    except:
        pass
    return items

# ========================================
# Tier 2: 新浪个股信息地雷页
# ========================================
def tier2_stock_bulletin(stock):
    """从个股公告页提取公告事件"""
    code_num = stock['code'][2:]
    
    results = []
    
    # 方法A: 公告页面 — vCB_AllBulletin
    urls_to_try = [
        f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/{code_num}/p/1.phtml",
        f"http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllMemordDetail/stockid/{code_num}.phtml",
        f"http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllMemordDetail.php?stockid={code_num}",
    ]
    
    html_content = ""
    for url in urls_to_try:
        html = fetch_url_text(url, timeout=6)
        if html and len(html) > 1000:
            html_content = html
            break
    
    if not html_content:
        return results
    
    seen = set()
    
    # 提取所有带公告关键词的标题文本
    # 方法1: 从link文本提取
    links = re.findall(r'<a[^>]*>(.*?)</a>', html_content)
    for text in links:
        text = re.sub(r'<[^>]+>', '', text).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) < 8 or text in seen:
            continue
        seen.add(text)
        
        cat = classify_announcement(text)
        if cat:
            results.append({
                "company": stock['name'], "code": stock['code'],
                "event": text[:80], "category": cat,
                "importance": calc_importance(text),
                "direction": judge_direction(text),
                "sector": stock['sector']
            })
    
    # 方法2: 从表格单元格提取
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        for cell in cells:
            plain = re.sub(r'<[^>]+>', '', cell).strip()
            plain = re.sub(r'\s+', ' ', plain)
            if len(plain) < 10 or plain in seen or re.match(r'^[\d.]+$', plain):
                continue
            seen.add(plain)
            
            # 检查是否包含日期模式和公告关键词
            has_date = bool(re.search(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', plain))
            cat = classify_announcement(plain)
            if has_date or cat:
                results.append({
                    "company": stock['name'], "code": stock['code'],
                    "event": plain[:80], "category": cat or "综合",
                    "importance": calc_importance(plain) if cat else 2,
                    "direction": judge_direction(plain),
                    "sector": stock['sector']
                })
    
    return results

# ========================================
# Tier 3: 上交所/深交所公开披露
# ========================================
def tier3_sse_szse():
    """获取上交所/深交所公开披露链接（仅索引）"""
    # 上交所: 当天披露文件列表
    today = time.strftime("%Y-%m-%d")
    date_path = today.replace('-', '')
    
    results = []
    
    # 上交所某日披露
    for exchange, domain in [("上交所", "http://www.sse.com.cn"), ("深交所", "http://www.szse.cn")]:
        results.append({
            "company": exchange, "code": "",
            "event": f"{exchange}公开披露: {today}的披露文件索引",
            "source_url": f"{domain}/disclosure/listedinfo/announcement/",
            "importance": 2,
            "direction": "neutral",
            "sector": "综合",
            "date": today
        })
    
    return results

# ========================================
# 工具函数
# ========================================
def judge_direction(title):
    """判断利好/利空"""
    positive = ["预增","扭亏","中标","重大合同","回购","增持","分红","送转",
                "增长","扩产","投产","战略合作","获批","突破","新高"]
    negative = ["预减","预亏","减持","处罚","立案","ST","退市","风险提示",
                "亏损","调查","问询","警示","违约","逾期"]
    
    pos_score = sum(1 for kw in positive if kw in title)
    neg_score = sum(1 for kw in negative if kw in title)
    
    if pos_score > neg_score: return "positive"
    if neg_score > pos_score: return "negative"
    return "neutral"

def filter_news_for_filings(news_items):
    """从新闻API数据中筛选公告类信息"""
    filings = []
    
    # 提取标题中出现的公司名
    company_name_map = {s['name']: s for s in CORE_STOCKS}
    
    for item in news_items:
        title = item['title']
        cat = classify_announcement(title)
        if not cat:
            continue
        
        # 匹配公司
        matched_company = ""
        matched_sector = "综合"
        for name, stock in company_name_map.items():
            if name in title:
                matched_company = name
                matched_sector = stock['sector']
                break
        
        filings.append({
            "company": matched_company or "（多家/市场公告）",
            "code": company_name_map[matched_company]['code'] if matched_company in company_name_map else "",
            "event": title,
            "source": "新浪财经新闻",
            "category": cat,
            "importance": calc_importance(title),
            "direction": judge_direction(title),
            "sector": matched_sector,
            "date": item.get('time', '')
        })
    
    return filings

# ========================================
# 主流程
# ========================================
def main():
    output_format = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--output' else 'text'
    today = time.strftime("%Y-%m-%d")
    
    all_filings = []
    
    # === Tier 1: 新闻API ===
    print(f"[{today}] Tier1: 新浪财经新闻API...", file=sys.stderr)
    news = tier1_news_api()
    news_filings = filter_news_for_filings(news)
    all_filings.extend(news_filings)
    print(f"  新闻API: {len(news)}条 → 公告筛选 {len(news_filings)}条", file=sys.stderr)
    
    # === Tier 2: 个股公告页 ===
    print(f"[{today}] Tier2: 个股公告查询 ({len(CORE_STOCKS)}支)...", file=sys.stderr)
    stock_hits = 0
    for stock in CORE_STOCKS:
        try:
            results = tier2_stock_bulletin(stock)
            if results:
                all_filings.extend(results)
                stock_hits += len(results)
            time.sleep(0.2)
        except Exception as e:
            pass
    print(f"  个股公告: 共命中 {stock_hits} 条", file=sys.stderr)
    
    # === Tier 3: 交易所披露 ===
    exchange_filings = tier3_sse_szse()
    all_filings.extend(exchange_filings)
    
    # === 去重+排序 ===
    seen = set()
    unique = []
    for f in all_filings:
        key = f"{f['company']}|{f['event'][:40]}"
        if key not in seen:
            seen.add(key)
            unique.append(f)
    
    unique.sort(key=lambda x: x['importance'], reverse=True)
    
    # 只保留重要性≥2
    filtered = [f for f in unique if f['importance'] >= 2]
    
    result = {
        "date": today,
        "total_raw": len(unique),
        "total_filtered": len(filtered),
        "filings": filtered[:12],
        "data_sources": [
            "新浪财经新闻API (feed.mix.sina.com.cn)",
            "新浪个股公告页 (vCB_AllBulletin)",
            "上交所/深交所公开披露索引"
        ]
    }
    
    # === 输出 ===
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"  研林 · 今日公司公告 ({today})")
        print(f"{'='*50}")
        print(f"  数据源: {len(result['data_sources'])}个")
        print(f"  原始{result['total_raw']}条 → 筛选{result['total_filtered']}条重要公告\n")
        
        for i, f in enumerate(result['filings'][:8], 1):
            stars = "⭐" * f['importance']
            arrow = "🟢" if f['direction'] == 'positive' else ("🔴" if f['direction'] == 'negative' else "⚪")
            tag = f"[{f['sector']}]" if f['sector'] and f['sector'] != '综合' else ""
            cat_tag = f"({f.get('category','')})" if f.get('category') else ""
            print(f"  {i}. {stars} {arrow} {tag} {cat_tag}")
            print(f"     {f['company']}: {f['event'][:65]}")
            print()

if __name__ == '__main__':
    main()
