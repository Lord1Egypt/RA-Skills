---
name: clawhub-daily
slug: clawhub-daily-ai
displayName: ClawHub Daily
version: 2.0.8
summary: Daily ClawHub Skill insights with 6-dimension recommendation
license: MIT-0
description: |
  每日扫描 ClawHub 全球 Skill 平台（500 个 Skill），通过 6 维度全维度推荐算法
  为用户推荐 8 个有价值、不重复、值得关注的 AI Agent Skill，并通过多渠道推送完整简报。

  数据出口说明（用户知情同意）：
  - 飞书（Lark）：云文档 + 卡片消息（有凭证时自动推送，无凭证时跳过）
  - 腾讯 IMA 知识库：官方 OpenAPI 推送（方式 A，有凭证时自动推送）；若安装了 ima-skill CLI 则自动调用（方式 B）
  - Obsidian 本地 vault：inbox/clawhub-daily/ 子目录（默认开启，仅写入本地磁盘）。vault 不可写时 fallback 到脚本目录 saved/ 子目录
  - 本地文件：data/recommended/*.md 简报文件（默认开启，仅写入本地磁盘）
  推送行为：executor 会尝试所有渠道，每个渠道独立 try/except，有凭证则推送，无凭证则跳过，一处失败不阻断其他渠道。

  凭证来源（优先级：CLI 参数 > 环境变量 > config.json）：
  - 飞书：FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID 环境变量，或 references/config.json
  - IMA：IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY 环境变量，或 references/config.json
  - Obsidian：OBSIDIAN_VAULT_PATH 环境变量（默认 E:\Obsidian\md\inbox\clawhub-daily）
  未配置任何凭证时仅生成本地文件，不执行外部推送。
  本技能运行时不读取 GH_TOKEN、GITHUB_TOKEN 或其他与推荐功能无关的环境变量（GH_TOKEN 仅用于维护者发布新版本，见 docs/PUBLISHING_GUIDE.md）。

  🔐 权限声明（capabilities）：
  - network（必需）：访问 ClawHub API（wry-manatee-359.convex.cloud）抓取数据；有凭证时访问飞书 API（open.feishu.cn）和 IMA API（ima.qq.com）推送简报
  - filesystem（必需）：写入 data/snapshots/（原始数据）、data/recommended/（简报）、Obsidian vault inbox/clawhub-daily/（简报副本）、saved/（vault 不可写时的 fallback）
  - env_vars（可选）：FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID / IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY / OBSIDIAN_VAULT_PATH。未配置时仅生成本地文件
  - subprocess（可选）：auto 模式下若官方 API 失败，可能调用 ima-skill CLI 命令（需用户预装）
  不申请的权限：shell 执行（除 ima-skill CLI 外）、系统信息收集、GitHub 凭证读取（GH_TOKEN）、任意文件系统访问

  触发场景：
  - 用户希望每日/定时收到 ClawHub Skill 推荐简报
  - 用户希望跟踪 AI Agent 生态的最新 Skill 趋势
  - 用户希望按痛点场景（自动化办公/开发工具/内容创作/数据采集/AI 增强/中文支持/金融分析）匹配推荐
  - 用户希望避免重复推荐，结合 7 天跨维度去重

  核心能力：
  - 真实抓取 ClawHub Top 500 Skill（基于 Convex API，0 token 消耗）
  - 适配新 API 数据结构（stats.installs / categories / badges.verified / changelog）
  - 6 维度全维度推荐：trending / quality / newcomers / panorama / actively_maintained / verified
  - 降级策略：候选不足时自动放宽阈值（fallback_fn）
  - optional 维度：verified 候选为 0 时自动跳过，不占配额
  - 7 天跨维度去重，避免重复推荐
  - 痛点匹配去重展示：同一 Skill 只在第一个命中场景展示
  - changelog 展示：有最近变更摘要的 Skill 展示"最近变更"字段
  - 痛点加权：基于 7 大场景库个性化排序
  - 多渠道推送：飞书云文档 + Top 5 卡片消息 + IMA 知识库（可选）+ 本地 Markdown
  - 简报中文化：中文一句话 + 英文原文 `<details>` 折叠
---

# ClawHub Daily Skill 洞察技能

> 每日扫描 ClawHub 全球 AI Agent Skill 平台，生成 6 维度精选简报

## 核心能力

- **真实数据**：直接调用 ClawHub Convex API（`wry-manatee-359.convex.cloud`），抓取 Top 500 Skill
- **新 API 适配**：`stats.installs`（非 `installsCurrent`）、`categories`（非 `capabilityTags`）、`badges.verified`、`latestVersion.changelog` 等嵌套字段
- **6 维度全维度推荐**：每天遍历全部 6 个维度，用户每天看全貌
  - 🔥 trending × 3（活跃安装≥100，降级≥30）
  - ⭐ quality × 1（下载≥1000+口碑≥0.5%，降级≥500+0.3%）
  - 🚀 newcomers × 1（≤60天+安装≥10+星≥3，降级≤90天+5+2）
  - 🏆 panorama × 2（评论≥1）
  - 🔧 actively_maintained × 1（90天内更新+版本≥3，降级180天+版本≥2）
  - 🛡️ verified × 1（平台安全审计通过，候选为空时跳过）
- **降级策略**：候选不足时自动放宽阈值（fallback_fn）
- **optional 维度**：verified 候选为 0 时自动跳过，不占配额
- **7 天跨维度去重**：同一 Skill 在不同维度和不同天都不会重复
- **痛点匹配去重**：同一 Skill 只在第一个命中场景展示（按权重排序）
- **changelog 展示**：有最近变更摘要的 Skill 展示"最近变更"字段
- **痛点匹配**：基于 7 大场景库（自动化办公/开发工具/内容创作/数据采集/AI 增强/中文支持/金融分析）加权
- **简报中文化**：中文一句话解读 + 英文原文 `<details>` 折叠（0 token 消耗）
- **多渠道推送**：飞书云文档 + Top 5 卡片消息（默认）+ IMA 知识库（可选）+ 本地 Markdown

## ⚠️ 数据推送知情说明

本技能会生成推荐简报并可能推送到以下外部服务，请用户知悉：

| 推送渠道 | 默认状态 | 所需凭证 | 数据内容 |
|---------|---------|---------|---------|
| **本地文件** | 开启 | 无 | 完整简报 Markdown（data/recommended/*.md）|
| **飞书云文档+卡片消息** | 需配置 | feishu_app_id / app_secret / user_open_id | 完整简报 + Top 5 摘要卡片 |
| **腾讯 IMA 知识库** | 需配置 | ima_client_id / api_key / kb_id | 完整简报 Markdown |

**安全约束**：
- 未配置凭证的渠道不会执行推送，仅生成本地文件
- 凭证优先级：CLI 参数 > 环境变量 > `references/config.json`
- `references/config.json` 和 `references/config.local.json` 均在 `.gitignore` 中，不会上传到 GitHub
- IMA HTTP API 模式强制要求 HTTPS 端点（拒绝 HTTP，防止凭证明文传输）
- 本技能不读取 GH_TOKEN、GITHUB_TOKEN 或其他与推荐功能无关的环境变量
- 不会收集或传输用户系统信息或其他与推荐无关的数据

## 🔐 权限声明（capabilities）

本技能在 `plugin.json` 的 `capabilities` 字段中声明所有运行时所需的权限，供用户和宿主平台在执行前审查：

| 权限类别 | 是否必需 | 说明 |
|---------|---------|------|
| **network** | ✅ 必需 | 访问 ClawHub Convex API 抓取数据；可选访问飞书/IMA API 推送简报 |
| **filesystem** | ✅ 必需 | 写入 `data/snapshots/`（原始数据）和 `data/recommended/`（简报 Markdown）|
| **env_vars** | ❌ 可选 | 读取 `FEISHU_APP_ID`/`FEISHU_APP_SECRET`/`FEISHU_USER_OPEN_ID`/`IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY` 环境变量（未配置时仅生成本地文件）|

**不申请的权限**：shell 执行、系统信息收集、GitHub 凭证读取（GH_TOKEN）、任意文件系统访问。

## 使用模式（二选一）

本技能支持 **2 种使用模式**，首次安装请阅读 [`references/setup-wizard.md`](references/setup-wizard.md)：

### 模式 A：常规对话模式 💬

**触发词**（在 Agent 对话中输入任一即可）：
- "每日推荐"
- "ClawHub 日报"

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

### 飞书卡片消息（默认推送渠道）

包含：
- **标题**：🦞 ClawHub 每日洞察 | 日期（维度）
- **元信息**：扫描数、推荐数、去重数、匹配场景
- **Top 3 详细解读**：每个 Skill 含数据、推荐理由、下一步
- **CTA 按钮**：查看完整简报（飞书文档）
- **备注**：执行时间 + 数据日期

总字数控制在 **200-400 字**（让用户决定是否点开）。

### IMA 知识库推送（可选渠道，需显式配置）

通过 IMA 官方 OpenAPI 两步流程推送：
1. `import_doc` 创建笔记（Markdown 格式）
2. `add_knowledge` 添加到 FIM 知识库

凭证来源：`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` 环境变量（或 `references/config.json`）

默认推送到 FIM 知识库（ID: `aFEGG-4YH3z_CaCS...`），可通过 `--kb-id` 或 config.json 覆盖。

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
