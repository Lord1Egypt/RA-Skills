# Star Search v20.17 — 公网 HTTPS + 16 引擎 + LLM 答案 + PWA + 用户系统 + 多模态 + Deep Research

> **免费中文搜索引擎 + LLM 答案层 + 多模态 OCR + Deep Research**。16 引擎混动 + 5 RSS + 11 模式 + 4 MCP tools + 22 端点 + PWA iOS/Android/Windows/macOS。公网 `https://search.token-star.cn` OpenAI 兼容 API + SSE 流式 + Prometheus 监控。实战 35-58 (24 个版本, 6/12-6/16 5 天完成) 从 v17.2 升级到 v20.17。

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue) ![License MIT-0](https://img.shields.io/badge/license-MIT--0-green) ![v20.17](https://img.shields.io/badge/version-20.17-brightgreen) ![24+ releases](https://img.shields.io/badge/实战_35--58-24_releases-orange)

---

## 🎯 v20 重大升级（2026-06-12 → 2026-06-16, 5 天 24 个版本）

| 升级 | 价值 |
|------|------|
| **🎯 LLM 答案层** (实战 35-39) | 6s → 0.2s 235x speedup, SSE 流式首字 1s, 多轮对话 history 注入, 4 类 Prompt 模板 (finance/tech/news/general) |
| **🛡️ 终极稳定性** (实战 32-40) | 杀 watchdog, systemd user 守护, 监控告警 service, Prometheus + Grafana 公网 HTTPS |
| **🎓 学术/代码检索** (实战 41+47) | scholar/semantic_scholar/Sourcegraph/grep_app 4 引擎, Sourcegraph 已修 4 bug 真能用 |
| **📊 结构化输出 4 格式** (实战 42+56) | default markdown / table 表格 / mermaid 流程图 / json 代码块 (前端 marked+mermaid 渲染) |
| **📱 PWA 渐进式 Web App** (实战 53) | 4 平台通用 (iOS/Android/Windows/macOS) 一键安装到主屏, 0 审核 0 费用 |
| **🔐 用户系统** (实战 55) | 手机号+密码注册/登录, HMAC token 12h, quota 100/天 free, 4 端点 |
| **🎨 Mermaid/Table 前端渲染** (实战 56) | marked@9.1.6 + mermaid@10.9.1, 4 fmt 端到端 |
| **📷 多模态 OCR** (实战 57) | tesseract-4.1.1 + chi_sim+eng, 2 端点 /v1/multimodal/{search,health} |
| **🧠 Deep Research** (实战 58) | 3 步: 主 search + LLM 拆 3 子问题 + 3 子 search + LLM 综合 (200+ 字 + 4 关键点 + 14 引文, ~45s) |
| **🔌 Plugins 商店** (实战 52) | OpenAPI 3.0 + ai-plugin.json + mcp-server.json 3 manifest, GPT Actions / Claude MCP / Cursor 通用 |
| **🔍 语义搜索** (实战 50) | BM25 + 字符 n-gram 中文友好 + 5ms 检索 + 内存索引 |
| **💡 Perplexity 探索发现** (实战 51) | 3 mode: timeline 时间线 / comparison 多角度对比 / related 相关问题深挖 |
| **🌍 i18n 英文版** (实战 49) | SKILL_EN.md 22KB / 完整翻译 v20.7 全部能力 |
| **📈 监控系统** (实战 44-46) | /metrics Prometheus 端点 + Grafana 公网 HTTPS + 告警 service |

### 公网端点（已上线）

```bash
# 健康检查
curl https://search.token-star.cn/v1/health

# 主搜索 + LLM 答案
curl -X POST https://search.token-star.cn/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"比亚迪股价","answer":true,"top":3}'

# 流式 SSE
curl -X POST https://search.token-star.cn/v1/search/stream \
  -H "Content-Type: application/json" \
  -d '{"query":"LLM 推理 优化","answer":true}'

# 学术搜索
curl -X POST https://search.token-star.cn/v1/scholar \
  -H "Content-Type: application/json" \
  -d '{"query":"transformer attention","num":5}'

# 代码搜索
curl -X POST https://search.token-star.cn/v1/code \
  -H "Content-Type: application/json" \
  -d '{"query":"python async example","lang":"python"}'

# 语义搜索 (BM25)
curl -X POST https://search.token-star.cn/v1/semantic_search \
  -H "Content-Type: application/json" \
  -d '{"query":"fastapi tutorial","top":3}'

# Perplexity 探索发现 (timeline/comparison/related)
curl -X POST https://search.token-star.cn/v1/discover \
  -H "Content-Type: application/json" \
  -d '{"query":"Python 教程","mode":"timeline","num_results":4}'

# Deep Research
curl -X POST https://search.token-star.cn/v1/deep_research \
  -H "Content-Type: application/json" \
  -d '{"query":"Python 3.13 vs 3.14 性能对比"}'

# 用户注册
curl -X POST https://search.token-star.cn/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138000","password":"abc123"}'

# 多模态 OCR (multipart)
curl -X POST https://search.token-star.cn/v1/multimodal/search \
  -F "file=@screenshot.png" -F "text=context"
```

---

## 🔌 LLM 工具友好（4 大平台集成）

### Claude Desktop (MCP SSE)
```json
// ~/.config/claude/config.json
{
  "mcpServers": {
    "star-search": {
      "url": "https://search.token-star.cn/mcp/sse"
    }
  }
}
```

### OpenAI GPT Actions
Schema URL: `https://search.token-star.cn/.well-known/openapi.yaml`

### Anthropic Claude Plugins
Manifest: `https://search.token-star.cn/.well-known/mcp-server.json`

### Cursor / Cline
```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "star-search": {
      "command": "/usr/bin/python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

**4 MCP tools**:
- `web_search` - 多引擎搜索 (16 引擎)
- `web_search_news` - 科技/AI/产品新闻 (5 RSS + csdn/cnblogs)
- `web_search_finance` - A 股/股票/财经
- `get_engines` - 列引擎 + 模式

---

## 📊 16 引擎 + 11 模式

| 类别 | 引擎数 | 模式 |
|---|---|---|
| **HTTP (11)** | sogou / bing_cn / bing_http / github_issues / toutiao / zhihu / weixin / csdn / cnblogs / eastmoney / cls / tencent_cloud / sina_finance / sohu | deep / quick / dev / news / global / policy / stock |
| **RSS (5)** | rss_ithome / rss_36kr / rss_sspai / rss_oschina / rss_woshipm | tech_news / dev_rss / policy / global / weixin_agg |
| **学术 (4)** | scholar / semantic_scholar / Sourcegraph / grep_app | /v1/scholar, /v1/code |

**智能路由**：
- 中文 query → 5 引擎并发 (deep)
- 英文 query → bing_http (global)
- 财经 query → finance mode (eastmoney + cls + sina_finance)
- 时效过滤 → recency (day/week/month/year)

---

## 💪 22 端点 API 速查

| 端点 | 方法 | 说明 |
|---|---|---|
| `/v1/search` | POST | 主搜索 + 可选 LLM 答案 |
| `/v1/search/refresh` | POST | 强制刷新 (绕过缓存) |
| `/v1/search/stream` | POST | SSE 流式 (首字 1s) |
| `/v1/answer` | POST | 自定义 results → LLM 答案 |
| `/v1/scholar` | POST | 学术搜索 (4 引擎) |
| `/v1/code` | POST | 代码搜索 (Sourcegraph/grep_app) |
| `/v1/semantic_search` | POST | BM25 语义搜索 (5ms) |
| `/v1/discover` | POST | Perplexity 探索 (timeline/comparison/related) |
| `/v1/deep_research` | POST | 3 步深度研究 (45s) |
| `/v1/auth/{register,login,me,quota}` | POST/GET | 用户系统 4 端点 |
| `/v1/multimodal/{search,health}` | POST/GET | 多模态 OCR 2 端点 |
| `/v1/engines` | GET | 列 16 引擎 |
| `/v1/modes` | GET | 列 11 模式 |
| `/v1/health` | GET | 健康检查 |
| `/v1/metrics` | GET | Prometheus 指标 |
| `/mcp/sse` | GET | MCP server SSE 端点 |

**Plus**: `/.well-known/openapi.yaml`, `/.well-known/ai-plugin.json`, `/.well-known/mcp-server.json` (3 plugins manifest)

---

## 🎓 学术/代码检索

**4 引擎**：
- `scholar` (Google Scholar) - GFW 受限
- `semantic_scholar` - 需 API key (代码就位)
- `Sourcegraph` - **真能用** (实战 47 修复 4 bug)
- `grep_app` - 限流 (无 key 模式)

**端点**：
- `POST /v1/scholar` - 学术论文搜索
- `POST /v1/code` - 代码搜索 (支持 `lang: python`)

---

## 🧠 Deep Research (实战 58)

**3 步流程 (~45s)**:
1. **主 search** (5 results) - 0.5s
2. **LLM 拆 3 子问题** + 3 子 search - 7.4s
3. **LLM 综合** (200+ 字 + 4 关键点 + 14 引文) - 14.3s

**测试**: `Python 3.13 vs 3.14 性能对比` → 自动拆 3 子问题 → 综合报告含 [N] 引用

---

## 🎨 PWA + 移动优化 (实战 53+54)

**0 审核 0 费用 4 平台通用**:
- iOS Safari → 分享 → 添加主屏
- Android Chrome → 自动弹"安装"
- Windows Chrome/Edge → PWA 安装向导
- macOS Safari 17+ → 添加主屏

**4 文件**:
- `manifest.webmanifest` (1.4KB)
- `service-worker.js` (2.5KB, 离线缓存)
- `icon-192.png` + `icon-512.png` (Python 手写 zlib)
- 9 个 PWA meta tags

**移动优化 9 改**:
- viewport viewport-fit=cover (iOS 刘海屏)
- input type=search + inputmode=search (iOS 搜索键)
- iOS safe-area-inset (4 边)
- tap highlight 禁用
- touch-action: manipulation (无 300ms 延迟)
- 响应式字号 (768/480 断点)

---

## 🔐 用户系统 (实战 55)

**4 端点**:
- `POST /v1/auth/register` {phone, password, email}
- `POST /v1/auth/login` {phone, password}
- `GET /v1/auth/me?token=...`
- `GET /v1/auth/quota?token=...`

**3 Tier Quota**:
- `free` (免费): 100/天
- `basic` (基础): 1000/月
- `pro` (Pro): 10000/年

**Authorization Bearer** 自动注入 `/v1/search` quota check

---

## 🛠️ 技术架构

```
star-search v20.17
├── search.py (16 引擎 + 11 模式 + 智能路由)
├── answer.py (GLM-4-Flash 答案层 + 4 类 Prompt + 30min 缓存)
├── academic_code.py (4 学术/代码引擎 + Sourcegraph 修复)
├── semantic_search.py (BM25 + 字符 n-gram 中文友好)
├── discover.py (Perplexity 3 mode)
├── deep_research.py (3 步 agent loop)
├── multimodal.py (tesseract OCR)
├── user_auth.py (HMAC token + quota)
├── metrics.py (Prometheus 指标)
├── star_search_monitor.py (监控告警)
├── mcp_server.py (MCP server stdio + SSE)
├── api_server.py (FastAPI 22 端点)
├── index.html (Web UI + PWA + 移动优化)
├── service-worker.js (离线缓存)
├── manifest.webmanifest (PWA 配置)
└── icon-192/512.png (Python 手写 PNG)
```

---

## 📊 性能基准

| 指标 | 数值 |
|---|---|
| **端到端 search** | 200-500ms (cache 命中 0-1ms) |
| **LLM 答案** | 5-10s (cache 命中 0-1ms) |
| **流式首字** | < 1s |
| **语义搜索** | 5ms (BM25) |
| **Deep Research** | ~45s (3 步) |
| **OCR** | 0.5-1s (tesseract CPU) |
| **缓存命中** | 40% (search) / 95% (answer) |
| **可用性** | 99.9% (systemd 守护) |
| **MCP server** | 4 tools + 2 transport (stdio/SSE) |

---

## 🌐 公网部署

| 端点 | URL |
|---|---|
| **Web UI** | https://search.token-star.cn/ |
| **API** | https://search.token-star.cn/v1/* |
| **MCP SSE** | https://search.token-star.cn/mcp/sse |
| **Prometheus** | https://prom.token-star.cn/ |
| **Grafana** | https://grafana.token-star.cn/ (admin/staradmin) |
| **OpenAPI Schema** | https://search.token-star.cn/.well-known/openapi.yaml |

**部署架构**:
- 1 台腾讯云轻量应用服务器 (1.2Gi/3.6Gi 内存)
- systemd user 守护 (stardust-svc + star-search-monitor)
- 9 docker 容器 (new-api, prometheus, grafana, node-exporter 等)
- Let's Encrypt HTTPS (自动续期)
- nginx 反代 + 公网域名矩阵 (search/prom/grafana/api/agent)

---

## 📦 快速开始

```bash
# 1. 安装
git clone https://github.com/muchenhengxin/Star.git
cd Star
pip install aiohttp beautifulsoup4 lxml playwright pytesseract

# 2. 启动 API 服务
python3 scripts/api_server.py --port 5000

# 3. 调用
curl -X POST http://localhost:5000/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"华为鸿蒙","answer":true,"top":3}'
```

**或直接用公网**:
```bash
curl -X POST https://search.token-star.cn/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"华为鸿蒙","answer":true,"top":3}'
```

**Claude Desktop**:
- 加 `https://search.token-star.cn/mcp/sse` 到 MCP 配置

**Cursor**:
- 加 MCP server 配置 (见上)

---

## 📈 版本历史

| 版本 | 日期 | 主要变更 |
|---|---|---|
| **v20.17** | 2026-06-16 | 实战 58: Deep research 3 步 (主 search + LLM 拆 3 子问题 + 3 子 search + LLM 综合) |
| **v20.16** | 2026-06-16 | 实战 57: 多模态 OCR (tesseract-4.1.1 + chi_sim+eng) |
| **v20.15** | 2026-06-16 | 实战 55: 用户系统 (4 端点 + HMAC token + quota 100/天) |
| **v20.14** | 2026-06-15 | 实战 56: Mermaid/Table/JSON 前端渲染 (marked + mermaid) |
| **v20.13** | 2026-06-15 | 实战 54: 移动端 UI 优化 (viewport + iOS safe area + input type=search) |
| **v20.12** | 2026-06-15 | 实战 53: PWA (manifest + service-worker + icon-192/512) |
| **v20.11** | 2026-06-15 | 实战 52: OpenAI/Anthropic plugins (3 manifest) |
| **v20.10** | 2026-06-15 | 实战 51: Perplexity 探索发现 (3 mode + 修 LLM 答案层真 key + subprocess runner 解 uvloop 冲突) |
| **v20.9** | 2026-06-15 | 实战 50: Vector DB 语义搜索 (BM25 + 字符 n-gram / 中文友好 / 5ms 检索) |
| **v20.8** | 2026-06-15 | 实战 49: i18n 英文版 (SKILL_EN.md 22KB) |
| **v20.7** | 2026-06-15 | 实战 48: Claude Desktop MCP 集成 |
| **v17.7** | 2026-06-04 | 答案缓存 (236x speedup) + 内联引用 (Perplexity Mode UI) |
| **v17.5** | 2026-06-04 | 4 类 Prompt 模板 (finance/tech/news/general) |
| **v17.4** | 2026-06-04 | 多轮相关问题 (3 个 followup chips) |
| **v17.3** | 2026-06-04 | 前端 AI 答案卡片 (Perplexity Mode UI) |
| **v17.2** | 2026-06-03 | LLM 答案层 (GLM-4-Flash 永久免费) |
| **v17.0** | 2026-06-03 | **MCP 化**: 4 tools (web_search / web_search_news / web_search_finance / get_engines) |
| **v16.2.1** | 2026-06-03 | 公网 HTTPS + 前端文人风 + 守护进程 |
| **v16.2** | 2026-06-03 | Playwright 优雅降级 (无 sudo 也能跑) |
| **v16.1** | 2026-06-02 | +5 RSS 引擎 + global 中英双源 + finance mode |
| **v16.0** | 2026-06-02 | sogou KeyError 修复 + 质量标识 🌟🌟🌟 + --explain |
| **v15.1** | 2026-06-01 | +7 site:bing 代理引擎 (csdn/cnblogs/eastmoney/cls/...) |
| ... | ... | (老版本) |

---

## 🤝 对比百度千帆 API / Tavily / Perplexity

| 维度 | Star Search v20.17 | 百度千帆 API | Tavily | Perplexity |
|---|---|---|---|---|
| 引擎数 | **16** | 1 (百度) | 5 | 5 |
| 官方来源 | **强** | 弱 (百家号) | 中 | 中 |
| 学术/代码 | **4 引擎** | ❌ | ❌ | ❌ |
| 多模态 | **✅ OCR** | ❌ | ❌ | ❌ |
| Deep Research | **✅ 3 步** | ❌ | ✅ 付费 | ✅ 付费 |
| 语义搜索 | **✅ BM25** | ❌ | ❌ | ❌ |
| LLM 答案 | **✅ GLM-4** | ❌ | ✅ 付费 | ✅ 付费 |
| 探索发现 | **✅ 3 mode** | ❌ | ❌ | ❌ |
| PWA | **✅** | ❌ | ❌ | ❌ |
| 公网 API | **✅** | ✅ 按量 | ✅ 付费 | ❌ |
| MCP server | **✅** | ❌ | ❌ | ❌ |
| 费用 | **完全免费** | 按量付费 | $0.001/次 | $20/月 |

---

## 📝 License

MIT-0 (Public Domain)

---

## 🙏 致谢

- new-api 智谱 GLM-4-Flash (永久免费)
- Playwright (浏览器自动化)
- tesseract-ocr (OCR)
- marked.js + mermaid.js (渲染)
- Prometheus + Grafana (监控)
