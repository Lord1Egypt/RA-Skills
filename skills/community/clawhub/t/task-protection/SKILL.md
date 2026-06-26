---
name: task-protection
version: 1.0.0
description: Comprehensive task lifecycle management with automatic tracking, failure analysis, and completion feedback. Use when executing recurring system tasks (backups, health checks, news delivery), critical operations (config changes, data sync, deployments), external interactions (email sending, message notifications, API calls), user-delegated one-time tasks, or long-running operations over 1 minute. Provides 9 tool functions, 8 failure type analysis, progress tracking, and automated reporting.
---

# Task Protection - 任务闭环管理机制

> **核心原则**：所有重要任务必须有记忆、追踪、反馈、故障分析机制 —— 闭环管理

---

## 🚀 快速开始

### 基础用法（脚本中）

```bash
#!/bin/bash
source /path/to/task-utils.sh

# 1. 初始化任务
TASK_ID="my_task_$(date +%Y%m%d_%H%M%S)"
task_init "$TASK_ID" "任务名称" "任务描述"

# 2. 开始执行
task_start "$TASK_ID"

# 3. 记录过程
task_log "$TASK_ID" "INFO" "正在执行..."

# 4. 完成任务
task_complete "$TASK_ID" "执行成功"
# 或失败时
task_fail "$TASK_ID" "错误信息" "错误类型"
```

### AI 直接执行的任务

AI 在回复中说明并创建状态文件：

```
📋 任务登记：
- ID: task_20260314_0948_write_article
- 名称：撰写文章
- 状态：执行中

✅ 任务完成！
📋 详情:
  - 完成时间：09:48
  - 耗时：45 秒
  - 状态：成功

📄 状态文件：memory/tasks/task_20260314_0948_write_article.json
```

---

## 📁 文件结构

```
task-protection/
├── SKILL.md (本文件)
├── scripts/
│   ├── task-utils.sh              # 核心工具函数库（9 个函数）
│   ├── ai-task-register.sh        # AI 任务自动登记
│   ├── daily-news.sh              # 示例：新闻推送
│   ├── system-health-check.sh     # 示例：健康检查
│   ├── check-tasks.sh             # 示例：任务扫描
│   └── weekly-task-report.sh      # 周报统计
├── memory/
│   ├── task-registry.json         # 任务注册表
│   └── tasks/                     # 任务状态文件目录
├── logs/
│   └── tasks/                     # 任务日志目录
└── docs/
    ├── QUICKSTART.md              # 快速上手指南
    ├── task-trigger-criteria.md   # 触发标准
    └── ai-task-registration.md    # AI 登记指南
```

---

## 🎯 何时使用

### ✅ 需要完整闭环的任务（5 类）

1. **周期性任务** —— 新闻推送、健康检查、备份、定时同步
2. **关键操作** —— 配置修改、数据同步、系统升级、服务重启
3. **对外交互** —— 邮件发送、消息推送、API 调用、文件上传
4. **用户委托** —— 用户直接交代的任务（写文章、分析文件等）
5. **长时间运行** —— 执行时间 > 1 分钟的任务

### ⚠️ 可简化处理的任务（3 类）

- **简单查询** —— 只读操作，无副作用（读取文件、查看状态）
- **即时对话** —— 纯聊天、问答
- **探索性工作** —— 研究性、尝试性任务

---

## 🛠️ 核心工具函数（9 个）

### 1. task_init - 初始化任务

```bash
task_init "task_001" "发送邮件" "向团队发送周报"
```

**参数**：
- `task_id` - 任务 ID（建议格式：`类型_YYYYMMDD_HHMMSS_描述`）
- `task_name` - 任务名称
- `task_description` - 任务描述（可选）

**输出**：
- 创建状态文件 `memory/tasks/{task_id}.json`
- 记录初始化日志

---

### 2. task_start - 开始执行

```bash
task_start "task_001"
```

**功能**：
- 更新状态为 `running`
- 记录开始时间
- 添加"执行"阶段

---

### 3. task_log - 记录日志

```bash
task_log "task_001" "INFO" "邮件发送中..."
task_log "task_001" "WARN" "网络延迟"
task_log "task_001" "ERROR" "发送失败"
```

**日志级别**：
- `INFO` - 正常进度
- `WARN` - 可恢复问题
- `ERROR` - 失败/异常
- `DEBUG` - 调试信息

---

### 4. task_stage - 更新阶段

```bash
task_stage "task_001" "准备内容" "running"
task_stage "task_001" "准备内容" "done"
task_stage "task_001" "验证结果" "warning"
```

**阶段状态**：
- `running` - 进行中
- `done` - 完成
- `failed` - 失败
- `warning` - 警告

---

### 5. task_complete - 完成任务

```bash
task_complete "task_001" "邮件已发送，收件人：team@company.com"
```

**功能**：
- 更新状态为 `success`
- 记录完成时间和耗时
- 保存结果信息

---

### 6. task_fail - 失败处理

```bash
task_fail "task_001" "发送超时" "timeout"
```

**故障类型（8 类）**：
- `command_not_found` - 命令不存在
- `authentication_failed` - 认证失败
- `network_error` - 网络错误
- `timeout` - 执行超时
- `resource_not_found` - 资源不存在
- `permission_denied` - 权限不足
- `validation_error` - 验证失败
- `unknown_error` - 未知错误

**功能**：
- 更新状态为 `failed`
- 自动分析故障原因
- 提供修复建议
- 记录错误详情

---

### 7. task_retry - 重试任务

```bash
task_retry "task_001" 3 60  # 最多 3 次，间隔 60 秒
```

**参数**：
- `task_id` - 任务 ID
- `max_retries` - 最大重试次数（默认 3）
- `interval` - 重试间隔秒数（默认 60）

**退避策略**：
- `linear` - 线性退避（60s, 60s, 60s）
- `exponential` - 指数退避（30s, 60s, 120s）
- `fixed` - 固定间隔

---

### 8. task_status - 查询状态

```bash
task_status "task_001"
```

**输出**：JSON 格式的任务状态

---

### 9. task_list - 列出任务

```bash
task_list
```

**输出**：所有已登记任务列表

---

## 📊 任务状态文件结构

```json
{
  "taskId": "task_20260314_0948_example",
  "name": "任务名称",
  "description": "任务描述",
  "status": "success|failed|running|pending",
  "stages": [
    {"name": "准备", "status": "done", "timestamp": "..."},
    {"name": "执行", "status": "done", "timestamp": "..."}
  ],
  "logs": ["[2026-03-14 09:48:00] [INFO] 任务初始化"],
  "errors": [],
  "result": "任务完成",
  "duration": 120,
  "createdAt": "2026-03-14T09:48:00+08:00",
  "startedAt": "2026-03-14T09:48:00+08:00",
  "completedAt": "2026-03-14T09:50:00+08:00"
}
```

---

## 🔄 典型工作流

### 脚本任务示例

```bash
#!/bin/bash
source /path/to/task-utils.sh

TASK_ID="health_check_$(date +%Y%m%d_%H%M%S)"

# 初始化
task_init "$TASK_ID" "系统健康检查" "检查 Gateway、磁盘、内存、日志"
task_start "$TASK_ID"

# 阶段 1: 检查 Gateway
task_stage "$TASK_ID" "检查 Gateway" "running"
if systemctl --user is-active openclaw-gateway > /dev/null 2>&1; then
    task_log "$TASK_ID" "INFO" "✅ Gateway 运行正常"
    task_stage "$TASK_ID" "检查 Gateway" "done"
else
    task_log "$TASK_ID" "ERROR" "❌ Gateway 未运行"
    task_stage "$TASK_ID" "检查 Gateway" "failed"
fi

# 阶段 2: 检查磁盘
task_stage "$TASK_ID" "检查磁盘" "running"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    task_log "$TASK_ID" "INFO" "✅ 磁盘使用：${DISK_USAGE}%"
    task_stage "$TASK_ID" "检查磁盘" "done"
else
    task_log "$TASK_ID" "WARN" "⚠️ 磁盘使用过高：${DISK_USAGE}%"
    task_stage "$TASK_ID" "检查磁盘" "warning"
fi

# 完成
if [ "$ISSUES_COUNT" -eq 0 ]; then
    task_complete "$TASK_ID" "系统健康状态良好"
else
    task_fail "$TASK_ID" "发现 $ISSUES_COUNT 个问题" "validation_error"
fi
```

---

## 📋 AI 任务登记流程

### 方式 1: 使用登记脚本

```bash
./scripts/ai-task-register.sh "撰写文章" "为同事写鼓励文章" "normal"
```

### 方式 2: AI 直接创建

AI 在回复中说明并创建状态文件：

```
📋 任务登记：
- ID: ai_task_20260314_0948_write
- 名称：撰写安慰文章
- 类型：one-time
- 优先级：normal
- 状态：pending

📝 执行中...

✅ 任务完成！
📋 详情:
  - 完成时间：09:48
  - 耗时：45 秒
  - 状态：成功

📄 状态文件：memory/tasks/ai_task_20260314_0948_write.json
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **任务 ID 唯一**：使用时间戳 `task_$(date +%Y%m%d_%H%M%S)`
2. **及时登记**：任务开始前登记，不要事后补
3. **详细日志**：关键决策和操作都要记录
4. **完整反馈**：完成/失败都通知用户
5. **故障分析**：失败时使用 8 类故障类型

### ❌ 避免做法

1. **事后补登记**：失去了追踪意义
2. **只记录成功**：失败也要记录
3. **模糊错误**：错误信息要具体
4. **无反馈**：完成任务不通知
5. **过度追踪**：简单问答不需要登记

---

## 📊 监控方式

### 命令行查询

```bash
# 查看所有任务
task_list

# 查询特定任务
task_status "task_001"

# 查看日志
tail -50 logs/tasks/task_001.log
```

### 监控面板

打开 `docs/task-dashboard.html` 可视化查看

### 查看注册表

```bash
cat memory/task-registry.json | jq '.tasks'
```

---

## 📚 参考文档

- **快速上手**：`docs/QUICKSTART.md`
- **触发标准**：`docs/task-trigger-criteria.md` - 什么任务需要闭环
- **AI 登记**：`docs/ai-task-registration.md` - AI 任务自动登记流程
- **完整框架**：`docs/task-protection.md` - 详细设计文档
- **使用示例**：`docs/task-protection-examples.md` - 更多场景示例

---

## 🔧 故障排查

### 问题：任务失败后如何重试？

```bash
task_retry "task_001" 3 60
```

### 问题：如何查看历史任务？

```bash
ls memory/tasks/*.json | xargs -I {} jq '.name, .status, .completedAt' {}
```

### 问题：如何清理过期任务？

```bash
task_cleanup 30  # 清理 30 天前的任务
```

---

## 📈 统计报告

### 生成周报

```bash
./scripts/weekly-task-report.sh
```

**输出**：`articles/任务周报 -YYYY-Www.md`

**包含**：
- 核心指标（总数、成功率、平均耗时）
- 任务分类统计
- 失败任务分析
- 故障类型分布
- 改进建议

---

**维护者**: 虾球 🦐  
**版本**: 1.0  
**最后更新**: 2026-03-14  
**许可**: MIT（免费开源）

_有任何问题随时提问！_
