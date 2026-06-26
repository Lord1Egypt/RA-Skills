#!/bin/bash
# 延吉公交实时查询工具
# 用法: ./yanji-bus.sh <线路号> [子线路号] [--from <站名> --to <站名>]
# 例如: ./yanji-bus.sh 26 1 --from 少年宫 --to 中国银行延边分行

LINE="${1:?用法: ./yanji-bus.sh <线路号> [子线路号] [--from <站名> --to <站名>]}"
SUBLINE="${2:-1}"

# 解析 --from / --to 参数
FROM_STATION=""
TO_STATION=""
shift 2 2>/dev/null
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM_STATION="$2"; shift 2 ;;
    --to)   TO_STATION="$2"; shift 2 ;;
    *)      shift ;;
  esac
done
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.69(0x1800452d) NetType/WIFI Language/en"
REFERER="http://bus.yanjibus.com:8082/html/bus-route-${LINE}-${SUBLINE}.html"

# 获取实时车辆数据
BUS_DATA=$(curl -s \
  -H "User-Agent: $UA" \
  -H "Referer: $REFERER" \
  -H "X-Requested-With: XMLHttpRequest" \
  "http://bus.yanjibus.com:8082/html/line_data_json_add/line_data_${LINE}_${SUBLINE}.json?r=0.$(date +%s)")

# 获取线路页面（站点信息）
ROUTE_HTML=$(curl -s \
  -H "User-Agent: $UA" \
  "http://bus.yanjibus.com:8082/html/bus-route-${LINE}-${SUBLINE}.html")

# 用 python3 解析所有数据
python3 -c "
import sys, json, re

html = sys.stdin.read()
from_station = '''$FROM_STATION'''
to_station = '''$TO_STATION'''

# 提取站点名称
up_stations = re.findall(r'id=\"bus-up-(\d+)\".*?bus-line-name\">([^<]+)', html)
down_stations = re.findall(r'id=\"bus-down-(\d+)\".*?bus-line-name\">([^<]+)', html)

# 方向判断
def find_station_index(stations, name):
    \"\"\"模糊匹配站名，返回索引和匹配的站名\"\"\"
    for i, (num, sname) in enumerate(stations):
        if name in sname or sname in name:
            return i, sname
    return -1, None

show_direction = None  # None=全部, 'up', 'down'
if from_station and to_station:
    # 在上行中查找
    up_from, up_from_name = find_station_index(up_stations, from_station)
    up_to, up_to_name = find_station_index(up_stations, to_station)
    # 在下行中查找
    down_from, down_from_name = find_station_index(down_stations, from_station)
    down_to, down_to_name = find_station_index(down_stations, to_station)

    up_ok = up_from >= 0 and up_to >= 0 and up_from < up_to
    down_ok = down_from >= 0 and down_to >= 0 and down_from < down_to

    if up_ok and not down_ok:
        show_direction = 'up'
        print(f'>>> 从 [{up_from_name}] 到 [{up_to_name}]，应乘坐【上行】(经过{up_to - up_from}站)')
    elif down_ok and not up_ok:
        show_direction = 'down'
        print(f'>>> 从 [{down_from_name}] 到 [{down_to_name}]，应乘坐【下行】(经过{down_to - down_from}站)')
    elif up_ok and down_ok:
        # 两个方向都可以，选站数少的
        if up_to - up_from <= down_to - down_from:
            show_direction = 'up'
            print(f'>>> 从 [{up_from_name}] 到 [{up_to_name}]，建议乘坐【上行】(经过{up_to - up_from}站，下行需{down_to - down_from}站)')
        else:
            show_direction = 'down'
            print(f'>>> 从 [{down_from_name}] 到 [{down_to_name}]，建议乘坐【下行】(经过{down_to - down_from}站，上行需{up_to - up_from}站)')
    else:
        # 都找不到合理方向
        missing = []
        all_names = [n for _, n in up_stations + down_stations]
        if up_from < 0 and down_from < 0:
            missing.append(f'起点站 [{from_station}]')
        if up_to < 0 and down_to < 0:
            missing.append(f'终点站 [{to_station}]')
        if missing:
            print(f'>>> 未找到{\"、\".join(missing)}，显示全部方向')
        else:
            print(f'>>> [{from_station}] 到 [{to_station}] 方向不可达（起点在终点之后），显示全部方向')
    print()

show_up = show_direction in (None, 'up')
show_down = show_direction in (None, 'down')

print('=== 站点信息 ===')
if show_up and up_stations:
    up_first = up_stations[0][1]
    up_last = up_stations[-1][1]
    print(f'【上行站点】({up_first} → {up_last})')
    for num, name in up_stations:
        marker = ''
        if from_station and to_station:
            idx, _ = find_station_index([(num, name)], from_station)
            if idx >= 0:
                marker = ' ◀ 上车'
            idx, _ = find_station_index([(num, name)], to_station)
            if idx >= 0:
                marker = ' ◀ 下车'
        print(f'  {num}. {name}{marker}')
    print()
if show_down and down_stations:
    down_first = down_stations[0][1]
    down_last = down_stations[-1][1]
    print(f'【下行站点】({down_first} → {down_last})')
    for num, name in down_stations:
        marker = ''
        if from_station and to_station:
            idx, _ = find_station_index([(num, name)], from_station)
            if idx >= 0:
                marker = ' ◀ 上车'
            idx, _ = find_station_index([(num, name)], to_station)
            if idx >= 0:
                marker = ' ◀ 下车'
        print(f'  {num}. {name}{marker}')

# 解析实时数据
bus_json = '''$BUS_DATA'''
print()
print('=== 实时车辆数据 ===')
try:
    data = json.loads(bus_json)
    busdata_str = data.get('busdata', '')
    busdata_str = busdata_str.replace(\"'\", '\"')
    busdata = json.loads(busdata_str)

    up_buses = busdata.get('up', {}).get('busarray', [])
    down_buses = busdata.get('down', {}).get('busarray', [])

    # 建立站名映射
    up_map = {num: name for num, name in up_stations}
    down_map = {num: name for num, name in down_stations}

    up_dir = ''
    down_dir = ''
    if up_stations:
        up_dir = f'({up_stations[0][1]} → {up_stations[-1][1]})'
    if down_stations:
        down_dir = f'({down_stations[0][1]} → {down_stations[-1][1]})'

    if show_up:
        if up_buses:
            print(f'【上行在途车辆: {len(up_buses)}辆】{up_dir}')
            for b in up_buses:
                snum = str(b['stationnum'])
                sname = up_map.get(snum, '未知站点')
                print(f'  -> 第{snum}站 [{sname}] 附近 | 速度:{b[\"speed\"]}km/h | 时间:{b[\"time\"]}')
        else:
            print(f'【上行: 暂无在途车辆】{up_dir}')
        print()

    if show_down:
        if down_buses:
            print(f'【下行在途车辆: {len(down_buses)}辆】{down_dir}')
            for b in down_buses:
                snum = str(b['stationnum'])
                sname = down_map.get(snum, '未知站点')
                print(f'  -> 第{snum}站 [{sname}] 附近 | 速度:{b[\"speed\"]}km/h | 时间:{b[\"time\"]}')
        else:
            print(f'【下行: 暂无在途车辆】{down_dir}')
except Exception as e:
    print(f'解析失败: {e}')
" <<< "$ROUTE_HTML"
