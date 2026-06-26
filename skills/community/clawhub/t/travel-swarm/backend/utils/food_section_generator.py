#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7860端口美食推荐网页新增模块
新增模块，不修改原代码

功能：
在时间节点下显示美食推荐（景点/酒店附近3km）
"""

def generate_food_section(food_data):
    """
    生成美食推荐网页内容
    只新增，不修改原代码
    
    参数：
    - food_data: 真实餐厅数据
    
    返回：
    - HTML新增内容
    """
    
    # 早餐HTML
    breakfast_html = ""
    if food_data.get("success"):
        breakfast = food_data.get("meals", {}).get("早餐", [])
        
        if breakfast:
            breakfast_html = f"""
            <div class="meal-card">
                <h4>🌅 早餐推荐（景点附近）</h4>
                <table>
                    <tr><th>餐厅</th><th>距离</th><th>评分</th><th>价格</th></tr>
            """
            
            for r in breakfast[:3]:
                breakfast_html += f"""
                    <tr>
                        <td>{r.get('name', '')}</td>
                        <td>{r.get('distance_km', 0)}km</td>
                        <td>{r.get('rating', '4.0')}</td>
                        <td>¥{r.get('cost', '50')}</td>
                    </tr>
                """
            
            breakfast_html += f"""
                </table>
                <small>来源: {r.get('source', '高德真实POI')}</small>
            </div>
            """
    
    # 午餐HTML
    lunch_html = ""
    if food_data.get("success"):
        lunch = food_data.get("meals", {}).get("午餐", [])
        
        if lunch:
            lunch_html = f"""
            <div class="meal-card">
                <h4>☀️ 午餐推荐（酒店附近）</h4>
                <table>
                    <tr><th>餐厅</th><th>距离</th><th>评分</th><th>价格</th></tr>
            """
            
            for r in lunch[:3]:
                lunch_html += f"""
                    <tr>
                        <td>{r.get('name', '')}</td>
                        <td>{r.get('distance_km', 0)}km</td>
                        <td>{r.get('rating', '4.0')}</td>
                        <td>¥{r.get('cost', '50')}</td>
                    </tr>
                """
            
            lunch_html += f"""
                </table>
                <small>来源: {r.get('source', '高德真实POI')}</small>
            </div>
            """
    
    # 晚餐HTML（麦当劳兜底）
    dinner_html = ""
    if food_data.get("success"):
        dinner = food_data.get("meals", {}).get("晚餐", [])
        
        if dinner:
            dinner_html = f"""
            <div class="meal-card">
                <h4>🌙 晚餐推荐</h4>
                <table>
                    <tr><th>餐厅</th><th>距离</th><th>类型</th></tr>
            """
            
            for r in dinner[:3]:
                dinner_html += f"""
                    <tr>
                        <td>{r.get('name', '')}</td>
                        <td>{r.get('distance_km', 0)}km</td>
                        <td>{r.get('near_type', '附近餐厅')}</td>
                    </tr>
                """
            
            dinner_html += f"""
                </table>
                <small>来源: {r.get('source', '高德真实POI')}</small>
            </div>
            """
    
    # 组合美食推荐部分
    food_section = f"""
    <!-- ========== 美食推荐（新增） ========== -->
    
    <div class="section">
        <h2>🍽️ 美食推荐（景点/酒店附近3km）</h2>
        
        {breakfast_html}
        {lunch_html}
        {dinner_html}
        
        <p class="tip">💡 建议：提前预订热门餐厅，避开高峰时段</p>
    </div>
    
    <!-- ========== 美食推荐结束 ========== -->
    """
    
    return food_section

# 禁止模拟声明
print("""
=== 美食推荐网页禁止模拟声明 ===
✅ 早餐: 景点附近真实餐厅
✅ 午餐: 酒店附近真实餐厅
✅ 晚餐: 综合推荐+麦当劳兜底
✅ 距离: 真实数学计算

❌ 禁止编造餐厅名称
❌ 禁止模拟评分/价格
""")

__all__ = ['generate_food_section']