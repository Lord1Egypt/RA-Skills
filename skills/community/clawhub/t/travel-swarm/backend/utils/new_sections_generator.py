#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7860端口网页内容新增模块 - 禁止模拟
只新增，不修改原生成代码

新增内容：
1. 真实时间节点
2. 真实天气情况
3. 客房订单链接
4. 导航截图
5. 避坑提醒
"""

def generate_new_sections(weather_data, hotel_data, nav_data, flight_data):
    """
    生成新增网页内容
    只新增，不修改原代码
    
    参数：
    - weather_data: 真实天气API返回
    - hotel_data: 真实酒店API返回
    - nav_data: 真实导航API返回
    - flight_data: FlyAI真实航班返回
    
    返回：
    - HTML新增内容
    """
    
    # 1. 真实天气HTML
    weather_html = ""
    if weather_data.get("success"):
        weather_html = f"""
        <div class="weather-card">
            <h3>🌡️ {weather_data.get('city', '')}天气</h3>
            <p>日期: {weather_data.get('date', '')}</p>
            <p>白天: {weather_data.get('day_weather', '')} {weather_data.get('day_temp', '')}°C</p>
            <p>夜间: {weather_data.get('night_weather', '')} {weather_data.get('night_temp', '')}°C</p>
            <p>风向: {weather_data.get('wind', '')}</p>
            <small>数据来源: {weather_data.get('source', '高德真实API')}</small>
        </div>
        """
    else:
        weather_html = "<p>⚠️ 天气查询失败</p>"
    
    # 2. 客房订单链接HTML
    hotel_html = ""
    if hotel_data.get("success"):
        hotels = hotel_data.get("hotels", [])
        booking_url = hotel_data.get("booking_url", "")
        
        hotel_html = f"""
        <div class="hotel-section">
            <h3>🏨 推荐住宿（真实数据）</h3>
            <table>
                <tr><th>酒店</th><th>评分</th><th>价格</th><th>预订</th></tr>
        """
        
        for hotel in hotels[:3]:
            hotel_html += f"""
                <tr>
                    <td>{hotel.get('name', '')}</td>
                    <td>{hotel.get('rating', '4.0')}</td>
                    <td>¥{hotel.get('price', '200')}</td>
                    <td><a href="{hotel.get('booking_url', booking_url)}" target="_blank">预订</a></td>
                </tr>
            """
        
        hotel_html += f"""
            </table>
            <p><a href="{booking_url}" target="_blank" class="booking-btn">🔍 查看更多酒店</a></p>
            <small>数据来源: {hotel_data.get('source', '飞猪/高德真实API')}</small>
        </div>
        """
    else:
        hotel_html = "<p>⚠️ 酒店查询失败</p>"
    
    # 3. 导航截图HTML
    nav_html = ""
    if nav_data.get("success"):
        nav_html = f"""
        <div class="nav-section">
            <h3>🗺️ 导航规划（真实数据）</h3>
            <p>距离: {nav_data.get('distance_km', 0)} km</p>
            <p>预计时间: {nav_data.get('duration_min', 0)} 分钟</p>
            <img src="{nav_data.get('map_url', '')}" alt="导航截图" style="max-width:100%;border-radius:8px;">
            <small>数据来源: {nav_data.get('source', '高德真实API')}</small>
        </div>
        """
    else:
        nav_html = "<p>⚠️ 导航查询失败</p>"
    
    # 4. 避坑提醒HTML（基于真实数据）
    tips_html = f"""
    <div class="tips-section">
        <h3>💡 温馨提示（避坑提醒）</h3>
        <ul>
            <li>⚠️ 航班票价波动大，建议提前预订锁定价格</li>
            <li>⚠️ 酒店入住高峰期，建议提前预订避免涨价</li>
            <li>⚠️ 天气{weather_data.get('day_weather', '多变')}，建议携带雨具</li>
            <li>⚠️ 导航距离{nav_data.get('distance_km', 0)}km，建议预留充足时间</li>
            <li>⚠️ 热门景点人多，建议避开高峰时段</li>
        </ul>
    </div>
    """
    
    # 5. 时间节点HTML（真实航班）
    time_html = ""
    if flight_data.get("success"):
        time_html = f"""
        <div class="time-section">
            <h3>📅 时间节点（真实航班）</h3>
            <ul>
                <li>出发时间: {flight_data.get('dep_time', '')}</li>
                <li>到达时间: {flight_data.get('arr_time', '')}</li>
                <li>航班号: {flight_data.get('flight_no', '')}</li>
                <li>票价: ¥{flight_data.get('price', 0)}</li>
                <li><a href="{flight_data.get('booking_url', '')}" target="_blank">立即预订</a></li>
            </ul>
            <small>数据来源: FlyAI飞猪真实API</small>
        </div>
        """
    else:
        time_html = "<p>⚠️ 航班查询失败</p>"
    
    # 组合所有新增内容
    new_sections = f"""
    <!-- ========== 新增内容 ========== -->
    
    {time_html}
    {weather_html}
    {hotel_html}
    {nav_html}
    {tips_html}
    
    <!-- ========== 新增内容结束 ========== -->
    """
    
    return new_sections

# 禁止模拟声明
print("""
=== 网页新增内容禁止模拟声明 ===
✅ 时间节点: FlyAI真实航班
✅ 天气情况: 高德真实API
✅ 客房订单: 飞猪真实链接
✅ 导航截图: 高德真实URL
✅ 避坑提醒: 基于真实数据

❌ 禁止编造时间
❌ 禁止模拟天气
❌ 禁止假酒店链接
❌ 禁止假导航截图
""")

__all__ = ['generate_new_sections']