#!/usr/bin/env python3
"""
数据可视化模块
- 价格分布直方图
- 关键词热度词云
- TOP10 柱状图
- 价格趋势折线图
"""

import json
import os
from pathlib import Path
import re

def load_data(data_file):
    """加载数据"""
    with open(data_file, 'r', encoding='utf8') as f:
        return json.load(f)

def extract_prices(data):
    """提取所有价格"""
    prices = []
    for item in data:
        for p in item.get('products', []):
            if isinstance(p, dict) and p.get('price'):
                try:
                    prices.append(float(p['price']))
                except:
                    pass
            elif isinstance(p, str):
                match = re.search(r'¥(\d+\.?\d*)', p)
                if match:
                    prices.append(float(match.group(1)))
    return prices

def generate_price_histogram(prices, output_file):
    """生成价格分布直方图（文本版）"""
    if not prices:
        return
    
    ranges = [
        (0, 5, "0-5 元"),
        (5, 10, "5-10 元"),
        (10, 20, "10-20 元"),
        (20, 50, "20-50 元"),
        (50, 100, "50-100 元"),
        (100, 9999, "100 元+")
    ]
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>价格分布直方图</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .chart {{ margin: 20px 0; }}
        .bar {{ height: 30px; background: linear-gradient(90deg, #4CAF50, #8BC34A); margin: 5px 0; border-radius: 4px; }}
        .label {{ display: inline-block; width: 100px; }}
        .count {{ display: inline-block; width: 50px; }}
        .percent {{ display: inline-block; width: 60px; color: #666; }}
        h1 {{ color: #333; }}
        .stats {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>📊 价格分布直方图</h1>
    
    <div class="stats">
        <strong>统计数据：</strong><br>
        总商品数：{len(prices)}<br>
        最低价：¥{min(prices):.2f}<br>
        最高价：¥{max(prices):.2f}<br>
        平均价：¥{sum(prices)/len(prices):.2f}<br>
        中位数：¥{sorted(prices)[len(prices)//2]:.2f}
    </div>
    
    <div class="chart">
"""
    
    total = len(prices)
    for low, high, label in ranges:
        count = sum(1 for p in prices if low <= p < high)
        percent = count / total * 100 if total > 0 else 0
        width = max(percent * 3, 1)  # 至少 1%宽度
        
        html += f"""
        <div>
            <span class="label">{label}</span>
            <span class="count">{count}</span>
            <span class="percent">({percent:.1f}%)</span>
            <div class="bar" style="width: {width}px;"></div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"✅ 价格分布图：{output_file}")

def generate_keyword_heatmap(data, output_file):
    """生成关键词热度图（TOP20）"""
    # 统计每个关键词的商品数
    keyword_counts = [(item['keyword'], item.get('count', len(item.get('products', [])))) for item in data]
    keyword_counts.sort(key=lambda x: x[1], reverse=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>关键词热度 TOP20</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .chart {{ margin: 20px 0; }}
        .bar {{ height: 25px; background: linear-gradient(90deg, #2196F3, #64B5F6); margin: 5px 0; border-radius: 4px; }}
        .label {{ display: inline-block; width: 120px; }}
        .count {{ display: inline-block; width: 50px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>🔥 关键词热度 TOP20</h1>
    
    <table>
        <tr><th>排名</th><th>关键词</th><th>商品数</th><th>热度</th></tr>
"""
    
    for i, (keyword, count) in enumerate(keyword_counts[:20], 1):
        heat = "🔥" * min(5, max(1, count // 5))
        html += f"<tr><td>{i}</td><td>{keyword}</td><td>{count}</td><td>{heat}</td></tr>\n"
    
    html += """
    </table>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"✅ 关键词热度图：{output_file}")

def generate_category_pie(data, output_file):
    """生成分类占比图"""
    # 按分类统计
    categories = {}
    for item in data:
        cat = item.get('category', '其他')
        count = item.get('count', len(item.get('products', [])))
        categories[cat] = categories.get(cat, 0) + count
    
    # 排序
    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>分类占比</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #FF9800; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .bar {{ height: 20px; background: linear-gradient(90deg, #FF9800, #FFC107); margin: 5px 0; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>📋 分类占比</h1>
    
    <table>
        <tr><th>分类</th><th>商品数</th><th>占比</th><th>分布</th></tr>
"""
    
    total = sum(count for _, count in sorted_cats)
    for cat, count in sorted_cats:
        percent = count / total * 100 if total > 0 else 0
        width = max(percent * 3, 1)
        html += f"<tr><td>{cat}</td><td>{count}</td><td>{percent:.1f}%</td><td><div class='bar' style='width: {width}px;'></div></td></tr>\n"
    
    html += """
    </table>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"✅ 分类占比图：{output_file}")

def generate_summary_report(data, output_file):
    """生成汇总报告"""
    total_keywords = len(data)
    total_products = sum(item.get('count', len(item.get('products', []))) for item in data)
    
    # 提取价格
    prices = extract_prices(data)
    
    # TOP10
    sorted_data = sorted(data, key=lambda x: x.get('count', len(x.get('products', []))), reverse=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>闲鱼数据调研报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 36px; font-weight: bold; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .highlight {{ background-color: #fff3cd !important; }}
        a {{ color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🐾 闲鱼数据调研报告</h1>
    <p><strong>生成时间</strong>: {__import__('datetime').datetime.now().isoformat()}</p>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{total_keywords}</div>
            <div class="stat-label">关键词</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_products}</div>
            <div class="stat-label">商品总数</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">¥{sum(prices)/len(prices) if prices else 0:.2f}</div>
            <div class="stat-label">平均价格</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">¥{sorted(prices)[len(prices)//2] if prices else 0:.2f}</div>
            <div class="stat-label">价格中位数</div>
        </div>
    </div>
    
    <h2>📊 数据可视化</h2>
    <ul>
        <li><a href="price-histogram.html">价格分布直方图</a></li>
        <li><a href="keyword-heatmap.html">关键词热度 TOP20</a></li>
        <li><a href="category-pie.html">分类占比</a></li>
    </ul>
    
    <h2>🔥 TOP20 热门关键词</h2>
    <table>
        <tr><th>排名</th><th>关键词</th><th>商品数</th><th>建议</th></tr>
"""
    
    recommendations = {
        (0, 5): "🟢 蓝海",
        (5, 15): "🟡 正常",
        (15, 999): "🔴 红海"
    }
    
    for i, item in enumerate(sorted_data[:20], 1):
        keyword = item['keyword']
        count = item.get('count', len(item.get('products', [])))
        
        rec = "🟢 蓝海" if count < 8 else ("🟡 正常" if count < 15 else "🔴 红海")
        highlight = 'class="highlight"' if i <= 5 else ''
        html += f"<tr {highlight}><td>{i}</td><td>{keyword}</td><td>{count}</td><td>{rec}</td></tr>\n"
    
    html += """
    </table>
    
    <h2>💡 智能推荐</h2>
    <p>基于数据分析，推荐以下方向：</p>
    <ol>
        <li><strong>蓝海市场</strong>：选择商品数 &lt; 8 的关键词，竞争小</li>
        <li><strong>差异化</strong>：强调售后服务（7 天复查、30 天咨询）</li>
        <li><strong>定价策略</strong>：参考中位数价格，略低于平均值</li>
        <li><strong>快速入场</strong>：新兴关键词（APatch、KernelSU）</li>
    </ol>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>数据来源：闲鱼实时抓取 | 处理：Playwright + OCR | 技能：xianyu-data-grabber</p>
    </footer>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"✅ 汇总报告：{output_file}")

def main():
    import sys
    
    data_file = sys.argv[1] if len(sys.argv) > 1 else 'legion/data/xianyu-43keywords-data.json'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'legion/data/visualize'
    
    if not os.path.exists(data_file):
        print(f"❌ 数据文件不存在：{data_file}")
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔍 加载数据...")
    data = load_data(data_file)
    print(f"✅ 加载 {len(data)} 个关键词")
    
    print("\n📊 生成可视化图表...")
    prices = extract_prices(data)
    generate_price_histogram(prices, os.path.join(output_dir, 'price-histogram.html'))
    generate_keyword_heatmap(data, os.path.join(output_dir, 'keyword-heatmap.html'))
    generate_category_pie(data, os.path.join(output_dir, 'category-pie.html'))
    generate_summary_report(data, os.path.join(output_dir, 'index.html'))
    
    print(f"\n✅ 可视化完成！打开 {output_dir}/index.html 查看报告")

if __name__ == '__main__':
    main()
