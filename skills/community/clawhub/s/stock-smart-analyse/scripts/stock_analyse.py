#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PJ选股智能评分12维模型 - 股票分析脚本

基于12个核心维度的股票智能分析评分系统。

用法:
    python stock_analyse.py --stock TSLA --interactive
    python stock_analyse.py --file scores.json
    python stock_analyse.py --stock AAPL --output report.md
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 定义12个评分维度
DIMENSIONS = [
    {
        "id": "industry",
        "name": "行业",
        "name_en": "Industry",
        "weight": 0.15,
        "description": "行业增长率、市场规模增长率等",
        "data_source": "市场研究报告（如Gartner、IDC、Statista等）",
        "criteria": [
            (1, 10, "行业增长率 < 0%；行业处于衰退期，市场需求持续下降"),
            (11, 20, "0% ≤ 行业增长率 < 2%；行业增长缓慢，市场需求有限"),
            (21, 30, "2% ≤ 行业增长率 < 4%；行业增长缓慢，市场需求略有回升"),
            (31, 40, "4% ≤ 行业增长率 < 6%；行业稳定，市场需求平稳"),
            (41, 50, "6% ≤ 行业增长率 < 8%；行业稳定，市场需求略有上升"),
            (51, 60, "8% ≤ 行业增长率 < 10%；行业增长良好，市场需求上升"),
            (61, 70, "10% ≤ 行业增长率 < 12%；行业增长良好，市场需求稳定增长"),
            (71, 80, "12% ≤ 行业增长率 < 15%；行业快速增长，市场需求快速上升"),
            (81, 90, "15% ≤ 行业增长率 < 20%；行业高速增长，市场需求强劲"),
            (91, 100, "行业增长率 ≥ 20%；行业处于巅峰期，市场需求非常旺盛"),
        ]
    },
    {
        "id": "market_leader",
        "name": "头部玩家",
        "name_en": "Market Leader",
        "weight": 0.10,
        "description": "公司在行业中的市场份额、竞争力",
        "data_source": "行业报告、市场份额数据",
        "criteria": [
            (1, 10, "市场份额 < 5%；公司在行业中处于劣势"),
            (11, 20, "5% ≤ 市场份额 < 10%；排名较低，市场份额较小"),
            (21, 30, "10% ≤ 市场份额 < 15%；排名较低，有一定市场份额"),
            (31, 40, "15% ≤ 市场份额 < 20%；有竞争力，市场份额中等"),
            (41, 50, "20% ≤ 市场份额 < 25%；有竞争力，市场份额较高"),
            (51, 60, "25% ≤ 市场份额 < 30%；领先地位，市场份额较大"),
            (61, 70, "30% ≤ 市场份额 < 35%；领先地位，市场份额很大"),
            (71, 80, "35% ≤ 市场份额 < 40%；重要地位，市场份额非常大"),
            (81, 90, "40% ≤ 市场份额 < 50%；主导地位，市场份额巨大"),
            (91, 100, "市场份额 ≥ 50%；绝对主导地位"),
        ]
    },
    {
        "id": "market_environment",
        "name": "市场环境",
        "name_en": "Market Environment",
        "weight": 0.10,
        "description": "宏观经济指标、政策支持、行业法规",
        "data_source": "政府报告、经济数据、政策文件",
        "criteria": [
            (1, 10, "严重不利的政策或经济环境"),
            (11, 20, "不利的政策或经济环境"),
            (21, 30, "略微不利的政策或经济环境"),
            (31, 40, "中性政策或经济环境"),
            (41, 50, "略微有利的政策或经济环境"),
            (51, 60, "有利的政策或经济环境"),
            (61, 70, "较有利的政策或经济环境"),
            (71, 80, "非常有利的政策或经济环境"),
            (81, 90, "极其有利的政策或经济环境"),
            (91, 100, "最有利的政策或经济环境"),
        ]
    },
    {
        "id": "management",
        "name": "管理团队",
        "name_en": "Management Team",
        "weight": 0.10,
        "description": "管理团队的资历、以往业绩、公众评价",
        "data_source": "公司年报、媒体报道、专业评估",
        "criteria": [
            (1, 10, "管理团队缺乏资历和经验；声誉差"),
            (11, 20, "管理团队资历和经验一般；声誉一般"),
            (21, 30, "管理团队资历和经验较好；声誉较好"),
            (31, 40, "管理团队资历和经验良好；有一定经验和声誉"),
            (41, 50, "管理团队资历和经验优秀；声誉良好"),
            (51, 60, "管理团队资历和经验非常优秀；声誉良好"),
            (61, 70, "管理团队有杰出的业绩记录；声誉很好"),
            (71, 80, "管理团队有卓越的业绩记录；声誉很好"),
            (81, 90, "管理团队受到广泛尊重和认可；声誉非常好"),
            (91, 100, "管理团队享有最高声誉"),
        ]
    },
    {
        "id": "market_cap",
        "name": "市值规模",
        "name_en": "Market Cap",
        "weight": 0.05,
        "description": "市值规模",
        "data_source": "股票市场数据（如Bloomberg、Yahoo Finance）",
        "criteria": [
            (1, 10, "市值 < 10亿美元"),
            (11, 20, "10亿美元 ≤ 市值 < 50亿美元"),
            (21, 30, "50亿美元 ≤ 市值 < 100亿美元"),
            (31, 40, "100亿美元 ≤ 市值 < 200亿美元"),
            (41, 50, "200亿美元 ≤ 市值 < 300亿美元"),
            (51, 60, "300亿美元 ≤ 市值 < 400亿美元"),
            (61, 70, "400亿美元 ≤ 市值 < 500亿美元"),
            (71, 80, "500亿美元 ≤ 市值 < 700亿美元"),
            (81, 90, "700亿美元 ≤ 市值 < 1000亿美元"),
            (91, 100, "市值 ≥ 1000亿美元"),
        ]
    },
    {
        "id": "main_business",
        "name": "主营业务",
        "name_en": "Main Business",
        "weight": 0.10,
        "description": "主营业务的市场需求、创新能力、核心竞争力",
        "data_source": "行业报告、公司年报",
        "criteria": [
            (1, 10, "主营业务需求低、缺乏竞争力"),
            (11, 20, "主营业务需求一般、竞争力弱"),
            (21, 30, "主营业务需求有限、竞争力一般"),
            (31, 40, "主营业务需求平稳、竞争力尚可"),
            (41, 50, "主营业务需求略增、竞争力较好"),
            (51, 60, "主营业务需求良好、竞争力强"),
            (61, 70, "主营业务需求稳定增长、竞争力很强"),
            (71, 80, "主营业务需求快速增长、竞争力非常强"),
            (81, 90, "主营业务需求强劲、竞争力极强"),
            (91, 100, "主营业务需求旺盛、竞争力最高"),
        ]
    },
    {
        "id": "revenue",
        "name": "收入",
        "name_en": "Revenue",
        "weight": 0.10,
        "description": "收入增长率和稳定性",
        "data_source": "公司财报、市场分析报告",
        "criteria": [
            (1, 10, "收入增长率 < 0%；不稳定"),
            (11, 20, "0% ≤ 收入增长率 < 5%；较不稳定"),
            (21, 30, "5% ≤ 收入增长率 < 10%；不稳定"),
            (31, 40, "10% ≤ 收入增长率 < 15%；较稳定"),
            (41, 50, "15% ≤ 收入增长率 < 20%；较稳定"),
            (51, 60, "20% ≤ 收入增长率 < 25%；稳定"),
            (61, 70, "25% ≤ 收入增长率 < 30%；稳定"),
            (71, 80, "30% ≤ 收入增长率 < 40%；较稳定"),
            (81, 90, "40% ≤ 收入增长率 < 50%；非常稳定"),
            (91, 100, "收入增长率 ≥ 50%；极其稳定"),
        ]
    },
    {
        "id": "profit",
        "name": "利润",
        "name_en": "Profit",
        "weight": 0.10,
        "description": "利润率和增长率",
        "data_source": "公司财报、市场分析报告",
        "criteria": [
            (1, 10, "利润率 < 5%；增长缓慢或负增长"),
            (11, 20, "5% ≤ 利润率 < 10%；增长缓慢"),
            (21, 30, "10% ≤ 利润率 < 15%；增长缓慢"),
            (31, 40, "15% ≤ 利润率 < 20%；增长平稳"),
            (41, 50, "20% ≤ 利润率 < 25%；增长平稳"),
            (51, 60, "25% ≤ 利润率 < 30%；增长较快"),
            (61, 70, "30% ≤ 利润率 < 35%；增长较快"),
            (71, 80, "35% ≤ 利润率 < 40%；增长非常快"),
            (81, 90, "40% ≤ 利润率 < 50%；增长非常快"),
            (91, 100, "利润率 ≥ 50%；增长极其快"),
        ]
    },
    {
        "id": "dividend",
        "name": "分红",
        "name_en": "Dividend",
        "weight": 0.05,
        "description": "分红率和稳定性",
        "data_source": "公司财报、分红公告",
        "criteria": [
            (1, 10, "无分红"),
            (11, 20, "分红率 < 1%"),
            (21, 30, "1% ≤ 分红率 < 2%；不稳定"),
            (31, 40, "2% ≤ 分红率 < 3%；不稳定"),
            (41, 50, "3% ≤ 分红率 < 4%；较稳定"),
            (51, 60, "4% ≤ 分红率 < 5%；较稳定"),
            (61, 70, "5% ≤ 分红率 < 6%；稳定"),
            (71, 80, "6% ≤ 分红率 < 7%；稳定"),
            (81, 90, "7% ≤ 分红率 < 8%；非常稳定"),
            (91, 100, "分红率 ≥ 8%；极其稳定"),
        ]
    },
    {
        "id": "buyback",
        "name": "回购",
        "name_en": "Buyback",
        "weight": 0.05,
        "description": "回购频率和规模",
        "data_source": "公司公告、财报",
        "criteria": [
            (1, 10, "无回购计划"),
            (11, 20, "回购金额 < 1亿美元；频度低，规模小"),
            (21, 30, "1亿 ≤ 回购金额 < 2亿美元；频率低，规模中等"),
            (31, 40, "2亿 ≤ 回购金额 < 3亿美元；频率适中"),
            (41, 50, "3亿 ≤ 回购金额 < 4亿美元；频率适中，规模较大"),
            (51, 60, "4亿 ≤ 回购金额 < 5亿美元；频率较高"),
            (61, 70, "5亿 ≤ 回购金额 < 6亿美元；频率较高，规模很大"),
            (71, 80, "6亿 ≤ 回购金额 < 7亿美元；频率非常高"),
            (81, 90, "7亿 ≤ 回购金额 < 8亿美元；频率极高"),
            (91, 100, "回购金额 ≥ 8亿美元；频率极高，规模最大"),
        ]
    },
    {
        "id": "institutional",
        "name": "机构持股",
        "name_en": "Institutional Holding",
        "weight": 0.05,
        "description": "机构持股比例和变动",
        "data_source": "机构持股报告（如13F文件）、市场分析",
        "criteria": [
            (1, 10, "机构持股 < 10%；无明显变动"),
            (11, 20, "10% ≤ 机构持股 < 20%；变动不大"),
            (21, 30, "20% ≤ 机构持股 < 30%；变动不大"),
            (31, 40, "30% ≤ 机构持股 < 40%；小幅增长"),
            (41, 50, "40% ≤ 机构持股 < 50%；小幅增长"),
            (51, 60, "50% ≤ 机构持股 < 60%；显著增长"),
            (61, 70, "60% ≤ 机构持股 < 70%；增长明显"),
            (71, 80, "70% ≤ 机构持股 < 80%；增长明显"),
            (81, 90, "80% ≤ 机构持股 < 90%；增长显著"),
            (91, 100, "机构持股 ≥ 90%；增长显著"),
        ]
    },
    {
        "id": "major_shareholder",
        "name": "大股东增减持",
        "name_en": "Major Shareholder",
        "weight": 0.05,
        "description": "大股东的增持或减持行为及其影响",
        "data_source": "公司公告、市场分析",
        "criteria": [
            (1, 10, "大股东显著减持（> 10%）"),
            (11, 20, "大股东减持（5%-10%）"),
            (21, 30, "大股东小幅减持（2%-5%）"),
            (31, 40, "大股东微幅减持（< 2%）"),
            (41, 50, "大股东持股未变"),
            (51, 60, "大股东持股未变"),
            (61, 70, "大股东小幅增持（< 2%）"),
            (71, 80, "大股东小幅增持（2%-5%）"),
            (81, 90, "大股东增持（5%-10%）"),
            (91, 100, "大股东显著增持（> 10%）"),
        ]
    },
]


def get_rating(score):
    """根据得分返回评级"""
    if score >= 90:
        return "强烈推荐买入", "⭐⭐⭐⭐⭐"
    elif score >= 80:
        return "推荐买入", "⭐⭐⭐⭐"
    elif score >= 70:
        return "建议持有", "⭐⭐⭐"
    elif score >= 60:
        return "谨慎观望", "⭐⭐"
    else:
        return "不建议投资", "⭐"


def validate_score(score):
    """验证分数是否在有效范围内"""
    return 1 <= score <= 100


def interactive_input():
    """交互式输入各维度得分"""
    scores = {}
    print("\n" + "=" * 60)
    print("PJ选股智能评分12维模型 - 交互式评分")
    print("=" * 60)
    
    for dim in DIMENSIONS:
        print(f"\n【{dim['name']}】(权重: {dim['weight']*100:.0f}%)")
        print(f"描述: {dim['description']}")
        print(f"数据来源: {dim['data_source']}")
        print("\n评分标准:")
        for min_score, max_score, desc in dim['criteria']:
            print(f"  {min_score:3d}-{max_score:3d}分: {desc}")
        
        while True:
            try:
                score = int(input(f"\n请输入{dim['name']}得分 (1-100): "))
                if validate_score(score):
                    scores[dim['id']] = score
                    break
                else:
                    print("分数必须在 1-100 之间，请重新输入。")
            except ValueError:
                print("请输入有效的数字。")
    
    return scores


def calculate_total_score(scores):
    """计算综合得分"""
    total = 0
    details = []
    
    for dim in DIMENSIONS:
        dim_id = dim['id']
        score = scores.get(dim_id, 50)  # 默认50分
        weighted_score = score * dim['weight']
        total += weighted_score
        details.append({
            'id': dim_id,
            'name': dim['name'],
            'score': score,
            'weight': dim['weight'],
            'weighted_score': weighted_score
        })
    
    return round(total, 2), details


def generate_report(stock_code, scores, output_format='markdown'):
    """生成分析报告"""
    total_score, details = calculate_total_score(scores)
    rating, stars = get_rating(total_score)
    
    if output_format == 'json':
        return json.dumps({
            'stock': stock_code,
            'total_score': total_score,
            'rating': rating,
            'stars': stars,
            'dimensions': {d['id']: {'score': d['score'], 'weight': d['weight']} for d in details},
            'analyzed_at': datetime.now().isoformat()
        }, ensure_ascii=False, indent=2)
    
    # Markdown格式
    report = f"""# 股票分析报告：{stock_code}

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 综合得分：{total_score}分

**评级**: {rating} {stars}

---

## 各维度得分明细

| 维度 | 得分 | 权重 | 加权得分 | 评价 |
|------|------|------|---------|------|
"""
    
    for d in details:
        # 根据得分给出评价
        if d['score'] >= 80:
            eval_text = "优秀"
        elif d['score'] >= 60:
            eval_text = "良好"
        elif d['score'] >= 40:
            eval_text = "一般"
        else:
            eval_text = "较弱"
        
        report += f"| {d['name']} | {d['score']} | {d['weight']*100:.0f}% | {d['weighted_score']:.2f} | {eval_text} |\n"
    
    report += f"| **合计** | - | **100%** | **{total_score}** | **{rating}** |\n"
    
    # 添加建议
    report += f"""
---

## 分析建议

"""
    
    # 找出优势和劣势
    sorted_details = sorted(details, key=lambda x: x['score'], reverse=True)
    strengths = sorted_details[:3]
    weaknesses = sorted_details[-3:]
    
    report += "### 优势维度\n"
    for s in strengths:
        report += f"- **{s['name']}**: {s['score']}分 (加权 {s['weighted_score']:.2f})\n"
    
    report += "\n### 关注维度\n"
    for w in weaknesses:
        report += f"- **{w['name']}**: {w['score']}分 (加权 {w['weighted_score']:.2f})\n"
    
    # 根据得分给出建议
    if total_score >= 80:
        report += "\n**综合建议**: 该股票综合表现优秀，建议重点关注，可考虑买入或加仓。\n"
    elif total_score >= 70:
        report += "\n**综合建议**: 该股票整体表现良好，可继续持有观察，注意市场变化。\n"
    elif total_score >= 60:
        report += "\n**综合建议**: 该股票表现一般，建议谨慎观望，可考虑减仓或观望。\n"
    else:
        report += "\n**综合建议**: 该股票综合表现较弱，建议谨慎投资或考虑退出。\n"
    
    report += "\n---\n\n*本报告由PJ选股智能评分12维模型生成，仅供参考，不构成投资建议。*\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='PJ选股智能评分12维模型')
    parser.add_argument('--stock', '-s', type=str, help='股票代码')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式输入')
    parser.add_argument('--file', '-f', type=str, help='从JSON文件读取评分数据')
    parser.add_argument('--output', '-o', type=str, help='输出报告路径')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='输出格式')
    
    args = parser.parse_args()
    
    scores = {}
    stock_code = args.stock or "UNKNOWN"
    
    if args.file:
        # 从文件读取
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            stock_code = data.get('stock', stock_code)
            scores = data.get('scores', data.get('dimensions', {}))
    elif args.interactive:
        # 交互式输入
        scores = interactive_input()
    else:
        # 显示帮助
        print(__doc__)
        print("\n可用的评分维度:")
        for dim in DIMENSIONS:
            print(f"  - {dim['name']} ({dim['id']}): 权重 {dim['weight']*100:.0f}%")
        sys.exit(0)
    
    # 生成报告
    report = generate_report(stock_code, scores, args.format)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"[OK] 报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
