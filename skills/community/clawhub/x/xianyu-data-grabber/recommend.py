#!/usr/bin/env python3
"""
智能推荐模块
- 推荐最优商品
- 推荐定价策略
- 预计销量和利润
- 生成行动建议
"""

import json
import sys
import os
from datetime import datetime

def load_data(data_file):
    with open(data_file, 'r', encoding='utf8') as f:
        return json.load(f)

def analyze_market(data):
    """分析市场数据"""
    recommendations = []
    
    for item in data:
        keyword = item['keyword']
        count = item.get('count', len(item.get('products', [])))
        products = item.get('products', [])
        
        # 提取价格
        prices = []
        for p in products:
            if isinstance(p, dict) and p.get('price'):
                try:
                    prices.append(float(p['price']))
                except:
                    pass
        
        # 计算指标
        avg_price = sum(prices) / len(prices) if prices else 0
        median_price = sorted(prices)[len(prices)//2] if prices else 0
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        
        # 竞争度评估
        if count < 8:
            competition = "低"
            score = 90
        elif count < 15:
            competition = "中"
            score = 70
        else:
            competition = "高"
            score = 50
        
        # 需求评估（基于商品数，假设商品多=需求大）
        if count > 20:
            demand = "高"
        elif count > 10:
            demand = "中"
        else:
            demand = "低"
        
        # 推荐指数
        recommendation_score = score * 0.6 + (100 if demand == "高" else (70 if demand == "中" else 50)) * 0.4
        
        # 定价建议
        if avg_price > 0:
            suggested_price = median_price * 0.9  # 略低于中位数
        else:
            suggested_price = 19.9  # 默认价格
        
        # 预计销量（简单估算）
        if competition == "低" and demand in ["中", "高"]:
            estimated_sales = (80, 150)
        elif competition == "中":
            estimated_sales = (30, 80)
        else:
            estimated_sales = (10, 40)
        
        # 预计利润
        profit_margin = 0.6  # 60% 利润率（虚拟商品）
        estimated_profit = (
            estimated_sales[0] * suggested_price * profit_margin,
            estimated_sales[1] * suggested_price * profit_margin
        )
        
        recommendations.append({
            'keyword': keyword,
            'competition': competition,
            'demand': demand,
            'product_count': count,
            'avg_price': avg_price,
            'median_price': median_price,
            'suggested_price': round(suggested_price, 2),
            'recommendation_score': round(recommendation_score, 1),
            'estimated_sales': estimated_sales,
            'estimated_profit': (round(estimated_profit[0], 2), round(estimated_profit[1], 2)),
            'action': get_action_suggestion(keyword, competition, demand, count)
        })
    
    # 按推荐指数排序
    recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
    
    return recommendations

def get_action_suggestion(keyword, competition, demand, count):
    """生成行动建议"""
    suggestions = []
    
    if competition == "低" and demand in ["中", "高"]:
        suggestions.append("🟢 强烈推荐 - 蓝海市场，尽快入场")
    elif competition == "中" and demand == "高":
        suggestions.append("🟡 推荐 - 需求大但竞争适中，差异化竞争")
    elif competition == "高":
        suggestions.append("🔴 谨慎 - 竞争激烈，需明显差异化")
    else:
        suggestions.append("⚪ 观察 - 需求不明确，建议调研")
    
    # 具体建议
    if "Magisk" in keyword or "面具" in keyword:
        suggestions.append("💡 建议：搭配模块合集，强调 24h 自动发货")
    if "救砖" in keyword or "基带" in keyword:
        suggestions.append("💡 建议：强调技术实力，定价可偏高")
    if "隐藏" in keyword or "Shamiko" in keyword:
        suggestions.append("💡 建议：强调兼容性和售后")
    if "刷机" in keyword or "ROM" in keyword:
        suggestions.append("💡 建议：提供教程 + 远程协助套餐")
    
    return suggestions

def generate_report(recommendations, output_file):
    """生成推荐报告"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>智能推荐报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .card.top {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .score {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .price {{ font-size: 20px; color: #FF9800; }}
        .profit {{ font-size: 18px; color: #2196F3; }}
        .tag {{ display: inline-block; padding: 3px 8px; border-radius: 4px; margin: 2px; font-size: 12px; }}
        .tag-low {{ background: #4CAF50; color: white; }}
        .tag-mid {{ background: #FFC107; color: black; }}
        .tag-high {{ background: #F44336; color: white; }}
        .suggestion {{ background: #E3F2FD; padding: 10px; border-left: 4px solid #2196F3; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>🤖 智能推荐报告</h1>
    <p><strong>生成时间</strong>: {datetime.now().isoformat()}</p>
    <p><strong>分析商品数</strong>: {sum(r['product_count'] for r in recommendations)} 个</p>
    
    <h2>🏆 TOP5 推荐商品</h2>
"""
    
    for i, rec in enumerate(recommendations[:5], 1):
        comp_class = "low" if rec['competition'] == "低" else ("mid" if rec['competition'] == "中" else "high")
        
        html += f"""
    <div class="card {'top' if i == 1 else ''}">
        <h3>{i}. {rec['keyword']}</h3>
        <p>
            <span class="score">推荐指数：{rec['recommendation_score']}</span> | 
            竞争度：<span class="tag tag-{comp_class}">{rec['competition']}</span> | 
            需求：<span class="tag tag-{comp_class}">{rec['demand']}</span>
        </p>
        <p>
            <strong>当前市场</strong>: {rec['product_count']} 个商品 | 
            <strong>平均价格</strong>: <span class="price">¥{rec['avg_price']:.2f}</span> | 
            <strong>中位价格</strong>: <span class="price">¥{rec['median_price']:.2f}</span>
        </p>
        <p>
            <strong>建议定价</strong>: <span class="price">¥{rec['suggested_price']}</span> | 
            <strong>预计销量</strong>: {rec['estimated_sales'][0]}-{rec['estimated_sales'][1]} 单/月 | 
            <strong>预计利润</strong>: <span class="profit">¥{rec['estimated_profit'][0]}-{rec['estimated_profit'][1]}</span>
        </p>
        <div class="suggestion">
            <strong>💡 行动建议</strong>:<br>
            {'<br>'.join(rec['action'])}
        </div>
    </div>
"""
    
    html += """
    <h2>📊 完整推荐列表</h2>
    <table>
        <tr><th>排名</th><th>关键词</th><th>推荐指数</th><th>竞争度</th><th>需求</th><th>建议定价</th><th>预计利润</th></tr>
"""
    
    for i, rec in enumerate(recommendations, 1):
        comp_class = "low" if rec['competition'] == "低" else ("mid" if rec['competition'] == "中" else "high")
        html += f"<tr><td>{i}</td><td>{rec['keyword']}</td><td>{rec['recommendation_score']}</td><td><span class='tag tag-{comp_class}'>{rec['competition']}</span></td><td>{rec['demand']}</td><td>¥{rec['suggested_price']}</td><td>¥{rec['estimated_profit'][0]}-{rec['estimated_profit'][1]}</td></tr>\n"
    
    html += """
    </table>
    
    <h2>💡 总体建议</h2>
    <div class="suggestion">
        <strong>选品策略</strong>:<br>
        1. 优先选择推荐指数 > 70 的关键词<br>
        2. 避开竞争度"高"的红海市场<br>
        3. 关注新兴技术词（APatch、KernelSU）<br><br>
        
        <strong>定价策略</strong>:<br>
        1. 参考中位数价格，略低 10% 吸引流量<br>
        2. 设置多档位（引流款/主力款/利润款）<br>
        3. 虚拟商品可设置自动发货提高转化<br><br>
        
        <strong>差异化策略</strong>:<br>
        1. 强调售后服务（7 天复查、30 天咨询）<br>
        2. 提供教程 + 远程协助套餐<br>
        3. 快速响应（5 分钟内回复）<br><br>
        
        <strong>行动建议</strong>:<br>
        1. 立即上架 TOP3 推荐商品<br>
        2. 每日擦亮 3 次（9:00/14:00/20:00）<br>
        3. 记录数据，1 周后优化<br>
    </div>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>数据来源：闲鱼实时抓取 | 推荐算法：基于竞争度 + 需求分析 | 技能：xianyu-data-grabber</p>
    </footer>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(html)
    
    print(f"✅ 推荐报告：{output_file}")

def main():
    data_file = sys.argv[1] if len(sys.argv) > 1 else 'legion/data/xianyu-43keywords-data.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'legion/data/recommendation-report.html'
    
    if not data_file or not os.path.exists(data_file):
        print(f"❌ 数据文件不存在：{data_file}")
        sys.exit(1)
    
    print("🔍 加载数据...")
    data = load_data(data_file)
    print(f"✅ 加载 {len(data)} 个关键词")
    
    print("\n🤖 分析市场数据...")
    recommendations = analyze_market(data)
    
    print("\n📊 生成推荐报告...")
    generate_report(recommendations, output_file)
    
    # 打印 TOP5
    print("\n🏆 TOP5 推荐商品:")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"  {i}. {rec['keyword']} - 推荐指数：{rec['recommendation_score']} - 建议定价：¥{rec['suggested_price']} - 预计利润：¥{rec['estimated_profit'][0]}-{rec['estimated_profit'][1]}")
    
    print(f"\n✅ 完成！打开 {output_file} 查看详细报告")

if __name__ == '__main__':
    main()
