# 🐙 SkillHub Daily — 国内技能洞察

> 每日扫描 SkillHub.cn 7.5 万+ 技能生态，7 维度推荐 8 个技能，聚焦**国内适配**与**活跃开发者**

[English](./README.en.md) | 中文

![Version](https://img.shields.io/badge/版本-7.0.1-blue)
![Platform](https://img.shields.io/badge/平台-SkillHub.cn-green)
![License](https://img.shields.io/badge/许可证-MIT--0-orange)

---

## 什么是 SkillHub Daily？

SkillHub Daily 是一个每日推荐引擎，扫描 SkillHub.cn 的 7 大排行榜 + 11 分类搜索 + 关键词搜索（1000+ 候选），通过 7 维度算法精选 8 个技能推荐给你。

与 [ClawHub Daily](https://clawhub.ai) 互补：ClawHub Daily 聚焦口碑精品与趋势洞察（500 技能），SkillHub Daily 聚焦**国内适配**、**活跃开发者发现**、**双实验室安全审计**（7.5 万+ 技能）。

## 核心特色

| 特色 | 说明 |
|------|------|
| 🇨🇳 国内优先 | 重点推荐适配国内生态的技能（飞书/微信/钉钉/小红书/抖音等） |
| 👤 活跃开发者 | 发现高产开发者及其代表作，追踪值得关注的技能作者 |
| 🔬 安全审计 | 调用 skillhub skill reports 获取双实验室安全评估 |
| 📊 AI 质量评估 | 调用 skillhub skill evaluation 获取 6 维度评分 |
| 🧠 3级权重记忆碰撞 | project_memory×3 / topics×2 / user_profile×1 |
| 🚫 7天去重 | 跨维度去重，避免重复推荐 |

## 7 维度推荐算法

| 维度 | 数量 | 说明 |
|------|------|------|
| 🔥 趋势飙升 | 2 | 同时登上 hot + trending 双榜 |
| 🚀 新星上线 | 1 | 30 天内上线 + installs > 100 |
| 🎯 痛点匹配 | 2 | 7 大痛点场景库匹配 |
| 🧠 记忆碰撞 | 1 | 3 级权重关键词碰撞 |
| 🇨🇳 国内优先 | 1 | 国内适配信号检测（25 个关键词） |
| 👤 活跃开发者 | 1 | 高产开发者的代表作 |
| 🏢 官方认证 | 1(可选) | verified=true |

## 安装

```bash
# 1. 安装 skillhub CLI
npm i -g skillhub

# 2. 登录
skillhub auth login

# 3. 克隆技能
git clone https://github.com/EdwardWason/skillhub-daily.git
```

## 使用

### 手动执行

```bash
# 一键执行（抓取 → 推荐 → 三处存放）
python skillhub_cn_daily_executor.py

# 只生成简报，不推送
python skillhub_cn_daily_executor.py --skip-push

# 跳过深度评估（节省时间）
python skillhub_cn_daily_executor.py --skip-eval
```

### 定时任务

已配置 TRAE Schedule 定时任务（ID: be17fc27），每天北京时间 06:50 自动执行。

> **用户须知**：运行本技能会自动将推荐简报写入 Obsidian、IMA 知识库、飞书云文档。简报中包含基于本地项目记忆关键词的推荐结果（不含原始记忆内容）。如不需推送，使用 `--skip-push` 参数。

## 三处存放

| 目的地 | 方式 | 配置 |
|--------|------|------|
| Obsidian inbox | Markdown + frontmatter | OBSIDIAN_VAULT_PATH |
| IMA FIM 知识库 | 两步流程（create_note + add_knowledge） | IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY / IMA_KB_ID |
| 飞书云文档 | lark-cli / lark-doc skill | 飞书授权 |

> **凭证安全**：所有凭证通过环境变量传递，不硬编码在代码中。请确保环境变量仅在本地配置，不要写入 .env 文件并提交到版本控制。

## 与 ClawHub Daily 互补

| | SkillHub Daily | ClawHub Daily |
|---|---|---|
| 平台 | SkillHub.cn（7.5 万+） | ClawHub.ai（500） |
| 特色 | 🇨🇳 国内优先 / 👤 开发者 / 🔬 安全审计 | 🦞 口碑精品 / 趋势洞察 |
| 评估 | AI 6维评分 + 双实验室审计 | 口碑率 + 活跃度 |
| 碰撞 | 3 级权重记忆碰撞 | 痛点关键词匹配 |

## 项目结构

```
skillhub-cn-daily/
├── SKILL.md                          # 技能定义
├── skillhub_cn_daily_executor.py     # 一键执行器
├── scripts/
│   ├── fetch_skillhub_cn.py          # 数据抓取
│   └── daily_recommend.py            # 推荐算法
├── data/                             # 运行时数据（gitignore）
│   ├── snapshots/                    # 扫描快照
│   └── recommended/                  # 推荐结果
├── .claude-plugin/plugin.json        # 插件配置
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## 依赖

- Python 3.8+
- skillhub CLI（`npm i -g skillhub`）
- 已登录 skillhub auth

## 许可证

MIT-0
