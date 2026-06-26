# -*- coding: utf-8 -*-
"""
同程旅行助手 - ClawHub技能
7大功能：酒店/机票/火车票/汽车票/景点门票/综合交通/度假线路
数据源：同程旅行程心API v2.0（结构化API）
"""

import json
import urllib.request
import urllib.error

PROXY_URL = 'https://1439498936-7vqpkiipef.ap-guangzhou.tencentscf.com'
PROXY_TOKEN = 'tp_8k2mX9vQ4z'


def _call_proxy(route, arguments):
    """调用同程SCF代理"""
    url = PROXY_URL.rstrip('/')
    body = json.dumps({
        'type': route,
        'params': arguments,
    }).encode('utf-8')

    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Proxy-Token', PROXY_TOKEN)

    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        err_body = ''
        try:
            err_body = e.read().decode('utf-8')[:300]
        except:
            pass
        return {'success': False, 'error': f'HTTP {e.code}: {err_body}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def tongcheng_hotel_search(destination: str, extra: str = "") -> str:
    """搜索同程酒店，返回酒店列表含价格、评分、设施和预订链接。

    Args:
        destination: 目的地城市，如"上海"、"北京"
        extra: 补充信息，如"外滩附近 明天入住"或"五星级 含早餐"
    """
    args = {'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_hotel_search', args)

    if not result.get('success'):
        return f"酒店查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    hotels = data.get('hotels', [])
    if not hotels:
        return f"未找到{destination}的酒店信息"

    lines = [f"## {destination}酒店搜索结果（共{data.get('total', len(hotels))}家）\n"]
    for i, h in enumerate(hotels[:12], 1):
        name = h.get('name', '')
        price = h.get('price', '')
        star = h.get('star', '')
        score = h.get('score', '')
        comments = h.get('commentNum', '')
        addr = h.get('address', '')
        desc = h.get('describe', '')
        brand = h.get('brandName', '')
        district = h.get('district', '')
        booking = h.get('bookingUrl', '')

        line = f"**{i}. {name}**"
        if brand:
            line += f" ({brand})"
        line += f"\n   💰 ¥{price}/晚 | ⭐ {score}分 | {star} | {comments}条评价"
        if district:
            line += f"\n   📍 {district} · {addr}"
        elif addr:
            line += f"\n   📍 {addr}"
        if desc:
            line += f"\n   📝 {desc}"
        if booking:
            line += f"\n   🔗 [预订]({booking})"
        lines.append(line)

    return '\n\n'.join(lines)


def tongcheng_flight_search(departure: str, destination: str, extra: str = "") -> str:
    """搜索同程机票，返回航班列表含价格、时刻和航司信息。

    Args:
        departure: 出发城市，如"北京"
        destination: 目的城市，如"上海"
        extra: 补充信息，如"明天"、"最早"、"直飞"
    """
    args = {'departure': departure, 'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_flight_search', args)

    if not result.get('success'):
        return f"机票查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    flights = data.get('flights', [])
    if not flights:
        return f"未找到{departure}→{destination}的航班信息"

    lines = [f"## {departure}→{destination}航班搜索结果（共{data.get('total', len(flights))}个）\n"]
    for i, f in enumerate(flights[:12], 1):
        no = f.get('flightNo', '')
        airline = f.get('airline', '')
        dep_airport = f.get('depAirport', '')
        arr_airport = f.get('arrAirport', '')
        dep_time = f.get('depTime', '')
        arr_time = f.get('arrTime', '')
        dep_date = f.get('depDate', '')
        duration = f.get('duration', '')
        price = f.get('price', '')
        trip_type = f.get('tripType', '')

        type_tag = '直飞' if trip_type == 'DIRECT' else '中转'
        line = f"**{i}. {no}** ({airline}) [{type_tag}]"
        line += f"\n   🛫 {dep_airport} {dep_date} {dep_time} → {arr_airport} {arr_time}"
        line += f"\n   ⏱ 飞行{duration} | 💰 ¥{price}起"
        lines.append(line)

    return '\n\n'.join(lines)


def tongcheng_train_search(departure: str, destination: str, extra: str = "") -> str:
    """搜索同程火车票，返回车次列表含余票、票价和坐席信息。

    Args:
        departure: 出发城市，如"北京"
        destination: 目的城市，如"上海"
        extra: 补充信息，如"明天"、"高铁"、"最早"
    """
    args = {'departure': departure, 'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_train_search', args)

    if not result.get('success'):
        return f"火车票查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    trains = data.get('trains', [])
    if not trains:
        return f"未找到{departure}→{destination}的火车票信息"

    lines = [f"## {departure}→{destination}火车票搜索结果（共{data.get('total', len(trains))}个）\n"]
    for i, t in enumerate(trains[:15], 1):
        no = t.get('trainNo', '')
        dep_station = t.get('depStation', '')
        arr_station = t.get('arrStation', '')
        dep_time = t.get('depTime', '')
        arr_time = t.get('arrTime', '')
        dep_date = t.get('depDate', '')
        duration = t.get('runTime', '')
        price = t.get('price', '')
        tickets = t.get('tickets', [])

        line = f"**{i}. {no}** {dep_station}→{arr_station}"
        line += f"\n   🚄 {dep_date} {dep_time}→{arr_time} | ⏱ {duration} | 💰 ¥{price}起"
        if tickets:
            ticket_strs = []
            for tk in tickets[:3]:
                t_type = tk.get('type', '')
                t_price = tk.get('price', '')
                t_left = tk.get('left', '')
                ticket_strs.append(f"{t_type} ¥{t_price}(余{t_left})")
            line += f"\n   🎫 {' | '.join(ticket_strs)}"
        lines.append(line)

    return '\n\n'.join(lines)


def tongcheng_bus_search(departure: str, destination: str, extra: str = "") -> str:
    """搜索同程汽车票，返回班次列表。

    Args:
        departure: 出发城市，如"上海"
        destination: 目的城市，如"苏州"
        extra: 补充信息，如"明天"、"最早"
    """
    args = {'departure': departure, 'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_bus_search', args)

    if not result.get('success'):
        return f"汽车票查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    buses = data.get('buses', [])
    if not buses:
        return f"未找到{departure}→{destination}的汽车票信息"

    lines = [f"## {departure}→{destination}汽车票搜索结果\n"]
    for i, b in enumerate(buses[:10], 1):
        lines.append(f"**{i}.** {json.dumps(b, ensure_ascii=False)[:200]}")
    return '\n\n'.join(lines)


def tongcheng_scenery_search(destination: str, extra: str = "") -> str:
    """搜索同程景点门票，返回景点列表含价格和评分。

    Args:
        destination: 目的地城市，如"上海"
        extra: 补充信息，如"亲子"、"自然风光"、"5A景区"
    """
    args = {'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_scenery_search', args)

    if not result.get('success'):
        return f"景点查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    sceneries = data.get('sceneries', [])
    if not sceneries:
        return f"未找到{destination}的景点信息"

    lines = [f"## {destination}景点搜索结果（共{data.get('total', len(sceneries))}个）\n"]
    for i, s in enumerate(sceneries[:12], 1):
        name = s.get('name', '')
        price = s.get('price', '')
        score = s.get('score', '')
        addr = s.get('address', '')
        desc = s.get('describe', '')
        booking = s.get('bookingUrl', '')

        line = f"**{i}. {name}**"
        if price:
            line += f" 💰 ¥{price}"
        if score:
            line += f" | ⭐ {score}分"
        if addr:
            line += f"\n   📍 {addr}"
        if desc:
            line += f"\n   📝 {desc}"
        if booking:
            line += f"\n   🔗 [预订]({booking})"
        lines.append(line)

    return '\n\n'.join(lines)


def tongcheng_traffic_search(departure: str, destination: str, extra: str = "") -> str:
    """查询同程综合交通方案，对比飞机/火车/汽车等多种出行方式。

    Args:
        departure: 出发城市，如"北京"
        destination: 目的城市，如"上海"
        extra: 补充信息，如"明天"、"最便宜"、"最快"
    """
    args = {'departure': departure, 'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_traffic_search', args)

    if not result.get('success'):
        return f"交通方案查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    trips = data.get('trips', [])
    if not trips:
        raw = data.get('raw_keys', [])
        if raw:
            return f"查询到数据类型：{', '.join(raw)}，暂无综合方案数据"
        return f"未找到{departure}→{destination}的综合交通方案"

    lines = [f"## {departure}→{destination}综合交通方案\n"]
    for i, t in enumerate(trips[:8], 1):
        lines.append(f"**方案{i}:** {json.dumps(t, ensure_ascii=False)[:300]}")
    return '\n\n'.join(lines)


def tongcheng_travel_search(destination: str, extra: str = "") -> str:
    """搜索同程度假线路，返回旅游套餐/跟团游/自由行产品。

    Args:
        destination: 目的地，如"三亚"、"云南"
        extra: 补充信息，如"5天4晚"、"跟团"、"亲子游"
    """
    args = {'destination': destination}
    if extra:
        args['extra'] = extra
    result = _call_proxy('tongcheng_travel_search', args)

    if not result.get('success'):
        return f"度假线路查询失败：{result.get('error', '未知错误')}"

    data = result.get('data', {})
    trips = data.get('trips', [])
    desc = data.get('desc', '')
    if not trips:
        return f"未找到{destination}的度假线路信息"

    lines = [f"## {destination}度假线路搜索结果（共{data.get('total', len(trips))}个）\n"]
    if desc:
        lines.append(f"📋 {desc}\n")
    for i, t in enumerate(trips[:8], 1):
        lines.append(f"**{i}.** {json.dumps(t, ensure_ascii=False)[:300]}")
    return '\n\n'.join(lines)
