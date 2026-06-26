## RSS Digest - 资讯流聚合技能

基于你自己的 **quotedance-service Feeds API** 和本地 `RSSHub (http://localhost:1200)`，为 Agent 提供一个「最近几天资讯流」的聚合能力。

- 默认：先从 quotedance-service 获取你已启用的订阅源，再由本地逐个抓取 RSS，生成 Markdown 资讯流。
- 可选：支持按 **资讯源名称关键字** 过滤，例如“只看 少数派 / 机核网 / 某个专栏”。
- 支持简单的 **本地缓存**，在配置的 TTL 内重复调用不会频繁打服务端和 RSS 源站。

---

### 配置

配置文件：`skills/quotedance-rss-digest/config.json`

```json
{
  "serviceUrl": "https://quotedance.api.gapgap.cc",
  "apiKey": "与 qutedance-quotes 相同的 API Key",
  "rsshubUrl": "http://localhost:1200",
  "defaults": {
    "recentDays": 3,
    "limit": 100,
    "cacheTtlMinutes": 30,
    "sourceCacheTtlMinutes": 15
  }
}
```

- **serviceUrl**：quotedance-service 的线上地址（与你现在使用的一致）
- **apiKey**：和 `qutedance-quotes/config.json` 中一致，通过 `X-API-Key` 鉴权
- **rsshubUrl**：你本地 RSSHub 服务地址（当订阅源 `rss_url` 为相对路径时会自动拼接）
- **defaults.recentDays**：默认拉取「最近几天」的天数
- **defaults.limit**：最终输出的最大文章数量
- **defaults.cacheTtlMinutes**：缓存有效期，分钟
- **defaults.sourceCacheTtlMinutes**：订阅源列表缓存有效期，分钟（默认建议 15）

---

### 能力

#### 1️⃣ 全部订阅源资讯流

- 调用 quotedance-service：
  - `GET /feeds/registry`
  - 通过 `X-API-Key` 自动识别用户，返回该用户 **已启用的订阅源列表**
- 脚本在本地做：
  - 逐个抓取订阅源的 `rss_url`（支持 RSS / Atom）
  - 本地聚合并去重（优先按链接去重）
  - 只保留最近 `recentDays` 天内的文章
  - 截断为最多 `limit` 条
  - 格式化为 Markdown 列表（标题、来源、时间、链接）
  - 结果写入简单缓存文件（同一参数组合在 TTL 内重复调用直接命中缓存）

#### 2️⃣ 按资讯源名称筛选

- 用户可以在对话中描述：
  - “看下少数派最近几天的文章”
  - “只看机核网的更新”
- 脚本会：
  - 先从 `/feeds/registry` 拉取该用户订阅源
  - 本地抓取这些订阅源的 RSS 内容并聚合
  - 在本地用 **资讯源名称关键字** 做模糊过滤（例如匹配 `source_name` / `feed_title` / `source.name` 等字段）
  - 同样支持最近 N 天过滤与缓存

> 注意：由于服务端的数据结构可能调整，脚本在取“来源名称”时做了多种字段兜底，只要大致有个 source/name/title 字段就能工作。

---

### 在对话中如何使用

当用户说：

- “帮我汇总下最近几天的资讯流”
- “看下我订阅源最近 3 天有啥值得看的”
- “只看 少数派 的更新”
- “汇总最近 5 天我所有订阅源的新文章”

Agent 应该：

1. 选择本技能 `rss-digest`
2. 推断参数：
   - 若用户没有提天数 → 使用 `defaults.recentDays`
   - 若用户提到“最近 N 天 / 两三天 / 一周左右” → 转成具体天数
   - 若提到具体资讯源名称 → 作为 name 关键字过滤
3. 调用脚本生成 Markdown 资讯流，并直接展示给用户，必要时做少量总结。

---

### 手动脚本用法

从 `workspace-quotedance` 目录运行：

```bash
cd ~/.openclaw/workspace-quotedance

# 默认：最近 defaults.recentDays 天，全部源
node skills/quotedance-rss-digest/scripts/rss-digest.js

# 指定最近 N 天
node skills/quotedance-rss-digest/scripts/rss-digest.js --days 5

# 只看某个资讯源（按名称关键字模糊匹配）
node skills/quotedance-rss-digest/scripts/rss-digest.js --name 少数派

# 同时指定天数和输出数量
node skills/quotedance-rss-digest/scripts/rss-digest.js --days 7 --limit 50

# 强制刷新（忽略文章缓存和订阅源缓存）
node skills/quotedance-rss-digest/scripts/rss-digest.js --refresh

# 只刷新订阅源列表（文章缓存仍按原规则）
node skills/quotedance-rss-digest/scripts/rss-digest.js --refresh-sources

# 清空缓存并立即重新抓取
node skills/quotedance-rss-digest/scripts/rss-digest.js --clear-cache
```

---

### 目录结构

```text
skills/quotedance-rss-digest/
├── SKILL.md
├── config.json
├── scripts/
│   └── rss-digest.js
└── memory/
    └── rss-cache-*.json   # 本地缓存（脚本运行时自动创建）
```

---

### 实现概要

- 从 `config.json` 读取：
  - `serviceUrl` / `apiKey` / `rsshubUrl` / `defaults`
- 请求 quotedance-service：
  - 使用 `X-API-Key` 做鉴权
  - 调用 `/feeds/registry` 获取当前用户已启用订阅源
- 本地处理：
  - 先读取订阅源缓存（`sourceCacheTtlMinutes`），超时后重新请求 `/feeds/registry`
  - 对每个订阅源抓取 RSS/Atom（`rss_url` 为相对路径时会拼接 `rsshubUrl`）
  - 聚合、去重并按发布时间倒序排序
  - 根据 `recentDays` 过滤最近几天的文章
  - 可选按 `name` 关键字过滤资讯源
  - 限制输出为 `limit` 条
  - 生成结构化 Markdown 文本
  - 结合 `cacheTtlMinutes` 做文章缓存（按 days + name + limit 组合区分）
