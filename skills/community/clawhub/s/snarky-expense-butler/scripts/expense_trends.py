#!/usr/bin/env python3
# 消费趋势图生成工具
# 优先使用大模型生成图片，matplotlib 兜底

import json
import sys
import os
import datetime
from datetime import timedelta
import calendar

DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expense_records.json'))
TRENDS_DIR = os.environ.get('EXPENSE_TRENDS_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trends'))

def load_data():
    """加载消费记录数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_openrouter_api_key():
    """尝试获取 OpenRouter API Key"""
    # 优先从环境变量读取
    key = os.environ.get('OPENROUTER_API_KEY', '')
    if key:
        return key
    # 尝试从 openclaw.json 读取
    try:
        config_path = os.path.expanduser('~/.openclaw/openclaw.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        # 尝试从 auth profiles 获取
        profiles = config.get('auth', {}).get('profiles', {})
        for name, profile in profiles.items():
            if 'openrouter' in name.lower():
                # The key is in system keychain, not directly accessible
                pass
    except Exception:
        pass
    return None

def get_week_data(data):
    """获取本周每天的消费数据"""
    today = datetime.datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    week_labels = [(start_of_week + timedelta(days=i)).strftime('%m/%d\n%a') for i in range(7)]

    amounts = []
    for date in week_dates:
        total = 0
        for record in data['records']:
            if record['date'] == date:
                total = record['total']
                break
        amounts.append(total)

    return week_labels, amounts, week_dates

def get_month_data(data):
    """获取本月每天的消费数据"""
    today = datetime.datetime.now()
    month_str = today.strftime('%Y-%m')
    _, days_in_month = calendar.monthrange(today.year, today.month)

    labels = []
    amounts = []
    for day in range(1, days_in_month + 1):
        date_str = f"{month_str}-{day:02d}"
        labels.append(str(day))
        total = 0
        for record in data['records']:
            if record['date'] == date_str:
                total = record['total']
                break
        amounts.append(total)

    return labels, amounts

def get_year_data(data):
    """获取本年每月的消费数据"""
    today = datetime.datetime.now()
    year = today.year

    labels = []
    amounts = []
    for month in range(1, 13):
        labels.append(f"{month}月")
        month_str = f"{year}-{month:02d}"
        total = 0
        for record in data['records']:
            if record['date'].startswith(month_str):
                total += round(sum(-item['amount'] for item in record['items']), 2)
        amounts.append(round(total, 2))

    return labels, amounts

def generate_with_llm(period, labels, amounts, output_path):
    """尝试用大模型生成趋势图"""
    api_key = get_openrouter_api_key()
    if not api_key:
        print("  ℹ️ 未找到 OPENROUTER_API_KEY，跳过大模型方案")
        return False

    try:
        import requests

        period_names = {'week': '本周', 'month': '本月', 'year': '本年'}
        period_name = period_names.get(period, period)

        # 构建数据描述
        data_desc = ""
        for label, amount in zip(labels, amounts):
            label_clean = label.replace('\n', ' ')
            data_desc += f"  {label_clean}: ¥{amount:.1f}\n"

        prompt = (
            f"请根据以下消费数据生成一张简洁美观的趋势图，图表标题为'{period_name}消费趋势'。\n"
            f"数据如下（标签: 金额）：\n{data_desc}\n"
            f"要求：使用中文字体，图表类型为柱状图（可叠加折线），背景简洁，有网格线，"
            f"Y轴标注金额（单位：元），X轴标注时间标签。配色使用柔和的蓝色系。"
            f"输出为图片，不要输出代码。"
        )

        # 用 OpenRouter 调用支持图片的模型
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            # Check if the model returned an image
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            if content and len(content) > 10:
                print("  ℹ️ 大模型返回了文本描述而非图片，降级到 matplotlib")
                return False
            print("  ℹ️ 大模型响应格式不包含图片，降级到 matplotlib")
            return False
        else:
            print(f"  ⚠️ 大模型 API 返回 {response.status_code}，降级到 matplotlib")
            return False

    except Exception as e:
        print(f"  ⚠️ 大模型生成失败: {e}，降级到 matplotlib")
        return False

def generate_with_matplotlib(period, labels, amounts, output_path):
    """使用 matplotlib 生成趋势图"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # 尝试设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'STHeiti', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    period_names = {'week': '本周消费趋势', 'month': '本月消费趋势', 'year': '本年消费趋势'}
    title = period_names.get(period, f'{period}消费趋势')

    fig, ax = plt.subplots(figsize=(12, 6) if period != 'week' else (10, 6))

    # 颜色
    bar_color = '#4A90D9'
    line_color = '#E85D5D'

    # 柱状图
    bars = ax.bar(range(len(labels)), amounts, color=bar_color, alpha=0.7, width=0.6, label='消费金额')

    # 折线图
    ax.plot(range(len(labels)), amounts, color=line_color, marker='o', linewidth=2, markersize=6, label='趋势线')

    # 在每个柱子上显示金额
    for i, (bar, amount) in enumerate(zip(bars, amounts)):
        if amount > 0:
            ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + max(amounts) * 0.02,
                    f'¥{amount:.0f}', ha='center', va='bottom', fontsize=9)

    # 标签和标题
    ax.set_xticks(range(len(labels)))
    if period == 'week':
        ax.set_xticklabels(labels, fontsize=10)
    elif period == 'month':
        # 每隔几天显示一个标签，避免拥挤
        step = max(1, len(labels) // 15)
        ax.set_xticks(range(0, len(labels), step))
        ax.set_xticklabels([labels[i] for i in range(0, len(labels), step)], fontsize=9)
    else:
        ax.set_xticklabels(labels, fontsize=10)

    ax.set_ylabel('金额（元）', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')

    # 设置 Y 轴从 0 开始
    ax.set_ylim(bottom=0)

    # 添加均值线
    avg = round(sum(amounts) / len(amounts), 2) if amounts else 0
    ax.axhline(y=avg, color='#FFA500', linestyle='--', linewidth=1, alpha=0.7, label=f'均值: ¥{avg}')
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return True

def main():
    if len(sys.argv) < 2:
        print("📊 消费趋势图生成工具")
        print("用法: python3 expense_trends.py <命令>")
        print()
        print("命令:")
        print("  week   - 周趋势图（7天）")
        print("  month  - 月趋势图（31天）")
        print("  year   - 年趋势图（12个月）")
        sys.exit(0)

    period = sys.argv[1]

    # 确保 trends 目录存在
    os.makedirs(TRENDS_DIR, exist_ok=True)

    data = load_data()
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')

    if period == 'week':
        labels, amounts, _ = get_week_data(data)
        filename = f'week_trend_{today_str}.png'
    elif period == 'month':
        labels, amounts = get_month_data(data)
        filename = f'month_trend_{today_str}.png'
    elif period == 'year':
        labels, amounts = get_year_data(data)
        filename = f'year_trend_{today_str}.png'
    else:
        print(f"❌ 未知命令: {period}")
        print("支持: week, month, year")
        sys.exit(1)

    output_path = os.path.join(TRENDS_DIR, filename)

    # 优先用大模型
    print(f"🎨 正在生成 {period} 趋势图...")
    success = generate_with_llm(period, labels, amounts, output_path)

    # 大模型失败，用 matplotlib 兜底
    if not success:
        print("  📊 使用 matplotlib 生成...")
        success = generate_with_matplotlib(period, labels, amounts, output_path)

    if success:
        print(f"✅ 趋势图已生成: {output_path}")
    else:
        print("❌ 趋势图生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
