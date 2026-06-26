# 成本利润计算器

"""
外贸订单成本利润计算工具
"""

def calculate_order_profit(
    purchase_price_cny,
    quantity,
    selling_price_usd,
    volume_cbm=0,
    weight_kg=0,
    shipping_method="海运拼箱",
    exchange_rate=7.2
):
    """
    计算订单利润
    
    参数:
        purchase_price_cny: 采购单价（人民币）
        quantity: 数量
        selling_price_usd: 售价单价（美元）
        volume_cbm: 总体积（立方米）
        weight_kg: 总重量（千克）
        shipping_method: 物流方式
        exchange_rate: 汇率
    
    返回: 利润分析
    """
    
    # 采购成本
    purchase_total_cny = purchase_price_cny * quantity
    purchase_total_usd = purchase_total_cny / exchange_rate
    
    # 运费估算
    shipping_rates = {
        "海运拼箱": {"per_cbm": 80, "per_kg": 0},
        "义新欧": {"per_cbm": 250, "per_kg": 0},
        "空运": {"per_cbm": 0, "per_kg": 6},
        "专线小包": {"per_cbm": 0, "per_kg": 8}
    }
    rate = shipping_rates.get(shipping_method, {"per_cbm": 80, "per_kg": 0})
    shipping_cost = volume_cbm * rate["per_cbm"] + weight_kg * rate["per_kg"]
    
    # 其他费用
    customs_fee = 50  # 报关费
    insurance_fee = purchase_total_usd * 0.005  # 保险费
    other_fee = purchase_total_usd * 0.02  # 其他费用（包装、国内运费等）
    
    # 总成本
    total_cost = purchase_total_usd + shipping_cost + customs_fee + insurance_fee + other_fee
    
    # 销售收入
    sales_revenue = selling_price_usd * quantity
    
    # 利润
    profit = sales_revenue - total_cost
    profit_margin = profit / sales_revenue * 100 if sales_revenue > 0 else 0
    
    return {
        "采购成本": f"${purchase_total_usd:.2f}",
        "运费": f"${shipping_cost:.2f}",
        "报关费": f"${customs_fee:.2f}",
        "保险费": f"${insurance_fee:.2f}",
        "其他费用": f"${other_fee:.2f}",
        "总成本": f"${total_cost:.2f}",
        "销售收入": f"${sales_revenue:.2f}",
        "毛利润": f"${profit:.2f}",
        "毛利率": f"{profit_margin:.1f}%",
        "单位成本": f"${total_cost/quantity:.2f}",
        "单位利润": f"${profit/quantity:.2f}"
    }


def calculate_min_selling_price(
    purchase_price_cny,
    quantity,
    volume_cbm=0,
    weight_kg=0,
    shipping_method="海运拼箱",
    target_margin=30,
    exchange_rate=7.2
):
    """
    计算最低售价（达到目标毛利率）
    
    参数:
        target_margin: 目标毛利率（%）
    
    返回: 最低售价
    """
    
    # 采购成本
    purchase_total_cny = purchase_price_cny * quantity
    purchase_total_usd = purchase_total_cny / exchange_rate
    
    # 运费
    shipping_rates = {
        "海运拼箱": {"per_cbm": 80, "per_kg": 0},
        "义新欧": {"per_cbm": 250, "per_kg": 0},
        "空运": {"per_cbm": 0, "per_kg": 6},
        "专线小包": {"per_cbm": 0, "per_kg": 8}
    }
    rate = shipping_rates.get(shipping_method, {"per_cbm": 80, "per_kg": 0})
    shipping_cost = volume_cbm * rate["per_cbm"] + weight_kg * rate["per_kg"]
    
    # 其他费用
    other_costs = purchase_total_usd * 0.025 + 50  # 保险+报关+其他
    
    # 固定成本
    fixed_costs = purchase_total_usd + shipping_cost + other_costs
    
    # 目标毛利率下的售价
    # 售价 = 成本 / (1 - 毛利率)
    min_revenue = fixed_costs / (1 - target_margin / 100)
    min_price = min_revenue / quantity
    
    return {
        "最低总价": f"${min_revenue:.2f}",
        "最低单价": f"${min_price:.2f}",
        "目标毛利率": f"{target_margin}%",
        "固定成本": f"${fixed_costs:.2f}"
    }


def compare_products(products_data):
    """
    对比多个产品的盈利能力
    
    参数:
        products_data: 产品列表 [
            {
                "name": "产品名",
                "purchase_cny": 采购价,
                "sell_usd": 售价,
                "volume": 体积,
                "weight": 重量
            },
            ...
        ]
    
    返回: 对比表格
    """
    
    results = []
    for p in products_data:
        profit = calculate_order_profit(
            purchase_price_cny=p["purchase_cny"],
            quantity=1,
            selling_price_usd=p["sell_usd"],
            volume_cbm=p.get("volume", 0),
            weight_kg=p.get("weight", 0)
        )
        
        # 解析利润率
        margin_str = profit["毛利率"]
        margin = float(margin_str.replace("%", ""))
        
        results.append({
            "产品": p["name"],
            "采购价": f"¥{p['purchase_cny']}",
            "售价": f"${p['sell_usd']}",
            "毛利率": profit["毛利率"],
            "单位利润": profit["单位利润"],
            "评分": margin  # 按毛利率排序
        })
    
    # 按毛利率排序
    results.sort(key=lambda x: x["评分"], reverse=True)
    
    return results


def pricing_strategy_analysis(
    purchase_price_cny,
    quantity,
    volume_cbm=0,
    weight_kg=0,
    shipping_method="海运拼箱"
):
    """
    定价策略分析
    
    返回: 不同毛利率下的定价建议
    """
    
    strategies = []
    for margin in [15, 20, 25, 30, 35, 40, 50]:
        result = calculate_min_selling_price(
            purchase_price_cny=purchase_price_cny,
            quantity=quantity,
            volume_cbm=volume_cbm,
            weight_kg=weight_kg,
            shipping_method=shipping_method,
            target_margin=margin
        )
        strategies.append({
            "目标毛利率": f"{margin}%",
            "建议单价": result["最低单价"],
            "建议总价": result["最低总价"]
        })
    
    return strategies


if __name__ == "__main__":
    # 测试
    print("=== 订单利润计算 ===")
    result = calculate_order_profit(
        purchase_price_cny=25,
        quantity=1000,
        selling_price_usd=5,
        volume_cbm=0.5,
        weight_kg=30,
        shipping_method="海运拼箱"
    )
    for k, v in result.items():
        print(f"{k}: {v}")
    
    print("\n=== 定价策略分析 ===")
    strategies = pricing_strategy_analysis(
        purchase_price_cny=25,
        quantity=1000,
        volume_cbm=0.5,
        weight_kg=30
    )
    for s in strategies:
        print(f"{s['目标毛利率']}: 单价{s['建议单价']}")
