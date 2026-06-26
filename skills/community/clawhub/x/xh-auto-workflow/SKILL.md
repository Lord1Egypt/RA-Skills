---
name: auto-workflow-pro
description: 自动化工作流引擎。定时执行任务链：数据采集→处理→通知→存档。支持cron定时、 webhook触发、文件监控。
---

# Auto Workflow Pro - 自动化工作流引擎

## 功能特点

### ⚙️ 任务链编排
- 可视化任务流程定义
- 支持串行/并行执行
- 任务间数据传递

### ⏰ 定时执行
- Cron表达式精确控制
- 间隔执行（每N分钟/小时）
- 单次定时任务

### 🔗 触发器
- Webhook HTTP触发
- 文件夹文件监控
- 队列消息触发

### 📋 内置任务
- HTTP请求
- 数据清洗/转换
- 文件读写
- 邮件/消息通知
- 数据库操作

## 安装

```bash
cd auto-workflow-pro
npm install
```

## 快速开始

### 定义工作流 (workflow.json)
```json
{
  "name": "daily-report",
  "trigger": { "type": "cron", "expr": "0 9 * * *" },
  "tasks": [
    { "type": "http", "url": "https://api.example.com/data", "save": "temp.json" },
    { "type": "transform", "input": "temp.json", "output": "report.json" },
    { "type": "email", "to": "user@example.com", "subject": "日报", "attach": "report.json" }
  ]
}
```

### 运行
```bash
# 立即执行
node workflow.js --run daily-report

# 守护进程模式（监听触发）
node workflow.js --daemon

# 查看任务状态
node workflow.js --status
```

## 示例场景

| 场景 | 触发 | 任务链 |
|------|------|--------|
| 每日数据同步 | cron 0 2 * * * | API获取 → 清洗 → 存库 |
| 新文件处理 | 文件监控 | 检测新文件 → 转换 → 通知 |
| 异常报警 | webhook | 检查服务 → 告警 → 记录 |

## 任务类型

- `http`: HTTP请求
- `transform`: 数据转换
- `email`: 发送邮件
- `webhook`: 回调通知
- `file`: 文件操作
- `database`: 数据库操作
- `sleep`: 延迟等待