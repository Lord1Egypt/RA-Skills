# QGIS Agent 🗺️🤖

把 **QGIS** 变成 AI 智能体的 GIS 引擎：通过简洁的 HTTP API，让任何智能体（WorkBuddy、Claude、Cursor、Coze、Dify……）用自然语言驱动 QGIS 的 **1000+ 空间分析算法**——矢量地理处理、栅格与地形分析、插值、网络分析、格式转换、渲染出图，一站式完成。

> 开源免费（MIT）。QGIS 本身就是免费开源软件，本项目的全部能力零许可成本。

## 架构

```
┌──────────────┐   HTTP(127.0.0.1:8767)   ┌─────────────────────┐   PyQGIS    ┌───────────┐
│ AI 智能体     │ ────────────────────────▶ │ scripts/server.py   │ ──────────▶ │ QGIS 4.x  │
│ (SKILL.md)   │ ◀──────────────────────── │ (QGIS 自带 Python)   │ ◀────────── │ Processing│
└──────────────┘        JSON               └─────────────────────┘             └───────────┘
```

核心设计：**不硬编码工具清单**。服务端接入 QGIS Processing 框架注册表，自动暴露当前安装的全部算法提供器与算法（QGIS 原生 300+、GDAL 70+、GRASS 80+、SAGA 400+、3D、点云……），并支持 `发现 → 查签名 → 执行` 的三步调用模式，版本升级算法自动跟随。

## 快速开始

### 1. 安装 QGIS（已装可跳过）

下载 OSGeo4W 独立安装包：https://qgis.org/download/ （支持 QGIS 3.28+ / 4.x）

### 2. 启动服务端

```bat
git clone https://github.com/<你的用户名>/qgis-agent.git
cd qgis-agent\scripts
start_server.bat
```

看到如下输出即启动成功：

```
QGISAgent Server v1.0  |  QGIS 4.0.3
监听: http://127.0.0.1:8767   算法总数: 1013
```

### 3. 接入你的智能体

**WorkBuddy / Claude 等基于技能的智能体**：把本仓库根目录的 `SKILL.md` 安装为技能。

- WorkBuddy：将整个仓库文件夹复制到 `~/.workbuddy/skills/qgis-agent/`
- 其他智能体：把 `SKILL.md` 的内容粘贴为系统提示词/技能文档即可

**任意能发 HTTP 请求的智能体**：无需任何客户端，直接 curl：

```bash
curl -s http://127.0.0.1:8767/health
curl -s "http://127.0.0.1:8767/search?q=buffer"
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:buffer","arguments":{"INPUT":"C:/data/roads.shp","DISTANCE":500,"OUTPUT":"C:/out/roads_buf.gpkg"}}'
```

## API 一览

| 方法 | 端点 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查（算法总数、当前工程）|
| GET | `/modules` | 全部算法提供器及数量 |
| GET | `/module/{provider}` | 某提供器下全部算法 |
| GET | `/search?q=关键词` | 按关键词搜索算法 |
| GET | `/tool/{algorithm_id}` | 算法完整参数签名 |
| POST | `/call` | 执行算法 `{"name","arguments"}` |
| GET | `/project` / `/layers` | 工程与图层信息 |
| POST | `/project/open` `/project/save` | 打开/保存 `.qgz` 工程 |
| POST | `/render` | 渲染当前工程为 PNG |
| POST | `/pyqgis` | 执行任意 PyQGIS 代码（默认关闭）|

## 示例：一句话完成选址分析

对智能体说：

> "帮我在 D:/data 里做工厂选址：距高速公路 2km 以外、坡度小于 8°、只在 A 区范围内，结果保存为 GeoPackage 并渲染预览图。"

智能体会自动拆解为算法链依次调用：`native:buffer` → `qgis:slope` → `qgis:reclassifybytable` → `qgis:pixelstopolygons` → `native:difference` → `native:clip` → `/render`。

更多调用示例见 [references/examples.md](references/examples.md)。

## 安全

- 服务仅监听 `127.0.0.1`，不暴露局域网
- 环境变量 `QGIS_ALLOWED_PATHS`（分号分隔）可限制可读写的目录白名单
- 环境变量 `PYQGIS_ENABLE_EXEC=1` 才会开启 `/pyqgis` 任意代码执行（默认关闭）
- 写操作（覆盖输出文件）建议智能体在执行前向用户确认

## 目录结构

```
qgis-agent/
├── SKILL.md               # 智能体技能定义（接入即用）
├── scripts/
│   ├── server.py          # PyQGIS HTTP 服务端
│   └── start_server.bat   # Windows 一键启动（自动探测 QGIS）
├── references/
│   └── examples.md        # 各类算法调用示例集
├── configs/
│   └── api.md             # API 详细说明
├── LICENSE
└── README.md
```

## 与其他 QGIS MCP 项目的区别

| | QGIS Agent（本项目）| 典型 QGIS MCP 插件方案 |
|---|---|---|
| 是否需要在 QGIS 中安装插件 | ❌ 不需要（无 GUI 独立运行）| ✅ 需要 |
| 协议 | 纯 HTTP + JSON，任何智能体零依赖接入 | 需 MCP 客户端 + Node/uv 运行时 |
| 算法暴露 | 动态接入 Processing 全部提供器（1000+）| 通常预定义 50~100 个工具 |
| 参考架构 | 与 [ArcGIS Agent 模式]一致 | — |

## License

MIT
