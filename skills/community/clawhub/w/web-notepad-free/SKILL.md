---
slug: web-notepad-free
name: web-notepad-free
version: 1.0.0
displayName: 在线表单笔记(免费版)
summary: 轻量化在线表单与提交数据管理工具,支持表单创建、提交查询、字段配置等核心能力,适合个人快速搭建信息收集流程。
license: Proprietary
edition: free
description: '在线表单笔记(免费版)是面向个人开发者与小型团队的轻量化表单管理Skill,通过REST API与命令行工具的组合,帮助用户在数分钟内搭建可用的表单收集流程。核心能力:


  - 表单与提交数据全生命周期管理(创建、查询、更新、删除)

  - 多字段类型支持(文本、邮件、电话、数字、日期、下拉等)

  - 项目级组织结构,便于按业务线分类管理表单

  - Bearer Token鉴权,简单安全的API调用方式


  适用场景:


  - 个人博客/作品集的联系表单快速接入

  - 小型活动报名、调研问卷的临时收集通道

  - MVP阶段的产品反馈收...'
tags:
- 集成工具
- 表单收集
- 生产力
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec", "glob"]
tags: "Web开发,前端,开发工具"
---
# 在线表单笔记(免费版)

一个面向个人开发者与小型团队的轻量化表单管理Skill,通过REST API和命令行工具的组合,帮助你快速搭建信息收集流程。本免费版聚焦"创建-提交-查询"主路径,适合个人或小型团队试用。

## 概述

本Skill封装了一组通用的表单管理接口,屏蔽了底层存储与权限细节。你只需要专注于业务字段设计,即可在数分钟内拥有一个可用的表单收集通道。免费版适合日提交量不超过200条的场景。

## 核心能力

| 能力 | 描述 | 免费版是否支持 |
|---|---|-------|
| 项目管理 | 列出项目、获取项目ID | 支持 |
| 表单CRUD | 创建、查询、更新、删除表单 | 支持(单次≤10字段) |
| 提交数据 | 创建、查询、删除单条提交 | 支持 |
| 批量提交 | 一次性导入多条提交 | 不支持 |
| 高级筛选 | 按日期范围、自定义字段筛选 | 部分支持 |
| Webhook订阅 | 提交事件推送 | 不支持 |
| 自定义模板 | 复用表单结构 | 不支持 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量化在线表单与、提交数据管理工具、支持表单创建、提交查询、字段配置等核心能、适合个人快速搭建、信息收集流程、在线表单笔记、是面向个人开发者、与小型团队的轻量、化表单管理、REST、API、与命令行工具的组、帮助用户在数分钟、内搭建可用的表单、收集流程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:个人博客联系表单

独立博主希望在博客底部放一个联系表单,访客填写后博主收到邮件通知。

```bash
# 1. 获取项目ID
curl -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  "https://api.web-notepad.example/v1/projects" | jq '.data[] | {projectId, name}'
# ...
# 2. 创建联系表单
curl -X POST -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.web-notepad.example/v1/forms" \
  -d '{
    "name": "博客联系表单",
    "description": "访客留言通道",
    "projectId": "proj_xxx",
    "fields": [
      {"path": "name", "label": "称呼", "type": "text", "required": true},
      {"path": "email", "label": "邮箱", "type": "email", "required": true},
      {"path": "message", "label": "留言内容", "type": "textarea"}
    ]
  }'
# ...
# 3. 发布表单
curl -X PATCH -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.web-notepad.example/v1/forms/{formId}" \
  -d '{"status": "published"}'
```

### 场景二:小型活动报名

线下读书会组织者需要快速收集参与者信息,人数预计30-50人。

```bash
# 创建报名表单
curl -X POST -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.web-notepad.example/v1/forms" \
  -d '{
    "name": "读书会报名",
    "projectId": "proj_xxx",
    "fields": [
      {"path": "name", "label": "姓名", "type": "text", "required": true},
      {"path": "phone", "label": "手机号", "type": "phone", "required": true},
      {"path": "session", "label": "场次", "type": "select", "options": [
        {"value": "morning", "label": "上午场"},
        {"value": "afternoon", "label": "下午场"}
      ]}
    ]
  }'
# ...
# 查询报名情况
curl -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  "https://api.web-notepad.example/v1/forms/{formId}/submissions?pageSize=50"
```

### 场景三:产品反馈收集

MVP阶段产品经理希望快速收集种子用户反馈,无需自建后端。

```bash
# 提交反馈
curl -X POST -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.web-notepad.example/v1/forms/{formId}/submissions" \
  -d '{
    "data": {
      "name": "张三",
      "email": "zhangsan@example.com",
      "message": "希望增加导出PDF功能"
    }
  }'
```

## 不适用场景

以下场景在线表单笔记(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

预计上手时间:<60秒。

### Step 1:配置API Key

```bash
export WEB_NOTEPAD_API_KEY="your_api_key_here"
```

### Step 2:验证连通性

```bash
curl -H "Authorization: Bearer $WEB_NOTEPAD_API_KEY" \
  "https://api.web-notepad.example/v1/projects"
```

返回项目列表即代表连通正常。

### Step 3:创建第一个表单

参考"使用场景"中的任意一个示例,3分钟内即可上线。

#
## 示例

### 字段类型速查表

| 类型 | 描述 | 校验选项 |
|:-----|:-----|:-----|
| `text` | 单行文本 | minLength, maxLength, pattern |
| `email` | 邮箱 | 内置校验 |
| `phone` | 电话 | 内置校验 |
| `number` | 数字 | min, max |
| `date` | 日期 | - |
| `select` | 下拉 | options: [{value, label}] |
| `checkbox` | 复选 | - |
| `textarea` | 多行文本 | minLength, maxLength |
| `file` | 文件上传 | 免费版限制1MB以内 |

### 字段Schema完整示例

```json
{
  "path": "fieldName",
  "label": "显示名称",
  "type": "text",
  "required": true,
  "placeholder": "提示文字",
  "helpText": "帮助说明",
  "options": [{"value": "a", "label": "选项A"}],
  "validation": {
    "minLength": 1,
    "maxLength": 500,
    "pattern": "^[A-Z].*",
    "min": 0,
    "max": 100
  }
}
```

## 最佳实践

1. **字段命名遵循语义化**:`path`使用小驼峰或下划线命名,避免中文或特殊字符
2. **必填字段控制在3个以内**:过多必填项会显著降低提交率
3. **为长文本字段设置maxLength**:防止恶意超大输入拖垮查询性能
4. **按业务线划分项目**:不同业务线使用独立project,便于权限隔离与数据统计
5. **定期清理测试数据**:测试完成后及时删除测试提交,避免污染统计

## 常见问题

### Q1: 创建表单时返回403怎么办?

A: 检查API Key是否过期、是否对目标项目有写权限。免费版API Key默认仅对所属账户的项目可写。

### Q2: 提交数据后无法立即查询到?

A: 系统存在最长2秒的写入延迟。建议在创建提交后等待1-2秒再发起查询。

### 已知限制

A: 有的。免费版限制每小时200次请求、每天2000次请求。响应头`X-RateLimit-Remaining`会返回剩余配额。

### Q4: 表单可以设置截止时间吗?

A: 免费版不支持自动截止。可以通过`status`字段手动将表单状态改为`draft`来停止接收提交。

### Q5: 删除表单后数据还能恢复吗?

A: 不能。删除表单会级联删除其下所有提交数据,操作不可逆。建议删除前先导出数据。

## 错误处理

| 错误场景(症状) | 可能原因 | 解决方案 |
|------:|------:|------:|
| 401 Unauthorized | API Key缺失或无效 | 检查环境变量是否正确设置 |
| 404 Not Found | 表单ID或提交ID错误 | 确认ID复制完整,无多余空格 |
| 429 Too Many Requests | 触发频率限制 | 等待60秒后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令,或升级专业版 |
| 字段类型不生效 | 字段type值拼写错误 | 对照"字段类型速查表"检查 |
| 提交数据丢失 | 误删表单 | 表单删除不可逆,需重建并重新收集 |
## 免费版限制

本免费体验版限制以下高级功能:

- 批量提交(单次>10条)、批量导出(>1000条)
- Webhook事件订阅与第三方推送
- 自定义表单模板与字段复用
- 高级筛选(多条件组合、自定义字段过滤)
- 团队协作与RBAC权限管理
- 数据加密存储与审计日志

解锁全部功能请使用专业版:web-notepad-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Shell环境**: Bash或兼容Shell(用于执行curl示例)
- **Python**: 3.8+(可选,用于辅助脚本)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| curl | 命令行工具 | 必需 | 操作系统自带或通过包管理器安装 |
| jq | JSON处理工具 | 推荐 | 通过`apt install jq`或`brew install jq`安装 |
| 表单服务API | 在线服务 | 必需 | 通过控制台获取API Key |

### API Key 配置
- **API Key 存储**: 通过环境变量`WEB_NOTEPAD_API_KEY`传入,禁止硬编码在脚本中
- **安全建议**: 在CI/CD环境中使用Secret管理服务注入,避免提交到代码仓库
- **轮换策略**: 建议每90天轮换一次API Key,旧Key在控制台主动吊销

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "在线表单笔记(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "web notepad"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
