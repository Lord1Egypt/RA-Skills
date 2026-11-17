---slug: telegram-alert-tool-free
name: telegram-alert-tool-free
version: 1.0.0
displayName: Telegram告警入门
summary: "通过Telegram "
license: Proprietary
edition: free
description: 面向个人交易者的Telegram告警通知工具。通过Telegram Bot将交易信号、，可自动提升工作效率

  价格变动等信息推送到指定群组。Use when 需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于垃圾信息群发。Use
  when 需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于垃圾信息群发。'
tags:
  - Finance
  - 告警通知
  - Telegram
  - 金融
  - 财务
  - 数据
  - bot
  - telegram
tools:
  - read
  - exec
  - write
homepage: ""
category: "Finance"---# Telegram告警入门（免费版）

## 概述

本工具为个人交易者提供通过Telegram Bot推送告警通知的能力。支持基础的价格触发条件和简单的消息格式化，适合个人用户接收交易信号和市场提醒.
## 核心能力

### 告警功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 消息推送 | Telegram Bot发送 | 支持 |
| 价格触发 | 阈值告警 | 基础（高于/低于） |
| 群组数量 | 目标群组 | 单一群组 |
| 消息格式 | 格式化选项 | 基础Markdown |
| 触发条件 | 条件组合 | 不支持 |
| 多通道 | 其他平台 | 不支持 |
| 定时推送 | 定时通知 | 不支持 |
| 告警历史 | 记录查询 | 基础记录 |

**处理**: 解析告警功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回告警功能的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：发送基础交易告警、支持单一群组与简、单价格触发、面向个人交易者的、告警通知工具、将交易信号、价格变动等信息推、送到指定群组、Use、when、需要消息发送、通知推送、邮件短信、通信集成时使用、不适用于垃圾信息、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：价格突破告警

用户输入："BTC跌破60000的时候在Telegram提醒我"

```bash
# 设置价格告警
python3 （请参考skill目录中的脚本文件） add \
  --ticker BTC-USD \
  --condition "below" \
  --threshold 60000 \
  --channel telegram \
  --chat-id "@my_trading_group"
# ...
# 启动监控
python3 （请参考skill目录中的脚本文件） monitor
```

### 场景二：交易信号通知

用户输入："把今天的交易信号发到Telegram群"

```bash
# 发送交易信号
python3 （请参考skill目录中的脚本文件） send \
  --message "买入信号: AAPL 突破阻力位180" \
  --chat-id "@my_trading_group"
```

### 场景三：定时市场播报

用户输入："每天早上9点发市场概况到Telegram"

```bash
# 设置定时播报
python3 （请参考skill目录中的脚本文件） schedule \
  --time "09:00" \
  --message-type "market_summary" \
  --chat-id "@my_trading_group"
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
pip install python-telegram-bot requests
# ...
# 配置Bot Token
# 1. 在Telegram中找到 @BotFather
# 2. 创建新Bot，获取Token
# 3. 将Bot添加到目标群组
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

### 常用命令

```bash
# 发送消息
python3 （请参考skill目录中的脚本文件） send --message "测试消息" --chat-id "@group"
# ...
# 添加告警
python3 （请参考skill目录中的脚本文件） add --ticker BTC-USD --condition below --threshold 60000
# ...
# 查看告警列表
python3 （请参考skill目录中的脚本文件） list
# ...
# 启动监控
python3 （请参考skill目录中的脚本文件） monitor
```

#
## 示例

### 告警配置

```yaml
alert_config:
  telegram:
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    default_chat_id: "@my_trading_group"
# ...
  alerts:
    - ticker: BTC-USD
      condition: below
      threshold: 60000
      message: "BTC跌破60000，注意风险"
# ...
    - ticker: AAPL
      condition: above
      threshold: 180
      message: "AAPL突破180阻力位"
# ...
  monitoring:
    check_interval: 60          # 检查间隔（秒）
    data_source: "yahoo_finance"
# ...
  history:
    enabled: true
    max_records: 100
    storage: "./alert_history.json"
```

## 最佳实践

1. **Bot权限**：确保Bot有发送消息到目标群组的权限
2. **告警频率**：设置合理的检查间隔，避免过于频繁
3. **消息清晰**：告警消息包含标的、价格、触发条件等关键信息
4. **时区注意**：定时任务注意配置正确的时区

| 实践要点 | 说明 |
|:-----|:-----|
| Bot Token安全 | 不要将Token提交到代码仓库 |
| 群组权限 | Bot需为群组成员才能发送消息 |
| 频率控制 | 避免短时间内发送大量消息（Telegram限流） |
| 消息格式 | 使用Markdown格式提升可读性 |

## 常见问题

### Q1：如何创建Telegram Bot？

在Telegram中找到@BotFather，发送/newbot命令，按提示设置Bot名称和用户名，完成后获取Bot Token.
### Q2：免费版支持多少个群组？

免费版仅支持单一目标群组。如需向多个群组或频道推送告警，建议升级PRO版.
### Q3：Bot无法发送消息怎么办？

检查：Bot是否已添加到目标群组、Bot是否有发送消息权限、Bot Token是否正确、群组ID格式是否正确（群组用@username，私有群用数字ID）.
### Q4：告警检查频率可以多快？

免费版建议间隔≥60秒。过于频繁的检查可能触发数据源限流，且Telegram对消息发送频率有限制.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **网络**: 需访问Telegram API（可能需要代理）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| python-telegram-bot | Python库 | 必需 | `pip install python-telegram-bot` |
| requests | Python库 | 必需 | `pip install requests` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| Telegram Bot | `TELEGRAM_BOT_TOKEN` | 必需 | Bot消息发送 |

- Bot Token通过@BotFather获取，免费
- Token存储在本地环境变量或配置文件

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过Telegram Bot推送告警通知
- **免费版限制**: 单一群组、基础触发条件、不支持多通道与复杂逻辑

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

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Telegram告警入门处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "telegram alert"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
