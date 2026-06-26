---
name: README-writer
description: 为本地项目或 GitHub 项目生成专业的 README.md 文档。**触发词："写 README"、"生成 README"、"README.md"、"项目文档"、"GitHub 文档"、"readme"、"项目介绍"、"文档生成"**。支持自动收集项目信息、交互式确认、中英双语。根据项目类型（Python/前端/Skill/CLI 等）生成对应的专业文档。
---

# README Writer - 项目文档生成器

📝 **为本地项目或 GitHub 项目生成专业的 README.md 文档**

采用交互式工作流程：自动收集信息 → 用户确认 → 生成目录 → 用户确认 → 生成 README → 迭代优化

---

## 🎯 何时使用（触发场景）

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

## 🔄 交互式工作流程

### 完整流程（11 步）

1. 用户输入（本地路径或 URL）
2. 自动收集项目信息
3. 展示信息，用户确认/修改
4. 询问 README 目的和风格偏好
5. 生成建议目录结构
6. 用户确认/调整目录
7. 💬 可选章节询问（致谢/贡献/更新日志）
8. 生成 README 草稿
9. 质量检查 + 用户反馈
10. 迭代优化（可多次）
11. 最终版本 + 备份

---

## 📊 第 1 步：项目信息收集

### 本地项目

**自动读取：**

- package.json → 项目名称、描述、版本、脚本
- requirements.txt → Python 依赖
- pyproject.toml → Python 项目配置
- Cargo.toml → Rust 项目
- 主语言文件（.py/.js/.ts/.rs 等）
- 目录结构（scripts/ docs/ tests/）
- 现有 README（如有）

**展示给用户确认：**

📊 检测到项目信息：

**基本信息：**
- 项目名称：[自动提取]
- 版本：[自动提取]
- 描述：[自动提取]
- 主要语言：[自动提取]

**项目类型：** [自动识别]

**核心功能：** [自动分析]

**以上信息是否正确？需要补充或修改吗？**

---

## 🎯 第 2 步：询问 README 目的

**询问模板：**

🎯 这个 README 的主要读者是谁？

**A. 潜在用户** - 快速了解项目用途
**B. 开发者** - 想要贡献代码
**C. 两者兼顾**（推荐）

📝 希望突出什么内容？

**A. 快速上手** - 安装 + 使用示例
**B. 功能特点** - 详细的功能列表
**C. API 文档** - 技术细节
**D. 项目背景** - 为什么创建这个项目

🎨 文档风格偏好？

**A. 简洁专业** - 像 requests 库
**B. 活泼友好** - 像 skill-rembg（emoji+ 双语）
**C. 详细完整** - 像大型框架

---

## 📑 第 3 步：生成目录结构

根据项目类型和偏好生成建议目录结构，用户确认后再继续。

---

## 💬 第 3.5 步：可选章节询问

**必须询问的章节：**

📝 需要添加以下章节吗？

### 1️⃣ 致谢部分（🙏 Acknowledgements）

感谢贡献者、使用的工具或平台

**请回复：**
- "有，致谢：OpenClaw、ClawHub"
- "没有，不需要"

### 2️⃣ 贡献指南（🤝 Contributing）

如何为项目贡献代码

**请回复：**
- "需要，是开源项目"
- "不需要，个人项目"

### 3️⃣ 更新日志（📝 Changelog）

项目版本历史

**请回复：**
- "需要，有多个版本"
- "不需要，初始版本"

**规则：**
- ✅ **必须先询问，再生成**
- ✅ **用户说"没有"就不生成该章节**
- ✅ **用户说"有"就列出具体内容**

---

## ✍️ 第 4 步：生成 README 草稿

### 生成规则

#### 0. Badge 区域（项目简介后）

**🎨 采用多行专业布局（丰富完整，用户可手动精简）：**

```markdown
<!-- Badge Row 1: Core Info - 项目身份 -->
[![ClawHub](https://img.shields.io/badge/ClawHub-skill--name-E75C46?logo=clawhub)](https://clawhub.ai/author/skill)
[![GitHub](https://img.shields.io/badge/GitHub-author-181717?logo=github)](https://github.com/author/repo)
[![Version](https://img.shields.io/badge/version-0.0.1-orange)](https://github.com/author/repo)

<!-- Badge Row 2: Package Registry - 包管理器（如已发布） -->
[![npm](https://img.shields.io/npm/v/package-name?color=CB3837&logo=npm)](https://npmjs.com/package/package-name)
[![PyPI](https://img.shields.io/pypi/v/package-name?color=3776AB&logo=pypi)](https://pypi.org/project/package-name)

<!-- Badge Row 3: Tech Stack - 技术栈/语言版本 -->
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-339D35?logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](https://python.org)
[![Rust](https://img.shields.io/badge/Rust-2021%20Edition-DEA584?logo=rust)](https://rust-lang.org)

<!-- Badge Row 4: Platforms - 平台支持 -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://openclaw.ai) 
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://openclaw.ai) 
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://openclaw.ai)
[![Android](https://img.shields.io/badge/Android-3DDC84?logo=android&logoColor=white)](https://openclaw.ai)
[![iOS](https://img.shields.io/badge/iOS-000000?logo=apple&logoColor=white)](https://openclaw.ai)
[![Web](https://img.shields.io/badge/Web-4285F4?logo=google-chrome&logoColor=white)](https://openclaw.ai)

<!-- Badge Row 5: License - 许可证 -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)
```

**💡 设计理念：**
- ✅ **Badge 丰富完整** - 生成所有可能的 Badge，用户可手动删除不需要的
- ✅ **URL 处理灵活** - 能确定的用实际链接，确定不了的用 Demo 占位符
- ✅ **无个人信息** - 所有 Demo 使用通用占位符（`author`、`repo`、`skill-name`）
- ✅ **Windows 用 Base64** - 避免图片链接失效问题

---

### 📋 Badge 动态生成规则

#### Row 1: 核心信息 Badge（项目身份）

**1. ClawHub Badge**
- **条件**：检测到是 OpenClaw Skill（有 `SKILL.md`）
- **格式**：`[![ClawHub](https://img.shields.io/badge/ClawHub-{skill-name}-E75C46?logo=clawhub)](https://clawhub.ai/author/skill)`
- **skill-name**：从 SKILL.md 的 `name` 字段读取，转换为 kebab-case
- **链接**：使用 Demo 占位符 `https://clawhub.ai/author/skill`

**2. GitHub Badge**
- **条件**：用户提供了 GitHub URL 或检测到 `.git` 目录
- **格式**：`[![GitHub](https://img.shields.io/badge/GitHub-{author}-181717?logo=github)](https://github.com/author/repo)`
- **author/repo**：从 Git 远程仓库或 package.json 提取
- **链接**：如无法提取，使用 Demo 占位符 `https://github.com/author/repo`

**3. Version Badge（必须生成）**
- **读取优先级**：
  1. `package.json` → `version`
  2. `pyproject.toml` → `version`
  3. `Cargo.toml` → `version`
  4. `pom.xml` → `version`
  5. `composer.json` → `version`
  6. **默认**：`0.0.1`
- **格式**：`[![Version](https://img.shields.io/badge/version-{version}-orange)](链接)`
- **链接**：使用项目主页或 Demo 占位符

---

#### Row 2: 包管理器 Badge（如已发布）

**根据项目类型生成对应的包管理器 Badge：**

| 项目类型 | Badge | 链接 |
|---------|-------|------|
| **npm 包** | `[![npm](https://img.shields.io/npm/v/package-name?color=CB3837&logo=npm)](https://npmjs.com/package/package-name)` | npmjs.com |
| **Python 包** | `[![PyPI](https://img.shields.io/pypi/v/package-name?color=3776AB&logo=pypi)](https://pypi.org/project/package-name)` | pypi.org |
| **Ruby Gem** | `[![Gem](https://img.shields.io/gem/v/gem-name?color=E9563D&logo=ruby)](https://rubygems.org/gems/gem-name)` | rubygems.org |
| **Go Module** | `[![Go](https://img.shields.io/badge/go.mod-v1.20-00ADD8?logo=go)](https://pkg.go.dev/module/path)` | pkg.go.dev |
| **Maven** | `[![Maven](https://img.shields.io/maven-central/v/group/artifact?color=E43C3C&logo=apache-maven)](https://search.maven.org)` | search.maven.org |

**链接处理**：如无法获取实际包名，使用 Demo 占位符

---

#### Row 3: 技术栈/语言版本 Badge

**自动读取项目配置生成：**

**Node.js 项目**（读取 `package.json` → `engines.node`）：
```markdown
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-339D35?logo=node.js)](https://nodejs.org)
```

**Python 项目**（读取 `pyproject.toml` 或 `setup.py` → `python_requires`）：
```markdown
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](https://python.org)
```

**Rust 项目**（读取 `Cargo.toml` → `edition`）：
```markdown
[![Rust](https://img.shields.io/badge/Rust-2021%20Edition-DEA584?logo=rust)](https://rust-lang.org)
```

**Go 项目**（读取 `go.mod` → `go` 版本）：
```markdown
[![Go](https://img.shields.io/badge/Go-1.20-00ADD8?logo=go)](https://go.dev)
```

**PHP 项目**（读取 `composer.json` → `require.php`）：
```markdown
[![PHP](https://img.shields.io/badge/PHP-%3E%3D8.0-777BB4?logo=php)](https://php.net)
```

**链接处理**：使用官方文档链接或 Demo 占位符

---

#### Row 4: 平台 Badge（全部生成，用户可精简）

**默认生成所有平台 Badge**，用户可根据实际情况手动删除：

```markdown
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://openclaw.ai) 
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://openclaw.ai) 
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://openclaw.ai)
[![Android](https://img.shields.io/badge/Android-3DDC84?logo=android&logoColor=white)](https://openclaw.ai)
[![iOS](https://img.shields.io/badge/iOS-000000?logo=apple&logoColor=white)](https://openclaw.ai)
[![Web](https://img.shields.io/badge/Web-4285F4?logo=google-chrome&logoColor=white)](https://openclaw.ai)
```

**颜色规范**：
- macOS: `#000000`（黑）
- Windows: `#0078D6`（蓝）+ **Base64 SVG Logo**
- Linux: `#FCC624`（黄）
- Android: `#3DDC84`（绿）
- iOS: `#000000`（黑）
- Web: `#4285F4`（蓝）

**链接处理**：使用 Demo 占位符 `https://openclaw.ai`

---

#### Row 5: License Badge

**读取优先级**：
1. `package.json` → `license`
2. `pyproject.toml` → `license`
3. `Cargo.toml` → `license`
4. `LICENSE` / `LICENSE.md` / `LICENSE.txt` 文件名
5. **默认**：`MIT`

**License 颜色映射**：
- MIT: `#BD2D2D`（红）
- Apache-2.0: `#D54D2D`（橙红）
- GPL-3.0: `#FF7A00`（橙）
- BSD-3-Clause: `#3B82F6`（蓝）
- ISC: `#10B981`（绿）
- Unlicense: `#6B7280`（灰）
- 其他：`#6B7280`（灰）

**格式**：`[![License](https://img.shields.io/badge/License-{LICENSE}-{COLOR})](LICENSE)`

**链接处理**：指向 `LICENSE` 文件（如不存在，用户可手动修改）

---

### ✅ Badge 生成示例（完整版）

#### 示例：Node.js 项目（完整 Badge 展示）

```markdown
<!-- Badge Row 1: Core Info -->
[![ClawHub](https://img.shields.io/badge/ClawHub-project--name-E75C46?logo=clawhub)](https://clawhub.ai/author/project)
[![GitHub](https://img.shields.io/badge/GitHub-author-181717?logo=github)](https://github.com/author/repo)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](https://github.com/author/repo)

<!-- Badge Row 2: Package Registry -->
[![npm](https://img.shields.io/npm/v/package-name?color=CB3837&logo=npm)](https://npmjs.com/package/package-name)

<!-- Badge Row 3: Tech Stack -->
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-339D35?logo=node.js)](https://nodejs.org)

<!-- Badge Row 4: Platforms -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://openclaw.ai) 
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://openclaw.ai) 
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://openclaw.ai)
[![Android](https://img.shields.io/badge/Android-3DDC84?logo=android&logoColor=white)](https://openclaw.ai)
[![iOS](https://img.shields.io/badge/iOS-000000?logo=apple&logoColor=white)](https://openclaw.ai)
[![Web](https://img.shields.io/badge/Web-4285F4?logo=google-chrome&logoColor=white)](https://openclaw.ai)

<!-- Badge Row 5: License -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)
```

**💡 提示用户**：在 README 末尾添加说明：
```markdown
> 💡 **Badge 说明**：以上 Badge 为自动生成，如与实际不符可手动删除或修改。
```

---

### ⚠️ Badge 生成规则总结

- ✅ **必须使用 HTML 注释分行**（`<!-- Badge Row X: ... -->`）
- ✅ **Badge 丰富完整** - 生成所有可能的 Badge，用户可手动精简
- ✅ **Version Badge 必须生成**（无版本号时用 0.0.1）
- ✅ **平台 Badge 全部生成**（macOS/Windows/Linux/Android/iOS/Web）
- ✅ **Windows 使用 Base64 SVG Logo**（避免图片链接失效）
- ✅ **License Badge 根据实际 License 生成**（无时默认 MIT）
- ✅ **URL 灵活处理** - 能确定用实际链接，确定不了用 Demo 占位符
- ✅ **无个人信息** - 所有 Demo 使用通用占位符（`author`、`repo`、`skill-name`）
- ✅ **颜色统一**（使用 shields.io 标准色）
- ✅ **放置位置**：项目描述后，目录前

#### 1. 中英双语规则

**中文部分：**
- 完整的项目介绍
- 所有章节内容
- 所有代码示例

**English Version：**
- ✅ **必须完整翻译**所有章节
- ✅ **代码示例中的注释和输出要用英文**
- ✅ **目录链接要对应英文锚点**
- ✅ **内容长度和信息量与中文一致**
- ✅ **英文部分必须有独立的 Table of Contents**
- ✅ **英文 TOC 条目数量必须与中文一致**

**章节对应规则：**
- 中文使用 `##` 标记主章节
- 英文使用 `###` 标记主章节
- 英文 TOC 使用 `### Table of Contents`
- 中文代码块使用 ``` 标记
- 英文代码块使用 ``` 标记

#### 2. 代码块格式

**所有代码块使用 ``` 标记**

格式：
```语言
代码内容
```

**规则：**
- ✅ **代码块必须指定语言**
- ✅ **不要使用 ~~~ 标记**
- ✅ **不要有多余的 ```**

#### 3. 可选章节

根据第 3.5 步的用户确认结果生成：
- 致谢部分（如用户确认需要）
- 贡献指南（如用户确认需要）
- 更新日志（如用户确认需要）

#### 4. 其他规则

- **Emoji 标记** - 适度使用，增强可读性
- **代码示例** - 至少 3 个实用示例
- **表格展示** - 参数、配置等用表格
- **质量检查** - 生成后自动检查

---

## 🔄 第 5 步：迭代优化

支持多次迭代，根据用户反馈修改 README。

---

## 📋 特殊场景处理

### 场景 1：已有 README

⚠️ 检测到已有 README.md

**选项：**
A. 完全重写（覆盖现有）
B. 基于现有优化（保留结构，改进内容）
C. 生成新版本（README.new.md）

### 场景 2：多语言项目

🌍 检测到多语言项目

**建议：**
A. 生成独立的 README_CN.md 和 README_EN.md
B. 在主 README 中分章节（中文 | English）

### 场景 3：大型项目

📊 检测到大型项目（>50 文件）

**建议：**
- README.md（简介 + 快速开始）
- docs/ 目录（详细文档）

---

## 🎨 README 风格指南

### 核心原则

1. **结构清晰** - emoji 标记章节，层级分明
2. **中英双语** - 默认中文 + English version，**内容完整一致**
3. **实用优先** - 根据项目类型调整
4. **灵活发挥** - 根据项目特点自由组织

### 项目类型特定内容

| 项目类型 | 特有章节 | 说明 |
|----------|---------|------|
| **Python** | 依赖安装、虚拟环境、PyPI 发布 | requirements.txt, setup.py |
| **前端** | 技术栈、构建命令、部署指南 | package.json, npm scripts |
| **API 服务** | 端点列表、请求示例、认证方式 | REST/GraphQL, curl 示例 |
| **CLI 工具** | 命令行参数、子命令、配置选项 | 参数说明，使用示例 |
| **库/SDK** | API 参考、类型定义、版本兼容性 | 函数/类说明，类型提示 |
| **OpenClaw Skill** | 触发词、使用场景、配置 | SKILL.md 内容提取 |

---

## ✅ 质量检查清单

生成 README 后自动检查：

### 基础检查

- [ ] 项目简介清晰（1-2 句话）
- [ ] 安装步骤完整且可执行
- [ ] 至少有 3 个使用示例
- [ ] 功能特点列出（3-5 个）
- [ ] 目录导航正确（如>100 行）
- [ ] 代码块指定语言
- [ ] 链接有效
- [ ] 许可证明确

### 中英双语检查

- [ ] 中文内容完整
- [ ] **English version 完整翻译所有章节**
- [ ] **英文目录链接正确（锚点用英文）**
- [ ] **英文代码示例注释已翻译**
- [ ] **英文内容长度与中文一致**
- [ ] **英文部分有独立的 Table of Contents**
- [ ] **英文 TOC 条目数量与中文目录一致**

### 可选章节检查

- [ ] **致谢部分已询问用户**（有/无）
- [ ] 贡献指南已询问（需要/不需要）
- [ ] 更新日志已询问（需要/不需要）

### Badge 检查（新增）

- [ ] **项目描述后有 Badge 区域**
- [ ] **使用 3 行布局**（核心信息 + 平台 + 许可证）
- [ ] **使用 HTML 注释分行**（`<!-- Badge Row X: ... -->`）
- [ ] **Version Badge 已生成**（无版本号时为 0.0.1）
- [ ] **平台 Badge 正确**（默认 macOS+Windows+Linux 或用户指定）
- [ ] **License Badge 正确**（根据实际 License 或默认 MIT）
- [ ] **每个 Badge 都有链接**
- [ ] **颜色符合标准**（使用 shields.io 标准色）

### 代码块检查

- [ ] **代码块使用 ``` 标记（无 ~~~）**
- [ ] **无多余的 ```**

### 禁止项

- ❌ **不要自动生成致谢部分**（必须先询问）
- ❌ **不要省略 English version 的内容**
- ❌ **不要使用中文锚点生成英文目录**
- ❌ **英文部分不要缺少 Table of Contents**
- ❌ **英文 TOC 条目不要与中文不一致**
- ❌ **不要使用 ~~~ 标记代码块**
- ❌ **不要生成多余的 ```**
- ❌ **Badge 不要缺少 Version**（无版本号时必须用 0.0.1）
- ❌ **平台 Badge 不要错误**（用户未指定时必须 macOS+Windows+Linux）
- ❌ **License 不要错误**（必须读取实际 License 或默认 MIT）
- ❌ **Badge 不要缺少链接**
- ❌ **不要省略 HTML 注释分行**

---

## 📝 版本管理

### 备份策略

生成前备份现有 README：
`cp README.md README.md.bak.日期`

### 版本记录

在 README 末尾添加更新日志章节。

---

## 🔧 配置选项

### 语言设置

| 参数 | 说明 | 默认 |
|------|------|------|
| `--lang bilingual` | 中英双语 | ✅ |
| `--lang chinese` | 仅中文 | - |
| `--lang english` | 仅英文 | - |

### 详细程度

| 参数 | 章节 | 适合 |
|------|------|------|
| `--detail minimal` | 简介、安装、使用 | 小型项目 |
| `--detail standard` | + 功能、API、贡献 | 中型项目（默认） |
| `--detail complete` | + FAQ、基准、架构 | 大型项目 |

### 风格选项

| 参数 | 说明 |
|------|------|
| `--style professional` | 简洁专业 |
| `--style friendly` | 活泼友好（emoji+ 双语） |
| `--style complete` | 详细完整 |

---

## 🚀 快速上手

### 基础使用

```
为这个项目写 README：~/.openclaw/skills/my-project
```

### 指定风格

```
为 https://github.com/user/repo 写 README，参考 skill-rembg 风格
```

### 指定类型

```
为 Python 项目写 README，突出 API 文档
```

---

## 📄 许可证

MIT License

---

**Happy Documenting! 📝✨**

[Top / 返回顶部](#readme-writer---项目文档生成器)
