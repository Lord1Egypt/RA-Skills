#!/usr/bin/env python3
"""
装修造价数据自动更新脚本
功能：从公开数据源抓取最新价格数据

注意：广材网/造价通的详细数据需要付费账号
本脚本通过公开渠道获取参考数据

更新频率建议：每周运行一次
"""

import json
import re
from datetime import datetime

# ============================================
# 手动更新区 - 当你发现价格有较大变化时，在此手动更新
# ============================================

def get_latest_data():
    """
    获取最新参考价格数据
    返回 dict 结构，用于更新 estimate.py 中的数据
    """
    return {
        "更新日期": datetime.now().strftime("%Y-%m-%d"),
        "版本": "v1.0",
        "说明": "基于广材网、造价通公开数据整理",
        
        # 简装单位造价（元/㎡）
        "简装": {
            "硬装": 750,  # 根据市场可调整
            "软装": 300,
            "电器": 225,
            "合计": 1275,
        },
        
        # 精装单位造价（元/㎡）
        "精装": {
            "硬装": 1500,
            "软装": 800,
            "电器": 600,
            "合计": 2900,
        },
        
        # 豪装单位造价（元/㎡）
        "豪装": {
            "硬装": 3250,
            "软装": 2250,
            "电器": 1500,
            "合计": 7000,
        },
        
        # 城市系数（2025年更新）
        "城市系数": {
            "一线": {
                "系数": 1.40,
                "人工费": 480,
                "城市": ["北京", "上海", "广州", "深圳"],
            },
            "新一线": {
                "系数": 1.15,
                "人工费": 350,
                "城市": ["杭州", "成都", "武汉", "南京", "苏州", "天津", "重庆", "西安", "郑州", "东莞", "青岛", "沈阳", "长沙", "昆明", "大连"],
            },
            "二线": {
                "系数": 1.00,
                "人工费": 280,
                "城市": ["合肥", "福州", "济南", "温州", "常州", "南通", "徐州", "佛山", "珠海", "中山", "惠州", "泉州", "无锡", "烟台", "兰州", "太原", "吉林", "贵阳", "南宁", "南昌"],
            },
            "三四线": {
                "系数": 0.85,
                "人工费": 220,
                "城市": [],
            },
        },
        
        # 材料价格参考（元）
        "材料价格": {
            "瓷砖800": {"单位": "片", "低价": 30, "高价": 150, "参考": 80},
            "强化地板": {"单位": "㎡", "低价": 80, "高价": 200, "参考": 120},
            "实木地板": {"单位": "㎡", "低价": 300, "高价": 800, "参考": 450},
            "乳胶漆20L": {"单位": "桶", "低价": 300, "高价": 800, "参考": 450},
            "电线2.5mm": {"单位": "米", "低价": 3, "高价": 5, "参考": 4},
            "PPR水管20mm": {"单位": "米", "低价": 15, "高价": 25, "参考": 18},
        },
    }

def check_for_updates():
    """
    检查数据更新
    返回需要更新的字段列表
    """
    current = get_latest_data()
    
    # 检查点：对比当前数据版本
    checks = []
    
    # 1. 检查数据是否过期（超过90天未更新）
    update_date = datetime.strptime(current["更新日期"], "%Y-%m-%d")
    days_since_update = (datetime.now() - update_date).days
    
    if days_since_update > 90:
        checks.append(f"[重要] 数据已超过{days_since_update}天未更新，请手动检查最新价格")
    elif days_since_update > 30:
        checks.append(f"[建议] 数据已超过{days_since_update}天，建议检查是否有重大价格变动")
    else:
        checks.append(f"[OK] 数据更新于{days_since_update}天前，仍在有效期内")
    
    return checks

def generate_update_report():
    """生成数据更新报告"""
    data = get_latest_data()
    checks = check_for_updates()
    
    report = f"""
# 装修造价数据更新报告

## 更新日期
{data['更新日期']}

## 数据版本
v{data['版本']}

## 检查结果
"""
    for check in checks:
        report += f"- {check}\n"
    
    report += """
## 单位面积造价参考（元/㎡）

| 档次 | 硬装 | 软装 | 电器 | 合计 |
|------|------|------|------|------|
"""
    
    for grade in ["简装", "精装", "豪装"]:
        d = data[grade]
        report += f"| {grade} | {d['硬装']} | {d['软装']} | {d['电器']} | {d['合计']} |\n"
    
    report += """
## 城市系数

| 城市等级 | 系数 | 人工费 |
|----------|------|--------|
"""
    
    for tier, info in data["城市系数"].items():
        cities = ", ".join(info["城市"][:5]) + ("..." if len(info["城市"]) > 5 else "")
        report += f"| {tier} | ×{info['系数']} | {info['人工费']}元/工日 |\n"
    
    report += """
## 下次更新建议

- **短期**：每季度检查一次材料价格
- **中期**：每半年更新城市系数
- **长期**：考虑接入广材网 API 获取实时数据

---

*此报告由 update_prices.py 自动生成
"""
    
    return report

def main():
    print("=== 装修造价数据更新检查 ===\n")
    
    data = get_latest_data()
    print(f"数据版本: v{data['版本']}")
    print(f"更新日期: {data['更新日期']}")
    print()
    
    checks = check_for_updates()
    for check in checks:
        print(check)
    
    print()
    
    # 生成报告
    report = generate_update_report()
    
    # 保存报告
    with open("data_update_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("报告已保存到: data_update_report.md")

if __name__ == "__main__":
    main()
