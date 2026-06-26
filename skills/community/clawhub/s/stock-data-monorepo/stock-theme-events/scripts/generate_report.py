#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本 - 根据题材聚类和新闻数据生成 Markdown 报告
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List
import os


def load_template(template_path: str = None) -> str:
    """加载报告模板"""
    if template_path and os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # 默认模板
    return """# A 股题材 - 事件关联分析报告

**数据日期**：{{date}}
**统计周期**：近 10 个交易日
**新闻范围**：近{{news_days}}天
**样本股票**：涨幅前 30 只（排除 ST）

---

## 一、主流炒作题材方向

| 排名 | 题材方向 | 涉及股票数 | 代表股票 |
|------|----------|------------|----------|
{{theme_table}}

---

## 二、题材 - 事件对应分析

{{theme_details}}

---

## 三、总结

- 当前市场主要炒作方向：{{top_themes_summary}}
- 新闻事件驱动明显：{{news_driver_summary}}
- 风险提示：题材轮动较快，注意追高风险

---

**报告生成时间**：{{generate_time}}
**数据来源**：同花顺、金十数据、东方财富
"""


def get_stock_names(stock_codes: List[str]) -> str:
    """获取股票名称（简化版，实际应用中可调用 API 获取）"""
    # 这里简化处理，只显示代码
    # 实际应用中可以调用 tushare/akshare 获取股票名称
    return "、".join(stock_codes[:5]) + ("..." if len(stock_codes) > 5 else "")


def generate_theme_table(top_themes: List[Dict]) -> str:
    """生成题材表格"""
    rows = []
    for i, theme_data in enumerate(top_themes, 1):
        theme = theme_data["theme"]
        count = theme_data["count"]
        stocks = theme_data.get("stocks", [])
        representative = get_stock_names(stocks)
        rows.append(f"| {i} | {theme} | {count} | {representative} |")
    
    return "\n".join(rows)


def generate_theme_details(top_themes: List[Dict], news_data: Dict) -> str:
    """生成题材详情"""
    sections = []
    
    for i, theme_data in enumerate(top_themes, 1):
        theme = theme_data["theme"]
        stocks = theme_data.get("stocks", [])
        
        # 获取对应新闻
        theme_news = []
        if news_data and "themes" in news_data:
            theme_news = news_data["themes"].get(theme, {}).get("news", [])
        
        # 构建章节
        section = f"""### {i}. {theme}（{len(stocks)} 只股票）

**涉及股票**：{get_stock_names(stocks)}

**对应新闻事件**：

"""
        
        if theme_news:
            for j, news in enumerate(theme_news, 1):
                title = news.get("title", "无标题")
                publish_time = news.get("publish_time", "未知时间")
                source = news.get("source", "未知来源")
                summary = news.get("content", news.get("summary", ""))
                url = news.get("url", "#")
                
                # 截断摘要
                if len(summary) > 150:
                    summary = summary[:150] + "..."
                
                section += f"""{j}. **[{title}]({url})** ({publish_time})
   - 来源：{source}
   - 摘要：{summary}

"""
        else:
            section += "*暂无直接相关的新闻事件，可能是资金驱动或技术面炒作*\n\n"
        
        sections.append(section)
    
    return "\n".join(sections)


def generate_report(themes_path: str, news_path: str, output_path: str,
                    template_path: str = None, news_days: int = 15):
    """
    生成 Markdown 报告
    
    Args:
        themes_path: 题材聚类 JSON 文件
        news_path: 新闻数据 JSON 文件
        output_path: 输出 Markdown 路径
        template_path: 模板文件路径
        news_days: 新闻搜索天数
    """
    # 加载数据
    with open(themes_path, 'r', encoding='utf-8') as f:
        themes_data = json.load(f)
    
    news_data = None
    if news_path and os.path.exists(news_path):
        with open(news_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
    
    # 加载模板
    template = load_template(template_path)
    
    # 准备数据
    top_themes = themes_data.get("top_themes", [])
    
    # 替换模板变量
    report = template
    report = report.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    report = report.replace("{{news_days}}", str(news_days))
    report = report.replace("{{theme_table}}", generate_theme_table(top_themes))
    report = report.replace("{{theme_details}}", generate_theme_details(top_themes, news_data))
    report = report.replace("{{top_themes_summary}}", "、".join([t["theme"] for t in top_themes[:3]]))
    report = report.replace("{{news_driver_summary}}", "政策面、消息面共振" if news_data else "以资金驱动为主")
    report = report.replace("{{generate_time}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # 保存报告
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已生成：{output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='报告生成脚本')
    parser.add_argument('--themes', required=True, help='题材聚类 JSON 文件')
    parser.add_argument('--news', help='新闻数据 JSON 文件')
    parser.add_argument('--output', required=True, help='输出 Markdown 路径')
    parser.add_argument('--template', help='模板文件路径')
    parser.add_argument('--news-days', type=int, default=15, help='新闻搜索天数')
    
    args = parser.parse_args()
    
    generate_report(args.themes, args.news, args.output, args.template, args.news_days)


if __name__ == '__main__':
    main()
