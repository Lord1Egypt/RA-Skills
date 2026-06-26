# 物流方案优化器

"""
根据货值、目的地、时效要求，推荐最优物流方案
"""

def recommend_logistics(value_usd, destination, urgency="normal"):
    """
    推荐物流方案
    
    参数:
        value_usd: 货值（美元）
        destination: 目的地（europe/america/asia/middle_east/africa）
        urgency: 紧急程度（normal/urgent）
    
    返回:
        推荐方案列表
    """
    
    recommendations = []
    
    # 义新欧班列（适合中高货值、欧洲/中亚）
    if destination in ["europe", "central_asia"] and value_usd >= 5000 and urgency == "normal":
        recommendations.append({
            "method": "义新欧班列",
            "cost_estimate": f"${value_usd * 0.03:.0f}-{value_usd * 0.05:.0f}",
            "transit_time": "15-21天",
            "advantages": "时效稳定、成本适中",
            "score": 90
        })
    
    # 海运拼箱（适合中低货值、不急）
    if value_usd >= 2000 and urgency == "normal":
        volume_cbm = value_usd / 1000  # 假设货值密度
        cost_per_cbm = {
            "europe": 100,
            "america": 80,
            "asia": 40,
            "middle_east": 60,
            "africa": 120
        }
        cost = volume_cbm * cost_per_cbm.get(destination, 80)
        
        recommendations.append({
            "method": "海运拼箱",
            "cost_estimate": f"${cost:.0f}",
            "transit_time": "30-45天",
            "advantages": "成本最低",
            "score": 85 if value_usd >= 5000 else 75
        })
    
    # 空运（适合高值、紧急）
    if urgency == "urgent" or value_usd >= 10000:
        weight_kg = value_usd / 20  # 假设货值密度
        cost_per_kg = {
            "europe": 6,
            "america": 8,
            "asia": 4,
            "middle_east": 5,
            "africa": 7
        }
        cost = weight_kg * cost_per_kg.get(destination, 6)
        
        recommendations.append({
            "method": "空运",
            "cost_estimate": f"${cost:.0f}",
            "transit_time": "3-7天",
            "advantages": "时效最快",
            "score": 95 if urgency == "urgent" else 70
        })
    
    # 专线小包（适合小件）
    if value_usd < 2000:
        recommendations.append({
            "method": "专线小包",
            "cost_estimate": f"${value_usd * 0.08:.0f}-{value_usd * 0.12:.0f}",
            "transit_time": "7-15天",
            "advantages": "适合小件、操作简单",
            "score": 80
        })
    
    # 按评分排序
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations


def calculate_landing_cost(
    purchase_price_cny,
    quantity,
    volume_cbm,
    weight_kg,
    shipping_method,
    destination
):
    """
    计算到岸成本
    
    返回: 单位到岸成本（美元）
    """
    exchange_rate = 7.2  # 人民币兑美元
    
    # 采购成本
    total_purchase = purchase_price_cny * quantity / exchange_rate
    
    # 运费估算
    shipping_costs = {
        "海运拼箱": volume_cbm * 80,
        "义新欧": volume_cbm * 250,
        "空运": weight_kg * 6,
        "专线小包": weight_kg * 8
    }
    shipping_cost = shipping_costs.get(shipping_method, 0)
    
    # 报关费用
    customs_cost = 50  # 约$50/票
    
    # 保险费用（货值0.5%）
    insurance_cost = total_purchase * 0.005
    
    # 总成本
    total_cost = total_purchase + shipping_cost + customs_cost + insurance_cost
    
    # 单位成本
    unit_cost = total_cost / quantity
    
    return {
        "total_purchase_usd": round(total_purchase, 2),
        "shipping_cost_usd": round(shipping_cost, 2),
        "customs_cost_usd": customs_cost,
        "insurance_cost_usd": round(insurance_cost, 2),
        "total_cost_usd": round(total_cost, 2),
        "unit_cost_usd": round(unit_cost, 2),
        "shipping_cost_ratio": f"{shipping_cost/total_purchase*100:.1f}%"
    }


def optimize_mix_container(products, target_value_usd=15000):
    """
    优化混拼柜组合
    
    参数:
        products: 产品列表 [{"name": "", "value": 0, "volume": 0}, ...]
        target_value_usd: 目标货值
    
    返回: 推荐组合
    """
    # 按货值密度（货值/体积）排序
    for p in products:
        p["density"] = p["value"] / p["volume"] if p["volume"] > 0 else 0
    
    products.sort(key=lambda x: x["density"], reverse=True)
    
    # 贪心算法填充
    selected = []
    total_value = 0
    total_volume = 0
    
    for p in products:
        if total_value + p["value"] <= target_value_usd * 1.2:  # 允许20%超
            selected.append(p)
            total_value += p["value"]
            total_volume += p["volume"]
    
    return {
        "selected_products": selected,
        "total_value_usd": total_value,
        "total_volume_cbm": total_volume,
        "estimated_shipping": f"${total_volume * 80:.0f}（海运拼箱）",
        "shipping_ratio": f"{total_volume * 80 / total_value * 100:.1f}%"
    }


if __name__ == "__main__":
    # 测试
    print("=== 物流方案推荐 ===")
    recs = recommend_logistics(8000, "europe", "normal")
    for r in recs:
        print(f"{r['method']}: {r['cost_estimate']}, {r['transit_time']}")
    
    print("\n=== 到岸成本计算 ===")
    cost = calculate_landing_cost(
        purchase_price_cny=25,
        quantity=1000,
        volume_cbm=0.5,
        weight_kg=30,
        shipping_method="海运拼箱",
        destination="europe"
    )
    print(f"单位成本: ${cost['unit_cost_usd']}")
    print(f"运费占比: {cost['shipping_cost_ratio']}")
