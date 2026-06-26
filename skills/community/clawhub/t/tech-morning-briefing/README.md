# ☀️ Tech Morning Briefing

<div align="center">

**每日科技晨报 · 三级分选 · 分组推送**

[![ClawHub](https://img.shields.io/badge/ClawHub-tech--morning--briefing-blue?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMCIgY3k9IjEwIiByPSI4IiBmaWxsPSIjNjBBN0ZGIi8+PC9zdmc+)](https://clawhub.ai)
[![GitHub](https://img.shields.io/badge/GitHub-uuoov%2Ftech--morning--briefing-black?logo=github)](https://github.com/uuoov/tech-morning-briefing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 这是什么？

一个 [OpenClaw](https://openclaw.ai) Agent Skill，每天早上自动帮你筛选科技新闻，推到飞书。

不是简单聚合 RSS——它会**采集 50+ 条新闻 → 评分筛选 → 分组归类 → 精选 8-10 条**，标题 AI 重写，摘要言之有物，最后按领域分组推送。

## 推送长什么样？

```
☀️ 晨报 | 2026年5月12日 星期一

━━━━━━━━━━━━━━━━━━━━

🧠 AI & 模型

⭐ Anthropic租下SpaceX 22万GPU超算
   推理算力军备竞赛再升级——独家租用Colossus 1全部算力，22万GPU、300MW
   🔗 VentureBeat

  DeepSeek V4开源：华为昇腾训练，推理成本降73%
   1.6T参数MIT协议开源，HuggingFace权重已上线
   🔗 CNBC

🔧 产品 & 工具

  OpenAI双发：GPT-Realtime-2 + Codex Chrome
   实时语音接入GPT-5推理，浏览器插件六个月ARR破10亿
   🔗 MacRumors

🚗 产业 & 硬件

⭐ 新能源车集体涨价：15+车企调价，智驾成分水岭
   比亚迪上调智驾包、特斯拉收缩金融，单车涨2千-1万
   🔗 网通社

📋 政策 & 动态

  L2辅助驾驶国标征求意见，驾驶员为第一责任主体
   华为小米比亚迪特斯拉联合起草，违规脱手强制禁用
   🔗 IT之家

━━━━━━━━━━━━━━━━━━━━

💬 "Artificial intelligence is the new electricity." — Andrew Ng
```

## 工作原理

```
┌─────────────────────────────────────────────────────┐
│                   每日定时触发 (cron)                  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  第一级：采集                                          │
│  6-8轮 web_search，关键词+freshness:week              │
│  覆盖 36kr/量子位/机器之心/TechCrunch/TheVerge 等     │
│  目标 50+ 条原始新闻，URL 去重                         │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  第二级：评分 + 分类                                    │
│  四维评分：影响力(0.3) / 新颖性(0.25) /               │
│          深度(0.2) / 相关性(0.25)                      │
│  分数 ≥7.0 → high  |  5.0-6.9 → medium  |  <5 → 丢弃  │
│  同时标记分类：ai / product / industry / policy        │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  第三级：精选推送                                       │
│  从 high 中选 8-10 条，覆盖 2-4 个分类                  │
│  每组最重磅标 ⭐，标题 AI 重写，摘要要求有具体信息       │
│  → 飞书聊天推送 + 归档文档追加                          │
└──────────────────────────────────────────────────────┘
```

## 四大分类

| 分类 | 标识 | 包含范围 |
|------|:----:|---------|
| **AI & 模型** | 🧠 | 大模型发布、AI 研究、算力基础设施、训练/推理突破 |
| **产品 & 工具** | 🔧 | 新产品发布、开发者工具、平台更新、应用层创新 |
| **产业 & 硬件** | 🚗 | 智能汽车、芯片半导体、制造、新能源、机器人 |
| **政策 & 动态** | 📋 | 监管法规、国标、融资、行业趋势、人事变动 |

分类优先级：跨类新闻按最核心属性归类。如"DeepSeek V4 用华为芯片训练"→ `ai`（模型是核心），而非 `industry`。

政策/时政类新闻不超过当日推送的 20%。

## 评分机制

| 维度 | 权重 | 判定标准 |
|------|:----:|---------|
| **影响力** | 30% | 影响了多少公司/用户？头部公司还是小团队？国家级政策还是地方性通知？ |
| **新颖性** | 25% | 独家首发还是旧闻重发？是否有新数据/新产品/新结论？ |
| **深度** | 20% | 有实质内容还是标题党？是否包含具体数字、技术细节、产品名？ |
| **相关性** | 25% | 和科技直接相关还是边缘沾边？政策类需涉及科技才不扣分 |

## 新闻池管理

每天的新闻不是用完就丢——池子会跨天维护：

- **carryOver**：高分但今天没被选中的新闻，保留到明天继续候选
- **自动过期**：`fetchedAt` 超过 3 天的自动清理
- **中等降级**：`medium` 级新闻保留一天，第二天还在就降为 discarded
- **容量上限**：100 条，超了按分数从低到高删

## 安装

### 从 ClawHub（推荐）

```bash
clawhub install tech-morning-briefing
```

### 手动安装

```bash
git clone https://github.com/uuoov/tech-morning-briefing.git ~/.openclaw/workspace/skills/morning-briefing
```

## 配置

### 前置依赖

| 依赖 | 说明 | 配置方式 |
|------|------|---------|
| **Tavily API Key** | 搜索引擎（替代 DuckDuckGo） | 在 `.env` 中设置 `TAVILY_API_KEY`，配置 `tools.web.search.provider: tavily` |
| **飞书应用** | 推送消息 + 文档同步 | OpenClaw feishu channel 开启 `feishu_doc` 工具即可 |
| **OpenClaw cron** | 定时触发 | 见下方 cron 配置 |

### 创建 Cron Job

```bash
openclaw cron create \
  --label morning-briefing \
  --schedule "30 7 * * *" \
  --timezone "Asia/Shanghai" \
  --task "执行晨报系统。请读取 SKILL.md 获取完整流程指引，然后按步骤执行：1.清理新闻池 2.多轮搜索采集50+条科技新闻 3.评分分类 4.按分组格式化晨报 5.推送 6.同步飞书文档 7.更新池和名言记录。" \
  --timeout 120
```

### 自定义

| 想改什么 | 改哪里 |
|---------|--------|
| 新闻来源/搜索策略 | 编辑 `SKILL.md` 中的搜索策略表 |
| 分类定义/归类逻辑 | 修改 `SKILL.md` 中"分类规则"一节 |
| 名言库 | 编辑 `data/quotes-used.json` 的 `pool` 数组 |
| 飞书归档文档 | 首次运行自动创建，token 存于 `data/config.json` |
| 推送时间/频率 | 修改 cron schedule |

## 文件结构

```
morning-briefing/
├── SKILL.md               # 完整流程指引（agent 运行时读取）
├── README.md              # 本文件
├── .gitignore             # 忽略 data/ 目录
└── data/                  # 运行时数据（不纳入版本控制）
    ├── config.json        # 飞书文档 token、文件夹 token
    ├── news-pool.json     # 新闻池（评分、分类、状态）
    └── quotes-used.json   # 名言轮换记录
```

## 飞书文档同步

晨报不仅推到聊天，还会追加到飞书归档文档：

1. **首次运行**：自动创建「晨报存档」文档，`doc_token` 存入 `config.json`
2. **后续运行**：每天 append 当天内容，按分组格式归档
3. **权限**：文档 owner 设为用户 open_id，确保完整访问权限

归档格式示例：

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

## FAQ

**Q: 为什么不用 RSS？**
A: web_search + Tavily 能覆盖更广的来源，不受 RSS feed 限制，还能按关键词灵活搜索。

**Q: 为什么不用 `site:` 限定搜索？**
A: 实测发现 `site:` 限定容易返回索引页和标签页而非具体文章，用广泛关键词 + `freshness:week` 效果更好。

**Q: 可以换推送渠道吗？**
A: 目前支持飞书。OpenClaw 支持 Telegram/Discord/微信等渠道，改 cron 的 announce target 即可。

**Q: 池子会越来越大吗？**
A: 不会。上限 100 条，自动清理过期和低分新闻。carryOver 最多多留 1 天。

**Q: 名言用完了怎么办？**
A: 内置 20 条，用完后自动重置轮换池。你也可以往 `quotes-used.json` 的 `pool` 里加新的。

## 致谢

- [OpenClaw](https://openclaw.ai) — Agent 运行时
- [Tavily](https://tavily.com) — 搜索 API
- [ClawHub](https://clawhub.ai) — Skill 分发

## License

[MIT](LICENSE)
