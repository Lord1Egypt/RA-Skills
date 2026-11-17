#!/usr/bin/env python3
"""
研林 · 产业投研日报生成器
将采集数据合成为完整券商级日报（Markdown格式）
"""
import json, sys, os, time, datetime

def load_json(path):
    """加载JSON文件"""
    if not os.path.exists(path):
        print(f"⚠️ 文件不存在: {path}", file=sys.stderr)
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(market_data, macro_data, news_data, filings_data, output_dir, report_date):
    """生成完整日报"""
    date_str = report_date or time.strftime("%Y-%m-%d")
    weekday_map = ["周一","周二","周三","周四","周五","周六","周日"]
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        weekday_str = weekday_map[dt.weekday()]
    except:
        weekday_str = ""
    
    lines = []
    
    # ===== 标题 =====
    lines.append(f"# 📊 产业投研日报 | {date_str}（{weekday_str}）")
    lines.append("")
    lines.append("> **报告周期：** 基于最新交易日数据复盘")
    lines.append("> **风格：** 券商投研团队标准 | **覆盖市场：** A股、港股、美股")
    lines.append("> **核心原则：** 去新闻堆砌、只保留边际增量、所有判断可归因、结论可落地")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ===== 板块一：今日核心投研结论 =====
    lines.append("## 一、【今日核心投研结论】")
    lines.append("")
    
    # 从新闻和行情数据中提取TOP结论
    indices = market_data.get('indices', {})
    sectors = market_data.get('sectors', {})
    events = news_data.get('events', [])
    
    # 查找涨幅最大板块
    top_sector = ""
    for s in sectors.get('top', [])[:1]:
        top_sector = f"{s['name']}（{s['change_pct']:+.2f}%）"
    
    # 生成结论
    high_impact_events = [e for e in events if e.get('importance',0) >= 4][:3]
    
    if high_impact_events:
        for i, evt in enumerate(high_impact_events[:2]):
            sectors_str = "/".join(evt.get('related_sectors', ['综合']))
            lines.append(f"### 🎯 结论{i+1}：{evt['title'][:50]}")
            lines.append(f"**核心催化：** {evt['title']}")
            lines.append(f"**传导时效：** 需结合具体事件进一步分析")
            lines.append(f"**机会定位：** 关注{sectors_str}赛道相关标的")
            lines.append("")
    
    if top_sector:
        lines.append(f"**市场亮点：** {top_sector} 领涨全市场，值得重点关注")
        lines.append("")
    
    # ===== 板块二：宏观&流动性观察 =====
    lines.append("## 二、【宏观&流动性观察】")
    lines.append("")
    
    dom = macro_data.get('domestic', {})
    ovr = macro_data.get('overseas', {})
    
    lines.append("| 指标 | 当前值 | 边际变化 | 影响解读 |")
    lines.append("|------|--------|---------|---------|")
    if dom:
        b = dom.get('bond_10y', {})
        lines.append(f"| 10Y国债收益率 | {b.get('value','-')}% | {b.get('weekly_change',0):+.0f}bp | {b.get('interpretation','-')} |")
        lines.append(f"| 央行OMO | {dom.get('omo_rate',{}).get('value','-')}% | 持平 | {dom.get('omo_rate',{}).get('note','-')} |")
    if ovr:
        lines.append(f"| 美元指数 | {ovr.get('dollar_index',{}).get('value','-')} | {ovr.get('dollar_index',{}).get('change',0):+.1f} | {ovr.get('dollar_index',{}).get('trend','-')} |")
        lines.append(f"| 美国10Y | {ovr.get('us_10y',{}).get('value','-')}% | {ovr.get('us_10y',{}).get('change',0):+d}bp | {ovr.get('us_10y',{}).get('trend','-')} |")
        lines.append(f"| 黄金 | ${ovr.get('gold',{}).get('value','-')}/oz | - | {ovr.get('gold',{}).get('trend','-')} |")
        lines.append(f"| 布油 | ${ovr.get('brent_oil',{}).get('value','-')}/bbl | - | {ovr.get('brent_oil',{}).get('trend','-')} |")
    lines.append("")
    
    # ===== 板块三：行业产业动态深度解读 =====
    lines.append("## 三、【行业产业动态深度解读】")
    lines.append("")
    
    if events:
        for evt in events[:4]:
            stars = "⭐" * evt.get('importance', 3)
            sectors_str = "/".join(evt.get('related_sectors', ['综合']))
            lines.append(f"### {stars} {evt['title']}")
            lines.append("")
            lines.append(f"**事件内容：** {evt['title']}")
            lines.append(f"**关联赛道：** {sectors_str}")
            lines.append(f"**边际变化：** 需结合具体信息进一步分析")
            lines.append(f"**传导时效：** 待评估")
            lines.append(f"**预期差：** 待评估")
            lines.append("")
    else:
        lines.append("*今日暂无高优先级产业事件。*")
        lines.append("")
    
    # ===== 板块四：重点公司公告速览 =====
    lines.append("## 四、【重点公司公告速览】")
    lines.append("")
    
    filings = filings_data.get('filings', [])
    if filings:
        lines.append("| 公司 | 公告内容 | 核心影响 | 投研评价 |")
        lines.append("|------|---------|---------|---------|")
        for f in filings:
            lines.append(f"| {f.get('company','-')} | {f.get('event','-')[:20]} | {f.get('impact','-')[:20]} | {f.get('rating','-')} |")
    else:
        lines.append("*今日无重大影响公告。*")
    lines.append("")
    
    # ===== 板块五：市场情绪&资金复盘 =====
    lines.append("## 五、【市场情绪&资金复盘】")
    lines.append("")
    
    if indices:
        lines.append("| 指数 | 收盘 | 涨跌幅 | 短期趋势 |")
        lines.append("|------|------|--------|---------|")
        for code, idx in indices.items():
            arrow = "🔴" if idx.get('change_pct',0) < 0 else "🟢"
            trend = "偏弱" if idx.get('change_pct',0) < -0.3 else ("偏强" if idx.get('change_pct',0) > 0.3 else "震荡")
            lines.append(f"| {idx.get('name','-')} | {idx.get('close',0):.2f} | {arrow} {idx.get('change_pct',0):+.2f}% | {trend} |")
    lines.append("")
    
    # 板块涨幅
    if sectors:
        lines.append("**行业涨幅TOP5：**")
        for s in sectors.get('top', [])[:5]:
            lines.append(f"- {s.get('name','-')} {s.get('change_pct',0):+.2f}%")
    lines.append("")
    
    # ===== 板块六：明日前瞻&跟踪清单 =====
    lines.append("## 六、【明日前瞻&跟踪清单】")
    lines.append("")
    lines.append("| 时间 | 事件 | 重要度 | 关注标的 |")
    lines.append("|------|------|--------|---------|")
    lines.append(f"| {date_str} | 关注当日市场走势 | ⭐⭐⭐ | 全市场 |")
    lines.append("")
    lines.append("*需结合最新经济日历进一步补充。*")
    lines.append("")
    
    # ===== 板块七：核心风险提示 =====
    lines.append("## 七、【核心风险提示】")
    lines.append("")
    lines.append("| 风险 | 概率-影响 | 核心逻辑 | 应对 |")
    lines.append("|------|----------|---------|------|")
    lines.append("| 🔴 外部市场波动 | 中·高 | 地缘政治风险 | 关注VIX、台积电ADR |")
    lines.append("| 🟡 业绩兑现风险 | 中·中 | Q2业绩预告密集期 | 分散配置，避免追高 |")
    lines.append("| 🟡 情绪退潮风险 | 中·中 | 短期涨幅过高板块有回调压力 | 控制仓位 |")
    lines.append("")
    
    # ===== 免责声明 =====
    lines.append("---")
    lines.append(f"> 📝 **免责声明：** 本报告由研林智能体基于公开信息和数据分析自动生成，仅供研究参考，不构成投资建议。")
    lines.append("")

    # ===== 写入文件 =====
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"研林产业投研日报_{date_str}.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 日报已生成: {output_path}")
    print(f"   共 {len(lines)} 行，{sum(len(l) for l in lines)} 字符")
    
    return output_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description="研林·产业投研日报生成器")
    parser.add_argument('--market-data', default='', help='市场数据JSON路径')
    parser.add_argument('--macro-data', default='', help='宏观数据JSON路径')
    parser.add_argument('--news-data', default='', help='新闻数据JSON路径')
    parser.add_argument('--filings-data', default='', help='公告数据JSON路径')
    parser.add_argument('--output', default='./output', help='输出目录')
    parser.add_argument('--date', default='', help='日期(YYYY-MM-DD)')
    parser.add_argument('--standalone', action='store_true', help='独立运行模式（自动采集所有数据）')
    
    args = parser.parse_args()
    
    if args.standalone:
        # 独立运行模式：自动采集数据
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../yanlin-market-data/scripts'))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../yanlin-macro-data/scripts'))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../yanlin-news-filter/scripts'))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../yanlin-company-filings/scripts'))
        
        # 采集市场数据
        import fetch_market_data
        market_data = json.loads(fetch_market_data.main_internal())
        
        # 采集宏观数据
        import fetch_macro_data
        macro_data = json.loads(fetch_macro_data.main_internal())
        
        # 采集新闻
        import filter_news
        news_data = json.loads(filter_news.main_internal())
        
        # 采集公告（空数据）
        filings_data = {"date": args.date or time.strftime("%Y-%m-%d"), "filings": []}
    else:
        market_data = load_json(args.market_data)
        macro_data = load_json(args.macro_data)
        news_data = load_json(args.news_data)
        filings_data = load_json(args.filings_data)
    
    output_path = generate_report(market_data, macro_data, news_data, filings_data, args.output, args.date)
    print(json.dumps({"status": "ok", "path": output_path}))

if __name__ == '__main__':
    main()
