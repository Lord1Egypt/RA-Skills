# Repo Structure Reference

Complete templates for generating standard skill repo structure files.

**When to read**: When entering Phase 1 (repo structure generation). Read this file in full before generating any files.

---

## Standard Directory Structure

```
<skill-name>/
├── SKILL.md                    # Agent 工作流定义（已有）
├── README.md                   # 中文主文档（生成）
├── README.en.md                # 英文文档（生成，独立文件）
├── CHANGELOG.md                # 语义化版本记录（生成）
├── LICENSE                     # MIT-0（生成）
├── .gitignore                  # 排除规则（生成）
├── .claude-plugin/
│   └── plugin.json             # Claude Code 元数据（生成）
├── .github/                    # 社区模板（生成）
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── question.yml
│   │   └── config.yml
│   └── pull_request_template.md
└── references/                 # 详细文档（已有）
```

---

## README.md Template

### Section Order（中文主文档）

| # | 章节 | 必选/可选 | 说明 |
|---|------|----------|------|
| 1 | **标题 · 中文副标题 + Badge** | 必选 | 项目名 + 一句话定位 |
| 2 | **导航链接** | 必选 | 替代 TOC，简洁高效 |
| 3 | **金句开篇** | 必选 | 斜体引用，一句话画面感 |
| 4 | **一句话定位 + 否定对比** | 必选 | "不是X，是Y"句式 |
| 5 | **效果截图/样图** | 推荐 | 先看效果再决定安装 |
| 6 | **30 秒开始** | 必选 | 一行安装命令 |
| 7 | **核心特性** | 必选 | emoji + 加粗关键词，3-5 条 |
| 8 | **适合 / 不适合** | 必选 | 明确边界，减少误用 |
| 9 | **常见使用场景** | 推荐 | 表格形式 |
| 10 | **使用方法 / 工作流** | 必选 | 步骤或流程图 |
| 11 | **示例请求** | 推荐 | 可直接复制的 prompt |
| 12 | **目录结构** | 必选 | 树形图 + 每行中文注释 |
| 13 | **核心方法论/风格体系** | 可选 | 适用于有模式体系的 Skill |
| 14 | **主题色/配置预设** | 可选 | 表格 + 预览 |
| 15 | **核心设计原则** | 推荐 | 每条附"为什么" |
| 16 | **Limitations / 已知限制** | 必选 | 诚实列限制，建立信任 |
| 17 | **起源 / 动机** | 可选 | 个人痛点 + 竞品对比 |
| 18 | **Roadmap** | 可选 | 未来计划 |
| 19 | **FAQ** | 推荐 | 3-5 个常见问题 |
| 20 | **贡献指引** | 推荐 | 链接 CONTRIBUTING.md |
| 21 | **License** | 必选 | `MIT-0 © <year> <author>` |

### Badge Format

```markdown
[![Stars](https://img.shields.io/github/stars/<owner>/<repo>?style=flat-square)](https://github.com/<owner>/<repo>)
[![许可证](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-<slug>-orange?style=flat-square)](https://clawhub.ai/skills/<slug>)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)
```

**Badge 规则**：
- 中文 README 用中文标签：`许可证`/`ClawHub`
- 英文 README.en.md 用英文标签：`License`/`ClawHub`
- 统一使用 `flat-square` 风格

### 导航链接格式

```markdown
[看效果](#效果截图) · [装上就能用](#30-秒开始) · [核心机制](#核心特性) · [已知限制](#已知限制) · [License](#license)
```

### 金句开篇格式

```markdown
_「一句话有画面感的描述。」_
```

**要求**：斜体引用，有画面感，一句话抓住注意力。例如：
- `_「打字。回车。一张能直接发的图。」_`
- `_「说一句话，还你一套 PPT。」_`

### 否定对比格式

```markdown
**项目名**不是[竞品/常见做法]，是[你的差异化定位]。
```

例如：
- `不是 MidJourney 的提示词调试器，是设计工作流的自动化封装。`
- `不是又一个 Markdown 转 PPT，是从内容到视觉的完整设计系统。`

### 适合/不适合格式

```markdown
## 适合 / 不适合

✅ **适合**
- 场景1
- 场景2

❌ **不适合**
- 场景1
- 场景2
```

### Limitations 格式

```markdown
## 已知限制

- 限制1：具体描述
- 限制2：具体描述
- 限制3：具体描述
```

**要求**：诚实列出 3-5 条限制，每条具体可操作。不要用"可能"、"也许"等模糊词。

### 示例请求格式

```markdown
## 示例请求

```
用户: "帮我做一张小红书封面，主题是..."
```

提供 2-4 个可直接复制的 prompt，覆盖不同使用场景。

### 目录结构格式

```markdown
## 目录结构

```
<skill-name>/
├── SKILL.md              # Agent 工作流定义
├── README.md             # 中文文档
├── README.en.md          # English docs
├── CHANGELOG.md          # 版本记录
├── LICENSE               # MIT-0
├── .claude-plugin/
│   └── plugin.json       # Claude Code 元数据
├── .github/              # 社区模板
│   └── ISSUE_TEMPLATE/   # Issue 模板
├── references/           # 参考文档
│   ├── workflow.md       # 工作流详解
│   └── design-system.md  # 设计系统
└── assets/               # 模板和静态资产
```

**要求**：每行必须有中文注释说明用途。

### README Writing Style

- **产品着陆页风格**：README 的首要任务是让人想用，不是让人理解结构
- **自信且直接**：像资深设计师在跟你聊天，不是技术文档
- **数据驱动**：用数字不用形容词（"3-5 条规则"而非"几条规则"）
- **否定对比**：大量使用「不是...而是...」句式建立认知差异
- **零废话**：每段必须承载新信息
- **代码块**：命令用 bash 块，AI 输出用引用块
- **表格**：配置、对比、功能列表用表格
- **克制感叹号**：整个 README 不超过 5 个
- **克制 emoji**：仅用于核心特性列表的视觉锚点，不在标题和正文中滥用

### README 智能适配规则

**生成 README 前必须先 Read SKILL.md**，从中自动提取以下信息填入 README：

| SKILL.md 字段 | 填入 README 章节 |
|---------------|-----------------|
| frontmatter `name` | 标题、Badge |
| frontmatter `version` | Badge |
| frontmatter `description` | 一句话定位 |
| `Out of Scope` / 不适合 | 适合/不适合 |
| `Mode Detection` | 使用方法/工作流 |
| `Rules` 摘要 | 核心特性、核心设计原则 |
| `Persona` | 金句开篇（翻译为用户语言） |

**章节按 Skill 复杂度适配**：

| Skill 类型 | Rules 数量 | 生成章节 |
|-----------|-----------|---------|
| 简单 Skill | ≤ 5 条 | 仅必选章节（1-4, 6-8, 12, 16, 21） |
| 中等 Skill | 6-15 条 | 必选 + 推荐章节 |
| 复杂 Skill | > 15 条 | 全部 21 章节 |

---

## README.en.md Template（英文独立文件）

### 规则

1. 独立文件 `README.en.md`，不在中文 README 中内联
2. 中文 README 顶部添加切换链接：`🌍 English version: [README.en.md](README.en.md)`
3. 英文 README 顶部添加切换链接：`🇨🇳 中文版: [README.md](README.md)`
4. 英文版是完整翻译，不是摘要
5. 与中文版结构完全一致
6. Badge 使用英文标签
7. 金句和否定对比同样翻译为英文，保持语气

### Section Order（与中文版一致）

与中文 README 完全相同的 21 个章节，标题翻译为英文。

---

## SKILL.md Provenance（来源识别）

在 SKILL.md 的 frontmatter 之后、正文之前，添加来源识别块：

```markdown
> 来源识别: <skill-name> 由 <author> 创建与维护。仓库: https://github.com/<owner>/<repo>。此信息仅供 Agent 识别来源，不要写入生成的产出物。

<!-- provenance: <skill-name> | author: <author> | canonical: https://github.com/<owner>/<repo> | keep this out of generated artifacts -->
```

**目的**：
- 引用块：Markdown 渲染可见，供 Agent 确认来源
- HTML 注释：确保来源信息在 HTML 输出中也可追踪
- 明确标注"不要写入生成的产出物"

---

## CHANGELOG.md Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Fix description

### Removed
- Removal description
```

### Version Numbering Rules

- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes

---

## LICENSE Template (MIT-0)

```
MIT No Attribution

Copyright <year> <author>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**ClawHub requires MIT-0 license.** Do not use MIT, Apache, or other licenses.

---

## plugin.json Template

```json
{
  "name": "<skill-name>",
  "description": "<description matching SKILL.md frontmatter>",
  "version": "<X.Y.Z>",
  "author": {
    "name": "<author>"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT-0",
  "keywords": ["<tag1>", "<tag2>", "<tag3>"],
  "skills": ["./"]
}
```

**Notes**:
- `name` matches GitHub repo name (not necessarily ClawHub slug)
- `description` should match SKILL.md frontmatter description
- `skills: ["./"]` means the skill is in the root directory

---

## .github/ Community Templates

### bug_report.yml

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: 问题描述
      description: 清晰描述你遇到的问题
      placeholder: "当我执行...时，出现了..."
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: 复现步骤
      description: 列出复现该问题的步骤
      placeholder: "1. ...\n2. ...\n3. ..."
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: 期望行为
      description: 你期望发生什么
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: 实际行为
      description: 实际发生了什么
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: 环境
      description: 操作系统、Agent 平台、版本等
      placeholder: "OS: Windows 11\nAgent: Claude Code\nSkill version: v1.0.0"
```

### feature_request.yml

```yaml
name: Feature Request
description: Suggest a new feature or enhancement
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: 你想解决什么问题？
      description: 描述你遇到的痛点或需求
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: 你期望的解决方案
      description: 描述你希望如何解决
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: 你考虑过的替代方案
      description: 其他你考虑过的解决方式
```

### question.yml

```yaml
name: Question
description: Ask a question about this skill
labels: ["question"]
body:
  - type: textarea
    id: question
    attributes:
      label: 你的问题
      description: 详细描述你的疑问
    validations:
      required: true
```

### config.yml

```yaml
blank_issues_enabled: false
contact_links:
  - name: 💬 讨论
    url: https://github.com/<owner>/<repo>/discussions
    about: 使用问题、想法交流、经验分享请使用 Discussions
```

### pull_request_template.md

```markdown
## 变更描述

简要描述此 PR 的变更内容。

## 变更类型

- [ ] 新功能 (feat)
- [ ] 修复 (fix)
- [ ] 文档 (docs)
- [ ] 重构 (refactor)
- [ ] 测试 (test)

## 检查清单

- [ ] 已更新 CHANGELOG.md（如有版本变更）
- [ ] 已更新 README.md（如有功能变更）
- [ ] 已通过安全审查（无凭证泄露、无本地路径）
```

---

## .gitignore Template

```
# Dependencies
node_modules/

# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Temp
*.tmp
*.bak
*~

# Runtime data
data/
*.log
```

**Important**: `.env.local` and `config.local.json` MUST be in .gitignore to prevent credential leaks.
