#!/usr/bin/env python3
"""
友盟推送助手 - 查询开关统计
调用 upush.umeng.com API 查询应用的开关统计数据
包括：新增关闭设备数、新增打开设备数、DAU、关闭设备数、日关闭率
支持生成美观的 HTML 折线图报告
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")
SCRIPT_DIR = Path(__file__).parent

# 开关统计类型定义
SWITCH_TYPES = {
    "addClose": "新增关闭设备数",
    "addOpen": "新增打开设备数",
    "dau": "DAU",
    "cnt": "关闭设备数",
    "ratio": "日关闭率"
}

def load_cookie():
    """从文件加载 Cookie"""
    if not os.path.exists(COOKIE_FILE):
        return None
    with open(COOKIE_FILE, 'r') as f:
        return f.read().strip()

def extract_ctoken(cookie):
    """从 Cookie 字符串中提取 ctoken 值"""
    for item in cookie.split(';'):
        item = item.strip()
        if item.startswith('ctoken='):
            return item.split('=', 1)[1]
    return None

def make_request(url, data):
    """
    发送 POST 请求到友盟 API
    
    Args:
        url: API URL
        data: 请求数据字典
    
    Returns:
        解析后的 JSON 响应
    """
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    # 提取 ctoken 用于 x-csrf-token 头
    ctoken = extract_ctoken(cookie)
    
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "x-csrf-token": ctoken if ctoken else ""
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        print(f"ERROR: HTTP 错误 {e.code}", file=sys.stderr)
        print(f"详情：{e.reason}", file=sys.stderr)
        if error_body:
            print(f"响应内容：{error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: 网络错误", file=sys.stderr)
        print(f"详情：{e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def parse_date(date_str):
    """
    解析日期字符串为 datetime 对象
    
    Args:
        date_str: 日期字符串，支持格式 yyyy-MM-dd 或自然语言描述
    
    Returns:
        datetime 对象
    """
    # 如果已经是 datetime 对象，直接返回
    if isinstance(date_str, datetime):
        return date_str
    
    # 尝试解析标准日期格式
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass
    
    # 处理自然语言描述（简单实现）
    today = datetime.now()
    
    if "昨天" in date_str or "昨日" in date_str:
        return today - timedelta(days=1)
    elif "今天" in date_str:
        return today
    elif "前天" in date_str:
        return today - timedelta(days=2)
    
    # 尝试解析"过去 N 天"格式
    import re
    match = re.search(r'过去 (\d+) 天', date_str)
    if match:
        days = int(match.group(1))
        return today - timedelta(days=days)
    
    raise ValueError(f"无法解析日期：{date_str}")

def calculate_date_range(start_input=None, end_input=None):
    """
    计算日期范围
    
    Args:
        start_input: 开始日期输入（None 表示使用默认值）
        end_input: 结束日期输入（None 表示使用默认值）
    
    Returns:
        (start_date, end_date) 元组，格式为 yyyy-MM-dd
    """
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    seven_days_ago = today - timedelta(days=7)
    
    # 处理结束日期
    if end_input:
        end_date = parse_date(end_input)
    else:
        end_date = yesterday
    
    # 处理开始日期
    if start_input:
        # 检查是否是"过去 N 天"的描述
        import re
        match = re.search(r'过去 (\d+) 天', start_input)
        if match:
            days = int(match.group(1))
            start_date = today - timedelta(days=days)
        else:
            start_date = parse_date(start_input)
    else:
        start_date = seven_days_ago
    
    # 确保开始日期不晚于结束日期
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def query_switch_trend(appkey, start_date, end_date, stat_type):
    """
    查询开关趋势数据
    
    Args:
        appkey: 应用 key
        start_date: 开始日期 (yyyy-MM-dd)
        end_date: 结束日期 (yyyy-MM-dd)
        stat_type: 统计类型 (addClose/addOpen/dau/cnt/ratio)
    
    Returns:
        API 响应结果
    """
    url = "https://upush.umeng.com/hsf/dataStatistic/getCloseTrend"
    data = {
        "appkey": appkey,
        "startDate": start_date,
        "endDate": end_date,
        "type": stat_type
    }
    
    result = make_request(url, data)
    return result

def format_value(value, stat_type):
    """
    格式化显示值
    
    Args:
        value: 数值
        stat_type: 统计类型
    
    Returns:
        格式化后的字符串
    """
    if value is None:
        return "N/A"
    
    try:
        num_value = float(value)
        if stat_type == "ratio":
            # 比率类型，转换为百分比
            return f"{num_value:.2f}%"
        else:
            # 其他类型，保留整数
            return f"{int(num_value):,}"
    except (ValueError, TypeError):
        return str(value)

def display_results(all_results, start_date, end_date):
    """
    展示查询结果
    
    Args:
        all_results: 所有统计类型的结果字典
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        (all_data_points, summary_stats) 元组
    """
    print("\n" + "=" * 80)
    print("📊 友盟推送 - 开关统计报告")
    print("=" * 80)
    print(f"统计时间：{start_date} 至 {end_date}")
    print("=" * 80 + "\n")
    
    # 收集所有数据点
    all_data_points = []
    for stat_type, result in all_results.items():
        if result.get('status'):
            data = result.get('data', {})
            # API 返回的数据可能是 list 格式（包含 name 和 value 字段）
            if isinstance(data, dict) and 'list' in data:
                data = data['list']
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    # 日期字段可能是 'name' 或 'date'
                    date = item.get('name') or item.get('date', 'N/A')
                    value = item.get('value')
                    if date and value is not None:
                        all_data_points.append({
                            'date': date,
                            'type': stat_type,
                            'value': value
                        })
    
    if not all_data_points:
        print("⚠️  未找到统计数据")
        return [], {}
    
    # 按日期分组
    from collections import defaultdict
    data_by_date = defaultdict(dict)
    for point in all_data_points:
        data_by_date[point['date']][point['type']] = point['value']
    
    # 按日期排序
    sorted_dates = sorted(data_by_date.keys())
    
    # 逐项详细列出每个日期的数据
    for date in sorted_dates:
        day_data = data_by_date[date]
        
        print(f"【{date}】")
        print("-" * 60)
        
        # 新增关闭设备数
        add_close = day_data.get('addClose')
        if add_close is not None:
            print(f"  新增关闭设备数：{format_value(add_close, 'addClose')}")
        else:
            print(f"  新增关闭设备数：无数据")
        
        # 新增打开设备数
        add_open = day_data.get('addOpen')
        if add_open is not None:
            print(f"  新增打开设备数：{format_value(add_open, 'addOpen')}")
        else:
            print(f"  新增打开设备数：无数据")
        
        # DAU
        dau = day_data.get('dau')
        if dau is not None:
            print(f"  DAU（日活跃设备数）：{format_value(dau, 'dau')}")
        else:
            print(f"  DAU（日活跃设备数）：无数据")
        
        # 关闭设备数
        cnt = day_data.get('cnt')
        if cnt is not None:
            print(f"  累计关闭设备数：{format_value(cnt, 'cnt')}")
        else:
            print(f"  累计关闭设备数：无数据")
        
        # 日关闭率
        ratio = day_data.get('ratio')
        if ratio is not None:
            print(f"  日关闭率：{format_value(ratio, 'ratio')}")
        else:
            print(f"  日关闭率：无数据")
        
        print("")
    
    # 汇总统计
    print("=" * 60)
    print("📈 汇总统计")
    print("=" * 60)
    
    total_add_close = sum(
        float(point['value']) for point in all_data_points 
        if point['type'] == 'addClose' and point['value'] is not None
    )
    total_add_open = sum(
        float(point['value']) for point in all_data_points 
        if point['type'] == 'addOpen' and point['value'] is not None
    )
    avg_dau = sum(
        float(point['value']) for point in all_data_points 
        if point['type'] == 'dau' and point['value'] is not None
    ) / len([p for p in all_data_points if p['type'] == 'dau']) if any(p['type'] == 'dau' for p in all_data_points) else 0
    total_cnt = sum(
        float(point['value']) for point in all_data_points 
        if point['type'] == 'cnt' and point['value'] is not None
    )
    avg_ratio = sum(
        float(point['value']) for point in all_data_points 
        if point['type'] == 'ratio' and point['value'] is not None
    ) / len([p for p in all_data_points if p['type'] == 'ratio']) if any(p['type'] == 'ratio' for p in all_data_points) else 0
    
    print(f"  累计新增关闭设备数：{int(total_add_close):,}")
    print(f"  累计新增打开设备数：{int(total_add_open):,}")
    print(f"  平均 DAU：{int(avg_dau):,}")
    print(f"  累计关闭设备数：{int(total_cnt):,}")
    print(f"  平均日关闭率：{avg_ratio:.2f}%")
    print("=" * 60)
    
    summary_stats = {
        'total_add_close': total_add_close,
        'total_add_open': total_add_open,
        'avg_dau': avg_dau,
        'total_cnt': total_cnt,
        'avg_ratio': avg_ratio
    }
    
    return all_data_points, summary_stats
    
    return all_data_points, {
        'total_add_close': total_add_close,
        'total_add_open': total_add_open,
        'avg_dau': avg_dau,
        'total_cnt': total_cnt,
        'avg_ratio': avg_ratio
    }

def generate_html_chart(all_data_points, summary_stats, appkey, start_date, end_date):
    """
    生成 HTML 图表报告
    
    Args:
        all_data_points: 所有数据点
        summary_stats: 汇总统计数据
        appkey: 应用 key
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        生成的 HTML 文件路径
    """
    # 读取模板
    template_file = SCRIPT_DIR / "switch_chart_template.html"
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 按日期分组数据
    from collections import defaultdict
    data_by_date = defaultdict(dict)
    for point in all_data_points:
        data_by_date[point['date']][point['type']] = point['value']
    
    # 按日期排序
    sorted_dates = sorted(data_by_date.keys())
    
    # 准备图表数据
    labels = [d for d in sorted_dates]
    addClose_data = [data_by_date[d].get('addClose', 0) or 0 for d in sorted_dates]
    addOpen_data = [data_by_date[d].get('addOpen', 0) or 0 for d in sorted_dates]
    dau_data = [data_by_date[d].get('dau', 0) or 0 for d in sorted_dates]
    ratio_data = [data_by_date[d].get('ratio', 0) or 0 for d in sorted_dates]
    
    # 生成表格行
    table_rows = []
    for date in sorted_dates:
        day_data = data_by_date[date]
        row = f"""<tr>
            <td>{date}</td>
            <td>{format_value(day_data.get('addClose'), 'addClose')}</td>
            <td>{format_value(day_data.get('addOpen'), 'addOpen')}</td>
            <td>{format_value(day_data.get('dau'), 'dau')}</td>
            <td>{format_value(day_data.get('cnt'), 'cnt')}</td>
            <td>{format_value(day_data.get('ratio'), 'ratio')}</td>
        </tr>"""
        table_rows.append(row)
    
    # 替换模板变量
    html_content = template
    html_content = html_content.replace('{{appkey}}', appkey)
    html_content = html_content.replace('{{start_date}}', start_date)
    html_content = html_content.replace('{{end_date}}', end_date)
    html_content = html_content.replace('{{total_add_close}}', f"{int(summary_stats['total_add_close']):,}")
    html_content = html_content.replace('{{total_add_open}}', f"{int(summary_stats['total_add_open']):,}")
    html_content = html_content.replace('{{avg_dau}}', f"{int(summary_stats['avg_dau']):,}")
    html_content = html_content.replace('{{avg_ratio}}', f"{summary_stats['avg_ratio']:.2f}")
    html_content = html_content.replace('{{labels}}', json.dumps(labels))
    html_content = html_content.replace('{{addClose_data}}', json.dumps(addClose_data))
    html_content = html_content.replace('{{addOpen_data}}', json.dumps(addOpen_data))
    html_content = html_content.replace('{{dau_data}}', json.dumps(dau_data))
    html_content = html_content.replace('{{ratio_data}}', json.dumps(ratio_data))
    html_content = html_content.replace('{{table_rows}}', '\n'.join(table_rows))
    html_content = html_content.replace('{{generated_time}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 保存 HTML 文件
    output_dir = SCRIPT_DIR.parent / "reports"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"switch_report_{appkey}_{timestamp}.html"
    output_file = output_dir / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(output_file)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_switch_statistics.py <appkey> [start_date] [end_date]")
        print("")
        print("参数说明:")
        print("  appkey      - 应用的唯一标识（必填）")
        print("  start_date  - 开始日期，格式 yyyy-MM-dd 或自然语言描述（可选，默认 7 天前）")
        print("  end_date    - 结束日期，格式 yyyy-MM-dd 或自然语言描述（可选，默认昨天）")
        print("")
        print("示例:")
        print("  # 查询最近 7 天（默认）")
        print("  python scripts/query_switch_statistics.py EXAMPLE_APPKEY_001")
        print("")
        print("  # 查询过去 30 天")
        print("  python scripts/query_switch_statistics.py EXAMPLE_APPKEY_001 \"过去 30 天\"")
        print("")
        print("  # 查询指定时间段")
        print("  python scripts/query_switch_statistics.py EXAMPLE_APPKEY_001 2026-04-01 2026-04-05")
        print("")
        print("  # 查询昨天")
        print("  python scripts/query_switch_statistics.py EXAMPLE_APPKEY_001 \"昨天\" \"昨天\"")
        sys.exit(1)
    
    appkey = sys.argv[1]
    start_input = sys.argv[2] if len(sys.argv) > 2 else None
    end_input = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 计算日期范围
    try:
        start_date, end_date = calculate_date_range(start_input, end_input)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("🔍 友盟推送 - 开关统计查询")
    print("=" * 80)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {start_date} 至 {end_date}")
    print("=" * 80)
    
    # 依次查询 5 种统计类型
    all_results = {}
    
    for stat_type, type_name in SWITCH_TYPES.items():
        print(f"\n📊 正在查询 {type_name} ({stat_type})...")
        result = query_switch_trend(appkey, start_date, end_date, stat_type)
        
        if result.get('status'):
            print(f"✅ {type_name} 查询成功")
            all_results[stat_type] = result
        else:
            print(f"❌ {type_name} 查询失败：{result.get('msg', '未知错误')}")
            all_results[stat_type] = result
    
    # 展示结果
    display_results(all_results, start_date, end_date)

if __name__ == "__main__":
    main()
