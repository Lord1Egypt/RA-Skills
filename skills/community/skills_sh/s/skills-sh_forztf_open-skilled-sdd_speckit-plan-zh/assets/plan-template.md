# 实现计划：[功能]

**分支**：`[###-feature-name]` | **日期**：[日期] | **规格**：[链接]
**输入**：来自 `/specs/[###-feature-name]/spec.md` 的功能规格

**注意**：此模板由 `/speckit.plan` 命令填写。请参见 `.specify/templates/commands/plan.md` 了解执行工作流程。

## 概要

[从功能规格中提取：主要需求 + 研究中的技术方法]

## 技术背景

<!--
  需要操作：用该项目的技术细节替换本节内容。
  此处提供的结构是为了指导迭代过程而提供的建议性框架。
-->

**语言/版本**：[例如，Python 3.11, Swift 5.9, Rust 1.75 或需要澄清]  
**主要依赖项**：[例如，FastAPI, UIKit, LLVM 或需要澄清]  
**存储**：[如果适用，例如，PostgreSQL, CoreData, 文件 或不适用]  
**测试**：[例如，pytest, XCTest, cargo test 或需要澄清]  
**目标平台**：[例如，Linux 服务器, iOS 15+, WASM 或需要澄清]
**项目类型**：[单体/网页/移动端 - 决定源码结构]  
**性能目标**：[领域特定，例如，1000 请求/秒, 10k 行/秒, 60 帧/秒 或需要澄清]  
**约束条件**：[领域特定，例如，<200ms p95, <100MB 内存, 支持离线 或需要澄清]  
**规模/范围**：[领域特定，例如，10k 用户, 1M LOC, 50 屏幕 或需要澄清]

## 宪章检查

*关卡：必须在第 0 阶段研究前通过。在第 1 阶段设计后重新检查。*

[基于宪章文件确定的关卡]

## 项目结构

### 文档（此功能）

```text
specs/[###-feature]/
├── plan.md              # 本文件（/speckit.plan 命令输出）
├── research.md          # 第 0 阶段输出（/speckit.plan 命令）
├── data-model.md        # 第 1 阶段输出（/speckit.plan 命令）
├── quickstart.md        # 第 1 阶段输出（/speckit.plan 命令）
├── contracts/           # 第 1 阶段输出（/speckit.plan 命令）
└── tasks.md             # 第 2 阶段输出（/speckit.tasks 命令 - 不由 /speckit.plan 创建）
```

### 源代码（仓库根目录）
<!--
  需要操作：用此功能的具体布局替换下面的占位符树。
  删除未使用的选项，并使用真实路径扩展所选结构（例如，apps/admin, packages/something）。
  提供的计划不得包含选项标签。
-->

```text
# [如果未使用则删除] 选项 1：单一项目（默认）
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [如果未使用则删除] 选项 2：Web 应用程序（当检测到 "frontend" + "backend" 时）
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [如果未使用则删除] 选项 3：移动端 + API（当检测到 "iOS/Android" 时）
api/
└── [与后端相同]

ios/ 或 android/
└── [平台特定结构：功能模块、UI 流程、平台测试]
```

**结构决策**：[记录选择的结构并引用上面捕获的真实目录]

## 复杂度跟踪

> **仅当宪章检查存在必须证明合理性的违规情况时才填写**

| 违规情况 | 为何需要 | 被拒绝的更简单替代方案原因 |
|-----------|------------|-------------------------------------|
| [例如，第 4 个项目] | [当前需求] | [为什么 3 个项目不够] |
| [例如，仓储模式] | [具体问题] | [为什么直接数据库访问不够] |