---
name: push2today
version: 1.0.0
trigger: "用户请求将任务执行结果推送到负一屏、推送手机、发送到手机负一屏"
description: 将任务执行结果推送到负一屏卡片显示，支持普通推送和定时任务推送
emoji: "📱"
metadata:
  {
    "openclaw":
      {
        "author": "your-name",
        "tags": ["push", "notification", "today", "负一屏"],
        "homepage": "https://github.com/your-name/push2today",
        "requires": { "bins": ["node"] },
        "env": {
          "AS_TODAY_AUTH_CODE": {
            "description": "API 认证令牌（必填）",
            "required": true
          },
          "AS_TODAY_API_URL": {
            "description": "API 地址（可选，默认内置）",
            "required": false
          }
        }
      },
  }
---

# Push2Today

将任务执行结果推送到负一屏显示。

## 工具说明

此 Skill 通过 `tools.json` 定义 `push2today` 工具，执行 `scripts/cli.js` 命令实现推送功能。

## 触发条件

以下任一触发短语都会激活此 skill：

- "推送到负一屏"
- "帮我推送到负一屏"
- "将结果推送到负一屏"
- "推送到手机"
- "帮我推送到手机"
- "帮我推送到手机负一屏"
- "发送到手机负一屏"
- "手机负一屏"
- "push to Today"
- "推送到 Today"

## 环境配置

使用此 skill 前，必须配置环境变量：

```bash
openclaw config set skills.entries.push2today.env.AS_TODAY_AUTH_CODE "your_actual_token_here"
```

**重要**：`AS_TODAY_AUTH_CODE` 是必填的环境变量，用于接口鉴权。如果未配置，skill 调用将失败。

## 工具参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| msgId | string | **是** | 消息 ID，从当前会话上下文自动获取 |
| summary | string | **是** | 任务摘要（64 字符以内） |
| result | string | **是** | 执行结果：`"任务执行成功"` 或 `"任务执行失败"` |
| content | string | **是** | 详细内容（长度限制 30717 字符） |
| scheduleTaskId | string | 否 | 定时任务 ID，来自定时任务时填写 |
| scheduleTaskName | string | 否 | 定时任务名称，来自定时任务时填写 |
| source | string | 否 | claw 类型，固定填写 `"openclaw"` |

## result 取值规则

- 任务执行成功或有有效结果 → `"任务执行成功"`
- 任务执行失败或遇到错误 → `"任务执行失败"`

## summary 格式要求

- 长度：64 字符以内
- 内容：简洁描述任务核心内容
- 示例：
  - "代码审查完成，发现 3 个问题"
  - "数据分析完成"
  - "定时任务执行成功"

## 使用示例

### 示例 1：普通推送

用户说"帮我推送到负一屏"时，执行：

```bash
node scripts/cli.js push2today --msgId "msg-123456" --summary "代码审查完成" --result "任务执行成功" --content "已完成代码审查，发现 3 个潜在问题需要修复..."
```

### 示例 2：推送到手机

用户说"帮我推送到手机"或"帮我推送到手机负一屏"时，执行：

```bash
node scripts/cli.js push2today --msgId "msg-789012" --summary "数据分析完成" --result "任务执行成功" --content "已完成销售数据分析，本季度增长 15%，环比增长 8%..."
```

### 示例 3：定时任务自动推送

定时任务执行完成后自动执行：

```bash
node scripts/cli.js push2today --msgId "msg-cron-001" --summary "晨间摘要完成" --result "任务执行成功" --content "已完成今日晨间摘要：天气晴朗，气温 20°C，今日有 3 个会议..." --scheduleTaskId "morning-brief" --scheduleTaskName "晨间摘要" --source "openclaw"
```

## 定时任务强制推送规则

所有定时任务执行完成后，**必须立即执行** push2today 命令推送结果。

这是强制操作，不需要：
- ❌ 等待用户确认
- ❌ 询问是否需要推送
- ❌ 添加额外说明

直接执行命令：
```bash
node scripts/cli.js push2today --msgId "从会话上下文获取" --summary "任务摘要" --result "任务执行成功" --content "详细的任务执行结果..." --scheduleTaskId "定时任务ID" --scheduleTaskName "定时任务名称" --source "openclaw"
```

## 约束

- content 参数长度不能超过 30717 字符
- summary 长度不能超过 64 字符
- 未配置 `AS_TODAY_AUTH_CODE` 环境变量时，返回明确的错误信息
- 定时任务必须填写 `scheduleTaskId`、`scheduleTaskName` 和 `source`
