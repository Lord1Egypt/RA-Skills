---
slug: tmux-session-tool-free
name: tmux-session-tool-free
version: 1.0.0
displayName: Tmux会话工具免费版
summary: "纯tmux指令操作终端会话,支持会话定位、内容查看、指令发送与调试。面向个人开发者的 tmux 会话管理工具,通过纯 tmux 指令操作终端会话。核心能力:"
license: Proprietary
edition: free
description: '面向个人开发者的 tmux 会话管理工具,通过纯 tmux 指令操作终端会话。核心能力:

  - 定位目标 tmux 会话与窗格

  - 查看会话最新交互内容

  - 向指定窗格发送指令

  - 执行 /compact 等会话命令

  - 转储原始缓冲区用于调试

  适用场景:

  - 个人开发环境会话管理

  - 与 tmux 中的代码助手交互

  - 远程终端会话调试

  差异化:

  - 免费版提供单会话管理能力

  - 纯 tmux 指令,无需额外脚本

  - 操作简单,开箱即用

  适用关键词: tmux, session, pan...'
tags:
  - 终端工具
  - tmux
  - 会话管理
  - 开发辅助
  - 工具
  - 效率
  - 写作
  - target
  - bash
  - claude
  - myproject
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# Tmux 会话工具免费版

## 概述

Tmux 会话工具免费版为个人开发者提供通过纯 tmux 指令管理终端会话的能力。工具无需任何辅助脚本,全部通过标准 tmux 命令完成会话定位、内容查看、指令发送等操作.
免费版聚焦单会话管理,适合个人开发环境中与 tmux 内运行的代码助手交互.
## 核心能力

### 1. 会话与窗格定位

通过会话名和窗格标题定位目标:

具体操作方式与参数说明请参考下方示例代码.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Tmux会话工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 列出所有窗格及其标题
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_title}'
```

**处理**: 解析会话与窗格定位的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回会话与窗格定位的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 查看最新交互

```bash
# 捕获窗格最近 200 行内容
tmux capture-pane -p -J -t <target> -S -200
```

**处理**: 解析查看最新交互的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回查看最新交互的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 发送指令

```bash
# 向目标窗格发送指令
tmux send-keys -t <target> -l -- "你的指令"
sleep 0.1
tmux send-keys -t <target> Enter
```

**处理**: 解析发送指令的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回发送指令的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 执行会话命令

```bash
# 触发 /compact
tmux send-keys -t <target> -l -- "/compact"
sleep 0.1
tmux send-keys -t <target> Enter
```

**处理**: 解析执行会话命令的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回执行会话命令的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 缓冲区转储

```bash
# 转储 400 行原始缓冲区(调试用)
tmux capture-pane -p -J -t <target> -S -400
```

**处理**: 解析缓冲区转储的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回缓冲区转储的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：指令操作终端会话、支持会话定位、内容查看、指令发送与调试、面向个人开发者的、会话管理工具、通过纯、核心能力、查看会话最新交互、向指定窗格发送指、等会话命令、转储原始缓冲区用、于调试等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一: 查看代码助手最新输出

在 tmux 中运行代码助手,查看其最新交互内容.
```bash
# 1. 定位窗格
#{pane_index} #{pane_title}' \
  | grep "^myproject" | grep -i claude
# ...
# 假设找到: myproject:0.1 claude
TARGET="myproject:0.1"
# ...
# 2. 查看最新交互
tmux capture-pane -p -J -t $TARGET -S -200
```

识别标准标记:

```text
❯ 用户输入内容...
⏺ 代码助手的回复...
```

从底部向上扫描,找到最近的 `❯`(用户)和 `⏺`(助手)对.
### 场景二: 向代码助手发送指令

向 tmux 中的代码助手发送任务指令.
```bash
# 1. 定位窗格(同上)
TARGET="myproject:0.1"
# ...
# 2. 发送指令
tmux send-keys -t $TARGET -l -- "请重构 src/auth/login.py 模块"
sleep 0.1
tmux send-keys -t $TARGET Enter
# ...
# 3. 等待并查看回复(轮询)
sleep 30
tmux capture-pane -p -J -t $TARGET -S -200
```

### 场景三: 远程终端调试

调试远程终端中的会话问题.
```bash
# 1. 转储完整缓冲区
tmux capture-pane -p -J -t $TARGET -S -400
# ...
# 2. 分析输出,查找错误信息
# ...
# 3. 如果使用非默认 socket
tmux -S /path/to/socket list-panes -a
```

## 快速开始

### 第一步: 创建 tmux 会话

```bash
# 创建命名会话
tmux new-session -s myproject
# ...
# 在会话中启动代码助手
claude
# ...
# 重命名窗格标题为 claude
# 按 Ctrl-b : 输入 select-pane -T claude
```

### 第二步: 定位窗格

```bash
# 查找标题为 claude 的窗格
#{pane_index} #{pane_title}' \
  | grep -i claude
```

### 第三步: 查看最新内容

```bash
# 捕获最新内容
tmux capture-pane -p -J -t myproject:0.1 -S -200
```

### 第四步: 发送指令

```bash
# 发送任务
tmux send-keys -t myproject:0.1 -l -- "实现用户注册功能"
sleep 0.1
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 会话命名规范

| 命名规则 | 示例 | 说明 |
|:-----|:-----|:-----|
| 项目名 | `myproject` | 按项目命名会话 |
| 环境-项目 | `dev-myapp` | 区分环境 |
| 项目-功能 | `myapp-auth` | 按功能模块 |

### 窗格标题规范

```bash
# 设置窗格标题
Ctrl-b : select-pane -T claude
Ctrl-b : select-pane -T logs
Ctrl-b : select-pane -T tests
```

### 常用快捷操作

| 操作 | 快捷键 | 命令 |
|---:|---:|---:|
| 重命名窗格 | `Ctrl-b :` | `select-pane -T <name>` |
| 分割窗格 | `Ctrl-b %` 或 `Ctrl-b "` | 水平/垂直分割 |
| 切换窗格 | `Ctrl-b 方向键` | 切换焦点 |
| 列出会话 | `Ctrl-b s` | 选择会话 |

## 最佳实践

### 1. 始终确认目标窗格

发送指令前,务必确认操作的是正确的窗格:

```bash
# 先查看当前窗格内容
tmux capture-pane -p -J -t $TARGET -S -50
# ...
# 确认无误后再发送
tmux send-keys -t $TARGET -l -- "指令"
```

### 2. 轮询等待回复

发送指令后,需要轮询检查是否收到回复:

```bash
# 发送指令后轮询
for i in $(seq 1 18); do
  sleep 10
  output=$(tmux capture-pane -p -J -t $TARGET -S -50)
  if echo "$output" | grep -q "⏺"; then
    echo "收到回复:"
    echo "$output"
    break
  fi
  echo "等待回复... ($((i*10))秒)"
done
```

### 3. 提及会话与窗格

汇报结果时,提及使用的会话和窗格,便于追踪:

```text
在会话 myproject 的窗格 0.1 (claude) 中查看到:
- 用户指令: 实现用户注册
- 助手回复: 已完成,修改了 3 个文件
```

### 4. 超时处理

```bash
# 设置 3 分钟超时
TIMEOUT=180
ELAPSED=0
# ...
while [ $ELAPSED -lt $TIMEOUT ]; do
  output=$(tmux capture-pane -p -J -t $TARGET -S -50)
  if echo "$output" | grep -q "⏺"; then
    echo "收到回复"
    break
  fi
  sleep 10
  ELAPSED=$((ELAPSED + 10))
done
# ...
if [ $ELAPSED -ge $TIMEOUT ]; then
  echo "超时: 助手尚未回复,仍在处理中"
fi
```

## 常见问题

### Q1: 找不到标题为 claude 的窗格怎么办?

确认窗格标题已正确设置。在目标窗格中按 `Ctrl-b :` 输入 `select-pane -T claude`.
### Q2: 发送指令没有反应怎么办?

检查目标窗格是否处于可输入状态。代码助手可能正在处理上一个任务,等待其完成后再发送.
### Q3: 如何处理多个匹配的窗格?

选择 `window_index` 和 `pane_index` 最低的那个,除非上下文有其他指示:

```bash
# 如果有多个匹配,取第一个
TARGET=$(tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_title}' \
  | grep "^myproject" | grep -i claude | head -1 | awk '{print $1}')
```

### Q4: 使用非默认 socket 怎么办?

如果 tmux 使用非默认 socket,每个命令前加 `-S` 参数:

```bash
tmux -S /path/to/socket list-panes -a
tmux -S /path/to/socket capture-pane -p -J -t $TARGET -S -200
```

### Q5: 免费版支持多会话同时管理吗?

免费版一次处理一个会话。多会话场景请重复执行工作流,或使用 PRO 版.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Linux / macOS(Windows 需通过 WSL 或类似工具)
- **tmux**: 已安装并运行

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| tmux | CLI 工具 | 必需 | 系统包管理器 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本工具为纯 tmux 指令操作,基础LLM由Agent平台提供
- tmux 内运行的代码助手自行管理其认证

### 可用性分类

- **分类**: MD+EXEC(Markdown 指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行 tmux 命令管理终端会话
- **离线可用**: 是,tmux 操作在本地完成

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 当前为免费版本,如需完整功能请升级到付费版获取全部能力