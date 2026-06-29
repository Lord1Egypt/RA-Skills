import os
#!/usr/bin/env python3
"""航班动态追踪 - Flight Tracker
基于飞常准(VariFlight) API，提供航班实时动态、延误分析、舒适度评分、机场天气
走SCF代理，用户零配置，API Key隐藏在代理端
"""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ========== 配置 ==========
# SCF代理（Key隐藏在代理端）
SCF_PROXY_URL = "https://1439498936-eqcpuaevzz.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 常用机场代码映射
AIRPORT_CODES = {
    "北京": "PEK", "北京首都": "PEK", "北京大兴": "PKX",
    "上海": "SHA", "上海虹桥": "SHA", "上海浦东": "PVG",
    "广州": "CAN", "深圳": "SZX", "成都": "CTU",
    "杭州": "HGH", "重庆": "CKG", "西安": "XIY",
    "武汉": "WUH", "长沙": "CSX", "南京": "NKG",
    "厦门": "XMN", "昆明": "KMG", "青岛": "TAO",
    "大连": "DLC", "天津": "TSN", "郑州": "CGO",
    "海口": "HAK", "三亚": "SYX", "贵阳": "KWE",
    "哈尔滨": "HRB", "沈阳": "SHE", "长春": "CGQ",
    "福州": "FOC", "济南": "TNA", "太原": "TYN",
    "南宁": "NNG", "兰州": "LHW", "乌鲁木齐": "URC",
    "拉萨": "LXA", "呼和浩特": "HET", "银川": "INC",
    "西宁": "XNN", "石家庄": "SJW", "合肥": "HFE",
    "南昌": "KHN", "温州": "WNZ", "宁波": "NGB",
    "烟台": "YNT", "珠海": "ZUH", "揭阳": "SWA",
    "桂林": "KWL", "丽江": "LJG", "大理": "DLU",
    "九寨沟": "JZH", "张家界": "DYG",
    # 国际
    "东京": "NRT", "东京成田": "NRT", "东京羽田": "HND",
    "大阪": "KIX", "首尔": "ICN", "釜山": "PUS",
    "曼谷": "BKK", "新加坡": "SIN", "吉隆坡": "KUL",
    "河内": "HAN", "胡志明": "SGN", "雅加达": "CGK",
    "马尼拉": "MNL", "金边": "PNH", "暹粒": "REP",
    "巴厘岛": "DPS", "清迈": "CNX", "普吉岛": "HKT",
    "悉尼": "SYD", "墨尔本": "MEL", "奥克兰": "AKL",
    "伦敦": "LHR", "巴黎": "CDG", "法兰克福": "FRA",
    "阿姆斯特丹": "AMS", "莫斯科": "SVO", "罗马": "FCO",
    "纽约": "JFK", "洛杉矶": "LAX", "旧金山": "SFO",
    "芝加哥": "ORD", "迪拜": "DXB",
}

# 城市代码（用于票价查询）
CITY_CODES = {
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "成都": "CTU", "杭州": "HGH", "重庆": "CKG", "西安": "XIY",
    "武汉": "WUH", "长沙": "CSX", "南京": "NKG", "厦门": "XMN",
    "昆明": "KMG", "青岛": "TAO", "大连": "DLC", "天津": "TSN",
    "郑州": "CGO", "海口": "HAK", "三亚": "SYX", "贵阳": "KWE",
    "哈尔滨": "HRB", "沈阳": "SHE", "长春": "CGQ",
    "东京": "TYO", "大阪": "OSA", "首尔": "SEL", "曼谷": "BKK",
    "新加坡": "SIN", "悉尼": "SYD", "伦敦": "LON", "巴黎": "PAR",
    "纽约": "NYC", "洛杉矶": "LAX", "迪拜": "DXB",
}

# 航空公司代码
AIRLINES = {
    "CA": "中国国航", "MU": "东方航空", "CZ": "南方航空",
    "HU": "海南航空", "3U": "四川航空", "MF": "厦门航空",
    "SC": "山东航空", "FM": "上海航空", "ZH": "深圳航空",
    "GS": "天津航空", "EU": "成都航空", "G5": "华夏航空",
    "PN": "西部航空", "9C": "春秋航空", "HO": "吉祥航空",
    "KY": "昆明航空", "FU": "福州航空", "AQ": "九元航空",
    "NS": "河北航空", "JR": "幸福航空", "DZ": "东海航空",
    "OQ": "重庆航空", "YI": "多彩航空", "RW": "江西航空",
    "CA": "国航", "MU": "东航", "CZ": "南航",
    "NH": "全日空", "JL": "日航", "KE": "大韩航空",
    "OZ": "韩亚航空", "TG": "泰航", "SQ": "新航",
    "CX": "国泰航空", "QF": "澳航", "EK": "阿联酋航空",
    "BA": "英航", "AF": "法航", "LH": "汉莎航空",
    "DL": "达美航空", "AA": "美航", "UA": "美联航",
}

# 航班状态中文映射
FLIGHT_STATES = {
    "计划": "📋 计划中",
    "起飞": "✈️ 已起飞",
    "到达": "🛬 已到达",
    "延误": "⏰ 延误",
    "取消": "❌ 取消",
    "备降": "🔄 备降",
    "返航": "🔙 返航",
    "取消待定": "⚠️ 可能取消",
}


def _api_request(endpoint, params):
    """通过SCF代理调用飞常准API"""
    body = json.dumps({
        "type": endpoint,
        "params": params
    }).encode('utf-8')

    req = urllib.request.Request(
        SCF_PROXY_URL,
        data=body,
        headers={
            'X-Proxy-Token': PROXY_TOKEN,
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            # SCF代理返回格式：{"code": 0, "data": {飞常准原始响应}}
            if result.get("code") == 0:
                return result.get("data", {})
            else:
                return {"code": -1, "message": result.get("error", "代理请求失败")}
    except urllib.error.HTTPError as e:
        return {"code": e.code, "message": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"code": -1, "message": str(e)}


def _resolve_airport(code_or_name):
    """解析机场代码或城市名"""
    if not code_or_name:
        return None
    code = code_or_name.upper().strip()
    if code in AIRPORT_CODES.values():
        return code
    # 中文城市名
    for name, airport_code in AIRPORT_CODES.items():
        if code_or_name == name:
            return airport_code
    # 直接传3字母代码
    if len(code) == 3 and code.isalpha():
        return code
    return None


def _resolve_city_code(name):
    """解析城市代码"""
    if not name:
        return None
    name = name.strip()
    if name in CITY_CODES:
        return CITY_CODES[name]
    return None


def _format_time(time_str):
    """格式化时间字符串"""
    if not time_str:
        return "—"
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return str(time_str)


def _format_datetime(time_str):
    """格式化完整时间"""
    if not time_str:
        return "—"
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%m-%d %H:%M")
    except (ValueError, TypeError):
        return str(time_str)


def _get_airline_name(flight_no):
    """从航班号获取航空公司名"""
    if not flight_no or len(flight_no) < 2:
        return "未知航司"
    prefix = flight_no[:2].upper()
    # 处理数字前缀（如9C）
    if flight_no[0].isdigit():
        prefix = flight_no[:2]
    return AIRLINES.get(prefix, prefix)


def _calc_delay_minutes(plan_str, actual_str):
    """计算延误分钟数"""
    if not plan_str or not actual_str:
        return None
    try:
        plan = datetime.strptime(plan_str, "%Y-%m-%d %H:%M:%S")
        actual = datetime.strptime(actual_str, "%Y-%m-%d %H:%M:%S")
        delta = (actual - plan).total_seconds() / 60
        return int(delta)
    except (ValueError, TypeError):
        return None


def _delay_emoji(delay_min):
    """根据延误时间返回emoji"""
    if delay_min is None:
        return ""
    if delay_min <= 0:
        return "✅"
    elif delay_min <= 15:
        return "🟢"
    elif delay_min <= 30:
        return "🟡"
    elif delay_min <= 60:
        return "🟠"
    else:
        return "🔴"


# ========== 工具1: 航班动态查询 ==========
def cmd_flight_status(flight_no, date=None):
    """查询单个航班的实时动态"""
    if not flight_no:
        return json.dumps({"status": "error", "message": "请提供航班号"}, ensure_ascii=False)

    flight_no = flight_no.upper().strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    result = _api_request("flight", {"fnum": flight_no, "date": date})

    if result.get("code") != 200:
        return json.dumps({
            "status": "error",
            "message": f"查询失败：{result.get('message', '未知错误')}"
        }, ensure_ascii=False)

    flights = result.get("data", [])
    if not flights:
        return json.dumps({
            "status": "empty",
            "message": f"未找到航班 {flight_no}（{date}）的动态信息"
        }, ensure_ascii=False)

    output = f"✈️ **航班动态：{flight_no}**（{date}）\n\n"

    for f in flights:
        state = f.get("FlightState", "未知")
        state_display = FLIGHT_STATES.get(state, state)

        airline = _get_airline_name(flight_no)
        dep = f.get("FlightDep", "")
        arr = f.get("FlightArr", "")
        dep_airport = f.get("FlightDepAirport", "")
        arr_airport = f.get("FlightArrAirport", "")
        dep_terminal = f.get("FlightHTerminal", "")
        arr_terminal = f.get("FlightTerminal", "")

        plan_dep = f.get("FlightDeptimePlanDate", "")
        plan_arr = f.get("FlightArrtimePlanDate", "")
        actual_dep = f.get("FlightDeptimeDate", "")
        actual_arr = f.get("FlightArrtimeDate", "")

        dep_delay = _calc_delay_minutes(plan_dep, actual_dep)
        arr_delay = _calc_delay_minutes(plan_arr, actual_arr)

        output += f"**状态**：{state_display}\n\n"
        output += f"| 项目 | 计划 | 实际 | 延误 |\n|------|------|------|------|\n"
        output += f"| 🛫 出发 {dep}({dep_airport} {dep_terminal}) | {_format_time(plan_dep)} | {_format_time(actual_dep) or '—'} | {_delay_emoji(dep_delay)} {f'{dep_delay}分钟' if dep_delay and dep_delay > 0 else '准点' if dep_delay is not None else '—'} |\n"
        output += f"| 🛬 到达 {arr}({arr_airport} {arr_terminal}) | {_format_time(plan_arr)} | {_format_time(actual_arr) or '—'} | {_delay_emoji(arr_delay)} {f'{arr_delay}分钟' if arr_delay and arr_delay > 0 else '准点' if arr_delay is not None else '—'} |\n"

        # 额外信息
        extras = []
        if f.get("OntimeRate"):
            extras.append(f"准点率：{f['OntimeRate']}")
        if f.get("ftype"):
            extras.append(f"机型：{f['ftype']}")
        if f.get("BoardGate"):
            extras.append(f"登机口：{f['BoardGate']}")
        if f.get("CheckDoor"):
            extras.append(f"到达出口：{f['CheckDoor']}")
        if f.get("BaggageID"):
            extras.append(f"行李转盘：{f['BaggageID']}")
        if f.get("distance"):
            extras.append(f"飞行距离：{f['distance']}km")

        if extras:
            output += f"\n📊 {' | '.join(extras)}\n"

        # 延误分析
        if dep_delay is not None and dep_delay > 30:
            output += f"\n⚠️ **延误提示**：出发延误{dep_delay}分钟"
            if f.get("DelayReason"):
                output += f"，原因：{f['DelayReason']}"
            output += "\n"

    return output


# ========== 工具2: 航线动态查询 ==========
def cmd_route_status(dep, arr, date=None):
    """查询某条航线上所有航班的动态"""
    dep_code = _resolve_airport(dep)
    arr_code = _resolve_airport(arr)

    if not dep_code or not arr_code:
        return json.dumps({
            "status": "error",
            "message": f"无法识别出发地/目的地：{dep}/{arr}。请使用城市名（如北京、上海）或机场代码（如PEK、SHA）"
        }, ensure_ascii=False)

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    result = _api_request("flights", {"dep": dep_code, "arr": arr_code, "date": date})

    if result.get("code") != 200:
        return json.dumps({
            "status": "error",
            "message": f"查询失败：{result.get('message', '未知错误')}"
        }, ensure_ascii=False)

    flights = result.get("data", [])
    if not flights:
        return json.dumps({
            "status": "empty",
            "message": f"未找到 {dep}→{arr}（{date}）的航班"
        }, ensure_ascii=False)

    # 按状态分类
    cancelled = []
    delayed = []
    normal = []
    arrived = []

    for f in flights:
        state = f.get("FlightState", "")
        if "取消" in state:
            cancelled.append(f)
        elif "延误" in state:
            delayed.append(f)
        elif "到达" in state or "到达" in state:
            arrived.append(f)
        else:
            normal.append(f)

    dep_name = flights[0].get("FlightDep", dep) if flights else dep
    arr_name = flights[0].get("FlightArr", arr) if flights else arr

    output = f"✈️ **航线动态：{dep_name} → {arr_name}**（{date}）\n\n"
    output += f"共 {len(flights)} 个航班"
    if cancelled:
        output += f"  ❌取消{len(cancelled)}"
    if delayed:
        output += f"  ⏰延误{len(delayed)}"
    output += "\n\n"

    # 延误航班优先展示
    all_sorted = delayed + cancelled + normal + arrived
    for i, f in enumerate(all_sorted[:15]):  # 最多展示15个
        state = f.get("FlightState", "未知")
        state_display = FLIGHT_STATES.get(state, state)
        fno = f.get("FlightNo", "")
        airline = _get_airline_name(fno)

        plan_dep = _format_time(f.get("FlightDeptimePlanDate", ""))
        plan_arr = _format_time(f.get("FlightArrtimePlanDate", ""))
        actual_dep = _format_time(f.get("FlightDeptimeDate", ""))
        actual_arr = _format_time(f.get("FlightArrtimeDate", ""))

        dep_delay = _calc_delay_minutes(f.get("FlightDeptimePlanDate", ""), f.get("FlightDeptimeDate", ""))
        delay_str = f"延误{dep_delay}min" if dep_delay and dep_delay > 0 else ""

        actual_dep_str = f"实际{_format_time(f.get('FlightDeptimeDate', ''))}" if f.get("FlightDeptimeDate") else ""

        output += f"{i+1}. **{fno}** {airline} {state_display}\n"
        output += f"   {plan_dep}→{plan_arr}"
        if actual_dep_str:
            output += f" | {actual_dep_str}"
        if delay_str:
            output += f" | {_delay_emoji(dep_delay)} {delay_str}"
        output += "\n"

    if len(all_sorted) > 15:
        output += f"\n...还有 {len(all_sorted) - 15} 个航班\n"

    return output


# ========== 工具3: 航班舒适度评分 ==========
def cmd_flight_happiness(dep, arr, date=None):
    """查询航线舒适度评分"""
    dep_code = _resolve_airport(dep)
    arr_code = _resolve_airport(arr)

    if not dep_code or not arr_code:
        return json.dumps({
            "status": "error",
            "message": f"无法识别出发地/目的地：{dep}/{arr}"
        }, ensure_ascii=False)

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    result = _api_request("happiness", {"dep": dep_code, "arr": arr_code, "date": date})

    if result.get("code") != 200:
        return json.dumps({
            "status": "error",
            "message": f"查询失败：{result.get('message', '未知错误')}"
        }, ensure_ascii=False)

    flights = result.get("data", [])
    if not flights:
        return json.dumps({
            "status": "empty",
            "message": f"未找到 {dep}→{arr} 的舒适度数据"
        }, ensure_ascii=False)

    output = f"😊 **航班舒适度：{dep} → {arr}**（{date}）\n\n"

    # 去重：按航班号+出发到达，并过滤取消的航班
    seen = set()
    unique_flights = []
    for f in flights:
        cancel_prob = f.get("CancelProb", "0%")
        try:
            cp = float(cancel_prob.replace("%", ""))
        except (ValueError, AttributeError):
            cp = 0
        if cp >= 100:
            continue  # 跳过已取消航班
        key = f"{f.get('FlightNo', '')}_{f.get('FlightDepcode', '')}_{f.get('FlightArrcode', '')}"
        if key not in seen:
            seen.add(key)
            unique_flights.append(f)

    for f in unique_flights[:10]:  # 最多10个
        fno = f.get("FlightNo", "")
        ontime_rate = f.get("OntimeRate", "—")
        cancel_prob = f.get("CancelProb", "—")
        dep_avg_delay = f.get("DepAvgDelaytime", "—")
        arr_avg_delay = f.get("ArrAvgDelaytime", "—")
        food = f.get("Food", "—")
        air_service = f.get("AirService", "—")
        generic = f.get("Generic", "")
        flight_year = f.get("FlightYear", "")

        # 综合评分
        score_parts = []
        try:
            if ontime_rate and ontime_rate != "—":
                ot = float(ontime_rate.replace("%", ""))
                score_parts.append(("准点率", min(ot, 100)))
        except (ValueError, AttributeError):
            pass

        try:
            if dep_avg_delay and dep_avg_delay != "—":
                avg_d = float(dep_avg_delay)
                score_parts.append(("出发延误", max(0, 100 - avg_d * 2)))
        except (ValueError, AttributeError):
            pass

        total_score = sum(s for _, s in score_parts) / len(score_parts) if score_parts else 0
        if total_score >= 80:
            score_emoji = "🟢"
        elif total_score >= 60:
            score_emoji = "🟡"
        else:
            score_emoji = "🔴"

        output += f"**{fno}** {score_emoji}{total_score:.0f}分"
        if generic:
            output += f" | 机型{generic}"
        output += "\n"
        output += f"  准点率：{ontime_rate} | 取消概率：{cancel_prob} | 出发均延：{dep_avg_delay}min | 到达均延：{arr_avg_delay}min\n"
        output += f"  餐食：{food} | 机上服务：{air_service}"
        if flight_year:
            output += f" | 机龄：{flight_year}年"
        output += "\n\n"

    return output


# ========== 工具4: 机场天气 ==========
def cmd_airport_weather(airport):
    """查询机场天气"""
    code = _resolve_airport(airport)
    if not code:
        return json.dumps({
            "status": "error",
            "message": f"无法识别机场：{airport}"
        }, ensure_ascii=False)

    result = _api_request("futureAirportWeather", {"code": code, "type": "1"})

    if result.get("code") != 200:
        return json.dumps({
            "status": "error",
            "message": f"查询失败：{result.get('message', '未知错误')}"
        }, ensure_ascii=False)

    data = result.get("data", {})
    current = data.get("current", {})
    future = data.get("future", {})

    output = f"🌤️ **{current.get('AirportCity', airport)}机场天气**\n\n"

    if current:
        output += f"**当前天气**（{current.get('ReportTime', '—')}）\n\n"
        output += f"| 项目 | 数据 |\n|------|------|\n"
        output += f"| 天气 | {current.get('Type', '—')} |\n"
        output += f"| 温度 | {current.get('Temperature', '—')}°C |\n"
        output += f"| 能见度 | {current.get('Visib', '—')}m |\n"
        output += f"| 风力 | {current.get('WindDirection', '—')} {current.get('WindPower', '—')} |\n"
        output += f"| AQI | {current.get('Aqi', '—')}（{current.get('Quality', '—')}） |\n"
        if current.get('PM2.5'):
            output += f"| PM2.5 | {current.get('PM2.5')} |\n"

        # 对飞行的影响评估
        visib = current.get('Visib', '9999')
        wind = current.get('WindPower', '0级')
        try:
            visib_val = int(visib)
            wind_level = int(wind.replace('级', '')) if '级' in str(wind) else 0
        except (ValueError, TypeError):
            visib_val = 9999
            wind_level = 0

        impact = ""
        if visib_val < 800:
            impact += "⚠️ 能见度极低（<800m），航班可能延误或取消\n"
        elif visib_val < 1500:
            impact += "🟡 能见度较低，部分航班可能受影响\n"
        if wind_level >= 8:
            impact += "⚠️ 风力极大（8级+），航班可能取消\n"
        elif wind_level >= 6:
            impact += "🟡 风力较大（6-7级），航班可能延误\n"

        if impact:
            output += f"\n**✈️ 对飞行的影响**：\n{impact}"

    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: flight_tracker.py <command> [args]\n命令: status <航班号> [日期] | route <出发> <到达> [日期] | comfort <出发> <到达> [日期] | weather <机场/城市>",
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "status":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供航班号，如 CA1507"}, ensure_ascii=False))
            return
        flight_no = sys.argv[2]
        date = sys.argv[3] if len(sys.argv) > 3 else None
        result = cmd_flight_status(flight_no, date)
        if isinstance(result, dict) or result.startswith("{"):
            print(result)
        else:
            print(result)

    elif command == "route":
        if len(sys.argv) < 4:
            print(json.dumps({"status": "error", "message": "请提供出发地和目的地，如 北京 上海"}, ensure_ascii=False))
            return
        dep = sys.argv[2]
        arr = sys.argv[3]
        date = sys.argv[4] if len(sys.argv) > 4 else None
        result = cmd_route_status(dep, arr, date)
        if isinstance(result, dict) or result.startswith("{"):
            print(result)
        else:
            print(result)

    elif command == "comfort":
        if len(sys.argv) < 4:
            print(json.dumps({"status": "error", "message": "请提供出发地和目的地"}, ensure_ascii=False))
            return
        dep = sys.argv[2]
        arr = sys.argv[3]
        date = sys.argv[4] if len(sys.argv) > 4 else None
        result = cmd_flight_happiness(dep, arr, date)
        if isinstance(result, dict) or result.startswith("{"):
            print(result)
        else:
            print(result)

    elif command == "weather":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供机场或城市名"}, ensure_ascii=False))
            return
        airport = sys.argv[2]
        result = cmd_airport_weather(airport)
        if isinstance(result, dict) or result.startswith("{"):
            print(result)
        else:
            print(result)

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: status | route | comfort | weather",
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
