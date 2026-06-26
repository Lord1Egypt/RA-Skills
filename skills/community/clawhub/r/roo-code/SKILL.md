---
name: "Roo Code"
version: "1.0.0"
description: "Roo Code AI 编程助手，精通 VS Code 内 AI Agent、多模式切换、MCP 集成"
tags: ["ai-coding", "vscode", "roo-code", "agent"]
author: "ClawSkills Team"
category: "developer-tools"
---
# Roo Code - VS Code 内的 AI 编程 Agent

## 简介
Roo Code（原名 Roo Cline，fork 自 Cline）是一款 VS Code 扩展，能在编辑器内自主执行多步编程任务。
它不只是代码补全——而是一个真正的 AI Agent，可以读写文件、执行终端命令、浏览网页、调用 MCP 工具。

## 核心功能
- **自主多步执行**：理解需求后自动规划步骤，逐步执行文件创建/修改/删除
- **文件读写**：直接在编辑器中创建和修改文件，带 diff 预览确认
- **终端命令执行**：运行 shell 命令（安装依赖、运行测试、启动服务等）
- **浏览器集成**：内置浏览器可截图查看页面效果，辅助前端开发
- **MCP Server 集成**：连接外部工具服务器，扩展 AI 能力边界
- **上下文提及（@）**：用 `@file` `@folder` `@url` 精确引用上下文

## 多模式系统
Roo Code 内置多种工作模式，每种模式有不同的系统提示词和工具权限：

| 模式 | 用途 | 可用工具 |
|------|------|---------|
| **Code** | 日常编码（默认） | 文件读写 + 终端 + 浏览器 |
| **Architect** | 架构设计与规划 | 只读文件 + 分析（不修改代码） |
| **Ask** | 问答与代码解释 | 只读文件（不执行任何操作） |
| **Debug** | 调试与问题排查 | 文件读写 + 终端 + 日志分析 |

切换模式：在聊天输入框顶部点击模式按钮，或在对话中输入 `@mode code`。

## 自定义模式（.roomodes）
在项目根目录创建 `.roomodes` 文件定义团队专属模式：
```json
{
  "customModes": [
    {
      "slug": "reviewer",
      "name": "Code Reviewer",
      "roleDefinition": "你是一位严格的代码审查员，关注安全性、性能和可维护性。",
      "groups": ["read"],
      "source": "project"
    },
    {
      "slug": "tester",
      "name": "Test Writer",
      "roleDefinition": "你是测试工程师，擅长编写全面的单元测试和集成测试。",
      "groups": ["read", "edit", "command"],
      "source": "project"
    }
  ]
}
```

## MCP Server 集成
Roo Code 支持通过 MCP（Model Context Protocol）连接外部工具：
```json
// .vscode/mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-github"],
      "env": { "GITHUB_TOKEN": "${env:GITHUB_TOKEN}" }
    }
  }
}
```
配置后 AI 可直接调用这些工具完成 GitHub 操作、数据库查询等任务。

## 支持的模型
| 供应商 | 模型 | 说明 |
|--------|------|------|
| Anthropic | Claude Sonnet/Opus | 官方推荐，效果最佳 |
| OpenAI | GPT-4o / o1 | 通过 API Key 配置 |
| Google | Gemini 2.0 Flash/Pro | 免费额度较多 |
| DeepSeek | DeepSeek V3/R1 | 高性价比 |
| Ollama | 本地模型 | 离线使用，隐私安全 |
| OpenRouter | 聚合多模型 | 一个 Key 用所有模型 |

## 与同类工具对比
| 特性 | Roo Code | Cline | Cursor | GitHub Copilot |
|------|----------|-------|--------|----------------|
| 开源 | 是（Apache 2.0） | 是 | 否 | 否 |
| Agent 能力 | 强（多步自主） | 强 | 中 | 弱 |
| 自定义模式 | 支持 .roomodes | 不支持 | 不支持 | 不支持 |
| MCP 集成 | 原生支持 | 原生支持 | 不支持 | 不支持 |
| 模型自由度 | 任意模型 | 任意模型 | 限定模型 | 限定模型 |
| 更新频率 | 极高（社区活跃） | 较高 | 高 | 中 |

## 典型使用场景
- **全栈开发**：Code 模式下一次对话完成前后端功能开发
- **架构评审**：Architect 模式分析项目结构，输出改进建议
- **自动化调试**：Debug 模式读取错误日志，定位并修复问题
- **项目初始化**：从零搭建项目骨架，包括配置文件和目录结构
- **MCP 扩展**：连接数据库/API/文件系统等外部工具完成复杂任务

## 安装
在 VS Code 扩展市场搜索 "Roo Code" 安装，或命令行：
```bash
code --install-extension RooVeterinaryInc.roo-cline
```
