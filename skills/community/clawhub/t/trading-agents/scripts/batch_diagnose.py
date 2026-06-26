#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量股票诊断模块
支持输入股票代码列表进行批量诊断，并通过钉钉机器人推送结果
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from .stock_advisor import StockAdvisorSystem

# 钉钉机器人Webhook URL（从环境变量读取）
DINGTALK_WEBHOOK_URL = os.getenv('DINGTALK_WEBHOOK_URL', '')
# 钉钉机器人签名密钥（可选，用于加签模式）
DINGTALK_SECRET = os.getenv('DINGTALK_SECRET', '')


def convert_to_ts_code(stock_code: str) -> str:
    """
    将股票代码转换为ts_code格式
    
    Args:
        stock_code: 6位股票代码（如 600519）或已带后缀的代码（如 600519.SH）
        
    Returns:
        ts_code格式（如 600519.SH）
    """
    code = stock_code.strip().upper()
    
    # 如果已经是 ts_code 格式，直接返回
    if '.' in code:
        return code
    
    # 移除可能的前缀
    if code.startswith('SH'):
        code = code[2:]
        return f"{code}.SH"
    elif code.startswith('SZ'):
        code = code[2:]
        return f"{code}.SZ"
    
    # 根据代码前缀判断交易所
    if code.startswith('6'):
        return f"{code}.SH"  # 上海
    elif code.startswith('0') or code.startswith('3'):
        return f"{code}.SZ"  # 深圳
    elif code.startswith('8') or code.startswith('4'):
        return f"{code}.BJ"  # 北交所
    else:
        return f"{code}.SZ"  # 默认深圳


def parse_stock_codes(codes_input: str) -> List[str]:
    """
    解析股票代码输入，支持多种格式
    
    Args:
        codes_input: 股票代码字符串，支持逗号、空格、换行分隔
        
    Returns:
        ts_code 格式的股票代码列表
    """
    # 替换各种分隔符为逗号
    codes_str = codes_input.replace('\n', ',').replace(' ', ',').replace('，', ',')
    
    # 分割并去重
    codes = [c.strip() for c in codes_str.split(',') if c.strip()]
    
    # 转换为 ts_code 格式
    ts_codes = [convert_to_ts_code(code) for code in codes]
    
    # 去重并保持顺序
    seen = set()
    unique_codes = []
    for code in ts_codes:
        if code not in seen:
            seen.add(code)
            unique_codes.append(code)
    
    return unique_codes


def batch_diagnose(
    stock_codes: List[str],
    output_dir: str = "report"
) -> List[Dict]:
    """
    批量诊断指定的股票列表
    
    Args:
        stock_codes: 股票代码列表（ts_code格式）
        output_dir: 报告输出目录
        
    Returns:
        诊断结果列表
    """
    print("=" * 60)
    print("批量股票诊断系统")
    print("=" * 60)
    print(f"待诊断股票: {len(stock_codes)} 只")
    print(f"股票列表: {', '.join(stock_codes)}")
    print("=" * 60)
    
    if not stock_codes:
        print("❌ 股票列表为空，无法进行诊断")
        return []
    
    # 创建诊断系统
    print("\n初始化诊断系统...")
    advisor = StockAdvisorSystem()
    
    # 诊断结果
    results = []
    
    # 逐一诊断
    for i, ts_code in enumerate(stock_codes, 1):
        print(f"\n{'=' * 60}")
        print(f"[{i}/{len(stock_codes)}] 正在诊断: {ts_code}")
        print(f"{'=' * 60}")
        
        try:
            # 执行诊断
            result = advisor.diagnose(ts_code, output_dir)
            
            if result:
                result['rank'] = i
                
                # 保存完整报告
                advisor.save_report(result)
                
                results.append(result)
                print(f"✅ {ts_code} 诊断完成")
            else:
                print(f"⚠️ {ts_code} 诊断结果为空")
                
        except Exception as e:
            print(f"❌ {ts_code} 诊断失败: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # 输出汇总
    print(f"\n{'=' * 60}")
    print("批量诊断汇总")
    print(f"{'=' * 60}")
    print(f"计划诊断: {len(stock_codes)} 只股票")
    print(f"成功完成: {len(results)} 只股票")
    print(f"报告目录: {output_dir}")
    
    if results:
        print(f"\n诊断完成的股票:")
        for r in results:
            print(f"  - {r['ts_code']} ({r['stock_name']})")
    
    return results


def generate_dingtalk_sign(timestamp: str, secret: str) -> str:
    """
    生成钉钉机器人签名（加签模式）
    
    Args:
        timestamp: 时间戳（毫秒）
        secret: 签名密钥
        
    Returns:
        签名字符串
    """
    import hmac
    import hashlib
    import base64
    import urllib.parse
    
    string_to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(
        secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign


def send_dingtalk_message(stocks: List[Dict], webhook_url: Optional[str] = None, secret: Optional[str] = None) -> bool:
    """
    通过钉钉机器人发送推荐买入股票消息
    
    Args:
        stocks: 推荐买入的股票列表
        webhook_url: 钉钉机器人Webhook URL，为空则使用环境变量
        secret: 签名密钥，为空则使用环境变量
        
    Returns:
        是否发送成功
    """
    url = webhook_url or DINGTALK_WEBHOOK_URL
    secret_key = secret or DINGTALK_SECRET
    
    if not url:
        print("\n⚠️ 未配置钉钉Webhook URL")
        print("请设置环境变量 DINGTALK_WEBHOOK_URL 或在.env文件中配置")
        return False
    
    if not stocks:
        print("\n⚠️ 没有推荐买入的股票，跳过发送")
        return False
    
    # 如果配置了签名密钥，生成签名
    if secret_key:
        timestamp = str(int(datetime.now().timestamp() * 1000))
        sign = generate_dingtalk_sign(timestamp, secret_key)
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    # 构建消息内容
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 构建Markdown格式消息
    markdown_title = "📈 智能诊股推荐"
    markdown_text = f"## 📈 智能诊股推荐\n\n"
    markdown_text += f"> 分析时间: {current_time}\n\n"
    markdown_text += f"**共 {len(stocks)} 只股票推荐买入：**\n\n"
    
    for i, stock in enumerate(stocks, 1):
        ts_code = stock.get('ts_code', 'N/A')
        stock_name = stock.get('stock_name', 'N/A')
        action = stock.get('action', 'N/A')
        overall_score = stock.get('overall_score', 'N/A')
        confidence = stock.get('confidence', 'N/A')
        position = stock.get('position', 'N/A')
        target_price = stock.get('target_price', 'N/A')
        stop_loss = stock.get('stop_loss', 'N/A')
        
        markdown_text += f"---\n\n"
        markdown_text += f"### {i}. {stock_name} ({ts_code})\n\n"
        markdown_text += f"- **操作建议**: {action}\n"
        markdown_text += f"- **综合评分**: {overall_score}/100\n"
        markdown_text += f"- **置信度**: {confidence}/100\n"
        markdown_text += f"- **建议仓位**: {position}%\n"
        markdown_text += f"- **目标价**: {target_price}\n"
        markdown_text += f"- **止损价**: {stop_loss}\n\n"
    
    markdown_text += f"---\n\n"
    markdown_text += f"*本消息由AgentScope智能诊股系统自动生成*"
    
    # 构建钉钉消息请求数据
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": markdown_title,
            "text": markdown_text
        }
    }
    
    try:
        print(f"\n{'=' * 60}")
        print("发送钉钉消息...")
        
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        result = response.json()
        
        if result.get('errcode') == 0:
            print("✅ 钉钉消息发送成功!")
            return True
        else:
            print(f"❌ 发送失败: {result.get('errmsg', '未知错误')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 发送超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 发送失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False


def send_dingtalk_text_message(text: str, webhook_url: Optional[str] = None, secret: Optional[str] = None) -> bool:
    """
    发送纯文本消息到钉钉
    
    Args:
        text: 消息文本内容
        webhook_url: 钉钉机器人Webhook URL
        secret: 签名密钥
        
    Returns:
        是否发送成功
    """
    url = webhook_url or DINGTALK_WEBHOOK_URL
    secret_key = secret or DINGTALK_SECRET
    
    if not url:
        print("⚠️ 未配置钉钉Webhook URL")
        return False
    
    # 如果配置了签名密钥，生成签名
    if secret_key:
        timestamp = str(int(datetime.now().timestamp() * 1000))
        sign = generate_dingtalk_sign(timestamp, secret_key)
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        result = response.json()
        return result.get('errcode') == 0
    except Exception as e:
        print(f"发送失败: {e}")
        return False


def analyze_reports_from_directory(
    report_dir: str = "report",
    top_n: int = 5,
    days: int = 2
) -> List[Dict]:
    """
    从报告目录读取最近的诊断报告，分析并排序，挑选推荐买入的股票
    
    Args:
        report_dir: 报告目录路径
        top_n: 返回前N只推荐买入的股票
        days: 分析最近几天的报告（默认2天，即昨天和今天）
        
    Returns:
        排序后的推荐买入股票列表
    """
    import re
    
    print(f"\n{'=' * 60}")
    print("分析诊断报告 - 筛选推荐买入股票")
    print(f"{'=' * 60}")
    print(f"报告目录: {report_dir}")
    print(f"分析范围: 最近 {days} 天的报告")
    
    if not os.path.exists(report_dir):
        print(f"❌ 报告目录不存在: {report_dir}")
        return []
    
    # 获取所有子目录（每个子目录是一次诊断）
    subdirs = [d for d in os.listdir(report_dir) 
               if os.path.isdir(os.path.join(report_dir, d))]
    
    if not subdirs:
        print("❌ 报告目录下没有诊断报告")
        return []
    
    # 筛选最近N天的报告
    today = datetime.now().date()
    date_threshold = today - timedelta(days=days - 1)  # 包含今天
    
    filtered_subdirs = []
    for subdir in subdirs:
        # 从report目录名解析日期（格式如: 000807_SZ_20260131_011712）
        date_match = re.search(r'_(\d{8})_\d{6}$', subdir)
        if date_match:
            try:
                report_date_str = date_match.group(1)
                report_date = datetime.strptime(report_date_str, '%Y%m%d').date()
                
                if report_date >= date_threshold:
                    filtered_subdirs.append(subdir)
            except ValueError:
                continue
        else:
            # 无法解析日期，检查文件修改时间
            subdir_path = os.path.join(report_dir, subdir)
            mtime = datetime.fromtimestamp(os.path.getmtime(subdir_path)).date()
            if mtime >= date_threshold:
                filtered_subdirs.append(subdir)
    
    print(f"\n找到 {len(subdirs)} 个诊断报告目录")
    print(f"符合时间范围的报告: {len(filtered_subdirs)} 个（{date_threshold} 至今天）")
    
    if not filtered_subdirs:
        print("⚠️ 没有符合时间范围的报告")
        return []
    
    all_decisions = []
    
    for subdir in filtered_subdirs:
        subdir_path = os.path.join(report_dir, subdir)
        
        # 尝试读取最终决策报告
        json_file = os.path.join(subdir_path, "complete_diagnosis_report.json")
        decision_file = os.path.join(subdir_path, "最终决策报告.md")
        
        decision_data = None
        
        # 优先从JSON文件读取（数据更完整）
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    decision_data = parse_decision_from_json(json_data, subdir)
            except Exception as e:
                print(f"  ⚠️ 解析JSON失败 ({subdir}): {e}")
        
        # 如果JSON不可用，从MD文件解析
        if decision_data is None and os.path.exists(decision_file):
            try:
                with open(decision_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    decision_data = parse_decision_from_md(md_content, subdir)
            except Exception as e:
                print(f"  ⚠️ 解析MD失败 ({subdir}): {e}")
        
        if decision_data:
            all_decisions.append(decision_data)
    
    print(f"\n成功解析 {len(all_decisions)} 份诊断报告")
    
    if not all_decisions:
        print("❌ 没有成功解析的诊断报告")
        return []
    
    # 筛选推荐买入的股票（操作建议为UP）
    buy_recommendations = [
        d for d in all_decisions 
        if d.get('action', '').upper() in ['UP', '买入', 'BUY', '增持']
    ]
    
    print(f"\n推荐买入的股票: {len(buy_recommendations)} 只")
    
    if not buy_recommendations:
        print("⚠️ 没有推荐买入的股票")
        # 显示所有股票的操作建议
        print("\n所有股票操作建议:")
        for d in all_decisions:
            print(f"  - {d.get('ts_code', 'N/A')} ({d.get('stock_name', 'N/A')}): {d.get('action', 'N/A')}")
        return []
    
    # 按综合评分排序（从高到低）
    buy_recommendations.sort(
        key=lambda x: (x.get('overall_score', 0), x.get('confidence', 0)),
        reverse=True
    )
    
    # 取前N只
    top_stocks = buy_recommendations[:top_n]
    
    # 输出结果
    print(f"\n{'=' * 60}")
    print(f"Top {len(top_stocks)} 推荐买入股票（按综合评分排序）")
    print(f"{'=' * 60}")
    print(f"{'排名':<4} {'代码':<12} {'名称':<10} {'操作':<6} {'综合评分':<8} {'置信度':<8} {'仓位':<6}")
    print("-" * 70)
    
    for i, stock in enumerate(top_stocks, 1):
        print(f"{i:<4} {stock.get('ts_code', 'N/A'):<12} "
              f"{stock.get('stock_name', 'N/A'):<10} "
              f"{stock.get('action', 'N/A'):<6} "
              f"{stock.get('overall_score', 'N/A'):<8} "
              f"{stock.get('confidence', 'N/A'):<8} "
              f"{stock.get('position', 'N/A'):<6}")
    
    print("-" * 70)
    
    return top_stocks


def parse_decision_from_json(json_data: Dict, subdir: str) -> Optional[Dict[str, Any]]:
    """从JSON数据解析决策信息"""
    import re
    
    final_decision = json_data.get('final_decision', '')
    
    if not final_decision:
        return None
    
    result: Dict[str, Any] = {
        'ts_code': json_data.get('ts_code', ''),
        'stock_name': json_data.get('stock_name', ''),
        'report_dir': subdir,
        'diagnosis_time': json_data.get('diagnosis_time', ''),
    }
    
    # 解析操作建议
    action_match = re.search(r'操作建议[\s\|]*\**([^\|\*\n]+)\**', final_decision)
    if action_match:
        result['action'] = action_match.group(1).strip()
    
    # 解析综合评分
    score_match = re.search(r'综合评分[\s\|]*\**(\d+)[/／](\d+)\**', final_decision)
    if score_match:
        result['overall_score'] = int(score_match.group(1))
    
    # 解析置信度
    conf_match = re.search(r'置信度[\s\|]*(\d+)[/／]?(\d*)', final_decision)
    if conf_match:
        result['confidence'] = int(conf_match.group(1))
    
    # 解析建议仓位
    pos_match = re.search(r'建议仓位[\s\|]*([\d.]+)', final_decision)
    if pos_match:
        result['position'] = float(pos_match.group(1))
    
    # 解析目标价
    target_match = re.search(r'目标价[\s\|]*([\d.]+)', final_decision)
    if target_match:
        result['target_price'] = float(target_match.group(1))
    
    # 解析止损价
    stop_match = re.search(r'止损价[\s\|]*([\d.]+)', final_decision)
    if stop_match:
        result['stop_loss'] = float(stop_match.group(1))
    
    # 解析决策理由
    reason_match = re.search(r'## 决策理由\n([^#]+)', final_decision)
    if reason_match:
        result['reason'] = reason_match.group(1).strip()
    
    return result


def parse_decision_from_md(md_content: str, subdir: str) -> Optional[Dict[str, Any]]:
    """从Markdown内容解析决策信息"""
    import re
    
    result: Dict[str, Any] = {
        'report_dir': subdir,
    }
    
    # 解析股票代码
    code_match = re.search(r'代码[：:][\s]*([\w.]+)', md_content)
    if code_match:
        result['ts_code'] = code_match.group(1).strip()
    
    # 解析股票名称
    name_match = re.search(r'名称[：:][\s]*([^\n]+)', md_content)
    if name_match:
        result['stock_name'] = name_match.group(1).strip()
    
    # 解析操作建议
    action_match = re.search(r'操作建议[\s\|]*\**([^\|\*\n]+)\**', md_content)
    if action_match:
        result['action'] = action_match.group(1).strip()
    
    # 解析综合评分
    score_match = re.search(r'综合评分[\s\|]*\**(\d+)[/／](\d+)\**', md_content)
    if score_match:
        result['overall_score'] = int(score_match.group(1))
    
    # 解析置信度
    conf_match = re.search(r'置信度[\s\|]*(\d+)[/／]?(\d*)', md_content)
    if conf_match:
        result['confidence'] = int(conf_match.group(1))
    
    # 解析建议仓位
    pos_match = re.search(r'建议仓位[\s\|]*([\d.]+)', md_content)
    if pos_match:
        result['position'] = float(pos_match.group(1))
    
    # 解析目标价
    target_match = re.search(r'目标价[\s\|]*([\d.]+)', md_content)
    if target_match:
        result['target_price'] = float(target_match.group(1))
    
    # 解析止损价
    stop_match = re.search(r'止损价[\s\|]*([\d.]+)', md_content)
    if stop_match:
        result['stop_loss'] = float(stop_match.group(1))
    
    # 解析决策理由
    reason_match = re.search(r'## 决策理由\n([^#]+)', md_content)
    if reason_match:
        result['reason'] = reason_match.group(1).strip()
    
    return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量股票诊断 - 支持输入股票代码列表'
    )
    parser.add_argument(
        '--stocks', '-s',
        type=str,
        required=False,
        help='股票代码列表，逗号分隔（如: 600519,000001,300750）'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        required=False,
        help='股票代码文件路径，每行一个代码'
    )
    parser.add_argument(
        '--output', '-o', 
        type=str, 
        default='report',
        help='报告输出目录（默认: report）'
    )
    parser.add_argument(
        '--analyze', '-a',
        action='store_true',
        help='分析已有报告，挑选推荐买入的股票'
    )
    parser.add_argument(
        '--analyze-top', '-at',
        type=int,
        default=5,
        help='分析时返回前N只推荐买入的股票（默认: 5）'
    )
    parser.add_argument(
        '--send-dingtalk', '-d',
        action='store_true',
        help='将推荐买入的股票发送到钉钉'
    )
    parser.add_argument(
        '--webhook-url',
        type=str,
        default='',
        help='钉钉机器人Webhook URL（也可通过环境变量DINGTALK_WEBHOOK_URL配置）'
    )
    parser.add_argument(
        '--secret',
        type=str,
        default='',
        help='钉钉机器人签名密钥（也可通过环境变量DINGTALK_SECRET配置）'
    )
    
    args = parser.parse_args()
    
    # 分析已有报告
    if args.analyze:
        top_stocks = analyze_reports_from_directory(
            report_dir=args.output,
            top_n=args.analyze_top
        )
        if top_stocks:
            print(f"\n✅ 分析完成，推荐买入 {len(top_stocks)} 只股票")
            
            # 发送钉钉消息
            if args.send_dingtalk:
                send_dingtalk_message(
                    top_stocks, 
                    args.webhook_url if args.webhook_url else None,
                    args.secret if args.secret else None
                )
        else:
            print("\n⚠️ 没有推荐买入的股票")
        return
    
    # 获取股票代码列表
    stock_codes = []
    
    if args.stocks:
        # 从命令行参数获取
        stock_codes = parse_stock_codes(args.stocks)
    elif args.file:
        # 从文件读取
        if os.path.exists(args.file):
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
                stock_codes = parse_stock_codes(content)
        else:
            print(f"❌ 文件不存在: {args.file}")
            return
    else:
        # 交互式输入
        print("请输入股票代码（逗号分隔，如: 600519,000001,300750）:")
        codes_input = input().strip()
        if codes_input:
            stock_codes = parse_stock_codes(codes_input)
    
    if not stock_codes:
        print("❌ 未提供有效的股票代码")
        print("\n使用方法:")
        print("  python batch_diagnose.py --stocks 600519,000001,300750")
        print("  python batch_diagnose.py --file stocks.txt")
        print("  python batch_diagnose.py --analyze --send-dingtalk")
        return
    
    # 执行批量诊断
    results = batch_diagnose(
        stock_codes=stock_codes,
        output_dir=args.output
    )
    
    if results:
        print(f"\n✅ 批量诊断完成，共诊断 {len(results)} 只股票")
        
        # 分析结果并发送钉钉
        if args.send_dingtalk:
            print("\n" + "=" * 60)
            print("分析诊断结果...")
            top_stocks = analyze_reports_from_directory(
                report_dir=args.output,
                top_n=args.analyze_top,
                days=1  # 只分析今天的报告
            )
            
            if top_stocks:
                send_dingtalk_message(
                    top_stocks,
                    args.webhook_url if args.webhook_url else None,
                    args.secret if args.secret else None
                )
    else:
        print("\n❌ 批量诊断未产生有效结果")


if __name__ == "__main__":
    main()
