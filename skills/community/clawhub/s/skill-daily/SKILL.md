---
name: clawhub-daily
description: |
  每日扫描 ClawHub 全球 Skill 平台，结合多维数据（⭐/📥/installsCurrent/comments/capabilityTags）
  通过 4 维度轮换算法为用户推荐 8-10 个有价值、不重复、值得关注的 AI Agent Skill，
  并通过飞书推送完整简报。

  触发场景：
  - 用户希望每日/定时收到 ClawHub Skill 推荐简报
  - 用户希望跟踪 AI Agent 生态的最新 Skill 趋势
  - 用户希望按痛点场景（自动化办公/开发工具/内容创作/数据采集/AI 增强/中文支持/金融分析）匹配推荐
  - 用户希望避免重复推荐，结合 10 天历史去重

  核心能力：
  - 真实抓取 ClawHub Top 200 Skill（基于 Convex API，0 token 消耗）
  - 计算 5 大指标：star_rate、installsCurrent、活跃度、comments 热度、能力标签匹配
  - 4 维度轮换：趋势 / 质量 / 新星 / 全景（按 `日期 % 4` 自动选）
  - 10 天历史去重，避免重复推荐
  - 痛点加权：基于 7 大场景库个性化排序
  - 多模块简报：热装、口碑、新星、痛点、热议、分类王者
  - 飞书云文档 + 200-400 字卡片消息推送
  - 简报中文化：中文一句话 + 英文原文 `<details>` 折叠
---

# ClawHub Daily Skill 洞察技能

> 每日扫描 ClawHub 全球 AI Agent Skill 平台，生成多维度精选简报

## 核心能力

- **真实数据**：直接调用 ClawHub Convex API（`wry-manatee-359.convex.cloud`），抓取 Top 200 Skill
- **多维分析**：⭐ stars / 📥 downloads / `installsCurrent` / `installsAllTime` / `comments` / `capabilityTags` 6 大维度
- **4 维度轮换**：每天换一组推荐角度（趋势 / 质量 / 新星 / 全景）
- **10 天去重**：基于历史快照，10 天滚动窗口
- **痛点匹配**：基于 7 大场景库（自动化办公/开发工具/内容创作/数据采集/AI 增强/中文支持/金融分析）加权
- **简报中文化**：中文一句话解读 + 英文原文 `<details>` 折叠（0 token 消耗）
- **多模块简报**：6 大推荐模块 + 回顾 + 行动建议
- **飞书推送**：完整云文档 + 200-400 字飞书卡片消息

## 使用模式（二选一）

本技能支持 **2 种使用模式**，首次安装请阅读 [`references/setup-wizard.md`](references/setup-wizard.md)：

### 模式 A：常规对话模式 💬

**触发词**（在 Agent 对话中输入任一即可）：
- "每日推荐"
- "ClawHub 日报"
- "今天有什么好 Skill"
- "帮我推荐技能"
- "扫描 ClawHub"

### 模式 B：Cron 定时任务模式 ⏰

**支持平台**：Trae SOLO / qclaw / WorkBuddy / OpenClaw / Hermes / 纯脚本

**预制提示词**：见 [`references/prompt-templates.md`](references/prompt-templates.md)

**推荐节奏**：每 2 天 1 次（与 10 天去重窗口完美匹配 → 5 个独立周期全覆盖 200 个 Skill）

## 适用场景

- AI Agent 开发者跟踪生态趋势
- 内容创作者寻找新的 AI 工具
- 团队 leader 评估可纳入工作流的 Skill
- 对 ClawHub 平台感兴趣的所有用户

## 不适用场景

- 需要中文 Skill 专项分析（请使用 `skillhub-daily` 技能）
- 需要即时的单次查询（请直接使用 Convex `listPublicPageV4` API）
- 需要下载/安装 Skill 本身（本技能只做推荐分析）

## 依赖

- Python 3.8+
- `requests`（HTTP 抓取）
- 飞书应用凭证（可选，用于推送）
- 网络可访问 `wry-manatee-359.convex.cloud`

## 快速开始

### 1. 首次安装：选择使用模式

阅读 [`references/setup-wizard.md`](references/setup-wizard.md) 选择 A 或 B。

### 2. 配置凭证（仅模式 B 推送时需要）

编辑 `references/config.json`：
```json
{
  "feishu_app_id": "<your_feishu_app_id>",
  "feishu_app_secret": "<your_feishu_app_secret>",
  "feishu_user_open_id": "<your_user_open_id>"
}
```

### 3. 手动运行

```bash
# 抓取数据
python scripts/fetch_clawhub.py --num 200 --output data/snapshots/2026-06-03.json

# 计算指标
python scripts/compute_metrics.py --input data/snapshots/2026-06-03.json

# 生成推荐
python scripts/daily_recommend.py --date 2026-06-03 --dimension trending

# 4. 推送到飞书
python scripts/push_to_feishu.py --recommendation data/recommended/2026-06-03.json

# 5. 推送到 IMA 知识库（可选）
python scripts/push_to_ima.py --recommendation data/recommended/2026-06-03.json
```

### 4. 一键执行

```bash
python clawhub_daily_executor.py
```

## 推荐维度

| 维度 | cron 标识 | 重点模块 | 频率 |
|------|---------|---------|------|
| **D1 趋势** | `trending` | 热装 + 痛点 + 回顾 | 第 1, 5, 9, ... 天 |
| **D2 质量** | `quality` | 口碑 + 痛点 + 回顾 | 第 2, 6, 10, ... 天 |
| **D3 新星** | `newcomers` | 新星 + 痛点 + 回顾 | 第 3, 7, 11, ... 天 |
| **D4 全景** | `panorama` | 热议 + 分类 + 回顾 | 第 4, 8, 12, ... 天 |

维度根据 `日期 % 4` 自动计算。

## 输出物

- `data/snapshots/YYYY-MM-DD.json` - 当日 200 个 Skill 原始数据
- `data/snapshots/YYYY-MM-DD.metrics.json` - 计算后的指标
- `data/recommended/YYYY-MM-DD.json` - 8-10 个推荐结果
- `data/recommended/YYYY-MM-DD.md` - 简报 Markdown

## 飞书/IMA 消息结构

### 飞书卡片消息

包含：
- **标题**：🦞 ClawHub 每日洞察 | 日期（维度）
- **元信息**：扫描数、推荐数、去重数、匹配场景
- **Top 3 详细解读**：每个 Skill 含数据、推荐理由、下一步
- **CTA 按钮**：查看完整简报（飞书文档）
- **备注**：执行时间 + 数据日期

总字数控制在 **200-400 字**（让用户决定是否点开）。

### IMA 知识库推送

完整 Markdown 简报，含：
- 标题 + 元信息
- Top 10 推荐详情
- 痛点匹配分组
- 翻页式浏览，可在 IMA 内检索

## 详细文档

- [使用向导](references/setup-wizard.md) - **首次安装必读**
- [Cron 提示词模板](references/prompt-templates.md) - **定时任务必读**
- [API 契约](references/api-contract.md)
- [数据字段](references/source-data-schema.md)
- [简报模板](references/briefing-template.md)
- [痛点库](references/pain-points.md)
- [使用指南](README.md)
- [CHANGELOG](CHANGELOG.md)

## 限制与边界

- **数据源单一**：仅 ClawHub Convex API，不抓取 SkillHub
- **去重窗口 10 天**：超出 10 天的会重新推荐
- **简报长度 8-10 个**：超过不会推送（避免信息过载）
- **语言**：中文为主，英文原文 `<details>` 折叠（0 token 消耗方案）

## 版本

- v1.0.0 (2026-06-03) - 初始版本，参考 skillhub-daily v6.2.0 架构设计
