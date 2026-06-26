#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
silver-daily: 银发每日头条 HTML 报告生成器
Usage:
  python generate_report.py [--output OUTPUT_FILE] [--data JSON_FILE]
"""

import json
import argparse
import os
from datetime import datetime

# ─── 默认演示数据 ──────────────────────────────────────────────
DEMO_DATA = {
    "date": datetime.now().strftime("%Y年%m月%d日"),
    "issue": "001",
    "top_story": {
        "title": "国务院常务会议：进一步释放银发消费需求，打造消费新场景新业态",
        "summary": "2026年2月24日，国务院常务会议明确要求发挥消费补贴政策牵引作用，将银发经济纳入扩内需核心战略。会议提出要推动老年用品、旅居养老、养老金融三大方向协同发力。",
        "url": "https://www.gov.cn/zhengce/202602/content_7059238.htm",
        "source": "中国政府网",
        "date": "2026-02-24"
    },
    "stats": [
        {"num": "3.2亿", "label": "60岁以上老年人口"},
        {"num": "30万亿", "label": "2026年银发经济规模"},
        {"num": "20%", "label": "老龄人口占总人口比"},
        {"num": "600+", "label": "今年银发研究论文数"}
    ],
    "sections": [
        {
            "id": "policy", "icon": "🏛️", "name": "政策解读",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "2026政府工作报告深度解读：银发经济七大重点",
                    "source": "知乎·AgeClub", "time": "3月6日", "tag": "两会",
                    "url": "https://zhuanlan.zhihu.com/p/2013178662007112635",
                    "summary": "报告提出制定推进银发经济高质量发展的措施，完善老年用品、养老金融、旅居养老等支持政策。"
                },
                {
                    "rank": 2, "featured": False,
                    "title": "长期护理保险服务管理文书（2026年版）正式印发",
                    "source": "国家医保局", "time": "12月1日", "tag": "长护险",
                    "url": "https://www.nhsa.gov.cn/art/2025/12/1/art_104_18899.html",
                    "summary": "国家医保局更新长护险服务管理文书标准，试点城市扩展至全国49个。"
                }
            ]
        },
        {
            "id": "consume", "icon": "🛍️", "name": "银发消费",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "银发经济爆发！2026年中国市场趋势全解读",
                    "source": "AgeClub", "time": "1月28日", "tag": "市场",
                    "url": "https://ageclub.net/article-detail/8165",
                    "summary": "2026年银发消费呈现悦己化、品质化、场景化三大趋势，旅居、康养、智能硬件成三大爆发赛道。"
                }
            ]
        },
        {
            "id": "finance", "icon": "💰", "name": "老年金融",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "养老金融多维突破：个人养老金账户扩围，商业养老险迎政策窗口",
                    "source": "中国消费者报", "time": "3月18日", "tag": "养老金",
                    "url": "https://finance.sina.com.cn/jjxw/2026-03-18/doc-inhrizpe3512648.shtml",
                    "summary": "银发金融资管规模预计突破5万亿元，商业银行加速推出养老专属理财产品。"
                }
            ]
        },
        {
            "id": "tech", "icon": "🤖", "name": "银发科技",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "养老机器人加速破局：情感陪护机器人订单翻倍增长",
                    "source": "央视网", "time": "3月5日", "tag": "机器人",
                    "url": "https://business.cctv.cn/2026/03/05/ARTIkoUbodguruWPA1dGPOi4260305.shtml",
                    "summary": "春晚亮相后，情感陪伴、生活辅助、健康监测三大功能成养老机构采购首选。"
                }
            ]
        },
        {
            "id": "health", "icon": "🏥", "name": "医疗健康",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "3.2亿老人老有所依：医养结合加速，社区嵌入式养老服务全面铺开",
                    "source": "腾讯新闻", "time": "3月12日", "tag": "医养结合",
                    "url": "https://news.qq.com/rain/a/20260312A08HWN00",
                    "summary": "15分钟养老服务圈成各地核心建设指标，覆盖率目标2026年底达80%。"
                }
            ]
        },
        {
            "id": "culture", "icon": "🎭", "name": "银发文娱",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "银发旅游升温，旅居养老纳入国家政策支持",
                    "source": "黑龙江省文旅厅", "time": "3月16日", "tag": "旅居养老",
                    "url": "https://wlt.hlj.gov.cn/wlt/c115793/202603/c00_31924109.shtml",
                    "summary": "旅游+养老融合市场规模预计年内突破5000亿元，异地候鸟式旅居模式渐成规模。"
                }
            ]
        },
        {
            "id": "home", "icon": "🏠", "name": "居家养老",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "AI+养老解锁新机遇：智能居家照护系统进入千家万户",
                    "source": "中国日报", "time": "12月17日", "tag": "智慧居家",
                    "url": "https://cn.chinadaily.com.cn/a/202512/17/WS6941f0a3a310942cc4996fc9.html",
                    "summary": "2026年适老化改造补贴户数较去年增长40%，跌倒检测准确率超95%。"
                }
            ]
        },
        {
            "id": "employ", "icon": "💼", "name": "银发就业",
            "news": [
                {
                    "rank": 1, "featured": True,
                    "title": "面向十五五：激发银发经济新动能，稳妥推进延迟退休是重要路径",
                    "source": "人民论坛", "time": "12月2日", "tag": "延迟退休",
                    "url": "https://paper.people.com.cn/rmlt/pc/content/202512/02/content_30125637.html",
                    "summary": "积极开发老年人力资源，退而不休的银发经济参与者正成为万亿市场的创造者与消费者。"
                }
            ]
        }
    ]
}


def render_news_card(news):
    featured_class = " featured" if news.get("featured") else ""
    rank_class = " top" if news.get("rank") == 1 else ""
    summary_html = f'<div class="news-summary">{news["summary"]}</div>' if news.get("summary") else ""
    return f'''
    <a class="news-card{featured_class}" href="{news["url"]}" target="_blank">
      <div class="news-rank{rank_class}">{news["rank"]}</div>
      <div class="news-body">
        <div class="news-title">{news["title"]}</div>
        <div class="news-meta">
          <span class="news-source">{news["source"]}</span>
          <span class="news-time">{news["time"]}</span>
          <span class="news-tag">{news["tag"]}</span>
        </div>
        {summary_html}
      </div>
    </a>'''


def render_section(section):
    news_html = "\n".join(render_news_card(n) for n in section["news"])
    count = len(section["news"])
    return f'''
  <div class="section-head">
    <div class="section-icon">{section["icon"]}</div>
    <div class="section-name">{section["name"]}</div>
    <div class="section-line"></div>
    <div class="section-count">{count} 条</div>
  </div>
  <div class="news-list">
    {news_html}
  </div>'''


def render_stats(stats):
    cards = ""
    for s in stats:
        cards += f'''
    <div class="stat-card">
      <div class="stat-num">{s["num"]}</div>
      <div class="stat-label">{s["label"]}</div>
    </div>'''
    return f'<div class="stats-row">{cards}\n  </div>'


def generate_html(data):
    top = data["top_story"]
    sections_html = "\n".join(render_section(s) for s in data["sections"])
    stats_html = render_stats(data["stats"])

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>银发每日头条 · {data["date"]}</title>
  <style>
    :root {{
      --gold: #c8922a;
      --gold-light: #f0d080;
      --silver: #8a9bb0;
      --ink: #1a1a2e;
      --bg: #faf8f5;
      --card-bg: #ffffff;
      --border: #e8e0d0;
      --muted: #7a7a8a;
      --tag-bg: #f5f0e8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'PingFang SC','Microsoft YaHei',serif; background: var(--bg); color: var(--ink); line-height: 1.7; }}
    .header {{ background: linear-gradient(135deg,#1a1a2e 0%,#2d2d4e 60%,#3a2a1a 100%); padding: 28px 24px 22px; text-align: center; }}
    .header-logo {{ font-size: 13px; color: var(--gold-light); letter-spacing: 4px; opacity: .8; margin-bottom: 6px; }}
    .header-title {{ font-size: 30px; font-weight: 700; color: #fff; letter-spacing: 3px; }}
    .header-title span {{ color: var(--gold); }}
    .header-date {{ margin-top: 8px; font-size: 13px; color: rgba(255,255,255,.55); }}
    .header-line {{ width: 60px; height: 2px; background: linear-gradient(90deg,transparent,var(--gold),transparent); margin: 12px auto 0; }}
    .container {{ max-width: 860px; margin: 0 auto; padding: 20px 16px 40px; }}
    .top-story {{ background: linear-gradient(135deg,#1a1a2e,#2d2640); border-radius: 10px; padding: 20px; margin: 18px 0; position: relative; }}
    .top-story::before {{ content: '头条'; position: absolute; top: -2px; right: 14px; font-size: 11px; background: var(--gold); color: #fff; padding: 3px 10px 4px; border-radius: 0 0 6px 6px; letter-spacing: 2px; }}
    .top-story-title {{ font-size: 18px; font-weight: 700; color: #fff; line-height: 1.5; margin-bottom: 10px; }}
    .top-story-summary {{ font-size: 13px; color: rgba(255,255,255,.65); line-height: 1.7; }}
    .top-story-link {{ display: inline-flex; align-items: center; gap: 5px; margin-top: 14px; font-size: 13px; color: var(--gold); text-decoration: none; border: 1px solid rgba(200,146,42,.4); padding: 5px 14px; border-radius: 20px; }}
    .top-story-link:hover {{ background: rgba(200,146,42,.15); }}
    .stats-row {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin: 16px 0 28px; }}
    .stat-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px 12px; text-align: center; }}
    .stat-num {{ font-size: 22px; font-weight: 800; color: var(--gold); line-height: 1.2; }}
    .stat-label {{ font-size: 11px; color: var(--muted); margin-top: 3px; }}
    .section-head {{ display: flex; align-items: center; gap: 10px; margin: 28px 0 14px; }}
    .section-icon {{ font-size: 22px; line-height: 1; }}
    .section-name {{ font-size: 17px; font-weight: 700; letter-spacing: 1px; }}
    .section-line {{ flex: 1; height: 1px; background: linear-gradient(90deg,var(--border),transparent); }}
    .section-count {{ font-size: 11px; color: var(--muted); background: var(--tag-bg); padding: 2px 8px; border-radius: 10px; }}
    .news-list {{ display: flex; flex-direction: column; gap: 10px; }}
    .news-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; display: flex; gap: 12px; text-decoration: none; color: inherit; transition: box-shadow .2s,transform .2s; }}
    .news-card:hover {{ box-shadow: 0 4px 16px rgba(0,0,0,.08); transform: translateY(-1px); }}
    .news-card.featured {{ border-left: 3px solid var(--gold); background: linear-gradient(to right,#fffdf7,#fff); }}
    .news-rank {{ font-size: 18px; font-weight: 800; color: var(--gold-light); min-width: 26px; text-align: center; line-height: 1.4; }}
    .news-rank.top {{ color: var(--gold); }}
    .news-body {{ flex: 1; min-width: 0; }}
    .news-title {{ font-size: 15px; font-weight: 600; line-height: 1.5; margin-bottom: 5px; }}
    .news-card:hover .news-title {{ color: #8a5a10; }}
    .news-meta {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    .news-source {{ font-size: 12px; color: var(--muted); }}
    .news-source::before {{ content: '📰 '; }}
    .news-time {{ font-size: 12px; color: #b0a890; }}
    .news-tag {{ font-size: 11px; background: var(--tag-bg); color: var(--gold); padding: 1px 7px; border-radius: 10px; border: 1px solid rgba(200,146,42,.2); }}
    .news-summary {{ font-size: 13px; color: #555; margin-top: 5px; line-height: 1.6; }}
    .footer {{ text-align: center; padding: 24px 16px; background: linear-gradient(180deg,var(--bg),#f0ece4); border-top: 1px solid var(--border); font-size: 12px; color: var(--muted); }}
    .footer-brand {{ font-size: 15px; font-weight: 700; color: var(--gold); letter-spacing: 2px; margin-bottom: 6px; }}
    @media (max-width:600px) {{ .stats-row {{ grid-template-columns: repeat(2,1fr); }} .header-title {{ font-size: 22px; }} }}
  </style>
</head>
<body>
<div class="header">
  <div class="header-logo">SILVER AGE DAILY · 银发每日头条</div>
  <div class="header-title">银发<span>每日</span>头条</div>
  <div class="header-date">{data["date"]} · 第 {data["issue"]} 期</div>
  <div class="header-line"></div>
</div>
<div class="container">
  {stats_html}
  <div class="top-story">
    <div class="top-story-title">{top["title"]}</div>
    <div class="top-story-summary">{top["summary"]}</div>
    <a href="{top["url"]}" class="top-story-link" target="_blank">查看全文 →</a>
  </div>
  {sections_html}
</div>
<div class="footer">
  <div class="footer-brand">银发每日头条</div>
  <div>聚焦银发经济 · 关注亿万老年人的美好生活</div>
  <div style="margin-top:8px;color:#b0a890;">内容来源于公开新闻资讯，仅供参考 · Silver Age Daily · 第{data["issue"]}期</div>
</div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="银发每日头条报告生成器")
    parser.add_argument("--output", default=None, help="输出文件路径")
    parser.add_argument("--data", default=None, help="新闻数据 JSON 文件路径")
    args = parser.parse_args()

    # 加载数据
    if args.data and os.path.exists(args.data):
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = DEMO_DATA
        data["date"] = datetime.now().strftime("%Y年%m月%d日")

    # 生成 HTML
    html = generate_html(data)

    # 确定输出路径
    if args.output:
        out_path = args.output
    else:
        os.makedirs("output", exist_ok=True)
        out_path = f"output/silver-daily-{datetime.now().strftime('%Y%m%d')}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] 银发每日头条已生成：{out_path}")
    print(f"日期：{data['date']}  · 第 {data['issue']} 期")
    total = sum(len(s["news"]) for s in data["sections"])
    print(f"共 {len(data['sections'])} 个板块，{total} 条资讯")


if __name__ == "__main__":
    main()
