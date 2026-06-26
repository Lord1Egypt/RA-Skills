#!/usr/bin/env python3
"""
store-hopper: 天气查询脚本（增强版）
用法: python3 weather.py <城市名> [--days N] [--codes-file data/city-codes.md] [--city-code CODE]
功能:
  1. 内置常用城市代码字典，覆盖主要城市和热门旅游目的地
  2. 支持从 city-codes.md 文件加载扩展代码
  3. 如果城市代码未找到，自动从中国气象局网站搜索
  4. 搜索到的新代码自动追加到 city-codes.md，下次直接使用
  5. CMA 不可用时自动降级到 wttr.in
输出: JSON 格式的天气预报数据
"""

import argparse
import json
import os
import re
import sys
import requests
from urllib.parse import quote


def summary(msg: str):
    """输出一行关键摘要到 stderr"""
    sys.stderr.write(f"[天气] {msg}\n")
    sys.stderr.flush()


# ───────────────── 内置城市代码字典 ─────────────────
# 覆盖中国主要城市及热门旅游城市，省去外部查询
BUILTIN_CITY_CODES = {
    # 直辖市
    "北京": "54511", "上海": "58362", "天津": "54527", "重庆": "57516",
    # 省会 & 一线城市
    "广州": "59287", "深圳": "59493", "杭州": "58457", "成都": "56294",
    "武汉": "57494", "南京": "58238", "西安": "57036", "长沙": "57679",
    "郑州": "57083", "济南": "54823", "合肥": "58321", "福州": "58847",
    "昆明": "56778", "贵阳": "57816", "南宁": "59431", "海口": "59758",
    "太原": "53772", "石家庄": "53698", "哈尔滨": "50953", "长春": "54161",
    "沈阳": "54342", "呼和浩特": "53463", "兰州": "52889", "银川": "53614",
    "西宁": "52866", "乌鲁木齐": "51463", "拉萨": "55591",
    "南昌": "58606",
    # 热门旅游 & 新一线城市
    "苏州": "58349", "青岛": "54857", "厦门": "59134", "大连": "54662",
    "三亚": "59948", "桂林": "57957", "丽江": "56651", "大理": "56751",
    "西双版纳": "56959", "景洪": "56959", "张家界": "57662",
    "黄山": "58531", "珠海": "59488", "东莞": "59289", "佛山": "59288",
    "无锡": "58354", "宁波": "58562", "温州": "58659",
    "常州": "58343", "烟台": "54765", "威海": "54774",
    "泉州": "58936", "漳州": "59126", "嘉兴": "58453",
    "绍兴": "58456", "金华": "58549", "台州": "58660",
    "洛阳": "57073", "开封": "57091",
    "秦皇岛": "54449", "承德": "54423",
    "嵊州": "58556", "余杭": "K1418",
    "中山": "59485", "惠州": "59297", "汕头": "59316",
    "芜湖": "58334", "扬州": "58245", "镇江": "58244",
    "徐州": "58027", "连云港": "58044",
    "唐山": "54534", "廊坊": "54518", "保定": "54602",
    "邯郸": "53798", "沧州": "54616",
    "襄阳": "57178", "宜昌": "57461",
    "株洲": "57687", "湘潭": "57688",
    "柳州": "59046", "北海": "59644",
    "遵义": "57713", "安顺": "57806",
    "曲靖": "56786", "玉溪": "56875",
}


# ───────────────── CMA 城市代码自动查询 ─────────────────

def search_city_code_cma(city: str) -> str | None:
    """
    从中国气象局网站自动搜索城市代码。
    尝试多种方式：
    1. CMA autocomplete API
    2. CMA 地图数据 API
    3. 抓取 CMA 搜索页面提取站点代码
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weather.cma.cn/",
        "Accept": "application/json, text/plain, */*",
    }

    # 方式 1: 尝试 CMA 搜索/自动补全 API
    try:
        url = f"https://weather.cma.cn/api/autocomplete?q={quote(city)}"
        resp = requests.get(url, timeout=8, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # 返回格式: {"code": 0, "data": ["城市名-代码-省份", ...]}
        if data.get("code") == 0 and data.get("data"):
            for item in data["data"]:
                parts = str(item).split("-")
                if len(parts) >= 2 and city in parts[0]:
                    return parts[1].strip()
    except Exception:
        pass

    # 方式 2: 尝试 CMA 地图数据 API
    try:
        url = "https://weather.cma.cn/api/map/weather/1"
        resp = requests.get(url, timeout=8, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == 0 and data.get("data"):
            stations = data.get("data", {}).get("city", [])
            if isinstance(stations, list):
                for s in stations:
                    if isinstance(s, dict) and city in s.get("name", ""):
                        return s.get("id", "")
    except Exception:
        pass

    # 方式 3: 尝试从重定向 URL 中提取代码
    try:
        search_url = f"https://weather.cma.cn/web/weather/{quote(city)}.html"
        resp = requests.get(search_url, timeout=8, headers=headers, allow_redirects=True)
        if resp.status_code == 200:
            # 从最终 URL 提取代码
            match = re.search(r'/weather/(\d{5,6})\.html', resp.url)
            if match:
                return match.group(1)
            # 从页面内容提取代码
            match = re.search(r'stationid["\s:=]+["\']?(\d{5,6})', resp.text)
            if match:
                return match.group(1)
    except Exception:
        pass

    return None


def save_city_code(codes_file: str, city: str, code: str):
    """将新发现的城市代码追加到 city-codes.md 文件"""
    if not codes_file:
        return
    try:
        # 先检查文件是否已包含该城市
        if os.path.exists(codes_file):
            with open(codes_file, "r", encoding="utf-8") as f:
                content = f.read()
                if city in content:
                    return  # 已存在，不重复添加

        with open(codes_file, "a", encoding="utf-8") as f:
            f.write(f"| {city} | {code} |\n")
    except Exception:
        pass  # 写入失败不影响主流程


# ───────────────── 天气查询 ─────────────────

def query_wttr(city: str, days: int = 3) -> dict:
    """通过 wttr.in 查询天气（备选方案）"""
    url = f"https://wttr.in/{quote(city)}?format=j1&lang=zh"
    resp = requests.get(url, timeout=15, headers={"User-Agent": "curl/7.68.0"})
    resp.raise_for_status()
    data = resp.json()

    forecasts = []
    for day in data.get("weather", [])[:days]:
        date = day.get("date", "")
        forecasts.append({
            "date": date,
            "weather": day.get("hourly", [{}])[4].get("lang_zh", [{}])[0].get("value", "")
                         if day.get("hourly") and len(day.get("hourly", [])) > 4
                         else day.get("hourly", [{}])[0].get("weatherDesc", [{}])[0].get("value", ""),
            "min_temp": day.get("mintempC", ""),
            "max_temp": day.get("maxtempC", ""),
            "wind": f"{day.get('hourly', [{}])[4].get('winddir16Point', '')} {day.get('hourly', [{}])[4].get('windspeedKmph', '')}km/h"
                    if day.get("hourly") and len(day.get("hourly", [])) > 4
                    else "",
        })

    return {
        "source": "wttr.in",
        "city": city,
        "forecasts": forecasts,
    }


def query_cma(city: str, city_code: str, days: int = 3) -> dict:
    """通过中国气象局网站查询天气（首选）"""
    url = f"https://weather.cma.cn/api/now/{city_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Referer": "https://weather.cma.cn/",
    }
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            return None

        forecast_url = f"https://weather.cma.cn/api/weather/view?stationid={city_code}"
        resp2 = requests.get(forecast_url, timeout=10, headers=headers)
        resp2.raise_for_status()
        fdata = resp2.json()

        if fdata.get("code") != 0:
            return None

        forecasts = []
        daily = fdata.get("data", {}).get("daily", [])
        for day in daily[:days]:
            forecasts.append({
                "date": day.get("date", ""),
                "weather": day.get("dayText", "") + " / " + day.get("nightText", ""),
                "min_temp": str(day.get("low", "")),
                "max_temp": str(day.get("high", "")),
                "wind": day.get("dayWindDir", "") + " " + day.get("dayWindScale", ""),
            })

        return {
            "source": "中国气象局",
            "city": city,
            "forecasts": forecasts,
        }
    except Exception:
        return None


def load_city_codes(codes_file: str) -> dict:
    """从 city-codes.md 加载城市代码映射"""
    codes = {}
    try:
        with open(codes_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "|" in line and not line.startswith("|--") and not line.startswith("| 城市"):
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        codes[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return codes


def classify_weather(weather_desc: str, max_temp: str) -> str:
    """根据天气描述判定标签: good / mild / bad"""
    bad_keywords = ["大雨", "暴雨", "大雪", "暴雪", "冰雹", "台风", "雷暴"]
    mild_keywords = ["小雨", "阵雨", "小雪", "阴", "雾", "霾"]

    for kw in bad_keywords:
        if kw in weather_desc:
            return "bad"
    for kw in mild_keywords:
        if kw in weather_desc:
            return "mild"
    return "good"


def resolve_city_code(city: str, codes_file: str = None, explicit_code: str = None) -> tuple:
    """
    多级查找城市代码，返回 (代码, 来源说明)
    优先级：显式指定 > 外部文件 > 内置字典 > CMA 在线搜索
    """
    # 1. 显式传入的代码
    if explicit_code:
        return explicit_code, "命令行指定"

    # 2. 从外部 city-codes.md 文件查找
    if codes_file:
        file_codes = load_city_codes(codes_file)
        if city in file_codes:
            return file_codes[city], "city-codes.md"

    # 3. 从内置字典查找（精确匹配）
    if city in BUILTIN_CITY_CODES:
        return BUILTIN_CITY_CODES[city], "内置字典"

    # 4. 模糊匹配内置字典（处理别名/简称，如"版纳"→"西双版纳"）
    for key, code in BUILTIN_CITY_CODES.items():
        if city in key or key in city:
            return code, f"内置字典(模糊匹配: {key})"

    # 5. 从 CMA 网站在线搜索
    found_code = search_city_code_cma(city)
    if found_code:
        # 自动保存到 city-codes.md 以备下次使用
        if codes_file:
            save_city_code(codes_file, city, found_code)
        return found_code, "CMA在线查询(已自动保存)"

    return None, "未找到"


def main():
    parser = argparse.ArgumentParser(description="查询城市天气预报（增强版）")
    parser.add_argument("city", help="城市名称（中文）")
    parser.add_argument("--days", type=int, default=3, help="预报天数（默认3天）")
    parser.add_argument("--codes-file", default=None, help="city-codes.md 文件路径")
    parser.add_argument("--city-code", default=None, help="直接指定城市代码")
    parser.add_argument("--lookup-only", action="store_true",
                        help="仅查询城市代码，不查天气")
    args = parser.parse_args()

    # 多级解析城市代码
    city_code, code_source = resolve_city_code(
        args.city, args.codes_file, args.city_code
    )

    # 仅查询代码模式
    if args.lookup_only:
        print(json.dumps({
            "city": args.city,
            "city_code": city_code,
            "source": code_source,
        }, ensure_ascii=False, indent=2))
        return

    result = None

    # 尝试中国气象局
    if city_code:
        result = query_cma(args.city, city_code, args.days)
        if result:
            result["city_code"] = city_code
            result["code_source"] = code_source

    # 降级到 wttr.in
    if not result:
        try:
            result = query_wttr(args.city, args.days)
            if city_code:
                result["city_code"] = city_code
                result["note"] = "CMA 查询失败，已降级到 wttr.in"
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            sys.exit(1)

    # 附加天气标签
    if result and result.get("forecasts"):
        for f in result["forecasts"]:
            f["tag"] = classify_weather(f.get("weather", ""), f.get("max_temp", ""))

    # 输出摘要到 stderr
    if result and result.get("forecasts"):
        fc = result["forecasts"]
        tags = set(f.get("tag", "good") for f in fc)
        worst = "bad" if "bad" in tags else ("mild" if "mild" in tags else "good")
        days_str = " | ".join(
            f"{f.get('date', '?')} {f.get('weather', '?')} {f.get('min_temp', '?')}~{f.get('max_temp', '?')}°C"
            for f in fc[:3]
        )
        summary(f"{args.city} [{worst}] {days_str} (来源:{result.get('source', '?')})")
    elif result and result.get("error"):
        summary(f"{args.city} 查询失败: {result['error']}")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
