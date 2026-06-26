#!/usr/bin/env python3
"""
竞品分析表格生成器
用法: python3 competitor_analysis.py --products <产品1,产品2> [--output <输出文件>]
"""

import argparse
import sys
import csv
from datetime import datetime

# 功能维度模板
FUNCTION_DIMENSIONS = [
    "账号体系",
    "核心功能",
    "用户界面",
    "交互体验",
    "搜索/筛选",
    "内容质量",
    "社交功能",
    "消息通知",
    "个性化推荐",
    "支付流程",
    "客服支持",
    "性能/稳定性",
    "数据安全",
    "商业模式",
]

# 评分标准
RATING_SCALE = {
    "3": "✅ 有此功能且体验好",
    "2": "⚠️ 有此功能但体验一般",
    "1": "❌ 有此功能但体验差",
    "0": "✗ 没有此功能",
}


def generate_csv(products: list) -> str:
    """生成竞品对比CSV内容"""
    
    output = []
    output.append("# 竞品分析记录")
    output.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append(f"**分析产品**: {', '.join(products)}")
    output.append("")
    output.append("## 功能对比矩阵")
    output.append("")
    
    # CSV表头
    header = ["功能维度"] + products
    output.append(",".join(header))
    
    # 评分标准说明
    output.append("")
    output.append("## 评分标准")
    for score, desc in RATING_SCALE.items():
        output.append(f"- {score}: {desc}")
    
    output.append("")
    output.append("## SWOT分析")
    output.append("")
    output.append("请为每个产品填写以下内容：")
    for product in products:
        output.append(f"""
### {product}

| | **有帮助** | **无帮助** |
|---|---|---|
| **内部** | 优势(S) | 劣势(W) |
| **外部** | 机会(O) | 威胁(T) |
""")
    
    return "\n".join(output)


def generate_markdown_table(products: list) -> str:
    """生成Markdown格式的竞品分析表格"""
    
    header = "| 功能维度 | " + " | ".join(products) + " |"
    separator = "|----------|" + "|".join(["----------" for _ in products]) + "|"
    
    lines = [header, separator]
    
    for dim in FUNCTION_DIMENSIONS:
        row = f"| {dim} | " + " | ".join(["" for _ in products]) + " |"
        lines.append(row)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="竞品分析表格生成器")
    parser.add_argument("--products", required=True, help="竞品名称，逗号分隔")
    parser.add_argument("--output", help="输出文件路径（可选）")
    parser.add_argument("--format", choices=["csv", "markdown"], default="markdown", help="输出格式")
    
    args = parser.parse_args()
    
    products = [p.strip() for p in args.products.split(",")]
    
    if len(products) < 2:
        print("错误: 至少需要2个产品进行对比", file=sys.stderr)
        sys.exit(1)
    
    if args.format == "csv":
        content = generate_csv(products)
    else:
        content = f"""# 竞品分析

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**分析产品**: {', '.join(products)}

## 评分标准

| 分数 | 说明 |
|------|------|
| 3 | ✅ 有此功能且体验好 |
| 2 | ⚠️ 有此功能但体验一般 |
| 1 | ❌ 有此功能但体验差 |
| 0 | ✗ 没有此功能 |

## 功能对比矩阵

{generate_markdown_table(products)}

## 用户评价

| 产品 | App Store | Android | 典型好评 | 典型差评 |
|------|-----------|---------|---------|---------|
| {products[0]} | | | | |

## 商业模式对比

| 产品 | 盈利模式 | 定价 | 用户规模 |
|------|---------|------|---------|
| {products[0]} | | | |

## SWOT分析

### {products[0]}

| | 有帮助 | 无帮助 |
|---|---|---|
| **内部** | 优势 | 劣势 |
| **外部** | 机会 | 威胁 |

## 分析结论

1. [主要发现1]
2. [主要发现2]
3. [主要发现3]

## 差异化机会

| 机会点 | 现有竞品处理方式 | 我们的机会 |
|--------|-----------------|----------|
| | | |
"""
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 竞品分析已保存到: {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
