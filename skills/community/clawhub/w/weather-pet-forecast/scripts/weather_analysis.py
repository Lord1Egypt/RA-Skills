#!/usr/bin/env python3
"""
Weather Forecast Analysis Script
Analyzes 3-day weather forecast with recommendations for humans and pets
Output language is determined by the --lang parameter (default: en)
"""

import json
import sys
import argparse
from datetime import datetime

# Language strings
LANG = {
    'en': {
        'error_no_data': 'Sorry, unable to fetch weather data. Please try again later.',
        'error_parse': 'Sorry, error parsing weather data for {location}',
        'error_process': 'Sorry, error processing weather data for {location}: {error}',
        'location': '**{location}, {country}**',
        'subtitle': 'Pet-friendly weather report for you and your furry friend',
        'header': '**3-Day Weather Forecast Analysis**',
        'days': ['Today', 'Tomorrow', 'Day After'],
        'weekdays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'temp': 'Temperature: **{min}°C ~ {max}°C** (feels like {avg}°C)',
        'conditions': 'Conditions: {desc}',
        'precip': 'Precipitation: {chance}%',
        'wind': 'Wind: {speed} km/h {dir}',
        'uv_humidity': 'UV Index: {uv} | Humidity: {humidity}% | Visibility: {vis} km',
        'tip_high_rain': 'Tip: High chance of rain, bring an umbrella and dress warmly.',
        'tip_high_uv': 'Tip: Strong UV, apply sunscreen for both you and your pet.',
        'tip_hot': 'Tip: Hot weather, stay hydrated and avoid midday sun.',
        'tip_cold': 'Tip: Cold weather, bundle up and stay warm.',
        'tip_nice': 'Tip: Pleasant weather, perfect for outdoor activities!',
        'trend_header': '**Weather Trend Analysis**',
        'temp_rising': 'Temperature rising, from {t0}°C to {t2}°C',
        'temp_falling': 'Temperature dropping, from {t0}°C to {t2}°C',
        'temp_stable': 'Temperature stable, around {min}-{max}°C',
        'care_rising': 'Getting warmer, dress in layers for temperature changes.',
        'care_falling': 'Cooling down, add warm clothing to prevent colds. Keep pets warm too!',
        'care_stable': 'Stable weather, dress comfortably based on how you feel.',
        'rain_none': 'No rain expected in the next 3 days',
        'rain_none_care': 'Great weather for outdoor activities with your furry friend!',
        'rain_low': 'Low rain chance, {day} at {chance}%',
        'rain_low_care': 'Good weather, plan outdoor activities with confidence.',
        'rain_one': '{day} may have rain ({chance}%)',
        'rain_one_care': 'Bring an umbrella. Use a pet raincoat for walks.',
        'rain_multiple': 'Rain expected on {count} days',
        'rain_multiple_care': 'Prepare rain gear. Keep joints warm in damp weather.',
        'human_header': '**Recommendations for You**',
        'human_intro': 'Based on the upcoming weather, here are some suggestions:',
        'clothing_freezing': 'Down jacket, heavy coat, scarf and gloves',
        'clothing_freezing_care': 'Very cold! Bundle up completely. Don\'t forget hat and scarf.',
        'clothing_cold': 'Heavy coat or down jacket',
        'clothing_cold_care': 'Cold weather - layer up so you can adjust as needed.',
        'clothing_cool': 'Coat or sweater',
        'clothing_cool_care': 'Temperature swings - bring a light jacket just in case.',
        'clothing_mild': 'Long sleeves or light jacket',
        'clothing_mild_care': 'Comfortable weather - dress casually and comfortably.',
        'clothing_warm': 'Long sleeves or light shirt',
        'clothing_warm_care': 'Pleasant temperature - wear what feels good.',
        'clothing_hot': 'Short sleeves or light clothing',
        'clothing_hot_care': 'Warm weather - stay hydrated and use sun protection.',
        'clothing_label': 'Clothing',
        'umbrella_must': 'Definitely bring an umbrella!',
        'umbrella_must_care': 'High rain chance - don\'t get caught in the rain, health comes first.',
        'umbrella_maybe': 'Bring an umbrella just in case',
        'umbrella_maybe_care': 'Might rain - better safe than wet.',
        'umbrella_no': 'No umbrella needed',
        'umbrella_no_care': 'Nice weather - head out light!',
        'umbrella_label': 'Umbrella',
        'activity_indoor': 'Indoor activities recommended',
        'activity_indoor_care': 'Rainy days are good for rest, malls, or museums. Ventilate indoors.',
        'activity_flexible': 'Be flexible with outdoor plans',
        'activity_flexible_care': 'Check forecasts and choose dry windows. Stay safe during activities.',
        'activity_outdoor': 'Great for outdoor activities',
        'activity_outdoor_care': 'Wonderful weather for parks, cycling, or picnics. Use sun protection.',
        'activity_label': 'Activities',
        'pet_header': '**Pet Care Recommendations**',
        'pet_intro': 'Your furry friend needs special attention too~',
        'pet_temp_hot': 'High Temperature Warning!',
        'pet_time_hot': 'Best walking times: 6-8 AM, 7-9 PM',
        'pet_care_hot': [
            'Too hot! Dogs can get heatstroke easily.',
            'NEVER walk at noon - pavement can burn paws.',
            'Always carry water and a portable bowl.',
            'Choose shaded routes, avoid direct sun.',
            'Brachycephalic breeds (Frenchies, Pugs) are extra sensitive to heat.',
            'Cool down with a wet towel after returning home.'
        ],
        'pet_temp_warm': 'Warm Weather',
        'pet_time_warm': 'Suggested walking times: 7-9 AM, 6-8 PM',
        'pet_care_warm': [
            'Temperature is elevated - take extra care.',
            'Shorten outdoor time to 15-20 minutes.',
            'Bring plenty of water for hydration.',
            'Watch for heavy panting or excessive drooling (heatstroke signs).',
            'Check paws for overheating after walks.',
            'Thick-coated dogs may benefit from a trim.'
        ],
        'pet_temp_freezing': 'Low Temperature Warning!',
        'pet_time_freezing': 'Suggested walking times: 11 AM - 2 PM (warmest)',
        'pet_care_freezing': [
            'Very cold! Your pet feels it too.',
            'Short-haired and small dogs MUST wear coats.',
            'Senior dogs and puppies have weak immunity - minimize outdoor time.',
            'Wipe paws and belly with warm water after returning.',
            'Check paws for frostbite.',
            'If shivering or lifting paws, it\'s too cold - head home.',
            'Salt/de-icer on ground is toxic - wash paws thoroughly.'
        ],
        'pet_temp_cold': 'Cold Weather',
        'pet_time_cold': 'Suggested walking times: 10 AM - 3 PM',
        'pet_care_cold': [
            'Chilly weather - keep your pet warm.',
            'Seniors, puppies, and short-haired dogs should wear coats.',
            'Active dogs can stay warm by running around.',
            'Dry off thoroughly after walks, especially paws.',
            'Cold weather burns more energy - consider increasing food slightly.'
        ],
        'pet_temp_good': 'Comfortable Temperature',
        'pet_time_good': 'Any time is fine, avoid strong midday UV',
        'pet_care_good': [
            'Perfect weather! Your pet will be happy.',
            'Extend outdoor time for more play.',
            'Great for parks and grassy areas.',
            'Remember to bring water.',
            'This is prime walking weather - enjoy time with your furry friend!'
        ],
        'pet_temp_label': 'Temperature Safety',
        'pet_time_label': 'Best Times',
        'pet_care_label': 'Care Guide',
        'rain_pet_high': [
            'Rainy Day Walking Guide:',
            'Put a raincoat on your pet to protect their fur.',
            'Choose waterproof or quick-dry dog jackets.',
            'Wet surfaces are slippery - shorten walks to 10-15 minutes.',
            'Dry thoroughly with towels immediately after returning, especially paws and belly.',
            'Use a blow dryer to dry fur - prevents colds and skin issues.',
            'Check ears for water and gently dry with cotton balls.',
            'Play indoor games to make up for less outdoor time.'
        ],
        'rain_pet_moderate': [
            'Possible Rain - Be Prepared:',
            'Carry a lightweight dog raincoat.',
            'Choose routes with shelter.',
            'If it rains, cut the walk short.',
            'Dry paws and belly after returning.'
        ],
        'rain_pet_low': [
            'Clear Weather - No Rain Protection Needed:',
            'Head out freely with your furry friend.',
            'Just bring enough water.',
            'Enjoy your outdoor time!'
        ],
        'rain_pet_label': 'Rain Preparation',
        'ground_hot': [
            'Hot Pavement Risk! Test with your hand:',
            'Press the back of your hand on the ground for 7 seconds.',
            'If it\'s too hot for you, it\'s too hot for paws.',
            'Choose grassy or shaded routes.',
            'Or wait until evening when ground cools.',
            'Dog booties can protect paws.'
        ],
        'ground_cold': [
            'Icy Ground Risk:',
            'Watch for slipping - choose cleared paths.',
            'Prevent your dog from licking salt/de-icer (toxic!).',
            'Rinse paws with warm water immediately after returning.',
            'Check paws for cracks or frostbite.',
            'Apply pet paw protection balm.'
        ],
        'ground_safe': [
            'Safe Ground Conditions:',
            'Paws won\'t be injured - walk freely.',
            'For long walks, periodically check paws.',
            'Keep paws clean and dry.'
        ],
        'ground_label': 'Ground Conditions',
        'uv_high': [
            'High UV Index - Pets Need Sun Protection:',
            'White/light-colored fur dogs sunburn more easily.',
            'Hairless or short-haired breeds need pet-safe sunscreen.',
            'Apply to ears, nose, belly - exposed areas.',
            'Avoid 10 AM - 4 PM peak UV hours.',
            'Choose shaded walking routes.',
            'Bring plenty of water to prevent dehydration.'
        ],
        'uv_moderate': [
            'Moderate UV - Some Protection Needed:',
            'Minimize outdoor time during 11 AM - 2 PM.',
            'Light-colored dogs can use pet sunscreen.',
            'Provide shade and plenty of water.',
            'Watch for signs of discomfort, rest as needed.'
        ],
        'uv_low': [
            'Safe UV Level - No Special Protection Needed:',
            'Normal outdoor activities are fine.',
            'Keep water available.',
            'Enjoy sunshine but don\'t overdo exposure.'
        ],
        'uv_label': 'UV Protection',
        'outdoor_header': '**Best Outdoor Activity Times**',
        'outdoor_all_good': 'Great weather all 3 days!',
        'outdoor_all_good_care': 'Perfect for family outings or a full day at the park with your furry friend!',
        'outdoor_best_days': 'Recommended days: **{days}**',
        'outdoor_best_days_care': 'These days look good - plan your outdoor activities!',
        'outdoor_rainy': 'Rain possible all 3 days - stay flexible',
        'outdoor_rainy_care': 'Watch real-time weather for dry spells to sneak in a walk.',
        'outdoor_rainy_alt': 'Or enjoy cozy indoor play time with your pet~',
        'closing': 'Wishing you and your furry friend health and happiness!',
        'closing_rain': 'Remember: rainy days have their charm, sunny days have their joy.',
        'closing_pet': 'Your pet\'s company makes every day warmer~',
        'temp_label': 'Temperature',
        'precip_label': 'Precipitation',
    },
    'zh': {
        'error_no_data': '抱歉，无法获取天气数据，请稍后再试。',
        'error_parse': '抱歉，解析 {location} 的天气数据时出错',
        'error_process': '抱歉，处理 {location} 的天气数据时出错: {error}',
        'location': '**{location}, {country}**',
        'subtitle': '为您和毛孩子准备的专属天气报告',
        'header': '**三天天气贴心分析**',
        'days': ['今天', '明天', '后天'],
        'weekdays': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        'temp': '温度: **{min}°C ~ {max}°C** (体感 {avg}°C)',
        'conditions': '天气: {desc}',
        'precip': '降水概率: {chance}%',
        'wind': '风力: {speed} km/h {dir}',
        'uv_humidity': 'UV指数: {uv} | 湿度: {humidity}% | 能见度: {vis} km',
        'tip_high_rain': '小贴士：雨势较大，记得带伞，多穿件衣服。',
        'tip_high_uv': '小贴士：紫外线较强，给您和毛孩子做好防晒。',
        'tip_hot': '小贴士：天气炎热，注意防暑降温。',
        'tip_cold': '小贴士：天气寒冷，注意保暖。',
        'tip_nice': '小贴士：天气舒适，适合户外活动~',
        'trend_header': '**天气趋势分析**',
        'temp_rising': '温度上升，从 {t0}°C 升至 {t2}°C',
        'temp_falling': '温度下降，从 {t0}°C 降至 {t2}°C',
        'temp_stable': '温度稳定，保持在 {min}-{max}°C 左右',
        'care_rising': '天气转暖，可适当减少衣物，但早晚温差大，建议备件外套。',
        'care_falling': '降温了，请添衣保暖，预防感冒。毛孩子也要注意保暖！',
        'care_stable': '天气稳定，根据体感选择舒适着装。',
        'rain_none': '未来三天无降水',
        'rain_none_care': '天气晴好，适合带毛孩子出门活动！',
        'rain_low': '基本无雨，{day}降水概率 {chance}%',
        'rain_low_care': '天气不错，可以安心安排户外活动。',
        'rain_one': '{day}可能下雨 ({chance}%)',
        'rain_one_care': '出门带伞。遛狗时给毛孩子穿雨衣。',
        'rain_multiple': '未来三天有 {count} 天可能下雨',
        'rain_multiple_care': '准备雨具。湿气重，注意关节保暖。',
        'human_header': '**给您的建议**',
        'human_intro': '根据这几天天气，给您一些建议：',
        'clothing_freezing': '羽绒服、厚外套、围巾手套',
        'clothing_freezing_care': '天冷！一定要穿戴暖和，围巾帽子别落下。',
        'clothing_cold': '厚外套或羽绒服',
        'clothing_cold_care': '天气较冷，多穿几层，热了可脱，冷了能保暖。',
        'clothing_cool': '外套或毛衣',
        'clothing_cool_care': '早晚温差大，带件薄外套备用。',
        'clothing_mild': '长袖或薄外套',
        'clothing_mild_care': '天气舒适，穿着轻松自在。',
        'clothing_warm': '长袖或薄衫',
        'clothing_warm_care': '温度宜人，怎么穿都舒服。',
        'clothing_hot': '短袖或薄衣',
        'clothing_hot_care': '天气暖和，注意防晒，多补水。',
        'clothing_label': '穿衣建议',
        'umbrella_must': '一定要带伞！',
        'umbrella_must_care': '降水概率高，别为了赶时间淋雨，健康最重要。',
        'umbrella_maybe': '建议带伞备用',
        'umbrella_maybe_care': '可能会下雨，带着有备无患。',
        'umbrella_no': '无需带伞',
        'umbrella_no_care': '天气不错，轻松出门~',
        'umbrella_label': '雨具准备',
        'activity_indoor': '室内活动为主',
        'activity_indoor_care': '雨天适合在家休息或去商场、博物馆。注意通风。',
        'activity_flexible': '户外活动需灵活安排',
        'activity_flexible_care': '提前看天气预报，选择不下雨的时段出门。',
        'activity_outdoor': '很适合户外活动',
        'activity_outdoor_care': '天气给力，去公园散步、骑行或野餐都不错。注意防晒。',
        'activity_label': '活动安排',
        'pet_header': '**给毛孩子的关爱建议**',
        'pet_intro': '家里的小宝贝也需要特别照顾~',
        'pet_temp_hot': '高温预警！',
        'pet_time_hot': '最佳遛狗时段：早上 6-8 点，晚上 7-9 点',
        'pet_care_hot': [
            '太热了！狗狗容易中暑！',
            '绝对不要中午遛狗，地面温度可能烫伤爪子。',
            '随时携带水和便携碗。',
            '选择有树荫的路线。',
            '短鼻犬（法斗、巴哥）更怕热，要格外小心。',
            '回家后用湿毛巾给狗狗降温。'
        ],
        'pet_temp_warm': '天气较热',
        'pet_time_warm': '建议遛狗时段：早上 7-9 点，晚上 6-8 点',
        'pet_care_warm': [
            '温度有点高，需要多注意。',
            '缩短户外时间，15-20分钟为宜。',
            '带足饮水。',
            '观察是否喘气过重、流口水过多（中暑征兆）。',
            '回家后检查爪子是否过热。',
            '厚毛狗狗可以考虑修剪毛发。'
        ],
        'pet_temp_freezing': '低温预警！',
        'pet_time_freezing': '建议遛狗时段：中午 11 点-下午 2 点（较暖时）',
        'pet_care_freezing': [
            '很冷！毛孩子也会觉得冷。',
            '短毛犬、小型犬一定要穿衣服。',
            '老年犬和幼犬抵抗力弱，缩短外出时间。',
            '回家后用温水擦干爪子和肚子。',
            '检查爪子有无冻伤。',
            '如果发抖或抬脚，说明太冷了，赶紧回家。',
            '地面可能有盐/融雪剂，回家要洗干净爪子。'
        ],
        'pet_temp_cold': '天气较冷',
        'pet_time_cold': '建议遛狗时段：上午 10 点-下午 3 点',
        'pet_care_cold': [
            '有点冷，需要给毛孩子保暖。',
            '老年犬、幼犬、短毛犬建议穿衣服。',
            '正常狗狗可以多跑动保暖。',
            '回家后擦干身体，特别是爪子。',
            '冷天需要更多能量，可适当增加食物。'
        ],
        'pet_temp_good': '温度适宜',
        'pet_time_good': '全天都可以，避开正午强紫外线',
        'pet_care_good': [
            '天气刚刚好，毛孩子会很开心！',
            '可以延长户外时间，尽情玩耍。',
            '适合去公园、草地活动。',
            '记得带水。',
            '这是遛狗的黄金时段，享受和毛孩子的美好时光~'
        ],
        'pet_temp_label': '温度安全',
        'pet_time_label': '最佳时段',
        'pet_care_label': '照顾指南',
        'rain_pet_high': [
            '雨天遛狗指南：',
            '给毛孩子穿雨衣，保护毛发。',
            '选择防水或速干的狗狗外套。',
            '雨天路滑，缩短遛狗时间，10-15分钟即可。',
            '回家后立即擦干全身，特别是爪子和肚子。',
            '用吹风机吹干毛发，防止感冒和皮肤病。',
            '检查耳朵是否进水，用棉球轻轻擦干。',
            '雨天可以在家陪狗狗玩玩具。'
        ],
        'rain_pet_moderate': [
            '可能有雨，做好准备：',
            '随身携带轻便的狗狗雨衣。',
            '选择有遮蔽的路线。',
            '如果下雨，立即缩短散步时间。',
            '回家后擦干爪子和肚子。'
        ],
        'rain_pet_low': [
            '天气晴好，无需特别防雨：',
            '可以放心带毛孩子出门。',
            '准备充足的水即可。',
            '享受美好的户外时光~'
        ],
        'rain_pet_label': '防雨准备',
        'ground_hot': [
            '地面烫脚风险！用手背测试：',
            '将手背贴在地面 7 秒钟。',
            '如果觉得烫手，对狗狗爪子就太烫了。',
            '选择草地或树荫下的路线。',
            '或在傍晚地面降温后再出门。',
            '狗狗靴套可以保护爪子。'
        ],
        'ground_cold': [
            '地面结冰风险：',
            '注意防滑，选择已清理的路面。',
            '避免让狗狗舔食地面的盐/融雪剂（有毒！）。',
            '回家后立即用温水清洗爪子。',
            '检查爪子有无裂缝或冻伤。',
            '可以涂抹宠物爪子保护膏。'
        ],
        'ground_safe': [
            '地面安全，正常行走即可：',
            '爪子不会受伤，可以放心散步。',
            '如果长时间散步，定期检查爪子。',
            '保持爪子清洁干燥。'
        ],
        'ground_label': '地面状况',
        'uv_high': [
            'UV指数很高，毛孩子也需要防晒：',
            '白色/浅色毛发狗狗更容易晒伤。',
            '无毛或短毛品种需要宠物专用防晒霜。',
            '重点涂抹耳朵、鼻子、肚子等暴露部位。',
            '避开上午 10 点-下午 4 点的强紫外线时段。',
            '选择有树荫的散步路线。',
            '带充足的水，防止脱水。'
        ],
        'uv_moderate': [
            'UV中等，注意适度防护：',
            '正午时段(11-14点)尽量减少外出。',
            '浅色毛发的狗狗可以涂抹宠物防晒霜。',
            '提供充足的饮水和遮阴处。',
            '观察狗狗是否不适，及时休息。'
        ],
        'uv_low': [
            'UV安全，无需特别防晒：',
            '正常户外活动即可。',
            '保持充足的饮水。',
            '享受阳光但不过度暴晒。'
        ],
        'uv_label': '紫外线防护',
        'outdoor_header': '**最佳户外活动安排**',
        'outdoor_all_good': '未来三天天气都很好！',
        'outdoor_all_good_care': '很适合安排家庭出游或和毛孩子去公园玩一整天~',
        'outdoor_best_days': '推荐选择 **{days}** 出门',
        'outdoor_best_days_care': '这几天天气不错，可以好好安排户外活动。',
        'outdoor_rainy': '三天都可能有雨，建议灵活安排',
        'outdoor_rainy_care': '关注实时天气，抓住雨停的间隙出门散步。',
        'outdoor_rainy_alt': '或者在家陪毛孩子玩，也是温馨的亲子时光~',
        'closing': '祝您和毛孩子健康快乐！',
        'closing_rain': '雨天有雨天的浪漫，晴天有晴天的美好。',
        'closing_pet': '毛孩子的陪伴，让每一天都充满温暖~',
        'temp_label': '温度变化',
        'precip_label': '降水情况',
    }
}


def t(key, lang='en', **kwargs):
    """Translate a key to the specified language with formatting."""
    if lang not in LANG:
        lang = 'en'
    strings = LANG[lang]
    if key not in strings:
        # Fallback to English if key not found
        strings = LANG['en']
    text = strings.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def analyze_weather(data, location_name=None, lang='en'):
    """Analyze weather data with recommendations for humans and pets."""
    
    if not data or 'weather' not in data:
        return t('error_no_data', lang)
    
    # Get location
    location = location_name or data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value', 'Unknown')
    country = data.get('nearest_area', [{}])[0].get('country', [{}])[0].get('value', '')
    
    output = []
    output.append(f"📍 {t('location', lang, location=location, country=country)}")
    output.append("")
    output.append(f"💕 {t('subtitle', lang)}")
    output.append("")
    output.append(f"📅 {t('header', lang)}")
    output.append("")
    
    # Parse 3-day data
    days_data = []
    day_names = t('days', lang)
    weekdays = t('weekdays', lang)
    
    for i, day in enumerate(data['weather'][:3]):
        date = day['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        weekday = weekdays[date_obj.weekday()]
        
        max_temp = int(day['maxtempC'])
        min_temp = int(day['mintempC'])
        avg_temp = int(day['avgtempC'])
        
        # Get noon data
        noon_data = day['hourly'][4]
        desc = noon_data['weatherDesc'][0]['value']
        humidity = int(noon_data['humidity'])
        wind_speed = int(noon_data['windspeedKmph'])
        wind_dir = noon_data['winddir16Point']
        uv_index = int(noon_data['uvIndex'])
        rain_chance = int(noon_data['chanceofrain'])
        visibility = int(noon_data['visibility'])
        
        day_name = day_names[i]
        
        # Day-by-day forecast
        output.append(f"**【{day_name}】{date} {weekday}**")
        output.append(f"🌡️ {t('temp', lang, min=min_temp, max=max_temp, avg=avg_temp)}")
        output.append(f"☁️ {t('conditions', lang, desc=desc)}")
        output.append(f"🌧️ {t('precip', lang, chance=rain_chance)}")
        output.append(f"💨 {t('wind', lang, speed=wind_speed, dir=wind_dir)}")
        output.append(f"☀️ {t('uv_humidity', lang, uv=uv_index, humidity=humidity, vis=visibility)}")
        
        # Add tips
        if rain_chance > 70:
            output.append(f"💭 {t('tip_high_rain', lang)}")
        elif uv_index > 6:
            output.append(f"💭 {t('tip_high_uv', lang)}")
        elif max_temp > 30:
            output.append(f"💭 {t('tip_hot', lang)}")
        elif min_temp < 0:
            output.append(f"💭 {t('tip_cold', lang)}")
        elif rain_chance == 0 and uv_index < 4:
            output.append(f"💭 {t('tip_nice', lang)}")
        
        output.append("")
        
        days_data.append({
            'name': day_name,
            'date': date,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'avg_temp': avg_temp,
            'desc': desc,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'rain_chance': rain_chance,
            'uv_index': uv_index,
            'visibility': visibility
        })
    
    # Trend Analysis
    output.append("---")
    output.append("")
    output.append(f"📊 {t('trend_header', lang)}")
    output.append("")
    
    temps = [d['max_temp'] for d in days_data]
    min_temps = [d['min_temp'] for d in days_data]
    rain_chances = [d['rain_chance'] for d in days_data]
    
    # Temperature trend
    temp_change = temps[2] - temps[0]
    if temp_change > 5:
        temp_trend = t('temp_rising', lang, t0=temps[0], t2=temps[2])
        temp_care = t('care_rising', lang)
    elif temp_change < -5:
        temp_trend = t('temp_falling', lang, t0=temps[0], t2=temps[2])
        temp_care = t('care_falling', lang)
    else:
        temp_trend = t('temp_stable', lang, min=min_temps[0], max=temps[0])
        temp_care = t('care_stable', lang)
    
    output.append(f"• **{t('temp_label', lang)}**: {temp_trend}")
    output.append(f"• **{t('precip_label', lang)}**: {temp_care}")
    output.append("")
    
    # Precipitation
    wet_days = sum(1 for r in rain_chances if r > 50)
    max_rain = max(rain_chances)
    rain_day_idx = rain_chances.index(max_rain) if max_rain > 0 else -1
    rain_day_name = days_data[rain_day_idx]['name'] if rain_day_idx >= 0 else ''
    
    if max_rain == 0:
        output.append(f"• {t('rain_none', lang)}")
        output.append(f"• {t('rain_none_care', lang)}")
    elif wet_days == 0:
        output.append(f"• {t('rain_low', lang, day=rain_day_name, chance=max_rain)}")
        output.append(f"• {t('rain_low_care', lang)}")
    elif wet_days == 1:
        output.append(f"• {t('rain_one', lang, day=rain_day_name, chance=max_rain)}")
        output.append(f"• {t('rain_one_care', lang)}")
    else:
        output.append(f"• {t('rain_multiple', lang, count=wet_days)}")
        output.append(f"• {t('rain_multiple_care', lang)}")
    output.append("")
    
    # Human recommendations
    output.append("---")
    output.append("")
    output.append(f"👥 {t('human_header', lang)}")
    output.append("")
    output.append(t('human_intro', lang))
    output.append("")
    
    # Clothing
    avg_min = sum(min_temps) / 3
    if avg_min < 0:
        clothing = t('clothing_freezing', lang)
        clothing_care = t('clothing_freezing_care', lang)
    elif avg_min < 5:
        clothing = t('clothing_cold', lang)
        clothing_care = t('clothing_cold_care', lang)
    elif avg_min < 10:
        clothing = t('clothing_cool', lang)
        clothing_care = t('clothing_cool_care', lang)
    elif avg_min < 15:
        clothing = t('clothing_mild', lang)
        clothing_care = t('clothing_mild_care', lang)
    elif avg_min < 20:
        clothing = t('clothing_warm', lang)
        clothing_care = t('clothing_warm_care', lang)
    else:
        clothing = t('clothing_hot', lang)
        clothing_care = t('clothing_hot_care', lang)
    
    output.append(f"🧥 **{t('clothing_label', lang)}**: {clothing}")
    output.append(f"   💡 {clothing_care}")
    output.append("")
    
    # Umbrella
    if max_rain > 60:
        umbrella = t('umbrella_must', lang)
        umbrella_care = t('umbrella_must_care', lang)
    elif max_rain > 30:
        umbrella = t('umbrella_maybe', lang)
        umbrella_care = t('umbrella_maybe_care', lang)
    else:
        umbrella = t('umbrella_no', lang)
        umbrella_care = t('umbrella_no_care', lang)
    
    output.append(f"🌂 **{t('umbrella_label', lang)}**: {umbrella}")
    output.append(f"   💡 {umbrella_care}")
    output.append("")
    
    # Activity
    if wet_days >= 2:
        activity = t('activity_indoor', lang)
        activity_care = t('activity_indoor_care', lang)
    elif max_rain > 50:
        activity = t('activity_flexible', lang)
        activity_care = t('activity_flexible_care', lang)
    else:
        activity = t('activity_outdoor', lang)
        activity_care = t('activity_outdoor_care', lang)
    
    output.append(f"🏃 **{t('activity_label', lang)}**: {activity}")
    output.append(f"   💡 {activity_care}")
    output.append("")
    
    # Pet recommendations
    output.append("---")
    output.append("")
    output.append(f"🐕 {t('pet_header', lang)}")
    output.append("")
    output.append(t('pet_intro', lang))
    output.append("")
    
    # Pet temperature safety
    avg_max = sum(temps) / 3
    if avg_max > 30:
        pet_temp = t('pet_temp_hot', lang)
        pet_time = t('pet_time_hot', lang)
        pet_care = t('pet_care_hot', lang)
    elif avg_max > 25:
        pet_temp = t('pet_temp_warm', lang)
        pet_time = t('pet_time_warm', lang)
        pet_care = t('pet_care_warm', lang)
    elif avg_min < 0:
        pet_temp = t('pet_temp_freezing', lang)
        pet_time = t('pet_time_freezing', lang)
        pet_care = t('pet_care_freezing', lang)
    elif avg_min < 5:
        pet_temp = t('pet_temp_cold', lang)
        pet_time = t('pet_time_cold', lang)
        pet_care = t('pet_care_cold', lang)
    else:
        pet_temp = t('pet_temp_good', lang)
        pet_time = t('pet_time_good', lang)
        pet_care = t('pet_care_good', lang)
    
    output.append(f"🌡️ **{t('pet_temp_label', lang)}**: {pet_temp}")
    output.append(f"⏰ **{t('pet_time_label', lang)}**: {pet_time}")
    output.append("")
    output.append(f"💝 **{t('pet_care_label', lang)}**:")
    for line in pet_care:
        output.append(f"   • {line}")
    output.append("")
    
    # Pet rain protection
    if max_rain > 50:
        rain_pet = t('rain_pet_high', lang)
    elif max_rain > 20:
        rain_pet = t('rain_pet_moderate', lang)
    else:
        rain_pet = t('rain_pet_low', lang)
    
    output.append(f"🌧️ **{t('rain_pet_label', lang)}**:")
    for line in rain_pet:
        output.append(f"   • {line}")
    output.append("")
    
    # Ground safety
    if avg_max > 28:
        ground_pet = t('ground_hot', lang)
    elif avg_min < 0:
        ground_pet = t('ground_cold', lang)
    else:
        ground_pet = t('ground_safe', lang)
    
    output.append(f"🐾 **{t('ground_label', lang)}**:")
    for line in ground_pet:
        output.append(f"   • {line}")
    output.append("")
    
    # UV protection
    max_uv = max(d['uv_index'] for d in days_data)
    if max_uv > 7:
        uv_pet = t('uv_high', lang)
    elif max_uv > 4:
        uv_pet = t('uv_moderate', lang)
    else:
        uv_pet = t('uv_low', lang)
    
    output.append(f"☀️ **{t('uv_label', lang)}**:")
    for line in uv_pet:
        output.append(f"   • {line}")
    output.append("")
    
    # Best days for outdoor
    output.append("---")
    output.append("")
    output.append(f"⏰ {t('outdoor_header', lang)}")
    output.append("")
    
    if max(rain_chances) < 30:
        output.append(f"✨ {t('outdoor_all_good', lang)}")
        output.append(f"   💝 {t('outdoor_all_good_care', lang)}")
    else:
        good_days = [days_data[i]['name'] for i, r in enumerate(rain_chances) if r < 30]
        if good_days:
            output.append(f"✨ {t('outdoor_best_days', lang, days='、'.join(good_days) if lang == 'zh' else ', '.join(good_days))}")
            output.append(f"   💝 {t('outdoor_best_days_care', lang)}")
        else:
            output.append(f"✨ {t('outdoor_rainy', lang)}")
            output.append(f"   💝 {t('outdoor_rainy_care', lang)}")
            output.append(f"   💝 {t('outdoor_rainy_alt', lang)}")
    
    output.append("")
    output.append("---")
    output.append("")
    output.append(f"💝 {t('closing', lang)}")
    output.append(f"🌧️ {t('closing_rain', lang)}")
    output.append(f"🐕 {t('closing_pet', lang)}")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='Weather forecast analysis for humans and pets')
    parser.add_argument('location', nargs='?', default='Beijing', help='Location name')
    parser.add_argument('--lang', '-l', default='en', choices=['en', 'zh'], help='Output language (default: en)')
    args = parser.parse_args()
    
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            print(t('error_no_data', args.lang), file=sys.stderr)
            sys.exit(1)
        
        data = json.loads(input_data)
        
        if 'weather' not in data:
            print(t('error_parse', args.lang, location=args.location), file=sys.stderr)
            sys.exit(1)
        
        print(analyze_weather(data, args.location, args.lang))
    except json.JSONDecodeError as e:
        print(t('error_parse', args.lang, location=args.location), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(t('error_process', args.lang, location=args.location, error=e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
