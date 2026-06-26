import requests
from rain_weather import plot_temp_precip
from cutimage import cutimage
from glass import add_rounded_frosted_glass_antialias
from PIL import Image, ImageDraw, ImageFont
from AI import AI
from makeimage import generate_image_with_zhipu
import os
import sys

# 字体路径（相对于脚本所在目录）
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simhei.ttf")

# 删除无用图片（忽略不存在的文件）
try:
    temp_files = ["1.png", "2.png", "3.png", "bg.png", "bg1.png", "bg2.png", "bg3.png",
                  "bg4.png", "bg5.png", "bg6.png", "bg7.png", "bg8.png", "bg9.png",
                  "bg10.png", "bg11.png"]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
except:
    pass
# ========== 中英文映射表 ==========
MOON_PHASE_CN = {
    "New Moon": "新月",
    "Waxing Crescent": "娥眉月",
    "First Quarter": "上弦月",
    "Waxing Gibbous": "盈凸月",
    "Full Moon": "满月",
    "Waning Gibbous": "亏凸月",
    "Last Quarter": "下弦月",
    "Waning Crescent": "残月",
}

WEATHER_DESC_CN = {
    "Sunny": "晴",
    "Clear": "晴",
    "Partly cloudy": "局部多云",
    "Partly Cloudy": "局部多云",
    "Cloudy": "多云",
    "Overcast": "阴",
    "Mist": "薄雾",
    "Fog": "雾",
    "Light rain": "小雨",
    "Moderate rain": "中雨",
    "Heavy rain": "大雨",
    "Light drizzle": "毛毛雨",
    "Patchy rain nearby": "局部有雨",
    "Light rain shower": "小阵雨",
    "Moderate rain at times": "有时中雨",
    "Heavy rain at times": "有时大雨",
    "Thunderstorm": "雷暴",
    "Thunderstorm with rain": "雷阵雨",
    "Thunderstorm with heavy rain": "强雷雨",
    "Snow": "雪",
    "Light snow": "小雪",
    "Heavy snow": "大雪",
    "Sleet": "雨夹雪",
    "Blizzard": "暴风雪",
    "Ice pellets": "冰粒",
    "Freezing drizzle": "冻毛毛雨",
    "Freezing rain": "冻雨",
    "Hail": "冰雹",
    "Hot": "炎热",
    "Cold": "寒冷",
    "Windy": "大风",
    "Duststorm": "沙尘暴",
    "Sandstorm": "沙尘暴",
    "Volcanic ash": "火山灰",
    "Tropical storm": "热带风暴",
    "Hurricane": "飓风",
    "Tornado": "龙卷风",
    "Clear night": "夜间晴朗",
    "Partly cloudy night": "夜间局部多云",
    "Cloudy night": "夜间多云",
}

def to_chinese(text: str, mapping: dict) -> str:
    """如果映射表中有对应的中文则返回中文，否则返回原文本"""
    return mapping.get(text.strip(), text)

def deg_to_cardinal(deg):
    """风向角度 → 中文十六方位"""
    dirs = ['北', '北北东', '东北', '东北东', '东', '东南东', '东南', '南南东',
            '南', '南南西', '西南', '西南西', '西', '西北西', '西北', '北北西']
    idx = int((deg + 11.25) // 22.5) % 16
    return dirs[idx]

def get_weather_structured(location="nanjing"):
    """
    获取指定地点当天的天气，返回结构化数据：
    - static_info: 不随时间变化的量（字典）
    - time_series: 随时间变化的量（字典，每个值是列表）
    所有天气描述、月相均为中文。
    """
    url = f"https://wttr.in/{location}?format=j1&lang=zh-cn&days=1"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None, None

    day = data['weather'][0]
    hourly = day['hourly']

    # ========== 静态信息 ==========
    moon_phase_en = day['astronomy'][0]['moon_phase']
    moon_phase_cn = to_chinese(moon_phase_en, MOON_PHASE_CN)

    static_info = {
        '温度最低_C': float(day['mintempC']),
        '温度最高_C': float(day['maxtempC']),
        '温度平均_C': float(day['avgtempC']),
        '总降水_mm': sum(float(h['precipMM']) for h in hourly),
        '日照时长_h': float(day['sunHour']),
        '日出时间': day['astronomy'][0]['sunrise'],
        '日落时间': day['astronomy'][0]['sunset'],
        '月相': moon_phase_cn,
        '月出时间': day['astronomy'][0]['moonrise'],
        '月落时间': day['astronomy'][0]['moonset'],
        '紫外线指数': int(day['uvIndex']),
    }

    # ========== 动态信息（逐小时列表） ==========
    time_series = {
        '时间点': [],
        '温度_C': [],
        '天气状况': [],
        '降水_mm': [],
        '降水概率_%': [],
        '湿度_%': [],
        '风速_Kmh': [],
        '风向文字': [],
        '风向角度': [],
        '气压_hPa': [],
        '能见度_Km': [],
        '紫外线指数': [],
    }

    for h in hourly:
        hour_int = int(h['time']) // 100
        time_series['时间点'].append(f"{hour_int}:00")
        time_series['温度_C'].append(float(h['tempC']))
        # 天气状况转换为中文
        weather_en = h['weatherDesc'][0]['value']
        weather_cn = to_chinese(weather_en, WEATHER_DESC_CN)
        time_series['天气状况'].append(weather_cn)
        time_series['降水_mm'].append(float(h['precipMM']))
        time_series['降水概率_%'].append(int(h['chanceofrain']))
        time_series['湿度_%'].append(int(h['humidity']))
        time_series['风速_Kmh'].append(float(h['windspeedKmph']))
        deg = float(h['winddirDegree'])
        time_series['风向角度'].append(deg)
        time_series['风向文字'].append(deg_to_cardinal(deg))
        time_series['气压_hPa'].append(int(h['pressure']))
        time_series['能见度_Km'].append(float(h['visibility']))
        time_series['紫外线指数'].append(int(h['uvIndex']))

    return static_info, time_series

def print_structured(static_info, time_series):
    """打印结构化数据（全部中文）"""
    print(f"\n🌡️  温度：{static_info['温度最低_C']:.1f} ~ {static_info['温度最高_C']:.1f}°C (平均 {static_info['温度平均_C']:.1f}°C)")
    print(f"       💧 总降水：{static_info['总降水_mm']:.1f} mm      ☀️ 日照时长：{static_info['日照时长_h']:.1f} h")
    print(f"       🌅 日出 {static_info['日出时间']}   🌇 日落 {static_info['日落时间']}")
    print(f"       🌙 月相：{static_info['月相']} (月出 {static_info['月出时间']}, 月落 {static_info['月落时间']})")
    print("       🕒 逐小时预报：")
    for i in range(len(time_series['时间点'])):
        line = (f"          {time_series['时间点'][i]}  {time_series['温度_C'][i]:.1f}°C  {time_series['天气状况'][i]}  "
                f"降水{time_series['降水_mm'][i]:.1f}mm({time_series['降水概率_%'][i]}%)  "
                f"湿度{time_series['湿度_%'][i]}%  风速{time_series['风速_Kmh'][i]:.1f}km/h {time_series['风向文字'][i]}")
        print(line)

def time_series_to_dict(time_series):
    """
    将 time_series 字典（值为列表）转换为以时间点为键的字典。
    输入: time_series = {'时间点': ['0:00','3:00',...], '温度_C': [17,16,...], ...}
    输出: {'0:00': {'温度_C': 17, ...}, '3:00': {...}, ...}
    """
    result = {}
    n = len(time_series['时间点'])
    for i in range(n):
        timestamp = time_series['时间点'][i]
        result[timestamp] = {}
        for key, values in time_series.items():
            if key != '时间点':
                result[timestamp][key] = values[i]
    return result

def series_to_field_dict(time_series):
    """
    将 time_series 字典（值为列表）转换为以字段名为键、以时间点为键的子字典。
    输入: time_series = {'时间点': ['0:00','3:00',...], '温度_C': [17,16,...], ...}
    输出: {'温度_C': {'0:00': 17, '3:00': 16, ...}, '降水_mm': {...}, ...}
    """
    result = {}
    fields = [key for key in time_series.keys() if key != '时间点']
    timestamps = time_series['时间点']
    n = len(timestamps)
    for field in fields:
        field_dict = {}
        for i in range(n):
            field_dict[timestamps[i]] = time_series[field][i]
        result[field] = field_dict
    return result

if __name__ == "__main__":
    # 支持命令行参数：python main.py 城市名
    # 例如：python main.py Nanjing
    if len(sys.argv) > 1:
        location = sys.argv[1]
    else:
        location = "Nanjing"  # 默认城市
    static, dynamic = get_weather_structured(location)
    if static and dynamic:
        # 1. 打印天气报表
        # print_structured(static, dynamic)

        # 2. 查看逐小时列表（原有结构）
        # print("\n逐小时温度列表:", dynamic['温度_C'])
        # print("逐小时降水列表:", dynamic['降水_mm'])
        # print("逐小时天气状况:", dynamic['天气状况'])

        # 3. 将列表转换为以时间为键的字典
        time_dict = time_series_to_dict(dynamic)
        # print("\n按时间索引的字典（所有字段）:")
        # print(time_dict)
        # print("\n按时间索引的字典示例（12:00）:")
        time_dict_1 = time_dict.get('12:00', {})
        # print(time_dict_1.get('温度_C', {}))

        # 4. 新增：将列表转换为以字段为键的字典
        field_dict = series_to_field_dict(dynamic)



        # print("\n以字段为键的字典（温度字段示例）:")
        # print(field_dict.get('温度_C', {}))
        # print("\n以字段为键的字典（湿度字段示例）:")
        # print(field_dict.get('湿度_%', {}))
        # print(field_dict.get('降水_mm', {}))

        weather_dict = (field_dict.get('天气状况', {}))
        generate_image_with_zhipu(weather_dict)
        # print(weather_dict.get('0:00', {}))




        # 5. 准备绘图数据（这里使用示例气温和降水，实际可改为从天气数据提取）
        # 注意：实际应用中您可以根据需要将 dynamic 中的温度、降水整合为字典键值
        # 这里为了演示 plot_temp_precip，保留原来的月份数据
        # temp_dict = {
        #     '一月': 12.5, '二月': 15.2, '三月': 18.0, '四月': 22.3,
        #     '五月': 25.1, '六月': 28.4, '七月': 30.2, '八月': 29.8,
        #     '九月': 25.6, '十月': 20.3, '十一月': 16.1, '十二月': 13.0
        # }
        # prec_dict = {
        #     '一月': 45, '二月': 52, '三月': 70, '四月': 88,
        #     '五月': 112, '六月': 158, '七月': 210, '八月': 195,
        #     '九月': 140, '十月': 86, '十一月': 58, '十二月': 40
        # }

        # 6. 调用绘图函数（需要保证 rain_weather.py 中存在 plot_temp_precip）
        plot_temp_precip(
            (field_dict.get('温度_C', {})), (field_dict.get('降水_mm', {})),
            components=('temp', 'precip'),  # 同时绘制气温和降水
            enable_adaptive=True,
            bar_downward_shift=-10,
            save_path='1.png',
            transparent=True
        )
        plot_temp_precip(
            (field_dict.get('湿度_%', {})),
            components=('temp'),
            bar_downward_shift=-10,
            save_path='2.png',
            transparent=True
        )
        plot_temp_precip(
            (field_dict.get('风速_Kmh', {})),
            components=('temp'),
            bar_downward_shift=-10,
            save_path='3.png',
            transparent=True
        )

        cutimage()

        add_rounded_frosted_glass_antialias(
            image_path="bg.png",
            output_path="bg1.png",
            rect_top_left=(50, 50),  # 直接指定左上角
            rect_size=(2410, 1080),
            corner_radius=100,
            blur_radius=12,
            overlay_opacity=160,
            ssaa_scale=2,
            edge_transition_radius=0
        )

        img_bg1 = Image.open("bg1.png")
        draw = ImageDraw.Draw(img_bg1)
        font1 = ImageFont.truetype(FONT_PATH, 500)
        font2 = ImageFont.truetype(FONT_PATH, 200)
        draw.text((100, 100), location, fill=(0,0,0),font=font1)
        draw.text((100, 700), "天气简报", fill=(0, 0, 0), font=font2)
        img_bg1.save("bg2.png")

        img1 = Image.open("1.png")
        img2 = Image.open("2.png")
        img3 = Image.open("3.png")

        add_rounded_frosted_glass_antialias(
            image_path="bg2.png",
            output_path="bg3.png",
            rect_top_left=(50, 1180),  # 直接指定左上角
            rect_size=(2410, (370+img1.height)),
            corner_radius=100,
            blur_radius=12,
            overlay_opacity=160,
            ssaa_scale=2,
            edge_transition_radius=0
        )
        add_rounded_frosted_glass_antialias(
            image_path="bg3.png",
            output_path="bg4.png",
            rect_top_left=(50, (1600+img1.height)),  # 直接指定左上角
            rect_size=(2410, (270+img2.height)),
            corner_radius=100,
            blur_radius=12,
            overlay_opacity=160,
            ssaa_scale=2,
            edge_transition_radius=0
        )
        add_rounded_frosted_glass_antialias(
            image_path="bg4.png",
            output_path="bg5.png",
            rect_top_left=(50, (1920+img1.height+img2.height)),  # 直接指定左上角
            rect_size=(2410, (270+img3.height)),
            corner_radius=100,
            blur_radius=12,
            overlay_opacity=160,
            ssaa_scale=2,
            edge_transition_radius=0
        )

        img_bg5 = Image.open("bg5.png")
        draw = ImageDraw.Draw(img_bg5)
        font3 = ImageFont.truetype(FONT_PATH, 150)
        draw.text((100, 1230), "温度(℃)&降水(mm)", fill=(0,0,0),font=font3)
        draw.text((100, (1650+img1.height)), "湿度(%)", fill=(0, 0, 0), font=font3)
        draw.text((100, (1970+img1.height+img2.height)), "风速(Kmh)", fill=(0, 0, 0), font=font3)
        img_bg5.save("bg6.png")

        # 贴图表
        background1 = Image.open("bg6.png")
        foreground1 = Image.open("1.png")
        background1.paste(foreground1, (70, 1380), foreground1)
        background1.save("bg7.png")

        background2 = Image.open("bg7.png")
        foreground2 = Image.open("2.png")
        background2.paste(foreground2, (70, (1800+img1.height)), foreground2)
        background2.save("bg8.png")

        background3 = Image.open("bg8.png")
        foreground3 = Image.open("3.png")
        background3.paste(foreground3, (70, (2120+img1.height+img2.height)), foreground3)
        background3.save("bg9.png")

        # 写文字
        img_bg6 = Image.open("bg9.png")
        draw = ImageDraw.Draw(img_bg6)
        font3 = ImageFont.truetype(FONT_PATH, 50)
        # 第一个图表的时间
        draw.text((220, (1380 + img1.height)), "0:00", fill=(0,0,0),font=font3)
        draw.text((500, (1380 + img1.height)), "3:00", fill=(0, 0, 0), font=font3)
        draw.text((780, (1380 + img1.height)), "6:00", fill=(0, 0, 0), font=font3)
        draw.text((1060, (1380 + img1.height)), "9:00", fill=(0, 0, 0), font=font3)
        draw.text((1340, (1380 + img1.height)), "12:00", fill=(0, 0, 0), font=font3)
        draw.text((1620, (1380 + img1.height)), "15:00", fill=(0, 0, 0), font=font3)
        draw.text((1900, (1380 + img1.height)), "18:00", fill=(0, 0, 0), font=font3)
        draw.text((2180, (1380 + img1.height)), "21:00", fill=(0, 0, 0), font=font3)
        # 第一个图表的天气情况
        draw.text((220, (1450 + img1.height)),(weather_dict.get('0:00', {})), fill=(0,0,0),font=font3)
        draw.text((500, (1450 + img1.height)), (weather_dict.get('3:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((780, (1450 + img1.height)), (weather_dict.get('6:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((1060, (1450 + img1.height)), (weather_dict.get('9:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((1340, (1450 + img1.height)), (weather_dict.get('12:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((1620, (1450 + img1.height)), (weather_dict.get('15:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((1900, (1450 + img1.height)), (weather_dict.get('18:00', {})), fill=(0, 0, 0), font=font3)
        draw.text((2180, (1450 + img1.height)), (weather_dict.get('21:00', {})), fill=(0, 0, 0), font=font3)

        # 第二个图表的时间
        draw.text((220, (1800+img1.height+img2.height)), "0:00", fill=(0,0,0),font=font3)
        draw.text((500, (1800+img1.height+img2.height)), "3:00", fill=(0, 0, 0), font=font3)
        draw.text((780, (1800+img1.height+img2.height)), "6:00", fill=(0, 0, 0), font=font3)
        draw.text((1060, (1800+img1.height+img2.height)), "9:00", fill=(0, 0, 0), font=font3)
        draw.text((1340, (1800+img1.height+img2.height)), "12:00", fill=(0, 0, 0), font=font3)
        draw.text((1620, (1800+img1.height+img2.height)), "15:00", fill=(0, 0, 0), font=font3)
        draw.text((1900, (1800+img1.height+img2.height)), "18:00", fill=(0, 0, 0), font=font3)
        draw.text((2180, (1800+img1.height+img2.height)), "21:00", fill=(0, 0, 0), font=font3)

        # 第三个图表的时间
        draw.text((220, (2120+img1.height+img2.height+img3.height)), "0:00", fill=(0, 0, 0), font=font3)
        draw.text((500, (2120+img1.height+img2.height+img3.height)), "3:00", fill=(0, 0, 0), font=font3)
        draw.text((780, (2120+img1.height+img2.height+img3.height)), "6:00", fill=(0, 0, 0), font=font3)
        draw.text((1060, (2120+img1.height+img2.height+img3.height)), "9:00", fill=(0, 0, 0), font=font3)
        draw.text((1340, (2120+img1.height+img2.height+img3.height)), "12:00", fill=(0, 0, 0), font=font3)
        draw.text((1620, (2120+img1.height+img2.height+img3.height)), "15:00", fill=(0, 0, 0), font=font3)
        draw.text((1900, (2120+img1.height+img2.height+img3.height)), "18:00", fill=(0, 0, 0), font=font3)
        draw.text((2180, (2120+img1.height+img2.height+img3.height)), "21:00", fill=(0, 0, 0), font=font3)

        img_bg6.save("bg10.png")

        add_rounded_frosted_glass_antialias(
            image_path="bg10.png",
            output_path="bg11.png",
            rect_top_left=(50, (2240+img1.height+img2.height+img3.height)),  # 直接指定左上角
            rect_size=(2410, 1080),
            corner_radius=100,
            blur_radius=12,
            overlay_opacity=160,
            ssaa_scale=2,
            edge_transition_radius=0
        )
        # 其他数据
        img_bg7 = Image.open("bg11.png")
        draw = ImageDraw.Draw(img_bg7)
        font3 = ImageFont.truetype(FONT_PATH, 60)
        draw.text((100, (2290+img1.height+img2.height+img3.height)), f"日出时间: {static['日出时间']}     日落时间: {static['日落时间']}     日照时长: {static['日照时长_h']}h", fill=(0,0,0),font=font3)
        draw.text((100, (2440+img1.height+img2.height+img3.height)), f"月出时间: {static['月出时间']}     月落时间: {static['月落时间']}     月相: {static['月相']}", fill=(0, 0, 0), font=font3)
        draw.text((100, (2590+img1.height+img2.height+img3.height)), f"紫外线指数: {static['紫外线指数']}     总降水: {static['总降水_mm']}mm", fill=(0, 0, 0), font=font3)

        # AI((static, dynamic))
        # print(static, dynamic)
        draw.text((100, (2740 + img1.height + img2.height + img3.height)), "温馨提示:\n\n"+AI((static, dynamic)), fill=(0, 0, 0), font=font3)

        font4 = ImageFont.truetype(FONT_PATH, 30)
        # 时间戳
        draw.text((1800, (3200 + img1.height + img2.height + img3.height)), "数据来源: wttr.in", fill=(0, 0, 0), font=font4)
        # 时间
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        draw.text((1800, (3260 + img1.height + img2.height + img3.height)), f"生成时间: {current_time}", fill=(0, 0, 0), font=font4)
        img_bg7.save("output.png")