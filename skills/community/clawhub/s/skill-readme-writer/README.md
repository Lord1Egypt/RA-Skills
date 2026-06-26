# README-Writer

📝 为本地项目或 GitHub 项目生成专业的 README.md 文档。采用 11 步交互式工作流程，自动收集项目信息、智能生成 Badge、中英双语完整翻译。

<!-- Badge Row 1: Core Info -->
[![ClawHub](https://img.shields.io/badge/ClawHub-README--writer-E75C46?logo=clawhub)](https://clawhub.ai/JustZeroX/README-writer)
[![GitHub](https://img.shields.io/badge/GitHub-JustZeroX-181717?logo=github)](https://github.com/JustZeroX/skill-README-Writer)
[![Version](https://img.shields.io/badge/version-0.0.1-orange)](https://github.com/author/skill-README-writer)

<!-- Badge Row 2: Platforms -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)]() 
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)]() 
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)]()

<!-- Badge Row 3: License -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)


---

### 中文 | [English](#english-version)

---

## 目录

- [✨ 核心功能](#-核心功能)
- [🎯 触发场景](#-触发场景)
- [🔄 11 步交互式流程](#-11 步交互式流程)
- [📊 项目信息收集](#-项目信息收集)
- [🎨 Badge 生成系统](#-badge-生成系统)
- [✅ 质量检查](#-质量检查)
- [🚀 快速开始](#-快速开始)
- [📄 许可证](#-许可证)

---

## ✨ 核心功能

- **🤖 自动收集项目信息** - 读取 package.json/pyproject.toml/Cargo.toml 等配置文件
- **💬 11 步交互式流程** - 每步都让用户确认，避免理解偏差
- **🎯 README 目的询问** - 了解读者和用途，针对性生成
- **📑 智能目录生成** - 根据项目类型生成合适的目录结构
- **🌍 中英双语完整翻译** - 中文 + English version，**内容完整一致**
- **🏷️ 3 行 Badge 系统** - 动态生成丰富的 Badge（核心信息 + 平台 + 许可证）
- **🔄 迭代优化** - 支持多次修改，直到满意
- **💾 自动备份** - 生成前自动备份现有 README
- **✅ 20 项质量检查** - 生成后自动检查
- **💬 可选章节询问** - 致谢/贡献/更新日志必须先询问
- **📊 项目类型检测** - 支持 14 种项目类型（Python/前端/API/CLI/库/Skill 等）

---

## 🎯 触发场景

**✅ 使用此技能当用户说：**

| 场景 | 示例 |
|------|------|
| **本地项目** | "为这个项目写 README：~/.openclaw/skills/my-project" |
| **GitHub 项目** | "给 https://github.com/user/repo 写 README" |
| **Skill 项目** | "为 easy-image-generate 写 README" |
| **优化现有** | "优化这个项目的 README" |
| **指定风格** | "参考 skill-rembg 风格写 README" |

**❌ 不使用此技能：**

- 代码审查 → 用代码分析工具
- 项目部署 → 用部署/CI/CD 工具
- 问题排查 → 用调试工具

---

## 🔄 11 步交互式流程

### 完整工作流程

```
1. 用户输入（本地路径或 URL）
    ↓
2. 自动收集项目信息
    ↓
3. 展示信息，用户确认/修改
    ↓
4. 询问 README 目的和风格偏好
    ↓
5. 生成建议目录结构
    ↓
6. 用户确认/调整目录
    ↓
7. 💬 可选章节询问（致谢/贡献/更新日志）
    ↓
8. 生成 README 草稿
    ↓
9. 质量检查 + 用户反馈
    ↓
10. 迭代优化（可多次）
    ↓
11. 最终版本 + 备份
```

---

## 📊 项目信息收集

### 自动读取的配置文件

| 文件 | 提取信息 |
|------|---------|
| `package.json` | 项目名称、描述、版本、脚本、依赖 |
| `pyproject.toml` | Python 项目配置、版本、依赖 |
| `Cargo.toml` | Rust 项目配置、版本、edition |
| `pom.xml` | Maven 项目版本、依赖 |
| `composer.json` | PHP 项目版本、依赖 |
| `go.mod` | Go 模块版本、依赖 |
| `SKILL.md` | OpenClaw Skill 元数据 |
| `LICENSE*` | 许可证类型 |

### 展示给用户确认

```markdown
📊 检测到项目信息：

**基本信息：**
- 项目名称：README-writer
- 版本：0.0.1
- 描述：为本地项目或 GitHub 项目生成专业的 README.md 文档
- 主要语言：Node.js >= 18.0.0

**项目类型：** OpenClaw Skill

**核心功能：**
- ✅ 自动收集项目信息
- ✅ 交互式确认流程
- ✅ 中英双语支持
- ✅ Badge 自动生成

**以上信息是否正确？需要补充或修改吗？**
```

---

## 🎨 Badge 生成系统

### 3 行专业布局

```markdown
<!-- Row 1: Core Info -->
[![ClawHub](...)](...)
[![GitHub](...)](...)
[![Version](...)](...)

<!-- Row 2: Platforms -->
[![macOS](...)](...) [![Windows](...)](...) [![Linux](...)](...)

<!-- Row 3: License -->
[![License](...)](...)
```

### 动态生成规则

| Badge 类型 | 读取源 | 默认值 |
|-----------|--------|--------|
| **Version** | package.json → pyproject.toml → Cargo.toml | `0.0.1` |
| **平台** | 用户指定 > 自动检测 | `macOS + Windows + Linux` |
| **License** | package.json → LICENSE 文件 | `MIT` |

**💡 设计理念：** Badge 丰富完整，用户可手动精简

---

## ✅ 质量检查

### 20 项检查清单

生成 README 后自动检查：

#### 基础检查（8 项）
- [ ] 项目简介清晰（1-2 句话）
- [ ] 安装步骤完整且可执行
- [ ] 至少有 3 个使用示例
- [ ] 功能特点列出（3-5 个）
- [ ] 目录导航正确（如>100 行）
- [ ] 代码块指定语言
- [ ] 链接有效
- [ ] 许可证明确

#### 中英双语检查（7 项）
- [ ] 中文内容完整
- [ ] **English version 完整翻译所有章节**
- [ ] **英文目录链接正确（锚点用英文）**
- [ ] **英文代码示例注释已翻译**
- [ ] **英文内容长度与中文一致**
- [ ] **英文部分有独立的 Table of Contents**
- [ ] **英文 TOC 条目数量与中文目录一致**

#### 可选章节检查（3 项）
- [ ] **致谢部分已询问用户**（有/无）
- [ ] 贡献指南已询问（需要/不需要）
- [ ] 更新日志已询问（需要/不需要）

#### Badge 检查（9 项）
- [ ] **项目描述后有 Badge 区域**
- [ ] **使用 3 行布局**
- [ ] **使用 HTML 注释分行**
- [ ] **Version Badge 已生成**
- [ ] **平台 Badge 正确**
- [ ] **License Badge 正确**
- [ ] **每个 Badge 都有链接**
- [ ] **颜色符合标准**
- [ ] **Windows 使用 Base64 Logo**

---

## 🚀 快速开始

### 基础使用

**本地项目：**
```
为这个项目写 README：~/.openclaw/skills/my-project
```

**GitHub 项目：**
```
给 https://github.com/user/repo 写 README
```

**指定风格：**
```
为项目写 README，参考 skill-rembg 风格
```

### 项目类型支持

| 项目类型 | 示例 |
|---------|------|
| **Python** | "为 Python 项目写 README" |
| **前端** | "为 React 项目写 README" |
| **API 服务** | "为 API 写 README" |
| **CLI 工具** | "为 CLI 工具写 README" |
| **库/SDK** | "为库写 README" |
| **OpenClaw Skill** | "为 easy-image-generate 写 README" |
| **Android/iOS/Web** | "为移动应用写 README" |

---

## 📄 许可证

MIT License

---

[Top / 返回顶部](#readme-writer)

---

## English Version

### Table of Contents

- [✨ Core Features](#-core-features)
- [🎯 Trigger Scenarios](#-trigger-scenarios)
- [🔄 11-Step Interactive Flow](#-11-step-interactive-flow)
- [📊 Project Information Collection](#-project-information-collection)
- [🎨 Badge Generation System](#-badge-generation-system)
- [✅ Quality Check](#-quality-check)
- [🚀 Quick Start](#-quick-start)
- [📄 License](#-license)

---

### ✨ Core Features

- **🤖 Auto Project Info** - Read package.json/pyproject.toml/Cargo.toml
- **💬 11-Step Interactive** - Confirm at each step
- **🎯 Purpose Inquiry** - Ask about README audience and purpose
- **📑 Smart TOC** - Generate suitable structure by project type
- **🌍 Bilingual** - Chinese + English version, **complete and consistent**
- **🏷️ 3-Row Badge** - Dynamic badges (Core Info/Platforms/License)
- **🔄 Iterative** - Support multiple revisions
- **💾 Auto Backup** - Backup existing README before generation
- **✅ 20-Item Quality Check** - Auto check after generation
- **💬 Optional Sections** - Ask before adding Acknowledgements/Contributing/Changelog
- **📊 14 Project Types** - Python/Frontend/API/CLI/Library/Skill/etc.

---

### 🎯 Trigger Scenarios

**✅ Use This Skill When:**

| Scenario | Example |
|----------|---------|
| **Local Project** | "Write README for this project: ~/.openclaw/skills/my-project" |
| **GitHub Project** | "Write README for https://github.com/user/repo" |
| **Skill Project** | "Write README for easy-image-generate" |
| **Optimize Existing** | "Optimize this project's README" |
| **Specify Style** | "Write README in skill-rembg style" |

**❌ Don't Use This Skill:**

- Code review → Use code analysis tools
- Project deployment → Use deployment/CI/CD tools
- Debugging → Use debugging tools

---

### 🔄 11-Step Interactive Flow

#### Complete Workflow

```
1. User input (local path or URL)
    ↓
2. Auto collect project info
    ↓
3. Show info, user confirm/modify
    ↓
4. Ask README purpose and style
    ↓
5. Generate suggested TOC
    ↓
6. User confirm/adjust TOC
    ↓
7. 💬 Ask optional sections
    ↓
8. Generate README draft
    ↓
9. Quality check + user feedback
    ↓
10. Iterative optimization
    ↓
11. Final version + backup
```

---

### 📊 Project Information Collection

#### Auto-Read Config Files

| File | Extract Info |
|------|-------------|
| `package.json` | Name, description, version, scripts, deps |
| `pyproject.toml` | Python config, version, deps |
| `Cargo.toml` | Rust config, version, edition |
| `pom.xml` | Maven version, deps |
| `composer.json` | PHP version, deps |
| `go.mod` | Go module version, deps |
| `SKILL.md` | OpenClaw Skill metadata |
| `LICENSE*` | License type |

#### Display for User Confirmation

```markdown
📊 Detected project info:

**Basic Info:**
- Project name: README-writer
- Version: 0.0.1
- Description: Generate professional README.md for local or GitHub projects
- Main language: Node.js >= 18.0.0

**Project Type:** OpenClaw Skill

**Core Features:**
- ✅ Auto collect project info
- ✅ Interactive confirmation process
- ✅ Bilingual support
- ✅ Badge auto-generation

**Is the above info correct? Need to add or modify?**
```

---

### 🎨 Badge Generation System

#### 3-Row Professional Layout

```markdown
<!-- Row 1: Core Info -->
[![ClawHub](...)](...)
[![GitHub](...)](...)
[![Version](...)](...)

<!-- Row 2: Platforms -->
[![macOS](...)](...) [![Windows](...)](...) [![Linux](...)](...)

<!-- Row 3: License -->
[![License](...)](...)
```

#### Dynamic Generation Rules

| Badge Type | Read Source | Default |
|-----------|-------------|---------|
| **Version** | package.json → pyproject.toml → Cargo.toml | `0.0.1` |
| **Platforms** | User specified > Auto detect | `macOS + Windows + Linux` |
| **License** | package.json → LICENSE file | `MIT` |

**💡 Design Philosophy:** Rich and complete badges, users can manually trim

---

### ✅ Quality Check

#### 20-Item Checklist

Auto check after generating README:

##### Basic Check (8 items)
- [ ] Clear project description (1-2 sentences)
- [ ] Executable installation steps
- [ ] At least 3 usage examples
- [ ] Feature list (3-5 items)
- [ ] Valid TOC navigation (if >100 lines)
- [ ] Code blocks specify language
- [ ] Links are valid
- [ ] License specified

##### Bilingual Check (7 items)
- [ ] Chinese content complete
- [ ] **English version complete translation of all sections**
- [ ] **English TOC links correct (use English anchors)**
- [ ] **English code example comments translated**
- [ ] **English content length consistent with Chinese**
- [ ] **English part has independent Table of Contents**
- [ ] **English TOC entries match Chinese TOC count**

##### Optional Sections Check (3 items)
- [ ] **Acknowledgements asked** (yes/no)
- [ ] Contributing asked (need/not need)
- [ ] Changelog asked (need/not need)

##### Badge Check (9 items)
- [ ] **Badge section after project description**
- [ ] **Use 3 row layout**
- [ ] **Use HTML comment line breaks**
- [ ] **Version Badge generated**
- [ ] **Platform Badge correct**
- [ ] **License Badge correct**
- [ ] **Every Badge has link**
- [ ] **Colors follow standard**
- [ ] **Windows uses Base64 Logo**

---

### 🚀 Quick Start

#### Basic Usage

**Local Project:**
```
为这个项目写 README：~/.openclaw/skills/my-project
```

**GitHub Project:**
```
给 https://github.com/user/repo 写 README
```

**Specify Style:**
```
为项目写 README，参考 skill-rembg 风格
```

#### Project Type Support

| Project Type | Example |
|-------------|---------|
| **Python** | "Write README for Python project" |
| **Frontend** | "Write README for React project" |
| **API Service** | "Write README for API" |
| **CLI Tool** | "Write README for CLI tool" |
| **Library/SDK** | "Write README for library" |
| **OpenClaw Skill** | "Write README for easy-image-generate" |
| **Android/iOS/Web** | "Write README for mobile app" |

---

### 📄 License

MIT License

---

[Top](#readme-writer)
