# 腾讯地图 JSAPI GL 资料（内嵌）

> 本目录是腾讯地图 JS API GL 的完整开发资料，内嵌在本 skill 包里，
> 在需要为旅游攻略 / 多 POI / 路线出 HTML 可视化时直接查阅。
>
> HTML 地图底图使用腾讯地图 JSAPI GL。底图 `<script>` 标签见下方「API Key」段，直接照抄即可。

## ⚠️ 强制约束：底图 & 命名空间

- **底图**：本 skill 全链路绑定腾讯位置服务——WebService API、GCJ-02 坐标系、Key 与额度体系均为腾讯地图。因此所有 HTML 可视化地图必须使用腾讯地图 JSAPI GL 作为底图，与数据层保持一致；换用其他地图 SDK 会导致坐标系、服务接口、样式体系不匹配。涉及中国区域的地图展示，也需符合国家地图合规要求，不使用未取得国内测绘资质的境外地图服务。
- **命名空间**：JSAPI GL 挂在全局 **`TMap`** 上（大小写严格：**T** 大写、**M** 大写，其余小写）。所有 API 必须走 `TMap.xxx`：`new TMap.Map(container, opts)`、`new TMap.LatLng(lat, lng)`、`new TMap.MultiMarker(...)`、`new TMap.MultiPolyline(...)`、`new TMap.InfoWindow(...)`、`new TMap.MultiLabel(...)` 等。
- ❌ 常见错误：把地图 API 写成非 `TMap` 的全局对象（如错误大小写 `TMAP.Map` / `Tmap.Map`、旧版 `qq.maps.Map`，或其他地图 SDK 的全局命名空间）——一律不允许，统一改用 `TMap.xxx`。

## 何时读这里

当需要把行程 / POI / 路线渲染成 HTML 地图时，按以下顺序查阅：

1. **底图 key 与 HTML 生成示例** → 下方「API Key」与「HTML 生成示例」段（照抄即可出图）
2. **画路线** → 下方「画路线：polyline 解压」段
3. **JSAPI 核心 API（地图初始化 / marker / 路线连线 / 弹窗等基础能力）** → `jsapigl/docs/*.md`（下方有完整文件名清单）
4. **可视化扩展库（热力图 / 轨迹 / 弧线 / 区域图等高级可视化）** → `visualization/docs/*.md`（下方有完整文件名清单）
5. **demo 代码** → `*/demos/`

## jsapigl/docs/ 文件清单（21 个核心 API 文档）

| 文档 | 说明 / 何时读 |
|------|--------------|
| `概述.md` | API 总览，第一次接入先看 |
| `地图.md` | 地图初始化、移动、缩放等核心 API |
| `基础类.md` | LatLng / Point 等基础数据类型 |
| `点标记.md` | Marker（POI 标记必读） |
| `点聚合.md` | MarkerCluster（多 POI 聚合） |
| `信息窗体.md` | InfoWindow（POI 弹窗，旅游攻略必读） |
| `矢量图形.md` | Polyline / Polygon（路线连线必读） |
| `文本标记.md` | Label 文字标注 |
| `DOM覆盖物.md` | 自定义 HTML 覆盖物 |
| `事件.md` | 地图/marker 事件处理 |
| `控件.md` | 缩放/比例尺等内置控件 |
| `室内图.md` | 室内地图 |
| `自定义图层.md` | 自定义图层 |
| `环境检测.md` | 浏览器/WebGL 支持检测 |
| `附加库：几何计算库.md` | geometry 库（距离/面积计算） |
| `附加库：地图工具.md` | tools 库（标尺/绘图工具） |
| `附加库：地图视角附加库.md` | view 库（视角控制） |
| `附加库：天气图层.md` | weather 图层 |
| `附加库：服务类库.md` | service 库（地理编码等） |
| `附加库：模型库.md` | model 库（3D GLTF/3DTiles） |
| `附加库：矢量数据图层.md` | vector 库（GeoJSON/MVT） |

## visualization/docs/ 文件清单（14 个可视化扩展）

| 文档 | 说明 / 何时读 |
|------|--------------|
| `参考手册.md` | 可视化扩展库总览 |
| `基础类.md` | 通用基础类 |
| `事件.md` | 可视化层事件 |
| `散点图.md` | 散点图（旅游 POI 可用） |
| `热力图.md` | 热力图 |
| `网格热力图.md` | 网格化热力图 |
| `蜂窝热力图.md` | 六边形热力图 |
| `辐射圈.md` | 辐射圈（POI 影响范围） |
| `弧线图.md` | 弧线（跨城路线视觉化好） |
| `轨迹图.md` | 轨迹动画（旅游路线播放） |
| `管道图.md` | 管道连线 |
| `区域图.md` | 多边形区域 |
| `围墙面.md` | 立体围墙 |
| `水晶体.md` | 立体水晶 |


## 目录结构

```
jsapi-guide/
├── README.md            本文档
├── jsapigl/
│   ├── docs/            核心 API 文档（上方 21 个 md）
│   └── demos/           核心 API 的 demo HTML
└── visualization/
    ├── docs/            可视化扩展库文档（上方 14 个 md）
    └── demos/           可视化扩展库的 demo HTML
```

## API Key

HTML 地图底图使用 client 解析到的 Key（tempkey / 环境变量 `TMAP_KEY` / `.env` 文件），在 `<script>` 标签中引用。生成 HTML 时将 `TMAP_KEY` 替换为实际解析到的 Key：

```html
<script src="https://map.qq.com/api/gljs?v=1&key={TMAP_KEY}"></script>
```

tempkey 生成的 Key 同时支持 JSAPI 底图加载和 WebService API 调用，放进 HTML `<head>` 即可显示底图。未配置 Key 时需先通过 tempkey 流程申请临时体验 Key。

> ⚠️ **安全提示**：将 Key 明文写在 HTML `<script src="...gljs?key=XXX">` 中，任何访问该页面的人都能通过查看源码或抓包拿到 Key，从而盗用你的额度。**仅在本地开发/内部预览场景可用**。若要将网页发布到公网，请务必改用下方「Key 安全 / 代理服务转发」方案。生成 HTML 后必须按 SKILL.md「HTML Key 安全检查」条目主动提示用户。

### HTML Key 安全检查 — 检测与提示

每次生成 / 写入含腾讯地图 JSAPI GL 的 HTML 后（识别标记：URL 含 `map.qq.com/api/gljs`），在同一轮内执行：

- **检测**：对文件内容执行正则 `gljs\?[^"']*[?&]key=[A-Z0-9-]{20,}`，判断是否含明文 Key。
- **命中时**：在最终回复中原样输出下方「固定安全提示文案」整段，逐字复制，不改写、翻译、精简、合并、拆分、加 emoji、调换顺序或省略。唯一允许的替换：将 `<HTML_FILE>` 替换为实际文件路径；命中多个文件则按行列出所有路径。
- **未命中时**：不输出安全提示，避免噪音。
- 不在未告知用户的情况下将带明文 Key 的 HTML 发布 / 部署到公网。

**固定安全提示文案（命中时原样输出，勿改动）：**

> ⚠️ **HTML Key 安全提示**：检测到 `<HTML_FILE>` 中包含明文 Key（形如 `gljs?...&key=...`），任何人可通过查看源码或抓包获取，存在盗用风险；当前形式仅限本地/内网使用，若需公网发布请参考官方代理方案：https://lbs.qq.com/webApi/javascriptGL/glGuide/glKeyDelegate 。

## Key 安全 / 代理服务转发

**官方文档**：https://lbs.qq.com/webApi/javascriptGL/glGuide/glKeyDelegate

将 Key 存到自有服务器，前端通过代理服务器请求腾讯 JSAPI，Key 完全不出现在 HTML 与网络请求中。核心两步：

### 1. 服务器端配置代理（以 Nginx 为例）

将下面配置里的 `XXXX-XXXX-XXXX-XXXX-XXXX-XXXX` 替换为你的正式 Key：

```nginx
server {
  listen 8080;
  server_name your.domain.com;   # 你的服务器域名或 IP

  location /_TMapService {
    set $args "$args&key=XXXX-XXXX-XXXX-XXXX-XXXX-XXXX";
    proxy_pass https://pr.map.qq.com/pingd?appid=jsapi_v3;
  }
  location /_TMapService/checkKey {
    set $args "$args&key=XXXX-XXXX-XXXX-XXXX-XXXX-XXXX";
    proxy_pass https://apikey.map.qq.com/mkey/index.php/mkey/check;
  }
  location /_TMapService/oversea {
    set $args "$args&apikey=XXXX-XXXX-XXXX-XXXX-XXXX-XXXX";
    proxy_pass https://overseactrl.map.qq.com;
  }
  location /_TMapService/service {
    set $args "$args&key=XXXX-XXXX-XXXX-XXXX-XXXX-XXXX";
    proxy_pass https://apis.map.qq.com/ws;
  }
}
```

### 2. 前端 HTML 改造（去掉明文 key）

在引入 JSAPI **之前**声明代理地址，`<script>` 引用去掉 `&key=` 参数：

```html
<!-- 必须写在 gljs <script> 之前 -->
<script>
  window._TMapSecurityConfig = {
    serviceHost: "https://your.domain.com/_TMapService"
  };
</script>
<!-- 注意：URL 不再包含 &key=... -->
<script src="https://map.qq.com/api/gljs?v=1"></script>
```

改造后，前端源码与网络请求都不再含 Key，达到防泄露目的。

### 地图样式

**使用系统默认样式即可，无需设置 `mapStyleId`**。若用户希望修改地图样式，可引导其前往腾讯位置服务官网登录账号，在控制台为对应 Key 配置样式后使用；下方样式表供已在控制台配置自定义样式的用户参考。

```js
const map = new TMap.Map('map', {
  center: new TMap.LatLng(39.9, 116.4), zoom: 12
  // 使用系统默认样式；如需自定义样式，在官网控制台为 Key 配置后再设置 mapStyleId
});
```

| styleId | 样式名称 | 说明 |
|---------|---------|------|
| style1 | 可视化官网黑光字 | 黑底 |
| style2 | 星渊 | 深蓝黑底 |
| style3 | 玉露 | 绿底 |
| style4 | 黑色极简 | 黑底 |
| style5 | 璃青 | 浅绿底 |
| style6 | 玄青 | 深灰黑底 |
| style7 | 浅色底图-可视化 | 浅灰白 |
| style8 | 白浅 | 白色 |
| style9 | 经典 | 标准 |

> 以上样式均需在官网控制台为 Key 配置后可用。tempkey 及未配置的正式 Key 使用系统默认样式，无需设置 `mapStyleId`。

## HTML 生成示例

地图能力使用 `TMap.Map` + `TMap.MultiMarker` + `TMap.MultiPolyline` + `TMap.InfoWindow`。把 POI 数据换成 client 返回的真实坐标即可：

```python
import os, json

# POI 数据（实际用 client 返回的坐标）
pois = [
    {"name": "象鼻山", "lat": 25.2675, "lng": 110.2966},
    {"name": "两江四湖", "lat": 25.2798, "lng": 110.2904},
    {"name": "靖江王府", "lat": 25.2858, "lng": 110.2992},
]
markers_js = json.dumps(
    [{"id": str(i), "position": [p["lat"], p["lng"]], "title": p["name"]} for i, p in enumerate(pois)],
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
  id: p.id, position: new TMap.LatLng(p.position[0], p.position[1]), properties: {{title: p.title}}
}})) }});
new TMap.MultiPolyline({{ map, geometries: [{{
  id: 'route', paths: pts.map(p => new TMap.LatLng(p.position[0], p.position[1]))
}}] }});
</script></body></html>'''

out = os.path.expanduser("~/Documents/itinerary_map.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(out)
```

旅游攻略类 HTML 还可把 `travel_guide` 返回的 `qr_path` 嵌入网页右下角浮窗（约 120×120）；POI 按天分色 + 数字角标 + polyline 连线。

## 画路线：polyline 解压

`direction` 返回腾讯路线接口原生响应（`result.routes`）。驾车/步行/骑行的 `routes[0].polyline` 是**压缩格式的一维数组**，画线前需解压成 `[lat,lng]` 点序列：前两个值是首点真实经纬度，其后每个值是相对前一点的差值（×1e6），逐项累加还原。

```python
def decode_polyline(coors):
    """腾讯压缩 polyline 一维数组 → [[lat,lng], ...]"""
    if not coors or len(coors) < 2:
        return []
    pts = [[coors[0], coors[1]]]
    for i in range(2, len(coors) - 1, 2):
        lat = pts[-1][0] + coors[i] / 1_000_000.0
        lng = pts[-1][1] + coors[i + 1] / 1_000_000.0
        pts.append([round(lat, 6), round(lng, 6)])
    return pts
```

解压后转成 `new TMap.LatLng(lat, lng)` 数组喂给 `MultiPolyline` 的 `paths`。

> 公交 `transit` 的 route 没有顶层 polyline，折线分散在 `steps` 各换乘段里（步行段的 `polyline` 字段、乘车段 `lines[0].polyline`），按需分别解压。
