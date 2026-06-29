#!/usr/bin/env python3
"""智能行李清单 - 根据目的地天气+行程天数+出行类型，自动生成打包清单"""

import sys
import json
import urllib.request
import urllib.parse

# 高德代理（免费，无需用户Key）
GAODE_PROXY = "https://gaode-proxy-jerspxcked.cn-hangzhou.fcapp.run"

# ==================== 天气查询 ====================

def gaode_call(api, params):
    """调用高德代理API"""
    data = json.dumps({"api": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(GAODE_PROXY, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_adcode(city_name):
    """城市名→adcode"""
    data = gaode_call("geocode/geo", {"address": city_name})
    geocodes = data.get("geocodes", [])
    if geocodes:
        return geocodes[0].get("adcode", "")
    return ""


def get_weather(city_name):
    """获取目的地实况+4天预报"""
    adcode = get_adcode(city_name)
    if not adcode:
        return None

    # 实况
    live_data = gaode_call("weather/weatherInfo", {"city": adcode})
    lives = live_data.get("lives", [])

    # 预报
    forecast_data = gaode_call("weather/weatherInfo", {"city": adcode, "extensions": "all"})
    forecasts = forecast_data.get("forecasts", [])

    result = {"city": city_name, "adcode": adcode}
    if lives:
        result["live"] = lives[0]
    if forecasts:
        result["forecast"] = forecasts[0].get("casts", [])

    return result


# ==================== 行李清单引擎 ====================

# 基础清单：所有人都要带的
BASE_LIST = {
    "证件与贵重物品": [
        {"item": "身份证", "essential": True},
        {"item": "手机及充电器", "essential": True},
        {"item": "充电宝", "essential": True},
        {"item": "钱包/现金/银行卡", "essential": True},
    ],
    "个人护理": [
        {"item": "牙刷/牙膏", "essential": True},
        {"item": "洗面奶", "essential": False},
        {"item": "护肤品/防晒霜", "essential": False},
        {"item": "毛巾", "essential": False},
        {"item": "纸巾/湿巾", "essential": True},
    ],
    "日常用品": [
        {"item": "伞", "essential": False},
        {"item": "水杯", "essential": False},
        {"item": "零食", "essential": False},
        {"item": "塑料袋（装脏衣/湿物）", "essential": False},
    ],
}

# 按出行类型的额外清单
TRIP_TYPE_EXTRAS = {
    "商务": {
        "商务装备": [
            {"item": "笔记本电脑及充电器", "essential": True},
            {"item": "商务正装1-2套", "essential": True},
            {"item": "皮鞋", "essential": True},
            {"item": "名片", "essential": False},
            {"item": "笔和笔记本", "essential": False},
        ]
    },
    "度假": {
        "度假装备": [
            {"item": "泳衣/泳裤", "essential": False},
            {"item": "沙滩巾", "essential": False},
            {"item": "墨镜", "essential": True},
            {"item": "遮阳帽/防晒帽", "essential": True},
            {"item": "相机", "essential": False},
        ]
    },
    "户外/徒步": {
        "户外装备": [
            {"item": "登山鞋", "essential": True},
            {"item": "速干衣裤", "essential": True},
            {"item": "冲锋衣", "essential": True},
            {"item": "登山杖", "essential": False},
            {"item": "头灯/手电筒", "essential": True},
            {"item": "急救包", "essential": True},
            {"item": "防蚊喷雾", "essential": False},
        ]
    },
    "探亲": {
        "探亲物品": [
            {"item": "礼品/特产", "essential": False},
            {"item": "给长辈的保健品", "essential": False},
            {"item": "家庭常用药", "essential": False},
        ]
    },
    "亲子": {
        "亲子装备": [
            {"item": "儿童换洗衣物", "essential": True},
            {"item": "儿童洗护用品", "essential": True},
            {"item": "儿童零食/水壶", "essential": True},
            {"item": "玩具/绘本", "essential": False},
            {"item": "婴儿推车", "essential": False},
            {"item": "纸尿裤", "essential": False},
            {"item": "儿童常用药", "essential": True},
        ]
    },
}

# 天气相关追加
def weather_extras(weather_info):
    """根据天气返回额外物品"""
    extras = {}
    if not weather_info:
        return extras

    # 解析天气数据
    live = weather_info.get("live", {})
    forecast = weather_info.get("forecast", [])

    # 当前温度
    temp = int(live.get("temperature", "20"))
    weather_text = live.get("weather", "晴")
    humidity = int(live.get("humidity", "50"))

    # 预报温度范围
    temps = []
    rain_days = 0
    for day in forecast:
        try:
            temps.append(int(day.get("daytemp", "20")))
            temps.append(int(day.get("nighttemp", "10")))
            dw = day.get("dayweather", "")
            nw = day.get("nightweather", "")
            if any(k in dw + nw for k in ["雨", "雷", "阵雨"]):
                rain_days += 1
        except (ValueError, TypeError):
            pass

    max_temp = max(temps) if temps else temp
    min_temp = min(temps) if temps else temp

    # 高温(>30°C)
    if max_temp >= 30:
        extras.setdefault("防暑防晒", []).extend([
            {"item": "防晒霜SPF50+", "essential": True},
            {"item": "遮阳帽/防晒帽", "essential": True},
            {"item": "墨镜", "essential": True},
            {"item": "轻薄透气衣物", "essential": True},
            {"item": "清凉油/风油精", "essential": False},
        ])

    # 低温(<10°C)
    if min_temp <= 10:
        extras.setdefault("保暖装备", []).extend([
            {"item": "羽绒服/厚外套", "essential": True},
            {"item": "保暖内衣", "essential": True},
            {"item": "围巾/手套", "essential": min_temp <= 0},
            {"item": "暖宝宝", "essential": min_temp <= 0},
            {"item": "保湿霜/润唇膏", "essential": True},
        ])

    # 零下(<0°C)
    if min_temp <= 0:
        extras.setdefault("极寒装备", []).extend([
            {"item": "雪地靴", "essential": True},
            {"item": "帽子(保暖)", "essential": True},
            {"item": "保温杯", "essential": True},
        ])

    # 雨天
    if rain_days > 0:
        extras.setdefault("防雨装备", []).extend([
            {"item": "雨伞", "essential": True},
            {"item": "防水鞋/鞋套", "essential": rain_days >= 2},
            {"item": "防水袋(保护电子设备)", "essential": False},
        ])
        if rain_days >= 3:
            extras["防雨装备"].append({"item": "轻便雨衣", "essential": True})

    # 高湿度(>70%)
    if humidity > 70 or any(k in weather_text for k in ["潮湿", "闷"]):
        extras.setdefault("防潮用品", []).extend([
            {"item": "速干毛巾", "essential": False},
            {"item": "除湿袋(行李箱用)", "essential": False},
        ])

    # 温差大(日温差>12°C)
    if max_temp - min_temp > 12:
        extras.setdefault("温差应对", []).extend([
            {"item": "薄外套/开衫(早晚穿)", "essential": True},
            {"item": "洋葱式穿搭衣物", "essential": True},
        ])

    return extras


# 天数相关衣物计算
def clothing_for_days(days, weather_info):
    """根据天数和天气计算衣物量"""
    items = []

    forecast = weather_info.get("forecast", []) if weather_info else []
    live = weather_info.get("live", {}) if weather_info else {}
    temp = int(live.get("temperature", "20")) if live else 20

    # 温度区间判断穿衣类型
    if temp >= 28:
        clothing_type = "夏装(短袖/短裤/裙装)"
    elif temp >= 20:
        clothing_type = "春秋装(长袖/薄外套)"
    elif temp >= 10:
        clothing_type = "秋装(卫衣/夹克)"
    else:
        clothing_type = "冬装(毛衣/厚外套)"

    # 内衣裤 = 天数 + 1
    underwear = min(days + 1, 7)
    items.append({"item": f"内衣裤×{underwear}", "essential": True})

    # 袜子 = 天数
    socks = min(days, 7)
    items.append({"item": f"袜子×{socks}", "essential": True})

    # 外套/上衣
    if days <= 2:
        tops = 2
    elif days <= 5:
        tops = 3
    else:
        tops = min(days // 2 + 1, 5)
    items.append({"item": f"{clothing_type}×{tops}", "essential": True})

    # 裤子
    if days <= 2:
        pants = 1
    elif days <= 5:
        pants = 2
    else:
        pants = min(days // 3 + 1, 4)
    items.append({"item": f"裤子/裙装×{pants}", "essential": True})

    # 鞋子
    items.append({"item": "运动鞋/休闲鞋", "essential": True})
    if days >= 4:
        items.append({"item": "拖鞋(酒店/休闲)", "essential": False})

    # 长途旅行加洗衣相关
    if days >= 5:
        items.append({"item": "旅行洗衣液/洗衣袋", "essential": False})

    return items


# 特殊目的地追加
DESTINATION_EXTRAS = {
    "海滩/海岛": {
        "海滩装备": [
            {"item": "泳衣/泳裤", "essential": True},
            {"item": "沙滩巾", "essential": True},
            {"item": "防水手机袋", "essential": True},
            {"item": "浮潜面镜(如需)", "essential": False},
            {"item": "沙滩鞋/人字拖", "essential": True},
        ]
    },
    "高原/山区": {
        "高原装备": [
            {"item": "高倍防晒霜", "essential": True},
            {"item": "红景天/高原药", "essential": True},
            {"item": "保温水壶", "essential": True},
            {"item": "防风外套", "essential": True},
            {"item": "唇膏(防干裂)", "essential": True},
        ]
    },
    "雪地/冰雪": {
        "冰雪装备": [
            {"item": "雪地靴", "essential": True},
            {"item": "暖宝宝", "essential": True},
            {"item": "防滑鞋套", "essential": True},
            {"item": "护目镜(雪地反光)", "essential": False},
            {"item": "防水手套", "essential": True},
        ]
    },
    "温泉": {
        "温泉装备": [
            {"item": "泳衣(温泉专用)", "essential": True},
            {"item": "浴巾(部分温泉不提供)", "essential": False},
            {"item": "防水袋", "essential": False},
        ]
    },
    "国际/出境": {
        "出境必备": [
            {"item": "护照", "essential": True},
            {"item": "签证(如需)", "essential": True},
            {"item": "转换插头", "essential": True},
            {"item": "外币/国际信用卡", "essential": True},
            {"item": "行程单/酒店预订单(英文)", "essential": True},
            {"item": "旅行保险", "essential": True},
        ]
    },
}


# ==================== 命令实现 ====================

def cmd_generate(params):
    """生成行李清单"""
    destination = params.get("destination", "")
    days = int(params.get("days", 3))
    trip_type = params.get("trip_type", "度假")  # 商务/度假/户外/探亲/亲子
    scene = params.get("scene", "")  # 海滩/高原/雪地/温泉/国际
    travelers = params.get("travelers", "1成人")  # 1成人/情侣/家庭(含儿童)/团队

    if not destination:
        return {"error": "请提供目的地城市名称"}

    # 1. 获取天气
    weather_info = get_weather(destination)
    if not weather_info:
        return {"error": f"无法获取{destination}的天气信息，请确认城市名称"}

    # 2. 组装清单
    checklist = {}

    # 基础清单
    for cat, items in BASE_LIST.items():
        checklist[cat] = items[:]

    # 天气追加
    w_extras = weather_extras(weather_info)
    for cat, items in w_extras.items():
        if cat in checklist:
            checklist[cat].extend(items)
        else:
            checklist[cat] = items

    # 天数→衣物量
    clothing = clothing_for_days(days, weather_info)
    checklist["衣物"] = clothing

    # 出行类型追加
    type_key = trip_type.split("/")[0] if "/" in trip_type else trip_type
    if type_key in TRIP_TYPE_EXTRAS:
        for cat, items in TRIP_TYPE_EXTRAS[type_key].items():
            if cat in checklist:
                checklist[cat].extend(items)
            else:
                checklist[cat] = items

    # 目的地场景追加
    if scene:
        for key in scene.split("/"):
            if key in DESTINATION_EXTRAS:
                for cat, items in DESTINATION_EXTRAS[key].items():
                    if cat in checklist:
                        checklist[cat].extend(items)
                    else:
                        checklist[cat] = items

    # 旅行者类型追加
    if "儿童" in travelers or "亲子" in travelers or "家庭" in travelers:
        for cat, items in TRIP_TYPE_EXTRAS.get("亲子", {}).items():
            if cat in checklist:
                seen = {i["item"] for i in checklist[cat]}
                for it in items:
                    if it["item"] not in seen:
                        checklist[cat].append(it)
                        seen.add(it["item"])
            else:
                checklist[cat] = items[:]

    # 3. 天气摘要
    live = weather_info.get("live", {})
    forecast = weather_info.get("forecast", [])

    weather_summary = {
        "destination": destination,
        "current": f"{live.get('weather', '未知')} {live.get('temperature', '?')}°C 湿度{live.get('humidity', '?')}%",
    }
    if forecast:
        day_strs = []
        for d in forecast[:min(days, 4)]:
            day_strs.append(f"{d.get('date', '')} {d.get('dayweather', '')} {d.get('daytemp', '?')}/{d.get('nighttemp', '?')}°C")
        weather_summary["forecast"] = day_strs

    # 4. 去重（跨分类去重，保留essential=true的版本）
    final_checklist = {}
    global_seen = {}  # item_name -> (category, essential)
    for cat, items in checklist.items():
        unique = []
        for it in items:
            name = it["item"]
            if name not in global_seen:
                global_seen[name] = (cat, it.get("essential", False))
                unique.append(it)
            else:
                # 已存在：如果新的是essential而旧的不是，升级到essential
                old_cat, old_essential = global_seen[name]
                if it.get("essential", False) and not old_essential:
                    # 找到旧的那条升级为essential
                    for old_it in final_checklist.get(old_cat, []):
                        if old_it["item"] == name:
                            old_it["essential"] = True
                            break
                    global_seen[name] = (old_cat, True)
        if unique:
            final_checklist[cat] = unique

    # 移除空分类
    final_checklist = {k: v for k, v in final_checklist.items() if v}

    # 5. 统计
    total = sum(len(v) for v in final_checklist.values())
    essential = sum(1 for v in final_checklist.values() for it in v if it.get("essential"))

    return {
        "weather": weather_summary,
        "trip_info": {"destination": destination, "days": days, "trip_type": trip_type, "scene": scene, "travelers": travelers},
        "checklist": final_checklist,
        "stats": {"total_items": total, "essential_items": essential, "optional_items": total - essential},
        "tips": _generate_tips(weather_info, trip_type, scene, days),
    }


def _generate_tips(weather_info, trip_type, scene, days):
    """生成出行小贴士"""
    tips = []

    live = weather_info.get("live", {}) if weather_info else {}
    forecast = weather_info.get("forecast", []) if weather_info else []
    temp = int(live.get("temperature", "20")) if live else 20

    # 温度贴士
    if temp >= 35:
        tips.append("🔥 高温预警！注意防暑降温，多喝水，避免正午户外活动")
    elif temp <= 0:
        tips.append("❄️ 严寒天气！注意保暖防冻，手机等电子设备低温易关机")
    elif temp >= 30:
        tips.append("☀️ 天气炎热，建议穿浅色透气衣物，随身带水")

    # 雨天贴士
    rain_days = sum(1 for d in forecast if any(k in d.get("dayweather", "") + d.get("nightweather", "") for k in ["雨", "雷"]))
    if rain_days >= 2:
        tips.append(f"🌧️ 未来{rain_days}天有雨，务必带好雨具，考虑防水鞋")

    # 出行类型贴士
    if "户外" in trip_type or "徒步" in trip_type:
        tips.append("🥾 户外活动建议穿防滑鞋，提前下载离线地图")
    if "国际" in scene or "出境" in scene:
        tips.append("✈️ 出境请提前确认护照有效期>6个月，备份证件电子版")
    if "亲子" in trip_type:
        tips.append("👶 带娃出行建议多备一套换洗衣物在随身包，以备不时之需")

    # 天数贴士
    if days >= 7:
        tips.append("🧳 长途旅行建议带旅行装洗护用品，节省空间")

    if not tips:
        tips.append("✅ 天气不错，轻装出行即可")

    return tips


def cmd_check(params):
    """检查已打包/未打包"""
    checklist = params.get("checklist", {})
    packed = params.get("packed", [])  # 已打包物品列表

    if not checklist:
        return {"error": "请提供清单数据(checklist)"}

    packed_set = set(packed)
    result = {"packed": [], "not_packed": [], "progress": 0}

    for cat, items in checklist.items():
        for it in items:
            name = it["item"] if isinstance(it, dict) else it
            essential = it.get("essential", False) if isinstance(it, dict) else False
            entry = {"item": name, "category": cat, "essential": essential}
            if name in packed_set:
                result["packed"].append(entry)
            else:
                result["not_packed"].append(entry)

    total = len(result["packed"]) + len(result["not_packed"])
    result["progress"] = round(len(result["packed"]) / total * 100, 1) if total > 0 else 0

    # 遗漏必带品提醒
    missed_essential = [i for i in result["not_packed"] if i["essential"]]
    if missed_essential:
        result["alert"] = f"⚠️ 还有{len(missed_essential)}件必带品未打包：" + "、".join(i["item"] for i in missed_essential[:5])

    return result


def cmd_quick(params):
    """快速清单（不查天气，纯逻辑生成）"""
    days = int(params.get("days", 3))
    trip_type = params.get("trip_type", "度假")
    scene = params.get("scene", "")

    # 简化版：不查天气
    checklist = {}
    for cat, items in BASE_LIST.items():
        checklist[cat] = items[:]

    # 衣物（默认温带春秋）
    checklist["衣物"] = clothing_for_days(days, {"live": {"temperature": "20"}, "forecast": []})

    # 出行类型
    type_key = trip_type.split("/")[0] if "/" in trip_type else trip_type
    if type_key in TRIP_TYPE_EXTRAS:
        for cat, items in TRIP_TYPE_EXTRAS[type_key].items():
            checklist[cat] = items[:]

    # 场景
    if scene:
        for key in scene.split("/"):
            if key in DESTINATION_EXTRAS:
                for cat, items in DESTINATION_EXTRAS[key].items():
                    checklist[cat] = items[:]

    total = sum(len(v) for v in checklist.values())
    essential = sum(1 for v in checklist.values() for it in v if it.get("essential"))

    return {
        "trip_info": {"days": days, "trip_type": trip_type, "scene": scene},
        "checklist": checklist,
        "stats": {"total_items": total, "essential_items": essential, "optional_items": total - essential},
        "note": "快速模式未查询实时天气，建议使用generate命令获取天气适配清单",
    }


# ==================== 主入口 ====================

COMMANDS = {
    "generate": cmd_generate,
    "check": cmd_check,
    "quick": cmd_quick,
}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "用法: python3 packing.py <command> '<json_params>'",
            "commands": {
                "generate": "生成天气适配清单 (destination, days, trip_type, scene, travelers)",
                "check": "检查打包进度 (checklist, packed)",
                "quick": "快速清单不查天气 (days, trip_type, scene)",
            }
        }, ensure_ascii=False))
        sys.exit(1)

    command = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if command not in COMMANDS:
        print(json.dumps({"error": f"未知命令: {command}，可用: {list(COMMANDS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = COMMANDS[command](params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"执行失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
