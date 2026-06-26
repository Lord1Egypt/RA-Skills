---
name: readme-craft
description: |
  README 写作与优化。从零创建、审计已有、或重写 README。
  蒸馏自 OMC/ECC 实战 README + awesome-readme/Standard README/Art of README 社区标准 + ClawHub 10+ README skills。
  当需要为项目写 README、审计 README 质量、或重写现有 README 时使用。
  不适用于：API 文档生成（用 doc-gen）、CHANGELOG 生成（用 git log）、CLAUDE.md 编写（那是机器配置，不是人类文档）。
license: MIT
version: "1.0.0"
metadata:
  author: sly
  tags: [readme, documentation, writing, open-source, developer-experience]
triggers:
  - readme
  - write readme
  - 写 readme
  - create readme
  - improve readme
  - readme 优化
  - audit readme
  - readme review
  - project documentation
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - WebFetch
  - Agent
---

# README Craft

写出让人在 30 秒内决定用不用你项目的 README。

不是模板填空。是认知漏斗设计——每一层让读者决定：继续深入，还是转身离开。

## 模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `create` | 从零创建 README | 新项目、无 README 的项目 |
| `audit` | 评分 + 诊断，不改动文件 | 想知道 README 好不好 |
| `rewrite` | 基于现有 README 重写 | README 过时、质量差、AI味重 |

```
/readme-craft                          # 自动检测模式（有 README → audit，无 → create）
/readme-craft --mode create            # 强制创建
/readme-craft --mode audit             # 只评分不改
/readme-craft --mode rewrite           # 重写现有
/readme-craft --mode audit --score-only # 仅输出分数
```

## When to Use

- 项目需要一个新 README
- 现有 README 读起来像 AI 生成的模板
- README 超过 6 个月没更新，和代码脱节
- 开源项目想提升 star/contributor 转化率
- 内部项目文档让新人看不懂

## When NOT to Use

- API 参考文档 → 用 doc-gen 或自动生成工具
- CLAUDE.md / AGENTS.md → 那是机器配置，结构完全不同
- CHANGELOG → 从 git log 生成
- 纯营销落地页 → README 不是广告，是技术文档

<example>
场景: Node.js CLI 工具项目没有 README
输入: /readme-craft
reasoning: 检测到无 README.md → create 模式。读取 package.json 发现 "bin" 字段 → CLI 项目类型。
输出:
```markdown
# logparse

Fast structured log parser for JSON and NDJSON streams.

[![CI](https://img.shields.io/github/actions/workflow/status/user/logparse/ci.yml)](...)
[![npm](https://img.shields.io/npm/v/logparse)](...)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Quick Start

\```bash
npm install -g logparse
echo '{"ts":"2026-01-01","msg":"hello"}' | logparse --format table
\```

## Install
...
```
</example>

<example>
场景: README 有 800 行，One-liner 是 "A utility for various things"
输入: /readme-craft --mode audit
输出:
```
## README Audit Report
**Score: 52/100 (D)**
| Category | Score | Max | Issues |
|----------|-------|-----|--------|
| Hook | 8 | 25 | 一行描述模糊（反模式 #7），无 Hero Visual |
| Onboarding | 12 | 25 | Quick Start 有 8 步，应精简到 3 步 |
...
### Anti-patterns: #7 模糊描述, #3 垃圾场, #14 README当API文档
```
</example>

<example>
场景: Python 库的 README 缺少代码示例
输入: /readme-craft --mode rewrite
reasoning: audit 得 61 分(C)。主要扣分：O3 Usage 无代码块(-5)、H3 无 Hero Visual(-7)、C1 Features 用散文(-5)。保留好的部分（安装说明完整、License 正确），补充代码示例和功能表格。
输出: 重写后的 README.md（新分 82 分 A 级），展示 diff 供确认。
</example>

<anti-example>
错误: 用 readme-craft 写 API 文档
原因: README 是项目入口，不是完整文档。API 文档应该在 docs/ 或用 doc-gen 工具。readme-craft 只在 README 中放 API 概览和链接。
</anti-example>

<anti-example>
错误: README 里列出全部 47 个函数的签名和参数
修正: README 只放 Top 3-5 核心 API 的概览表，底部加 `[Full API Reference](docs/api.md)` 链接。
</anti-example>

---

## 核心原则

### 1. 认知漏斗（Cognitive Funnel）

README 的每一层都是一个过滤器。读者在任何一层都可以决定离开或深入。

```
┌─────────────────────────────────┐
│ 项目名 → 这东西和我有关吗？      │  0.5 秒
├─────────────────────────────────┤
│ 一行描述 → 它解决什么问题？       │  2 秒
├─────────────────────────────────┤
│ Demo/截图 → 长什么样？           │  5 秒
├─────────────────────────────────┤
│ Quick Start → 用起来难不难？      │  30 秒
├─────────────────────────────────┤
│ 功能详情 → 能满足我的需求吗？     │  2 分钟
├─────────────────────────────────┤
│ API / 配置 → 具体怎么用？        │  5 分钟
├─────────────────────────────────┤
│ 贡献指南 → 我能参与吗？          │  按需
└─────────────────────────────────┘
```

**规则：不要在漏斗上层放下层的信息。** Quick Start 里不放 API 细节。一行描述里不解释架构。

### 2. Show, Don't Tell

一个语法高亮的代码块 > 三段文字描述。一个 GIF demo > 一页功能列表。

### 3. 「无源码测试」

如果有人不看源码就能用你的项目，README 就够了。（Ken Williams 原则）

### 4. 不卖广告

README 的职责是让人快速评估——合适就用，不合适就走。不是让人留下。

### 5. 保持同步

过时的 README 比没有 README 更有害——它会误导人。

---

## Golden Structure

根据项目类型，使用适当的结构。所有类型共享前 3 节和最后 1 节。

### 通用结构（12 节）

| # | Section | 必需 | 说明 |
|---|---------|------|------|
| 1 | **Title + Badges** | 必需 | 项目名 + 状态徽章（CI/version/license） |
| 2 | **One-liner** | 必需 | < 120 字符，和 package manager 描述一致 |
| 3 | **Hero Visual** | 推荐 | GIF demo / 截图 / 架构图（按项目类型选） |
| 4 | **Quick Start** | 必需 | 3 步以内从零到跑通 |
| 5 | **Features** | 推荐 | 要点列表或表格，不要写散文 |
| 6 | **Installation** | 必需 | 所有平台/包管理器的安装方式 |
| 7 | **Usage** | 必需 | 带语法高亮的代码示例 |
| 8 | **Configuration** | 按需 | 环境变量 / 配置文件 / CLI flags |
| 9 | **API** | 按需 | 核心 API 概览（详细文档链到外部） |
| 10 | **Contributing** | 推荐 | 简短说明或链到 CONTRIBUTING.md |
| 11 | **Credits** | 按需 | 致谢、灵感来源 |
| 12 | **License** | 必需 | SPDX 标识符 + 链接到 LICENSE 文件，放在最后 |

### 项目类型适配

| 类型 | Hero Visual | Quick Start 重点 | 特殊节 |
|------|------------|------------------|--------|
| **CLI 工具** | 终端 GIF (vhs/asciinema) | `npm i -g && cmd --help` | Magic Keywords / Commands 表格 |
| **库/SDK** | 代码截图 | `npm i && import` + 3行用法 | API 概览 + 完整文档链接 |
| **Web 应用** | 浏览器截图/GIF | `git clone && npm start` | 技术栈表格、环境变量 |
| **框架** | 架构图 (Mermaid) | `npx create-xxx` | 概念解释、对比表格 |
| **插件/扩展** | 安装截图 | 一键安装命令 | 兼容性表格、依赖关系 |
| **Monorepo** | 目录树 | 顶层入口 + 子包导航 | 包关系图 |

---

## 徽章规范

必需：CI/Build Status + License。推荐：Version + Coverage。总数 ≤ 8 个，否则信噪比下降。

详细徽章格式和选择指南见 `references/badge-and-visuals.md`。

---

## 审计评分体系（22 项，100 分）

6 类别加权评分。详细 22 项检查清单见 `references/quality-checklist.md`。

| 类别 | 权重 | 核心判定 |
|------|------|----------|
| **Hook** | 25% | 项目名清晰？一行描述 < 120 字符？有 Hero Visual？ |
| **Onboarding** | 25% | Quick Start ≤ 3 步？安装命令可复制？Usage 有代码块？ |
| **Content** | 20% | Features 用列表不用散文？配置有文档？信息不过时？ |
| **Trust** | 15% | License 在最后？Contributing 存在？CI badge 绿色？ |
| **Structure** | 10% | 认知漏斗顺序？超 100 行有 TOC？无信息重复？ |
| **Polish** | 5% | 无死链？Markdown 格式正确？移动端可读？ |

等级：**S**(90-100) **A**(80-89) **B**(70-79) **C**(60-69) **D**(<60)

---

## 反模式速查

最常见 5 个（完整 15 个见 `references/anti-patterns.md`）：

| # | 反模式 | 修复 |
|---|--------|------|
| 7 | **模糊描述**「A utility for things」 | 说清楚解决什么问题、给谁用 |
| 8 | **省略安装** | 写完整命令，包括前置依赖 |
| 9 | **只说不做**（无代码示例） | 每个功能至少一个代码块 |
| 3 | **垃圾场**（全塞一个文件） | 拆分到 docs/、CONTRIBUTING.md |
| 10 | **时光胶囊**（README 过时） | 改代码时同步改 README |

---

## 执行流程

### Create 模式

```
1. 扫描项目 → package.json / Cargo.toml / pyproject.toml / go.mod / Makefile
2. 检测项目类型 → CLI / 库 / Web 应用 / 框架 / 插件 / Monorepo
3. 提取信息 → 名称、描述、依赖、入口点、脚本/命令
4. 扫描源码 → 核心导出、公共 API、主要功能
5. 选择模板 → 按项目类型选 Golden Structure 变体
6. 生成 README → 填充内容，生成代码示例
7. 自审 → 跑 22 项检查，确保 ≥ 80 分
8. 写入文件 → README.md（如有需要同时生成 README_CN.md）
```

### Audit 模式

```
1. 读取 README.md
2. 逐项检查 22 个评分点
3. 计算总分 + 等级
4. 输出诊断报告：
   - 总分和等级
   - 每个类别的得分
   - Top 3 改进建议（按影响力排序）
   - 反模式检测结果
```

### Rewrite 模式

```
1. 读取现有 README.md
2. Audit（内部）→ 获取当前分数和问题列表
3. 扫描项目获取最新信息
4. 重写 → 保留好的部分，修复问题，补充缺失
5. 自审 → 确保新版 ≥ 旧版分数 + 10 分（或 ≥ 80）
6. 展示 diff → 让用户确认再写入
```

---

## 视觉资产

按项目类型自动选择：CLI → 终端 GIF (vhs/asciinema)，库 → 代码截图，框架 → Mermaid 架构图，Web 应用 → 浏览器截图。

具体格式模板见 `references/badge-and-visuals.md`。

---

## 输出格式

### Create / Rewrite 输出

直接写入 `README.md`。如果要求双语，同时生成 `README_CN.md`（或 `README_EN.md`）。

### Audit 输出

```markdown
## README Audit Report

**Score: 73/100 (B)**

| Category | Score | Max | Issues |
|----------|-------|-----|--------|
| Hook | 18 | 25 | 缺少 Hero Visual |
| Onboarding | 20 | 25 | Quick Start 超过 5 步 |
| Content | 15 | 20 | 配置项未文档化 |
| Trust | 12 | 15 | 无 Contributing 指南 |
| Structure | 5 | 10 | 缺少 TOC |
| Polish | 3 | 5 | 2 个死链 |

### Top 3 Improvements
1. 添加 GIF demo（+7 分）
2. 简化 Quick Start 到 3 步（+5 分）
3. 添加 CONTRIBUTING.md 链接（+3 分）

### Anti-patterns Detected
- #8 省略安装：缺少前置依赖说明
- #9 只说不做：Features 节没有代码示例
```

---

## 输出制品

| 请求类型 | 主产物 | 辅助产物 |
|----------|--------|----------|
| create | `README.md` | `README_CN.md`（如需双语） |
| audit | 审计报告（stdout） | 无文件变更 |
| rewrite | `README.md`（更新） | diff 预览 |

## Related Skills

| Skill | 关系 |
|-------|------|
| deslop | README 写完后可用 deslop 去 AI 味 |
| doc-gen | 生成 API 文档、架构文档（README 之外的文档） |
| slopbuster | 更强的去 AI 味工具，适合对外发布的 README |
| improvement-learner | 评估此 skill 本身的质量 |

## References

详细参考资料见 `references/` 目录：
- `references/quality-checklist.md` — 完整 22 项检查清单与评分细则
- `references/anti-patterns.md` — 15 个反模式完整版 + 检测方法
- `references/badge-and-visuals.md` — 徽章格式模板、视觉资产生成指南
- `references/community-standards.md` — 社区标准汇总（awesome-readme, Standard README, Art of README）
- `references/real-world-patterns.md` — 从 OMC/ECC 等项目提取的实战模式
