# ClawHub Daily Skill 洞察

> 每日扫描 ClawHub 全球 AI Agent Skill 平台，6 维度全维度精选简报

> **⚠️ 数据出口说明**：简报默认写入本地文件；若配置了飞书/IMA 凭证，会推送到飞书云文档和腾讯 IMA 知识库。未配置凭证时仅生成本地文件，不执行外部推送。详见 [SKILL.md](SKILL.md) 的"数据出口说明"。

> **📌 命名说明**：本项目在 GitHub 仓库为 `clawhub-daily`；在 ClawHub 市场注册名为 `skill-daily`（因 ClawHub 保护 `clawhub-` 命名空间）。两个名字指向同一个 Skill。

[![Status](https://img.shields.io/badge/status-active-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.4-blue)]()
[![Schedule](https://img.shields.io/badge/schedule-daily-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Modes](https://img.shields.io/badge/modes-interactive%20%2F%20cron-purple)]()

## 🌐 English

**ClawHub Daily** is an Agent Skill that scans 200 Skills from ClawHub (the global AI Agent Skill platform) every day, picks 6 most valuable ones through all-dimension daily recommendation + 7 pain-point matching + 7-day deduplication, and pushes a full brief to Lark/Feishu.

- **Real data**: ClawHub Convex API (not hardcoded)
- **All-dimension daily**: trending×2 / quality×1 / newcomers×1 / panorama×2 = 6 per day
- **7 pain-points**: 🤖 automation / 🛠️ dev / ✍️ content / 🕷️ scraping / 🧠 AI / 🇨🇳 Chinese / 💰 finance
- **7-day dedup**: avoid repeated recommendations
- **Bilingual brief**: Chinese one-liner + English `<details>`
- **Lark/Feishu push**: cloud doc + card message with direct link

---

## ✨ 核心能力

- 🎯 **真实数据**：从 ClawHub Convex API 抓取 Top 200 Skill（不是硬编码）
- 🔄 **全维度每日推荐**：趋势×2 + 质量×1 + 新星×1 + 全景×2 = 每日 6 个，每天看全貌
- 🚫 **7 天去重**：自动避免重复推荐（7 天滚动窗口，跨维度去重）
- 🎨 **痛点匹配**：基于 7 大场景库个性化推荐
- 🇨🇳 **简报中文化**：中文一句话 + 英文原文 `<details>` 折叠
- 📊 **多模块简报**：热装、口碑、新星、痛点、热议、分类王者
- 📤 **多通道推送**：飞书云文档 + 卡片消息 / IMA 知识库 / 本地 Markdown
- 🔗 **可点击链接**：云文档和 Markdown 中 Skill 名称/链接均可直接点击跳转

## 🎯 使用模式（二选一）

ClawHub Daily 提供 **2 种使用模式**，**首次安装后请阅读** [`references/setup-wizard.md`](references/setup-wizard.md) 选择：

| 模式 | 适合 | 触发方式 |
|------|------|---------|
| 💬 **A 常规对话** | 手动调用 | 在 Agent 对话中输入"每日推荐"、"ClawHub 日报"等 |
| ⏰ **B Cron 定时** | 每天自动推送 | 参考 [`references/prompt-templates.md`](references/prompt-templates.md) 配置 |

**推荐默认**：模式 B + 每天 1 次（全维度推荐，每日 6 个）。

## 📦 技能包结构

```
clawhub-daily/
├── SKILL.md                          # 技能说明
├── README.md                         # 本文档
├── CHANGELOG.md                      # 变更日志
├── LICENSE                           # MIT 协议
├── .claude-plugin/
│   └── plugin.json                   # ClawHub 发布元数据
├── .gitignore                        # Git 忽略规则
├── references/
│   ├── setup-wizard.md               # 首次安装模式选择
│   ├── prompt-templates.md           # Cron 提示词模板
│   ├── config.json                   # 凭证配置模板（占位符）
│   ├── config.local.json             # 本地凭证（不入 Git，不发布）
│   ├── api-contract.md               # Convex API 详细参数
│   ├── source-data-schema.md         # 数据字段说明
│   ├── briefing-template.md          # 简报模板
│   └── pain-points.md                # 痛点库
├── scripts/
│   ├── fetch_clawhub.py              # 抓取 200 个 Skill
│   ├── compute_metrics.py            # 指标计算
│   ├── daily_recommend.py            # 推荐生成（全维度）
│   └── push_to_feishu.py             # 飞书推送
└── data/
    ├── snapshots/                    # 原始快照
    └── recommended/                  # 推荐结果 + Markdown
```

## 🚀 快速开始

### 方式 1：完整流程（推荐）

```bash
# 进入技能目录
cd clawhub-daily

# 一键执行：抓取 → 指标 → 推荐 → 飞书
python clawhub_daily_executor.py
```

执行器会自动：
1. 抓取 200 个 Skill（10-15 秒，0 token）
2. 计算 5 大指标
3. 全维度推荐 6 个 Skill（趋势×2 + 质量×1 + 新星×1 + 全景×2）
4. 创建飞书云文档
5. 发送卡片消息（含云文档直达链接）

### 方式 2：分步执行

```bash
# Step 1: 抓取数据
python scripts/fetch_clawhub.py --num 200 --date 2026-06-05 --output data/snapshots

# Step 2: 计算指标
python scripts/compute_metrics.py --input data/snapshots/2026-06-05.json

# Step 3: 生成推荐（默认全维度）
python scripts/daily_recommend.py --date 2026-06-05 --data-dir data

# Step 4: 推送到飞书
python scripts/push_to_feishu.py --recommendation data/recommended/2026-06-05.json
```

### 方式 3：仅生成推荐（不推送）

```bash
python clawhub_daily_executor.py --skip-push
```

## ⚙️ 配置

### 飞书凭证

凭证**不硬编码**在代码中，**必须**通过以下方式之一提供（优先级从高到低）：

1. **CLI 参数**：`--app-id` / `--app-secret` / `--user-open-id`
2. **环境变量**：`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_USER_OPEN_ID`
3. **config.local.json**（推荐）：复制 `config.json` 为 `config.local.json`，填入真实值（不入 Git）
4. **config.json**：占位符模板，适合公开仓库

```json
// references/config.local.json（不入 Git，不发布）
{
  "feishu_app_id": "<your_feishu_app_id>",
  "feishu_app_secret": "<your_feishu_app_secret>",
  "feishu_user_open_id": "<your_user_open_id>"
}
```

> 🔒 **`references/config.local.json` 已加入 `.gitignore`**，请勿将真实凭证提交到 GitHub。

### 推荐维度

默认全维度模式（每日推荐 6 个）：

| 维度 | 配额 | 过滤条件 | 价值 |
|------|------|---------|------|
| 🔥 trending | 2 | installsCurrent ≥ 100 | 跟热度走 |
| ⭐ quality | 1 | downloads ≥ 1000 且 star_rate ≥ 0.5% | 跟口碑走 |
| 🚀 newcomers | 1 | age_days ≤ 60 + installs ≥ 10 + stars ≥ 3 | 抓潜力股 |
| 🏆 panorama | 2 | comments ≥ 1 | 看社区讨论 |

单维度模式（兼容旧版）：
```bash
python scripts/daily_recommend.py --date 2026-06-05 --dimension quality
```

### 去重窗口

```bash
python scripts/daily_recommend.py --date 2026-06-05 --lookback-days 14
```

默认 7 天（7×6=42 个去重池）。

## 📊 输出物

| 文件 | 内容 |
|------|------|
| `data/snapshots/<date>.json` | 当日 200 个 Skill 原始数据 |
| `data/snapshots/<date>.metrics.json` | 计算后的指标（star_rate 等）|
| `data/recommended/<date>.md` | 简报 Markdown（Skill 链接可点击）|
| `data/recommended/<date>.json` | 推荐结果（含飞书 blocks + 维度统计）|

## 🔍 数据流程图

```
   ClawHub Convex API
        │
        ▼
   fetch_clawhub.py
        │
        ▼
   <date>.json (200 个 Skill)
        │
        ▼
   compute_metrics.py
        │
        ▼
   <date>.metrics.json
        │
        ▼
   daily_recommend.py ───── 读取 7 天历史
        │                       │
        │                       ▼
        │                 全维度推荐 + 跨维度去重 + 痛点加权
        │                       │
        ▼                       ▼
   <date>.json 推荐结果
   <date>.md 简报
        │
        ▼
   push_to_feishu.py
        │
        ▼
   飞书云文档 + 卡片消息（含直达链接）
```

## 🛠️ 维护指南

### 调整痛点优先级

编辑 `references/pain-points.md` 和 `scripts/daily_recommend.py` 中的 `PAIN_POINTS_DB`，调整各场景的 `weight` 值。

### 添加新场景

1. 在 `references/pain-points.md` 添加场景定义
2. 在 `scripts/daily_recommend.py` 的 `PAIN_POINTS_DB` 同步
3. 重新运行推荐生成

### 调整维度配额

编辑 `scripts/daily_recommend.py` 中的 `DIMENSION_CONFIG`：
```python
"trending": {
    "filter_fn": lambda s: s['installs_current'] >= 100,
    "limit": 2,  # 每日配额
    ...
}
```

### 查看历史推荐

```bash
ls data/recommended/
cat data/recommended/2026-06-05.md
```

## 🐛 故障排查

### 抓取失败

- 检查网络能否访问 `wry-manatee-359.convex.cloud`
- 查看 `data/snapshots/<date>.json` 是否生成
- 错误码含义见 [api-contract.md](references/api-contract.md)

### 推荐为空

- 检查 `data/snapshots/<date>.metrics.json` 是否生成
- 确认 `data/recommended/` 目录下有过去 7 天的 JSON（用于去重）
- 调整 `DIMENSION_CONFIG` 的 `filter_fn` 降低门槛

### 飞书推送失败

- 确认 `references/config.local.json` 的凭证有效
- 确认 `user_open_id` 是 P2P 对话对象（需先发过消息）
- 检查飞书云文档 block 数量（< 200 为宜）
- 查看 [setup-wizard.md](references/setup-wizard.md) 的"飞书应用创建"步骤

### 定时任务 Token 授权失败

- SOLO Schedule 启动的进程读不到环境变量，必须使用 `config.local.json`
- 详见 [`references/config.local.json`](references/config.json) 配置说明

## ⏰ 定时任务配置

详细模板见 [`references/prompt-templates.md`](references/prompt-templates.md)，支持：

- Trae SOLO（推荐）
- qclaw / WorkBuddy / OpenClaw / Hermes
- Linux/Mac crontab
- Windows Task Scheduler

默认建议：每天 1 次（全维度推荐，每日 6 个，7 天去重）。

## 📌 已知限制

- **数据源单一**：仅 ClawHub Convex API，不抓取 SkillHub
- **单次最多抓 200 个**：Convex 翻页稳定上限
- **去重窗口 7 天**：超出 7 天的会重新推荐（用户可配置）
- **新星维度候选少**：当前仅 2 个候选，可能经常空推荐
- **语言**：中文为主，英文原文 `<details>` 折叠（0 token 中文化方案）

## 📚 详细文档

- [SKILL.md](SKILL.md) - 技能说明
- [使用向导](references/setup-wizard.md) - 首次安装必读
- [Cron 提示词模板](references/prompt-templates.md) - 定时任务配置
- [API 契约](references/api-contract.md)
- [数据字段](references/source-data-schema.md)
- [简报模板](references/briefing-template.md)
- [痛点库](references/pain-points.md)
- [CHANGELOG](CHANGELOG.md) - 变更日志

## 🤝 贡献

欢迎 PR！请参考 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

## 📜 版本

- **v1.0.4** (2026-06-05) - 全维度每日推荐 + 7 天去重 + 飞书卡片优化 + 可点击链接
- **v1.0.3** (2026-06-05) - 修复 D4 阈值、dedup 语义、痛点词边界
- **v1.0.0** (2026-06-03) - 初始版本

## 📄 License

MIT-0 © clawhub-daily contributors
