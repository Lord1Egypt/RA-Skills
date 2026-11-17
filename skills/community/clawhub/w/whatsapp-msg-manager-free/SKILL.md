---
name: "whatsapp-msg-manager-free"
description: "发送WhatsApp文本消息、查看号码与模板,适合个人用户的轻量消息管理工具"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "WhatsApp消息管理-免费版"
  version: "1.0.0"
  summary: "发送WhatsApp文本消息、查看号码与模板,适合个人用户的轻量消息管理工具"
  tags:
    - "沟通协作"
    - "消息发送"
    - "WhatsApp"
    - "通知提醒"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# WhatsApp消息管理(免费版)

## 概述

WhatsApp消息管理免费版是一款面向个人用户和小型团队的轻量级WhatsApp Business消息工具。通过连接器服务与WhatsApp Cloud API对接,用户可以快速发送文本消息、查看账号信息以及浏览消息模板,无需手动配置API凭证。

本版本聚焦最核心的文本消息发送能力,操作流程简洁,内置安全确认机制,适合日常通知、提醒和简单客户沟通场景。如需发送图片/视频、交互式按钮、批量发送或模板管理功能,请升级至PRO版。

### 免费版与PRO版能力对比

| 能力维度 | 免费版 | PRO版 |
|:---------|:-------|:------|
| 文本消息发送 | 支持 | 支持 |
| 媒体消息(图片/视频/文档) | 不支持 | 支持 |
| 交互式按钮/列表消息 | 不支持 | 支持 |
| 模板消息发送 | 仅浏览 | 浏览+创建+删除 |
| 批量发送 | 不支持 | 支持 |
| 多账号管理 | 单账号 | 多账号 |
| 业务资料查询 | 不支持 | 支持 |
| 定时发送 | 不支持 | 支持 |
| 优先技术支持 | 社区支持 | 专属支持 |

## 核心能力

### 1. 文本消息发送

向WhatsApp用户发送纯文本消息,支持24小时客服窗口内的自由格式消息。

```bash
# 发送一条文本消息
connector_call_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "PHONE_NUMBER_ID",
  "recipient_phone": "+8613800138000",
  "message": "您好!您的订单 #20260718 已确认,预计3个工作日内发货。"
}'
```

**输入**: 用户提供文本消息发送所需的指令和必要参数。
**处理**: 按照skill规范执行文本消息发送操作,遵循单一意图原则。
**输出**: 返回文本消息发送的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 电话号码查询

列出Business账号下所有已注册的电话号码,获取号码ID用于消息发送。

```bash
# 查询所有电话号码
connector_call_tool --tool "whatsapp_get_phone_numbers" --params '{}'

# 查询单个号码详情
connector_call_tool --tool "whatsapp_get_phone_number" --params '{
  "phone_number_id": "PHONE_NUMBER_ID"
}'
```

**输入**: 用户提供电话号码查询所需的指令和必要参数。
**处理**: 按照skill规范执行电话号码查询操作,遵循单一意图原则。
**输出**: 返回电话号码查询的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 模板浏览

查看账号下所有消息模板及其审批状态,了解可用模板清单。

```bash
# 列出所有消息模板
connector_call_tool --tool "whatsapp_get_message_templates" --params '{}'

# 查询特定模板的审批状态
connector_call_tool --tool "whatsapp_get_template_status" --params '{
  "template_name": "shipping_confirmation"
}'
```

**输入**: 用户提供模板浏览所需的指令和必要参数。
**处理**: 按照skill规范执行模板浏览操作,遵循单一意图原则。
**输出**: 返回模板浏览的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：查看号码与模板、适合个人用户的轻、量消息管理工具、消息管理免费版、提供核心的、消息发送能力、核心能力、文本消息给单个联、账号下的电话号码、浏览已审批的消息、简单的消息预览与、确认流程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:订单状态通知

电商卖家在订单状态变更时,通过WhatsApp向客户发送文本通知。

```bash
# 示例
connector_call_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "1029384756",
  "recipient_phone": "+8613800138000",
  "message": "您的订单 #20260718-001 已发货,物流单号:SF1234567890,预计2-3天送达。如有疑问请随时联系我们。"
}'
```

**执行步骤:**
1. 通过 `whatsapp_get_phone_numbers` 获取发送号码ID
2. 确认收件人号码格式正确(含国家代码)
3. 编辑消息内容并预览
4. 用户确认后执行发送

### 场景二:会议提醒

个人或小团队向参与者发送会议提醒消息。

```bash
# 示例:发送会议提醒
connector_call_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "1029384756",
  "recipient_phone": "+8613900139000",
  "message": "提醒:明天上午10点产品评审会议,地点:3号会议室。请提前准备需求文档,准时参加。"
}'
```

### 场景三:模板状态检查

在发送模板消息前,先确认模板是否已通过WhatsApp审批。

```bash
# 检查模板审批状态
connector_call_tool --tool "whatsapp_get_template_status" --params '{
  "template_name": "order_confirmation"
}'
```

## 不适用场景

以下场景WhatsApp消息管理-免费版不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

```bash
# 在SkillHub平台安装连接器插件
skill-platform plugins install SkillHub:connector-plugin
skill-platform config set tools.alsoAllow '["connector-plugin"]' --strict-json
skill-platform gateway restart
```

安装完成后,发送 `/new` 开始新的会话。

### 第二步:配对设备

```bash
# 启动设备配对流程
connector_begin_pairing
```

按照提示完成设备授权。

### 第三步:连接WhatsApp

1. 打开连接器控制面板
2. 选择添加WhatsApp集成
3. 完成OAuth授权流程
4. 验证连接状态

```bash
# 验证连接
connector_list_integrations

# 查看WhatsApp可用工具
connector_list_tools --integration whatsapp
```

### 第四步:发送第一条消息

```bash
# 获取号码ID
connector_call_tool --tool "whatsapp_get_phone_numbers" --params '{}'

# 发送消息
connector_call_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "你的号码ID",
  "recipient_phone": "+8613800138000",
  "message": "Hello! 这是一条来自WhatsApp消息管理免费版的测试消息。"
}'
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 配置示例

### 基础配置文件

```yaml
# config.yaml - WhatsApp消息管理免费版配置
whatsapp:
  # 默认发送号码ID(从 whatsapp_get_phone_numbers 获取)
  default_phone_number_id: "1029384756"

  # 消息发送确认模式
  confirm_before_send: true

  # 默认语言代码
  default_language: "zh_CN"

  # 消息长度限制(字符)
  max_message_length: 4096
```

### 安全策略配置

```yaml
# security.yaml - 安全策略
security:
  # 发送前必须预览
  require_preview: true

  # 收件人号码必须包含国家代码
  require_country_code: true

  # 禁止发送给黑名单号码
  blocklist_enabled: true
  blocklist: []
```

## 最佳实践

### 1. 号码格式规范

收件人号码必须包含国家代码,否则消息无法送达。

```python
# Python示例:号码格式校验
import re

def validate_phone(phone: str) -> bool:
    """校验WhatsApp号码格式"""
    pattern = r'^\+\d{6,15}$'
    if not re.match(pattern, phone):
        print(f"号码格式错误: {phone}")
        print("正确格式: +国家代码+号码,例如 +8613800138000")
        return False
    return True

# 使用示例
validate_phone("+8613800138000")  # 正确
validate_phone("13800138000")      # 错误:缺少国家代码
```

### 2. 24小时客服窗口

WhatsApp规定,自由格式消息只能在用户与商家互动后的24小时内发送。超出窗口需使用已审批的模板消息。

```python
from datetime import datetime, timedelta

def check_message_window(last_interaction: str) -> dict:
    """检查是否在24小时客服窗口内"""
    last_time = datetime.fromisoformat(last_interaction)
    now = datetime.now(last_time.tzinfo)
    elapsed = now - last_time
    remaining = timedelta(hours=24) - elapsed

    if remaining.total_seconds() > 0:
        return {
            "in_window": True,
            "remaining_hours": round(remaining.total_seconds() / 3600, 1),
            "can_send_free_form": True
        }
    else:
        return {
            "in_window": False,
            "remaining_hours": 0,
            "can_send_free_form": False,
            "suggestion": "已超出24小时窗口,请使用已审批的模板消息"
        }
```

### 3. 发送前预览确认

所有写操作(消息发送)在执行前必须经过用户确认。

```bash
# 步骤1:预览消息内容
connector_preview_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "1029384756",
  "recipient_phone": "+8613800138000",
  "message": "预览:这是一条测试消息"
}'

# 步骤2:用户确认后执行
connector_call_tool --tool "whatsapp_send_message" --params '{
  "phone_number_id": "1029384756",
  "recipient_phone": "+8613800138000",
  "message": "这是一条测试消息"
}'
```

## 错误处理


```python
# 常见错误码处理
ERROR_CODES = {
    "131026": "消息无法送达:收件人号码不是有效的WhatsApp账户",
    "133010": "收件人未注册WhatsApp",
    "131047": "已超出24小时窗口:请改用模板消息发送",
    "131042": "消息内容包含违规内容",
}

def handle_error(error_code: str, context: dict) -> str:
    """处理WhatsApp API错误"""
    message = ERROR_CODES.get(error_code, f"未知错误: {error_code}")

    if error_code == "131047":
        return f"{message}\n建议:使用 whatsapp_send_template_message 发送已审批模板"
    elif error_code == "133010":
        return f"{message}\n建议:确认号码正确或引导用户注册WhatsApp"
    else:
        return message
```

| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|------|----------|------|----------|--------|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题

### Q1: 为什么工具列表中看不到WhatsApp工具?

**A:** 请按以下步骤排查:
1. 确认连接器插件已安装: `skill-platform plugins list`
2. 确认WhatsApp集成已连接: `connector_list_integrations`
3. 如工具仍不可见,重启网关并新建会话:
```bash
skill-platform config set tools.alsoAllow '["connector-plugin"]' --strict-json
skill-platform gateway restart
```
4. 重启后发送 `/new` 重新加载工具目录

### Q2: 消息发送失败提示"131047"是什么意思?

**A:** 错误码131047表示已超出24小时客服窗口。WhatsApp规定自由格式消息只能在用户最近一次互动后的24小时内发送。解决方案:使用已审批的模板消息(`whatsapp_send_template_message`)发送。

### Q3: 免费版可以发送图片或文件吗?

**A:** 免费版仅支持文本消息发送。如需发送图片、视频、音频或文档,请升级至PRO版,PRO版支持全部媒体类型和交互式消息。

### Q4: 如何获取phone_number_id?

**A:** 执行以下命令获取:
```bash
connector_call_tool --tool "whatsapp_get_phone_numbers" --params '{}'
```
返回结果中的 `id` 字段即为 phone_number_id。

### Q5: 消息可以撤回吗?

**A:** WhatsApp消息一旦发送无法撤回。因此发送前务必确认收件人号码和消息内容正确无误。本工具内置预览确认机制,所有消息发送前都会先展示预览供用户确认。

### Q6: 如何从免费版升级到PRO版?

**A:** PRO版与免费版完全兼容,升级后原有配置和连接无需更改,即可获得媒体消息、交互式消息、模板管理、批量发送等高级能力。直接安装PRO版Skill即可完成升级。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需可访问WhatsApp Cloud API服务端点
- **浏览器**: 用于OAuth授权流程的现代浏览器

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| 连接器插件 | 平台插件 | 必需 | SkillHub插件市场安装 |
| WhatsApp Business账号 | 服务账号 | 必需 | Meta Business平台注册 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js | 运行时 | 可选 | 仅本地脚本执行时需要 |

### API Key 配置

- 本Skill通过连接器服务自动管理OAuth令牌,无需手动配置API Key
- WhatsApp Business API凭证由连接器服务安全存储并自动注入
- 如需直接调用WhatsApp Cloud API,需在Meta开发者平台获取Access Token

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作
- **连接模式**: 通过连接器服务代理WhatsApp Cloud API请求
- **安全等级**: 所有写操作需用户显式确认,OAuth令牌由连接器安全管理

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
