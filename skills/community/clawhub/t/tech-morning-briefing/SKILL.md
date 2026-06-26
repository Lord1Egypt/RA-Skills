# 晨报系统 — Morning Briefing

每日科技新闻晨报，三级分选 + 分组归类，飞书推送 + 文档同步。

---

## 核心流程

### 第一级：采集（目标 50+ 条）

使用 web_search（Tavily）搜索，分多轮从不同信息源采集：

**搜索策略（关键词 + freshness:week，不依赖 site: 限定）：**

| 来源 | 搜索关键词示例 |
|------|---------------|
| 36氪 | `AI创业融资 中国科技` |
| 量子位 | `大模型 AI开源` |
| 机器之心 | `AI研究 前沿模型` |
| IEEE | `technology research breakthrough` |
| TechCrunch | `AI startup funding` |
| The Verge | `tech AI product launch` |
| Solidot | `开源 Linux 安全` |
| 中文综合 | `华为 小米 比亚迪 科技新闻` |

**搜索技巧：**
- 每轮用 `web_search` 搜索 2-4 个关键词组合
- `freshness: "week"` 限定一周内
- 每轮 `count: 10`
- 总共至少跑 6-8 轮搜索，确保 50+ 条原始新闻
- 去重：按 URL 去重，同一事件只保留最早来源
- ⚠️ 避免纯 `site:` 限定搜索——容易返回索引页/标签页而非文章，用广泛关键词更有效

**采集结果写入池：**
```json
{
  "title": "原始标题",
  "url": "https://...",
  "source": "36kr",
  "category": "ai",
  "summary": "搜索结果摘要",
  "fetchedAt": "2026-05-12T08:00:00+08:00",
  "score": null,
  "tier": "raw",
  "pushedDate": null
}
```

### 第二级：评分 + 分类

对池中所有 `tier: "raw"` 的新闻逐条评分（0-10）并分类：

**评分维度：**

| 维度 | 权重 | 说明 |
|------|------|------|
| 影响力 | 0.3 | 行业影响范围、公司规模、政策级别 |
| 新颖性 | 0.25 | 是否独家/首发，还是旧闻重发 |
| 深度 | 0.2 | 有没有实质内容，还是标题党 |
| 相关性 | 0.25 | 科技相关度（政策类需额外扣分除非涉及科技） |

**评分规则：**
- 7.0+ → 高价值 → `tier: "high"`
- 5.0-6.9 → 中等 → `tier: "medium"`
- <5.0 → 低价值 → `tier: "discarded"`
- 政策/时政类新闻总量不超过当日推送的 20%

**分类规则（每条新闻标记 category）：**

| category | 标识 | 包含范围 |
|----------|------|---------|
| `ai` | 🧠 AI & 模型 | 大模型发布、AI 研究、算力基础设施、训练/推理突破 |
| `product` | 🔧 产品 & 工具 | 新产品发布、开发者工具、平台更新、应用层创新 |
| `industry` | 🚗 产业 & 硬件 | 智能汽车、芯片半导体、制造、新能源、机器人 |
| `policy` | 📋 政策 & 动态 | 监管法规、国标、融资、行业趋势、人事变动 |

分类优先级：如果一条新闻跨多个类别，按最核心的归类。如"DeepSeek V4用华为芯片训练"→ `ai`（模型本身是核心），而非 `industry`。

### 第三级：推送选择

1. 从 `tier: "high"` 中按分数降序取前 **8-10 条**作为当日推送
2. 推送条目尽量覆盖 2-4 个分类，避免单一类别占满
3. 已推送过的（`pushedDate` 不为 null）不再推送，除非是新进展
4. `tier: "high"` 但今天没被选中的，保留在池中，标记 `carryOver: true`
5. `tier: "medium"` 的保留一天，第二天如果还在就降为 `discarded`
6. `discarded` 的新闻从池中移除
7. 池中新闻最多保留 3 天（按 `fetchedAt` 算），超过自动清理

---

## 推送格式

按分组输出，每组内按分数降序，最重磅的用 ⭐ 标记：

```
☀️ 晨报 | 2026年5月12日 星期一

━━━━━━━━━━━━━━━━━━━━

🧠 AI & 模型

⭐ [Anthropic租下SpaceX 22万GPU超算](https://venturebeat.com/...)
   推理算力军备竞赛再升级——独家租用Colossus 1全部算力，22万GPU、300MW。ARR从8700万飙至300亿美元。
   🔗 VentureBeat

  [NVIDIA Vera Rubin：七芯片架构定义AI工厂](https://thegpu.ai/...)
   单GPU 3.6TB/s，NVL72全互联260TB/s，四大前沿实验室确认采用
   🔗 TheGPU

  [DeepSeek V4开源：华为昇腾训练，推理成本降73%](https://cnbc.com/...)
   1.6T参数MIT协议开源，HuggingFace权重已上线
   🔗 CNBC

🔧 产品 & 工具

  [OpenAI双发：GPT-Realtime-2 + Codex Chrome](https://macrumors.com/...)
   实时语音接入GPT-5推理，浏览器插件六个月ARR破10亿
   🔗 MacRumors

🚗 产业 & 硬件

⭐ [新能源车集体涨价：15+车企调价，智驾成分水岭](https://...)
   比亚迪上调智驾包、特斯拉收缩金融，单车涨2千-1万
   🔗 网通社

📋 政策 & 动态

  [L2辅助驾驶国标征求意见，驾驶员为第一责任主体](https://...)
   华为小米比亚迪特斯拉联合起草，违规脱手强制禁用
   🔗 IT之家

  [AlphaGo作者新公司11亿美元种子轮，估值51亿](https://...)
   David Silver创立Ineffable Intelligence，聚焦AI推理
   🔗 Instagram

━━━━━━━━━━━━━━━━━━━━

💬 "Artificial intelligence is the new electricity." — Andrew Ng
```

**格式要求：**
- 分组输出，每个分类带 emoji 标识，顺序固定：🧠→🔧→🚗→📋
- 每个分类内最重磅一条用 ⭐ 标记（仅一条）
- 标题：AI 重写，凝练有信息量，不是原标题照搬
- 标题带超链接指向真实 URL（markdown `[文字](URL)` 格式）
- 摘要：2-3 句，有具体信息（数字、产品名、技术点），不空泛
- 来源行用 `🔗 来源名`，不直接贴 URL
- 如果某个分类当日无新闻，跳过该分类，不输出空板块
- 每条控制在 3 行以内（标题+摘要+来源）
- 分隔线用 ━━
- 结尾英文名人名言，每天换一条，优先选科技/创新/思维类

---

## 飞书文档同步

每日推送后，将内容同步到飞书文档库：

1. 首次运行时用 `feishu_doc` 的 `create` action 创建文档，标题格式：`晨报存档`
   - **必须**传 `owner_open_id` 为当前用户的 open_id，确保用户有完整权限
   - 创建后把 `doc_token` 存到 `data/config.json`
2. 后续每天用 `append` action 追加当天晨报内容
3. 追加内容格式（markdown）：
   ```markdown
   ## 2026年5月12日 星期一

   ### 🧠 AI & 模型
   - ⭐ [标题](URL) — 摘要
   - [标题](URL) — 摘要

   ### 🔧 产品 & 工具
   - [标题](URL) — 摘要

   ### 🚗 产业 & 硬件
   - ⭐ [标题](URL) — 摘要

   ### 📋 政策 & 动态
   - [标题](URL) — 摘要

   ---
   ```

---

## 新闻池管理

池文件：`data/news-pool.json`

```json
{
  "meta": { "version": 1 },
  "pool": [
    {
      "title": "...",
      "url": "...",
      "source": "...",
      "category": "ai",
      "summary": "...",
      "fetchedAt": "ISO date",
      "score": 7.5,
      "tier": "high",
      "carryOver": false,
      "pushedDate": null
    }
  ],
  "history": ["2026-05-11", "2026-05-10"],
  "lastUpdate": "2026-05-12T08:00:00+08:00"
}
```

**池维护规则：**
- 每天采集前先清理：移除 `fetchedAt` 超过 3 天的、`tier: "discarded"` 的
- `carryOver: true` 的保留，但最多再留 1 天
- 已推送的保留 1 天后清理
- 池容量上限 100 条，超了按 score 从低到高删

---

## 执行步骤（cron 触发时）

1. 读取 `data/news-pool.json`，清理过期新闻
2. 多轮搜索采集 50+ 条新闻，去重后加入池（`tier: "raw"`, `category: null`）
3. 对所有 `tier: "raw"` 的新闻评分 + 分类，更新 score、tier、category
4. 从 `tier: "high"` 中选 8-10 条推送（注意分类覆盖），标记 `pushedDate`
5. 未选中的 high 值新闻标记 `carryOver: true`
6. 按分组格式化晨报内容
7. 推送到飞书聊天（通过 cron announce）
8. 读取 `data/config.json` 获取 feishuDocToken，追加到飞书文档
9. 保存更新后的 news-pool.json、quotes-used.json 和 history
10. 结束

---

## 名人名言库

轮换池，避免重复：

```
"The best way to predict the future is to invent it." — Alan Kay
"Any sufficiently advanced technology is indistinguishable from magic." — Arthur C. Clarke
"Innovation distinguishes between a leader and a follower." — Steve Jobs
"The only way to do great work is to love what you do." — Steve Jobs
"Stay hungry, stay foolish." — Steve Jobs
"Technology is anything that wasn't around when you were born." — Alan Kay
"The most dangerous phrase is: We've always done it this way." — Grace Hopper
"Science is what we understand well enough to explain to a computer; art is everything else. — Donald Knuth"
"Simplicity is the ultimate sophistication." — Leonardo da Vinci
"The question of whether computers can think is like the question of whether submarines can swim." — Edsger Dijkstra
"First, solve the problem. Then, write the code." — John Johnson
"Measuring programming progress by lines of code is like measuring aircraft building progress by weight." — Bill Gates
"Premature optimization is the root of all evil." — Donald Knuth
"The Web does not just connect machines, it connects people." — Tim Berners-Lee
"Artificial intelligence is the new electricity." — Andrew Ng
"The biggest risk is not taking any risk." — Mark Zuckerberg
"We choose to go to the moon not because it is easy, but because it is hard. — John F. Kennedy"
"In the middle of difficulty lies opportunity." — Albert Einstein
"Logic will get you from A to B. Imagination will take you everywhere." — Albert Einstein
"The advance of technology is based on making it fit in so that you don't really even notice it." — Bill Gates
```

随机选一条，记录已用过的避免短期内重复。所有用过的记入 `data/quotes-used.json` 的 `used` 数组，当 pool 耗尽时清空 used 重新开始。

---

## 目录结构

```
skills/morning-briefing/
├── SKILL.md             # 本文件 — 完整流程指引
├── README.md            # 项目说明（GitHub/ClawHub 展示）
├── data/
│   ├── config.json      # 飞书文档 token 等配置
│   ├── news-pool.json   # 新闻池
│   └── quotes-used.json # 已用名言记录
```

---

## 配置说明

### 前置依赖

- **web_search**：需要 Tavily API Key（配置为 OpenClaw 搜索提供者）
- **feishu_doc**：需要飞书应用开启文档权限（OpenClaw feishu channel 内置）
- **cron**：通过 OpenClaw cron job 定时触发

### Cron 配置示例

```json
{
  "label": "morning-briefing",
  "schedule": "30 7 * * *",
  "timezone": "Asia/Shanghai",
  "task": "执行晨报系统。请读取 SKILL.md 获取完整流程指引，然后按步骤执行：1.清理新闻池 2.多轮搜索采集50+条科技新闻 3.评分分类 4.按分组格式化晨报 5.推送 6.同步飞书文档 7.更新池和名言记录。",
  "timeout": 120
}
```
