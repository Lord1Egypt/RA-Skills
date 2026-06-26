---
name: skills-monitor
displayName: Skills Monitor — AI Skills 监控评估平台
slug: skills-monitor
description: AI Skills 一站式监控评估平台 — 7因子评估引擎、跨模型基准评测、中心化 Dashboard、智能推荐
version: 0.7.0
author: MerkyorLynn
license: GPL-3.0
tags: [monitoring, benchmark, evaluation, agent, skills, dashboard, diagnostic, recommendation]
categories: [Development, Monitoring, Testing, Productivity]
icon: 🩺
---

# 🩺 Skills Monitor — AI Skills 监控评估平台

> 🎯 对 AI Skills 进行**采集、评估、对比、推荐、诊断、上报**的一站式监控系统

## ✨ 核心能力

### 1. 7因子综合评估引擎
对每个 Skill 从 **成功率、延迟、质量、成本、稳定性、社区热度、兼容性** 七个维度进行量化评分，输出 0-100 综合得分。

### 2. 跨模型基准评测 (TOP1000 × 6 Models)
内置 1000 个热门 Skills 在 6 大主流模型上的完整评测数据：
- **Claude Opus 4.6** / **GPT-5.4** / **Gemini 3.0 Pro**
- **GLM-5** / **MiniMax 2.5** / **DeepSeek 3.2**
- 支持 `mock` (零成本模拟) 和 `live` (真实 API 调用) 两种模式
- 按 Skill × Model 精确返回差异化基准分数

### 3. 智能推荐引擎
- 基于评估得分 + 用户场景自动推荐最优 Skill
- 互补推荐：根据已安装 Skills 的空缺领域推荐
- 升级推荐：发现更优替代方案
- ClawHub 社区数据联动

### 4. 诊断报告系统
- 自动生成健康度评分 + 问题发现 + 优化建议
- 支持定时自动诊断 + 安装后自动诊断
- Markdown 格式报告，支持企微/微信推送

### 5. 中心化 Dashboard
- Web 实时面板（支持 PWA 移动端）
- 多 Agent 统一管理
- 微信小程序端查看
- 企业微信/微信公众号推送通知

### 6. 安全与合规
- OS Keychain 集成 (keyring)，零明文存储
- 敏感信息自动脱敏引擎
- GDPR 合规管理

## 🚀 快速开始

### 安装

通过 SkillsHUB 一键安装：

```bash
# 方式一：SkillsHUB CLI
skills install skills-monitor

# 方式二：手动安装
python install_skills.py skills-monitor
```

### 初始化

```bash
# 初始化身份（生成 Agent ID + API Key）
skills-monitor init

# 查看身份信息
skills-monitor identity --show-key
```

### 基本使用

```bash
# 查看系统状态
skills-monitor status

# 列出已安装 Skills
skills-monitor list

# 运行单个 Skill 并采集数据
skills-monitor run <skill-slug> [task]

# 7因子综合评估
skills-monitor evaluate --skill <slug>
skills-monitor evaluate              # 评估所有 Skills

# 基准评测
skills-monitor benchmark <slug> --runs 20

# 查询大模型基准分数
skills-monitor baseline <slug> --model claude-opus-4.6

# 对比分析
skills-monitor compare <slug>

# 智能推荐
skills-monitor recommend

# 生成综合日报
skills-monitor report

# 生成诊断报告（含推送）
skills-monitor diagnose --send

# 上报数据到中心化服务器
skills-monitor upload --server https://your-server.com --register
```

### 启动 Dashboard

```bash
# 本地 Web 面板
skills-monitor web --port 5050

# 中心化服务器（含 API + 微信回调 + PWA）
skills-monitor server --port 5100
```

### 作为 Python 库使用

```python
from skills_monitor import (
    SkillEvaluator,
    SkillRecommender,
    DiagnosticReporter,
    BatchBenchmark,
    ReportGenerator,
    DataUploader,
)

# 7因子评估
evaluator = SkillEvaluator(store, agent_id)
score = evaluator.evaluate_skill("your-skill-slug")

# 跨模型基准评测
bench = BatchBenchmark(mode="mock")
baseline = bench.get_baseline_for_skill("your-skill-slug", "claude-opus-4.6")

# 智能推荐
recommender = SkillRecommender(registry, store, agent_id)
recs = recommender.get_all_recommendations(max_per_type=5)

# 诊断报告
diag = DiagnosticReporter(store=store, registry=registry, agent_id=agent_id)
content, filepath = diag.generate_and_save(trigger="manual")

# 数据上报
uploader = DataUploader("https://your-server.com")
uploader.init(agent_id, api_key)
uploader.upload_daily()
```

## 📊 支持的命令

| 命令 | 说明 |
|------|------|
| `init` | 初始化身份（生成 Agent ID + API Key） |
| `identity` | 查看身份信息 |
| `status` | 查看系统状态 |
| `list` | 列出已安装 Skills |
| `evaluate` | 7因子综合评估 |
| `benchmark` | 基准评测运行 |
| `baseline` | 查询大模型基准分数 |
| `compare` | 对比分析 |
| `recommend` | 智能推荐 |
| `report` | 生成综合日报 |
| `diagnose` | 生成诊断报告（含推送） |
| `upload` | 数据上报到中心化服务器 |
| `dashboard` | 启动 Web 面板 |
| `server` | 启动中心化服务器 |

## 🏗️ 架构

```
skills-monitor/
├── skills_monitor/              # 核心 Python 包
│   ├── core/                    # 核心逻辑层
│   │   ├── identity.py          # 身份管理
│   │   ├── evaluator.py         # 7因子评估引擎
│   │   ├── benchmark.py         # 基准运行器
│   │   ├── recommender.py       # 推荐引擎
│   │   ├── diagnostic.py        # 诊断报告
│   │   ├── reporter.py          # 报告生成器
│   │   ├── uploader.py          # 数据上报
│   │   ├── llm_baseline.py      # LLM 基准评测
│   │   └── ...                  # 更多模块
│   ├── adapters/                # 适配器层
│   │   ├── skill_registry.py    # Skill 注册发现
│   │   ├── clawhub_client.py    # ClawHub 社区
│   │   └── runners.py           # 运行适配器
│   └── data/                    # 数据层
│       ├── store.py             # SQLite 存储
│       ├── gdpr_manager.py      # GDPR 合规
│       └── top1000_skills_dataset.json
├── server/                      # 中心化服务器
├── miniprogram/                 # 微信小程序
├── main.py                      # Skill 入口
├── skill.json                   # Skill 配置
└── requirements.txt             # 依赖清单
```

## 📦 依赖

- Python >= 3.9
- Flask >= 2.3.0
- Flask-SQLAlchemy >= 3.0.0
- requests >= 2.28.0
- pandas >= 1.5.0
- APScheduler >= 3.10.0
- keyring >= 25.0.0
- python-dotenv >= 1.0.0

## 🔗 生态集成

- **ClawHub**: 社区热度数据、Skill 下载安装
- **企业微信**: 诊断报告推送
- **微信公众号**: 报告查看 + 消息通知
- **微信小程序**: 移动端 Dashboard
- **PWA**: 渐进式 Web 应用支持

## 📄 许可证

GPL-3.0

## 👤 作者

MerkyorLynn — [GitHub](https://github.com/MerkyorLynn/skills-monitor)
