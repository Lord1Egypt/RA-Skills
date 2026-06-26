---
name: smart-search
description: 统一搜索入口 — 智能路由 + 自动降级。根据查询场景自动选择最优工具（Serper/Google、OpenCLI、多引擎聚合、深度爬虫、远程浏览器、直接抓取等），任一工具失败时自动降级到下一优先级。触发条件：用户要求搜索信息、查找网页、获取最新资讯、验证事实、搜索中英文内容、或任何需要联网获取信息的场景。当搜索相关的所有场景都使用此 Skill，包括 web-search-plus、multi-search-engine、crawl4ai、firecrawl、opencli、web_fetch 等工具的协调调用。
metadata: {"openclaw": {"requires": {"bins": ["python3", "bash", "opencli"], "env": {"SERPER_API_KEY": "optional — T1 结构化搜索", "FIRECRAWL_API_KEY": "optional — T5 远程浏览器"}, "note": "所有 API Key 存储在 .env 和 config.json 中，不包含在 Skill 内容里"}}}
---

# Smart Search

统一搜索入口。一句话：**永远不因缺 API Key 放弃搜索。**

## 降级链路

```
T1: web-search-plus (Serper)       ← 结构化搜索，默认首选（2500次/月）
    ↓ 额度用尽 / API 错误
T2: opencli google search          ← 免 Key，直接调 Google，结构化 JSON ✅ 实测可用
    ↓ 失败
T3: multi-search-engine (crawl4ai) ← 爬取百度/搜狗等国内引擎，免 Key
    ↓ 验证码拦截
T4: crawl4ai (深度爬取)            ← 指定 URL 完整抓取，JS 渲染支持
    ↓ 失败
T5: firecrawl-cli                  ← 远程浏览器反爬（需 API Key）
    ↓ 无 Key 或额度用完
T6: web_fetch                      ← 已知 URL 直接提取 Markdown
    ↓ sandbox 网络限制 / 失败
T7: OpenCLI 其他搜索               ← zhihu search / bilibili search 等垂直搜索
```

## 场景路由

| 场景 | 首选工具 | 说明 |
|------|----------|------|
| 英文搜索 / 结构化结果 | T1 web-search-plus | Serper，返回 JSON 结构 |
| 中文内容 / 国内信息 | T2 opencli google | 免 Key，直接调 Google |
| AI 新闻 / 技术动态 | T1→T2 | Serper → opencli google |
| 知乎内容搜索 | T7 opencli zhihu search | 垂直搜索 |
| 深度页面 / JS 渲染 | T4 crawl4ai | 指定 URL 完整抓取 |
| 重度反爬网站 | T5 firecrawl-cli | 远程沙箱 |
| 已知 URL 提取 | T6 web_fetch | 直接给 URL 时 |

## 使用方法

### T1: 结构化搜索（默认）

```bash
python3 skills/web-search-plus/scripts/search.py -q "查询内容" --count 5
```

### T2: OpenCLI Google 搜索（免 Key）

```bash
opencli google search "查询内容" --limit 5 -f json
```

### T3: 国内引擎（crawl4ai 爬百度）

```python
python3 -c "
import asyncio
from crawl4ai import AsyncWebCrawler
async def main():
    async with AsyncWebCrawler() as c:
        r = await c.arun(url='https://www.baidu.com/s?wd=查询内容')
        print(r.markdown[:3000])
asyncio.run(main())
"
```

### T4: 深度爬取（指定 URL）

```python
python3 -c "
import asyncio
from crawl4ai import AsyncWebCrawler
async def main():
    async with AsyncWebCrawler() as c:
        r = await c.arun(url='https://example.com/article')
        print(r.markdown)
asyncio.run(main())
"
```

### T5: 远程浏览器

```bash
firecrawl search "查询内容" --limit 5
```

### T6: 直接提取

```
web_fetch(url="https://example.com", extractMode="markdown")
```

### T7: OpenCLI 垂直搜索

```bash
opencli zhihu search "查询内容" --limit 5 -f json
opencli bilibili search "查询内容" --limit 5 -f json
opencli hackernews top --limit 5 -f json
```

## 降级执行策略

当首选工具失败时：

1. **不要报 API Key 错误给用户**
2. 按 T1→T2→T3→...→T7 顺序尝试下一个工具
3. 记录哪个工具成功了（方便后续优化）
4. 所有工具都失败时才告知用户

## ⚠️ 禁止事项

- **不要使用** `web_search` (Brave) — 无 API Key，必然失败
- 不要在没有降级尝试前就告诉用户搜索失败
- 不要在用户消息里暴露 API Key 或错误详情

## ⚡ 环境说明

| 环境 | T1 | T2 | T3 | T4 | T5 | T6 | T7 |
|------|----|----|----|----|----|----|----|
| 本机（sandbox） | ✅ | ✅ | ✅(百度可爬) | ✅ | ❌(额度完) | ⚠️(部分拦截) | ✅ |
| 其他 VPS | ✅ | ✅ | ✅ | ✅ | ✅(有Key时) | ✅ | ✅ |

sandbox 网络限制：
- `web_fetch` 对部分域名会被拦（Google、部分境外站点）
- crawl4ai 能正常抓取百度，但搜索结果质量不如 Serper
- OpenCLI 依赖 Chrome 浏览器 bridge（需 Chrome 运行）

## OpenCLI 可用搜索命令

```bash
opencli google search   "query"   # Google 搜索
opencli google news              # Google 新闻
opencli google suggest           # Google 联想词
opencli google trends            # Google 趋势
opencli zhihu search    "query"  # 知乎搜索
opencli zhihu hot                # 知乎热榜
opencli bilibili search "query"  # B站搜索
opencli hackernews top           # HackerNews 热帖
opencli arxiv search    "query"  # 学术论文搜索
opencli 36kr search     "query"  # 36kr 搜索
```

查看完整命令列表：`opencli list -f yaml | grep search`

## 配置

- Serper Key: `skills/web-search-plus/.env`
- Firecrawl Key: `skills/firecrawl-cli/.env`
- 多引擎配置: 见 `skills/multi-search-engine/SKILL.md`

## Token 安全

本 Skill 不包含任何 API Key。所有凭证存储在本地 `.env` 和 `config.json` 文件中，不会被打包进 `.skill` 分享文件。
