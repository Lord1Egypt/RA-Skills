# Synapse Wiki

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/ankechenlab-node/synapse-wiki/releases)

> 智能知识库管理系统 — 让知识随时间复利增长，越用越聪明。

**Synapse Wiki** 是基于 Karpathy LLM Wiki 模式的智能知识库系统。它自动将原始资料编译为结构化的知识网络，支持智能查询和健康检查。

## 核心特性

| 特性 | 说明 |
|------|------|
| **三层架构** | raw/ (原始资料) → wiki/ (知识页面) → outputs/ (产出) |
| **自动摄取** | 将原始资料编译为结构化 Wiki 页面 |
| **智能查询** | 基于知识网络综合答案 |
| **健康检查** | 自动检测死链接、孤立页面、矛盾 |
| **增量积累** | 知识随时间复利增长，越用越聪明 |

## 快速开始

### 安装

```bash
# 方式 1：使用安装脚本（推荐）
git clone https://github.com/ankechenlab/synapse-wiki.git
cd synapse-wiki
./install.sh

# 方式 2：手动复制到 Claude skills
cp -r synapse-wiki ~/.claude/skills/
```

### 使用

```bash
# 1. 初始化新知识库
/synapse-wiki init ~/my-wiki "AI 学习知识库"

# 2. 摄取资料
/synapse-wiki ingest ~/my-wiki raw/articles/article.md

# 3. 查询知识
/synapse-wiki query ~/my-wiki "LLM Wiki 的核心思想"

# 4. 健康检查
/synapse-wiki lint ~/my-wiki
```

## 三层架构

```
<wiki-root>/
├── CLAUDE.md              ← Schema 定义
├── log.md                 ← 时间线日志
├── raw/                   ← 原始资料层（LLM 只读）
│   ├── articles/          ← 网页文章
│   ├── papers/            ← 学术论文
│   └── notes/             ← 个人笔记
└── wiki/                  ← Wiki 知识层（LLM 编写）
    ├── index.md           ← 主目录
    ├── concepts/          ← 概念页面
    ├── entities/          ← 实体页面
    └── summaries/         ← 摘要页面
```

## 依赖要求

- Python 3.8+
- Claude Code (OpenClaw 平台)

## 测试

```bash
cd synapse-wiki
python3 tests/baseline_test.py
```

**测试结果**: 4/4 通过 (init, ingest, lint, query)

## 项目结构

```
synapse-wiki/
├── SKILL.md                 # OpenClaw Skill 主文件
├── README.md                # 本文件
├── RELEASE.md               # 发布说明
├── CHANGELOG.md             # 变更日志
├── install.sh               # 安装脚本
├── .gitignore              # Git 忽略文件
├── LICENSE                 # MIT 许可证
├── scripts/
│   ├── scaffold.py         # Wiki 初始化
│   ├── ingest.py           # 资料摄取
│   ├── query.py            # 知识查询
│   └── lint_wiki.py        # 健康检查
├── commands/
│   ├── init.sh
│   ├── ingest.sh
│   ├── query.sh
│   └── lint.sh
└── tests/
    └── baseline_test.py    # 基线测试
```

## 相关项目

- **synapse-code** — 智能代码开发工作流引擎 ([GitHub](https://github.com/ankechenlab/synapse-code))

## 贡献者

- **Initial work**: Anke
- **Based on**: Karpathy [llm-wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件

## 链接

- [GitHub Repository](https://github.com/ankechenlab/synapse-wiki)
- [Issue Tracker](https://github.com/ankechenlab/synapse-wiki/issues)
- [OpenClaw Documentation](https://github.com/openclaw)
