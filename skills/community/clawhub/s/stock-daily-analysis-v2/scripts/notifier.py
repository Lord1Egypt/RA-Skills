# -*- coding: utf-8 -*-
"""
通知/输出处理模块
负责格式化分析报告并输出结果
支持多渠道推送: 飞书、企业微信、Telegram、Discord、邮件
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnalysisReport:
    """分析报告数据结构"""
    code: str
    name: str
    sentiment_score: int
    trend_prediction: str
    operation_advice: str
    decision_type: str
    confidence_level: str
    technical_summary: Dict[str, Any]
    ai_analysis: Optional[str] = None
    risk_warning: str = ""
    buy_reason: str = ""
    support_levels: List[float] = None
    resistance_levels: List[float] = None
    
    def __post_init__(self):
        if self.support_levels is None:
            self.support_levels = []
        if self.resistance_levels is None:
            self.resistance_levels = []


def format_analysis_report(report: AnalysisReport) -> str:
    """格式化分析报告为文本"""
    lines = [
        f"{'='*50}",
        f"📊 {report.name} ({report.code}) 分析报告",
        f"{'='*50}",
        "",
        f"【核心结论】",
        f"  操作建议: {report.operation_advice}",
        f"  趋势预测: {report.trend_prediction}",
        f"  情绪评分: {report.sentiment_score}/100",
        f"  置信度: {report.confidence_level}",
        "",
        f"【技术面分析】",
    ]
    
    tech = report.technical_summary
    if 'current_price' in tech:
        lines.append(f"  当前价格: {tech.get('current_price', 'N/A')}")
    
    if 'ma5' in tech:
        lines.append(f"  MA5: {tech.get('ma5', 'N/A'):.2f} (乖离率: {tech.get('bias_ma5', 0):+.2f}%)")
    if 'ma10' in tech:
        lines.append(f"  MA10: {tech.get('ma10', 'N/A'):.2f} (乖离率: {tech.get('bias_ma10', 0):+.2f}%)")
    if 'ma20' in tech:
        lines.append(f"  MA20: {tech.get('ma20', 'N/A'):.2f}")
    
    if 'trend_status' in tech:
        lines.append(f"  趋势状态: {tech.get('trend_status', 'N/A')}")
    
    if 'volume_status' in tech:
        lines.append(f"  量能状态: {tech.get('volume_status', 'N/A')}")
    
    if 'macd_status' in tech:
        lines.append(f"  MACD: {tech.get('macd_status', 'N/A')}")
    
    if 'rsi_status' in tech:
        lines.append(f"  RSI: {tech.get('rsi_status', 'N/A')}")
    
    lines.append("")
    
    # 支撑压力位
    if report.support_levels:
        lines.append(f"【支撑位】")
        for level in report.support_levels[:3]:
            lines.append(f"  - {level:.2f}")
        lines.append("")
    
    if report.resistance_levels:
        lines.append(f"【压力位】")
        for level in report.resistance_levels[:3]:
            lines.append(f"  - {level:.2f}")
        lines.append("")
    
    if report.buy_reason:
        lines.append(f"【买入理由】")
        lines.append(f"  {report.buy_reason}")
        lines.append("")
    
    if report.risk_warning:
        lines.append(f"【风险提示】")
        lines.append(f"  {report.risk_warning}")
        lines.append("")
    
    if report.ai_analysis:
        lines.append(f"【AI 分析】")
        lines.append(f"  {report.ai_analysis}")
        lines.append("")
    
    lines.append(f"{'='*50}")
    
    return "\n".join(lines)


def format_dashboard_report(reports: List[AnalysisReport]) -> str:
    """格式化决策仪表盘报告"""
    if not reports:
        return "暂无分析报告"
    
    buy_count = sum(1 for r in reports if r.decision_type == 'buy')
    hold_count = sum(1 for r in reports if r.decision_type == 'hold')
    sell_count = sum(1 for r in reports if r.decision_type == 'sell')
    
    lines = [
        f"{'='*60}",
        f"📊 股票分析决策仪表盘",
        f"{'='*60}",
        "",
        f"分析股票数: {len(reports)} 只",
        f"🟢 买入: {buy_count}  🟡 观望: {hold_count}  🔴 卖出: {sell_count}",
        "",
        f"{'='*60}",
    ]
    
    for report in reports:
        emoji = "🟢" if report.decision_type == 'buy' else "🟡" if report.decision_type == 'hold' else "🔴"
        lines.append(f"{emoji} {report.name} ({report.code})")
        lines.append(f"   建议: {report.operation_advice} | 评分: {report.sentiment_score}/100")
        lines.append(f"   趋势: {report.trend_prediction}")
        
        tech = report.technical_summary
        key_info = []
        
        if 'bias_ma5' in tech:
            key_info.append(f"乖离率: {tech['bias_ma5']:+.1f}%")
        if 'macd_status' in tech:
            key_info.append(f"MACD: {tech['macd_status']}")
        
        if key_info:
            lines.append(f"   关键指标: {' | '.join(key_info)}")
        
        lines.append("")
    
    lines.append(f"{'='*60}")
    
    return "\n".join(lines)


def format_markdown_report(reports: List[AnalysisReport], title: str = None) -> str:
    """生成 Markdown 格式报告 (用于推送)"""
    if not reports:
        return "暂无分析报告"
    
    buy_count = sum(1 for r in reports if r.decision_type == 'buy')
    hold_count = sum(1 for r in reports if r.decision_type == 'hold')
    sell_count = sum(1 for r in reports if r.decision_type == 'sell')
    
    title = title or "📊 股票分析决策仪表盘"
    
    lines = [
        f"## {title}",
        "",
        f"**分析股票数**: {len(reports)} 只",
        f"| 🟢 买入 | 🟡 观望 | 🔴 卖出 |",
        f"|:---:|:---:|:---:|",
        f"| {buy_count} | {hold_count} | {sell_count} |",
        ""
    ]
    
    # 分类显示
    buy_stocks = [r for r in reports if r.decision_type == 'buy']
    hold_stocks = [r for r in reports if r.decision_type == 'hold']
    sell_stocks = [r for r in reports if r.decision_type == 'sell']
    
    if buy_stocks:
        lines.append("### 🟢 买入推荐")
        for r in buy_stocks:
            lines.append(f"- **{r.name}** ({r.code}) | 评分: {r.sentiment_score} | {r.trend_prediction}")
        lines.append("")
    
    if hold_stocks:
        lines.append("### 🟡 观望")
        for r in hold_stocks:
            lines.append(f"- **{r.name}** ({r.code}) | 评分: {r.sentiment_score} | {r.trend_prediction}")
        lines.append("")
    
    if sell_stocks:
        lines.append("### 🔴 卖出建议")
        for r in sell_stocks:
            lines.append(f"- **{r.name}** ({r.code}) | 评分: {r.sentiment_score} | {r.trend_prediction}")
        lines.append("")
    
    lines.append("")
    lines.append("---")
    lines.append("*仅供参考，不构成投资建议*")
    
    return "\n".join(lines)


def create_report_from_result(result: Dict[str, Any]) -> AnalysisReport:
    """从分析结果字典创建报告对象"""
    technical = result.get('technical_indicators', {})
    ai_result = result.get('ai_analysis', {})
    
    advice = ai_result.get('operation_advice', '观望')
    if advice in ['买入', '加仓', '强烈买入']:
        decision_type = 'buy'
    elif advice in ['卖出', '减仓', '强烈卖出']:
        decision_type = 'sell'
    else:
        decision_type = 'hold'
    
    return AnalysisReport(
        code=result.get('code', ''),
        name=result.get('name', ''),
        sentiment_score=ai_result.get('sentiment_score', 50),
        trend_prediction=ai_result.get('trend_prediction', '震荡'),
        operation_advice=advice,
        decision_type=decision_type,
        confidence_level=ai_result.get('confidence_level', '中'),
        technical_summary=technical,
        ai_analysis=ai_result.get('analysis_summary', ''),
        risk_warning=ai_result.get('risk_warning', ''),
        buy_reason=ai_result.get('buy_reason', ''),
        support_levels=technical.get('support_levels', []),
        resistance_levels=technical.get('resistance_levels', []),
    )


def print_report(report: AnalysisReport) -> None:
    """打印分析报告到控制台"""
    print(format_analysis_report(report))


def print_dashboard(reports: List[AnalysisReport]) -> None:
    """打印决策仪表盘到控制台"""
    print(format_dashboard_report(reports))


# ===== 推送功能 =====

def push_to_channels(results: List[Dict], config: Dict) -> Dict[str, Any]:
    """
    推送报告到各渠道
    
    Args:
        results: 分析结果列表
        config: 推送配置
        
    Returns:
        推送结果
    """
    push_results = {}
    
    # 转换为报告格式
    reports = [create_report_from_result(r) for r in results if 'error' not in r]
    markdown = format_markdown_report(reports)
    
    # 飞书推送
    if config.get('feishu_webhook'):
        try:
            push_results['feishu'] = push_to_feishu(config['feishu_webhook'], markdown)
        except Exception as e:
            push_results['feishu'] = {'error': str(e)}
    
    # 企业微信推送
    if config.get('wechat_webhook'):
        try:
            push_results['wechat'] = push_to_wechat(config['wechat_webhook'], markdown)
        except Exception as e:
            push_results['wechat'] = {'error': str(e)}
    
    # Telegram 推送
    if config.get('telegram_token') and config.get('telegram_chat_id'):
        try:
            push_results['telegram'] = push_to_telegram(
                config['telegram_token'],
                config['telegram_chat_id'],
                markdown
            )
        except Exception as e:
            push_results['telegram'] = {'error': str(e)}
    
    # Discord 推送
    if config.get('discord_webhook'):
        try:
            push_results['discord'] = push_to_discord(config['discord_webhook'], markdown)
        except Exception as e:
            push_results['discord'] = {'error': str(e)}
    
    # 邮件推送
    if config.get('email_sender') and config.get('email_receivers'):
        try:
            push_results['email'] = send_email(
                config['email_sender'],
                config['email_password'],
                config['email_receivers'].split(','),
                "股票分析报告",
                markdown
            )
        except Exception as e:
            push_results['email'] = {'error': str(e)}
    
    return push_results


def push_to_feishu(webhook: str, content: str) -> Dict[str, Any]:
    """推送消息到飞书"""
    import requests
    
    # 飞书卡片消息格式
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📊 股票分析报告"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    response = requests.post(webhook, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            return {'status': 'success', 'message': '飞书推送成功'}
        else:
            return {'status': 'error', 'message': result.get('msg', '未知错误')}
    else:
        return {'status': 'error', 'message': f'HTTP {response.status_code}'}


def push_to_wechat(webhook: str, content: str) -> Dict[str, Any]:
    """推送消息到企业微信"""
    import requests
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    response = requests.post(webhook, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('errcode') == 0:
            return {'status': 'success', 'message': '企业微信推送成功'}
        else:
            return {'status': 'error', 'message': result.get('errmsg', '未知错误')}
    else:
        return {'status': 'error', 'message': f'HTTP {response.status_code}'}


def push_to_telegram(token: str, chat_id: str, content: str) -> Dict[str, Any]:
    """推送消息到 Telegram"""
    import requests
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": content,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            return {'status': 'success', 'message': 'Telegram推送成功'}
        else:
            return {'status': 'error', 'message': result.get('description', '未知错误')}
    else:
        return {'status': 'error', 'message': f'HTTP {response.status_code}'}


def push_to_discord(webhook: str, content: str) -> Dict[str, Any]:
    """推送消息到 Discord"""
    import requests
    
    payload = {
        "content": content
    }
    
    response = requests.post(webhook, json=payload, timeout=30)
    
    if response.status_code in (200, 204):
        return {'status': 'success', 'message': 'Discord推送成功'}
    else:
        return {'status': 'error', 'message': f'HTTP {response.status_code}'}


def send_email(sender: str, password: str, receivers: List[str], 
               subject: str, content: str) -> Dict[str, Any]:
    """发送邮件"""
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    
    # 简单判断 QQ 邮箱
    if '@qq.com' in sender:
        # QQ 邮箱使用授权码
        smtp_server = 'smtp.qq.com'
        smtp_port = 465
    else:
        smtp_server = 'smtp.qq.com'  # 默认
        smtp_port = 465
    
    msg = MIMEText(content, 'markdown', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
        return {'status': 'success', 'message': '邮件发送成功'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
