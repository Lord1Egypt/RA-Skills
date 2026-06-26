# WorkBuddy Skill: Psych Literature Search

自动搜索并整理心理学（及跨学科）学术文献的 WorkBuddy Skill。

支持从 **Web of Science**、**Springer Nature**、**Semantic Scholar** 三大来源检索文献，并自动提取研究变量、操作性定义等深度信息，输出结构化 Markdown 报告。

---

## ✨ 功能特色

- **多库搜索** — 同时检索 Web of Science、Springer Nature，无 API Key 时自动切换 Semantic Scholar 免费通道
- **深度信息提取** — 自动提取：文献标题、关键词（双语）、DOI 链接、摘要（原文 + 中文翻译）、研究变量、概念定义、操作性定义（测量工具 / 量表）
- **期刊质量指标** — 自动标注期刊 JCR 分区（Q1–Q4）、影响因子、SSCI 收录状态
- **四表结构输出** — 文献概览表、关键词与摘要表、研究变量与操作性定义表、综合分析表
- **APA 7 参考文献** — 自动生成标准 APA 第 7 版参考文献列表

---

## 🔑 触发词

### 中文

| 触发词 | 说明 |
|---|---|
| `帮我搜索 / 查找 / 找 XX 主题的文献` | 核心触发 |
| `做文献综述 / 文献检索` | 系统综述场景 |
| `整理 XX 相关的研究论文` | 按主题整理 |
| `搜索 Web of Science / Springer 文献` | 指定数据库 |
| `XX 的研究变量是什么 / 操作性定义是什么` | 变量定义提取 |
| `文献表格 / 文献整理` | 输出结构化表格 |

### English

| Trigger Phrase | Description |
|---|---|
| `search literature on [topic]` | Core trigger |
| `find papers / articles about [topic]` | General search |
| `literature review on [topic]` | Systematic review |
| `search Web of Science / Springer for [topic]` | Specify database |
| `what are the research variables / operational definitions in studies on [topic]` | Variable extraction |
| `organize papers into a table` | Structured output |

---

## 📦 安装方式

### 方式一：导入 ZIP 包（推荐）

1. 在 [Releases](../../releases) 页面下载最新 `psych-literature-search.zip`
2. 在 WorkBuddy 中进入 **技能管理** → **导入技能**
3. 选择下载的 ZIP 文件，完成导入

### 方式二：克隆仓库到本地

```bash
# 克隆到 WorkBuddy 技能目录
git clone https://github.com/你的用户名/workbuddy-skill-psych-literature-search.git \
  ~/.workbuddy/skills/psych-literature-search/
```

---

## 🔧 配置 API Key（可选，推荐）

配置 API Key 后可获取更丰富的元数据（期刊分区、被引次数等）。无 Key 时自动使用 Semantic Scholar 免费通道，功能不受影响。

### Web of Science API Key

1. 访问 [Clarivate Developer Portal](https://developer.clarivate.com)
2. 注册账号并申请 **Web of Science Core Collection API** Key（免费）
3. 在 WorkBuddy 对话中告知 Key，或直接修改 `SKILL.md` 中的配置

### Springer Nature API Key

1. 访问 [Springer Nature API](https://dev.springernature.com)
2. 注册后即时生成免费 API Key
3. 同上方式配置

> ⚠️ **注意**：API Key 为个人资产，请勿提交到公开仓库。本仓库的 `scripts/` 目录不含任何 Key。

---

## 📊 输出格式示例

执行搜索后，Skill 会生成包含以下四表的完整报告：

### 表一：文献概览

| # | 标题（链接） | 第一作者 | 年份 | 期刊 | 分区 | 被引 |
|---|---|---|---|---|---|---|
| 1 | [Empathy and moral judgment...](https://doi.org/...) | Zhang | 2025 | Cogn Affect Behav Neurosci | Q2 | 12 |

### 表二：关键词与摘要

| # | 标题 | 关键词（中文） | 关键词（英文） | 摘要（中文概述） |
|---|---|---|---|---|

### 表三：研究变量与操作性定义

| # | 标题 | 研究变量 | 概念定义 | 操作性定义（测量工具） |
|---|---|---|---|---|
| 1 | ... | 认知共情、情感共情 | 认知共情 = 观点采择能力（Davis, 1983） | IRI 量表，28 题，7 点计分，α = .78 |

### 表四：综合分析与研究趋势

- 核心发现（3–5 条，注明文献编号）
- 研究方法趋势
- 研究空白与未来方向

### APA 7 参考文献列表

自动附于报告末尾，格式符合 APA 第 7 版规范。

---

## 📁 目录结构

```
psych-literature-search/
├── SKILL.md                  # Skill 定义文件（触发词、工作流）
├── README.md                 # 本文件
├── assets/                   # 资源文件（如有）
├── references/               # 参考文档
│   ├── api_reference.md      # API 申请地址、端点、字段映射
│   └── output_templates.md  # 输出格式模板与规则
└── scripts/                  # 搜索脚本
    ├── search_wos.py         # Web of Science 搜索脚本
    ├── search_springer.py    # Springer Nature 搜索脚本
    └── journal_level.py      # 期刊分区 / 影响因子查询脚本
```

---

## 🔬 技术说明

| 项目 | 说明 |
|---|---|
| 运行环境 | Python 3.13+（WorkBuddy 托管运行时） |
| 依赖库 | `requests`（API 调用） |
| 数据来源 | Web of Science API / Springer Nature API / Semantic Scholar API |
| 输出格式 | Markdown（表格），兼容 Word / Typora / Obsidian |
| 中文翻译 | 由 WorkBuddy 内置 AI 完成，非机器翻译 |

---

## 📝 更新日志

### v1.0.0（2026-05-30）

- ✅ 初始版本发布
- ✅ 支持 Web of Science / Springer / Semantic Scholar 三源搜索
- ✅ 完整四表结构输出
- ✅ 研究变量与操作性定义自动提取
- ✅ APA 7 参考文献自动生成

---

## 📄 许可证

MIT License — 自由使用、修改和分发。

---

## 💬 问题反馈

如有 Bug 报告或功能建议，欢迎在 [Issues](../../issues) 页面提交。

---

> 🤖 本 Skill 由 WorkBuddy AI 辅助创建并持续迭代。
> 欢迎 Star ⭐ 和 Fork 🍴 本仓库！
