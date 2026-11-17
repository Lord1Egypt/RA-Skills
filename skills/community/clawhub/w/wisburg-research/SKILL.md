---
name: wisburg-research
description: 通过 wisburg CLI 查询智堡（Wisburg）Open API 的财经研究数据 —— 包括宏观/策略研报、企业研究报告、电话会纪要、财经资讯流、Mikko 日志快评、AI 市场日报、文章、文献和资管报告。当用户提到"查研报"、"宏观/策略报告"、"某公司的研究/财报会议"、"市场日报"、"今日财经资讯"、"Mikko日志"、"mikko"、"快评"、"智堡"、"wisburg"，或者询问中国/海外市场的研究观点、资讯动向、机构观点时，**主动使用本 skill**——即使用户没有明确说"用 wisburg"。也适用于需要按时间窗口或关键词检索财经研究素材的研究/投研工作流。
homepage: https://github.com/Weaxs/wisburg-cli
metadata: {"openclaw":{"requires":{"bins":["wisburg"]},"primaryEnv":"WISBURG_API_KEY","install":[{"id":"npm","kind":"node","package":"wisburg-cli","bins":["wisburg"],"label":"Install Wisburg CLI (npm)"}]}}
---

# Wisburg Research

通过 `wisburg` CLI 查询智堡 Open API。智堡（Wisburg）是聚焦宏观、策略和企业研究的中文财经研究平台，本 skill 让你能够代表用户查到研报、电话会纪要、市场日报、资讯流等。

## 触发场景

凡是涉及以下内容，优先考虑本 skill：

- **研报、研究观点**："找几篇宏观研报"、"看看最近的策略报告"、"美联储加息有什么研究"
- **企业研究**："腾讯有什么研报"、"特斯拉的研究怎么说"
- **电话会议纪要**："最近哪家公司的 earnings call 值得看"、"看一下英伟达的电话会纪要"
- **财经资讯**："今天有什么财经新闻"、"最近的市场资讯"、"看看资讯流"
- **Mikko 日志（快评）**："看看 Mikko 日志"、"mikko 今天写了什么"、"最近有什么快评"
- **AI 市场日报**："今天的市场日报"、"昨天的 AI 日报"
- **文章 / 文献 / 资管报告**：智堡平台上的长文、文献库、专业资管研究
- 用户直接提到 **"智堡"** 或 **"wisburg"**

不要用本 skill 做：实时行情查询（智堡不是行情接口）、个股交易数据、外部券商系统对接。

## 前置检查

调用 CLI 前确认两件事：

1. **CLI 已安装**：`command -v wisburg` 应返回路径。如果没装，提示用户运行 `npm install -g wisburg-cli`，不要自己装（用户的 npm 全局目录权限可能要 sudo）。
2. **API Key 已配置**：环境变量 `WISBURG_API_KEY` 或 `~/.wisburg/config.json` 里的 apiKey。如果没有，提示用户 `export WISBURG_API_KEY=...` 或 `wisburg config set-api-key <key>`。在请求失败、错误信息提到 missing API key 时再做这个检查也行——别在每次调用前都跑一遍。

## 子命令失败时,先用 `wisburg request` 重试,再考虑放弃

这条放在最前面是因为它是这个 skill 最容易被忽略、却最关键的一条。

**规则**:任何 `wisburg <资源> <动作>` 调用如果失败、被权限拒绝、超时或返回奇怪结果,**不要直接放弃,也不要让用户手动跑命令**——先用底层端点重试同一个意图:

```bash
# 子命令路径(可能失败)
wisburg market-daily list --first 1

# 等价的 request 兜底(几乎总能用)
wisburg request GET /api/market-daily --query first=1
```

**为什么要这样**:`wisburg <子命令>` 只是 `wisburg request GET /api/<资源>` 的薄封装。在某些环境(subagent bash 沙箱白名单只放行了 `wisburg --version`、CLI 版本旧、子命令名拼写漂移)子命令会失败,但底层 HTTP 端点和 `wisburg request` 通用入口一直可用。**子命令失败 ≠ 拿不到数据**,这是两件事。

**怎么应用**:看到子命令报错(non-zero exit、`permission denied`、`unknown command`、network error 之类)时,立刻把命令改写成 `wisburg request GET /api/<资源> --query <参数>=<值>` 重试一次,再决定是不是真的拿不到。`--query` 参数可以重复多次传递不同 KEY=VALUE。

## 资源命令一览

CLI 把每个 Open API 资源映射成同名子命令,所有 list 命令都支持相同的过滤参数。第二列是 `wisburg request` 兜底时对应的 API 路径。

| 资源 | 子命令 | 兜底路径 | 用途 |
| --- | --- | --- | --- |
| `reports` | `wisburg reports list` / `get <id>` | `/api/reports`、`/api/reports/<id>` | 研报笔记(宏观/策略类研报) |
| `archives` | `wisburg archives list` / `get <id>` | `/api/archives`、`/api/archives/<id>` | 文献(深度长文、研究档案) |
| `company-reports` | `wisburg company-reports list` / `get <id>` | `/api/company-reports`、`/api/company-reports/<id>` | 企业研究 |
| `earningscalls` | `wisburg earningscalls list` / `get <id>` | `/api/earningscalls`、`/api/earningscalls/<id>` | 电话会纪要 |
| `articles` | `wisburg articles list` / `get <id>` | `/api/articles`、`/api/articles/<id>` | 平台文章 |
| `market-daily` | `wisburg market-daily list` | `/api/market-daily` | AI 市场日报(无单条 detail) |
| `feed` | `wisburg feed list` | `/api/feed` | 资讯流(最新动态) |
| `images` | `wisburg images list` | `/api/images` | 图片流 |
| `am-reports` | `wisburg am-reports list` / `get <id>` | `/api/am-reports`、`/api/am-reports/<id>` | 资管报告 |
| `mikko-logs` | `wisburg mikko-logs list` / `get <id>` | `/api/mikko-logs`、`/api/mikko-logs/<id>` | Mikko 日志(快评/碎碎念,列表即全文) |

**`mikko-logs` 与其他资源的区别**：它是快评流，列表项的 `content` 就是 markdown 全文（关键数据常以 `**加粗**` 标出），没有 `title`——呈现时用 `datetime` 做条目锚点，配图在 `images` 数组里。**列表即全文，不要逐条 `get`**；`get` 只在已知 id、想单条复核时用。

## 列表过滤参数

list 命令统一支持：

- `--first <n>` —— 返回条数，默认无（API 端默认通常 10-20），最大 100
- `--query <关键词>` —— 全文检索关键词
- `--start-time <time>` / `--end-time <time>` —— 时间窗口，支持 ISO 字符串（`2025-01-01`）或 Unix 时间戳
- `--after <cursor>` —— 翻页游标，从上一次响应的 `pageInfo.endCursor` 取得

**`--first` 数量词映射**:用户给出明确数量词时,直接映射到 `--first` 的具体数字,不要靠默认值再筛选:

- "一篇 / 最新一条 / 今天的" → `--first 1`
- "几篇 / 几条" → `--first 3`
- "3-5 篇" → `--first 5`(取区间上限,反正用户可挑可舍)
- "10 篇左右" → `--first 10`
- 没说数量 → `--first 5`(给一个手感合适的默认,而不是依赖 API 端的 10-20)

不要在用户已经说"3-5 篇"的时候拉 `--first 10` 再人工筛——既慢又费 token。

输出默认是格式化 JSON。如果用户只想看几条结果，结合 `jq` 或在脚本里解析。

## 典型用法

**根据关键词找研报：**
```bash
wisburg reports list --first 5 --query "美联储"
```

**最近一周的资讯流：**
```bash
wisburg feed list --first 20 --start-time 2026-05-23
```
（用绝对日期，别用 "上周" 这种，CLI 不解析自然语言时间。）

**翻看某条研报详情：**
```bash
wisburg reports get 12345
```

**今日 AI 市场日报：**
```bash
wisburg market-daily list --first 1
```

**某天的 Mikko 日志：**
```bash
wisburg mikko-logs list --first 20 --start-time 2026-08-26 --end-time 2026-08-27
```

**走原始接口（CLI 没暴露的参数,或子命令不可用时的兜底）：**
```bash
wisburg request GET /api/reports --query first=5 --query category=macro

# 子命令在某环境被拒时,等价兜底:
wisburg request GET /api/market-daily --query first=1
wisburg request GET /api/earningscalls --query first=5 --query query=英伟达
wisburg request GET /api/earningscalls/89612
```

## 输出处理

返回的 JSON 通常长这样：
```json
{
  "data": [ { "id": "...", "title": "...", "publishedAt": "...", "summary": "..." } ],
  "pageInfo": { "hasNextPage": true, "endCursor": "..." }
}
```

呈现给用户时：

- **不要把整段 JSON 直接抛给用户**，除非他们明确要 raw 数据。
- 把 `data` 数组里的每条做成简洁中文条目：标题、发布时间、摘要片段、ID（方便后续 `get` 详情）。
- 如果用户问"某某主题最新研报"，列出标题 + 简短摘要即可，不要先 `get` 每一条全文。
- 详情 `get` 拿到的内容如果很长，先给用户一个中文摘要 + 关键观点，而不是直接复述全文。

## 常见坑

- **时间字段**：API 接受 ISO 日期或时间戳。如果用户说 "今天/昨天/上周"，先在本地解析成 `YYYY-MM-DD` 再传。
- **分页**：单次 `--first 100` 是上限。要更多结果用 `--after <cursor>` 翻下一页，别 hammering 服务。
- **找不到结果**：先放宽关键词，或者去掉时间过滤再看；如果用户问的是非常细分的术语，可能 `articles` 比 `reports` 更合适——先试 `feed list` 探探有没有相关内容。
- **资源选择**：用户说"研报"通常是 `reports`（笔记类），但深度研报有时在 `archives` 或 `company-reports`。如果第一次查不到，换一个资源再试，比直接告诉用户"没找到"更有价值。
- **错误处理**：CLI 失败会以非零退出码 + `error: ...` 输出到 stderr。常见原因：API key 缺失/过期、网络/超时、参数格式错误（比如时间字符串）、子命令在沙箱被拒。**遇到子命令失败时,先按文档开头那条规则用 `wisburg request` 兜底重试,再决定是不是真的拿不到数据。**

## 工作流建议

1. **理解用户意图** → 选最匹配的资源（必要时多个资源都试）
2. **构造命令** → 关键词、时间、`--first` 控制条数
3. **执行 CLI** → 用 Bash 工具
4. **解析 JSON** → 提取关键字段，不要原文塞回给用户
5. **追问细节** → 如果用户对某条感兴趣，用 `get <id>` 拉详情并做摘要

记住：用户要的是**结论和洞察**，不是 JSON。CLI 是采集工具，最终回答要像一个懂行的研究员讲给他听。
