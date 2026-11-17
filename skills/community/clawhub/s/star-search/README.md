# Star Search v16.0 — 16 引擎直搜 + 定时增量 + OpenAI API + 智能缓存 + 智能去重 + 质量标识

> **免费中文搜索。16 引擎混动：搜狗HTTP / Bing CN / GitHub Issues / 头条 / 知乎 / 微信公众号（site:bing 直搜免反爬）/ 搜狗PW / 百度 / 360 / 微信PW / Bing国际 + 7 个 site:bing 新引擎（v15.1 csdn/cnblogs/eastmoney/cls/tencent_cloud/sina_finance/sohu）。HTTP 引擎 <1秒直出，v13 智能缓存，v14 OpenAI API + 增量追加，v15 定时 cron 客户端，v16 修复 sogou KeyError + 🌟🌟🌟 质量标识 + --explain 评分透明，全面超越百度千帆 API。**

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue) ![License MIT](https://img.shields.io/badge/license-MIT-green) ![Version 16.0](https://img.shields.io/badge/version-16.0-orange) ![Engines 16](https://img.shields.io/badge/engines-16-brightgreen)

---

## v16.0 核心升级（2026-06-02）

| 升级 | 价值 |
|------|------|
| **修复 sogou KeyError** (v16) | 反复刷 stderr 的"搜狗挂了"假象没了，6/6 mode smoke test 0 错误 |
| **🌟🌟🌟 质量标识** (v16) | `cross_verified >= 3` 标 🌟🌟🌟，可视化"这条结果有多可信" |
| **--explain 评分透明** (v16) | 调试模式显示每条结果的 `cross_verified=+40 · domain_auth=+8` 评分构成 |
| **16 引擎** | v15.1 加 7 个 site:bing 代理 (csdn/cnblogs/eastmoney/cls/tencent_cloud/sina_finance/sohu) |
| **定时增量客户端** (v15) | `cron_refresh.py` 异步并发拉多 query，JSONL 输出，可配 cron |
| **OpenAI-compatible API** (v14) | FastAPI 5 endpoints，subagent/脚本可直接调用 |
| **增量追加** (v14) | `force_refresh` 绕过缓存 + 与历史合并，节省 78% 时间 |
| **智能缓存 v13** | 分桶TTL（news 5min / dev 1h）+ query 归一化 + 桶复用（num 5/8/10 共享）+ 命中率统计 |
| **GitHub Issues 引擎** (v12.1) | 开发者向查询直接拿到 issue 级讨论（带 [bug] / [feature-request] 标签），自动过滤 bot 批量 issue |
| **智能去重** (v12.2) | 主题词 key + Jaccard 双策略合并同事件多转载 |
| **跨源聚合** (v12.2) | ⭐ 标记可视化跨源验证，cluster_size 字段记录合并条数 |
| **dev 模式** (v12.1) | 搜狗HTTP + 百度 + GitHub Issues + Bing CN，开发者首选 |
| **搜狗 HTTP** (v11.2) | 搜狗无需浏览器，0.5-1秒直出 |

---

## 为什么选 Star Search？

百度千帆 API 按量付费 + 来源偏自媒体。Star Search 通过多引擎混合 + 智能去重实现**免费、高质量、可验证**的中文搜索，三类查询全部超越百度 API。

| 维度 | Star Search v12.2 | 百度千帆 API | 对比 |
|:----|:----------------|:-----------|:----:|
| 引擎数 | **7** (HTTP + Playwright) | 1 (百度) | ✅ **远超** |
| 官方来源 | **强** (gov.cn / pbc.gov.cn / 新华网) | 弱 (百家号/自媒体) | ✅ **完胜** |
| 开发者向 | **GitHub Issues 引擎** | 无 | ✅ **独有** |
| 跨源验证 | ⭐ 标记 + cluster_size | 无 | ✅ **独有** |
| 速度 | quick 0.5-1s / deep 4-6s | 1-2s | ⚖️ 持平 |
| 摘要 | 中等 (HTML 解析) | 长 (百字级) | ⚖️ 略弱 |
| 费用 | **免费** | 按量付费 | ✅ **完全替代** |

**实测对比**（3 类查询 × 2 引擎）：

| 查询类型 | baidu-search | star-search v12.2 | 赢家 |
|---------|-------------|------------------|------|
| 政策类（央行 2026 货币政策）| 8条 0官方源，有标题党 | 8条 **4条官方源** | **Star 压倒** |
| 开发者向（Python asyncio 2026）| 8条 CSDN/聚合站 | 8条 + **2条 GitHub Issues** | **Star 完胜** |
| 新闻类（DeepSeek V4 Flash 免费）| 7条自媒体为主 | 8条 6条带 ⭐（最新5/28）| **Star 时效优** |

详细对比：`references/vs-baidu-search-comparison.md`

---

## 快速开始

```bash
# 默认查询（中文→deep 模式，5引擎并发）
python3 scripts/search.py "存储芯片超级周期"

# 开发者向（搜狗HTTP + 百度 + GitHub Issues + Bing CN）
python3 scripts/search.py "FastAPI 异步 中间件" --mode dev

# 极速查询（仅搜狗HTTP，0.5-1秒）
python3 scripts/search.py "华为" --mode quick

# 单引擎（Bing CN 返回真实直链）
python3 scripts/search.py "英伟达" --engine bing_cn

# 时效过滤
python3 scripts/search.py "央行 降息" --mode policy --recency month

# 精确匹配
python3 scripts/search.py "Python教程" --exact

# JSON 输出（脚本/子代理推荐）
python3 scripts/search.py "AI Agent" --mode news --json

# 列出所有引擎和模式
python3 scripts/search.py --list
```

**前置依赖**：
- Python 3.8+ + `pip install aiohttp beautifulsoup4 playwright`
- Playwright 浏览器（仅搜狗/百度/360/微信引擎需要）：`playwright install chromium`
- 无需 API Key

---

## 7 大引擎

| 引擎 | 类型 | 权重 | URL类型 | 说明 |
|------|------|------|---------|------|
| **Bing CN** | HTTP (aiohttp) | 85 | 真实直链 | 中文搜索主力，新华网/知乎/东方财富 |
| **GitHub Issues** | HTTP (aiohttp) | 80 | 真实直链 | **v12.1 新增**，issue 级讨论，过滤 bot/PR |
| **搜狗 HTTP** | HTTP (aiohttp) | 95 | 跳转链接 | <1秒，高质量中文结果 |
| 搜狗 (Playwright) | Playwright | 100 | 跳转链接 | URL 解析 + 反爬 fallback |
| 百度 | Playwright | 80 | 跳转链接 | 国内引擎 |
| 360 | Playwright | 60 | 跳转链接 | 国内补充 |
| 微信 (weixin) | Playwright | 85 | 跳转链接 | 搜狗微信 |
| Bing HTTP | HTTP (aiohttp) | 70 | 真实直链 | 国际版 (global 模式) |

---

## 7 种模式

| 模式 | 引擎组合 | 速度 | 适用场景 |
|------|---------|------|---------|
| **deep** (默认) | 搜狗HTTP+百度+360+微信+Bing CN | 4-6秒 | 综合研究，最大覆盖 |
| **quick** | 搜狗HTTP | 0.5-1秒 | 极速验证 |
| **dev** | 搜狗HTTP+百度+**GitHub Issues**+Bing CN | 4-6秒 | **v12.1 开发者向** |
| **news** | 搜狗HTTP+百度+微信+Bing CN | 3-4秒 | 新闻追踪 |
| **global** | Bing HTTP (纯 HTTP) | 1-2秒 | 英文国际 |
| **policy** | 百度+搜狗HTTP+Bing CN | 3-4秒 | 政策研究 |
| **stock** | 搜狗HTTP+百度+微信+Bing CN | 3-4秒 | 财经股票 |

---

## v12.2 智能去重算法

**双策略合并**：
1. **主题词 key**（精确召回同事件）：归一化标题 → 去停用词 → 取前10字符
2. **Jaccard bigram**（兜底相似标题）：字符 bigram Jaccard > 0.5

**跨源聚合加成**：
- `cross_verified = (来源数-1) + (引擎数-1)`，每多一源 +10 分
- 来源数 ≥3 加 15 分，=2 加 8 分
- 排序后输出时带 **⭐** 标记表示多源验证

**输出字段**（v12.2 新增）：
- `cluster_id`：所属簇 ID
- `cluster_size`：合并了几条原始结果
- `source_count`：独立来源数
- `source_engines`：覆盖的引擎列表

---

## JSON 输出格式

```json
[
  {
    "title": "DeepSeek-V4-Flash登顶全球调用量榜首",
    "url": "https://weixin.sogou.com/link?url=...",
    "url_type": "redirect",
    "engine": "weixin",
    "cross_verified": 3,
    "source_count": 3,
    "source_engines": "bing_cn,sogou,weixin",
    "cluster_size": 2,
    "cluster_id": 1,
    "date": "2026-05-28",
    "summary": "DeepSeekV4-Flash(轻量版...",
    "score": 156.0
  }
]
```

---

## 性能基准

| 模式 | 耗时 | 输入→输出 | 真实 URL 占比 |
|------|------|-----------|--------------|
| quick | 0.5-1秒 | 1→N | 0%（跳转链） |
| Bing CN 单引擎 | 1-2秒 | 1→10 | **100%** |
| deep (5引擎) | 4-6秒 | 25-30→8-10 | ~40% (Bing CN + GitHub) |
| dev (4引擎) | 4-6秒 | 25-30→8-10 | ~50% (Bing CN + GitHub) |
| global (Bing HTTP) | 1-2秒 | 1→10 | 100% |

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| **15.0** | 2026-06-01 | **10 引擎直搜 + 定时增量**：toutiao/zhihu/weixin 3 个 site:bing 代理（100% 目标域，免反爬 <1秒）+ cron_refresh.py 客户端 |
| **14.0** | 2026-06-01 | **OpenAI API + 增量追加**：FastAPI 5 endpoints（/v1/search + /v1/search/refresh）+ force_refresh 强制刷新 + 与历史合并（refresh=true/false 标记）|
| **13.0** | 2026-06-01 | **智能缓存层**：分桶TTL（news 5min / dev 1h）+ query归一化 + 桶复用（num 5/8/10 共享）+ 命中率统计 |
| **12.2** | 2026-06-01 | **智能去重 + 跨源聚合**：主题词 key + Jaccard 双策略，⭐ 标记，cluster_size |
| **12.1** | 2026-06-01 | **GitHub Issues 引擎**：开发者向查询，issue 级讨论，过滤 bot/PR。dev 模式 |
| 11.2 | 2026-05-28 | 搜狗 HTTP 模式（aiohttp，<1秒），quick 模式 0.5-1秒 |
| 11.1 | 2026-05-25 | Bing CN HTTP 引擎 — 真实直链，官方源覆盖，3秒内 |
| 10.x | 2026-05-15 | Playwright + 搜狗/百度/360 多引擎 |
| 8.3 | 2026-05-10 | 旗舰版：URL 异步解析、摘要 100% 覆盖 |

---

## 技术架构

```
search.py (v12.2, Hybrid HTTP + Playwright + 智能去重)
│
├── HTTP 引擎 (aiohttp, 无需浏览器)
│   ├── 搜狗 HTTP  <1秒, 质量高
│   ├── Bing CN     真实直链, 官方源
│   ├── GitHub Issues  开发者向, 真实直链
│   └── Bing HTTP   国际版
│
├── Playwright 引擎 (需浏览器, 反爬 fallback)
│   ├── 搜狗        URL 跳转解析
│   ├── 百度        国内引擎
│   ├── 360         国内补充
│   └── 微信        搜狗微信
│
├── 智能去重 v12.2
│   ├── 主题词 key  +  Jaccard 双策略
│   ├── 跨源聚合加成
│   └── ⭐ 可视化标记
│
├── 语言感知路由
│   ├── 中文 → CN_ENGINES (deep/dev/news/policy/stock)
│   └── 英文 → GLOBAL_ENGINES
│
└── 缓存层
    └── SQLite 1小时, (query + engine + mode) key
```

---

## 依赖

```
pip install aiohttp beautifulsoup4 lxml playwright
playwright install chromium
```

无需 API Key。

---

## License

MIT
