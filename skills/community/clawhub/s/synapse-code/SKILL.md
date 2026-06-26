---
name: synapse-code
description: >
  Synapse Code — 智能代码开发工作流引擎。
  一体化完成项目初始化、代码交付、知识沉淀和影响分析。
  内建代码图谱引擎，越用越懂你的项目。
  当用户提到开发、实现功能、运行 pipeline、记录知识、检查影响范围时使用此技能。
version: 2.0.1
updated: 2026-04-15
date: 2026-04-10
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "requires": { "bins": ["python3", "npm"] },
        "install": [
          { "kind": "node", "package": "gitnexus", "bins": ["gitnexus"] }
        ],
        "homepage": "https://github.com/ankechenlab-node/synapse-code",
      },
  }
tags: [pipeline, workflow, knowledge-management, code-analysis, development, multi-agent, brain-compatible]
---

# Synapse Code Skill

**Synapse Code = 代码交付 + 知识沉淀 一体化工作流**

核心理念：开发不仅是写代码，更是知识积累的过程。

| | 传统开发 | Synapse Code |
|--|---------|--------------|
| **知识留存** | 随会话消失 | 自动沉淀到项目记忆 |
| **影响分析** | 手动追踪调用链 | 一键查询影响范围 |
| **项目状态** | 靠记忆回忆 | 实时可视化的进度 |
| **团队协作** | 口头传递上下文 | 可查询的知识库 |

---

## 🚦 快速决策：我该用什么模式？

```
你的任务是什么？
│
├─ 修复小 bug / 简单改动     → standalone（独立模式）
│   └─ 例："登录按钮点不了"、"改个文案"
│
├─ 日常功能开发             → lite（轻量模式）
│   └─ 例："加个导出功能"、"实现搜索"
│
├─ 大型模块 / 新功能         → full（完整模式）
│   └─ 例："设计整个订单系统"、"从零搭建 API"
│
└─ 复杂任务 / 多模块协作     → full + 并行模式
    └─ 例："同时开发前端和后端"、"拆分 5 个子任务"
```

**不想思考？直接用 `auto` 模式** — 系统会自动检测你的环境并推荐最佳模式。

---

## 📋 命令速查卡片

| 命令 | 用途 | 示例 |
|------|------|------|
| `/synapse-code init` | 初始化项目 | `/synapse-code init ~/my-project` |
| `/synapse-code run` | 运行 Pipeline | `/synapse-code run my-project "实现登录功能"` |
| `/synapse-code status` | 检查项目状态 | `/synapse-code status ~/my-project` |
| `/synapse-code query` | 查询历史记录 | `/synapse-code query ~/my-project --contains "登录"` |
| `/synapse-code log` | 手动记录知识 | `/synapse-code log ~/my-project` |

**常用组合**:
```bash
# 新项目开始
/synapse-code init ~/my-project
/synapse-code run my-project "设计用户系统"

# 日常开发
/synapse-code run my-project "修复登录 bug"
/synapse-code status my-project  # 检查进度

# 查询历史
/synapse-code query my-project --task-type bugfix --contains "认证"
```

---

## 六大场景支持

Synapse Code 支持 6 大场景，覆盖从代码开发到内容创作的全方位需求：

| 场景 | 典型任务 | Agent 团队 | 交付物 |
|------|---------|-----------|--------|
| **📝 文案写作** | 公众号文章、产品新闻稿、技术文档 | 选题策划 + 大纲策划 + 写作者 + 编辑 | 选题案 + 大纲 + 初稿 + 终稿 |
| **🎨 设计创作** | Logo 设计、UI 界面、海报、信息图表 | 需求分析 + 竞品调研 + 设计师 + 审核员 | 需求文档 + 竞品分析 + 设计方案 + 审核报告 |
| **📊 数据分析** | 销售分析、用户分析、竞品对比、数据可视化 | 数据工程师 + 分析师 + 可视化专家 + 报告撰写 | 数据集 + 分析报告 + 图表 + Dashboard |
| **🌐 翻译本地化** | 文档翻译、论文翻译、UI 本地化 | 术语专家 + 翻译员 + 校对员 + 本地化专家 | 术语表 + 翻译稿 + 校对报告 + 本地化版本 |
| **📚 学习研究** | 技术调研、竞品分析、文献综述、研究报告 | 文献研究员 + 阅读分析师 + 知识整理师 + 报告撰写 | 文献综述 + 分析报告 + 知识图谱 + 研究报告 |
| **💻 代码开发** | 功能开发、Bug 修复、系统设计、重构优化 | 需求分析师 + 架构师 + 开发工程师 + 测试工程师 + 运维工程师 | 需求文档 + 技术方案 + 代码 + 测试 + 部署清单 |

### 场景自动识别

系统会根据你的输入自动识别场景：

```
你：/synapse-code run my-project "写一篇公众号文章，介绍 AI 编程技巧"
     ↓
📝 检测到【文案写作场景】
     使用轻量模式（4 阶段）
     [1/4] 选题策划：分析受众...
     [2/4] 大纲策划：搭建结构...
     [3/4] 文案写作：撰写初稿...
     [4/4] 编辑润色：优化文案...
```

### 手动指定场景

```bash
# 文案写作
/synapse-code run my-project "写产品发布新闻稿" --scenario writing

# 设计创作
/synapse-code run my-project "设计一个简约现代的 logo" --scenario design

# 数据分析
/synapse-code run my-project "分析 Q3 销售数据" --scenario analytics

# 翻译本地化
/synapse-code run my-project "翻译技术文档到英文" --scenario translation

# 学习研究
/synapse-code run my-project "调研 RAG 技术的最新进展" --scenario research

# 代码开发（默认）
/synapse-code run my-project "实现登录功能"
```

---

## 三种工作模式

Synapse Code 提供三种工作模式，自动检测你的环境并选择最佳方案：

### 🚀 独立模式（新手推荐）
**无需任何配置，立即可用**

适合场景：
- 第一次使用，不想配置复杂环境
- 快速原型开发，简单功能实现
- 个人小项目，无需复杂流程

工作流程：
```
你：/synapse-code run my-project "实现登录功能"
     ↓
Claude 直接分析需求 → 生成代码 → 完成
```

### ⚡ 轻量模式（推荐）
**需要基础 Pipeline 配置，3-4 阶段简化流程**

适合场景：
- 日常功能开发
- 小团队协作
- 需要一定质量保证

工作流程：
```
代码开发：REQ（需求分析） → DEV（代码开发） → QA（质量检查）
文案写作：选题策划 → 大纲策划 → 文案写作 → 编辑润色
数据分析：数据收集 → 分析建模 → 可视化 → 报告撰写
```

### 🎯 完整模式（企业级）
**需要完整 Pipeline，6 阶段 SOP 流程**

适合场景：
- 大型项目开发
- 企业级应用
- 需要严格质量把控

工作流程：
```
代码开发：REQ → ARCH → DEV → INT → QA → DEPLOY
设计创作：需求分析 → 竞品调研 → 设计创作 → 设计审核 → ...
```

---

## 功能范围

1. **项目初始化检测** — 自动检测 `.knowledge/` `.synapse/` `.gitnexus/` 是否存在
2. **Pipeline 命令封装** — 提供简洁的 `pipeline run` 命令
3. **Auto-Log 触发** — Pipeline 成功后自动调用 `auto_log.py`
4. **Task Type 推断** — 根据需求描述自动推断 task_type
5. **代码图谱分析** — 内建 GitNexus 引擎，支持影响分析和调用链追踪

## 命令

### 初始化命令

```bash
# 初始化项目的 Synapse + Pipeline 环境
/synapse-code init [project_path]
```

执行内容：
1. 检测 `.git/` 存在
2. 调用 `scaffold.py` 创建 `.knowledge/` `.synapse/` 目录
3. 调用 `gitnexus analyze --force` 建图
4. 创建 pipeline 项目

### Pipeline 命令

```bash
# 运行完整 Pipeline
/synapse-code run [project_name] "需求描述"
```

### Auto-Log 命令

```bash
# 手动触发 auto-log
/synapse-code log [project_path]
```

### 状态检查命令

```bash
# 检查项目状态
/synapse-code status [project_path]
```

### 记忆查询命令

```bash
# 查询特定 task_type 的历史记录
/synapse-code query [project_path] --task-type debug --limit 5

# 按关键词搜索记录
/synapse-code query [project_path] --contains "登录 bug"
```

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/init_project.py` | 初始化项目环境（含合约验证） |
| `scripts/run_pipeline.py` | 运行 Pipeline 并自动触发 auto-log |
| `scripts/auto_log_trigger.py` | 消费 pipeline_summary.json 写入 memory |
| `scripts/check_status.py` | 检查项目状态 |
| `scripts/infer_task_type.py` | 根据描述推断 task_type |
| `scripts/query_memory.py` | 查询记忆记录 |

## 使用场景

### 代码开发
- 🚀 新功能开发 — "实现用户登录功能"
- 🐛 Bug 修复 — "修复登录页面无法提交的问题"
- 🏗️ 系统设计 — "设计一个完整的电商系统"
- 📝 代码重构 — "优化数据库查询性能"

### 文案写作
- 📰 公众号文章 — "写一篇 AI 编程技巧入门"
- 📢 产品新闻稿 — "写产品发布新闻稿"
- 📧 商务邮件 — "写一封给投资人的邮件"
- 📖 技术文档 — "写 API 使用文档"

### 设计创作
- 🎨 Logo 设计 — "设计一个简约现代的 logo"
- 🖥️ UI 设计 — "设计一个 dashboard 界面"
- 📊 海报设计 — "做个产品发布海报"
- 📈 信息图表 — "展示销售数据的信息图"

### 数据分析
- 📉 销售分析 — "分析 Q3 销售数据"
- 👥 用户分析 — "做用户行为分析报告"
- 📊 竞品对比 — "对比我们和竞品的市场份额"
- 📈 数据可视化 — "做个销售数据 dashboard"

### 翻译本地化
- 📄 文档翻译 — "翻译技术文档到英文"
- 📚 论文翻译 — "翻译这篇论文到中文"
- 🌐 UI 本地化 — "本地化 App 的 UI 文案"

### 学习研究
- 🔍 技术调研 — "调研 RAG 技术的最新进展"
- 📊 竞品分析 — "分析 AI 编程助手市场格局"
- 📖 文献综述 — "整理 XX 领域的研究现状"
- 📝 研究报告 — "写一份行业分析报告"

### 知识管理
- 📝 知识沉淀 — 自动记录开发经验
- 🔍 影响分析 — 改动前查询影响范围
- 📊 状态检查 — 实时查看项目进度

## Brain 调度集成 (v2.0 新增)

Synapse Code v2.0 可作为 synapse-brain 的被调度 Hand Agent 运行：

```
用户 → synapse-brain（意图识别 + 路由）
         ↓ 路由到 code
       synapse-code（执行开发）
         ↓ 完成后
       synapse-brain（汇总 + 状态保存）
```

当 synapse-code 被 Brain 调度时：
1. 自动接收任务参数（mode, scenario, description）
2. 执行对应 Pipeline 阶段
3. 完成后返回结构化结果
4. 自动触发 synapse-wiki 知识沉淀

```bash
# 直接调用（v1.x 方式）
/synapse-code run my-project "实现登录功能"

# 通过 Brain 调度（v2.0 推荐）
/synapse-brain dispatch "实现登录功能" --skill synapse-code --mode lite
```

## 与 synapse-wiki 互操作

Pipeline 完成后，自动触发 wiki 知识沉淀：

```
synapse-code Pipeline 完成
         ↓
    检测 auto_log 配置
         ↓ (enabled)
    synapse-wiki ingest
         ↓
    知识写入 wiki/summaries/
         ↓
    更新 session state
```

配置 `config.json` 启用互操作：

```json
{
  "pipeline": { "workspace": "~/pipeline-workspace", "auto_log": true },
  "interop": {
    "wiki_enabled": true,
    "wiki_root": "~/my-project/wiki"
  }
}
```

## 安装

```bash
# 方式 1: 使用安装脚本（推荐）
cd ~/.claude/skills/synapse-code
./install.sh

# 方式 2: 手动复制
cp -r synapse-code ~/.claude/skills/

# 方式 3: OpenClaw (如有 .skill 文件)
claude skill install synapse-code.skill
```

安装后会自动创建 `config.json`，根据需要修改 Pipeline workspace 路径。

## 配置

编辑 `~/.claude/skills/synapse-code/config.json`:

```json
{
  "pipeline": {
    "workspace": "~/pipeline-workspace",
    "enabled": true,
    "auto_log": true
  },
  "paths": {
    "pipeline_script": "~/pipeline-workspace/pipeline.py",
    "pipeline_summary": "/tmp/pipeline_summary.json"
  }
}
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `pipeline.workspace` | Pipeline 工作目录 | `~/pipeline-workspace` |
| `pipeline.auto_log` | Pipeline 成功后自动记录知识 | `true` |
| `paths.pipeline_script` | pipeline.py 路径 | `~/pipeline-workspace/pipeline.py` |
| `paths.pipeline_summary` | Pipeline 输出摘要路径 | `/tmp/pipeline_summary.json` |

## 相关文件

- `~/pipeline-workspace/pipeline.py` — Pipeline 引擎
- `scripts/auto_log.py` — Auto-log 脚本（内置）
- `~/pipeline-workspace/SYNAPSE_INTEGRATION.md` — 整合文档
