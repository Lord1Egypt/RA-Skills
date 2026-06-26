#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report.py
调用 DeepSeek API，基于抓取的数据生成大白话体检报告
"""

import json
import logging
import os
import requests
from datetime import datetime


DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

STYLE_PROMPTS = {
    "casual": """你是一个接地气的股票分析博主，专门帮普通散户看懂股票。
风格要求：
- 用大白话，把数据翻译成人话，不要堆砌专业术语
- 带一点幽默感，但不要哗众取宠
- 直接说结论，不绕弯子
- 对风险要直白提示，不要美化
""",
    "analysis": """你是专业的股票分析师，风格严谨理性。
风格要求：
- 客观陈述数据，给出逻辑清晰的分析
- 结合行业背景解读指标
- 明确列出多空两方观点
"""
}


def _format_money(amount: float, unit: str = "元") -> str:
    """格式化金额：亿/万"""
    if amount is None:
        return "N/A"
    if abs(amount) >= 1e8:
        return f"{amount/1e8:.2f}亿{unit}"
    elif abs(amount) >= 1e4:
        return f"{amount/1e4:.2f}万{unit}"
    else:
        return f"{amount:.2f}{unit}"


def _pct(val, suffix="%") -> str:
    if val is None:
        return "N/A"
    sign = "▲" if val > 0 else ("▼" if val < 0 else "")
    return f"{sign}{abs(val):.2f}{suffix}"


def build_data_summary(data: dict) -> str:
    """把抓取的数据整理成结构化文本，供 LLM 分析"""
    stock = data.get("stock", {})
    basic = data.get("basic", {})
    quote = data.get("quote", {})
    history = data.get("history", {})
    fin = data.get("financials", {})
    ff = data.get("fund_flow", {})
    news = data.get("news", [])

    lines = [
        f"【股票基本信息】",
        f"名称：{basic.get('name') or stock.get('name')}",
        f"代码：{stock.get('full')}",
        f"行业：{basic.get('industry', 'N/A')}",
        f"上市时间：{basic.get('list_date', 'N/A')}",
        f"总市值：{_format_money(quote.get('market_cap'))}",
        "",
        f"【今日行情】",
        f"当前价：{quote.get('price', 'N/A')} 元",
        f"涨跌幅：{_pct(quote.get('change_pct'))}",
        f"成交额：{_format_money(quote.get('amount'))}",
        f"换手率：{quote.get('turnover', 'N/A')}%",
        f"今日最高：{quote.get('high', 'N/A')}，最低：{quote.get('low', 'N/A')}",
        "",
        f"【技术面】",
        f"近1周涨跌：{_pct(history.get('week_change'))}",
        f"近1月涨跌：{_pct(history.get('month_change'))}",
        f"MA5（5日均线）：{history.get('ma5', 'N/A')}",
        f"MA20（20日均线）：{history.get('ma20', 'N/A')}",
        f"MA60（60日均线）：{history.get('ma60', 'N/A')}",
        f"近20日最高：{history.get('recent_high', 'N/A')}，最低：{history.get('recent_low', 'N/A')}",
        "",
        f"【估值】",
        f"动态PE：{quote.get('pe_dynamic', 'N/A')} 倍",
        f"市净率PB：{quote.get('pb', 'N/A')} 倍",
        "",
    ]

    if fin:
        lines += [
            f"【财务健康（{fin.get('report_date', '最新')}）】",
            f"ROE净资产收益率：{fin.get('roe', 'N/A')}%",
            f"销售毛利率：{fin.get('gross_margin', 'N/A')}%",
            f"净利率：{fin.get('net_margin', 'N/A')}%",
            f"资产负债率：{fin.get('debt_ratio', 'N/A')}%",
            f"营收增长率：{fin.get('revenue_growth', 'N/A')}%",
            f"净利润增长率：{fin.get('profit_growth', 'N/A')}%",
            f"每股收益EPS：{fin.get('eps', 'N/A')} 元",
            "",
        ]

    if ff:
        lines += [
            f"【主力资金（{ff.get('date', '今日')}）】",
            f"主力净流入：{_format_money(ff.get('main_net'))}（占比{ff.get('main_net_pct', 'N/A')}%）",
            f"超大单净流入：{_format_money(ff.get('super_net'))}",
            f"大单净流入：{_format_money(ff.get('big_net'))}",
            f"小单净流入：{_format_money(ff.get('small_net'))}",
            "",
        ]

    if news:
        lines.append("【近期新闻】")
        for i, n in enumerate(news, 1):
            lines.append(f"{i}. [{n.get('date','')}] {n.get('title','')}（来源：{n.get('source','')}）")
        lines.append("")

    return "\n".join(lines)


def build_prompt(data: dict, style: str = "casual") -> str:
    style_text = STYLE_PROMPTS.get(style, STYLE_PROMPTS["casual"])
    data_text = build_data_summary(data)
    stock_name = data.get("basic", {}).get("name") or data.get("stock", {}).get("name")

    return f"""{style_text}

请根据以下数据，为 {stock_name} 写一份个股体检报告。

{data_text}

报告格式要求（严格按照以下结构输出，不要加任何额外说明）：

📊 【今日行情】
（2~3句话说明今天的价格和涨跌情况，结合近期走势给出判断）

💪 【财务健康度】
（用大白话解读毛利率、ROE、负债率等核心财务数据，给出"健康/一般/需注意"的整体评价）

🎯 【估值水位】
（解读PE和PB，判断当前估值是高还是低，对比行业给出参考）

🌊 【主力资金动向】
（解读主力净流入数据，判断主力是在买入、卖出还是观望）

📰 【近期热点】
（总结近期新闻，分析对股价可能的影响）

⚡ 【总体体检结论】
（综合各维度，用1~2句话给出整体判断，态度要明确，不要模棱两可）

⚠️ 【风险提示】
以下内容由AI根据公开数据自动生成，仅供参考学习，不构成任何投资建议。股市有风险，投资需谨慎，请结合自身情况独立决策。"""


def call_deepseek(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY 未设置，请在环境变量中配置")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def generate_report(data: dict, config: dict) -> str:
    """主函数：生成完整报告"""
    stock = data.get("stock", {})
    basic = data.get("basic", {})
    name = basic.get("name") or stock.get("name")
    full_code = stock.get("full", "")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 构建报告头
    header = f"{'='*50}\n🏥 个股体检报告 | {name}（{full_code}）\n📅 生成时间：{now}\n{'='*50}\n"

    logging.info("🤖 调用 DeepSeek 生成大白话报告...")
    prompt = build_prompt(data, style=config.get("style", "casual"))

    report_body = call_deepseek(
        prompt=prompt,
        model=config.get("deepseek_model", "deepseek-chat"),
        max_tokens=config.get("max_tokens", 2000),
        temperature=config.get("temperature", 0.7),
    )

    full_report = header + "\n" + report_body + "\n"
    logging.info(f"✅ 报告生成完成，共 {len(full_report)} 字")
    return full_report
