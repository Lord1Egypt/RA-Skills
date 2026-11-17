---
name: wq-news-event-driven-stock-pick
description: "新闻流事件驱动选股系统 - 接收财经新闻输入，通过百度千帆API进行事件NLP分析，关联受益A股标的，输出事件驱动选股信号。"
version: 1.0.0
author: Racing Quant AI
license: MIT
metadata:
  hermes:
    tags: [quant, finance, news, event-driven, stock-picking, a-share]
---

# 新闻流事件驱动选股系统

当用户在飞书群中发送财经新闻或政策信息时，自动触发事件驱动选股分析流程。

## 触发条件

- 用户在"新闻流事件驱动选股"群中发送任何包含财经/政策/行业/公司信息的文本
- 用户明确要求分析某条新闻
- 用户粘贴的新闻链接或新闻摘要

## 分析流程

### 1. 调用千帆API分析引擎

使用百度千帆 API 进行深度新闻分析，执行以下脚本：

```bash
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py
```

将新闻文本通过 `-t` 参数传入脚本（推荐方式）：

```bash
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py -t "新闻内容..."
```

也可通过 stdin 传入（注意需设置足够超时）：

```bash
echo '新闻内容...' | python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py
```

指定模型（可选，默认 ernie-4.5-turbo-128k）：

```bash
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py -t "新闻内容..." -m ernie-4.5-turbo-128k
```

⚠️ 注意：GLM-5.2 模型有推理模式，需要较大 max_tokens（建议 16384+）且耗时较长。默认使用 ERNIE-4.5-Turbo-128K 更快更稳定。使用 GLM 时请显式指定：

```bash
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py -t "新闻内容..." -m glm-5.2 --max-tokens 16384
```

### 2. 脚本输出

脚本返回结构化的 JSON 分析结果，包含：
- `event_type`: 事件类型 (policy/earnings/industry/company/macro)
- `event_summary`: 事件摘要
- `affected_sectors`: 受影响板块列表
- `beneficiary_stocks`: 受益标的列表（含股票代码、名称、受益逻辑、信号强度）
- `risk_factors`: 风险提示
- `signal_summary`: 综合信号评级

### 3. 格式化输出

将脚本返回的 JSON 结果格式化为易读的 Markdown 报告，发送给用户。

输出模板见 `templates/output_template.md`。

## 事件分类体系

详见 `references/event_taxonomy.md`。

| 类型 | 代号 | 示例 |
|------|------|------|
| 政策类 | policy | 降准降息、产业政策、监管新规 |
| 财报类 | earnings | 业绩超预期/不及预期、预告修正 |
| 行业类 | industry | 供需变化、价格异动、技术突破 |
| 公司类 | company | 并购重组、股权变动、高管变更 |
| 宏观类 | macro | GDP/CPI/PMI数据、国际经贸 |

## 信号强度评级

| 等级 | 代号 | 标准 |
|------|------|------|
| 强信号 | strong | 直接受益，主营业务收入占比>30% |
| 中信号 | medium | 间接受益，供应链/上下游关联 |
| 弱信号 | weak | 情绪面受益，概念相关性 |

## 降级机制

- 如果千帆API不可用，使用当前模型直接进行内联分析
- 如果无法匹配具体标的，输出板块方向判断
- 始终标注数据来源和分析置信度

## Web Dashboard (事件驱动交易台)

系统包含一个可视化 Web 前端页面，位于 `~/.hermes/output/event-driven-trader-dashboard.html`。

### 架构

```
浏览器 (HTML+JS)  ──fetch──>  Flask 后端 (app.py, :5566)  ──subprocess──>  news_analyzer.py  ──>  千帆API
     ↑                              |
     └─── JSON 渲染到各区域 ────────┘
```

- **前端**: `~/.hermes/output/event-driven-trader-dashboard.html` — 七层全链路分析面板（新闻输入、分析流水线、影响力面板、板块热力、标的排序、共振矩阵、分析报告）
- **后端**: `~/.hermes/output/app.py` — Flask 服务，端口 5566，提供 `POST /api/analyze` 接口
- **分析引擎**: `scripts/news_analyzer.py` — 调用百度千帆 API 返回结构化 JSON

### 本地开发环境

```bash
cd ~/.hermes/output && python3 app.py
# 访问 http://localhost:5566
```

### 线上生产部署 (racingai.top/event-driven)

Dashboard 已部署在 ECS 服务器 (&lt;SERVER_IP&gt;) 上，地址：`http://racingai.top/event-driven`

**ECS 部署架构**：

```
Nginx (:80)
  ├── /event-driven      -> Python http.server (:5566) -> 返回HTML或React SPA页面
  ├── = /api/analyze     -> Python http.server (:5566) -> 调用 news_analyzer.py -> 千帆API (精确匹配)
  ├── = /api/health      -> Python http.server (:5566) -> 健康检查 (精确匹配)
  └── /                  -> Vite dev server (:5173, fintech React应用) -> /api 由 Vite proxy 到 Go 后端 (:8080)
```

⚠️ **nginx 路由必须用精确匹配** `location = /api/analyze`，不能用前缀匹配 `location /api/`。前缀匹配会拦截所有 `/api/` 请求（包括策略页面的 `/api/strategy/list` 等），导致 Go 后端 API 调用全部断裂。

**ECS 文件清单**：

| 文件 | 路径 | 说明 |
|------|------|------|
| 前端页面 | `/var/www/event-driven/event-driven-trader-dashboard.html` | 同步自本地 |
| 后端服务 | `/var/www/event-driven/server.py` | 纯标准库HTTP服务（零依赖），**仅部署于 ECS，不随技能分发** |
| 分析引擎 | `/var/www/event-driven/news_analyzer.py` | 同步自本地 |
| systemd | `/etc/systemd/system/event-driven.service` | 开机自启+崩溃重启 |
| nginx | `/etc/nginx/conf.d/port_mapping.conf` | 路由配置 |

**⚠️ 关键：ECS 服务器 Python 版本为 3.6.8**

ECS 上无法使用 Flask（需 Python 3.9+），因此线上后端使用纯 `http.server` 标准库实现（`server.py`），零外部依赖。

**Python 3.6 兼容性陷阱**：
- `subprocess.run(capture_output=True)` → 3.7+ 才支持，改用 `stdout=subprocess.PIPE, stderr=subprocess.PIPE`
- `subprocess.run(text=True)` → 3.7+ 才支持，改用手动 `.decode("utf-8")`
- ECS 上不要 `pip install flask`，直接用 `server.py`（已处理兼容性）

**同步更新到 ECS**：

```bash
# 复制文件到ECS
scp ~/.hermes/output/event-driven-trader-dashboard.html root@&lt;SERVER_IP&gt;:/var/www/event-driven/
scp ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py root@&lt;SERVER_IP&gt;:/var/www/event-driven/
# 重启服务
ssh root@&lt;SERVER_IP&gt; "systemctl restart event-driven"
```

详细部署文档见 `references/web-dashboard-setup.md`。

### API 接口

- `POST /api/analyze` - body: `{"text": "新闻内容", "model": "ernie-4.5-turbo-128k"}`，返回 `news_analyzer.py` 的 JSON 分析结果
- `GET /api/health` - 健康检查

### ⚠️ 关键陷阱

1. **静态页陷阱**: HTML 文件本身是纯静态展示页，初始数据为硬编码的碳达峰示例。`runAnalysis()` 必须通过 `fetch` 调用后端 API 并用 `renderMetrics/renderSectors/renderTargets/renderReport` 四个函数动态渲染结果。如果只播放 pipeline 动画而不更新数据，用户会认为"点击没反应"。

2. **Python 3.6 陷阱**: ECS 服务器仅有 Python 3.6.8，`subprocess.run` 不支持 `capture_output=True` 和 `text=True` 参数（3.7+ 才有）。线上 `server.py` 已用 `stdout=subprocess.PIPE` + 手动 `.decode("utf-8")` 规避。

3. **后端必须运行**: 无论本地（Flask app.py）还是线上（server.py），后端服务必须在运行中，否则前端 fetch 失败会弹出错误提示。

## React SPA 集成 (racingai.top 主站)

事件驱动交易台不仅作为独立 HTML 页面运行，还集成在 racingai.top 的 React SPA（fintech 应用）中，用户通过顶部导航栏 "事件驱动" Tab 访问。

### 前端组件

- **组件路径** (ECS): `&lt;APP_DIR&gt;/fintech/my-app/src/pages/EventDrivenTrader.tsx`
- **路由路径**: `/event-driven`（在 `src/constants/index.ts` 定义，`src/app/router.tsx` 注册）
- **技术栈**: React 19 + Ant Design 5 + ECharts 5 (echarts-for-react)
- **运行模式**: Vite dev server (:5173)，HMR 热更新

### React 端关键陷阱

1. **懒加载 + ECharts = 需要刷新才能用 (终极修复)**: `EventDrivenTrader` 原本用 `lazy()` 懒加载，首次路由跳转时 ECharts 初始化不完整。尝试在 `router.tsx` 中改为直接 `import` 仍然不够——**最终修复方案是在 `NavBar.tsx` 中对"事件驱动"按钮使用 `window.location.href = '/event-driven'` 全页跳转**，而非 React Router 的 `navigate()`。这样点击直接加载独立 HTML 页面（Python 后端 :5566 提供），完全绕过 React SPA 的客户端路由问题。NavBar.tsx 中用 `external: true` 标记此类链接，`handleClick` 中判断后用 `window.location.href` 而非 `navigate()`。

2. **handleAnalyze 必须真正调 API**: 组件初始版本的 `handleAnalyze()` 只调了 `message.success('分析已启动...')` 弹 toast，没有实际调用后端。必须改为 `async` 函数，通过 `fetch('/api/analyze')` 调用后端并 `setResult(data)` 更新状态，然后用 `result` 状态驱动所有区域渲染。

3. **nginx 精确匹配**: React SPA 中的 axios 实例 `baseURL` 为 `/api`，策略页面的 `/api/strategy/list` 等请求通过 Vite proxy 走 Go 后端 (:8080)。如果 nginx 用 `location /api/` 前缀匹配拦截，会把这些请求也送到 Python 后端 (:5566) 导致全部 404。必须用 `location = /api/analyze` 精确匹配。

### 同步 React 组件到 ECS

```bash
# 上传组件到ECS (Vite HMR 会自动热更新)
scp EventDrivenTrader.tsx root@&lt;SERVER_IP&gt;:&lt;APP_DIR&gt;/fintech/my-app/src/pages/
scp router.tsx root@&lt;SERVER_IP&gt;:&lt;APP_DIR&gt;/fintech/my-app/src/app/
# 如果 HMR 未完全生效（如结构性改动），重启前端服务
ssh root@&lt;SERVER_IP&gt; "systemctl restart fintech-frontend"
```

详细部署文档见 `references/web-dashboard-setup.md`。

- 分析结果仅供参考，不构成投资建议
- 需要结合市场环境、估值水平综合判断
- 事件驱动策略适合短期交易，需注意时效性
