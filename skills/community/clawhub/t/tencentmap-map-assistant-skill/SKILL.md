---
name: tencentmap-map-assistant-skill
description: 腾讯地图·地图助手 Skill，一句自然语言调用腾讯地图全套能力，无需开发者账号、开箱即用。提供 AI 旅游攻略、地点搜索（含评分/人均/营业时间）、关键词提示、路线规划（驾车/步行/公交/骑行）、地址解析与逆解析、行政区划、IP 定位、距离计算、天气查询，并可将行程或多 POI 渲染成网页地图或生成腾讯地图小程序指南。涉及找地点、规划路线、旅游行程、查天气、坐标转换等出行场景时使用。
license: MIT
version: 1.4.7
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
| 批量距离计算 | 多对多距离矩阵 | `distance_matrix` |
| 天气查询 | 行政区/坐标 → 实时或预报天气 | `weather` |
| 行程 / POI 可视化 | 把行程或多 POI 结果渲染为网页地图 | — |

## 安装

仅依赖 `requests`（多数环境已自带）。如缺失：

```
pip install requests
```

## 用法

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/tencentmap-map-assistant-skill/scripts'))
from tmap_client import TmapClient

client = TmapClient()

result = client.travel_guide("武汉5天攻略")
pois   = client.poi_search("黄鹤楼", region="武汉")
addr   = client.geocoder("深圳市腾讯滨海大厦")
```

配置自己的腾讯位置服务 Key（持久化到 `.env`，之后自动启用）：

```python
from tmap_client import save_key_to_dotenv
save_key_to_dotenv("你的 Key")
```


## Key 检查

1. 已有 Key（用户传入 `TmapClient(key=...)`、环境变量 `TMAP_KEY`、skill 包内 `.env` 文件或 `~/.tencentmap/tempkey.json`）→ 直接使用

2. 未检测到 Key 时向用户输出以下选项：

   > - **申请临时体验 Key（推荐）**：手机验证即可，14 天有效
   > - **前往官网注册正式 Key**：https://lbs.qq.com/dev/console/key/manage

3. 用户选择"申请临时 Key" → 读取 `tempkey-guide.md` 按其中步骤执行


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

### 批量距离计算 — distance_matrix

`distance_matrix(from_list, to_list, mode="driving")`：批量计算多个起点到多个终点的距离与时长。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `from_list` | List[str] | 是 | 起点列表 `["lat,lng", ...]` |
| `to_list` | List[str] | 是 | 终点列表 `["lat,lng", ...]` |
| `mode` | str | 否 | `driving` / `walking` / `bicycling`，默认 `driving` |

### 天气查询 — weather

`weather(adcode=None, location=None, type="now")`：查实时或预报天气。`adcode` 与 `location` 二选一。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `adcode` | str | 否 | 行政区划代码，如北京 `"110000"` |
| `location` | str | 否 | 坐标 `"lat,lng"` |
| `type` | str | 否 | `now` 实时 / `future` 预报，默认 `now` |

### 行程 / POI 可视化 HTML

涉及"多 POI 对比 / 路线 / 多天行程 / 个人专属地图"等"看图比看字直观"的场景，可基于结构化数据渲染网页地图。地图底图使用腾讯地图 JSAPI GL，HTML 模板、底图 `<script>` 标签、API 用法与 polyline 解压方法见 `references/jsapi-guide/README.md`。

## 使用要点

1. **Key**：未配置 Key 时按"Key 检查"流程处理；如已有 Key，用 `save_key_to_dotenv` 配置后稳定性更佳
2. **地图样式**：使用 tempkey 或正式 Key 时使用系统默认样式，无需设置 `mapStyleId`。若用户希望修改地图样式，可引导用户前往腾讯位置服务官网登录账号，在控制台为对应 Key 配置样式后使用。
3. **travel_guide / 个人地图指南的二维码**：返回的 `output_markdown` 是成品文件，Read 后完整作为回复——其中二维码使用了 Markdown `![]()` 语法，WorkBuddy 会话直接支持，会自然展示在对话中。**同时**将 `qr_path` 指向的 PNG 文件复制到当前工作空间作为实体产物。`generate_map_guide` 同理。呈现后可在末尾轻轻邀请一句，引导用户扫码进入小程序，与朋友共同编辑行程、规划多人出行。
4. **个人地图指南**：搜索结果、路线规划、HTML 地图等多地点场景，可用 `generate_map_guide` 将地点列表存为手机上的个人专属地图，扫码保存自己的专属地图。调用时机和细节见 `references/agent-notes.md`。
5. **query**：包含明确目的地，建议带天数（如"X 天 / X 日游"）。
6. **可视化**：多 POI 对比 / 路线 / 多天行程等场景适合生成 HTML 网页地图；单点查询直接返回结构化数据。

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
p1 = client.poi_search("深圳北站", region="深圳")["data"][0]
p2 = client.poi_search("深圳湾口岸", region="深圳")["data"][0]
guide = client.generate_map_guide(
    [{"name": p1["title"], "lat": p1["location"]["lat"], "lng": p1["location"]["lng"], "poi_id": p1["id"], "day": 1, "num": 1},
     {"name": p2["title"], "lat": p2["location"]["lat"], "lng": p2["location"]["lng"], "poi_id": p2["id"], "day": 1, "num": 2}],
    city="深圳")
```

> 调用细节、Key 流程、HTML 生成规范与 JSAPI 资料见 `references/`。
