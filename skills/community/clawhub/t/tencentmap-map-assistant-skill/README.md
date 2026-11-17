# tencentmap-map-assistant-skill

腾讯位置服务出品。一句自然语言调用腾讯地图全套能力——AI 旅游攻略、地点搜索、路线规划、地址解析、天气查询，无需开发者账号、开箱即用。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.5.2-green.svg)](https://github.com/TencentLBS/tencentmap-map-assistant)

---

## ✨ 能力一览

| 能力 | 说明 | 方法 |
|:-----|:-----|:-----|
| 🗺 AI 旅游攻略 | 自然语言生成多日行程，含小程序二维码入口 | `travel_guide` |
| 📋 个人地图指南 | 从 POI 列表生成地图指南，含小程序二维码入口 | `generate_map_guide` |
| 🔍 地点搜索 | 城市/区域搜索、周边圆形搜索、POI 详情 | `poi_search` / `poi_nearby` / `poi_detail` |
| 💡 关键词输入提示 | 输入补全候选 POI | `poi_sug` |
| 🏛 行政区划 | 省市区列表、下级区划、区划搜索 | `district_list` / `district_children` / `district_search` |
| 📍 地址解析 | 地址 → 坐标 | `geocoder` |
| 📍 逆地址解析 | 坐标 → 地址（可附周边 POI） | `regeocoder` |
| 🌐 IP 定位 | IP → 位置 | `ip_location` |
| 🚗 路线规划 | 驾车 / 步行 / 公交 / 骑行 | `direction` |
| 📏 两点间距离 | 计算两点之间的驾车/步行/骑行距离与用时 | `distance_matrix` |
| 🌤 天气查询 | 行政区/坐标 → 实时或预报天气 | `weather` |
| 🎨 行程可视化 | 把行程或多 POI 渲染成网页地图 | HTML 生成 |

## 🚀 快速开始

### 安装依赖

```bash
pip install -e .
```

> 仅依赖 `requests`，多数环境已自带。

### 基本用法

```python
from tmap_client import TmapClient

client = TmapClient()

# AI 旅游攻略
result = client.travel_guide("武汉5天攻略")

# 地点搜索（含评分、人均、营业时间）
pois = client.poi_search("黄鹤楼", region="武汉")

# 周边搜索
nearby = client.poi_nearby("咖啡", location="22.540601,113.93397", radius=1000)

# 路线规划
route = client.direction("深圳北站", "深圳湾口岸", mode="driving")

# 地址 → 坐标
addr = client.geocoder("深圳市腾讯滨海大厦")

# 坐标 → 地址
loc = client.regeocoder(22.540601, 113.93397, get_poi=True)

# 天气查询
weather = client.weather(adcode="110000", type="now")
```

### 配置正式 Key

未配置 Key 时可通过 tempkey 流程申请 AI 场景临时体验 Key（手机验证，1 年有效，覆盖 WebService API + JSAPI 底图加载）。如已有腾讯位置服务 Key：

```python
from tmap_client import save_key_to_dotenv

save_key_to_dotenv("你的 Key")  # 持久化保存（~/.tencentmap/tempkey.json），之后自动走正式通道
```

> 申请正式 Key：https://lbs.qq.com/dev/console/quick-register

## 📖 API 参考

### `travel_guide(query, lat=30.572815, lng=104.066801)`

生成 AI 旅游攻略，含行程详情与腾讯地图小程序入口二维码。

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `query` | str | ✅ | 自然语言描述，如 "成都3天美食游" |
| `lat` / `lng` | float | | 用户当前位置（辅助上下文，不影响目的地） |

返回：结构化攻略数据 + `output_markdown`（成品攻略文件路径）+ `qr_path`（小程序二维码 PNG）。

> 单次调用约 30-50 秒。

### `poi_search(keyword, region=None, location=None, page_size=10, page_index=1)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `keyword` | str | ✅ | 搜索关键词 |
| `region` | str | 二选一 | 城市/区域名 |
| `location` | str | 二选一 | 中心点 "lat,lng"，启用 5km 邻近搜索 |
| `page_size` | int | | 每页 1-20，默认 10 |
| `page_index` | int | | 页码，默认 1 |

### `poi_nearby(keyword, location, radius=1000, page_size=10, page_index=1)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `keyword` | str | ✅ | 搜索词 |
| `location` | str | ✅ | 中心点 "lat,lng" |
| `radius` | int | | 半径（米），10-1000，默认 1000 |
| `page_index` | int | | 页码，默认 1 |

### `poi_detail(poi_id)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `poi_id` | str | ✅ | POI 唯一 ID（从搜索结果获取） |

### `poi_sug(keyword, region=None, location=None)`

关键词输入提示，用于补全候选 POI。

### `direction(from_addr, to_addr, mode="driving", region=None)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `from_addr` | str | ✅ | 起点地址/景点名/"lat,lng" |
| `to_addr` | str | ✅ | 终点地址/景点名/"lat,lng" |
| `mode` | str | | `driving` / `walking` / `bicycling` / `transit` |
| `region` | str | | 城市名，辅助消歧 |

> 起终点支持地址/景点名自动转坐标。

### `geocoder(address, policy=1)`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `address` | str | ✅ | 地址或地点名 |
| `policy` | int | | `1`=宽松（支持景点名），`0`=标准 |

### `regeocoder(lat, lng, get_poi=False)`

坐标 → 地址，`get_poi=True` 时附带周边 POI 列表。

### `ip_location(ip=None)`

IP → 位置。不传 IP 则定位调用方公网 IP。

### `district_list()` / `district_children(parent_id)` / `district_search(keyword)`

行政区划查询：全国省级列表 / 下级区划 / 关键词搜索。

### `distance_matrix(origin, dest, mode="driving")`

计算两点之间的驾车/步行/骑行距离与用时。

### `weather(adcode=None, location=None, type="now")`

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `adcode` | str | 二选一 | 行政区划代码 |
| `location` | str | 二选一 | 坐标 "lat,lng" |
| `type` | str | | `now` 实时 / `future` 预报 |

## 📁 项目结构

```
tencentmap-map-assistant-skill/
├── SKILL.md                          # Skill 定义与使用说明
├── scripts/
│   ├── send_code.py / create_key.py / save_config.py  # tempkey 临时 Key 配置工具
│   ├── tmap_client.py                # 核心客户端（所有 API 封装）
│   └── test_all.py                   # 测试套件
├── references/
│   ├── agent-notes.md                # AI 调用指引
│   └── jsapi-guide/
│       ├── README.md                 # JSAPI GL 开发指南 + HTML 模板
│       ├── jsapigl/
│       │   ├── docs/                 # 核心 API 文档（21 篇）
│       │   └── demos/                # 核心 API Demo（85+ 个 HTML）
│       └── visualization/
│           ├── docs/                 # 可视化扩展文档（15 篇）
│           └── demos/                # 可视化 Demo（44 个 HTML）
├── setup.py                           # pip install -e . 安装入口
├── .env.example                      # 环境变量模板
├── tempkey-guide.md                  # 临时 Key 申请指南
└── README.md                         # 本文件
```

## 🎨 可视化渲染

多 POI 对比、路线、多天行程等场景可将数据渲染为交互式网页地图：

```python
import json

# POI 数据（实际用 client 返回的坐标）
pois = [
    {"name": "象鼻山", "lat": 25.2675, "lng": 110.2966},
    {"name": "两江四湖", "lat": 25.2798, "lng": 110.2904},
]

# 生成 HTML 地图（底图 key 已内置，直接使用）
markers_js = json.dumps(
    [{"id": str(i), "position": [p["lat"], p["lng"]], "title": p["name"]}
     for i, p in enumerate(pois)],
    ensure_ascii=False,
)

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body,#map{{height:100%;margin:0}}</style>
<script src="https://map.qq.com/api/gljs?v=1&key={TMAP_KEY}"></script>
</head><body><div id="map"></div><script>
const pts = {markers_js};
const map = new TMap.Map('map', {{
  center: new TMap.LatLng(pts[0].position[0], pts[0].position[1]), zoom: 12
}});
new TMap.MultiMarker({{ map, geometries: pts.map(p => ({{
  id: p.id, position: new TMap.LatLng(p.position[0], p.position[1])
}})) }});
new TMap.MultiPolyline({{ map, geometries: [{{
  id: 'route', paths: pts.map(p => new TMap.LatLng(p.position[0], p.position[1]))
}}] }});
</script></body></html>'''

with open("map.html", "w", encoding="utf-8") as f:
    f.write(html)
```

> 更多渲染能力（散点图、热力图、弧线图、轨迹回放等）参见 `references/jsapi-guide/`。

## 🔒 隐私与数据

- AI 旅游攻略（`travel_guide`）与个人地图指南（`generate_map_guide`）会将用户输入的行程/POI 数据发送至腾讯地图服务器，用于生成攻略内容和微信小程序二维码。服务器端数据留存与使用遵循[腾讯位置服务隐私政策](https://lbs.qq.com/userAgreements/agreements/privacy)。

## 🔑 Key 策略

| 场景 | 行为 |
|:-----|:-----|
| 未配置 Key | 需通过 tempkey 流程申请临时体验 Key，或配置正式 Key |
| 已配置 Key | 走正式通道（apis.map.qq.com），使用你自己的额度 |
| Key 优先级 | 传入参数 → 环境变量 `TMAP_KEY` → `~/.tencentmap/tempkey.json` |
