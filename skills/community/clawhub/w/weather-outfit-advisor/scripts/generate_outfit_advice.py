#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整穿搭建议生成示例脚本
整合天气查询和图片搜索，生成完整的穿搭建议

使用方法：
    python generate_outfit_advice.py <city> [date] [style_preference]
    
示例：
    python generate_outfit_advice.py Paris "2026-06-01" casual
    python generate_outfit_advice.py 北京 tomorrow business
"""

import sys
import json
import subprocess
from datetime import datetime


def run_script(script_name: str, *args):
    """运行脚本并返回 JSON 结果"""
    cmd = ["python3", script_name] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 解析 stdout 中的 JSON
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"错误：无法解析 {script_name} 的输出", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return None


def generate_outfit_advice(city: str, date: str, style: str = "casual"):
    """
    生成完整的穿搭建议
    
    Args:
        city: 城市名称
        date: 日期
        style: 风格偏好（casual/business/sporty等）
    """
    print("=" * 60, file=sys.stderr)
    print(f"正在生成 {city} 的穿搭建议...", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # 步骤 1: 查询天气
    print("\n📊 步骤 1: 查询天气...", file=sys.stderr)
    weather_data = run_script("get_weather.py", city, date)
    
    if not weather_data or not weather_data.get('success'):
        print("❌ 天气查询失败", file=sys.stderr)
        return
    
    forecast = weather_data.get('forecast', {})
    current = weather_data.get('current', {})
    
    # 提取关键信息
    max_temp = forecast.get('max_temp_c', 0)
    min_temp = forecast.get('min_temp_c', 0)
    weather_desc = forecast.get('weather_desc', '')
    rain_chance = forecast.get('daily_chance_of_rain', 0)
    humidity = current.get('humidity', 0)
    
    print(f"✓ 温度：{min_temp}-{max_temp}°C", file=sys.stderr)
    print(f"✓ 天气：{weather_desc}", file=sys.stderr)
    print(f"✓ 降雨概率：{rain_chance}%", file=sys.stderr)
    
    # 步骤 2: 搜索图片
    print("\n📸 步骤 2: 搜索穿搭参考图片...", file=sys.stderr)
    
    # 根据风格生成搜索词
    search_terms = {
        'casual': f"{city} casual outfit",
        'business': f"{city} business attire",
        'sporty': f"{city} sporty style",
        'fashion': f"{city} street style fashion"
    }
    
    search_query = search_terms.get(style, f"{city} outfit")
    image_data = run_script("search_images.py", search_query, "5")
    
    if image_data and image_data.get('success'):
        print(f"✓ 找到 {len(image_data.get('images', []))} 张图片", file=sys.stderr)
    else:
        print("⚠️ 图片搜索不可用，将提供文字建议", file=sys.stderr)
    
    # 步骤 3: 生成穿搭建议
    print("\n👔 步骤 3: 生成穿搭建议...", file=sys.stderr)
    
    # 根据温度确定穿搭
    if max_temp < 5:
        outfit = {
            'top': '厚羽绒服 + 保暖内衣 + 厚毛衣',
            'bottom': '加绒裤子/羽绒裤',
            'shoes': '保暖防水靴子',
            'accessories': '围巾、手套、帽子、暖宝宝'
        }
    elif max_temp < 10:
        outfit = {
            'top': '厚外套/棉服 + 毛衣/针织衫',
            'bottom': '牛仔裤/休闲裤 + 秋裤',
            'shoes': '运动鞋/短靴',
            'accessories': '围巾、帽子'
        }
    elif max_temp < 15:
        outfit = {
            'top': '风衣/夹克 + 卫衣/长袖 T 恤',
            'bottom': '牛仔裤/休闲裤',
            'shoes': '运动鞋/休闲鞋',
            'accessories': '薄围巾'
        }
    elif max_temp < 20:
        outfit = {
            'top': '薄外套/牛仔外套 + 长袖衬衫/T 恤',
            'bottom': '休闲裤/裙子',
            'shoes': '休闲鞋/乐福鞋',
            'accessories': '可选配饰'
        }
    elif max_temp < 25:
        outfit = {
            'top': '长袖 T 恤/薄衬衫',
            'bottom': '休闲裤/裙子',
            'shoes': '休闲鞋',
            'accessories': '太阳镜'
        }
    elif max_temp < 30:
        outfit = {
            'top': '短袖 T 恤/衬衫',
            'bottom': '短裤/裙子',
            'shoes': '凉鞋/透气运动鞋',
            'accessories': '遮阳帽、太阳镜'
        }
    else:
        outfit = {
            'top': '透气短袖/背心/防晒衣',
            'bottom': '短裤/短裙',
            'shoes': '凉鞋',
            'accessories': '遮阳帽、防晒霜、小风扇'
        }
    
    # 根据天气调整
    tips = []
    if rain_chance > 50:
        outfit['accessories'] += '、雨伞/雨衣'
        tips.append('☔ 降雨概率较高，务必携带雨具')
        outfit['shoes'] = '防水鞋子'
    
    if humidity > 70:
        tips.append('💦 湿度较大，建议选择透气速干面料')
    
    if current.get('wind_speed_kmph', 0) > 20:
        tips.append('💨 风力较大，避免穿裙子或选择防走光款式')
    
    if current.get('uv_index', 0) >= 6:
        tips.append('☀️ 紫外线较强，注意防晒')
        outfit['accessories'] += '、防晒霜'
    
    # 输出完整建议
    print("\n" + "=" * 60, file=sys.stderr)
    print("✅ 穿搭建议已生成！", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # 打印 Markdown 格式的建议
    output = []
    output.append(f"\n## 📍 目的地：{city}")
    output.append(f"## 📅 日期：{forecast.get('target_date', date)}")
    output.append("")
    output.append("## 🌤️ 天气概况")
    output.append(f"- **温度**：{min_temp}-{max_temp}°C")
    output.append(f"- **天气状况**：{weather_desc}")
    output.append(f"- **湿度**：{humidity}%")
    output.append(f"- **降雨概率**：{rain_chance}%")
    output.append("")
    output.append("## 👔 穿搭建议")
    output.append("")
    output.append("### 推荐搭配")
    output.append(f"- **上身**：{outfit['top']}")
    output.append(f"- **下身**：{outfit['bottom']}")
    output.append(f"- **鞋子**：{outfit['shoes']}")
    output.append(f"- **配件**：{outfit['accessories']}")
    output.append("")
    
    if tips:
        output.append("### ⚠️ 注意事项")
        for tip in tips:
            output.append(f"- {tip}")
        output.append("")
    
    # 添加图片参考
    if image_data and image_data.get('success') and image_data.get('images'):
        output.append("## 🖼️ 穿搭参考图片")
        output.append("")
        output.append(f"搜索关键词：{search_query}")
        output.append("")
        
        for i, img in enumerate(image_data['images'], 1):
            output.append(f"### 图片{i}: {img.get('photographer', 'Unknown')}")
            if img.get('alt'):
                output.append(f"**描述**：{img['alt']}")
            output.append(f"**尺寸**：{img.get('width', 0)}x{img.get('height', 0)}")
            output.append(f"[查看图片]({img.get('url', '#')})")
            output.append("")
    
    # 打印输出
    final_output = '\n'.join(output)
    print(final_output)
    
    return {
        'weather': weather_data,
        'images': image_data,
        'outfit': outfit,
        'tips': tips
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python generate_outfit_advice.py <city> [date] [style]")
        print("示例：python generate_outfit_advice.py Paris '2026-06-01' casual")
        print("      python generate_outfit_advice.py 北京 tomorrow business")
        sys.exit(1)
    
    city = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else 'tomorrow'
    style = sys.argv[3] if len(sys.argv) > 3 else 'casual'
    
    generate_outfit_advice(city, date, style)


if __name__ == '__main__':
    main()
