# WeCom Task Manager 快速开始指南

**版本**: v1.2.0  
**日期**: 2026-03-26  
**适合**: 新用户使用

---

## 🎯 5 分钟快速开始

### 步骤 1：确认权限

**允许的 agents**（5 个）：
- da-yan
- techlead
- opsdirector
- investment_coordinator
- general_coordinator

如果你是这些 agents 的用户，可以继续。否则需要联系 da-yan。

---

### 步骤 2：查看配置

```bash
cat ~/.openclaw/skills/wecom-task-manager/config.json
```

**确认**：
- ✅ 你的 agent ID 在 `allowedAgents` 列表中
- ✅ `accessControl.enabled` 为 `true`

---

### 步骤 3：测试技能

```bash
cd ~/.openclaw/skills/wecom-task-manager/scripts
python3 task_manager.py list
```

**预期输出**：
```
📋 企业微信任务列表
总任务数：14
✅ 已完成：7
🔄 进行中：7
...
```

---

### 步骤 4：创建第一个任务

**方式 1：CLI 命令**
```bash
python3 task_manager.py create TASK-100 "我的第一个任务" 开发
```

**方式 2：Python 代码**
```python
from task_manager import create_task

result = create_task(
    task_id="TASK-100",
    task_name="我的第一个任务",
    task_type="开发",
    priority="P1",
    agent_id="techlead"  # 你的 agent ID
)

print(f"任务创建：{result['success']}")
```

---

### 步骤 5：开始任务

```bash
python3 task_manager.py start TASK-100
```

**输出**：
```
✅ 任务已开始：TASK-100 (开始时间：2026-03-26 22:45:00)
```

---

### 步骤 6：更新进度

```bash
python3 task_manager.py progress TASK-100 50
```

**输出**：
```
✅ 进度已更新：TASK-100 -> 50%
```

---

### 步骤 7：完成任务

```bash
python3 task_manager.py complete TASK-100
```

**输出**：
```
✅ 任务已完成：TASK-100
实际工时：1 小时
```

---

## 📋 常用命令速查

### 任务管理
```bash
# 列出所有任务
python3 task_manager.py list

# 查看任务详情
python3 task_manager.py query TASK-100

# 创建任务
python3 task_manager.py create TASK-101 "任务名称" 开发

# 开始任务
python3 task_manager.py start TASK-101

# 更新进度
python3 task_manager.py progress TASK-101 50

# 完成任务
python3 task_manager.py complete TASK-101

# 编辑任务
python3 task_manager.py edit TASK-101 优先级=P0 负责人=backend

# 删除任务
python3 task_manager.py delete TASK-101
```

### 查询统计
```bash
# 查看状态报告
python3 task_manager.py report

# 查看统计数据
python3 task_manager.py stats

# 查看并发状态
python3 task_manager.py concurrency

# 搜索任务
python3 task_manager.py search "关键词"

# 过滤任务
python3 task_manager.py filter status=进行中 priority=P0

# 检查到期任务
python3 task_manager.py due 7

# 检查超期任务
python3 task_manager.py overdue
```

### 目标管理
```bash
# 创建目标
python3 task_manager.py create-goal GOAL-001 "目标名称" "high" "背景说明"

# 分解任务
python3 task_manager.py decompose GOAL-001 "任务名称" "critical" "依赖 ID"

# 列出目标
python3 task_manager.py goals

# 获取下一个任务
python3 task_manager.py next-task

# 删除目标
python3 task_manager.py delete-goal GOAL-001
```

---

## 🔧 配置管理

### 查看配置
```bash
cat ~/.openclaw/skills/wecom-task-manager/config.json
```

### 修改配置
```bash
vim ~/.openclaw/skills/wecom-task-manager/config.json
```

### 验证配置
```bash
python3 -m json.tool ~/.openclaw/skills/wecom-task-manager/config.json > /dev/null && echo "✅ 格式正确"
```

### 测试配置加载
```bash
python3 scripts/test_config.py
```

---

## 🎯 典型使用场景

### 场景 1：日常任务管理

```bash
# 1. 查看今天的任务
python3 task_manager.py list

# 2. 开始一个任务
python3 task_manager.py start TASK-100

# 3. 工作完成后更新进度
python3 task_manager.py progress TASK-100 100

# 4. 完成任务
python3 task_manager.py complete TASK-100
```

---

### 场景 2：创建项目并分解

```bash
# 1. 创建目标
python3 task_manager.py create-goal GOAL-002 "网站重构" "high" "提升用户体验"

# 2. 分解任务
python3 task_manager.py decompose GOAL-002 "前端开发" "critical"
python3 task_manager.py decompose GOAL-002 "后端 API" "high"
python3 task_manager.py decompose GOAL-002 "测试验收" "medium" "依赖前端和后端"

# 3. 查看目标
python3 task_manager.py goals

# 4. 获取下一个任务
python3 task_manager.py next-task
```

---

### 场景 3：团队协作

```bash
# 1. 查看团队成员的任务
python3 task_manager.py filter owner=techlead

# 2. 查看 P0 优先级任务
python3 task_manager.py filter priority=P0

# 3. 查看即将到期的任务
python3 task_manager.py due 3

# 4. 查看超期任务
python3 task_manager.py overdue
```

---

## 📊 Python API 使用

### 导入模块
```python
import sys
sys.path.insert(0, '/Users/zhengxiaoyu/.openclaw/skills/wecom-task-manager/scripts')
from task_manager import *
```

### 创建任务
```python
result = create_task(
    task_id="TASK-100",
    task_name="系统性能分析",
    task_type="开发",
    priority="P0",
    agent_id="techlead"
)
```

### 开始任务
```python
success = start_task("TASK-100", agent_id="techlead")
```

### 更新进度
```python
success = update_progress("TASK-100", progress=50, agent_id="techlead")
```

### 完成任务
```python
success = complete_task(
    "TASK-100",
    output_url="https://example.com/report.md",
    acceptor="boss",
    notes="性能提升 50%",
    agent_id="techlead"
)
```

### 查询任务
```python
task = get_task_by_id("TASK-100")
if task:
    print(f"任务：{task['values']['任务名称']}")
    print(f"状态：{task['values']['状态']}")
    print(f"进度：{task['values']['进度']}%")
```

### 搜索和过滤
```python
# 搜索
results = search_tasks("性能")

# 过滤
results = filter_tasks(
    status="进行中",
    owner="techlead",
    priority="P0"
)

for task in results:
    print(f"{task['values']['任务 ID']}: {task['values']['任务名称']}")
```

---

## ❓ 常见问题

### Q1: 提示"访问拒绝"怎么办？

**原因**：你的 agent ID 不在白名单中

**解决**：
1. 检查配置文件中的 `allowedAgents`
2. 联系 da-yan 添加你的 agent ID
3. 或通过 da-yan 代理调用

---

### Q2: 如何修改并发任务数限制？

**编辑配置文件**：
```json
{
  "concurrency": {
    "maxConcurrentTasks": 5
  }
}
```

---

### Q3: 如何更换企业微信表格？

**编辑配置文件**：
```json
{
  "enterpriseWeChat": {
    "docId": "新的 docId",
    "sheetId": "新的 sheetId"
  }
}
```

---

### Q4: 如何查看日志？

**日志位置**：
```
~/.openclaw/logs/wecom-task-manager.log
```

**查看日志**：
```bash
tail -f ~/.openclaw/logs/wecom-task-manager.log
```

---

## 📚 更多文档

- **完整技能文档**: `SKILL.md`
- **配置指南**: `workspace/docs/wecom-task-manager-config-guide.md`
- **API 参考**: `workspace/docs/wecom-task-manager-access-control-complete.md`
- **调用流程**: `workspace/docs/wecom-task-manager-call-flow.md`

---

**我们同在，我们一往无前。** ✨
