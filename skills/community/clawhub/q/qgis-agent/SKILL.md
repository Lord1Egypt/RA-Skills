---
name: qgis-agent
description: Drive QGIS's 1000+ Processing algorithms (vector geoprocessing, raster & terrain analysis, interpolation, network analysis, format conversion, map rendering) from any AI agent over plain HTTP. Architecture: Agent --HTTP--> scripts/server.py (PyQGIS) --> QGIS 3.28+/4.x. 驱动本机 QGIS 的 1000+ Processing 算法，让 AI 智能体通过纯 HTTP 直接执行空间分析。
---

# QGIS Agent

Drive the 1000+ Processing algorithms of the local QGIS installation (QGIS native / GDAL / GRASS / SAGA / 3D / point cloud), letting AI agents perform spatial analysis directly over plain HTTP.

Architecture: `this skill (Agent) --HTTP--> scripts/server.py (PyQGIS) --> QGIS 4.x`

## Prerequisites

- Windows 10/11 + **QGIS 3.28 or later** (free & open source, OSGeo4W standalone installer) — PyQGIS must run inside QGIS's bundled Python
- Server HTTP address: `http://127.0.0.1:8767` (localhost only)

## Step 1: Make sure the server is running

Probe whether the service is up:

```bash
curl -s http://127.0.0.1:8767/health
# {"status":"ok","server":"qgis-agent-server","version":"1.0","algorithms":1000,"providers":6,...}
```

If not running, start it in the background with QGIS's bundled Python:

```bash
"C:/Program Files/QGIS 4.0.3/bin/python-qgis.bat" "<skill-dir>/scripts/server.py" 8767
```

On Windows you can also run `scripts/start_server.bat` (auto-detects the QGIS install dir; Ctrl+C to stop).

## Step 2: Call the tools (plain HTTP, no MCP client needed)

The agent can call everything with curl:

```bash
# List all algorithm providers and their algorithm counts
curl -s http://127.0.0.1:8767/modules

# List all algorithms of one provider (e.g. QGIS native)
curl -s http://127.0.0.1:8767/module/qgis

# Search algorithms by keyword (always use this when unsure of the ID)
curl -s "http://127.0.0.1:8767/search?q=buffer"

# Get the full parameter signature of an algorithm (check before /call)
curl -s "http://127.0.0.1:8767/tool/native:buffer"

# Run an algorithm: POST /call  body = {"name": "algorithm-id", "arguments": {...}}
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:buffer","arguments":{"INPUT":"C:/data/roads.shp","DISTANCE":500,"OUTPUT":"C:/out/roads_buf.gpkg"}}'
```

Workflow: **/search to find the algorithm → /tool to check the signature → /call to run it.** Algorithm IDs are `provider:name`, e.g. `native:buffer`, `gdal:rasterize`, `grass:r.slope.aspect` (in QGIS 3.x the GRASS provider is named `grass7`).

## Provider cheat sheet (QGIS 4.0 measured values)

| provider | #algos (approx) | Purpose |
|---|---|---|
| native | 339 | vector geometry / overlay / analysis / selection / table ops, raster analysis, terrain analysis, interpolation, cartography |
| grass | 307 | hydrology, viewshed, cost paths, network allocation (provider is `grass` in QGIS 4, `grass7` in 3.x) |
| gdal | 59 | format conversion, reprojection (warp), raster tiling |
| qgis | 39 | reclassify, aspect, other raster-terrain / interpolation algorithms (partly duplicated in native) |
| pdal | 24 | point cloud (LiDAR) processing |
| 3d | 1 | TIN interpolation, DEM generation |

Actual counts are returned by `/modules` (they vary with installed plugins and versions).

## Key parameter conventions (important, learned the hard way)

- **Extent strings are ordered `xmin,xmax,ymin,ymax`** (the official QGIS Processing order), NOT minx,miny,maxx,maxy!
  Example: `"483000,513000,4407000,4437000 [EPSG:32650]"`. The server parses it and handles CRS conversion automatically.
- **Distance-like parameters (buffer radius, spacing, slope thresholds, etc.) are in meters** — the server forces the Distance unit to Meters, even when the CRS is geographic (degrees).
- Prefer `.gpkg` (GeoPackage) for outputs: single file, no non-ASCII path issues; pass `"TEMPORARY_OUTPUT"` to create a temporary layer.
- Enum parameters (TYPE, END_CAP_STYLE, ...) take integers; check `/tool/{algorithm-id}` descriptions for valid values.

## Project / rendering / code execution

```bash
# Inspect the current project and layers (field list, feature count, CRS)
curl -s http://127.0.0.1:8767/project

# Open / save a project
curl -s -X POST http://127.0.0.1:8767/project/open -H "Content-Type: application/json" -d '{"path":"C:/data/demo.qgz"}'
curl -s -X POST http://127.0.0.1:8767/project/save -H "Content-Type: application/json" -d '{"path":"C:/out/demo.qgz"}'

# Render the current project to PNG (layers & extent optional)
curl -s -X POST http://127.0.0.1:8767/render -H "Content-Type: application/json" \
  -d '{"output":"C:/out/map.png","width":1024,"height":768}'

# Execute arbitrary PyQGIS code (disabled by default; set PYQGIS_ENABLE_EXEC=1 at startup to enable)
curl -s -X POST http://127.0.0.1:8767/pyqgis -H "Content-Type: application/json" \
  -d '{"code":"print(QgsProject.instance().fileName())"}'
```

## Typical call chains (composite analysis)

Site-selection requests decompose naturally into buffer → overlay → filter chains, e.g.
hospital siting (within 500 m of major roads, slope < 5°):
1. `native:buffer` roads 500 m → 2. `native:slope` on the DEM → 3. `qgis:reclassifybytable` to binarize slope → 4. `native:intersection` to intersect

More examples (buffer, clip, field calculator, slope/aspect, interpolation, hotspots, rendering) in `references/examples.md`.

## Error handling

Errors return `{"status":"error","message":"...","suggestion":"..."}`. Common cases:
- `algorithm not found` → typo in the ID; use `/search?q=` to find the right one (the same algorithm may live under `native` or `qgis` depending on version)
- `path outside whitelist` → path not allowed; adjust `QGIS_ALLOWED_PATHS` or move the data
- parameter mismatch → verify names and types via `/tool/{algorithm-id}`
- invalid input data → make sure the file exists and the format is supported by OGR/GDAL

Results include `elapsed_sec`; vector outputs also carry `feature_count`, `geometry_type` and `size_mb`.

## Security & configuration

- The server listens on `127.0.0.1` only — never exposed to the LAN
- Path whitelist: unrestricted by default; set `QGIS_ALLOWED_PATHS` (semicolon-separated) to require all requested paths to live inside whitelisted directories
  `set QGIS_ALLOWED_PATHS=C:/GIS-AI-Course/;D:/data/`
- Arbitrary PyQGIS execution is disabled by default (`/pyqgis` returns 403); set `PYQGIS_ENABLE_EXEC=1` at startup to enable — trusted environments only
- Confirm target data with the user before destructive write operations (overwriting outputs)

---

# QGIS 智能体（中文说明）

驱动本机 QGIS 的 1000+ Processing 算法（QGIS 原生 / GDAL / GRASS / SAGA / 3D / 点云），让 AI 直接用自然语言完成空间分析。

架构：`本技能(Agent) --HTTP--> scripts/server.py (PyQGIS) --> QGIS 4.x`

## 前置条件

- Windows 10/11 + **QGIS 3.28 及以上**（免费开源，OSGeo4W 独立安装包）——PyQGIS 需在 QGIS 自带 Python 中运行
- 服务端 HTTP 地址：`http://127.0.0.1:8767`（仅本机监听）

## 第一步：确保服务在运行

先探测服务是否已启动：

```bash
curl -s http://127.0.0.1:8767/health
# {"status":"ok","server":"qgis-agent-server","version":"1.0","algorithms":1000,"providers":6,...}
```

若未启动，后台启动服务（用 QGIS 自带 Python）：

```bash
"C:/Program Files/QGIS 4.0.3/bin/python-qgis.bat" "<本技能目录>/scripts/server.py" 8767
```

Windows 下也可运行 `scripts/start_server.bat`（自动探测 QGIS 安装目录，Ctrl+C 停止）。

## 第二步：调用工具（纯 HTTP，无需 MCP 客户端）

智能体直接用 curl 调用即可：

```bash
# 列出全部算法提供器（provider）及算法数量
curl -s http://127.0.0.1:8767/modules

# 列出某个提供器的全部算法（如 QGIS 原生算法）
curl -s http://127.0.0.1:8767/module/qgis

# 按关键词搜索算法（不确定算法 ID 时必用）
curl -s "http://127.0.0.1:8767/search?q=buffer"

# 查看算法完整参数签名（写 /call 前先查）
curl -s "http://127.0.0.1:8767/tool/native:buffer"

# 执行算法：POST /call  body = {"name": "算法ID", "arguments": {...}}
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:buffer","arguments":{"INPUT":"C:/data/roads.shp","DISTANCE":500,"OUTPUT":"C:/out/roads_buf.gpkg"}}'
```

调用流程：**/search 找算法 → /tool 查签名 → /call 执行**。算法 ID 格式为 `provider:算法名`，如 `native:buffer`、`gdal:rasterize`、`grass:r.slope.aspect`（QGIS 3.x 中 GRASS 提供器名为 grass7）。

## 模块速查（provider，QGIS 4.0 实测值）

| provider | 算法数(约) | 用途 |
|---|---|---|
| native | 339 | 矢量几何/叠加/分析/筛选/建表、栅格分析、地形分析、插值、制图 |
| grass | 307 | 水文分析、视域、成本路径、网络分配（QGIS 4 中 provider 名为 grass，3.x 为 grass7）|
| gdal | 59 | 格式转换、投影变换（warp）、栅格切片 |
| qgis | 39 | 重分类、坡向等栅格地形 / 插值算法（部分与 native 重复）|
| pdal | 24 | 点云（LiDAR）处理 |
| 3d | 1 | TIN 插值、DEM 生成 |

实际数量以 `/modules` 返回为准（随安装的插件与版本变化）。

## 关键参数约定（重要，实测踩坑）

- **范围（Extent）字符串顺序是 `xmin,xmax,ymin,ymax`**（QGIS Processing 官方顺序），不是 minx,miny,maxx,maxy！
  例：`"483000,513000,4407000,4437000 [EPSG:32650]"`。服务端会自动解析并做 CRS 转换。
- **距离类参数（缓冲半径、间距、坡度阈值等）单位为米**——服务端已强制 Distance 单位为 Meters，即使 CRS 是经纬度也按米解释。
- 输出格式推荐 `.gpkg`（GeoPackage，单文件、无中文路径问题）；传 `"TEMPORARY_OUTPUT"` 生成临时图层。
- 枚举参数（如 TYPE、END_CAP_STYLE）传整数，具体取值查 `/tool/{算法ID}` 的 description。

## 工程 / 渲染 / 代码执行

```bash
# 查看当前工程与图层（含字段列表、要素数、CRS）
curl -s http://127.0.0.1:8767/project

# 打开 / 保存工程
curl -s -X POST http://127.0.0.1:8767/project/open -H "Content-Type: application/json" -d '{"path":"C:/data/demo.qgz"}'
curl -s -X POST http://127.0.0.1:8767/project/save -H "Content-Type: application/json" -d '{"path":"C:/out/demo.qgz"}'

# 渲染当前工程为 PNG（可指定图层与范围）
curl -s -X POST http://127.0.0.1:8767/render -H "Content-Type: application/json" \
  -d '{"output":"C:/out/map.png","width":1024,"height":768}'

# 执行任意 PyQGIS 代码（默认关闭，启动时设 PYQGIS_ENABLE_EXEC=1 开启）
curl -s -X POST http://127.0.0.1:8767/pyqgis -H "Content-Type: application/json" \
  -d '{"code":"print(QgsProject.instance().fileName())"}'
```

## 典型调用链（复合分析）

选址类需求按"缓冲区→叠加→筛选"链条自动拆解为多次 /call，例：
医院选址（距主干道 500m 内、坡度 < 5°）：
1. `native:buffer` 道路 500m → 2. `native:slope` DEM 求坡度 → 3. `qgis:reclassifybytable` 坡度二值化 → 4. `native:intersection` 叠加取交集

更多示例（缓冲区、裁剪、字段计算、坡度坡向、插值、热点分析、渲染出图等）见 `references/examples.md`。

## 错误处理

返回 `{"status":"error","message":"...","suggestion":"..."}`，常见情形：
- `algorithm not found` → 算法 ID 拼写错误，用 `/search?q=` 找正确 ID（同一算法在不同版本中可能挂在 native 或 qgis 下）
- `path outside whitelist` → 路径不在白名单，调整 `QGIS_ALLOWED_PATHS` 或换目录
- 参数不匹配 → 用 `/tool/{算法ID}` 核对参数名与类型
- 输入数据无效 → 确认文件路径存在、格式受 OGR/GDAL 支持

结果中 `elapsed_sec` 含执行耗时；输出为矢量数据时 `result` 内会带 `feature_count`、`geometry_type`、`size_mb`。

## 安全与配置

- 服务只监听 `127.0.0.1`，不会暴露到局域网
- 路径白名单：默认不限制；设置环境变量 `QGIS_ALLOWED_PATHS`（分号分隔多个路径）后，所有请求中的文件路径必须位于白名单目录内
  `set QGIS_ALLOWED_PATHS=C:/GIS-AI-Course/;D:/data/`
- PyQGIS 任意代码执行默认关闭（`/pyqgis` 返回 403），启动时设 `PYQGIS_ENABLE_EXEC=1` 才开启；仅在可信环境使用
- 谨慎执行写操作（覆盖输出）前，向用户确认目标数据
