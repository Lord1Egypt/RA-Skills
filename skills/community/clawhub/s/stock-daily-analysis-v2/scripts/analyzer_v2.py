# -*- coding: utf-8 -*-
"""
股票每日分析 - 完整集成版 (v2.1)
基于 ZhuLinsen/daily_stock_analysis 原版功能

新增功能:
- 大盘复盘 (cn/us/both)
- 板块分析
- 基本面聚合
- 多渠道推送 (飞书/企业微信/Telegram/Discord/邮件)
- Agent 问股 (简化版)
- 并发批量分析

优化:
- 添加飞书卡片消息支持
- 批量分析并发执行
- 更好的错误处理
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入模块
from scripts.data_fetcher import get_daily_data, get_realtime_quote, get_stock_name
from scripts.trend_analyzer import StockTrendAnalyzer
from scripts.ai_analyzer import AIAnalyzer
from scripts.notifier import (
    AnalysisReport, format_analysis_report, format_dashboard_report,
    format_markdown_report, push_to_channels
)
from scripts.fundamental import FundamentalAnalyzer
from scripts.market import MarketSummary, get_market_summary
from scripts.sector import SectorAnalyzer, get_sector_performance
from scripts.agent import StockAgent


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path is None:
        skill_dir = Path(__file__).parent.parent
        config_path = skill_dir / "config.json"
    
    default_config = {
        "data": {"days": 60, "realtime_enabled": True},
        "analysis": {"bias_threshold": 5.0},
        "fundamental": {"enabled": True, "timeout": 120},
        "market": {"enabled": True},
        "sector": {"enabled": True},
        "push": {
            "enabled": False,
            "feishu_webhook": "",
            "wechat_webhook": "",
            "telegram_token": "",
            "telegram_chat_id": "",
            "discord_webhook": "",
            "email_sender": "",
            "email_password": "",
            "email_receivers": ""
        }
    }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            # 合并配置
            config = default_config.copy()
            for key, value in user_config.items():
                if isinstance(value, dict) and key in config:
                    config[key].update(value)
                else:
                    config[key] = value
            return config
    except Exception as e:
        logger.warning(f"加载配置文件失败: {e}，使用默认配置")
        return default_config


def analyze_stock(code: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    分析单只股票 (完整版)
    
    Args:
        code: 股票代码 (如 '600519', 'AAPL', '00700')
        config: 配置字典，可选
        
    Returns:
        包含技术分析 + 基本面分析的完整结果
    """
    if config is None:
        config = load_config()
    
    logger.info(f"开始分析股票: {code}")
    
    # 获取股票名称
    name = get_stock_name(code)
    
    # 获取历史数据
    days = config.get('data', {}).get('days', 60)
    df = get_daily_data(code, days=days)
    
    if df is None or df.empty:
        logger.error(f"无法获取 {code} 的数据")
        return {
            'code': code,
            'name': name,
            'error': '数据获取失败',
            'technical_indicators': {},
            'ai_analysis': {'operation_advice': '数据不足', 'sentiment_score': 0}
        }
    
    # 技术分析
    analyzer = StockTrendAnalyzer()
    trend_result = analyzer.analyze(df, code)
    
    # 获取实时行情
    quote = get_realtime_quote(code)
    if quote:
        name = quote.get('name') or name
    
    # 基本面分析 (可选)
    fundamental_result = {}
    if config.get('fundamental', {}).get('enabled', True):
        try:
            fund_analyzer = FundamentalAnalyzer()
            fundamental_result = fund_analyzer.analyze(code)
        except Exception as e:
            logger.warning(f"基本面分析失败: {e}")
    
    # AI 深度分析 (含基本面)
    ai_config = config.get('ai', {})
    ai_analyzer = AIAnalyzer(ai_config)
    ai_result = ai_analyzer.analyze(code, name, trend_result.to_dict(), fundamental_result)
    
    # 整合结果
    result = {
        'code': code,
        'name': name,
        'market': guess_market(code),
        'technical_indicators': trend_result.to_dict(),
        'fundamental': fundamental_result,
        'ai_analysis': ai_result
    }
    
    logger.info(f"{code} 分析完成，评分: {ai_result.get('sentiment_score', trend_result.signal_score)}")
    return result


def analyze_stocks(codes: List[str], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    分析多只股票 (串行)
    
    Args:
        codes: 股票代码列表
        config: 配置字典，可选
        
    Returns:
        分析结果列表
    """
    results = []
    for code in codes:
        try:
            result = analyze_stock(code, config)
            results.append(result)
        except Exception as e:
            logger.error(f"分析 {code} 时出错: {e}")
            results.append({
                'code': code,
                'name': code,
                'error': str(e),
                'ai_analysis': {'operation_advice': '分析失败', 'sentiment_score': 0}
            })
    
    return results


def analyze_stocks_concurrent(codes: List[str], config: Optional[Dict] = None, 
                               max_workers: int = 5) -> List[Dict[str, Any]]:
    """
    分析多只股票 (并发)
    
    Args:
        codes: 股票代码列表
        config: 配置字典
        max_workers: 最大并发数
        
    Returns:
        分析结果列表
    """
    if config is None:
        config = load_config()
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_code = {
            executor.submit(analyze_stock, code, config): code 
            for code in codes
        }
        
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"分析 {code} 时出错: {e}")
                results.append({
                    'code': code,
                    'name': code,
                    'error': str(e),
                    'ai_analysis': {'operation_advice': '分析失败', 'sentiment_score': 0}
                })
    
    # 按原始顺序返回
    code_to_result = {r['code']: r for r in results}
    return [code_to_result.get(c, {'code': c, 'error': '未完成'}) for c in codes]


def market_review(market: str = 'cn', config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    大盘复盘
    
    Args:
        market: 市场类型 'cn'(A股) / 'us'(美股) / 'both'
        config: 配置字典
        
    Returns:
        大盘复盘结果
    """
    if config is None:
        config = load_config()
    
    logger.info(f"开始 {market} 大盘复盘...")
    
    result = {
        'market': market,
        'timestamp': get_timestamp()
    }
    
    if market in ('cn', 'both'):
        try:
            cn_summary = get_market_summary('cn')
            result['cn'] = cn_summary
        except Exception as e:
            logger.error(f"A股复盘失败: {e}")
            result['cn'] = {'error': str(e)}
    
    if market in ('us', 'both'):
        try:
            us_summary = get_market_summary('us')
            result['us'] = us_summary
        except Exception as e:
            logger.error(f"美股复盘失败: {e}")
            result['us'] = {'error': str(e)}
    
    return result


def sector_analysis(config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    板块分析
    
    Returns:
        板块涨跌榜
    """
    if config is None:
        config = load_config()
    
    logger.info("开始板块分析...")
    
    try:
        sectors = get_sector_performance()
        return {
            'sectors': sectors,
            'timestamp': get_timestamp()
        }
    except Exception as e:
        logger.error(f"板块分析失败: {e}")
        return {'error': str(e), 'sectors': []}


def agent_query(question: str, stocks: List[str] = None, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Agent 问股
    
    Args:
        question: 问题，如 "推荐新能源股票"
        stocks: 自选股列表
        config: 配置
        
    Returns:
        Agent 回答
    """
    if config is None:
        config = load_config()
    
    logger.info(f"Agent 问股: {question}")
    
    agent = StockAgent(config.get('ai', {}))
    result = agent.answer(question, stocks or [])
    
    return result


def push_report(results: List[Dict], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    推送报告到各渠道
    
    Args:
        results: 分析结果列表
        config: 配置
        
    Returns:
        推送结果
    """
    if config is None:
        config = load_config()
    
    push_config = config.get('push', {})
    if not push_config.get('enabled', False):
        return {'status': 'disabled', 'message': '推送未启用'}
    
    return push_to_channels(results, push_config)


def push_to_feishu_card(webhook: str, title: str, content: str) -> Dict[str, Any]:
    """
    推送飞书卡片消息
    
    Args:
        webhook: 飞书 Webhook URL
        title: 标题
        content: 内容 (Markdown)
        
    Returns:
        推送结果
    """
    import requests
    
    # 构建飞书卡片
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": "green"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "查看详情"
                            },
                            "url": "https://openclaw.ai",
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return {'status': 'success'}
            else:
                return {'status': 'error', 'message': result.get('msg', '未知错误')}
        return {'status': 'error', 'message': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def daily_push(config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    每日定时推送
    
    从配置中读取 STOCK_LIST 进行分析并推送
    
    Args:
        config: 配置
        
    Returns:
        推送结果
    """
    if config is None:
        config = load_config()
    
    # 获取自选股列表
    stock_list = config.get('stock_list', '')
    if not stock_list:
        return {'status': 'error', 'message': '未配置 STOCK_LIST'}
    
    codes = [s.strip() for s in stock_list.split(',') if s.strip()]
    
    if not codes:
        return {'status': 'error', 'message': 'STOCK_LIST 为空'}
    
    logger.info(f"开始每日推送，分析 {len(codes)} 只股票...")
    
    # 分析股票 (使用并发)
    results = analyze_stocks_concurrent(codes, config)
    
    # 推送到各渠道
    push_config = config.get('push', {})
    if push_config.get('enabled', False):
        push_result = push_to_channels(results, push_config)
        
        # 飞书卡片推送 (更美观)
        if push_config.get('feishu_webhook'):
            reports = [create_report_from_result(r) for r in results if 'error' not in r]
            markdown = format_markdown_report(reports, "📊 每日股票分析报告")
            card_result = push_to_feishu_card(
                push_config['feishu_webhook'],
                "📊 每日股票分析报告",
                markdown
            )
            push_result['feishu_card'] = card_result
        
        return push_result
    else:
        return {
            'status': 'skipped',
            'message': '推送未启用',
            'results_count': len(results)
        }


def print_analysis(codes: List[str]) -> None:
    """分析股票并打印报告"""
    results = analyze_stocks(codes)
    
    reports = []
    for result in results:
        if 'error' not in result:
            report = create_report_from_result(result)
            reports.append(report)
    
    if reports:
        print("\n" + format_dashboard_report(reports))
        
        for report in reports:
            print("\n" + format_analysis_report(report))
    else:
        print("没有可显示的报告")


def create_report_from_result(result: Dict[str, Any]):
    """创建报告对象"""
    from scripts.notifier import create_report_from_result as _create
    return _create(result)


# 辅助函数
def guess_market(code: str) -> str:
    """猜测市场类型"""
    code = str(code).upper()
    if code.startswith('HK') or code.startswith('0') or len(code) == 5:
        return 'hk'
    elif code.isdigit() and len(code) == 6:
        return 'cn'
    elif code.isalpha() and len(code) <= 5:
        return 'us'
    return 'unknown'


def get_timestamp() -> str:
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 便捷函数
if __name__ == "__main__":
    import sys
    
    print("=== 股票每日分析系统 v2.1 (完整集成版) ===\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'analyze':
            codes = sys.argv[2:] if len(sys.argv) > 2 else ['600519']
            print_analysis(codes)
            
        elif command == 'review':
            market = sys.argv[2] if len(sys.argv) > 2 else 'cn'
            result = market_review(market)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif command == 'sector':
            result = sector_analysis()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif command == 'agent':
            question = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "推荐银行股"
            result = agent_query(question)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == 'push':
            # 每日推送
            result = daily_push()
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == 'concurrent':
            # 并发分析
            codes = sys.argv[2:] if len(sys.argv) > 2 else ['600519', '000858', '601318']
            results = analyze_stocks_concurrent(codes)
            for r in results:
                print(f"{r.get('name')}: {r.get('ai_analysis', {}).get('operation_advice', 'N/A')}")
        
        else:
            print(f"未知命令: {command}")
            print_usage()
    else:
        print("测试分析茅台 (600519)...\n")
        print_analysis(['600519'])


def print_usage():
    """打印使用说明"""
    print("""
用法:
    python -m scripts.analyzer_v2 analyze <股票代码...>   # 分析股票
    python -m scripts.analyzer_v2 review <cn/us/both>   # 大盘复盘
    python -m scripts.analyzer_v2 sector                 # 板块分析
    python -m scripts.analyzer_v2 agent <问题>            # Agent 问股
    python -m scripts.analyzer_v2 push                   # 每日定时推送
    python -m scripts.analyzer_v2 concurrent <股票...>   # 并发分析

示例:
    python -m scripts.analyzer_v2 analyze 600519 AAPL
    python -m scripts.analyzer_v2 review cn
    python -m scripts.analyzer_v2 sector
    python -m scripts.analyzer_v2 agent 推荐新能源股票
    python -m scripts.analyzer_v2 push
""")
