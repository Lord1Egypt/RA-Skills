#!/usr/bin/env bash
# unit-converter: 常用单位换算（纯本地，无网络依赖）
# 用法:
#   unit-converter length 1 km m        # 长度: 1千米=？米
#   unit-converter weight 5 kg g        # 重量: 5千克=？克
#   unit-converter temp 100 c f         # 温度: 100摄氏度=？华氏度
#   unit-converter speed 60 kmh mph     # 速度: 60km/h=？mph
#   unit-converter data 1 GB MB         # 存储: 1GB=？MB
#   unit-converter area 1 ha m2         # 面积: 1公顷=？平方米
#   unit-converter volume 1 L ml        # 体积: 1升=？毫升
set -euo pipefail

show_help() { sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; }

[ $# -lt 4 ] && { show_help; exit 1; }

CAT="$1"; VAL="$2"; FROM="$3"; TO="$4"
[[ "$VAL" =~ ^-?[0-9]+(\.[0-9]+)?$ ]] || { echo "数值格式不对: $VAL" >&2; exit 1; }

python3 - "$CAT" "$VAL" "$FROM" "$TO" <<'PY'
import sys
cat, val, frm, to = sys.argv[1], float(sys.argv[2]), sys.argv[3].lower(), sys.argv[4].lower()

# 各类单位换算表（转换为基准单位）
UNITS = {
  "length": {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000, "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mile": 1609.344},
  "weight": {"mg": 0.001, "g": 1, "kg": 1000, "t": 1000000, "oz": 28.3495, "lb": 453.592},
  "area": {"m2": 1, "km2": 1000000, "ha": 10000, "acre": 4046.86, "ft2": 0.092903},
  "volume": {"ml": 0.001, "l": 1, "m3": 1000, "gal": 3.78541, "cup": 0.236588},
  "data": {"b": 1, "kb": 1024, "mb": 1024**2, "gb": 1024**3, "tb": 1024**4},
  "speed": {"kmh": 1, "mph": 1.609344, "ms": 3.6, "knot": 1.852},
}

NAMES = {
  "length": {"mm":"毫米","cm":"厘米","m":"米","km":"千米","in":"英寸","ft":"英尺","yd":"码","mile":"英里"},
  "weight": {"mg":"毫克","g":"克","kg":"千克","t":"吨","oz":"盎司","lb":"磅"},
  "area": {"m2":"平方米","km2":"平方千米","ha":"公顷","acre":"英亩","ft2":"平方英尺"},
  "volume": {"ml":"毫升","l":"升","m3":"立方米","gal":"加仑","cup":"杯"},
  "data": {"b":"字节","kb":"KB","mb":"MB","gb":"GB","tb":"TB"},
  "speed": {"kmh":"公里/小时","mph":"英里/小时","ms":"米/秒","knot":"节"},
}
CATNAMES = {"length":"长度","weight":"重量","area":"面积","volume":"体积","data":"存储","speed":"速度"}

# 温度特殊处理
if cat == "temp":
    frm_l, to_l = frm.lower(), to.lower()
    if frm_l in ("c", "celsius", "摄氏度", "℃") and to_l in ("f", "fahrenheit", "华氏度", "℉"):
        r = val * 9/5 + 32
        print(f"🌡️ {val:g}°C = {r:g}°F")
    elif frm_l in ("f", "fahrenheit", "华氏度", "℉") and to_l in ("c", "celsius", "摄氏度", "℃"):
        r = (val - 32) * 5/9
        print(f"🌡️ {val:g}°F = {r:g}°C")
    else:
        print("温度只支持 C（摄氏）↔ F（华氏）"); sys.exit(1)
    sys.exit(0)

if cat not in UNITS:
    print(f"不支持的单位类别: {cat}（试试 length/weight/temp/speed/data/area/volume）"); sys.exit(1)
if frm not in UNITS[cat] or to not in UNITS[cat]:
    print(f"单位不支持: {frm} / {to}（{cat} 支持: {', '.join(UNITS[cat])}）"); sys.exit(1)

base = val * UNITS[cat][frm]
r = base / UNITS[cat][to]
fname = NAMES[cat].get(frm, frm)
tname = NAMES[cat].get(to, to)
print(f"📐 {val:g} {fname}（{frm}） = {r:g} {tname}（{to}）")
PY
