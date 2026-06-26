---
name: today-task
description: 通用任务结果推送器，当任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。
trigger: 当用户说"任务完成，推送到负一屏"、"推送任务结果"、"发送到负一屏"或任何任务完成后需要推送结果到负一屏的场景
config:
  required:
    - authCode: "授权码，从负一屏获取，用于身份验证"
    - pushServiceUrl: "推送服务URL，config.json中有默认值"
  optional:
    - timeout: "超时时间（秒），默认30"
    - max_content_length: "最大内容长度，默认5000"
    - auto_generate_id: "是否自动生成任务ID，默认true"
    - default_result: "默认任务结果，默认'任务已完成'"
    - log_level: "日志级别，默认'INFO'"
    - save_records: "是否保存推送记录，默认true"
    - records_dir: "记录目录，默认'push_records'"
    - max_records: "最大记录数，默认100"
---

# Today Task

## 技能概述

这是一个通用的任务结果推送器，专门用于在任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。

## 🚀 使用方式（模型必读）

### 第一步：执行任务推送（只支持 JSON 输入（确保格式完整））

```bash
# 1. 创建JSON文件
{
 "task_name": "任务名称",
 "task_content": "# Markdown内容",
 "task_result": "完成状态"
}

# 2. 推送
python scripts/task_push.py --data task.json
```

### 快速创建工具

```bash
# 从markdown文件创建JSON
python scripts/create_task_json.py "任务名称" content.md
# 输出：已创建 任务名称_20260402.json
```

### 为什么？

- ✅ JSON 确保 markdown 格式 100%保留
- ✅ 避免命令行编码和转义问题
- ✅ 使用更简单可靠

---

**注意**：不再支持`--name`、`--content`等命令行参数。

### 第二步：推送成功后自动检查技能更新

```bash
python scripts/update_checker.py
```

**更新检查策略**：

- **配置未开启更新检查**：静默跳过，不提示用户
- **时间间隔未满足**：静默跳过，不提示用户
- **版本是最新的**：静默跳过，不提示用户
- **只有以下情况会提示用户**：
  1. **发现新版本可用**：显示更新通知和更新命令
  2. **更新检查异常**：网络问题、ClawHub 服务异常等，显示错误信息

### 第三步：在对话中整合显示结果

**使用 JSON 推送成功 + 有更新时：**

```
✅ 任务推送成功！

🔄 技能更新检查：
发现新版本可用！
当前版本: {当前版本}
最新版本: {最新版本}

💡 更新命令: `clawhub update today-task`
```

**使用 JSON 推送成功 + 无更新/无需检查时：**

```
✅ 任务推送成功！
（技能更新检查：配置未开启/时间间隔未满足/已是最新版本，无需提示）
```

**使用 JSON 推送成功 + 更新检查异常时：**

```
✅ 任务推送成功！
⚠️ 更新检查异常：无法从ClawHub获取版本信息，请检查网络或稍后重试
```

**推送失败时：**

```
❌ 任务推送失败！
{错误信息}
```

### 关键要求：

1. **只使用 JSON 输入**：必须通过 JSON 文件推送，确保 markdown 格式完整保留
2. **智能更新检查**：只在必要时提示用户（有更新或检查异常）
3. **减少干扰**：配置未开启、时间间隔未满足、版本最新时不提示
4. **结果整合显示**：将推送结果和更新检查结果一起在对话中回复
5. **异常处理**：更新检查异常时给出明确提示
6. **给出具体命令**：如果有更新，必须显示 `clawhub update today-task`

## 🔒 安全说明

本技能已通过安全审查，不包含恶意代码。除可选的技能更新检查外，所有网络请求仅发送到用户配置的指定 URL。更新检查会联系 ClawHub 服务获取版本信息。

### ⚠️ 重要安全提示

**本技能会传输以下数据到配置的端点：**

1. **授权码 (authCode)**：用于服务认证的敏感令牌
2. **任务内容 (task_content)**：您输入的任务文本内容
3. **任务元数据**：任务名称、ID、时间戳、执行结果等

### 🔐 安全特性

- **HTTPS 加密传输**：所有数据通过 TLS 加密传输
- **本地日志脱敏**：敏感信息在日志中显示为 `ABC***` 格式
- **用户完全控制**：可配置自定义端点，控制数据流向

详细安全声明请查看 [SECURITY.md](./SECURITY.md)。

## ⚙️ 配置要求（必需）

**本技能需要以下配置才能正常工作：**

### 1. 授权码 (authCode) - **必需**

- **用途**：用于身份验证，确保只有授权用户可以向负一屏推送内容
- **安全重要性**：授权码是敏感令牌，会通过网络传输到配置的端点
- **获取方式**：
  先从从 OpenClaw 全局配置中获取，使用命令 openclaw config get skills.entries.today-task.config.authCode。
  如果不存在则提示用户按如下步骤获取：
  1. 从手机桌面右滑进入负一屏
  2. 点击左上角头像
  3. 进入"我的"页面，点击右上角设置图标
  4. 选择"动态管理"
  5. 点击"关联账号"
  6. 找到"Claw 智能体"并点击获取授权码

#### ⚠️ 授权码安全警告

1. **授权码会通过网络传输**：作为 HTTP 请求的一部分发送到配置的端点
2. **不要在聊天中粘贴授权码**：避免授权码被记录在聊天历史中
3. **使用安全配置方式**：推荐使用 OpenClaw 全局配置或本地配置文件
4. **定期更新授权码**：增强安全性，防止未授权访问

### 2. 推送 URL (pushServiceUrl) - **必需**

- **用途**：指定推送服务的目标地址
- **获取方式**：从config.json 中获取
- **默认值**：`https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload`

### 🔧 配置方式

本技能使用**混合配置系统**，支持灵活的配置优先级：

## ⚠️ 重要安全说明

### 数据传输透明度

**使用本技能时，您的数据将被发送到配置的推送端点：**

#### 1. 默认端点（如果使用默认配置）

```
https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload
```

- **服务提供商**：华为云（Huawei Cloud）
- **地理位置**：中国东莞（DRCN = Dongguan）
- **数据传输**：通过 HTTPS 加密传输

#### 2. 传输的数据包括：

- **授权码** (`authCode`)：用于服务认证的令牌
- **任务内容** (`task_content`)：您输入的任务文本内容
- **任务元数据**：任务名称、ID、时间戳、执行结果等

#### 3. 隐私建议：

- 避免在任务内容中包含高度敏感的个人信息
- 了解数据发送的目的地
- 可以配置自定义端点以控制数据流向

### 配置优先级规则

1. **优先使用 OpenClaw 全局配置**
2. **如果没有设置，则使用本地 config.json 中的配置**
3. **如果都没有设置，技能将无法正常工作**

#### OpenClaw 全局配置命令

```bash
# 设置授权码
openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE

# 设置推送URL
openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL

# 查看技能配置
openclaw config get skills.entries.today-task

# 删除配置
openclaw config unset skills.entries.today-task.config.authCode
openclaw config unset skills.entries.today-task.config.pushServiceUrl
```

#### 本地配置文件 (config.json)

其他配置项在技能目录的 `config.json` 文件中设置：

```json
{
  "timeout": 30,
  "max_content_length": 5000,
  "auto_generate_id": true,
  "default_result": "任务已完成",
  "log_level": "INFO",
  "save_records": true,
  "records_dir": "push_records",
  "max_records": 100,
  "pushServiceUrl": "https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload"
}
```

**注意**：如果缺少必需的授权码或推送 URL 配置，技能将无法正常工作并会显示明确的错误信息。

## 💾 数据存储说明

**本技能会在本地创建以下目录用于运行记录：**

### 📁 日志目录 (`logs/`)

- **用途**：运行监控和故障排查
- **内容**：包含脱敏的运行信息（授权码显示为 `Twe7***` 格式）
- **控制**：通过 `log_level` 配置项控制详细程度

### 📁 推送记录目录 (`push_records/`)

- **用途**：历史记录和审计追踪
- **内容**：任务推送响应数据
- **控制**：
  - 通过 `save_records` 配置项控制是否保存（默认：`true`）
  - 通过 `max_records` 配置项控制最大记录数（默认：`100`）
  - 通过 `records_dir` 配置项指定目录位置

### 🔐 隐私保护措施

1. **敏感信息脱敏**：授权码等敏感信息在日志中仅显示部分字符
2. **用户完全控制**：可关闭记录保存功能
3. **本地存储**：所有文件仅存储在用户本地设备
4. **定期清理**：建议定期清理或通过配置限制文件数量

**用户责任**：请定期检查和管理这些本地文件，确保符合您的隐私要求。

## 🎯 设计理念

- **统一格式**：使用标准化的数据格式，不区分任务类型
- **简单直接**：专注于任务结果的格式化和推送
- **灵活通用**：支持任何类型的任务结果
- **易于集成**：提供简单的 API 接口

## 📋 触发条件

- "任务完成，推送到负一屏"
- "推送任务结果"
- "发送到负一屏"
- 任何任务完成后需要推送结果到负一屏的场景

## 🔄 工作流程

1. **版本检查**：自动检查技能更新，输出版本信息（如有更新会通知）
2. **任务完成**：其他技能或任务执行完成
3. **结果收集**：收集任务执行结果数据
4. **格式转换**：将任务结果转换为标准格式
5. **数据验证**：验证数据完整性和格式
6. **执行推送**：推送到负一屏系统
7. **结果反馈**：返回推送状态和记录，包含版本更新信息

## 📊 标准数据格式

### 推送数据格式

```json
{
  "authCode": "string",           // 授权码，负一屏上对openclaw进行账号关联之后生成的授权码
  "msgContent": [                 // MsgContent数组，消息内容
    {
      "scheduleTaskId": "string", // 任务ID，必填，对于周期性任务此ID需要保持一致
      "scheduleTaskName": "string", // 任务名称，必填，如"生成日报任务、生成新闻任务"
      "summary": "string",        // 任务摘要，必填，说明具体是什么任务，以及任务的执行状态，比如 "生成新闻早报任务已完成"、"生成新闻早报任务异常"
      "result": "string",         // 任务执行结果，必填，说明是已成功完成了，还是异常中断了
      "content": "string",        // 任务的执行结果具体内容，markdown格式的长文本数据，必填
      "source": "string",         // 来源，人工是openclaw的任务，则值为OpenClaw，必填
      "taskFinishTime": "number"  // 任务完成的时间戳，秒的时间戳，必填
    }
  ]
}
}
```

## ⏰ 时间戳使用指南

### 重要提醒

**避免使用错误的时间戳获取方式，这可能导致推送时间显示不正确！**

#### ❌ 错误方式（不要使用）

```powershell
# PowerShell 中的错误方式（可能产生时区问题）
[int][double]::Parse((Get-Date -UFormat %s))
[int](Get-Date -UFormat %s)
```

#### ✅ 正确方式

##### Python（本技能使用的方式）

```python
import time
timestamp = int(time.time())  # UTC 时间戳，推荐使用
```

##### PowerShell（其他脚本中使用）

````powershell
# 正确！使用 UTC 时间，避免时区问题
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()

##### PowerShell需要设置控制台编码为UTF-8
```powershell
# 正确设置控制台编码为UTF-8
chcp 65001
````

##### 本技能的时间戳处理

本技能自动处理时间戳：

- 使用 Python 的 `time.time()` 获取 UTC 时间戳
- 自动验证时间戳合理性
- 确保与负一屏服务时间一致

### 时区说明

- **负一屏服务使用 UTC 时间戳**
- 本地时间可能因时区设置不同而产生误差
- 始终使用 **UTC 时间** 避免时区问题
- 中国时区（UTC+8）的用户需要注意时间转换

### 验证时间戳

如果你在其他脚本中集成本技能，请验证时间戳：

```python
# 验证时间戳是否在合理范围内
import time

def validate_timestamp(timestamp):
    min_valid = 1609459200  # 2021-01-01
    max_valid = int(time.time()) + 31536000  # 当前时间 + 1年
    return min_valid <= timestamp <= max_valid

# 使用示例
current_ts = int(time.time())
if validate_timestamp(current_ts):
    print(f"时间戳有效: {current_ts}")
else:
    print(f"时间戳可能有问题: {current_ts}")
```

### 常见问题

1. **时间显示不对**：检查是否使用了本地时间而非 UTC 时间
2. **时间戳为 0 或负数**：时间戳获取方式错误
3. **时间差 8 小时**：中国时区（UTC+8）未正确转换

### 最佳实践

1. **统一使用 UTC 时间**：所有时间戳都使用 UTC
2. **验证时间戳**：在关键操作前验证时间戳有效性
3. **记录时间源**：明确记录时间戳的来源和时区
4. **使用本技能的工具**：本技能已正确处理时间戳，无需额外处理

## 内容格式规范

任务的执行结果具体内容使用 markdown 格式，遵循以下样式规范：

1. **主标题文本**

   - font size: Subtitle_L (Bold) = 18
   - color: font_primary = #000000 90%
   - 行高：默认

2. **一级文本**

   - font size: Body_L (Bold) = 16
   - color: font_primary = #000000 90%
   - 行高：22

3. **二级文本**

   - font size: Body_M (Bold) = 14
   - color: font_primary = #000000 90%
   - 行高：22

4. **段落文本**

   - font size: Body_M (regular) = 14
   - color: font_secondary = #000000 60%
   - 行高：22

5. **分割线**

   - 使用控件：Divider

6. **AI 生成注释文本**
   - font size: 10 medium
   - color: font_fourth #000000 20%
   - 行高：默认

## 📁 输入要求

### 任务结果数据格式

```json
{
  "task_id": "string", // 任务ID（必填）
  "task_name": "string", // 任务名称（必填）
  "task_result": "string", // 任务执行结果描述（必填）
  "task_content": "string", // 任务详细内容，markdown格式（必填）
  "schedule_task_id": "string", // 周期性任务ID（必填，非周期性任务时等于task_id）
  "auth_code": "string" // 授权码（可选，可在配置中设置）
}
```

### 简化输入格式

```json
// 格式1：完整格式
{
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "task_result": "任务已完成",
  "task_content": "# 今日新闻汇总\n\n## 热点新闻\n\n1. OpenAI发布新一代模型...",
  "schedule_task_id": "news_20240327_1001",
  "auth_code": "asdf166553"
}
```

## 🛠️ 推送流程

1. **数据接收**：接收任务结果数据
2. **格式标准化**：转换为标准 pushData 格式
3. **数据验证**：验证必需字段
4. **授权码处理**：使用配置的授权码或数据中的授权码
5. **推送执行**：调用负一屏 API 推送数据
6. **结果处理**：处理推送结果并保存记录

## 📝 输出格式

### 成功响应

```json
{
  "success": true,
  "message": "任务结果推送成功",
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "push_time": "2024-03-27 10:15:30",
  "record_id": "push_20240327_101530",
  "hiboard_response": {
    "code": "0000000000",
    "desc": "成功"
  },
  "update_check": {
    // 版本更新检查
    "status": "skipped_or_error",
    "message": "更新检查异常或配置未开启",
    "should_notify": false // 是否提示用户，true则提示用户
  }
}
```

### 错误响应

```json
{
  "success": false,
  "message": "错误描述",
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "error_type": "validation|format|network|system|auth|service",
  "push_time": "2024-03-27 10:15:30",
  "suggestion": "建议的解决方案",
  "update_check": {
    // 版本更新检查
    "status": "skipped_or_error",
    "message": "更新检查异常或配置未开启",
    "should_notify": false // 是否提示用户，true则提示用户
  }
}
```

## 🚨 错误码处理指南

系统提供了详细的错误码处理功能，当推送失败时会返回具体的错误信息和解决方案。

### 常见错误码及解决方案

#### 1. 错误码: 0000900034 - 授权码无效或未关联

**问题描述**: 授权码无效或用户未在负一屏关联账号
**解决方案**:

1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw 智能体"并点击获取授权码

#### 2. 错误码: 0200100004 - 负一屏云推送服务异常

**问题描述**: 负一屏云推送到服务动态云有报错，需要检查返回的 desc 字段

##### CP 错误码: 82600017 - 设备未联网或未登录华为账号

**解决方案**:

1. 检查设备 Wi-Fi 或移动数据是否已连接
2. 打开"设置"应用
3. 进入"华为账号"或"帐号中心"
4. 确保已登录华为账号
5. 如未登录，请使用华为账号登录

##### CP 错误码: 82600013 - 服务动态推送开关已关闭

**解决方案**:

1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 找到"AI 任务完成通知"
6. 打开"场景开关"和"服务提供方开关"

##### CP 错误码: 82600005 - 服务动态云服务异常

**解决方案**:

1. 等待几分钟后重试
2. 如问题持续，可能是服务端维护
3. 可稍后再试或联系技术支持

### 错误信息格式

错误信息会包含详细的结构化内容：

- 错误代码和描述
- 问题分析
- 具体解决方案
- 操作步骤
- 技术支持信息

### 示例错误信息

```
错误代码: 0000900034
错误描述: 授权码无效

[问题分析] 授权码无效或未关联

[解决方案] 请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码

[操作步骤]
1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw智能体"并点击获取授权码

[技术支持]
- 如问题无法解决，请记录错误代码并提供给技术支持
- 错误发生时间: 2026-03-30 17:10:00
```

## 🔗 与其他技能配合

### 典型工作流

```
1. 执行某个任务（如查询新闻、检查天气、生成报告等）
2. 任务完成后，生成markdown格式的结果
3. 调用本技能推送结果到负一屏
4. 用户可以在负一屏查看任务结果
```

### 集成示例

```python
# 在其他技能中调用本技能
def complete_task_and_push(task_name, task_content, task_result="任务已完成"):
    # 1. 准备任务数据
    task_data = {
        "task_id": f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "task_name": task_name,
        "task_result": task_result,
        "task_content": task_content
    }

    # 2. 调用推送技能
    push_result = push_to_negative_screen(task_data)

    return push_result
```

## 🚀 使用示例

### ⚠️ 首次使用安全提示

**首次使用本技能时请注意：**

1. **数据流向**：任务内容将发送到配置的推送端点
2. **默认端点**：`hiboard-claw-drcn.ai.dbankcloud.cn`（华为云服务）
3. **传输内容**：任务内容 + 授权码 + 元数据
4. **安全建议**：
   - 了解数据发送目的地
   - 避免包含高度敏感信息
   - 可以配置自定义端点

### 基本使用

```
# 任务完成后
任务完成，推送到负一屏
```

### 在脚本中使用（只支持 JSON 输入）

```bash
# 1. 首先创建 JSON 文件（推荐使用工具）
python scripts/create_task_json.py "任务名称" content.md

# 2. 推送任务结果（实际发送）
python scripts/task_push.py --data task_result.json

# 3. 安全测试：使用 --dry-run 参数避免实际发送
python scripts/task_push.py --data task_result.json --dry-run

# 4. 使用配置文件中的授权码
python scripts/task_push.py --data task_result.json --config config.json

# 重要：不再支持 --name、--content、--result 参数
# 必须使用 JSON 文件确保 markdown 格式完整保留
```

### 🔒 安全测试选项

- **`--dry-run`**：模拟推送，不实际发送数据
- **`--verbose`**：显示详细日志，包括端点信息
- **`--validate-only`**：仅验证数据格式，不推送

### 🔄 版本更新检查

**本技能包含自动版本更新检查功能：**

#### 检查时机

- 每次运行脚本时自动检查
- 从 ClawHub 获取最新版本信息
- 比较本地版本与远程版本

#### 输出信息

当检测到更新时，脚本会输出：

```
[检查] 检查技能更新...
[信息] 本地版本: 1.0.12
[信息] 从ClawHub检查...
[信息] ClawHub版本: 1.0.13
[信息] 远程版本: 1.0.13

============================================================
[通知] 技能更新通知
============================================================
本地版本: 1.0.12
远程版本: 1.0.13
来源: clawhub
更新命令: clawhub update today-task
============================================================
```

#### 更新策略

1. **仅通知，不自动更新**：出于安全考虑，脚本只通知有更新可用
2. **用户手动更新**：需要用户明确执行更新命令
3. **更新命令**：`clawhub update today-task`

#### 注意事项

- 如果本地有修改，更新可能被阻止
- 可以使用 `--force` 参数强制更新：`clawhub update today-task --force`
- 更新前建议备份本地修改

### ⚠️ 命令行授权码安全警告

**重要**：避免在命令行中直接传递授权码：

```bash
# ❌ 不安全：授权码在命令行历史中可见
python scripts/task_push.py --auth-code YOUR_AUTH_CODE --data task.json

# ✅ 安全：使用配置文件或 OpenClaw 全局配置
python scripts/task_push.py --data task.json
```

**授权码安全建议：**

1. **使用 OpenClaw 全局配置**：`openclaw config set skills.entries.today-task.config.authCode YOUR_CODE`
2. **使用本地配置文件**：在 `config.json` 中配置授权码
3. **避免聊天粘贴**：不要在聊天消息中粘贴授权码
4. **定期更新**：定期在负一屏中更新授权码

### 在 OpenClaw 技能中集成

```python
# 在技能脚本中调用
from task_pusher import TaskPusher

def skill_main():
    # ... 执行任务逻辑 ...

    # 生成markdown格式的结果
    markdown_content = generate_markdown_result(data)

    # 任务完成后推送结果
    pusher = TaskPusher()
    result = pusher.push({
        "task_id": f"task_{int(time.time())}",
        "task_name": "AI新闻汇总",
        "task_result": "任务已完成",
        "task_content": markdown_content
    })

    return result
```

## ⚙️ 配置说明 - 混合配置系统

本技能使用混合配置系统，支持灵活的配置优先级：

### 配置优先级规则

1. **auth_code (授权码)**：

   - 优先使用 OpenClaw 全局配置
   - 如果没有设置，则使用本地配置（如果存在）
   - 如果都没有设置，则提示用户配置

2. **pushServiceUrl (推送 URL)**：

   - 优先使用 OpenClaw 全局配置
   - 如果没有设置，则使用本地 config.json 中的 `pushServiceUrl` 配置
   - 如果都没有设置，则提示用户配置

3. **其他配置项**：使用本地 config.json 中的配置

### 配置加载顺序

1. 首先加载本地 config.json 文件中的基础配置
2. 然后检查 OpenClaw 全局配置
3. 根据优先级规则合并配置
4. 验证必需配置是否完整

### OpenClaw 全局配置命令

#### 1. 设置授权码

```bash
openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
```

#### 2. 设置推送 URL

```bash
openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL
```

#### 3. 查看技能配置

```bash
openclaw config get skills.entries.today-task
```

#### 4. 删除配置

```bash
# 删除授权码配置
openclaw config unset skills.entries.today-task.config.authCode

# 删除推送URL配置
openclaw config unset skills.entries.today-task.config.pushServiceUrl
```

### 配置示例

```bash
# 设置授权码
openclaw config set skills.entries.today-task.config.authCode KzLEP2FjYPg1

# 设置推送URL
openclaw config set skills.entries.today-task.config.pushServiceUrl https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload
```

### 本地配置文件 (config.json)

其他配置项在技能目录的 `config.json` 文件中设置：

```json
{
  "timeout": 30,
  "max_content_length": 5000,
  "auto_generate_id": true,
  "default_result": "任务已完成",
  "log_level": "INFO",
  "save_records": true,
  "records_dir": "push_records",
  "max_records": 100,
  "pushServiceUrl": "https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload"
}
```

**配置优先级说明**：

1. **auth_code (授权码)**：优先使用 OpenClaw 全局配置，如果没有则使用本地配置
2. **pushServiceUrl (推送 URL)**：优先使用 OpenClaw 全局配置，如果没有则使用本地 config.json 中的配置
3. **其他配置项**：使用本地 config.json 中的配置

### 🔑 授权码获取说明

**授权码是必填字段**，用于验证推送权限。如果未设置授权码或授权码无效，推送将失败。

**获取步骤**：

1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw 智能体"并点击获取授权码

**推送 URL 说明**：

- 默认 URL: `https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload`

### 🔄 自动检测授权码功能

当用户在对话中提供授权码时，系统会自动检测并提示使用 OpenClaw 配置命令。

**支持格式**：

- "我的授权码是 aqvIVhhWz7ir"
- "使用授权码 FrF2e6Pwqvpz"
- "授权码: NWrU7qbN8vvx"
- "auth: HO4hza2l9MYy"

**工作原理**：

1. 系统会分析用户输入，检测是否符合授权码格式
2. 检测到授权码后，生成 OpenClaw 配置命令
3. 提示用户使用命令设置配置
4. 设置完成后，技能将使用新的授权码

**使用示例**：

```
用户：我的授权码是 aqvIVhhWz7ir
系统：检测到授权码: aqvi***
请使用以下OpenClaw命令设置授权码:
openclaw config set skills.entries.today-task.config.authCode aqvIVhhWz7ir
```

### 🔑 授权码获取说明

**授权码是必填字段**，用于验证推送权限。如果未设置授权码或授权码无效，推送将失败并显示以下提示：

```
📱 请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码
```

**获取步骤**：

1. 打开负一屏应用
2. 进入"我的"页面
3. 找到"动态管理"
4. 点击"关联账号"
5. 找到"Claw 智能体"并点击获取授权码

**常见授权码错误**：

- `0000900034` - 授权码无效
- `The authCode is invalid` - 授权码无效
- 授权码未设置 - 配置文件中缺少 auth_code 字段

### 🔄 自动更新授权码功能

**新增功能**：当用户在对话中提供授权码时，系统会自动检测并更新到配置文件中。

**支持格式**：

- "我的授权码是 aqvIVhhWz7ir"
- "使用授权码 FrF2e6Pwqvpz"
- "授权码: NWrU7qbN8vvx"
- "auth: HO4hza2l9MYy"

**工作原理**：

1. 系统会分析用户输入，检测是否符合授权码格式
2. 检测到授权码后，自动更新到配置文件
3. 更新完成后会显示确认信息
4. 后续推送将使用新的授权码

**授权码格式要求**：

- 长度：10-20 个字符
- 组成：字母、数字，可能包含下划线或连字符
- 示例：`aqvIVhhWz7ir`, `FrF2e6Pwqvpz`, `NWrU7qbN8vvx`

**使用示例**：

```
用户：我的授权码是 aqvIVhhWz7ir
系统：✅ 检测到授权码，已更新到配置文件
```

### 配置验证

配置验证失败时会显示以下提示：

```
配置中缺少必需字段: auth_code, hiboards_url
请使用以下方式设置配置:
1. auth_code (授权码): 使用OpenClaw全局配置命令设置
   命令: openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
2. hiboards_url (推送URL): 使用OpenClaw全局配置命令设置
   命令: openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL

其他配置项请在技能目录的config.json文件中设置。
```

## 📁 文件结构

```
push-task-to-negative-screen/
├── SKILL.md                    # 技能定义
├── README.md                   # 使用说明
├── config.json                 # 配置文件示例
├── scripts/
│   ├── task_push.py           # 主推送脚本
│   ├── task_pusher.py         # 推送器类
│   ├── config.py              # 配置管理
│   ├── logger.py              # 日志工具
│   ├── hiboards_client.py     # 负一屏客户端
│   └── simple_test.py         # 测试脚本
└── push_records/              # 推送记录目录（自动创建）
```

## 💡 设计优势

1. **格式统一**：所有任务使用相同的推送格式
2. **简单易用**：接口简单，易于集成
3. **灵活性强**：支持任何类型的任务结果
4. **配置方便**：支持配置文件
5. **错误处理完善**：详细的错误信息和建议
6. **记录完整**：保存完整的推送记录

## 🎨 Markdown 内容生成建议

### 最佳实践

1. **使用标题层级**：合理使用#、##、###等标题
2. **列表展示**：使用-或\*表示列表项
3. **代码块**：使用```包裹代码
4. **表格**：使用 markdown 表格格式
5. **分割线**：使用---作为分割线

### 示例模板

```markdown
# 任务名称

## 执行结果

✅ 任务已完成

## 详细内容

- 项目 1: 结果描述
- 项目 2: 结果描述
- 项目 3: 结果描述

## 关键指标

| 指标   | 数值   | 状态 |
| ------ | ------ | ---- |
| 完成率 | 100%   | ✅   |
| 用时   | 5 分钟 | ⏱️   |

---

_生成时间: 2026-03-30 10:30:00_
```

## 🔐 完整安全指南

### 1. 数据流向透明度

**本技能设计为透明数据流：**

```
用户输入 → 技能处理 → HTTPS传输 → 配置的端点
```

#### 端点说明：

- **默认端点**：华为云负一屏服务 (`ai.dbankcloud.cn`)
- **自定义端点**：用户配置的任何 HTTPS 端点
- **本地测试**：使用 `--dry-run` 避免网络传输

### 2. 传输的数据

每次推送包含：

| 数据字段       | 内容             | 敏感性    |
| -------------- | ---------------- | --------- |
| `authCode`     | 授权令牌         | 🔴 高敏感 |
| `task_content` | 任务文本内容     | 🟡 中敏感 |
| 任务元数据     | 名称、ID、时间等 | 🟢 低敏感 |

### 3. 隐私保护措施

#### 本地保护：

- ✅ 日志脱敏：`authCode` 显示为 `ABC***`
- ✅ 可选记录：可关闭推送记录保存
- ✅ 本地存储：所有文件仅存本地

#### 传输保护：

- ✅ HTTPS 加密：所有传输使用 TLS
- ✅ 证书验证：验证服务器身份
- ✅ 最小数据：仅发送必要数据

### 4. 用户控制权

#### 配置控制：

- 端点配置：使用自定义端点
- 记录控制：关闭本地记录保存
- 日志控制：调整日志详细程度

#### 操作控制：

- 测试模式：`--dry-run` 模拟推送
- 验证模式：`--validate-only` 仅验证格式
- 详细日志：`--verbose` 查看完整信息

### 5. 最佳安全实践

#### 对于所有用户：

1. **了解数据流向**：知道数据发送到哪里
2. **审查任务内容**：避免包含敏感信息
3. **定期更新授权码**：增强安全性

#### 对于敏感数据：

1. **使用自定义端点**：控制数据目的地
2. **关闭本地记录**：`save_records: false`
3. **使用测试模式**：`--dry-run` 验证功能

#### 对于企业用户：

1. **部署私有端点**：完全控制数据流
2. **审计推送记录**：定期审查 `push_records/`
3. **监控技能使用**：通过日志监控活动

### 6. 合规性说明

#### 数据保护：

- 符合最小必要原则
- 提供用户控制选项
- 透明数据处理流程

#### 隐私权：

- 用户知情权：明确告知数据流向
- 用户控制权：提供配置选项
- 用户退出权：可停止使用并删除数据

### 7. 紧急措施

如果发现安全问题：

1. **立即停止使用**技能
2. **撤销授权码**：在负一屏中撤销
3. **删除本地数据**：清理 `logs/` 和 `push_records/`
4. **联系支持**：报告安全问题

---

**重要**：详细安全声明请查看 [SECURITY.md](./SECURITY.md)

_最后更新: 2026-03-31_
