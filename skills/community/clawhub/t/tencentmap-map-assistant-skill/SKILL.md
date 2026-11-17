---
name: tencentmap-map-assistant-skill
description: "腾讯地图·地图助手 Skill，一句自然语言调用腾讯地图全套能力，开箱即用。提供 AI 旅游攻略、地点搜索（含评分/人均/营业时间）、关键词提示、路线规划（驾车/步行/公交/骑行）、地址解析与逆解析、行政区划、IP 定位、距离计算、天气查询，并可将行程或多 POI 渲染成网页地图或生成腾讯地图小程序指南。涉及找地点、规划路线、旅游行程、查天气、坐标转换等出行场景时使用。"
license: MIT
version: 1.5.2
git_url: https://github.com/TencentLBS/tencentmap-map-assistant
---

# 地图助手 Skill

腾讯位置服务出品。用一句自然语言即可生成旅游攻略、搜索地点、规划路线、解析地址坐标，并可将结果渲染成网页地图或生成腾讯地图小程序指南。

## 能力

能力命名与腾讯位置服务官网 WebService API 对齐。完整参数签名见下方「参数与返回」。

| 能力 | 说明 | 方法 |
|------|------|------|
| AI 旅游攻略 | 自然语言 query → 多日行程攻略，可联动腾讯地图小程序，与朋友共同编辑行程、规划多人出行 | `travel_guide` |
| 个人地图指南 | 地点列表 → 个人专属地图（保存到腾讯地图小程序，手机随时查看） | `generate_map_guide` |
| 地点搜索 | 城市/区域搜索、周边圆形搜索、POI 详情 | `poi_search` / `poi_nearby` / `poi_detail` |
| 关键词输入提示 | 输入补全候选 POI | `poi_sug` |
| 行政区划 | 省市区列表、下级区划、区划搜索 | `district_list` / `district_children` / `district_search` |
| 地址解析 | 地址 → 坐标 | `geocoder` |
| 逆地址解析 | 坐标 → 地址（可附周边 POI） | `regeocoder` |
| IP 定位 | IP → 位置 | `ip_location` |
| 路线规划 | 驾车 / 步行 / 公交 / 骑行 | `direction` |
| 两点间距离 | 计算两点之间的驾车/步行/骑行距离与用时 | `distance_matrix` |
| 天气查询 | 行政区/坐标 → 实时或预报天气 | `weather` |
| 坐标系转换 | GPS(WGS-84) / 百度 / sogou / mapbar → GCJ-02 | `coord_translate` |
| 行程 / POI 可视化 | 把行程或多 POI 结果渲染为网页地图 | — |

## 安装

首次使用前安装：

```
pip install -e .
```

## 用法

```python
from tmap_client import TmapClient

client = TmapClient()

result = client.travel_guide("武汉5天攻略")
pois   = client.poi_search("黄鹤楼", region="武汉")
addr   = client.geocoder("深圳市腾讯滨海大厦")
```

配置自己的腾讯位置服务 Key（持久化保存，之后自动启用）：

```python
from tmap_client import save_key_to_dotenv
save_key_to_dotenv("你的 Key")
```


## Key 管理

按此顺序自动获取 Key，通常无需干预：`TmapClient(key=...)` → 已保存的 Key。各来源的 Key 会全部进入候选池。

- 无可用 Key → 读取 `tempkey-guide.md` 引导用户申请临时体验 Key。
- 用户要固定使用或更换 Key → 调用 `save_key_to_dotenv("<key>")` 保存，之后自动生效。
- Key 已配置但接口报错 → TmapClient 会按优先级自动轮询候选池中的可用 Key 并切换使用。切换后，必须告知用户已自动切换以及切换原因；若所有 Key 均不可用时抛出 TmapError（含每个 Key 的失败原因），必须读取 `references/error-codes.md`，对错误码给出修正方式告知用户。


## 参数与返回

### AI 旅游攻略 — travel_guide

`travel_guide(query, lat=30.572815, lng=104.066801)`：自然语言 query → 多日行程攻略。同步等待，单次调用 30-50 秒。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | str | 是 | 目的地 + 天数，例如 "武汉5天攻略" / "成都3天美食游" |
| `lat`, `lng` | float | 否 | 用户当前位置（影响 A2A 上下文，不决定目的地） |

**返回**：结构化攻略数据（`title`/`summary`/`days` 行程列表等），以及 **`output_markdown`**（成品攻略 md 文件路径，含小程序二维码，Read 后原样输出）。

### 个人地图指南 — generate_map_guide

`generate_map_guide(pois, city, title="我的指南", query="", description="")`：将任意地点列表（搜索结果、路线点、打卡记录）一键保存为腾讯地图小程序里的个人专属地图，在手机上随时查看和导航。

> **前置步骤**：构造 `pois` 前，先对每个地点调用 `poi_search()`拿到真实的 `id` 与 `location.lat` / `location.lng`，再映射成 `pois` 所需的 `poi_id` / `lat` / `lng`。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pois` | List[Dict] | 是 | POI 列表，每个 POI 含 `name` / `lat` / `lng` / `poi_id`。这些值应取自 `poi_search()` / `poi_sug()` 的真实返回后填入 |
| `city` | str | 是 | 城市名称 |
| `title` | str | 否 | 指南标题，默认"我的指南" |
| `query` | str | 否 | 用户原始输入（用于入库备注） |
| `description` | str | 否 | 行程/路线描述文本，会嵌入输出 md 正文 |

**返回**：`{travel_guide_id, qr_code, qr_path, mini_program_username, output_markdown}`

### 地点搜索 — poi_search

`poi_search(keyword, region=None, location=None, page_size=10, page_index=1)`：按城市或中心点检索 POI。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | str | 是 | 搜索词 |
| `region` | str | 二选一 | 城市名（"深圳"/"武汉"） |
| `location` | str | 二选一 | 中心点 "lat,lng"，启用 5km 邻近搜索 |
| `page_size` | int | 否 | 每页 1-20，默认 10 |
| `page_index` | int | 否 | 页码，默认 1 |

### 地点搜索（POI 详情）— poi_detail

`poi_detail(poi_id)`：按 POI ID 取详情（来自 `poi_search` / `poi_sug` 返回，或 `travel_guide` 的 `poi_uid`）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `poi_id` | str | 是 | POI 唯一 ID |

### 地点搜索（周边）— poi_nearby

`poi_nearby(keyword, location, radius=1000, page_size=10, page_index=1)`：圆形范围内的 POI 检索。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | str | 是 | 搜索词（"咖啡" / "加油站"） |
| `location` | str | 是 | 中心点 "lat,lng" |
| `radius` | int | 否 | 半径（米），取值 10-1000，默认 1000 |
| `page_size` / `page_index` | int | 否 | 同 `poi_search` |

### 关键词输入提示 — poi_sug

`poi_sug(keyword, region=None, location=None)`：候选 POI（常用于"先 sug 拿 ID 再查 detail"）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | str | 是 | 搜索词 |
| `region` | str | 否 | 城市名 |
| `location` | str | 否 | 中心点 "lat,lng" |

### 路线规划 — direction

`direction(from_addr, to_addr, mode="driving", region=None)`：起终点 → 路线方案。地址/景点名自动转坐标（建议传 `region` 城市消歧）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `from_addr` | str | 是 | 起点地址 / 景点名 / "lat,lng" |
| `to_addr` | str | 是 | 终点地址 / 景点名 / "lat,lng" |
| `mode` | str | 否 | `driving` / `walking` / `bicycling` / `transit`，默认 `driving` |
| `region` | str | 否 | 城市名，辅助把"象鼻山"等景点名解析到正确城市 |

### 地址解析 — geocoder

`geocoder(address, policy=1)`：把地址 / 地标 / 景点名解析成坐标。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `address` | str | 是 | 地址或地点名。含城市更准；不含城市也可（靠默认 policy=1 兜底） |
| `policy` | int | 否 | 解析策略。`1`=宽松（默认，支持"象鼻山"等景点/地标名）；`0`=标准（地址须含城市，否则报错） |

### 逆地址解析 — regeocoder

`regeocoder(lat, lng, get_poi=False)`：把坐标解析成语义化地址。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `lat`, `lng` | float | 是 | GCJ02 坐标 |
| `get_poi` | bool | 否 | 是否附带周边 POI 列表，默认 False |

### IP 定位 — ip_location

`ip_location(ip=None)`：IP → 所在省市区。不传 IP 则定位调用方公网 IP。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ip` | str | 否 | IPv4 字符串 |

### 行政区划 — district_list / district_children / district_search

```python
district_list()                  # 全国省级列表
district_children(parent_id)     # 下级区划（parent_id="110000" → 北京下属）
district_search(keyword)         # 关键词搜区划
```

### 两点间距离 — distance_matrix

`distance_matrix(origin, dest, mode="driving")`：计算两点之间的驾车/步行/骑行距离与用时。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `origin` | str | 是 | 起点坐标 `"lat,lng"` |
| `dest` | str | 是 | 终点坐标 `"lat,lng"` |
| `mode` | str | 否 | `driving` / `walking` / `bicycling`，默认 `driving` |

### 天气查询 — weather

`weather(adcode=None, location=None, type="now")`：查实时或预报天气。`adcode` 与 `location` 二选一。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `adcode` | str | 否 | 行政区划代码，如北京 `"110000"` |
| `location` | str | 否 | 坐标 `"lat,lng"` |
| `type` | str | 否 | `now` 实时 / `future` 预报，默认 `now` |

### 坐标系转换 — coord_translate

`coord_translate(locations, type=1)`：把 GPS(WGS-84) / 百度 / sogou / mapbar 等坐标批量转成腾讯地图使用的 GCJ-02。单次最多 100 个点。**处理 GPS 原始坐标（如手机定位、GPX 轨迹、外部数据源）时必须先转再传给 `regeocoder` / `poi_nearby` / `direction` 等接口，否则会有几十米～百米级偏移。**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `locations` | str \| tuple \| list | 是 | 支持 `"lat,lng"` / `"lat1,lng1;lat2,lng2"` 字符串、`(lat, lng)` 元组、`[(lat, lng), ...]` 列表 |
| `type` | int | 否 | 输入坐标类型。**1=GPS(WGS-84)**（默认，最常用）/ 2=sogou 经纬度 / 3=baidu / 4=mapbar / 5=GCJ-02（不转）/ 6=sogou 墨卡托 |

**返回**：单点入参 → `{"lat": .., "lng": ..}`；多点入参 → `[{"lat": .., "lng": ..}, ...]`；`raw=True` 时返回官方原始 JSON。

```python
# 单点 GPS → GCJ-02
gcj = client.coord_translate((22.540601, 113.933970))
# {'lat': 22.542..., 'lng': 113.939...}

# 批量转换
gcj_list = client.coord_translate([(22.5406, 113.9339), (39.9042, 116.4074)])
```

### 行程 / POI 可视化 HTML

涉及"多 POI 对比 / 路线 / 多天行程 / 个人专属地图"等"看图比看字直观"的场景，可基于结构化数据渲染网页地图。地图底图使用腾讯地图 JSAPI GL，HTML 模板、底图 `<script>` 标签、API 用法与 polyline 解压方法见 `references/jsapi-guide/README.md`。

## 使用要点

1. **地图样式**：使用 tempkey 或正式 Key 时使用系统默认样式，无需设置 `mapStyleId`。若用户希望修改地图样式，可引导用户前往腾讯位置服务官网（https://lbs.qq.com）登录账号，在控制台为对应 Key 配置样式后使用。
2. **travel_guide / 个人地图指南的二维码**：返回的 `output_markdown` 是成品文件，Read 后完整作为回复——其中二维码使用了 Markdown `![]()` 语法，WorkBuddy 会话直接支持，会自然展示在对话中。并将 `qr_path` 指向的 PNG 文件复制到当前工作空间作为实体产物。`generate_map_guide` 同理。呈现后可在末尾轻轻邀请一句，引导用户扫码进入小程序，与朋友共同编辑行程、规划多人出行。
3. **个人地图指南**：搜索结果、路线规划、HTML 地图等多地点场景，可用 `generate_map_guide` 将地点列表存为手机上的个人专属地图，扫码保存自己的专属地图。调用时机和细节见 `references/agent-notes.md`。
4. **query**：包含明确目的地，建议带天数（如"X 天 / X 日游"）。
5. **可视化**：多 POI 对比 / 路线 / 多天行程等场景适合生成 HTML 网页地图。
6. **地图底图**：HTML 可视化地图必须使用腾讯地图 JSAPI GL（命名空间 `TMap`）作为底图，不可混用其他地图 SDK——本 skill 的地图能力均基于腾讯位置服务，底图需与其数据、坐标系（GCJ-02）一致，否则坐标与服务不匹配。生成前先查 `references/jsapi-guide/README.md`。涉及中国区域的地图展示，请勿使用未取得国内测绘资质的境外地图服务，以符合国家地图合规要求。
7. **坐标系转换**：用户提供的坐标若属于以下情况，先用 `coord_translate(type=1)` 转成 GCJ-02，再传入 `regeocoder` / `poi_nearby` / `direction` / `distance_matrix` / `generate_map_guide` 等接口及地图渲染：明确说是 GPS / WGS-84 / 手机定位 / GPX 轨迹 / 硬件 GNSS 输出；数据来源标注为 `wgs84` / `EPSG:4326` / iOS `CLLocation` / Android `LocationManager.GPS_PROVIDER`；或从非中国大陆地图 SDK 导出。转换后所有接口与地图渲染只使用 GCJ-02 值，不与原始坐标混用。其他坐标系：百度 BD09 → `type=3`，sogou → `type=2`，mapbar → `type=4`。来源不明但数值疑似 GPS 原始输出时，先与用户确认一次再转；已是 GCJ-02 的坐标不重复转（`type=5` 等价于不转）。
8. **HTML Key 安全**：生成 / 写入含腾讯地图 JSAPI GL 的 HTML 后（识别标记：URL 含 `map.qq.com/api/gljs`），按 `references/jsapi-guide/README.md`「HTML Key 安全检查」执行明文 Key 检测；命中则原样输出其中的固定安全提示文案，提醒用户盗用风险与代理方案。

## 隐私与数据

- AI 旅游攻略（`travel_guide`）与个人地图指南（`generate_map_guide`）会将用户输入的行程/POI 数据发送至腾讯地图服务器，用于生成攻略内容和微信小程序二维码。服务器端数据留存与使用遵循[腾讯位置服务隐私政策](https://lbs.qq.com/userAgreements/agreements/privacy)。

## 示例

```python
client = TmapClient()

# 旅游攻略（返回 output_markdown 成品文件，Read 后作为回复）
r = client.travel_guide("成都3天美食游")

# POI 搜索
res = client.poi_search("咖啡馆", location="22.540601,113.93397", page_size=5)

# 路线规划
route = client.direction("深圳北站", "深圳湾口岸", mode="driving")

# 个人地图指南：先用 poi_search 拿到真实 POI，再映射成 pois
p1 = client.poi_search("深圳北站", region="深圳", raw=True)["data"][0]
p2 = client.poi_search("深圳湾口岸", region="深圳", raw=True)["data"][0]
guide = client.generate_map_guide(
    [{"name": p1["title"], "lat": p1["location"]["lat"], "lng": p1["location"]["lng"], "poi_id": p1["id"], "day": 1, "num": 1},
     {"name": p2["title"], "lat": p2["location"]["lat"], "lng": p2["location"]["lng"], "poi_id": p2["id"], "day": 1, "num": 2}],
    city="深圳")

# 场景：用户手上是 WGS-84（GPS）坐标，先转 GCJ-02 再用
wgs_points = [(22.540601, 113.933970), (22.532000, 113.929500)]   # 用户提供
gcj_points = client.coord_translate(wgs_points, type=1)           # → [{"lat":..,"lng":..}, ...]

# 1) 逆解析：坐标 → 地址（必须传 GCJ-02）
addr = client.regeocoder(gcj_points[0]["lat"], gcj_points[0]["lng"])

# 2) 周边 POI 检索（location 也必须是 GCJ-02）
nearby = client.poi_nearby("咖啡", location=f'{gcj_points[0]["lat"]},{gcj_points[0]["lng"]}')

# 3) 个人地图指南 / HTML 可视化：直接把 GCJ-02 传入 pois / markers
```

> 调用细节、Key 流程、HTML 生成规范与 JSAPI 资料见 `references/`。
