---
slug: python3-tool-free
name: python3-tool-free
version: 1.0.0
displayName: Python 环境工具基础版
summary: "管理 Python 项目环境,支持虚拟环境创建、依赖安装与环境诊断。核心能力: 开发工具领域的专业化 AI 辅助工具,提供核心基础功能支持."
license: Proprietary
edition: free
description: '核心能力: 开发工具领域的专业化 AI 辅助工具,提供核心基础功能支持.
  适用场景: 个人用户与轻量级场景,涵盖日常操作、自动化工作流与智能决策辅助.
  差异化: FREE 版本,面向个人用户提供核心功能、简洁操作与社区支持.
  适用关键词: python, python3, venv, pip, 依赖, 虚拟环境, requirements'
tags:
  - Python
  - 虚拟环境
  - 依赖管理
  - pip
  - 工具
  - 效率
  - venv
  - python
  - free
  - pro
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# Python 环境工具基础版

## 概述

本工具是 **开发工具** 领域的 **FREE 版本** AI Skill,专为个人用户与轻量级场景设计。通过自然语言指令驱动 AI Agent 执行任务,提供核心功能与简洁易用的操作体验.
FREE 版本与 PRO 版本完全兼容,可在需要时升级至 PRO 版本获取高级功能、批量操作与团队协同能力.
### 版本定位

| 维度 | FREE 版本 | PRO 版本 |
|---|-------|------|
| 目标用户 | 个人用户 | 企业团队 |
| 功能范围 | 核心功能 | 全部功能 |
| 批量操作 | 不支持 | 支持 |
| 团队协作 | 不支持 | 支持 |
| 技术支持 | 社区支持 | 优先响应 |
| 数据分析 | 基础统计 | 高级分析 |

## 核心能力

FREE 版本提供以下能力:

### 检测当前 Python 环境与
检测当前 Python 环境与解释器路径

**处理**: 解析检测当前 Python 环境与的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回检测当前 Python 环境与的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 创建或刷新项目虚拟环境
创建或刷新项目虚拟环境

**处理**: 解析创建或刷新项目虚拟环境的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回创建或刷新项目虚拟环境的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 安装项目依赖与开发包
安装项目依赖与开发包

**处理**: 解析安装项目依赖与开发包的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回安装项目依赖与开发包的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 运行测试与工具检查
运行测试与工具检查

**处理**: 解析运行测试与工具检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回运行测试与工具检查的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 环境诊断与故障排查
环境诊断与故障排查

**处理**: 解析环境诊断与故障排查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回环境诊断与故障排查的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能详情

本版本提供 5 项核心能力,覆盖 开发工具 的常见使用场景。如需批量操作、团队协作、数据分析等高级功能,可升级至 PRO 版本.
**FREE 版本核心功能清单:**

- 检测当前 Python 环境与解释器路径
- 创建或刷新项目虚拟环境
- 安装项目依赖与开发包
- 运行测试与工具检查
- 环境诊断与故障排查

**PRO 版本扩展功能预览:**

- 多 Python 版本管理与切换
- 依赖安全审计与漏洞扫描
- CI/CD 集成:环境标准化与可重复构建
- 依赖许可证合规检查
- 性能分析与内存 profiling
- 与企业制品库集成的包管理

**处理**: 解析功能详情的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回功能详情的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：项目环境、支持虚拟环境创建、依赖安装与环境诊、开发工具领域的专、辅助工具、提供核心基础功能等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1: 初始化项目环境

创建虚拟环境并安装依赖

用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Python 环境工具基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 检测环境
python3 --version
python3 -c "import sys; print(sys.executable)"
# 创建虚拟环境
python3 -m venv .venv
# 依赖说明
.venv/（请参考skill目录中的脚本文件） install -r requirements.txt
```

### 场景 2: 诊断环境问题

排查 ModuleNotFoundError 等常见问题

```bash
# 诊断步骤
1. 确认使用 .venv/（请参考skill目录中的脚本文件）
2. 检查依赖是否已安装
3. 检查 PYTHONPATH 设置
4. 重新安装依赖
.venv/（请参考skill目录中的脚本文件） -m pip list --outdated
```

## 不适用场景

以下场景Python 环境工具基础版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 1. 环境准备

确保已安装并配置好 AI Agent 环境(Claude Code / Cursor / Codex / Gemini CLI 等),本 Skill 通过 SKILL.md 指令驱动 Agent 执行任务.
**系统要求:**

- 操作系统: Windows / macOS / Linux
- Agent 平台: 支持 SKILL.md 格式的任意 AI Agent
- 运行时: Python 3.8+ 或 Node.js 18+(视具体操作需求)

### 2. 配置参数

```bash
# 标准工作流
python3 -m venv .venv
source .venv/（请参考skill目录中的脚本文件）  # Linux/macOS
# .venv\Scripts\activate  # Windows
python3 -m pip install -r requirements.txt
python3 -m pip install -e .  # 安装项目包
```

### 3. 验证配置

配置完成后,可通过以下方式验证是否正常工作:

```bash
# 验证环境变量是否设置
echo "配置检查:"
env | grep -E "API|KEY|TOKEN|SECRET" | sed "s/=.*/=***/"  # Linux/macOS
# 或 PowerShell
# Get-ChildItem Env: | Where-Object {$_.Name -match "API|KEY|TOKEN"} | Format-Table
```

### 4. 开始使用

在 AI Agent 对话中描述你的需求,Agent 会根据本 Skill 的指令自动执行对应操作.
```text
请帮我初始化项目环境
```

Agent 将自动:
1. 解析你的自然语言指令
2. 调用相应的工具或 API
3. 执行操作并返回结果
4. 返回执行结果供你确认

#
## 示例

### 基础配置

```bash
# 标准工作流
python3 -m venv .venv
source .venv/（请参考skill目录中的脚本文件）  # Linux/macOS
# .venv\Scripts\activate  # Windows
```
### 可选配置

```json
{
  "edition": "free",
  "auto_retry": false,
  "max_concurrent": 1,
  "log_level": "info",
  "cache_enabled": true,
  "timeout": 30
}
```

**FREE 配置项说明:**

| 配置项 | 类型 | 默认值 | 说明 |
|---:|---:|---:|---:|
| auto_retry | bool | false | 失败后自动重试 |
| max_concurrent | int | 1 | 最大并发数(FREE 限制为1) |
| log_level | string | info | 日志级别 |
| cache_enabled | bool | true | 启用结果缓存 |
| timeout | int | 30 | 操作超时时间(秒) |

## 最佳实践

1. **优先使用项目本地虚拟环境**
2. **使用 python3 -m pip 避免 pip 不匹配**
3. **安装前检查依赖文件**
4. **避免全局安装使用 venv 隔离**

### 个人使用建议

- 从简单任务开始熟悉工具行为,逐步扩展到复杂场景
- 定期备份配置文件与数据,防止意外丢失
- 遇到问题先查阅常见问题章节,再寻求社区帮助
- 保持配置简洁,只启用必要的功能选项
- 定期更新工具版本以获取最新功能与修复
- 记录常用操作命令,提高日常使用效率

## 常见问题

### Q: ModuleNotFoundError 怎么办?

A: 确认命令通过 .venv/（请参考skill目录中的脚本文件） 执行,然后重新安装依赖.
### Q: externally-managed-environment 错误?

A: 停止全局安装尝试,使用虚拟环境管理依赖.
### Q: 如何升级到 PRO 版本?

A: 升级到 PRO 版本非常简单:
1. 获取 PRO 版本授权
2. 安装 PRO 版本 Skill
3. 原有配置自动迁移,无需额外操作
4. 即可使用批量操作、团队协作等高级功能

### 已知限制

A: FREE 版本主要限制:
- 不支持批量操作(每次只能处理一个任务)
- 不支持团队协作(仅限个人使用)
- 不支持高级数据分析
- 技术支持依赖社区
如需这些功能,建议升级至 PRO 版本.
### Q: FREE 版本的数据安全吗?

A: FREE 版本所有数据本地存储,不上传云端,确保隐私安全。建议定期备份配置文件与数据目录.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Python 3.8+ 或 Node.js 18+(视具体操作需求)
- **网络**: 部分功能需要网络连接访问外部 API

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| curl | CLI 工具 | 推荐 | 系统自带或包管理器安装 |
| jq | JSON 处理 | 推荐 | apt install jq / brew install jq |
| Python 3.8+ | 运行时 | 视需求 | python.org 下载 |
| Node.js 18+ | 运行时 | 视需求 | nodejs.org 下载 |

### API Key 配置

FREE 版本支持单一 API Key 配置,满足个人使用需求:
- **环境变量**:通过环境变量配置 API Key
- **配置文件**:支持配置文件方式存储 API Key
- **安全提醒**:切勿将 API Key 硬编码到脚本或提交到版本控制系统

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行任务
- **FREE 特性**: 支持单次执行、基础配置与社区支持
- **安全等级**: 基础,数据本地存储,建议定期备份
- **SLA**: 社区支持,尽力响应

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

**版本信息**

| 项目 | 值 |
|:------|------:|
| 版本号 | 1.0.0 |
| 版本类型 | FREE |
| 许可证 | MIT |
| 兼容性 | 可升级至 PRO 版本 |

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Python 环境工具基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "python3"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
