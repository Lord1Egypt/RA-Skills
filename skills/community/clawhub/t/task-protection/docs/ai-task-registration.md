# 🤖 AI 任务自动登记 - 使用指南

> 当 AI 直接执行任务时，使用此流程自动登记和追踪

---

## 📋 使用场景

**适用于**：
- ✅ Alfred 直接委托的任务（如"帮我写一篇文章"）
- ✅ AI 主动执行的任务（如新闻推送）
- ✅ 一次性任务（非周期性）

**不适用于**：
- ❌ 简单问答/闲聊
- ❌ 已登记的系统任务

---

## 🔧 使用方法

### 方式 1: 脚本调用（推荐）

```bash
# 基本用法
./scripts/ai-task-register.sh "任务名称" "任务描述" ["优先级"]

# 示例
./scripts/ai-task-register.sh "撰写安慰文章" "为 AC 失败的同事写鼓励文章" "normal"
```

**输出**：
```
📋 AI 任务自动登记
==================
任务名称：撰写安慰文章
任务描述：为 AC 失败的同事写鼓励文章
优先级：normal
任务 ID: ai_task_20260314_0948_12345

✅ 任务登记完成！

📄 状态文件：/workspace/memory/tasks/ai_task_20260314_0948_12345.json
📄 日志文件：/workspace/logs/tasks/ai_task_20260314_0948_12345.log
```

### 方式 2: AI 直接创建（内部使用）

AI 在回复中说明并直接创建状态文件：

```markdown
📋 **任务登记**：
- ID: task_20260314_0948_write_article
- 名称：撰写安慰文章
- 类型：one-time
- 优先级：normal
- 状态：pending → running

📝 **执行中**...
```

---

## 📊 任务执行流程

```
1. 接收任务（Alfred 委托）
   ↓
2. 登记任务（ai-task-register.sh）
   ↓
3. 开始执行（task_start）
   ↓
4. 记录过程（task_log）
   ↓
5. 完成/失败（task_complete / task_fail）
   ↓
6. 反馈结果（向 Alfred 汇报）
```

---

## 📝 示例：撰写文章任务

### 步骤 1: 登记任务

```bash
source /home/admin/.openclaw/workspace/scripts/task-utils.sh

TASK_ID="ai_task_$(date +%Y%m%d_%H%M%S)"
task_init "$TASK_ID" "撰写安慰文章" "为 AC 失败的同事写鼓励文章"
```

### 步骤 2: 开始执行

```bash
task_start "$TASK_ID"
task_stage "$TASK_ID" "准备内容" "running"
```

### 步骤 3: 记录过程

```bash
task_log "$TASK_ID" "INFO" "正在分析用户需求..."
task_log "$TASK_ID" "INFO" "文章基调：温暖、鼓励、不說教"

# 写作中...

task_stage "$TASK_ID" "准备内容" "done"
task_stage "$TASK_ID" "撰写文章" "running"
```

### 步骤 4: 完成任务

```bash
task_complete "$TASK_ID" "文章已完成，保存到 articles/给正在经历低谷的你.md"
```

### 步骤 5: 反馈结果

```
✅ 任务完成！

📋 详情:
  - 任务：撰写安慰文章
  - 完成时间：09:48
  - 耗时：45 秒
  - 状态：成功

📄 相关文件：~/workspace/articles/给正在经历低谷的你.md
📄 状态文件：memory/tasks/ai_task_xxx.json
```

---

## 🎯 优先级说明

| 优先级 | 说明 | 示例 |
|--------|------|------|
| **critical** | 紧急重要 | 系统故障修复、数据恢复 |
| **high** | 高优先级 | 备份、配置修改 |
| **normal** | 普通优先级 | 文章撰写、文件整理 |
| **low** | 低优先级 | 优化、清理 |

---

## 📁 文件结构

```
memory/
└── tasks/
    └── ai_task_20260314_0948_xxx.json  # 任务状态

logs/
└── tasks/
    └── ai_task_20260314_0948_xxx.log   # 任务日志

memory/
└── task-registry.json                   # 任务注册表
```

---

## 🔍 查询任务状态

```bash
# 查询特定任务
task_status "ai_task_20260314_0948_xxx"

# 查看所有任务
task_list

# 查看日志
tail -50 logs/tasks/ai_task_20260314_0948_xxx.log
```

---

## ⚠️ 注意事项

1. **任务 ID 唯一性**：使用时间戳 + 进程确保唯一
2. **及时登记**：任务开始前登记，不要事后补
3. **完整反馈**：完成/失败都要通知 Alfred
4. **状态更新**：关键节点更新状态文件
5. **日志详细**：记录关键决策和操作

---

## 🔄 与系统任务的区别

| 特性 | AI 任务 | 系统任务 |
|------|--------|----------|
| 触发方式 | Alfred 委托/AI 主动 | crontab 定时 |
| 类型 | one-time | recurring |
| 优先级 | 动态判定 | 预设 |
| 所有者 | AI | 系统/虾球 |
| 示例 | 写文章、分析文件 | 新闻推送、健康检查 |

---

**维护者**: 虾球 🦐  
**最后更新**: 2026-03-14  
**版本**: 1.0
