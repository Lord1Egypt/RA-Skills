#!/usr/bin/env python3
"""
新浪每日新闻抓取脚本
数据源：新浪财经 7x24 实时新闻流
URL: https://finance.sina.com.cn/7x24/?tag=0
"""
import re
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today_str = now.strftime("%Y-%m-%d")
yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")

# 新闻分类关键词
CATEGORIES = {
    "国际政治军事": ["伊朗", "美国", "伊朗", "阿拉伯", "以色列", "北约", "俄罗斯", "乌克兰",
                     "刚果", "埃博拉", "世卫", "武装", "军事", "外交", "总统", "议会",
                     "阿根廷", "南南合作", "谭德塞", "黎巴嫩", "德黑兰", "印度洋",
                     "阿富汗", "巴基斯坦", "欧洲", "朝鲜", "韩国", "日本", "中东"],
    "中国政治外交": ["中国", "国务院", "外交部", "新华社", "香港", "澳门", "台湾",
                     "全国人大", "政协", "中央", "部委", "一带一路", "东盟", "金砖"],
    "中国财经股市": ["A股", "沪指", "深成指", "创业板", "北向资金", "涨停", "跌停",
                     "央行", "利率", "LPR", "降准", "加息", "非农", "美联储",
                     "楼面价", "地王", "房价", "房地产", "保险", "基金", "易方达",
                     "融资", "IPO", "上市", "科创板", "溢价", "央企", "保利", "华润",
                     "深圳", "南沙", "前海", "北京", "丰台区", "航空航天", "46亿元",
                     "南非", "限电", "电力"],
    "科技与AI": ["AI", "大模型", "人工智能", "芯片", "半导体", "算力", "字节跳动",
                 "豆包", "华为", "京东方", "BOE", "vivo", "创维", "合成细胞",
                 "深圳先进院", "Nature", "生物", "万兴", "AIGC", "智能",
                 "KAMAGRA", "机器人", "如厕", "流水线"],
    "社会热点": ["交通事故", "死亡", "受伤", "立案", "警方", "食品安全", "检测",
                 "驴肉", "马肉", "西地那非", "KAMAGRA", "爱达·魔都号", "邮轮",
                 "天气", "雷雨", "龙卷", "预警", "橙色"],
    "产业与制造": ["汽车", "造车", "滚装船", "飞机", "部件", "武昌造船",
                   "空轨", "轨道交通", "金华", "通号", "智能调度",
                   "能建", "燃机", "科特迪瓦", "松贡", "电站"],
}

def classify(title, content):
    text = title + content
    for cat, keywords in CATEGORIES.items():
        if any(kw in text for kw in keywords):
            return cat
    return "其他"

def parse_news(text):
    """解析新闻文本，提取时间、标题、内容、来源、阅读量"""
    items = []
    # 匹配格式：时间\n[【标题】](链接)\n内容\n阅读量 阅读
    pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2})\n\n'           # 时间
        r'\[?【?([^】\]]+)】?\]?\s*\(.*?\)?'   # 标题（可能带【】或无括号）
        r'([\s\S]*?)'                          # 内容
        r'(\d+(?:\.\d+)?万)\s*阅读'            # 阅读量
    )
    
    for m in pattern.finditer(text):
        time_str = m.group(1)
        title = m.group(2).strip()
        content = m.group(3).strip()
        views = m.group(4)
        
        # 提取来源（括号内的媒体名）
        source = ""
        src_match = re.search(r'（([^）]+)）$', content)
        if src_match:
            source = src_match.group(1)
            content = content[:src_match.start()].strip()
        
        items.append({
            "time": time_str,
            "title": title,
            "content": content,
            "source": source,
            "views": views,
        })
    
    return items

def generate_report(items):
    """生成分类报告"""
    # 按类别分组
    grouped = {}
    for item in items:
        cat = classify(item["title"], item["content"])
        grouped.setdefault(cat, []).append(item)
    
    report_lines = []
    report_lines.append(f"# 📰 新浪每日新闻日报 — {today_str}")
    report_lines.append(f"> 数据源：新浪财经 7×24 实时新闻（{today_str} 00:00 - {now.strftime('%H:%M')}）")
    report_lines.append(f"> 共 {len(items)} 条新闻\n")
    
    # 按固定顺序输出
    cat_order = ["国际政治军事", "中国政治外交", "中国财经股市", "科技与AI", "产业与制造", "社会热点", "其他"]
    
    idx = 1
    for cat in cat_order:
        cat_items = grouped.get(cat, [])
        if not cat_items:
            continue
        report_lines.append(f"## {roman_numeral(idx)}、{cat}（{len(cat_items)}条）\n")
        for item in cat_items:
            source_tag = f" | {item['source']}" if item['source'] else ""
            report_lines.append(
                f"- **[{item['time']}] {item['title']}**{source_tag} | 阅读 {item['views']}"
            )
            if item['content']:
                report_lines.append(f"  {item['content'][:120]}")
        report_lines.append("")
        idx += 1
    
    # 剩余未排序的类别
    for cat, cat_items in grouped.items():
        if cat in cat_order:
            continue
        report_lines.append(f"## {roman_numeral(idx)}、{cat}（{len(cat_items)}条）\n")
        for item in cat_items:
            source_tag = f" | {item['source']}" if item['source'] else ""
            report_lines.append(
                f"- **[{item['time']}] {item['title']}**{source_tag} | 阅读 {item['views']}"
            )
            if item['content']:
                report_lines.append(f"  {item['content'][:120]}")
        report_lines.append("")
        idx += 1
    
    report_lines.append("---")
    report_lines.append(f"*数据来源：新浪财经 7×24 | 抓取时间：{now.strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(report_lines)

def roman_numeral(n):
    numerals = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    return numerals[n - 1] if n <= len(numerals) else str(n)


if __name__ == "__main__":
    import sys
    
    # 如果传入了文本，直接解析；否则提示调用方式
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        # 读取 stdin
        text = sys.stdin.read()
    
    if not text or len(text) < 100:
        print("ERROR: 新闻文本太短，可能抓取失败")
        sys.exit(1)
    
    items = parse_news(text)
    if not items:
        print("ERROR: 未解析到任何新闻条目")
        sys.exit(1)
    
    report = generate_report(items)
    print(report)
