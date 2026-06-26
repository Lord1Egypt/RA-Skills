---
name: "Windsurf"
version: "1.0.0"
description: "Windsurf AI IDE 助手，精通 Cascade Agent、AI Flow、规则配置、快捷键"
tags: ["ide", "ai-coding", "windsurf", "codeium"]
author: "ClawSkills Team"
category: "developer-tools"
---

# Windsurf AI IDE 技能指南

## 概述

Windsurf 是 Codeium 推出的 AI 原生 IDE，基于 VS Code fork 构建。核心卖点是 Cascade —— 一个能自主执行多步骤任务的 AI Agent，比传统的代码补全和聊天助手更进一步。

## 核心功能

### Cascade（AI Agent 模式）

Cascade 是 Windsurf 的旗舰功能，区别于普通 AI 聊天：

- **多步骤自动执行**：给出高层目标，Cascade 自动拆解为多个步骤依次执行
- **文件读写**：自动读取相关文件、创建新文件、修改现有代码
- **终端命令**：自动运行 npm install、git commit 等命令
- **上下文感知**：自动索引整个项目，理解文件间的依赖关系
- **Write/Chat 模式**：Write 模式直接修改代码，Chat 模式仅讨论不动代码

使用技巧：
- 描述目标而非步骤，让 Cascade 自己规划执行路径
- 遇到错误时 Cascade 会自动尝试修复，通常不需要手动干预
- 用 `@file` 或 `@folder` 显式指定上下文范围，提高准确度

### AI Flow（智能代码补全）

AI Flow 是 Windsurf 的上下文感知补全引擎：

- **多行补全**：不只补全当前行，能预测接下来多行代码
- **跨文件感知**：根据项目中其他文件的模式和类型定义生成补全
- **Tab 接受**：按 Tab 接受建议，按 Esc 拒绝
- **Supercomplete**：基于最近编辑行为预测下一步操作

### Cmd+I 内联编辑

选中代码后按 `Cmd+I`（macOS）或 `Ctrl+I`（Windows/Linux）：

- 直接在代码位置弹出编辑指令输入框
- 适合小范围重构、添加注释、修改逻辑
- 修改以 diff 形式展示，可逐个接受或拒绝

### Chat 面板

侧边栏对话面板，用于：
- 询问代码相关问题、解释复杂逻辑
- 生成代码片段后手动粘贴
- 用 `@` 引用文件、符号、文档等上下文

## 规则配置

在项目根目录创建 `.windsurfrules` 文件，控制 AI 行为：

```
# .windsurfrules 示例

你是一个 TypeScript 全栈开发专家。

技术栈：
- 前端：React 18 + TypeScript + Tailwind CSS
- 后端：Node.js + Express + Prisma
- 测试：Vitest + React Testing Library

代码规范：
- 使用函数式组件和 Hooks
- 所有函数必须有 TypeScript 类型标注
- 错误处理使用 try-catch，禁止静默吞错
- 组件文件使用 PascalCase 命名
```

也支持全局规则文件 `~/.windsurf/global_rules.md`，对所有项目生效。

## 快捷键速查表

| 功能 | macOS | Windows/Linux |
|------|-------|---------------|
| 打开 Cascade | `Cmd+L` | `Ctrl+L` |
| 内联编辑 | `Cmd+I` | `Ctrl+I` |
| 接受补全 | `Tab` | `Tab` |
| 拒绝补全 | `Esc` | `Esc` |
| 命令面板 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 切换 Write/Chat | 面板内切换 | 面板内切换 |
| 引用文件 | `@file` | `@file` |
| 引用文件夹 | `@folder` | `@folder` |
| 终止执行 | `Cmd+Backspace` | `Ctrl+Backspace` |

## Windsurf vs Cursor 对比

| 维度 | Windsurf (Cascade) | Cursor (Composer) |
|------|-------------------|-------------------|
| 自主性 | 高，自动规划多步骤 | 中，需要更多人工确认 |
| 可控性 | 较低，Agent 自行决策 | 高，每步可审查 |
| 代码索引 | 自动全项目索引 | 需手动 @codebase |
| 终端集成 | 自动执行命令 | 需确认后执行 |
| 免费额度 | 有免费层 | 有免费层 |
| VS Code 兼容 | 完全兼容插件 | 完全兼容插件 |
| 适合人群 | 喜欢放手让 AI 干 | 喜欢精细控制 |

Windsurf 更像"放手让 AI 干"，Cursor 更像"AI 辅助你干"。选择取决于你对 AI 自主性的接受程度。

## 使用场景和最佳实践

**适合场景**：从零搭建脚手架、批量重构、快速原型、探索不熟悉的技术栈

**最佳实践：**
1. 先写好 `.windsurfrules`，确保 AI 输出符合团队规范
2. 大任务用 Cascade，小修改用 Cmd+I 内联编辑
3. Cascade 执行过程中可随时中断并调整方向
4. 定期检查 Cascade 的自动提交，避免引入不需要的改动
5. 敏感文件（.env、密钥）加入 `.gitignore`，防止 AI 误操作
6. 复杂项目建议分模块给 Cascade 任务，避免一次性改动过大
