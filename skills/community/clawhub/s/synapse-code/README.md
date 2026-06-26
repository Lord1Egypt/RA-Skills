# Synapse Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ankechenlab/synapse-code/releases)

> 智能代码开发工作流引擎 — 代码交付 + 知识沉淀 一体化

**Synapse Code** 是基于 OpenClaw 多 Agent 架构的智能代码开发系统。支持六大场景、三种模式，内建代码图谱引擎，越用越懂你的项目。

## 核心特性

| 特性 | 说明 |
|------|------|
| **六大场景** | 代码开发、文案写作、设计创作、数据分析、翻译本地化、学习研究 |
| **三种模式** | standalone (独立)、lite (轻量)、full (完整) |
| **OpenClaw 原生** | 基于子代理架构，最多支持 8 个并发 Agent |
| **自动场景识别** | 根据用户输入自动匹配场景 |
| **知识沉淀** | Auto-log 自动记录开发经验 |
| **影响分析** | 内建 GitNexus 代码图谱引擎 |

## 六大场景

| 场景 | 典型任务 | Agent 团队 |
|------|---------|-----------|
| **💻 代码开发** | 功能开发、Bug 修复、系统设计 | 需求分析师 + 架构师 + 开发工程师 + 测试工程师 + 运维工程师 |
| **📝 文案写作** | 公众号文章、产品新闻稿、技术文档 | 选题策划 + 大纲策划 + 写作者 + 编辑 |
| **🎨 设计创作** | Logo 设计、UI 界面、海报设计 | 需求分析 + 竞品调研 + 设计师 + 审核员 |
| **📊 数据分析** | 销售分析、用户分析、数据可视化 | 数据工程师 + 分析师 + 可视化专家 + 报告撰写 |
| **🌐 翻译本地化** | 文档翻译、论文翻译、UI 本地化 | 术语专家 + 翻译员 + 校对员 + 本地化专家 |
| **📚 学习研究** | 技术调研、竞品分析、文献综述 | 文献研究员 + 阅读分析师 + 知识整理师 + 报告撰写 |

## 快速开始

### 安装

```bash
# 方式 1：使用安装脚本（推荐）
git clone https://github.com/ankechenlab/synapse-code.git
cd synapse-code
./install.sh

# 方式 2：手动复制到 Claude skills
cp -r synapse-code ~/.claude/skills/
```

### 使用

```bash
# 代码开发（默认场景）
/synapse-code run my-project "实现登录功能"

# 文案写作
/synapse-code run my-project "写公众号文章" --scenario writing

# 数据分析
/synapse-code run my-project "分析销售数据" --scenario analytics

# 设计创作
/synapse-code run my-project "设计 logo" --scenario design

# 学习研究
/synapse-code run my-project "技术调研" --scenario research

# 翻译本地化
/synapse-code run my-project "翻译文档" --scenario translation
```

### 三种模式

| 模式 | 配置要求 | 流程 | 适合场景 |
|------|---------|------|---------|
| **standalone** | 无需配置 | 直接开发 | 新手、快速原型 |
| **lite** | 基础 Pipeline | 3 阶段 | 日常功能开发 |
| **full** | 完整 Pipeline | 6 阶段 | 企业级项目 |

## 配置

编辑 `~/.claude/skills/synapse-code/config.json`:

```json
{
  "pipeline": {
    "workspace": "~/pipeline-workspace",
    "mode": "auto",
    "auto_log": true
  },
  "gitnexus": {
    "enabled": true
  }
}
```

## 依赖要求

- Python 3.8+
- npm (用于安装 GitNexus)
- Claude Code (OpenClaw 平台)

## 测试

```bash
cd synapse-code
python3 tests/baseline_test.py
```

**测试结果**: 3/3 通过 (init_syntax, infer, status)

## 项目结构

```
synapse-code/
├── SKILL.md                 # OpenClaw Skill 主文件
├── README.md                # 本文件
├── RELEASE.md               # 发布说明
├── CHANGELOG.md             # 变更日志
├── config.template.json     # 配置模板
├── install.sh               # 安装脚本
├── .gitignore              # Git 忽略文件
├── LICENSE                 # MIT 许可证
├── package.json            # npm 依赖
├── scripts/
│   ├── infer_task_type.py  # Task Type 推断
│   ├── init_project.py     # 项目初始化
│   ├── run_pipeline.py     # Pipeline 运行
│   ├── auto_log.py         # Auto-log 核心
│   ├── check_status.py     # 状态检查
│   └── query_memory.py     # 记忆查询
├── commands/               # 命令脚本 (7 个)
├── agents/                 # Agent 模板 (27 个)
│   ├── orchestrator.md     # 调度核心
│   ├── development/        # 代码开发 (5 个)
│   ├── writing/            # 文案写作 (4 个)
│   ├── design/             # 设计创作 (4 个)
│   ├── analytics/          # 数据分析 (4 个)
│   ├── translation/        # 翻译本地化 (4 个)
│   └── research/           # 学习研究 (4 个)
└── tests/
    └── baseline_test.py    # 基线测试
```

## 相关项目

- **synapse-wiki** — 智能知识库管理系统 ([GitHub](https://github.com/ankechenlab/synapse-wiki))

## 贡献者

- **Initial work**: Anke

## 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件

## 链接

- [GitHub Repository](https://github.com/ankechenlab/synapse-code)
- [Issue Tracker](https://github.com/ankechenlab/synapse-code/issues)
- [OpenClaw Documentation](https://github.com/openclaw)
- [生产级场景能力矩阵](PRODUCTION_SCENARIOS.md)
