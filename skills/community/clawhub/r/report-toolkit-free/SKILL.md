---
slug: report-toolkit-free
name: report-toolkit-free
version: 1.0.1
displayName: 报告工具包-免费版
summary: "自定义定期报告生成工具"
license: "MIT"
edition: free
description: "自定义定期报告产出工具免费版,面向个人开发者与小型项目。核心能力: - 自定义报告配置与数据源 - 定时调度(每日/每周/每月) - 多格式输出(文本/Markdown/HTML) - 多渠道交付(聊天/文件/邮件) - 环境变量安全管控凭证 - 历史报告归档 适用场景: - 个人项目数据周报 - 收入/支出定期汇总 - GitHub 活动统计报告 差异化:免费版包含基础报告产出能力"
tags:
  - 报告生成
  - 定时调度
  - 数据汇总
  - 工具
  - 效率
  - report
  - delivery
  - file
  - 返回结构
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free
---
# 报告工具包 - 免费版

## 概述

报告工具包免费版是面向个人的自定义定期报告生成工具。用户定义数据源和报告格式,工具负责按计划生成报告并通过指定渠道交付。采用「用户定义数据,工具负责调度与格式化」的模型. 关键词: report toolkit
## 核心能力

### 1. 自定义数据源

支持 API 数据、数据库查询、文件读取等多种数据源,用户通过环境变量提供凭证.

**处理**: 解析自定义数据源的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自定义数据源的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 定时调度

支持每日、每周、每月定时生成报告,使用 Cron 表达式配置.

**处理**: 解析定时调度的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回定时调度的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 多格式输出

支持纯文本、Markdown、HTML 三种输出格式.

**处理**: 解析多格式输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多格式输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 多渠道交付

支持聊天回复、本地文件保存、邮件发送三种交付渠道.

**处理**: 解析多渠道交付的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多渠道交付的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 凭证安全管理

API Key 等凭证通过环境变量引用,不存储在配置文件中.

**处理**: 解析凭证安全管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回凭证安全管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 6. 历史归档

生成的报告按名称归档,便于历史查阅.

**处理**: 解析历史归档的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回历史归档的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：自定义定期报告生、成工具、支持多数据源、定时调度与多渠道、适合个人使用、成工具免费版、面向个人开发者与、小型项目、核心能力、自定义报告配置与、环境变量安全管理、历史报告归档等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:每周收入报告

每周一早上 9 点生成收入汇总报告.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 报告工具包-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```yaml
# ./report/weekly-revenue/config.md
name: weekly-revenue
schedule: "0 9 * * 1"  # 每周一 9 点
sources:
  - type: api
    url: "https://api.stripe.com/v1/balance"
    env: STRIPE_API_KEY  # 环境变量引用
format: markdown
delivery: file
```

```bash
# 设置环境变量
export STRIPE_API_KEY=${STRIPE_API_KEY:?请设置环境变量}
# ...
# 手动触发报告
./report-cli run weekly-revenue
# ...
# 查看历史报告
ls ./report/weekly-revenue/generated/
# 2025-01-06.md  2025-01-13.md  2025-01-20.md
```

### 场景二:GitHub 活动统计

生成个人 GitHub 活动周报.
```yaml
# ./report/github-activity/config.md
name: github-activity
schedule: "0 10 * * 1"  # 每周一 10 点
sources:
  - type: api
users/{username}/events"
    env: GITHUB_TOKEN
    params:
      username: "your-username"
format: markdown
delivery: chat
```

### 场景三:服务器磁盘使用报告

每日生成磁盘使用情况报告.
```yaml
# ./report/disk-usage/config.md
name: disk-usage
schedule: "0 8 * * *"  # 每日 8 点
sources:
  - type: command
    command: "df -h"
format: text
delivery: file
```

## 不适用场景

以下场景报告工具包-免费版不适合处理：

- 数据库架构设计决策
- NoSQL选型
- 数据仓库ETL设计

## 触发条件

需要数据库操作、SQL查询、数据存储管理时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 初始化

```bash
# 创建报告目录
mkdir -p ./report
# ...
# 查看已有报告
cat ./report/memory.md 2>/dev/null || echo "暂无报告配置"
```

### 创建领先个报告

```bash
# 创建报告配置
mkdir -p ./report/my-report
cat > ./report/my-report/config.md << 'EOF'
name: my-report
schedule: "0 9 * * *"  # 每日 9 点
sources:
  - type: api
    env: MY_API_KEY
format: markdown
delivery: file
EOF
# ...
# 设置 API Key
export MY_API_KEY=${MY_API_KEY:?请设置环境变量}
# ...
# 手动运行
./report-cli run my-report
```

## 示例

### 报告配置格式

```yaml
name: report-name          # 报告名称(英文)
schedule: "0 9 * * *"      # Cron 表达式
sources:                    # 数据源列表
  - type: api              # API 数据源
    url: "https://..."
    env: API_KEY           # 凭证环境变量名
    params:                # 查询参数
      key: value
  - type: command          # 命令行数据源
    command: "df -h"
  - type: file             # 文件数据源
    path: "/path/to/data.json"
format: markdown           # 输出格式: text, markdown, html
delivery: file             # 交付方式: chat, file, email
```

### 调度频率

| 频率 | Cron 表达式 | 说明 |
|:-----|:-----|:-----|
| 每日 | `0 9 * * *` | 每天 9 点 |
| 每周 | `0 9 * * 1` | 每周一 9 点 |
| 每月 | `0 9 1 * *` | 每月 1 日 9 点 |
| 按需 | - | 手动触发 |

### 交付渠道

| 渠道 | 配置 | 说明 |
|---:|---:|---:|
| chat | `delivery: chat` | 在对话中返回报告 |
| file | `delivery: file` | 保存到 ./report/{name}/generated/ |
| email | `delivery: email` | 通过 SMTP 发送邮件 |

## 优秀实践

1. **凭证不落盘**:API Key 通过环境变量引用,配置文件中只写变量名
2. **合理调度**:非紧急报告避开高峰时段,减少 API 调用压力
3. **格式选择**:邮件用 HTML,聊天用 Markdown,存档用纯文本
4. **历史保留**:定期清理过期报告,保留最近 90 天
5. **错误通知**:报告生成失败时及时通知,避免长期静默失败

## 常见问题

### Q: 报告需要访问外部 API,如何安全提供凭证?

A: 通过环境变量提供。在配置中写 `env: API_KEY_NAME`,实际值通过 `export API_KEY_NAME="value"` 设置。配置文件只记录变量名,不存储实际值.
### Q: 如何查看已有的报告?

A: 运行 `./report-cli list` 查看所有报告配置。查看历史报告:`ls ./report/{name}/generated/`。手动触发:`./report-cli run {name}`.
### Q: 报告生成失败怎么办?

A: 检查以下几点:1) 环境变量是否正确设置;2) API 是否可达;3) 数据源 URL 是否正确;4) 查看错误日志 `./report/{name}/logs/`。修复后手动重新运行.
### Q: 可以暂停报告吗?

A: 可以。运行 `./report-cli pause {name}` 暂停调度。恢复运行 `./report-cli resume {name}`。暂停期间不会生成报告.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Shell 环境**: Bash 或兼容 Shell

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| curl | CLI工具 | API数据源必需 | 系统自带 |
| jq | CLI工具 | JSON处理推荐 | 包管理器安装 |
| sendmail/msmtp | 邮件工具 | 邮件交付必需 | 包管理器安装 |
| Python 3 | 运行时 | 推荐 | 官方网站下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 外部 API:通过环境变量配置(如 `STRIPE_API_KEY`、`GITHUB_TOKEN`)
- 邮件发送:配置 `SMTP_HOST`、`SMTP_USER`、`SMTP_PASSWORD`
- 本 Skill 本身无需 API Key

### 可用性分类

- **分类**: MD+执行方法(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行报告生成与交付
- **限制**: 免费版最多 5 个报告配置,不支持多租户与高级模板

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "报告工具包-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "reportkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
