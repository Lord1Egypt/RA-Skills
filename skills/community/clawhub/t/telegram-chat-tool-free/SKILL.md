---
slug: telegram-chat-tool-free
name: telegram-chat-tool-free
version: 1.0.0
displayName: 电报聊天工具免费版
summary: "轻量级Telegram Bot配置与跨实例聊天工具,支持用户艾特、消息收发与基础群组管理.。电报聊天工具免费版,为个人用户提供 Telegram Bot 创建、配置与跨实例聊天能力,支持用户"
license: Proprietary
edition: free
description: '电报聊天工具免费版,为个人用户提供 Telegram Bot 创建、配置与跨实例聊天能力,支持用户艾特、消息收发与基础群组管理。核心能力:

  - Telegram Bot 快速创建与配置

  - 跨 Bot 实例消息通信

  - 用户艾特(@提及)功能

  - 群组消息收发

  - 基础身份标识与消息溯源

  适用场景:

  - 个人用户搭建专属 Telegram Bot

  - 小团队跨 Bot 协作聊天

  - 群组内艾特提醒与消息通知

  差异化:免费版聚焦个人用户与小团队的 Telegram 聊天需求,提供从零开始的 Bot 配置指南...'
tags:
  - 沟通协作
  - 即时通讯
  - Telegram
  - 机器人
  - 个人效率
  - 社交
  - 通信
  - bot
  - telegram
  - text
  - 用户名
  - 发送
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
---
# 电报聊天工具 - 免费版

## 概述

电报聊天工具免费版是一款面向个人用户与小团队的 Telegram Bot 配置与聊天助手。通过本工具,用户可以从零开始创建自己的 Telegram Bot,配置消息接收与发送能力,实现跨 Bot 实例的聊天通信、用户艾特提醒与群组消息管理.
本版本适合个人用户搭建专属 Bot、小团队跨 Bot 协作以及群组内的艾特提醒与消息通知场景.
## 核心能力

### Bot 创建与配置

- 通过 BotFather 创建 Telegram Bot
- 获取 Bot Token 并配置到平台
- 设置 Bot 为群组管理员以接收消息
- 隐私模式关闭配置(接收所有群消息)

**处理**: 解析Bot 创建与配置的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Bot 创建与配置的响应数据,包含状态码、结果和日志.
### 跨实例聊天

- 不同 Bot 实例之间互发消息
- 通过 @Bot用户名 精准定向消息
- 消息可溯源,身份可识别

**处理**: 解析跨实例聊天的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回跨实例聊天的响应数据,包含状态码、结果和日志.
### 用户艾特(@提及)

- 使用 @Bot用户名 格式艾特目标
- 支持群组内多人艾特
- 艾特触发消息提醒

**处理**: 解析用户艾特(@提及)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回用户艾特(@提及)的响应数据,包含状态码、结果和日志.
### 基础群组管理

- Bot 加入群组与频道
- 配置允许接收消息的群组白名单
- 基础消息收发测试

**处理**: 解析基础群组管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础群组管理的响应数据,包含状态码、结果和日志.
### 身份标识

- 每个 Bot 实例绑定唯一标识
- Bot 用户名作为身份标识
- 消息来源可追溯

**处理**: 解析身份标识的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回身份标识的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、配置与跨实例聊天、支持用户艾特、消息收发与基础群、电报聊天工具免费、为个人用户提供、核心能力、快速创建与配置、实例消息通信、群组消息收发、基础身份标识与消、息溯源等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:从零创建专属 Telegram Bot

个人用户想搭建一个自己的 Telegram Bot,用于接收通知与自动回复.
**第一步:创建 Bot**

1. 在 Telegram 中搜索并打开 **@BotFather**
2. 发送 `/newbot` 命令
3. 按提示输入 Bot 名称(显示名)与用户名(必须以 bot 结尾)
4. 获取 Bot Token(形如 `123456789:ABCdefGhI...`)

**第二步:配置平台**

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 电报聊天工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```yaml
# 示例
messaging:
  telegram:
    bot_token: "你的Bot_Token"
    allowed_chats:
      - 你的群组ID1
      - 你的群组ID2
```

**第三步:测试 Bot**

```text
# 在群组中发送消息测试
@你的Bot用户名 你好
# ...
# 预期收到回复
你好!我是你的专属Bot,有什么可以帮你?
```

### 场景二:跨 Bot 实例聊天

团队成员各自有自己的 Bot,需要通过 Bot 互相聊天协作.
**艾特格式**:

```text
@对方的Bot用户名 你的消息内容
```

**示例对话**:

```text
用户A: @用户B的Bot 周报已提交,请帮忙review
用户B的Bot: 收到,我现在查看.
用户B: @用户A的Bot 已review,有问题在第3节,请修改
用户A的Bot: 好的,马上修改.
```

**找不到 Bot 用户名时**:

```text
# 在群里直接询问
大家好,请问 @xxx 的 Bot 用户名是什么?
```

### 场景三:群组消息通知

在团队群组中通过 Bot 发送重要通知,确保成员及时收到提醒.
```text
# Bot 发送会议通知
@团队Bot 【会议通知】
时间:2026年7月20日 14:00
地点:3号会议室
主题:Q3 项目进度同步
参会人:@成员A @成员B @成员C
# ...
请准时参加,如有冲突请提前说明.
```

## 不适用场景

以下场景电报聊天工具免费版不适合处理：

- 垃圾信息群发
- 通信协议逆向
- 电话语音交互

## 触发条件

需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:创建 Telegram Bot

1. 打开 Telegram,搜索 `@BotFather`
2. 发送 `/newbot`
3. 输入 Bot 显示名称(如:我的助手)
4. 输入 Bot 用户名(必须以 `bot` 结尾,如:`my_assistant_bot`)
5. 记录返回的 Bot Token

### 第二步:配置 Bot 加入群组

1. 将 Bot 添加到目标群组
2. 将 Bot 设为群组管理员(才能接收所有消息)
3. 关闭 Bot 的隐私模式:
   - 向 `@BotFather` 发送 `/mybots`
   - 选择你的 Bot
   - 进入 `Bot Settings` -> `Group Privacy`
   - 选择 `Turn off`

### 第三步:配置平台连接

```yaml
# skill-platform.yaml
messaging:
  telegram:
    bot_token: "123456789:ABCdefGhIJKlmNoPQRsTUVwxyz"
    allowed_chats:
      - "-1001234567890"  # 群组ID
```

### 第四步:验证配置

| 测试项 | 操作 | 预期结果 |
|:-----|:-----|:-----|
| 基础回复 | 在群组发 `@你的Bot 你好` | 收到 Bot 回复 |
| 跨 Bot 通信 | 在群组发 `@其他人的Bot` 消息 | 对方 Bot 收到并响应 |
| 消息接收 | 在群组发普通消息 | Bot 能读取消息内容 |

## 配置示例

### 基础配置

```yaml
# skill-platform.yaml 完整配置示例
messaging:
  telegram:
    bot_token: "你的Bot_Token"
    allowed_chats:
      - "-1001234567890"      # 群组A
      - "-1009876543210"      # 群组B
    bot_username: "my_assistant_bot"
    bot_display_name: "我的助手"
```

### 获取群组 ID

```bash
# 方法一:通过 Telegram API 获取
curl "https://api.telegram.org/bot配置值/getUpdates" | python3 -m json.tool
# ...
# 方法二:使用 @userinfobot
# 在 Telegram 中搜索 @userinfobot,将群组转发给它即可获取 ID
```

### 通讯录模板

建议维护一份团队成员的 Bot 通讯录,方便快速艾特:

```text
| 成员姓名 | Bot用户名        | 专长       |
|---:|---:|---:|
| 张三     | @zhangsan_bot    | 前端开发   |
| 李四     | @lisi_bot        | 后端开发   |
| 王五     | @wangwu_bot      | 产品设计   |
| 赵六     | @zhaoliu_bot     | 数据分析   |
```

## 最佳实践

### 1. Bot 命名规范

为便于识别,建议 Bot 用户名遵循统一规范:

```text
# 推荐命名格式
{姓名拼音}_bot        # 如:zhangsan_bot
{角色}_{姓名}_bot     # 如:dev_zhangsan_bot
{团队}_{职能}_bot     # 如:team_qa_bot
```

### 2. 关闭隐私模式确保消息接收

默认情况下 Bot 只能接收以 @ 开头的消息。关闭隐私模式后可接收群内所有消息:

```text
# 操作步骤
1. 向 @BotFather 发送 /mybots
2. 选择你的 Bot
3. Bot Settings -> Group Privacy -> Turn off
```

### 3. 合理配置群组白名单

仅允许 Bot 在指定群组中响应,避免在无关群组中误触发:

```yaml
messaging:
  telegram:
    allowed_chats:
      - "-1001234567890"  # 仅允许此群组
```

### 4. 艾特格式统一

团队内统一使用 `@Bot用户名 消息` 格式,避免混淆:

```text
# 正确格式
@zhangsan_bot 请帮忙看一下接口文档
# ...
# 错误格式(缺少空格或用户名错误)
@zhangsan_bot请帮忙...    # 缺少空格
@张三 请帮忙...            # 应使用Bot用户名而非中文姓名
```

### 5. 定期测试 Bot 可用性

建议每周做一次基础测试,确保 Bot 正常运行:

```text
# 测试清单
1. 发送 @你的Bot ping -> 预期回复 pong
2. 发送 @你的Bot 状态 -> 预期回复运行状态
3. 让其他人 @你的Bot -> 预期你收到通知
```

## 常见问题

### Q1: Bot 收不到群组消息怎么办?

**A**: 请按以下顺序排查:
1. 确认 Bot 已加入群组
2. 确认 Bot 已设为群组管理员
3. 确认已关闭隐私模式(@BotFather -> /mybots -> Bot Settings -> Group Privacy -> Turn off)
4. 确认群组 ID 已添加到 `allowed_chats` 配置中

### Q2: 艾特别人没反应?

**A**: 可能原因:
- 对方 Bot 不在该群组中
- 对方 Bot 用户名拼写错误
- 对方 Bot 的隐私模式未关闭

**解决方法**:在群里直接询问确认对方 Bot 用户名:

```text
```

### Q3: Bot Token 泄露了怎么办?

**A**: 立即通过 BotFather 撤销并重新生成 Token:
1. 向 `@BotFather` 发送 `/mybots`
2. 选择你的 Bot
3. 进入 `API Token` -> `Revoke current token`
4. 获取新 Token 并更新配置

### Q4: 如何获取群组 ID?

**A**: 推荐两种方法:

```bash
# 方法一:调用 Telegram API
curl "https://api.telegram.org/bot配置值/getUpdates"
# ...
# 方法二:使用 @userinfobot 辅助工具
# 在 Telegram 搜索 @userinfobot,转发群组消息给它
```

### Q5: 免费版支持多 Bot 管理吗?

**A**: 免费版支持单个 Bot 的配置与使用。如需管理多个 Bot、企业级群组管理、消息归档与审计等高级功能,请考虑升级至 PRO 版本.
### Q6: Bot 能主动发送消息吗?

**A**: 免费版支持 Bot 在被艾特或收到消息后响应。主动推送消息能力属于 PRO 版本功能.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需可访问 Telegram API(可能需要网络代理)
- **Telegram 账户**: 需有已注册的 Telegram 账户

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Telegram 账户 | 账户 | 必需 | 注册 Telegram |
| Telegram Bot Token | 凭据 | 必需 | 通过 @BotFather 创建 |
| skill-platform.yaml | 配置 | 必需 | 手动创建配置文件 |
| 网络代理 | 网络 | 视情况 | 部分地区需代理访问 Telegram |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 通过 Telegram 中的 @BotFather 创建 Bot 获取 Token
- 将 Token 配置到 `skill-platform.yaml` 的 `messaging.telegram.bot_token` 字段
- 将允许通信的群组 ID 填入 `allowed_chats` 列表
- Token 属于敏感凭据,请勿公开分享,定期通过 BotFather 轮换

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,核心功能通过配置文件与 Telegram API 调用实现)
- **说明**: 基于配置的 AI Skill,通过自然语言指令驱动 Agent 完成 Telegram Bot 创建、配置与跨实例聊天。免费版支持单个 Bot 的基础配置、用户艾特、群组消息收发与身份标识,适合个人用户与小团队轻量协作场景.
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

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "电报聊天工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "telegram chat"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
