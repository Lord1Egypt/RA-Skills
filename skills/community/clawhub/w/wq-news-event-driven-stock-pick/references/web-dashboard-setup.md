# Web Dashboard 架构与部署指南

## 两套部署环境

### 1. 本地开发环境 (Flask)

| 文件 | 位置 | 说明 |
|------|------|------|
| 前端页面 | `~/.hermes/output/event-driven-trader-dashboard.html` | 七层全链路分析面板 |
| Flask 后端 | `~/.hermes/output/app.py` | API 服务，端口 5566 |
| 分析引擎 | `~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py` | 千帆API调用 |

启动: `cd ~/.hermes/output && python3 app.py` → 访问 `http://localhost:5566`

### 2. 线上生产环境 (racingai.top/event-driven)

| 文件 | 位置 | 说明 |
|------|------|------|
| 前端页面 | `/var/www/event-driven/event-driven-trader-dashboard.html` | 同步自本地 |
| 后端服务 | `/var/www/event-driven/server.py` | 纯标准库HTTP服务（零依赖） |
| 分析引擎 | `/var/www/event-driven/news_analyzer.py` | 同步自本地 |
| systemd | `/etc/systemd/system/event-driven.service` | 开机自启+崩溃重启 |
| nginx | `/etc/nginx/conf.d/port_mapping.conf` | 路由配置 |

服务管理: `systemctl restart event-driven` / `systemctl status event-driven`

## 架构数据流

```
用户在浏览器输入新闻 -> 点击"开始分析"
  ↓
runAnalysis() 读取 #newsText -> fetch POST /api/analyze
  ↓
后端 (app.py 或 server.py) 接收 JSON -> subprocess 调用 news_analyzer.py -t "新闻" -m ernie-4.5-turbo-128k
  ↓
news_analyzer.py -> 百度千帆 API (ernie-4.5-turbo-128k, temperature=0.3, max_tokens=8192)
  ↓
返回结构化 JSON -> 后端透传给前端
  ↓
前端渲染函数更新 5 个区域：
  - renderMetrics(data)    -> 影响力面板（事件方向、受益标的数、利空板块数、置信度）
  - renderSectors(data)    -> 板块热力（affected_sectors -> 颜色编码利好/利空）
  - renderTargets(data)    -> 标的排序表（beneficiary_stocks -> 信号强度排序）
  - renderReport(data)     -> 分析报告 3 个 Tab（事件解读、产业链拆解、操作建议）
  - updatePipelineDesc(data) -> pipeline 步骤描述文字
```

## Nginx 路由配置 (ECS)

⚠️ **关键：必须用精确匹配 `location =`**，不能用前缀匹配 `location /api/`。
前缀匹配会拦截所有 `/api/` 请求（包括策略页面的 `/api/strategy/list` 等），导致 Go 后端 API 全部 404。

```nginx
server {
    listen 80;
    server_name racingai.top www.racingai.top;

    # 事件驱动交易台 - 页面
    location /event-driven {
        proxy_pass http://127.0.0.1:5566;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 事件驱动交易台 - 分析API (精确匹配！不能用 location /api/)
    location = /api/analyze {
        proxy_pass http://127.0.0.1:5566;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }

    # 事件驱动交易台 - 健康检查 (精确匹配)
    location = /api/health {
        proxy_pass http://127.0.0.1:5566;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 其他流量走 Vite dev server (其余 /api/ 由 Vite proxy 到 Go 后端 :8080)
    location / {
        proxy_pass http://127.0.0.1:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 三层路由架构

```
racingai.top (Nginx :80)
├── /event-driven          → Python http.server (:5566) → 独立HTML页面 或 React SPA页面
├── = /api/analyze          → Python http.server (:5566) → news_analyzer.py → 千帆API (精确匹配)
├── = /api/health           → Python http.server (:5566) → 健康检查 (精确匹配)
└── /                       → Vite dev server (:5173)    → React SPA (fintech应用)
                               └── /api/* → Vite proxy → Go backend (:8080) → 策略/持仓API
```

**为什么用精确匹配**：fintech React 应用的 axios `baseURL` 是 `/api`，策略页面会调用 `/api/strategy/list` 等接口。如果 nginx 用 `location /api/` 前缀匹配，这些请求会被错误路由到 Python 后端 (:5566) 而非通过 Vite proxy 到 Go 后端 (:8080)，导致策略页面全部 500/404。

## Systemd 服务配置 (ECS)

```ini
[Unit]
Description=Event-Driven Trader Backend
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /var/www/event-driven/server.py
WorkingDirectory=/var/www/event-driven
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## 千帆 API 返回的 JSON 结构

```json
{
  "event_type": "policy|earnings|industry|company|macro",
  "event_title": "事件标题",
  "event_summary": "事件摘要",
  "market_impact": {
    "direction": "利好|利空|中性",
    "duration": "短期情绪|中期趋势|长期逻辑",
    "intensity": "high|medium|low"
  },
  "affected_sectors": [
    {"sector": "板块名称", "impact": "利好|利空", "reason": "原因"}
  ],
  "beneficiary_stocks": [
    {"code": "600000", "name": "名称", "signal": "strong|medium|weak", "logic": "逻辑", "key_point": "关注要点"}
  ],
  "risk_factors": ["风险1", "风险2"],
  "signal_summary": "综合信号评级",
  "confidence": "high|medium|low",
  "disclaimer": "免责声明",
  "_meta": {"model": "...", "usage": {...}}
}
```

## 前端渲染函数说明

| 函数 | 目标区域 | 数据来源 |
|------|---------|---------|
| `renderMetrics(data)` | `#impact .metrics` | `market_impact`, `beneficiary_stocks`, `affected_sectors`, `confidence` |
| `renderSectors(data)` | `#sectors .sectors` | `affected_sectors[]` -> 颜色映射：利好=绿、利空=红、中性=黄 |
| `renderTargets(data)` | `#targets tbody` | `beneficiary_stocks[]` -> signal 映射到 badge 样式 |
| `renderReport(data)` | `#tab-event`, `#tab-chain`, `#tab-action` | 全量 JSON -> 3 个 Tab 面板 |
| `updatePipelineDesc(data)` | `.pipe-desc` 元素 | `event_title`, `beneficiary_stocks.length` |

## 同步更新流程

当本地 HTML 或 news_analyzer.py 有更新时，同步到 ECS：

```bash
# 复制更新文件
scp ~/.hermes/output/event-driven-trader-dashboard.html root@&lt;SERVER_IP&gt;:/var/www/event-driven/
scp ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py root@&lt;SERVER_IP&gt;:/var/www/event-driven/
# 重启服务（HTML 更新不需要重启，news_analyzer.py 更新也不需要，只有 server.py 更新才需要）
ssh root@&lt;SERVER_IP&gt; "systemctl restart event-driven"
```

## 常见问题

### 点击"开始分析"没反应

可能有三种原因：

**原因A - React SPA 中 handleAnalyze 是空壳**: fintech React 应用中的 `EventDrivenTrader.tsx` 组件，如果 `handleAnalyze()` 只调了 `message.success()` 弹 toast 而没有 `fetch('/api/analyze')`，点击按钮不会真正分析。必须改为 async 函数调用 API 并 `setResult(data)` 更新状态。

**原因B - 独立HTML页面 runAnalysis 是空壳**: `event-driven-trader-dashboard.html` 中的 `runAnalysis()` 如果只播放 pipeline 动画而不 fetch API，数据不会更新。必须调用 fetch 并用 renderMetrics/renderSectors/renderTargets/renderReport 渲染结果。

**原因C - 后端服务未运行**: 后端未运行时 fetch 失败。

排查步骤：
1. 确认服务运行中：本地 `python3 app.py` / 线上 `systemctl status event-driven`
2. `curl http://localhost:5566/api/health` 应返回 `{"status":"ok"}`
3. 线上：`curl http://racingai.top/api/health`
4. 测试分析接口：`curl -X POST http://racingai.top/api/analyze -H 'Content-Type: application/json' -d '{"text":"央行降准0.5个百分点"}'`
5. 浏览器 F12 控制台检查 fetch 请求是否发出、是否有 CORS 错误

### React SPA "事件驱动" Tab 需要刷新才能用

**原因**: `EventDrivenTrader` 组件被 `lazy(() => import(...))` 懒加载，依赖重型库 `echarts-for-react`，首次路由跳转时 chunk 加载和 ECharts 初始化不完整。

**修复**: 在 `router.tsx` 中将 `EventDrivenTrader` 从懒加载改为直接导入：
```tsx
// 错误（会导致需要刷新）：
const EventDrivenTrader = lazy(() => import('@/pages/EventDrivenTrader'))

// 正确（直接导入）：
import EventDrivenTrader from '@/pages/EventDrivenTrader'
```

### 策略页面 API 全部 500/404

**原因**: nginx 配置用了 `location /api/` 前缀匹配，拦截了所有 `/api/` 请求到 Python 后端 (:5566)，导致策略页面的 `/api/strategy/list` 等调用无法到达 Go 后端 (:8080)。

**修复**: 改用精确匹配 `location = /api/analyze` 和 `location = /api/health`，让其余 `/api/` 请求继续走 Vite proxy 到 Go 后端。

### Python 3.6 兼容性错误

ECS 服务器仅有 Python 3.6.8。如果 `server.py` 报错 `__init__() got an unexpected keyword argument 'capture_output'` 或 `'text'`：

- `capture_output=True` → 改用 `stdout=subprocess.PIPE, stderr=subprocess.PIPE`
- `text=True` → 改用手动 `.decode("utf-8")` 解码 bytes 输出
- 不要在 ECS 上 `pip install flask`（Flask 3.x 需 Python 3.9+），使用纯标准库的 `server.py`

### 分析超时

千帆 API 默认 120 秒超时。如果 GLM 等推理模型较慢，可增大 `subprocess.run` 的 `timeout` 参数，或在前端调用中增大 `--max-tokens`。

### 前端数据不更新

确认 `runAnalysis()` 中的 `fetch` 调用成功（resp.ok 为 true），且返回的 JSON 不含 `error` 字段。如果千帆 API 返回非 JSON 内容，`news_analyzer.py` 的 `extract_analysis()` 会返回 `{"error": "Failed to parse JSON..."}`。
