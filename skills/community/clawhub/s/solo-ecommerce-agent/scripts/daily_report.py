#!/usr/bin/env python3
"""
每日运营日报脚本
汇总选品、商品、客服、订单数据，生成日报
"""

import json
from datetime import datetime
from pathlib import Path

# 数据目录
DATA_DIR = Path.home() / "solo-ecommerce-data"
DATA_DIR.mkdir(exist_ok=True)

def generate_daily_report():
    """
    生成每日运营日报
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 读取各模块数据
    products = load_json(DATA_DIR / "products.json", [])
    orders = load_json(DATA_DIR / "orders.json", [])
    recommendations = load_json(DATA_DIR / "recommendations.json", [])
    customers = load_json(DATA_DIR / "customers.json", {})
    
    # 计算指标
    total_products = len(products)
    published_products = len([p for p in products if p.get("status") == "published"])
    
    total_orders = len(orders)
    total_amount = sum(o.get("amount", 0) for o in orders)
    pending_shipment = len([o for o in orders if o.get("status") == "待发货"])
    after_sale = len([o for o in orders if o.get("status") == "售后"])
    
    total_customers = len(customers)
    total_messages = sum(
        len(c.get("messages", [])) for c in customers.values()
    )
    
    top_recommendations = sorted(
        recommendations, 
        key=lambda x: x.get("opportunity_score", 0), 
        reverse=True
    )[:5]
    
    # 生成日报
    report = f"""
# 电商运营日报 - {today}

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 在售商品 | {published_products}/{total_products} |
| 订单数 | {total_orders} |
| 销售额 | ¥{total_amount:.2f} |
| 客单价 | ¥{(total_amount/total_orders if total_orders else 0):.2f} |
| 待发货 | {pending_shipment} |
| 售后中 | {after_sale} |
| 客户数 | {total_customers} |
| 消息数 | {total_messages} |

## 🔍 选品推荐 TOP5

"""
    
    for i, rec in enumerate(top_recommendations, 1):
        score = rec.get("opportunity_score", 0)
        keyword = rec.get("keyword", "未知")
        price = rec.get("suggested_price", "未知")
        report += f"{i}. **{keyword}** - 机会指数：{score}，建议定价：{price}\n"
    
    report += f"""
## 📦 待处理事项

- 待发货订单：{pending_shipment}笔
- 售后申请：{after_sale}笔
- 客服消息：{total_messages}条

## ⚠️ 异常提醒

"""
    
    # 检查异常
    if pending_shipment > 10:
        report += f"- ⚠️ 待发货积压：{pending_shipment}笔，需及时处理\n"
    if after_sale > 3:
        report += f"- ⚠️ 售后积压：{after_sale}笔，需及时处理\n"
    
    if pending_shipment <= 10 and after_sale <= 3:
        report += "- ✅ 运营状态正常\n"
    
    # 保存日报
    report_file = DATA_DIR / "logs" / f"{today}.log"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"\n日报已保存：{report_file}")
    
    return report

def load_json(filepath, default=None):
    """加载JSON文件"""
    if not filepath.exists():
        return default if default is not None else []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default if default is not None else []

def main():
    """主入口"""
    print("=" * 50)
    print("电商运营日报")
    print("=" * 50)
    
    generate_daily_report()

if __name__ == "__main__":
    main()
