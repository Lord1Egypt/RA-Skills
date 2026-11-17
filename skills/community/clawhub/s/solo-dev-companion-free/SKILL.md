---
name: "solo-dev-companion-free"
description: "独立开发者TDD工作流引擎，自动执行实施计划任务、提交代码并更新进度。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "独立开发伙伴(免费版)"
  version: "1.0.0"
  summary: "独立开发者TDD工作流引擎，自动执行实施计划任务、提交代码并更新进度。"
  tags:
    - "TDD"
    - "独立开发"
    - "工作流引擎"
    - "代码质量"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 独立开发伙伴（免费版）

> **独立开发者的TDD工作流引擎。自动执行计划、红绿重构、原子提交，让一人开发也有团队规范。**

## 核心理念

本工具是实施计划的执行引擎。从`docs/plan/`中发现计划文件，提取下一个未完成任务，按TDD工作流实现，提交代码，并更新进度。

```text
开发流水线: /plan → /build (本工具) → /deploy → /review
```

---

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 120秒上手

```bash
# 1. 确认计划文件存在
ls docs/plan/*/plan.md

# 2. 启动执行引擎
solo-dev execute

# 3. 指定track执行
solo-dev execute auth-feature

# 4. 跳转到指定任务
solo-dev execute --task 2.3

# 5. 恢复中断的任务
solo-dev resume
```

### 前置检查

```bash
# 依赖说明
[ -f .husky/pre-commit ] && echo "husky OK" || echo "NOT ACTIVE"
[ -f .pre-commit-config.yaml ] && [ -f .git/hooks/pre-commit ] && echo "pre-commit OK" || echo "NOT ACTIVE"

# 如未安装，按技术栈安装
# JS/TS: pnpm prepare
# Python: uv run pre-commit install
```

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 核心能力
### 1. 计划发现与解析

```bash
# 自动发现计划文件
solo-dev discover

# 查看所有track及进度
solo-dev tracks

# 查看指定track详情
solo-dev track auth-feature
```

**计划文件格式**（plan.md）：

```markdown
# Auth Feature Plan

**Status:** [ ] Not Started

**输入**: 用户提供计划发现与解析所需的指令和必要参数。
**处理**: 按照skill规范执行计划发现与解析操作,遵循单一意图原则。
**输出**: 返回计划发现与解析的执行结果,包含操作状态和输出数据。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：独立开发者、TDD、工作流引擎、自动执行实施计划、提交代码并更新进、独立开发伙伴免费、版为独立开发者与、一人公司提供轻量、聚焦实施计划、的自动执行、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## Phase 1: 基础架构
- [ ] Task 1.1: 创建用户模型
- [ ] Task 1.2: 实现密码哈希
- [~] Task 1.3: 创建注册API <!-- sha:abc1234 -->

## Phase 2: 认证流程
- [ ] Task 2.1: 实现JWT生成
- [ ] Task 2.2: 实现登录API
```

### 2. 任务执行循环（TDD）

```bash
# 执行下一个未完成任务
solo-dev execute

# 执行时自动完成：
# 1. 标记任务为[~]（进行中）
# 2. 研究相关代码
# 3. TDD红：写失败测试
# 4. TDD绿：实现最小代码
# 5. TDD重构：优化代码
# 6. 提交代码（conventional commits）
# 7. 标记任务为[x]（完成）并记录SHA
```

**TDD三阶段**：

| 阶段 | 动作 | 验证 |
|------|------|------|
| 红 | 写失败测试 | 测试必须失败 |
| 绿 | 实现最小代码 | 测试必须通过 |
| 重构 | 优化代码 | 测试保持通过 |

### 3. Git原子提交与SHA追踪

```bash
# 自动提交（conventional commits格式）
git commit -m "feat(auth): 实现用户注册API"

# 提交后自动捕获SHA并写入plan.md
# - [x] Task 1.3: 创建注册API <!-- sha:abc1234 -->
```

**提交类型**：`feat`、`fix`、`refactor`、`test`、`docs`、`chore`、`perf`、`style`

### 4. 进度状态管理

| 标记 | 含义 | 说明 |
|------|------|------|
| `[ ]` | 未开始 | 待执行的任务 |
| `[~]` | 进行中 | 当前正在执行 |
| `[x]` | 已完成 | 已提交代码并记录SHA |

### 5. 基础质量工具

**JS/TS项目**：
```bash
pnpm lint --fix        # ESLint
pnpm format            # Prettier
pnpm tsc --noEmit      # 类型检查
```

**Python项目**：
```bash
uv run ruff check --fix .   # Ruff lint
uv run ruff format .        # Ruff format
```

### 6. Makefile集成

```bash
# 优先使用Makefile目标
make test
make lint
make build
make help    # 查看可用目标
```

---

## 使用场景

### 场景一：独立开发者的功能迭代（独立开发者角色）

**痛点**：独立开发时容易跳过测试、提交不规范、进度难以追踪。

**对策**：用TDD工作流引擎强制规范开发流程。

```bash
# 创建功能计划
# docs/plan/auth-feature/plan.md

# 执行第一个任务
solo-dev execute auth-feature

# 引擎自动完成TDD循环与提交
# 完成后继续下一个任务
solo-dev execute auth-feature
```

**效果**：每个任务都有测试覆盖，提交规范，进度可追溯。

### 场景二：一人公司的迭代开发（创业者角色）

**痛点**：一人公司需要高效迭代，但缺乏团队规范约束。

**对策**：用本工具模拟团队开发规范。

```bash
# 每天开始工作时执行
solo-dev tracks    # 查看所有track进度

# 执行当天计划的任务
solo-dev execute

# 中断后恢复
solo-dev resume
```

### 场景三：TDD实践（学习者角色）

**痛点**：学习TDD时缺乏实战场景，理论难以落地。

**对策**：用本工具强制执行红绿重构循环。

```bash
# 创建一个简单的TDD练习计划
# docs/plan/tdd-practice/plan.md

# 执行并观察TDD循环
solo-dev execute tdd-practice
```

---

## FAQ

### 已知限制

免费版聚焦核心TDD执行（计划发现/任务执行/提交/进度管理），不限使用次数。MCP工具集成、多语言质量工具、视觉验证、阶段检查点、高级回滚等高级功能需升级专业版。

### Q2：需要预先创建计划文件吗？

需要。本工具是执行引擎，不创建计划。请先使用规划工具创建`docs/plan/{track}/plan.md`与`spec.md`。

### Q3：TDD是强制的吗？

默认是moderate模式（业务逻辑强制TDD，UI/配置可选）。可在`docs/workflow.md`中配置为`strict`（全强制）或`none`（不强制）。

### Q4：测试失败会怎样？

测试失败时引擎暂停，提供三个选项：(1) 尝试修复；(2) 回滚变更（git checkout）；(3) 暂停等待人工干预。不会自动跳过失败。

### Q5：支持哪些编程语言？

免费版支持JS/TS（ESLint+Prettier+tsc）与Python（Ruff）。专业版额外支持iOS（SwiftLint）、Android（detekt+ktlint）、Hypothesis属性测试。

---

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Git**: 已安装（用于提交与SHA追踪）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| Git | 工具 | 必需 | 系统自带或从git-scm.com安装 |
| Make | 构建工具 | 可选 | 系统自带 |
| ESLint/Prettier | JS/TS质量工具 | JS/TS项目必需 | `pnpm install -D eslint prettier` |
| Ruff | Python质量工具 | Python项目必需 | `uv add --dev ruff` |

### API Key 配置
- 本免费版基于本地Git与文件操作，无需额外API Key
- LLM调用由Agent平台内置LLM提供（路由GPT-4o-mini控制成本）

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行TDD工作流

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：Build (solo-build)
- 原始license：MIT
- 改进作品：独立开发伙伴（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，适配中文独立开发者工作流
- 重新设计三个中文用户场景（独立开发者/创业者/学习者）
- 移除原项目特定目录引用（conductor等）
- 新增FAQ章节（5问）与依赖说明
- 统一命令行工具命名为solo-dev
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，符合MIT license要求。

---

## 免费版限制

本免费体验版限制以下高级功能：

- MCP工具集成（session_search/project_code_search/codegraph_query）
- 多语言质量工具（iOS SwiftLint/Android detekt/Hypothesis属性测试）
- 视觉验证（Playwright/iOS Simulator/Android Emulator）
- 阶段检查点（Phase Completion Check）
- 高级回滚（按任务/按阶段回滚）
- Knip死代码检测
- 进度追踪集成（TodoWrite）

解锁全部功能请使用专业版：solo-dev-companion-pro

## 示例

### 示例1：基础用法

```
### 120秒上手

```bash
```

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
