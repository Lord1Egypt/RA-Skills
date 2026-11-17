---
name: text-helper
description: A Day3 OpenClaw training skill for keyword extraction, content summary, and todo list generation.
---

# text-helper

This is a Day3 OpenClaw training skill for organizing study notes, technical text, and task descriptions.

## 功能

本 Skill 包含两个工具：

1. **extract_keywords**
   从输入文本中提取关键词，适合整理学习笔记、技术文档和任务描述。

2. **generate_todo_list**
   根据任务或项目描述生成待办事项清单，适合把自然语言任务整理成可执行步骤。

## 使用场景

- 从学习笔记中提取重点关键词
- 从技术文档中提炼核心概念
- 将任务描述整理成待办清单
- 辅助 OpenClaw / Kaiser 完成文本整理类任务

## 输入示例

**关键词提取：**
请从这段话里提取5个关键词：今天学习OpenClaw Skill开发，重点包括skill.json、TypeScript源代码、MCP协议和工具调用链路。

**待办清单生成：**
请根据这段描述生成待办清单：我要完成Day3 Skill开发作业，包括创建项目、编写skill.json、实现TypeScript代码、注册Skill、测试并整理日志。

## 文件说明

- skill.json：定义 Skill 名称、描述和工具参数
- src/index.ts：实现关键词提取和待办清单生成逻辑
- package.json：定义依赖和构建命令
- tsconfig.json：定义 TypeScript 编译规则
- README.md：说明 Skill 的功能和使用方式
