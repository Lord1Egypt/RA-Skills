#!/usr/bin/env python3
"""滑雪场查询 - 全球滑雪场查询与推荐"""

import json

# 滑雪场数据
SKI_RESORTS = {
    "niseko": {
        "name": "二世谷（新雪谷）",
        "country": "日本",
        "region": "北海道",
        "elevation": "260-1150m",
        "vertical_drop": 890,
        "runs": {"beginner": 0.3, "intermediate": 0.4, "advanced": 0.3},
        "total_runs": 30,
        "longest_run": "5.6km",
        "lifts": 14,
        "snow_quality": "粉雪",
        "avg_snow_depth": "3-5m",
        "season": "11月下旬-5月上旬",
        "peak_season": "12月-2月",
        "day_pass": 8500,
        "currency": "JPY",
        "day_pass_cny": 400,
        "night_ski": True,
        "rental_available": True,
        "highlights": ["全球最佳粉雪", "夜场滑雪", "温泉", "日式美食"],
        "nearby_airport": "新千岁机场(CTS)",
        "transfer_time": "2.5小时"
    },
    "hakuba": {
        "name": "白马",
        "country": "日本",
        "region": "长野",
        "elevation": "760-1670m",
        "vertical_drop": 910,
        "runs": {"beginner": 0.3, "intermediate": 0.45, "advanced": 0.25},
        "total_runs": 50,
        "longest_run": "8km",
        "lifts": 24,
        "snow_quality": "粉雪",
        "avg_snow_depth": "2-4m",
        "season": "12月上旬-4月下旬",
        "peak_season": "1月-2月",
        "day_pass": 6500,
        "currency": "JPY",
        "day_pass_cny": 300,
        "night_ski": True,
        "rental_available": True,
        "highlights": ["1998冬奥场地", "10个滑雪区", "温泉村", "英文友好"],
        "nearby_airport": "东京成田/羽田(NRT/HND)",
        "transfer_time": "3小时"
    },
    "rut": {
        "name": "留寿都",
        "country": "日本",
        "region": "北海道",
        "elevation": "330-994m",
        "vertical_drop": 664,
        "runs": {"beginner": 0.35, "intermediate": 0.4, "advanced": 0.25},
        "total_runs": 37,
        "longest_run": "3.5km",
        "lifts": 12,
        "snow_quality": "粉雪",
        "avg_snow_depth": "2.5-4m",
        "season": "11月下旬-4月上旬",
        "peak_season": "12月-2月",
        "day_pass": 7000,
        "currency": "JPY",
        "day_pass_cny": 330,
        "night_ski": True,
        "rental_available": True,
        "highlights": ["三座山峰", "树滑天堂", "人少雪好", "性价比高"],
        "nearby_airport": "新千岁机场(CTS)",
        "transfer_time": "2小时"
    },
    "chamonix": {
        "name": "霞慕尼",
        "country": "法国",
        "region": "阿尔卑斯",
        "elevation": "1035-3842m",
        "vertical_drop": 2807,
        "runs": {"beginner": 0.2, "intermediate": 0.35, "advanced": 0.45},
        "total_runs": 110,
        "longest_run": "22km",
        "lifts": 47,
        "snow_quality": "高山雪",
        "avg_snow_depth": "2-5m",
        "season": "12月中旬-5月上旬",
        "peak_season": "1月-3月",
        "day_pass": 63,
        "currency": "EUR",
        "day_pass_cny": 490,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["勃朗峰脚下", "欧洲最高落差", "野雪天堂", "越野滑雪"],
        "nearby_airport": "日内瓦(GVA)",
        "transfer_time": "1小时"
    },
    "zermatt": {
        "name": "采尔马特",
        "country": "瑞士",
        "region": "阿尔卑斯",
        "elevation": "1620-3899m",
        "vertical_drop": 2279,
        "runs": {"beginner": 0.2, "intermediate": 0.4, "advanced": 0.4},
        "total_runs": 200,
        "longest_run": "25km",
        "lifts": 52,
        "snow_quality": "高山雪",
        "avg_snow_depth": "2-6m",
        "season": "全年(冰川区域)",
        "peak_season": "12月-4月",
        "day_pass": 89,
        "currency": "CHF",
        "day_pass_cny": 720,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["马特洪峰", "全年可滑", "瑞士巧克力", "无车小镇"],
        "nearby_airport": "日内瓦(GVA)/苏黎世(ZRH)",
        "transfer_time": "3.5小时"
    },
    "val_thorens": {
        "name": "瓦托伦斯",
        "country": "法国",
        "region": "三峡谷",
        "elevation": "1800-3230m",
        "vertical_drop": 1430,
        "runs": {"beginner": 0.2, "intermediate": 0.45, "advanced": 0.35},
        "total_runs": 600,
        "longest_run": "12km",
        "lifts": 173,
        "snow_quality": "高山雪",
        "avg_snow_depth": "2-5m",
        "season": "11月下旬-5月上旬",
        "peak_season": "1月-3月",
        "day_pass": 62,
        "currency": "EUR",
        "day_pass_cny": 480,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["全球最大滑雪区", "三峡谷通票", "高海拔保雪", "欧洲最大雪场"],
        "nearby_airport": "里昂(LYS)/日内瓦(GVA)",
        "transfer_time": "3小时"
    },
    "whistler": {
        "name": "惠斯勒黑梳",
        "country": "加拿大",
        "region": "不列颠哥伦比亚",
        "elevation": "675-2284m",
        "vertical_drop": 1609,
        "runs": {"beginner": 0.2, "intermediate": 0.4, "advanced": 0.4},
        "total_runs": 200,
        "longest_run": "11km",
        "lifts": 37,
        "snow_quality": "粉雪",
        "avg_snow_depth": "3-6m",
        "season": "11月中旬-5月下旬",
        "peak_season": "12月-3月",
        "day_pass": 159,
        "currency": "CAD",
        "day_pass_cny": 830,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["2010冬奥场地", "北美最大", "两山连通", "直升机滑雪"],
        "nearby_airport": "温哥华(YVR)",
        "transfer_time": "2小时"
    },
    "aspen": {
        "name": "阿斯彭",
        "country": "美国",
        "region": "科罗拉多",
        "elevation": "2426-3850m",
        "vertical_drop": 1424,
        "runs": {"beginner": 0.15, "intermediate": 0.35, "advanced": 0.5},
        "total_runs": 300,
        "longest_run": "5.3km",
        "lifts": 36,
        "snow_quality": "干粉",
        "avg_snow_depth": "2-5m",
        "season": "11月-4月",
        "peak_season": "12月-3月",
        "day_pass": 199,
        "currency": "USD",
        "day_pass_cny": 1440,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["四山通票", "名流聚集", "X Games", "高端度假"],
        "nearby_airport": "阿斯彭/皮特金(ASE)",
        "transfer_time": "15分钟"
    },
    "park_city": {
        "name": "帕克城",
        "country": "美国",
        "region": "犹他",
        "elevation": "2103-3048m",
        "vertical_drop": 945,
        "runs": {"beginner": 0.25, "intermediate": 0.4, "advanced": 0.35},
        "total_runs": 300,
        "longest_run": "5.7km",
        "lifts": 41,
        "snow_quality": "干粉",
        "avg_snow_depth": "2-4m",
        "season": "11月-4月",
        "peak_season": "12月-3月",
        "day_pass": 165,
        "currency": "USD",
        "day_pass_cny": 1195,
        "night_ski": True,
        "rental_available": True,
        "highlights": ["2002冬奥场地", "圣丹斯电影节", "美国最大超雪场", "盐湖城近"],
        "nearby_airport": "盐湖城(SLC)",
        "transfer_time": "45分钟"
    },
    "st_anton": {
        "name": "圣安东",
        "country": "奥地利",
        "region": "阿尔贝格",
        "elevation": "1300-2811m",
        "vertical_drop": 1511,
        "runs": {"beginner": 0.15, "intermediate": 0.4, "advanced": 0.45},
        "total_runs": 300,
        "longest_run": "10km",
        "lifts": 88,
        "snow_quality": "高山雪",
        "avg_snow_depth": "2-5m",
        "season": "12月上旬-4月下旬",
        "peak_season": "1月-3月",
        "day_pass": 57,
        "currency": "EUR",
        "day_pass_cny": 440,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["阿尔贝格滑雪区", "越野滑雪圣地", " après-ski", "奥式温泉"],
        "nearby_airport": "因斯布鲁克(INN)/苏黎世(ZRH)",
        "transfer_time": "1.5小时"
    },
    "cortina": {
        "name": "科尔蒂纳",
        "country": "意大利",
        "region": "多洛米蒂",
        "elevation": "1224-3260m",
        "vertical_drop": 1710,
        "runs": {"beginner": 0.25, "intermediate": 0.4, "advanced": 0.35},
        "total_runs": 120,
        "longest_run": "9km",
        "lifts": 52,
        "snow_quality": "高山雪",
        "avg_snow_depth": "2-4m",
        "season": "12月上旬-4月中旬",
        "peak_season": "1月-3月",
        "day_pass": 55,
        "currency": "EUR",
        "day_pass_cny": 430,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["2026冬奥场地", "多洛米蒂 UNESCO", "意大利美食", "时尚小镇"],
        "nearby_airport": "威尼斯(VCE)",
        "transfer_time": "2小时"
    },
    "yabuli": {
        "name": "亚布力",
        "country": "中国",
        "region": "黑龙江",
        "elevation": "400-1374m",
        "vertical_drop": 974,
        "runs": {"beginner": 0.3, "intermediate": 0.4, "advanced": 0.3},
        "total_runs": 50,
        "longest_run": "5km",
        "lifts": 18,
        "snow_quality": "干雪",
        "avg_snow_depth": "1-2m",
        "season": "11月中旬-3月下旬",
        "peak_season": "12月-2月",
        "day_pass": 380,
        "currency": "CNY",
        "day_pass_cny": 380,
        "night_ski": True,
        "rental_available": True,
        "highlights": ["中国最大雪场", "6届冬运举办地", "高铁直达", "性价比高"],
        "nearby_airport": "哈尔滨太平(HRB)",
        "transfer_time": "3小时(高铁1.5小时到亚布力站)"
    },
    "changbaishan": {
        "name": "长白山万达",
        "country": "中国",
        "region": "吉林",
        "elevation": "700-1340m",
        "vertical_drop": 640,
        "runs": {"beginner": 0.35, "intermediate": 0.4, "advanced": 0.25},
        "total_runs": 43,
        "longest_run": "4km",
        "lifts": 10,
        "snow_quality": "粉雪",
        "avg_snow_depth": "1-2m",
        "season": "11月中旬-4月上旬",
        "peak_season": "12月-2月",
        "day_pass": 450,
        "currency": "CNY",
        "day_pass_cny": 450,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["度假村一体化", "温泉", "雪地摩托", "适合家庭"],
        "nearby_airport": "长白山机场(NBS)",
        "transfer_time": "30分钟"
    },
    "songhua_lake": {
        "name": "松花湖",
        "country": "中国",
        "region": "吉林",
        "elevation": "500-935m",
        "vertical_drop": 435,
        "runs": {"beginner": 0.4, "intermediate": 0.4, "advanced": 0.2},
        "total_runs": 34,
        "longest_run": "4.8km",
        "lifts": 6,
        "snow_quality": "粉雪",
        "avg_snow_depth": "0.8-1.5m",
        "season": "11月下旬-3月中旬",
        "peak_season": "12月-2月",
        "day_pass": 380,
        "currency": "CNY",
        "day_pass_cny": 380,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["万科运营", "新手友好", "吉林市近", "北大壶隔壁"],
        "nearby_airport": "长春龙嘉(CGQ)",
        "transfer_time": "1.5小时"
    },
    "beidahu": {
        "name": "北大湖",
        "country": "中国",
        "region": "吉林",
        "elevation": "530-1400m",
        "vertical_drop": 870,
        "runs": {"beginner": 0.25, "intermediate": 0.4, "advanced": 0.35},
        "total_runs": 64,
        "longest_run": "5.3km",
        "lifts": 12,
        "snow_quality": "粉雪",
        "avg_snow_depth": "1-2m",
        "season": "11月中旬-3月下旬",
        "peak_season": "12月-2月",
        "day_pass": 450,
        "currency": "CNY",
        "day_pass_cny": 450,
        "night_ski": False,
        "rental_available": True,
        "highlights": ["落差最大", "专业雪道多", "国家队训练地", "松花湖邻居"],
        "nearby_airport": "长春龙嘉(CGQ)",
        "transfer_time": "1.5小时"
    }
}


def search(country: str = "", level: str = "", budget: str = "") -> str:
    """搜索滑雪场，支持按国家/难度/预算筛选"""
    results = []
    for key, resort in SKI_RESORTS.items():
        if country and country.lower() not in resort["country"].lower():
            continue
        if level:
            level_map = {"初级": "beginner", "中级": "intermediate", "高级": "advanced",
                        "新手": "beginner", "进阶": "intermediate", "expert": "advanced"}
            target = level_map.get(level, level)
            if target in resort["runs"] and resort["runs"][target] < 0.3:
                continue
        if budget:
            budget_map = {"便宜": 500, "中等": 800, "高端": 99999}
            max_cny = budget_map.get(budget, None)
            if max_cny and resort["day_pass_cny"] > max_cny:
                continue

        level_desc = []
        for lvl, pct in resort["runs"].items():
            lvl_cn = {"beginner": "初级", "intermediate": "中级", "advanced": "高级"}[lvl]
            level_desc.append(f"{lvl_cn}{int(pct*100)}%")

        results.append({
            "name": resort["name"],
            "country": resort["country"],
            "region": resort["region"],
            "vertical_drop": resort["vertical_drop"],
            "total_runs": resort["total_runs"],
            "levels": " ".join(level_desc),
            "snow": resort["snow_quality"],
            "season": resort["season"],
            "day_pass_cny": resort["day_pass_cny"],
            "highlights": resort["highlights"],
            "night_ski": resort["night_ski"],
            "nearby_airport": resort["nearby_airport"]
        })

    if not results:
        return f"未找到匹配的滑雪场。支持国家：日本、法国、瑞士、加拿大、美国、奥地利、意大利、中国"

    results.sort(key=lambda x: x["day_pass_cny"])

    output = f"🎿 滑雪场搜索结果（{len(results)}个）\n\n"
    for r in results:
        night = "🌙夜场" if r["night_ski"] else ""
        output += f"**{r['name']}**（{r['country']}·{r['region']}）{night}\n"
        output += f"  ⛷ 雪道：{r['total_runs']}条 落差：{r['vertical_drop']}m | {r['levels']}\n"
        output += f"  ❄️ 雪质：{r['snow']}  📅 雪季：{r['season']}\n"
        output += f"  💰 日票：{r['day_pass_cny']}元/天  ✈️ 最近：{r['nearby_airport']}\n"
        output += f"  ✨ {'、'.join(r['highlights'])}\n\n"
    return output


def detail(resort_name: str = "") -> str:
    """查看滑雪场详情"""
    if not resort_name:
        return "请输入滑雪场名称，如：二世谷、霞慕尼、亚布力"

    matched = None
    for key, resort in SKI_RESORTS.items():
        if resort_name.lower() in resort["name"].lower() or resort_name.lower() == key:
            matched = resort
            break

    if not matched:
        return f"未找到滑雪场'{resort_name}'。支持：{', '.join(r['name'] for r in SKI_RESORTS.values())}"

    level_desc = []
    for lvl, pct in matched["runs"].items():
        lvl_cn = {"beginner": "初级", "intermediate": "中级", "advanced": "高级"}[lvl]
        level_desc.append(f"{lvl_cn}{int(pct*100)}%")

    output = f"🎿 **{matched['name']}**（{matched['country']}·{matched['region']}）\n\n"
    output += f"**海拔**：{matched['elevation']}\n"
    output += f"**落差**：{matched['vertical_drop']}m\n"
    output += f"**雪道**：{matched['total_runs']}条（{' '.join(level_desc)}）\n"
    output += f"**最长雪道**：{matched['longest_run']}\n"
    output += f"**缆车**：{matched['lifts']}条\n"
    output += f"**雪质**：{matched['snow_quality']}，平均雪深{matched['avg_snow_depth']}\n"
    output += f"**雪季**：{matched['season']}（旺季{matched['peak_season']}）\n"
    output += f"**日票**：{matched['day_pass']} {matched['currency']}（约{matched['day_pass_cny']}元）\n"
    output += f"**夜场**：{'有' if matched['night_ski'] else '无'}  **装备租赁**：{'有' if matched['rental_available'] else '无'}\n"
    output += f"**最近机场**：{matched['nearby_airport']}（{matched['transfer_time']}）\n"
    output += f"**亮点**：{'、'.join(matched['highlights'])}\n"
    return output


def compare(resorts: str = "") -> str:
    """对比多个滑雪场"""
    if not resorts:
        return "请输入滑雪场名称，逗号分隔，如：二世谷,白马,亚布力"

    names = [n.strip() for n in resorts.split(",")]
    matched = []
    for name in names:
        for key, resort in SKI_RESORTS.items():
            if name.lower() in resort["name"].lower() or name.lower() == key:
                matched.append(resort)
                break

    if not matched:
        return f"未找到匹配的滑雪场。支持：{', '.join(r['name'] for r in SKI_RESORTS.values())}"

    output = f"🎿 滑雪场对比（{len(matched)}个）\n\n"
    output += f"{'项目':<8}"
    for m in matched:
        output += f"| {m['name']:<12}"
    output += "\n" + "-" * (10 + 15 * len(matched)) + "\n"

    for field, label in [("country", "国家"), ("vertical_drop", "落差m"), ("total_runs", "雪道数"),
                          ("snow_quality", "雪质"), ("day_pass_cny", "日票¥"), ("night_ski", "夜场"),
                          ("season", "雪季")]:
        output += f"{label:<8}"
        for m in matched:
            val = m.get(field, "")
            if field == "night_ski":
                val = "✅" if val else "❌"
            output += f"| {str(val):<12}"
        output += "\n"

    return output


TOOLS = {
    "search": search,
    "detail": detail,
    "compare": compare
}

if __name__ == "__main__":
    import sys
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "search"
    tool_args = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            tool_args[k] = v
    func = TOOLS.get(tool_name)
    if func:
        print(func(**tool_args))
    else:
        print(f"未知工具: {tool_name}, 可用: {list(TOOLS.keys())}")
