# star-search vs baidu-search 对比 (v12.2)

## 核心差异

| 维度 | star-search v12.2 | baidu-search (千帆API) |
|------|------------------|----------------------|
| 本质 | Hybrid HTTP+Playwright 多引擎爬虫 + 智能去重聚合 | 百度AI搜索API |
| 引擎数 | **7** (搜狗HTTP / Bing CN / 搜狗 / 百度 / 360 / 微信 / **GitHub Issues**) | 1 (百度) |
| 速度 | quick 0.5-1s · deep 4-6s (5引擎并发) · Bing CN 1-2s | ~1-2s (单引擎) |
| URL质量 | **Bing CN / GitHub Issues 返回真实直链**；搜狗/微信/百度/360为跳转链 | 全部真实直链 |
| 官方来源覆盖率 | **强** — Bing CN 覆盖新华网/上交所/东方财富/gov.cn/pbc.gov.cn/sse.com.cn | **弱** — 多为百家号/自媒体 |
| 开发者向 | **GitHub Issues 引擎（v12.1）** — issue级讨论、PR/bot 过滤 | 无 |
| 微信生态内容 | 有 (weixin.sogou.com) | 无 |
| 智能去重 | v12.2：主题词key + Jaccard 双策略 + 跨源聚合（⭐ 标记） | 无（百度原始排序） |
| 排序 | 多引擎加权 + 域名权威性 + 跨源验证 + 时间衰减 | 百度原始排序 |
| 费用 | **免费** | 按量付费 (千帆API) |
| 缓存 | SQLite 1小时 | 无 |
| 参数 | --exact / --sources / --recency / --mode / --engine | 有限 (count/recency) |

## 对比测试结果 (2026-06-01, v12.2)

### 测试1: DeepSeek V4 Flash API 限时免费（科技新闻）

| 项目 | baidu-search | star-search v12.2 |
|------|-------------|-------------------|
| 条目数 | 7条 | 8条 (21条去重) |
| 速度 | ~3s | 4s |
| 来源构成 | 3条什么值得买(自媒体) + 2条CSDN + 1条腾讯云 + 1条百度百科 | 5条微信行业文章 + 3条第三方官网站 |
| 时效 | 5月8-20日 | **5月24-28日**（最新榜单位居第1） |
| 跨源验证 | 无 | ⭐ 6条 (75%) |
| 摘要 | 长 (百字级) | 短 (HTML 摘要) |
| 胜者 | 摘要质量 + 方法细节 | **时效 + 跨源 + 多视角** → **平** |

### 测试2: 央行2026年货币政策 降准降息（政策查询）

| 项目 | baidu-search | star-search v12.2 |
|------|-------------|-------------------|
| 条目数 | 8条 | 8条 (24条去重) |
| **官方源** | **0条** (无 gov.cn / pbc.gov.cn) | **4条** (🏛️) — safe.gov.cn / pbc.gov.cn / creditchina.gov.cn / **gov.cn 国务院政策解读** |
| 媒体源 | nbd / jiemian / cctv / cls 财经媒体 | 同上 + ⭐ 跨源验证 |
| 标题党 | 2条（"房价又要大涨"/"此轮牛市已走完上半场"） | 0条 |
| 胜者 | — | **star-search 压倒性胜出** |

### 测试3: Python asyncio 协程 最佳实践 2026（开发者向）

| 项目 | baidu-search | star-search v12.2 |
|------|-------------|-------------------|
| 条目数 | 8条 | 8条 (24条去重) |
| 来源 | CSDN / 聚合博客站（千篇一律的"asyncio 完全指南"模板） | CSDN + 廖雪峰 + 百度百科 + **GitHub Issues (hs-bindgen, hydrus)** |
| 开发者向 | 弱（无 issue 级讨论） | **强** — GitHub Issues 引擎直接给真实 issue 链接（带 [feature-request] / [bug] 标签） |
| 胜者 | — | **star-search 完胜**（v12.1 GitHub Issues 引擎是独有优势） |

## 实测结论

v12.2 三个核心升级决定了对比格局：

### 1. GitHub Issues 引擎（v12.1 新增）
开发者向查询的杀手锏。百度 API 完全无 issue 级内容；star-search 通过 GitHub 官方 API（`api.github.com/search/issues`）直接拿到带标签的 issue 讨论。
- 自动过滤 bot（Renovate/Dependabot 等）
- 过滤 PR（只留 issue）
- 限速 60次/小时（无需 token）

### 2. 智能去重 + 跨源聚合（v12.2）
- **主题词 key + Jaccard 双策略** 合并同事件多转载
- **⭐ 标记** 可视化跨源/跨引擎验证
- **cluster_size** 字段记录合并了几条
- 5引擎 24条 → 8条 优质结果，去重几乎无性能开销

### 3. Bing CN 直链
延续 v11.1 优势，4 条官方源（gov.cn 系）覆盖让政策类查询 star-search 完胜百度 API。

## 使用场景建议

**用 star-search（优先）**：
- 默认查询（v12.2 dev 模式 = 搜狗HTTP + 百度 + GitHub Issues + Bing CN）
- 官方媒体/政府/学术查询
- 微信生态内容
- 开发者向查询（GitHub Issues）
- 跨源验证的深度研究
- 免费场景

**用 baidu-search 的场景**：
- 百度独家结果（百度百科、百家号）
- 需要长摘要（百度 API 摘要质量高于 HTML 解析）

**推荐流程**：默认 `python3 search.py "..." --mode deep`；开发者向加 `--mode dev`；极快速 `--mode quick`；政策类加 `--mode policy`；微信类加 `--mode news`。

## 演进

| 版本 | star-search 与 baidu-search 关系 |
|------|--------------------------------|
| v10.x | star-search 劣势：URL 跳转、无官方来源、百度被拦截 |
| v11.0 | HTTP 引擎试水：Google/DDG 从腾讯云超时不可用 |
| v11.1 | Bing CN HTTP 上线 — 真实URL、官方来源，**正式与 baidu-search 形成互补** |
| v11.2 | 搜狗 HTTP 模式加入 — quick 模式 0.5-1s |
| v12.1 | **GitHub Issues 引擎** + dev 模式（开发者向完胜） |
| v12.2 | **智能去重 + 跨源聚合 + ⭐ 标记**（多源新闻聚合能力提升） |
