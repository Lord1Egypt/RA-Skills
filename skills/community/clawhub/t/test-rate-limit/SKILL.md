---
name: kimi_cli_headless_execution
title: Kimi CLI 无头执行操作手册
version: 1.0
language: zh-CN
category: dev-tool-cli-automation
description: >
  教 OpenClaw 在自动化脚本、后台任务、CI/CD、无 TTY 环境等非交互场景中，
  正确使用 Kimi Code CLI 的 `-p/--prompt`、`--print`、`--quiet`、`--wire` 等参数完成无头执行。
  涵盖命令构造、自动审批控制、输出格式选择、会话管理、错误处理与安全护栏。
tags:
  - Kimi CLI
  - headless
  - 无头执行
  - 自动化
  - CI/CD
  - 命令行工具
  - 代码代理
owner: Assistant
status: production-ready
---

# Skill: Kimi CLI 无头执行操作手册

## Overview

Kimi Code CLI 默认以交互式 Shell/TUI 模式启动，但在自动化场景中需要**无头执行**（不进入交互界面，传入提示词后直接输出结果并退出）。本 Skill 指导 Agent 在需要调用 `kimi` 命令完成后台任务时，如何构造正确的无头执行命令，确保输出可控、错误可处理、操作安全。

---

## Core Mission

执行本 Skill 时，最终必须做到：

1. **构造出可在当前环境直接执行的 `kimi` 无头命令**
2. **根据场景选择最合适的输出模式**（`--quiet` 快速文本 / `--print` 完整过程 / `--wire` 服务化）
3. **明确是否启用自动审批（`--yolo`）并告知用户风险**
4. **处理命令执行结果或错误，给出下一步建议**

---

## Trigger Conditions

在以下情况下必须触发本 Skill：

- 用户要求 Agent **使用 Kimi CLI 自动完成某个任务**（如“让 Kimi CLI 无头重构这段代码”、“用 Kimi CLI 分析当前目录的 bug”）
- 任务需要运行在 **无 TTY 环境**、**后台脚本** 或 **CI/CD 流水线** 中
- 用户询问 **Kimi CLI 是否支持无头模式 / 非交互执行 / 自动化调用**
- Agent 自身需要通过 `kimi` 命令行工具调用 Kimi 模型能力，而不是通过 API 直接请求

## Non-Trigger Cases

以下情况不应套用本 Skill 的完整执行流程：

- 用户只是问 Kimi CLI 的安装、登录、配置方法（直接文字回答即可）
- 用户想手动和 Kimi CLI 进行交互式聊天（建议用户直接运行 `kimi`）
- 当前环境未安装 `kimi` 命令，且用户未要求安装（应先提示安装或换用 API）
- 用户要求比较 Kimi CLI 与其他 CLI 工具的优缺点（纯问答场景）

---

## Pre-Flight Check

在构造命令前，必须先确认：

1. **命令是否存在**：运行 `which kimi` 或 `kimi --version`，确认 Kimi CLI 已安装
2. **是否需要登录**：若用户未配置 API Key 且未通过 `kimi login` 登录，需提示用户先完成认证
3. **工作目录是否正确**：若任务涉及特定项目路径，必须显式使用 `--work-dir PATH`
4. **是否需要文件修改权限**：若 Kimi CLI 需要自动修改文件/执行 Shell，必须加 `--yolo`（并告知风险）

---

## Command Reference

### 基础无头执行（最常用）

| 参数 | 简写 | 说明 |
|------|------|------|
| `--prompt TEXT` | `-p` | 传入用户提示，不进入交互模式 |
| `--command TEXT` | `-c` | `--prompt` 的别名 |
| `--print` | | 以 Print 模式运行（非交互式），隐式启用 `--yolo` |
| `--quiet` | | 等价于 `--print --output-format text --final-message-only` |
| `--yolo` | `-y` | 自动批准所有文件修改和 Shell 命令执行 |
| `--work-dir PATH` | `-w` | 指定工作目录 |
| `--model NAME` | `-m` | 指定模型，覆盖配置文件 |
| `--continue` | `-C` | 继续当前工作目录的上一个会话 |
| `--session ID` / `--resume ID` | `-S` / `-r` | 恢复指定会话 |
| `--output-format FORMAT` | | 仅在 `--print` 下有效：`text`（默认）或 `stream-json` |
| `--final-message-only` | | 仅在 `--print` 下有效：只输出最终 assistant 消息 |
| `--wire` | | 以 Wire 服务器模式运行（实验性），适合程序集成 |

### 关键模式选择策略

- **快速单次问答（推荐默认）**：`kimi -p "任务描述" --quiet`
  - 优点：输出最干净，直接返回最终结论，适合脚本捕获
  - 缺点：不展示中间思考/工具调用过程

- **需要观察完整过程**：`kimi -p "任务描述" --print`
  - 优点：能看到 Kimi CLI 使用的工具、执行的命令、读取的文件
  - 缺点：输出较长，包含中间步骤，需 Agent 自行过滤关键信息

- **需要结构化/流式输出**：`kimi -p "任务描述" --print --output-format stream-json`
  - 优点：每行一个 JSON 对象，便于程序解析
  - 缺点：需要额外的 JSON 解析逻辑

- **长任务/多轮迭代**：`kimi -p "任务描述" --print --max-ralph-iterations N`
  - 开启 Ralph 循环模式，让 Agent 反复迭代直到完成任务或达到上限

- **服务化/后台常驻**：`kimi --wire`
  - 启动 Wire 协议服务器，供本地客户端（如 IDE 插件、其他 Agent）通过协议通信
  - 不接受初始提示词，需要配合 Wire 客户端使用

---

## Execution Policy

执行时必须按以下顺序构造命令：

### Step 1：确定执行模式
根据用户需求选择输出模式：
- 只需要最终结果 → `--quiet`
- 需要查看 Kimi 的分析/操作过程 → `--print`
- 需要程序解析 → `--print --output-format stream-json`

### Step 2：确定是否需要自动审批
若任务涉及**读写文件、执行 Shell 命令、安装依赖**等需要审批的操作：
- 无头模式下必须加 `--yolo`（或依赖 `--print` 隐式启用 `--yolo`）
- **但在加之前，必须向用户声明风险**："YOLO 模式下所有文件修改和命令都会自动执行，请确认是否继续？"

### Step 3：确定工作目录
若任务与当前目录无关，或需要操作特定项目：
- 显式添加 `--work-dir "目标路径"`

### Step 4：确定会话策略
- 全新单次任务：不加会话参数
- 继续之前的上下文：加 `--continue`
- 恢复指定会话：加 `--session <ID>`

### Step 5：组装并执行
按照以下优先级拼接命令（注意参数顺序）：

```bash
kimi \
  [--work-dir PATH] \
  [--model NAME] \
  [--continue | --session ID] \
  -p "具体任务提示词" \
  [--quiet | --print [--output-format stream-json] [--final-message-only]] \
  [--yolo]
```

**典型命令示例**：

```bash
# 示例1：快速无头分析当前目录代码
kimi -p "分析当前项目的主要架构和潜在问题" --quiet

# 示例2：让 Kimi 自动修复指定文件的 bug（自动审批）
kimi -w ./src -p "修复 main.py 中的空指针异常" --quiet --yolo

# 示例3：完整过程输出，用于观察 Kimi 的思考链
kimi -p "为这个项目添加单元测试" --print

# 示例4：结构化流式输出，供程序解析
kimi -p "生成 CHANGELOG" --print --output-format stream-json

# 示例5：恢复之前会话继续工作
kimi -w ./my-project -p "继续完成刚才的优化" --continue --quiet --yolo
```

---

## Output Handling

### `--quiet` 模式输出
直接返回纯文本字符串，可直接作为答案呈现给用户，无需额外解析。

### `--print` + `text` 模式输出
通常包含：
- 系统信息（版本、模型等）
- 工具调用记录（读取文件、执行命令）
- 思考过程
- 最终回答

Agent 应该：
1. 先检查退出码（`$?`）是否为 0
2. 向用户摘要展示关键动作（如“Kimi 读取了 3 个文件，执行了 2 条命令”）
3. 提取最终结论部分呈现

### `--print` + `stream-json` 模式输出
每行是一个 JSONL 对象，常见 `type` 字段包括：
- `start`：开始
- `thinking`：思考内容
- `tool_call` / `tool_result`：工具调用及结果
- `content`：模型生成的内容片段
- `done`：结束标记

Agent 应该：
- 过滤 `type == "content"` 的片段拼接成完整回复
- 或过滤 `type == "tool_result"` 获取工具执行结果

### Wire 模式
`kimi --wire` 启动后，需要配合 Wire 客户端进行通信。此模式下：
- 不输出到 stdout
- 在默认端口（或配置端口）监听
- Agent 应告知用户 "Wire 服务器已启动，请通过 Wire 客户端连接"

---

## Guardrails

1. **未经许可不得在关键系统目录使用 `--yolo`**
   - 避免在 `$HOME` 根目录、`/etc`、`/usr` 等全局目录自动执行命令
2. **必须确认 `--yolo` 的风险**
   - 在启用前向用户明确说明：所有文件修改和 Shell 命令都会自动执行，无法撤销
3. **优先使用 `--quiet` 避免信息过载**
   - 除非用户明确要求查看过程，否则默认用 `--quiet`
4. **不要混淆 `-p` 的两种含义**
   - 在 `kimi` 主命令中 `-p` 是 `--prompt`
   - 在 `kimi web` 子命令中 `-p` 是 `--port`，注意上下文
5. **检查命令退出码**
   - Kimi CLI 执行失败时（如 API 限流、网络错误、认证失败），应捕获 stderr 并告知用户
6. **避免在 `--quiet`/`--print` 中混用交互式参数**
   - 无头模式下不要期望用户能在中途输入确认

---

## Failure Modes

### Failure Mode 1：未安装 Kimi CLI
**表现**：`command not found: kimi`  
**处理**：提示用户通过 `pip install kimi-cli` 或官方推荐方式安装，或换用 Moonshot API 直接调用。

### Failure Mode 2：未登录/未配置 API Key
**表现**：报错信息包含 `Unauthorized`、`请登录` 或 `API key not found`  
**处理**：提示用户运行 `kimi login` 或在 `~/.kimi/config.toml` 中配置 API key。

### Failure Mode 3：加了 `--yolo` 但用户不想自动执行
**表现**：用户反馈 "Kimi 直接改了我文件但我没同意"  
**处理**：道歉并解释 `--yolo` 的作用，今后在涉及文件修改前必须显式征得同意。

### Failure Mode 4：`--print --output-format stream-json` 输出为空或解析失败
**表现**：没有任何 stdout 或 JSON 解析报错  
**处理**：先降级到 `--quiet` 或 `--print --output-format text` 重新执行，确认是基础命令问题还是格式问题。

### Failure Mode 5：会话恢复失败
**表现**：`--continue` 或 `--session ID` 提示会话不存在  
**处理**：不加会话参数以新建会话执行，或提示用户通过 `kimi info` 查看可用会话。

---

## Input Schema

```yaml
input_schema:
  type: object
  required:
    - task_description
  properties:
    task_description:
      type: string
      description: 要交给 Kimi CLI 执行的具体任务描述
    work_dir:
      type: string
      description: 工作目录路径，默认为当前目录
    output_mode:
      type: string
      enum: [quiet, print, stream-json, wire]
      description: 输出模式选择
    auto_approve:
      type: boolean
      description: 是否启用 --yolo 自动审批
    model:
      type: string
      description: 指定使用的模型名称
    session_strategy:
      type: string
      enum: [new, continue, resume]
      description: 会话策略
    session_id:
      type: string
      description: 当 session_strategy 为 resume 时必填
```

## Output Schema

```yaml
output_schema:
  type: object
  properties:
    constructed_command:
      type: string
      description: 最终构造并执行的 kimi 命令
    execution_result:
      type: string
      description: 命令输出内容或结果摘要
    exit_code:
      type: integer
      description: 命令退出码
    warnings:
      type: array
      items:
        type: string
      description: 执行过程中的警告或风险提示
    next_steps:
      type: array
      items:
        type: string
      description: 建议的后续操作
```

---

## Response Template

```markdown
### 构造的命令
\`\`\`bash
{constructed_command}
\`\`\`

### 执行结果
{execution_result_summary}

### 风险提示
{yolo_warning_if_applicable}

### 后续建议
{next_steps}
```

---

## Final Rule

本 Skill 的终极要求只有一句话：

**在无头场景下调用 Kimi CLI 时，必须让命令“一次成型、自动跑完、输出干净、风险可知”。**

- 不要构造出还需要人机交互的命令
- 不要在用户不知情时自动修改文件
- 不要让输出模式与解析需求不匹配
- 命令执行失败后，要有清晰的降级方案
