# Star Search v16.2.0 — Public HTTPS Release 🚀

> **比百度搜索更懂中文，比任何 API 更适合 LLM agent。** 16 引擎直搜 + 5 RSS 引擎 + OpenAI-compatible API + 公网 HTTPS 部署。**完全免费**，无需 API key，无登录。

发布日期：2026-06-03 · License：MIT-0 · Star Search v16.2.0

---

## ✨ 这次发布的核心：公网 HTTPS 部署

**5 个端点全部上线，即用即接**：

```
https://search.token-star.cn/v1/health          ← 健康检查
https://search.token-star.cn/v1/search          ← 主搜索
https://search.token-star.cn/v1/search/refresh  ← 增量追加
https://search.token-star.cn/v1/modes           ← 11 种模式
https://search.token-star.cn/v1/engines         ← 16 个引擎
```

**实测速度**（公网 RTT）：

| 模式 | 查询 | 响应 | 数量 |
|---|---|---|---|
| tech_news | 华为鸿蒙 | **436ms** | 3 |
| global | GPT-4 vs Claude 3.5 | **361ms** | 3 |
| health | — | **70ms** | — |

---

## 🎯 为什么你应该试试

### vs 百度千帆 API

| 维度 | 百度千帆 API | Star Search v16.2 |
|---|---|---|
| **价格** | 按量付费，要 API key | **完全免费**，无 key |
| **官方来源** | 弱（百家号多） | **强**（gov.cn / pbc.gov.cn / 新华网） |
| **政策类查询** | 8 条 0 官方源 | 8 条 **4 官方源** |
| **开发者向** | 无 issue 级内容 | **GitHub Issues 引擎** |
| **跨源验证** | 无 | **🌟🌟🌟 质量标识** |
| **英文国际** | 一般 | **Bing 国际 + global 中英双源** |
| **RSS 实时** | 无 | **5 个真 RSS 源**（ithome/36kr/sspai/oschina/woshipm） |
| **OpenAI 兼容** | 不是 | **是**（subagent 可直接调） |
| **自部署** | 不行 | **一行命令起**（Docker / system pip） |

### vs DeepSeek / Kimi / 豆包

star-search **不是给人用的产品**，是**给 LLM agent 当工具**：

- Claude / Cursor / 自家 agent 可直接当 tool 调
- 返回**强结构化 JSON**（带 `cross_verified` / `engine` / `date` / `cluster_size` 元数据）
- LLM 自己生成综述（不需要我们代笔）
- **数据是事实**（URL + 标题 + 摘要 + 来源 + 时间），不是答案

---

## 🆕 v16.2 升级内容

### 1. 公网 HTTPS 部署
- `https://search.token-star.cn` 子域，Let's Encrypt 证书自动续期
- 子域架构（不影响主域 token-star.cn 的 New API / Agent Platform）
- FastAPI server 跑在腾讯云 ubuntu 用户 systemd (端口 5000)

### 2. Playwright 优雅降级
- 11 HTTP 引擎在没浏览器的服务器上独立工作
- Playwright 缺时自动跳过（不抛异常）
- 显式调用 `--engine sogou` 才触发 PW 缺失错误

### 3. 5 个真 RSS 引擎（v16.1）
- rss_ithome / rss_36kr / rss_sspai / rss_oschina / rss_woshipm
- <1 秒出真实新闻

### 4. global 中英双源路由（v16.1）
- 中文 query → bing_cn + bing_http 双源
- 跨源结果标 🌟🌟🌟（可视化验证）

### 5. cron_refresh 5 preset（v16.1）
- dev / finance / tech / weixin / all
- 30 分钟循环拉 + JSONL 输出

---

## 📦 11 HTTP 引擎 + 5 RSS 引擎 + 4 Playwright 引擎（待 sudo 启用）

**HTTP 引擎（11 个，0 浏览器 < 1 秒）**

| 引擎 | 用途 | 类型 |
|---|---|---|
| sogou_http | 搜狗中文 | aiohttp |
| bing_cn | Bing 中文 | aiohttp |
| bing_http | Bing 国际（global） | aiohttp |
| github_issues | GitHub issue 级讨论 | aiohttp |
| toutiao | 头条（site:bing 代理） | aiohttp |
| zhihu | 知乎（site:bing 代理） | aiohttp |
| weixin_bing | 微信公众号（site:bing 代理） | aiohttp |
| csdn / cnblogs / tencent_cloud | 开发者向 3 站 | aiohttp |
| eastmoney / cls / sina_finance | 财经 3 站 | aiohttp |
| sohu | 综合 | aiohttp |

**RSS 引擎（5 个，< 1 秒真新闻）**

| 引擎 | 源 |
|---|---|
| rss_ithome | IT 之家（科技） |
| rss_36kr | 36 氪（创投） |
| rss_sspai | 少数派（数字生活） |
| rss_oschina | 开源中国（开发者） |
| rss_woshipm | 人人都是产品经理 |

**Playwright 引擎（4 个，需 sudo 装系统依赖）**

| 引擎 | 用途 |
|---|---|
| sogou_pw | 搜狗真访问 |
| baidu_pw | 百度真访问 |
| 360_pw | 360 真访问 |
| weixin_pw | 微信公众号真访问 |

---

## 🚀 30 秒接入

### curl 试一下

```bash
curl -X POST https://search.token-star.cn/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"华为鸿蒙","mode":"tech_news","top":3}'
```

返回：

```json
{
  "query": "华为鸿蒙",
  "mode": "tech_news",
  "count": 3,
  "elapsed_ms": 335,
  "results": [
    {
      "title": "【IT之家开箱】华为 nova 16 Pro 手机美图",
      "url": "https://www.ithome.com/0/959/088.htm",
      "score": 95,
      "cross_verified": 0,
      "engine": "rss_ithome"
    },
    ...
  ]
}
```

### Python 客户端

```python
import httpx

r = httpx.post('https://search.token-star.cn/v1/search', json={
    'query': '华为鸿蒙',
    'mode': 'tech_news',
    'top': 3
}).json()
for item in r['results']:
    print(f"{item['score']:5.1f}  {item['title']}")
```

### Claude / Cursor 当 tool 用

OpenAI-compatible schema，**任何 LLM agent 直接调**：

```json
{
  "name": "star_search",
  "description": "Search the Chinese web with cross-source verification. Returns structured results with score, engine, cross_verified, date.",
  "parameters": {
    "query": "string",
    "mode": "string (quick|deep|dev|news|global|policy|stock|tech_news|finance|weixin|rss_ithome|rss_36kr|...)",
    "top": "integer 1-20"
  }
}
```

### 自部署

```bash
git clone https://github.com/muchenhengxin/Star.git ~/.hermes/skills/research/star-search
cd ~/.hermes/skills/research/star-search
python3 scripts/api_server.py --port 5000
# → http://127.0.0.1:5000/v1/health
```

---

## 🛣️ 路线图

| 版本 | 目标 | 状态 |
|---|---|---|
| v16.2 | **公网 HTTPS + Playwright 优雅降级** | ✅ **这次发布** |
| v17.0 | **MCP server 化**（让 Claude Desktop 当 tool 用） | 设计中 |
| v18.0 | 补小红书 / B站 / 抖音 / 微博 / 知乎热榜 | 设计中 |
| v19.0 | 自建索引（cron 持续抓 + ES/Meilisearch） | 设计中 |
| v20.0 | 多用户平台（对接 token-star.cn Agent Platform） | 设计中 |

---

## 🙏 谁该用这个

- 🤖 **LLM agent 开发者**：要给 agent 实时搜索能力的，OpenAI-compatible 5 分钟接入
- 📰 **财经研究**：5 个财经引擎（eastmoney/cls/sina_finance + 3 引擎）+ 5 个 RSS + cross_verified
- 🔧 **中文技术搜索**：github_issues + csdn + cnblogs + tencent_cloud + oschina RSS
- 📊 **政策研究**：gov.cn / pbc.gov.cn / sse.com.cn 强官方源
- 🌏 **中英双语**：global mode 自动判断（中文 query → 双源，英文 → bing_http）
- 🛡️ **隐私敏感**：自部署，数据全在你磁盘，不上传任何云

---

## 📜 License

MIT-0 — 免费使用、修改、再分发，**无需署名**。

## 🔗 链接

- **公网 API**：https://search.token-star.cn
- **GitHub**：https://github.com/muchenhengxin/Star
- **ClawHub**：https://clawhub.ai/skill/star-search
- **SKILL.md**：仓库根目录
- **踩过的坑**：见仓库 `references/`

---

**Star Search v16.2.0 — 2026-06-03**

让 LLM 拿到实时事实层，让中文搜索比百度更准确，让隐私不妥协。
