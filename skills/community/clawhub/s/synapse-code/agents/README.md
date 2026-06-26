# Agents - Synapse Code 专业 Agent 角色模板

本目录包含 Synapse Code Pipeline 各阶段的专业 Agent 角色定义（SOUL.md 模板）。

## 目录结构

```
agents/
├── README.md                 # 本文件
├── orchestrator.md           # Pipeline 调度核心（主代理）
│
├── development/              # 代码开发场景
│   ├── req-analyst.md        # 需求分析师
│   ├── architect.md          # 架构师
│   ├── developer.md          # 开发工程师
│   ├── qa-engineer.md        # 测试工程师
│   └── devops-engineer.md    # 运维工程师
│
├── writing/                  # 文案写作场景
│   ├── topic-planner.md      # 选题策划师
│   ├── outline-planner.md    # 大纲策划师
│   ├── writer.md             # 文案写作者
│   └── editor.md             # 编辑
│
├── design/                   # 设计创作场景
│   ├── requirement-analyst.md # 需求分析师
│   ├── researcher.md         # 竞品分析师
│   ├── designer.md           # 设计师
│   └── reviewer.md           # 审核员
│
├── analytics/                # 数据分析场景
│   ├── data-engineer.md      # 数据工程师
│   ├── analyst.md            # 数据分析师
│   ├── visualization-expert.md # 可视化专家
│   └── report-writer.md      # 报告撰写师
│
├── translation/              # 翻译本地化场景
│   ├── terminology-expert.md # 术语专家
│   ├── translator.md         # 翻译员
│   ├── proofreader.md        # 校对员
│   └── localization-expert.md # 本地化专家
│
└── research/                 # 学习研究场景
    ├── researcher.md         # 文献研究员
    ├── analyst.md            # 阅读分析师
    ├── synthesizer.md        # 知识整理师
    └── report-writer.md      # 报告撰写师
```

## 使用方式

### 方式 1：OpenClaw agents add

```bash
# 创建各专业 Agent
openclaw agents add synapse-req
openclaw agents add synapse-arch
openclaw agents add synapse-dev
openclaw agents add synapse-qa
openclaw agents add synapse-deploy
openclaw agents add synapse-orchestrator

# 将对应的 SOUL.md 内容复制到每个 Agent 的工作区
cp agents/req-analyst.md ~/.openclaw/workspace-synapse-req/SOUL.md
cp agents/architect.md ~/.openclaw/workspace-synapse-arch/SOUL.md
cp agents/developer.md ~/.openclaw/workspace-synapse-dev/SOUL.md
cp agents/qa-engineer.md ~/.openclaw/workspace-synapse-qa/SOUL.md
cp agents/devops-engineer.md ~/.openclaw/workspace-synapse-deploy/SOUL.md
cp agents/orchestrator.md ~/.openclaw/workspace-synapse-orchestrator/SOUL.md
```

### 方式 2：作为 Skill 内置资源

Synapse Code Skill 会自动加载这些 Agent 模板，用户无需手动配置。

## Agent 角色说明

### 代码开发场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **Orchestrator** | Pipeline 调度核心 | 全程 | 执行报告 |
| **Req-Analyst** | 需求分析 | REQ | 需求文档 |
| **Architect** | 架构设计 | ARCH | 技术方案 |
| **Developer** | 代码开发 | DEV | 可运行代码 |
| **QA-Engineer** | 质量保障 | QA | 质量报告 |
| **DevOps-Engineer** | 部署运维 | DEPLOY | 部署清单 |

### 文案写作场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **主编 (Orchestrator)** | 统筹整体方向 | 全程 | 执行报告 |
| **Topic-Planner** | 选题策划 | 1 | 选题策划案 |
| **Outline-Planner** | 大纲策划 | 2 | 文章大纲 |
| **Writer** | 文案写作 | 3 | 文案初稿 |
| **Editor** | 编辑润色 | 4 | 润色终稿 |

### 设计创作场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **设计总监 (Orchestrator)** | 把握整体风格 | 全程 | 执行报告 |
| **Requirement-Analyst** | 需求分析 | 1 | 设计需求文档 |
| **Researcher** | 竞品调研 | 2 | 竞品分析报告 |
| **Designer** | 设计创作 | 3 | 设计方案 |
| **Reviewer** | 设计审核 | 4 | 审核报告 |

### 数据分析场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **分析总监 (Orchestrator)** | 确定分析框架 | 全程 | 执行报告 |
| **Data-Engineer** | 数据收集清洗 | 1 | 干净数据集 |
| **Analyst** | 统计分析 | 2 | 分析洞察 |
| **Visualization-Expert** | 可视化制作 | 3 | 图表/Dashboard |
| **Report-Writer** | 报告撰写 | 4 | 完整报告 |

### 翻译本地化场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **翻译总监 (Orchestrator)** | 把控整体质量 | 全程 | 执行报告 |
| **Terminology-Expert** | 术语整理 | 1 | 术语表 |
| **Translator** | 初稿翻译 | 2 | 翻译初稿 |
| **Proofreader** | 校对润色 | 3 | 校对报告 |
| **Localization-Expert** | 本地化适配 | 4 | 本地化终稿 |

### 学习研究场景
| Agent | 职责 | 阶段 | 输出 |
|-------|------|------|------|
| **研究主管 (Orchestrator)** | 确定研究框架 | 全程 | 执行报告 |
| **Researcher** | 文献搜集 | 1 | 文献综述 |
| **Analyst** | 阅读分析 | 2 | 分析报告 |
| **Synthesizer** | 知识整理 | 3 | 知识结构 |
| **Report-Writer** | 报告撰写 | 4 | 研究报告 |

## 模式配置

### 独立模式 (Standalone)
使用 Agent: Orchestrator（独立完成）

### 轻量模式 (Lite)
使用 Agent: Orchestrator + 3-4 个子 Agent（场景特定）

### 完整模式 (Full)
使用 Agent: 全部子 Agent + Orchestrator

### 并行模式 (Parallel)
使用 Agent: Orchestrator + N 个子代理（最多 8 个）

## 场景配置

### config.json 场景配置
```json
{
  "synapse": {
    "pipeline": {
      "default_scenario": "auto",
      "scenarios": {
        "development": {
          "name": "代码开发",
          "agents": ["req-analyst", "architect", "developer", "qa-engineer"],
          "default_mode": "lite"
        },
        "writing": {
          "name": "文案写作",
          "agents": ["topic-planner", "outline-planner", "writer", "editor"],
          "default_mode": "lite"
        },
        "design": {
          "name": "设计创作",
          "agents": ["requirement-analyst", "researcher", "designer", "reviewer"],
          "default_mode": "lite"
        },
        "analytics": {
          "name": "数据分析",
          "agents": ["data-engineer", "analyst", "visualization-expert", "report-writer"],
          "default_mode": "lite"
        },
        "translation": {
          "name": "翻译本地化",
          "agents": ["terminology-expert", "translator", "proofreader", "localization-expert"],
          "default_mode": "lite"
        },
        "research": {
          "name": "学习研究",
          "agents": ["researcher", "analyst", "synthesizer", "report-writer"],
          "default_mode": "lite"
        }
      }
    }
  }
}
```

### 场景自动识别

系统会根据用户输入自动识别场景：

| 场景类型 | 典型关键词 |
|---------|-----------|
| **代码开发** | 代码、开发、实现、功能、bug、接口、API、编程 |
| **文案写作** | 文章、文案、写、公众号、邮件、稿、翻译 |
| **设计创作** | 设计、logo、UI、图、视觉、排版、海报 |
| **数据分析** | 数据、分析、报表、图表、可视化、销售 |
| **翻译本地化** | 翻译、译成、本地化、英文版、中文版 |
| **学习研究** | 调研、研究、学习、了解、进展、文献 |

### 手动指定场景

```bash
/synapse-code run my-project "写一篇公众号文章" --scenario writing
/synapse-code run my-project "分析 Q3 销售数据" --scenario analytics
/synapse-code run my-project "设计一个 logo" --scenario design
```

## 最佳实践

1. **首次使用** — 从独立模式开始，感受 Pipeline 流程
2. **日常开发** — 使用轻量模式，平衡效率和质量
3. **大型项目** — 使用完整模式，确保每个环节专业把关
4. **批量任务** — 使用并行模式，最大化效率

## 相关文档

- [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) — Pipeline 架构设计
- [SKILL.md](../SKILL.md) — Synapse Code Skill 完整文档
- [OpenClaw 多 Agent 教程](https://github.com/datawhalechina/openclaw-tutorial/blob/main/docs/day9-multi-agent.md)
