"""
销量和热度推断模块（无需官方 API）

基于搜索结果数据推断车辆的市场热度、销售速度和受欢迎程度
"""

from __future__ import annotations
from typing import Any
from datetime import datetime


def calculate_market_popularity(
    make: str,
    model: str,
    total_listings: int,
    price_range: tuple[int, int],
    avg_price: int,
    budget: int,
) -> dict[str, Any]:
    """
    基于搜索结果推断市场热度
    
    Args:
        make: 品牌
        model: 车型
        total_listings: 搜索结果总数
        price_range: (最低价, 最高价)
        avg_price: 平均价格
        budget: 用户预算
        
    Returns:
        热度评估字典
    """
    
    # 1. 供应量评分（0-100）
    if total_listings >= 50:
        supply_score = 100
        supply_level = "abundant"
        supply_desc = "供应充足"
    elif total_listings >= 30:
        supply_score = 80
        supply_level = "high"
        supply_desc = "供应较多"
    elif total_listings >= 15:
        supply_score = 60
        supply_level = "moderate"
        supply_desc = "供应适中"
    elif total_listings >= 5:
        supply_score = 40
        supply_level = "limited"
        supply_desc = "供应有限"
    else:
        supply_score = 20
        supply_level = "scarce"
        supply_desc = "供应稀缺"
    
    # 2. 价格竞争力评分
    min_price, max_price = price_range
    price_spread = max_price - min_price
    
    if price_spread > 0:
        # 用户预算在价格范围中的位置
        if avg_price <= budget:
            price_competitiveness = min(100, ((budget - avg_price) / budget) * 100 + 50)
        else:
            price_competitiveness = max(0, 50 - ((avg_price - budget) / budget) * 50)
    else:
        price_competitiveness = 50
    
    # 3. 市场热度推断（综合评分）
    # 供应量多 = 需求旺盛 = 热门车型
    # 但也可能是价格合理导致供应多
    popularity_score = supply_score * 0.7 + price_competitiveness * 0.3
    
    # 4. 推断销售速度
    if popularity_score >= 80:
        sales_speed = "fast"
        estimated_days = "10-20 天"
        speed_desc = "热销车型，预计很快售出"
    elif popularity_score >= 60:
        sales_speed = "moderate"
        estimated_days = "20-40 天"
        speed_desc = "正常销售速度"
    elif popularity_score >= 40:
        sales_speed = "slow"
        estimated_days = "40-60 天"
        speed_desc = "销售较慢，可能议价空间大"
    else:
        sales_speed = "very_slow"
        estimated_days = "60+ 天"
        speed_desc = "冷门车型或定价偏高"
    
    # 5. 推荐建议
    recommendations = []
    
    if supply_level in ["abundant", "high"]:
        recommendations.append("✅ 市场选择多，可以慢慢挑选比较")
    
    if price_competitiveness > 70:
        recommendations.append("✅ 价格具有竞争力，性价比好")
    elif price_competitiveness < 30:
        recommendations.append("⚠️ 平均价格偏高，建议谨慎或等待降价")
    
    if sales_speed == "fast":
        recommendations.append("🔥 热门车型，看中的车建议尽快联系")
    elif sales_speed == "very_slow":
        recommendations.append("💡 销售较慢，可以尝试议价")
    
    if total_listings < 5:
        recommendations.append("⚠️ 供应稀缺，可能难找到合适的车")
    
    return {
        "make": make,
        "model": model,
        "popularity_score": round(popularity_score, 1),
        "supply_score": supply_score,
        "supply_level": supply_level,
        "supply_description": supply_desc,
        "total_listings": total_listings,
        "price_competitiveness": round(price_competitiveness, 1),
        "avg_price": avg_price,
        "price_range": price_range,
        "sales_speed": sales_speed,
        "estimated_days_to_sell": estimated_days,
        "speed_description": speed_desc,
        "recommendations": recommendations,
        "calculated_at": datetime.now().isoformat(),
    }


def analyze_price_distribution(items: list[dict]) -> dict[str, Any]:
    """
    分析价格分布，识别性价比最高的车辆
    """
    if not items:
        return {}
    
    prices = [item.get('price') for item in items if item.get('price')]
    
    if not prices:
        return {}
    
    prices_sorted = sorted(prices)
    count = len(prices)
    
    min_price = prices_sorted[0]
    max_price = prices_sorted[-1]
    avg_price = sum(prices) / count
    median_price = prices_sorted[count // 2]
    
    # 计算四分位数
    q1_price = prices_sorted[count // 4]
    q3_price = prices_sorted[3 * count // 4]
    
    # 识别"好交易"（价格低于 Q1）
    good_deals = [item for item in items if item.get('price') and item['price'] < q1_price]
    
    # 识别"高价"（价格高于 Q3）
    high_priced = [item for item in items if item.get('price') and item['price'] > q3_price]
    
    return {
        "min_price": min_price,
        "max_price": max_price,
        "avg_price": int(avg_price),
        "median_price": median_price,
        "q1_price": q1_price,
        "q3_price": q3_price,
        "price_spread": max_price - min_price,
        "good_deals_count": len(good_deals),
        "good_deals_threshold": q1_price,
        "high_priced_count": len(high_priced),
        "price_distribution": {
            "under_q1": len([p for p in prices if p < q1_price]),
            "q1_to_median": len([p for p in prices if q1_price <= p < median_price]),
            "median_to_q3": len([p for p in prices if median_price <= p < q3_price]),
            "above_q3": len([p for p in prices if p >= q3_price]),
        }
    }


def detect_listing_age(item: dict) -> dict[str, Any]:
    """
    从列表中检测车辆上架时间（如果可用）
    """
    age_info = {}
    
    # 尝试提取上架时间
    age_text = item.get('age') or item.get('listed_date') or item.get('days_on_market')
    
    if age_text:
        age_lower = str(age_text).lower()
        
        # 解析不同格式
        if 'hour' in age_lower or '小时' in age_lower:
            age_info['listing_age'] = 'new'
            age_info['days_listed'] = 0
            age_info['freshness'] = 'very_fresh'
        elif 'day' in age_lower or '天' in age_lower:
            # 提取天数
            import re
            days_match = re.search(r'(\d+)', age_text)
            if days_match:
                days = int(days_match.group(1))
                age_info['days_listed'] = days
                
                if days <= 3:
                    age_info['listing_age'] = 'very_new'
                    age_info['freshness'] = 'fresh'
                elif days <= 7:
                    age_info['listing_age'] = 'new'
                    age_info['freshness'] = 'recent'
                elif days <= 14:
                    age_info['listing_age'] = 'moderate'
                    age_info['freshness'] = 'moderate'
                elif days <= 30:
                    age_info['listing_age'] = 'old'
                    age_info['freshness'] = 'old'
                else:
                    age_info['listing_age'] = 'very_old'
                    age_info['freshness'] = 'stale'
        elif 'week' in age_lower or '周' in age_lower:
            age_info['listing_age'] = 'moderate'
            age_info['freshness'] = 'moderate'
            age_info['days_listed'] = 10  # 估计
        elif 'month' in age_lower or '月' in age_lower:
            age_info['listing_age'] = 'old'
            age_info['freshness'] = 'old'
            age_info['days_listed'] = 35  # 估计
    
    # 根据新鲜度给出建议
    if age_info.get('freshness') == 'very_fresh':
        age_info['recommendation'] = "🆕 刚上架，是新机会"
    elif age_info.get('freshness') == 'fresh':
        age_info['recommendation'] = "✨ 最近上架，可以关注"
    elif age_info.get('freshness') == 'stale':
        age_info['recommendation'] = "⏰ 上架很久未售出，可能有议价空间"
    
    return age_info


def calculate_sales_momentum(multi_search_results: list[dict]) -> dict[str, Any]:
    """
    通过多次搜索对比，检测销售动量
    
    Args:
        multi_search_results: 不同时间的搜索结果列表
    """
    if len(multi_search_results) < 2:
        return {"error": "需要至少 2 次搜索结果"}
    
    # 对比第一次和最后一次
    first_search = multi_search_results[0]
    last_search = multi_search_results[-1]
    
    first_count = first_search.get('total', 0)
    last_count = last_search.get('total', 0)
    
    change = last_count - first_count
    change_percent = (change / first_count * 100) if first_count > 0 else 0
    
    if change < -5:
        momentum = "declining"
        momentum_desc = "供应量下降，市场需求旺盛"
    elif change > 5:
        momentum = "increasing"
        momentum_desc = "供应量上升，新车源增加或需求减少"
    else:
        momentum = "stable"
        momentum_desc = "供应量稳定"
    
    return {
        "first_count": first_count,
        "last_count": last_count,
        "change": change,
        "change_percent": round(change_percent, 1),
        "momentum": momentum,
        "momentum_description": momentum_desc,
        "search_count": len(multi_search_results),
    }


def rank_by_inferred_popularity(items: list[dict], budget: int) -> list[dict]:
    """
    基于推断的热度对车辆排序
    """
    ranked_items = []
    
    for item in items:
        price = item.get('price', 0)
        listing_age_days = detect_listing_age(item).get('days_listed', 30)
        
        # 计算推断评分
        score = 0
        
        # 1. 价格合理性（40%）
        if price > 0 and price <= budget:
            price_score = ((budget - price) / budget) * 40
            score += price_score
        
        # 2. 新鲜度（30%）- 新上架的可能是热门
        if listing_age_days <= 3:
            freshness_score = 30
        elif listing_age_days <= 7:
            freshness_score = 25
        elif listing_age_days <= 14:
            freshness_score = 20
        elif listing_age_days <= 30:
            freshness_score = 10
        else:
            freshness_score = 5
        
        score += freshness_score
        
        # 3. Trade 卖家加分（20%）- 经销商车更规范
        if item.get('is_trade') or item.get('seller_type_display') == 'Trade':
            score += 20
        else:
            score += 10  # 私人卖家也有优势（可能更便宜）
        
        # 4. 有图片加分（10%）
        if item.get('image_url') or item.get('number_of_images'):
            score += 10
        
        item['inferred_popularity_score'] = round(score, 2)
        ranked_items.append(item)
    
    # 排序
    ranked_items.sort(key=lambda x: x['inferred_popularity_score'], reverse=True)
    
    return ranked_items


# 主函数：综合分析
def analyze_market_without_api(
    make: str,
    model: str,
    search_results: dict,
    budget: int,
) -> dict[str, Any]:
    """
    综合分析市场数据（无需官方 API）
    
    Returns:
        完整的市场分析报告
    """
    items = search_results.get('items', [])
    total = search_results.get('total', len(items))
    
    # 1. 价格分布分析
    price_analysis = analyze_price_distribution(items)
    
    # 2. 市场热度推断
    popularity = calculate_market_popularity(
        make=make,
        model=model,
        total_listings=total,
        price_range=(price_analysis.get('min_price', 0), price_analysis.get('max_price', 0)),
        avg_price=price_analysis.get('avg_price', 0),
        budget=budget,
    )
    
    # 3. 按推断热度排序
    ranked_items = rank_by_inferred_popularity(items, budget)
    
    # 4. 识别最佳交易
    top_deals = ranked_items[:5] if len(ranked_items) >= 5 else ranked_items
    
    return {
        "market_overview": {
            "make": make,
            "model": model,
            "total_listings": total,
            "analyzed_listings": len(items),
        },
        "popularity_analysis": popularity,
        "price_analysis": price_analysis,
        "top_recommendations": top_deals,
        "analysis_method": "inferred_from_search_data",
        "confidence_level": "medium",  # 中等置信度（基于推断）
        "note": "分析基于搜索结果推断，不使用官方 API",
    }
