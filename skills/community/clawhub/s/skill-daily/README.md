# ClawHub Daily Skill 洞察

> 每日扫描 ClawHub 全球 AI Agent Skill 平台，生成多维度精选简报，自动推送飞书

> **📌 命名说明**：本项目在 GitHub 仓库为 `clawhub-daily`；在 ClawHub 市场注册名为 `skill-daily`（因 ClawHub 保护 `clawhub-` 命名空间）。两个名字指向同一个 Skill。

[![Status](https://img.shields.io/badge/status-active-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Schedule](https://img.shields.io/badge/schedule-every%202%20days-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Modes](https://img.shields.io/badge/modes-interactive%20%2F%20cron-purple)]()

## 🌐 English

**ClawHub Daily** is an Agent Skill that scans 200 Skills from ClawHub (the global AI Agent Skill platform) every day, picks 8-10 most valuable ones through 4-dimension rotation + 7 pain-point matching + 10-day deduplication, and pushes a full brief to Lark/Feishu.

- **Real data**: ClawHub Convex API (not hardcoded)
- **4-dimension rotation**: trending / quality / newcomers / panorama
- **7 pain-points**: 🤖 automation / 🛠️ dev / ✍️ content / 🕷️ scraping / 🧠 AI / 🇨🇳 Chinese / 💰 finance
- **10-day dedup**: avoid repeated recommendations
- **Bilingual brief**: Chinese one-liner + English `<details>`
- **Lark/Feishu push**: cloud doc + 200-400 char card message

---

## ✨ 核心能力

- 🎯 **真实数据**：从 ClawHub Convex API 抓取 Top 200 Skill（不是硬编码）
- 🔄 **4 维度轮换**：趋势 / 质量 / 新星 / 全景，按日期自动切换
- 🚫 **10 天去重**：自动避免重复推荐（10 天滚动窗口 = 5 个独立周期全覆盖）
- 🎨 **痛点匹配**：基于 7 大场景库个性化推荐
- 🇨🇳 **简报中文化**：中文一句话 + 英文原文 `<details>` 折叠
- 📊 **多模块简报**：热装、口碑、新星、痛点、热议、分类王者
- 📤 **多通道推送**：飞书云文档 + 卡片消息 / IMA 知识库 / 本地 Markdown

## 🎯 使用模式（二选一）

ClawHub Daily 提供 **2 种使用模式**，**首次安装后请阅读** [`references/setup-wizard.md`](references/setup-wizard.md) 选择：

| 模式 | 适合 | 触发方式 |
|------|------|---------|
| 💬 **A 常规对话** | 每天手动调用 | 在 Agent 对话中输入"每日推荐"、"ClawHub 日报"等 |
| ⏰ **B Cron 定时** | 每天自动推送 | 参考 [`references/prompt-templates.md`](references/prompt-templates.md) 配置 |

**推荐默认**：模式 B + 每 2 天 1 次（与 10 天去重窗口完美匹配）。

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
│   ├── config.json                   # 凭证配置（用户自填）
│   ├── api-contract.md               # Convex API 详细参数
│   ├── source-data-schema.md         # 数据字段说明
│   ├── briefing-template.md          # 简报模板
│   └── pain-points.md                # 痛点库
├── scripts/
│   ├── fetch_clawhub.py              # 抓取 200 个 Skill
│   ├── compute_metrics.py            # 指标计算
│   ├── daily_recommend.py            # 推荐生成
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
3. 按日期自动选维度，生成 8-10 个推荐
4. 创建飞书云文档
5. 发送 200-400 字卡片消息

### 方式 2：分步执行

```bash
# Step 1: 抓取数据
python scripts/fetch_clawhub.py --num 200 --date 2026-06-03 --output data/snapshots

# Step 2: 计算指标
python scripts/compute_metrics.py --input data/snapshots/2026-06-03.json

# Step 3: 生成推荐
python scripts/daily_recommend.py --date 2026-06-03 --data-dir data

# Step 4: 推送到飞书
python scripts/push_to_feishu.py --recommendation data/recommended/2026-06-03.json
```

### 方式 3：仅生成推荐（不推送）

```bash
python clawhub_daily_executor.py --skip-push
```

## ⚙️ 配置

### 飞书凭证

凭证**不硬编码**在代码中，**必须**通过以下两种方式之一提供：

#### 方式 A：编辑 `references/config.json`（推荐）

```json
{
  "feishu_app_id": "<your_feishu_app_id>",
  "feishu_app_secret": "<your_feishu_app_secret>",
  "feishu_user_open_id": "<your_user_open_id>"
}
```

#### 方式 B：命令行参数

```bash
python scripts/push_to_feishu.py \
  --recommendation path/to/recommendation.json \
  --app-id <your_app_id> \
  --app-secret <your_app_secret> \
  --user-open-id <your_open_id>
```

> 🔒 **`references/config.json` 已加入 `.gitignore`**，请勿将真实凭证提交到 GitHub。

### 抓取数量

```bash
python scripts/fetch_clawhub.py --num 500  # 抓 500 个
```

### 排序方式

```bash
python scripts/fetch_clawhub.py --sort stars  # 按星标排序
python scripts/fetch_clawhub.py --sort installs  # 按安装量
```

支持的 `sort`：`downloads` / `installs` / `stars` / `updated` / `recommended`

### 推荐维度

每天自动按 `日期 % 4` 选择维度：
- D1 (trending): 今日热装 - `installsCurrent` 高
- D2 (quality): 口碑精品 - `star_rate` 高
- D3 (newcomers): 新星崛起 - `age_days` 小且 `installsCurrent` ≥ 10
- D4 (panorama): 分类王者 - `comments` 多

手动指定：
```bash
python scripts/daily_recommend.py --date 2026-06-03 --dimension quality
```

### 去重窗口

```bash
python scripts/daily_recommend.py --date 2026-06-03 --lookback-days 14
```

### 推荐数量

```bash
python scripts/daily_recommend.py --date 2026-06-03 --target 8
```

## 📊 输出物

| 文件 | 内容 |
|------|------|
| `data/snapshots/<date>.json` | 当日 200 个 Skill 原始数据 |
| `data/snapshots/<date>.metrics.json` | 计算后的指标（star_rate 等）|
| `data/recommended/<date>.md` | 简报 Markdown |
| `data/recommended/<date>.json` | 推荐结果（含飞书 blocks）|

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
   daily_recommend.py ───── 读取 10 天历史
        │                       │
        │                       ▼
        │                 去重 + 痛点加权
        │                       │
        ▼                       ▼
   <date>.json 推荐结果
   <date>.md 简报
        │
        ▼
   push_to_feishu.py
        │
        ▼
   飞书云文档 + 卡片消息
```

## 🛠️ 维护指南

### 调整痛点优先级

编辑 `references/pain-points.md` 和 `scripts/daily_recommend.py` 中的 `PAIN_POINTS_DB`，调整各场景的 `weight` 值。

### 添加新场景

1. 在 `references/pain-points.md` 添加场景定义
2. 在 `scripts/daily_recommend.py` 的 `PAIN_POINTS_DB` 同步
3. 重新运行推荐生成

### 调整维度规则

编辑 `scripts/daily_recommend.py` 中的 `DIMENSION_CONFIG`：
```python
"quality": {
    "filter_fn": lambda s: s['downloads'] >= 1000 and s['star_rate'] >= 0.5,
    "sort_field": "star_rate",
    ...
}
```

### 查看历史推荐

```bash
ls data/recommended/
cat data/recommended/2026-06-03.md
```

## 🐛 故障排查

### 抓取失败

- 检查网络能否访问 `wry-manatee-359.convex.cloud`
- 查看 `data/snapshots/<date>.json` 是否生成
- 错误码含义见 [api-contract.md](references/api-contract.md)

### 推荐为空

- 检查 `data/snapshots/<date>.metrics.json` 是否生成
- 确认 `data/recommended/` 目录下有过去 10 天的 JSON（用于去重）
- 调整 `DIMENSION_CONFIG` 的 `filter_fn` 降低门槛

### 飞书推送失败

- 确认 `references/config.json` 的凭证有效（或检查命令行参数）
- 确认 `user_open_id` 是 P2P 对话对象（需先发过消息）
- 检查飞书云文档 block 数量（< 200 为宜）
- 查看 [setup-wizard.md](references/setup-wizard.md) 的"飞书应用创建"步骤

## ⏰ 定时任务配置

详细模板见 [`references/prompt-templates.md`](references/prompt-templates.md)，支持：

- Trae SOLO（推荐）
- qclaw / WorkBuddy / OpenClaw / Hermes
- Linux/Mac crontab
- Windows Task Scheduler

默认建议：每 2 天 1 次（与 10 天去重窗口完美匹配 → 5 个独立周期全覆盖 200 个 Skill）。

## 📌 已知限制

- **数据源单一**：仅 ClawHub Convex API，不抓取 SkillHub
- **单次最多抓 200 个**：Convex 翻页稳定上限
- **去重窗口 10 天**：超出 10 天的会重新推荐（用户可配置）
- **推荐数量上限 10**：避免信息过载
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

欢迎 PR！请参考 [CONTRIBUTING.md](docs/CONTRIBUTING.md)（如有）。

## 📜 版本

- **v1.0.0** (2026-06-03) - 初始版本，参考 skillhub-daily v6.2.0 架构设计

## 📄 License

MIT © clawhub-daily contributors
