#!/usr/bin/env python3
"""
成交商品特征分析 Skill
分析成交商品的品类、价格带、颜色、包型、上市时间等特征分布及环比变化

数据源：/api/v1/store/dashboard/bi
- categoryFeature / previousCategoryFeature: 品类分布
- brandFeature / previousBrandFeature: 品牌分布
- shapeFeature / previousShapeFeature: 包型分布
- priceRangeFeature / previousPriceRangeFeature: 价格带分布
- xrColorFeature / previousXrColorFeature: 颜色分布
- launchDateFeature / previousLaunchDateFeature: 上市时间分布
- orderFeature: 订单特征（折扣、连带）
"""

import sys
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data


def analyze(store_id: str, from_date: str, to_date: str, store_name: str = ""):
    """成交商品特征分析 - 包含环比变化"""
    
    print("=" * 70)
    print(f"成交商品特征分析报告 - {store_name or store_id}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print("=" * 70)
    print()
    
    # ========== 第一步：获取数据 ==========
    print("【第一步：获取数据】")
    print("API: /api/v1/store/dashboard/bi")
    print(f"参数: storeId={store_id}, fromDate={from_date}, toDate={to_date}")
    print()
    
    data = get_copilot_data(f'/api/v1/store/dashboard/bi?storeId={store_id}&fromDate={from_date}&toDate={to_date}')
    
    # ========== 第二步：品类特征分析（含环比）==========
    print("【第二步：品类特征分析】")
    print()
    
    category_current = {item['name']: item for item in data.get('categoryFeature', [])}
    category_previous = {item['name']: item for item in data.get('previousCategoryFeature', [])}
    
    if category_current:
        print("成交商品品类分布及环比变化:")
        print(f"{'品类':<12} {'本期销售额':>10} {'占比':>6} {'销售额环比':>10} {'趋势':>4}")
        print("-" * 52)
        
        # 按本期销售额排序
        sorted_categories = sorted(category_current.items(), key=lambda x: x[1].get('dealMoney', 0), reverse=True)
        
        for name, current in sorted_categories[:5]:
            money = current.get('dealMoney', 0)
            share = current.get('moneyPercentage', '0')
            
            # 计算环比
            previous = category_previous.get(name, {})
            prev_money = previous.get('dealMoney', 0)
            if prev_money > 0:
                change = (money - prev_money) / prev_money * 100
                trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                change_str = f"{change:+.1f}%"
            else:
                change_str = "新增"
                trend = "+"
            
            print(f"{name:<12} ¥{money:>8,.0f} {share:>5} {change_str:>10} {trend:>4}")
        print()
        print("  说明: 占比=该品类销售额/总销售额; 销售额环比=本期vs上期销售额变化")
        print()
    
    # ========== 第三步：价格带特征分析（含环比）==========
    print("【第三步：价格带特征分析】")
    print()
    
    price_current = {item['name']: item for item in data.get('priceRangeFeature', [])}
    price_previous = {item['name']: item for item in data.get('previousPriceRangeFeature', [])}
    
    if price_current:
        print("成交商品价格带分布及环比变化:")
        print(f"{'价格带':<12} {'本期销售额':>10} {'占比':>6} {'销售额环比':>10} {'趋势':>4}")
        print("-" * 52)
        
        sorted_prices = sorted(price_current.items(), key=lambda x: x[1].get('dealMoney', 0), reverse=True)
        
        for name, current in sorted_prices[:5]:
            money = current.get('dealMoney', 0)
            share = current.get('moneyPercentage', '0')
            
            previous = price_previous.get(name, {})
            prev_money = previous.get('dealMoney', 0)
            if prev_money > 0:
                change = (money - prev_money) / prev_money * 100
                trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                change_str = f"{change:+.1f}%"
            else:
                change_str = "新增"
                trend = "+"
            
            print(f"{name:<12} ¥{money:>8,.0f} {share:>5} {change_str:>10} {trend:>4}")
        print()
    
    # ========== 第四步：包型特征分析（含环比）==========
    print("【第四步：包型特征分析】")
    print()
    
    shape_current = {item['name']: item for item in data.get('shapeFeature', [])}
    shape_previous = {item['name']: item for item in data.get('previousShapeFeature', [])}
    
    if shape_current:
        print("成交商品包型分布及环比变化:")
        print(f"{'包型':<12} {'本期销售额':>10} {'占比':>6} {'销售额环比':>10} {'趋势':>4}")
        print("-" * 52)
        
        sorted_shapes = sorted(shape_current.items(), key=lambda x: x[1].get('dealMoney', 0), reverse=True)
        
        for name, current in sorted_shapes[:5]:
            money = current.get('dealMoney', 0)
            share = current.get('moneyPercentage', '0')
            
            previous = shape_previous.get(name, {})
            prev_money = previous.get('dealMoney', 0)
            if prev_money > 0:
                change = (money - prev_money) / prev_money * 100
                trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                change_str = f"{change:+.1f}%"
            else:
                change_str = "新增"
                trend = "+"
            
            print(f"{name:<12} ¥{money:>8,.0f} {share:>5} {change_str:>10} {trend:>4}")
        print()
    
    # ========== 第五步：颜色特征分析（含环比）==========
    print("【第五步：颜色特征分析】")
    print()
    
    color_current = {item['name']: item for item in data.get('xrColorFeature', [])}
    color_previous = {item['name']: item for item in data.get('previousXrColorFeature', [])}
    
    if color_current:
        print("成交商品颜色分布及环比变化:")
        print(f"{'颜色':<12} {'本期销售额':>10} {'占比':>6} {'销售额环比':>10} {'趋势':>4}")
        print("-" * 52)
        
        sorted_colors = sorted(color_current.items(), key=lambda x: x[1].get('dealMoney', 0), reverse=True)
        
        for name, current in sorted_colors[:5]:
            money = current.get('dealMoney', 0)
            share = current.get('moneyPercentage', '0')
            
            previous = color_previous.get(name, {})
            prev_money = previous.get('dealMoney', 0)
            if prev_money > 0:
                change = (money - prev_money) / prev_money * 100
                trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                change_str = f"{change:+.1f}%"
            else:
                change_str = "新增"
                trend = "+"
            
            print(f"{name:<12} ¥{money:>8,.0f} {share:>5} {change_str:>10} {trend:>4}")
        print()
    
    # ========== 第六步：上市时间特征分析 ==========
    print("【第六步：上市时间特征分析】")
    print()
    
    launch_current = {item['name']: item for item in data.get('launchDateFeature', [])}
    launch_previous = {item['name']: item for item in data.get('previousLaunchDateFeature', [])}
    
    if launch_current:
        print("成交商品上市时间分布及环比变化:")
        print(f"{'上市时间':<12} {'本期销售额':>10} {'占比':>6} {'销售额环比':>10} {'趋势':>4}")
        print("-" * 52)
        
        # 按时间倒序
        sorted_launch = sorted(launch_current.items(), key=lambda x: x[0], reverse=True)
        
        for name, current in sorted_launch[:5]:
            money = current.get('dealMoney', 0)
            share = current.get('moneyPercentage', '0')
            
            previous = launch_previous.get(name, {})
            prev_money = previous.get('dealMoney', 0)
            if prev_money > 0:
                change = (money - prev_money) / prev_money * 100
                trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                change_str = f"{change:+.1f}%"
            else:
                change_str = "新增"
                trend = "+"
            
            print(f"{name:<12} ¥{money:>8,.0f} {share:>5} {change_str:>10} {trend:>4}")
        print()
    
    # ========== 第七步：生成分析结论 ==========
    print("【第七步：生成分析结论】")
    print()
    
    findings = []
    
    # 分析1: 品类变化趋势
    if category_current and category_previous:
        top_current = max(category_current.items(), key=lambda x: x[1].get('dealMoney', 0))
        top_previous = max(category_previous.items(), key=lambda x: x[1].get('dealMoney', 0))
        
        if top_current[0] == top_previous[0]:
            change = (top_current[1].get('dealMoney', 0) - top_previous[1].get('dealMoney', 0)) / top_previous[1].get('dealMoney', 1) * 100
            if abs(change) > 20:
                trend = "增长" if change > 0 else "下滑"
                findings.append(f"{'✅' if change > 0 else '⚠️'} 主力品类{top_current[0]}{trend}明显（{change:+.1f}%）")
    
    # 分析2: 价格带迁移
    if price_current and price_previous:
        high_price_current = sum(p.get('moneyShare', 0) for p in price_current.values() if any(x in p.get('name', '') for x in ['1000', '1200', '1500']))
        high_price_previous = sum(p.get('moneyShare', 0) for p in price_previous.values() if any(x in p.get('name', '') for x in ['1000', '1200', '1500']))
        
        if high_price_current > high_price_previous + 0.1:
            findings.append(f"✅ 价格带上移：1000元以上占比提升{(high_price_current - high_price_previous)*100:.1f}个百分点")
        elif high_price_current < high_price_previous - 0.1:
            findings.append(f"⚠️  价格带下移：1000元以上占比下降{(high_price_previous - high_price_current)*100:.1f}个百分点")
    
    # 分析3: 新款表现
    if launch_current and launch_previous:
        recent_current = sum(l.get('moneyShare', 0) for l in launch_current.values() if '2026' in l.get('name', ''))
        recent_previous = sum(l.get('moneyShare', 0) for l in launch_previous.values() if '2026' in l.get('name', ''))
        
        if recent_current < recent_previous - 0.05:
            findings.append(f"⚠️  新款表现疲软：2026年新款销售占比下降{(recent_previous - recent_current)*100:.1f}个百分点")
    
    # 分析4: 包型趋势
    if shape_current and shape_previous:
        for shape_name in ['方包', '托特包', '桶包']:
            if shape_name in shape_current and shape_name in shape_previous:
                current_share = shape_current[shape_name].get('moneyShare', 0)
                previous_share = shape_previous[shape_name].get('moneyShare', 0)
                change = (current_share - previous_share) * 100
                if abs(change) > 5:
                    trend = "上升" if change > 0 else "下降"
                    findings.append(f"{'✅' if change > 0 else '💡'} {shape_name}趋势{trend}（{change:+.1f}pp）")
    
    if findings:
        print("关键发现:")
        for finding in findings:
            print(f"  {finding}")
    else:
        print("  成交商品特征稳定")
    print()
    
    print("=" * 70)
    print("分析完成")
    print("=" * 70)


if __name__ == "__main__":
    analyze(
        store_id="416759_1714379448487",
        from_date="2026-03-01",
        to_date="2026-03-26",
        store_name="正义路60号店"
    )
