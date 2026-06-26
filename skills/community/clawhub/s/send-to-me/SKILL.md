---
name: send-to-me
description: 企业微信消息发送工具。当需要发送消息、报告、通知或告警时使用，支持指定消息来源（sender）和接收人（touser）。
---

# Send To Me

## 概述

本技能用于向企业微信发送文本消息。当需要发送消息、报告、通知、告警等任何需要向我发送消息的场景时，都可以使用此技能。

> **作者微信公众号：XiaoqiangClub** <br/>
> **配置教程：https://xiaoqiangclub.blog.csdn.net/article/details/144614019**

## 特点

- **使用广泛验证的 python-dotenv 库**: 稳定可靠的 .env 配置解析
- **CLI 支持**: 提供命令行工具，可直接终端调用
- **灵活配置**: 支持命令行参数、环境变量、.env 文件配置
- **美化格式**: 内置多种消息格式模板，支持 emoji 和结构化内容
- **指定接收人**: 支持通过参数或配置文件指定消息接收人

## 快速开始

### 1. 安装依赖

```bash
pip install python-dotenv
```

### 2. 配置企业微信

首次使用需要配置企业微信参数，详见：[配置教程](https://xiaoqiangclub.blog.csdn.net/article/details/144614019)

```bash
# 复制配置文件
cp env_example.txt .env

# 编辑 .env 文件，填入你的企业微信配置
```

### 3. 发送消息

```bash
# 发送简单消息
python scripts/send_message.py "你好，这是一条测试消息"

# 指定消息来源
python scripts/send_message.py "备份任务已完成" -s "📦 数据备份服务"

# 指定接收人（发送给指定用户，多个用 | 分隔）
python scripts/send_message.py "重要通知" -t "zhangsan|lisi"

# 发送给部门
python scripts/send_message.py "部门通知" -p "2"

# 使用格式化模板
python scripts/send_message.py "$(python -c 'from scripts.message_formatter import MessageFormatter; print(MessageFormatter.task_report("数据备份", "success", "备份完成", "文件大小: 1.2GB"))')"
```

## 配置

### 配置文件（推荐）

在 skill 目录下创建 `.env` 文件：

```bash
WECOM_CORP_ID=your_corp_id
WECOM_CORP_SECRET=your_corp_secret
WECOM_AGENT_ID=your_agent_id
WECOM_TOUSER=@all
WECOM_SENDER=🎸 XiaoqiangClub
```

> **如何获取配置信息？请阅读：**
> https://xiaoqiangclub.blog.csdn.net/article/details/144614019

### 环境变量

```bash
# Windows
set WECOM_CORP_ID=your_corp_id
set WECOM_CORP_SECRET=your_corp_secret
set WECOM_AGENT_ID=your_agent_id

# Linux/Mac
export WECOM_CORP_ID=your_corp_id
export WECOM_CORP_SECRET=your_corp_secret
export WECOM_AGENT_ID=your_agent_id
```

### 命令行参数

```bash
python scripts/send_message.py "消息内容" -c corp_id -k corp_secret -a agent_id
```

### 配置优先级

```
命令行参数 > 环境变量 > .env 文件
```

## 接收人配置 (touser / toparty / totag)

企业微信支持三种接收方式，可以组合使用：

| 参数      | 说明         | 示例                                   |
| --------- | ------------ | -------------------------------------- |
| `touser`  | 指定用户账号 | `zhangsan` 或 `zhangsan\|lisi\|wangwu` |
| `toparty` | 指定部门 ID  | `2` 或 `2\|3\|4`                       |
| `totag`   | 指定标签 ID  | `1` 或 `1\|2\|3`                       |
| `@all`    | 发送给所有人 | `touser=@all`                          |

> **注意**：touser、toparty、totag 至少要有一个非空，否则消息无法送达

### 如何获取用户账号？

企业微信管理后台 → 通讯录 → 查看用户的 **账号** 字段

## 消息来源 (sender)

`sender` 参数用于标识**消息的发送来源**，让接收者知道这条消息是从哪个服务/系统/应用发出的。

### sender 命名建议

| 场景       | sender 示例        | 说明                   |
| ---------- | ------------------ | ---------------------- |
| 定时任务   | `📦 数据备份服务`  | 标识备份任务发送的消息 |
| 监控系统   | `🚨 系统监控中心`  | 标识监控告警消息       |
| CI/CD      | `🔄 CI/CD 流水线`  | 标识构建/部署消息      |
| 数据分析   | `📊 数据分析平台`  | 标识报表消息           |
| 定时脚本   | `⏰ 定时清理任务`  | 标识定时任务消息       |
| 通用机器人 | `🎸 XiaoqiangClub` | 通用自动发送的消息     |

### 使用示例

```python
from scripts.send_message import send_wechat_message

send_wechat_message(
    message="备份任务已完成",
    sender="📦 数据备份服务"
)
```

## 消息格式模板

本 skill 内置了 `MessageFormatter` 类，提供多种预设的消息格式：

### 1. 任务报告 (task_report)

适用于定期任务执行结果的汇报。

```python
from scripts.message_formatter import MessageFormatter

message = MessageFormatter.task_report(
    task_name="数据备份",
    status="success",
    message="数据库备份任务已成功完成",
    details="备份文件: backup_2024.db\n备份大小: 1.2GB\n耗时: 5分30秒"
)
```

**输出效果：**

```
📋 任务报告

━━━━━━━━━━
🏷️ 任务名称: 数据备份
📊 执行状态: ✅ SUCCESS
⏰ 执行时间: 2024-11-04 18:30:00
━━━━━━━━━━

📝 简要说明: 数据库备份任务已成功完成

📌 详细信息:
备份文件: backup_2024.db
备份大小: 1.2GB
耗时: 5分30秒
```

### 2. 任务通知 (job_notification)

适用于实时任务状态变更通知。

```python
message = MessageFormatter.job_notification(
    job_name="每日报表生成",
    event="completed",
    message="已生成今日报表，请查收附件。"
)
```

**输出效果：**

```
🚀 任务通知

━━━━━━━━━━
📦 任务名称: 每日报表生成
📌 事件类型: 🏁 COMPLETED
⏰ 通知时间: 2024-11-04 18:30:00
━━━━━━━━━━

已生成今日报表，请查收附件。
```

### 3. 系统告警 (system_alert)

适用于系统异常或告警信息的推送。

```python
message = MessageFormatter.system_alert(
    level="error",
    title="数据库连接失败",
    message="主数据库连接超时，请检查网络和数据库状态。",
    details="1. 检查数据库服务器状态\n2. 检查防火墙规则\n3. 查看数据库日志"
)
```

**输出效果：**

```
🚨 系统告警

━━━━━━━━━━
⚠️ 告警级别: 🟠 错误 ❌
📌 告警标题: 数据库连接失败
⏰ 发生时间: 2024-11-04 18:30:00
━━━━━━━━━━

📝 告警内容:
主数据库连接超时，请检查网络和数据库状态。

📌 处理建议:
1. 检查数据库服务器状态
2. 检查防火墙规则
3. 查看数据库日志
```

### 4. 每日汇总 (daily_summary)

适用于日报、周报等汇总信息。

```python
message = MessageFormatter.daily_summary(
    date="2024-11-04",
    stats={
        "处理任务": "128 个",
        "成功": "125 个",
        "失败": "3 个",
        "总耗时": "2小时30分"
    },
    highlights="- 优化了数据处理流程，处理速度提升20%\n- 修复了定时任务的时区问题"
)
```

**输出效果：**

```
📊 每日汇总

━━━━━━━━━━
📅 汇总日期: 2024-11-04
⏰ 生成时间: 2024-11-04 18:30:00
━━━━━━━━━━

📈 统计数据:
  • 处理任务: 128 个
  • 成功: 125 个
  • 失败: 3 个
  • 总耗时: 2小时30分

✨ 今日要点:
- 优化了数据处理流程，处理速度提升20%
- 修复了定时任务的时区问题
```

### 5. 自定义消息 (custom)

适用于灵活的自定义消息格式。

```python
message = MessageFormatter.custom(
    title="项目更新",
    content="项目开发进度报告",
    fields={
        "当前阶段": "开发中",
        "完成度": "65%",
        "预计完成": "2024-12-01"
    }
)
```

**输出效果：**

```
📌 项目更新

━━━━━━━━━━

项目开发进度报告

  • 当前阶段: 开发中
  • 完成度: 65%
  • 预计完成: 2024-12-01
```

## 命令行参数

| 参数            | 简写 | 说明                 | 默认值            |
| --------------- | ---- | -------------------- | ----------------- |
| `message`       | -    | 消息内容（必填）     | -                 |
| `--sender`      | `-s` | 消息发送来源         | .env 配置         |
| `--corp-id`     | `-c` | 企业微信 CorpID      | .env 配置         |
| `--corp-secret` | `-k` | 企业微信密钥         | .env 配置         |
| `--agent-id`    | `-a` | 企业微信应用 AgentID | .env 配置         |
| `--touser`      | `-t` | 接收用户             | @all 或 .env 配置 |
| `--toparty`     | `-p` | 接收部门             | 空                |
| `--totag`       | `-g` | 接收标签             | 空                |

## 代码调用

```python
from scripts.send_message import send_wechat_message

success = send_wechat_message(
    message="任务执行完成",
    sender="📦 数据备份服务",
    touser="@all",
    toparty="",
    totag=""
)

if success:
    print("消息发送成功")
else:
    print("消息发送失败")
```

## 返回值

- 发送成功: `True`
- 发送失败: `False`

## 注意事项

1. 企业微信 API 有调用频率限制，请合理使用
2. touser、toparty、totag 至少要有一个非空，否则消息无法送达
3. 请妥善保管 CorpID 和 CorpSecret，不要泄露到代码仓库
4. 建议使用 `MessageFormatter` 格式化消息，可读性更好

---

**作者微信公众号：XiaoqiangClub** <br/>
**配置教程：https://xiaoqiangclub.blog.csdn.net/article/details/144614019**
