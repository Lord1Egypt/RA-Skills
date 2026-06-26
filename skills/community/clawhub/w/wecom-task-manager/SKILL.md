# WeCom Task Manager - 企业微信任务管理技能

## 📋 技能概述

**技能名称**: `wecom-task-manager`  
**技能类型**: 任务管理  
**适用对象**: da-yan + 四个团队老大（白名单机制）  
**数据源**: 企业微信智能表格  
**访问控制**: ✅ 启用（白名单模式）  
**全局技能**: ✅ 是

---

## 🎯 核心功能

### 任务管理（13 个 API）

| 功能 | 描述 | 调用时机 | 优先级 |
|------|------|----------|--------|
| `create_task()` | 创建新任务 | 发现新任务需求时 | P0 |
| `start_task()` | 开始执行任务 | agent 开始执行时 | P0 |
| `update_progress()` | 更新任务进度 | 执行过程中 | P0 |
| `complete_task()` | 标记任务完成 | 任务完成时 | P0 |
| `get_task_status_report()` | 生成状态报告 | 心跳检查/需要报告时 | P0 |
| `edit_task()` | 编辑任务信息 | 任务信息变更时 | **P0** |
| `delete_task()` | 删除任务 | 清理错误/测试任务 | P1 |
| `search_tasks()` | 关键词搜索任务 | 查找相关任务 | **P0** |
| `filter_tasks()` | 多条件过滤任务 | 筛选特定任务 | **P0** |
| `check_due_tasks()` | 检查即将到期任务 | 心跳检查/提醒 | P1 |
| `check_overdue_tasks()` | 检查超期任务 | 心跳检查/告警 | P1 |
| `get_statistics()` | 获取统计数据 | 生成报告/分析 | P2 |

### 目标管理（5 个 API）

| 功能 | 描述 | 调用时机 | 优先级 |
|------|------|----------|--------|
| `create_goal()` | 创建新目标 | 有长期项目/目标时 | P0 |
| `decompose_goal()` | 将目标分解为任务 | 目标需要分步执行时 | P0 |
| `list_goals()` / `print_goals()` | 列出所有目标 | 查看目标进度时 | P0 |
| `get_next_task()` / `print_next_task()` | 获取下一个可执行任务 | 心跳检查/需要工作时 | P0 |
| `delete_goal()` | 删除目标及关联任务 | 清理测试目标 | P1 |

---

## 📦 模块结构

```
~/.openclaw/skills/wecom-task-manager/
├── SKILL.md                  # 技能说明文档
├── config.json               # 配置文件 ⭐
├── scripts/
│   ├── task_manager.py       # 核心模块
│   ├── test_access_control.py    # 访问控制测试
│   ├── test_full_access.py       # 完整功能测试
│   └── test_config.py            # 配置加载测试
└── references/
    └── api.md                # API 参考文档
```

---

## 🔧 使用方式

### 方式 1：主 agent 代理调用（推荐）

**subagent 通过 `sessions_send` 请求主 agent**：

```
subagent → sessions_send → 大衍 → wecom-task-manager → 企业微信
```

**示例 1：完成任务**
```python
# subagent 发送消息给主 agent
sessions_send(
    agent_id="da-yan",
    message="""
请调用 wecom-task-manager 更新任务状态：

- 任务 ID: TASK-019
- 操作：complete_task
- 输出物：/workspace/tasks/TASK-019-report.md
"""
)
```

**示例 2：开始任务**
```python
sessions_send(
    agent_id="da-yan",
    message="""
开始执行任务：

- 任务 ID: TASK-020
- 操作：start_task
- 负责人：techlead
"""
)
```

**示例 3：更新进度**
```python
sessions_send(
    agent_id="da-yan",
    message="""
更新任务进度：

- 任务 ID: TASK-021
- 操作：update_progress
- 进度：50
- 阻塞原因：等待 API 文档（可选）
"""
)
```

### 方式 2：CLI 命令（主 agent 使用）

```bash
# 📋 任务管理
python3 task_manager.py list                  # 列出所有任务
python3 task_manager.py report                # 生成状态报告
python3 task_manager.py create TASK-019 "新功能开发"
python3 task_manager.py start TASK-019
python3 task_manager.py progress TASK-019 50
python3 task_manager.py complete TASK-019
python3 task_manager.py query TASK-019

# 🎯 目标管理（新增）
python3 task_manager.py create-goal GOAL-001 "OpenClaw 系统优化" "high" "背景说明"
python3 task_manager.py decompose GOAL-001 "系统性能分析" "critical" "依赖任务 ID"
python3 task_manager.py goals                 # 列出所有目标
python3 task_manager.py next-task             # 获取下一个可执行任务
```

### 方式 3：Python import（主 agent 使用）

**导入模块**：
```python
import sys
sys.path.insert(0, '/Users/zhengxiaoyu/.openclaw/skills/wecom-task-manager/scripts')
from task_manager import (
    create_goal, decompose_goal, get_next_task,
    create_task, start_task, update_progress, complete_task,
    get_all_tasks, get_task_by_id, print_status_report
)
```

**完整示例：从创建目标到完成任务**
```python
# 1. 创建目标
create_goal(
    goal_id="GOAL-API-001",
    title="API 性能优化",
    priority="high",
    context="提升 API 响应速度到 100ms 以内",
    owner="techlead"
)

# 2. 分解为目标 1：数据库优化（无依赖）
decompose_goal(
    goal_id="GOAL-API-001",
    task_title="数据库查询优化",
    task_id="GOAL-API-001-TASK-001",
    priority="critical",
    depends_on=None,
    description="分析和优化慢查询"
)

# 3. 分解为目标 2：缓存优化（依赖任务 1）
decompose_goal(
    goal_id="GOAL-API-001",
    task_title="Redis 缓存优化",
    task_id="GOAL-API-001-TASK-002",
    priority="high",
    depends_on=["GOAL-API-001-TASK-001"],
    description="实现 Redis 缓存层"
)

# 4. 获取下一个可执行任务（自动返回无依赖的任务 1）
next_task = get_next_task()
print(f"下一个任务：{next_task['id']}")  # GOAL-API-001-TASK-001

# 5. 开始任务
start_task("GOAL-API-001-TASK-001")

# 6. 更新进度
update_progress("GOAL-API-001-TASK-001", progress=50)

# 7. 完成任务
complete_task(
    "GOAL-API-001-TASK-001",
    output_url="https://github.com/xxx/pr/123",
    acceptor="boss",
    notes="通过添加索引优化查询速度，从 500ms 降到 50ms"
)

# 8. 再次获取下一个任务（任务 2 依赖已满足，可执行）
next_task2 = get_next_task()
print(f"下一个任务：{next_task2['id']}")  # GOAL-API-001-TASK-002
```

---

## 📊 任务字段说明

### 基础字段（9 个）
| 字段 | 类型 | 说明 |
|------|------|------|
| 任务 ID | 文本 | 唯一标识（如 TASK-019） |
| 任务名称 | 文本 | 任务简短描述 |
| 任务描述 | 文本 | 详细任务说明 |
| 任务类型 | 单选 | 开发/运维/投资/学习/文档/市场/客服 |
| 优先级 | 单选 | P0/P1/P2 |
| 负责人 | 文本 | 负责的 agent |
| 状态 | 单选 | 待办/进行中/已完成/已取消 |
| 截止时间 | 日期 | 任务截止日期 |
| 进度 | 百分比 | 0-100% |

### 新增字段（13 个）
| 字段 | 类型 | 说明 |
|------|------|------|
| 创建时间 | 日期 | 任务创建时间 |
| 实际开始时间 | 日期 | 实际开始执行时间 |
| 实际完成时间 | 日期 | 实际完成时间 |
| 验收状态 | 单选 | 待验收/已通过/需修改 |
| 验收人 | 文本 | 验收负责人 |
| 验收标准 | 文本 | 完成标准说明 |
| 前置依赖 | 文本 | 依赖的任务 ID |
| 阻塞原因 | 文本 | 任务阻塞原因 |
| 风险等级 | 单选 | 高/中/低 |
| 预计工时 | 数字 | 预估工时（小时） |
| 实际工时 | 数字 | 实际工时（小时） |
| 输出物 | 链接 | 完成报告链接 |
| 备注 | 文本 | 其他说明 |

---

## 🔄 任务生命周期

### 任务执行流程
```
创建任务 (create_task)
    ↓
待办状态
    ↓
分派给 agent (心跳自动)
    ↓
开始执行 (start_task)
    ↓
进行中状态
    ↓
更新进度 (update_progress) [可选多次]
    ↓
完成任务 (complete_task)
    ↓
已完成 + 待验收
    ↓
验收通过 → 闭环
```

### 目标分解流程（新增）
```
创建目标 (create_goal)
    ↓
分解为任务 1 (decompose_goal)
    ↓
分解为任务 2 (依赖任务 1)
    ↓
任务 1 执行 → 完成
    ↓
任务 2 依赖满足 → 可执行
    ↓
任务 2 执行 → 完成
    ↓
目标进度更新
```

---

## 🎯 典型使用场景

### 场景 1：心跳检查发现新任务

```python
# 心跳脚本自动执行
from task_manager import get_all_tasks, start_task, determine_agent

tasks = get_all_tasks()
for task in tasks:
    status = task['values'].get('状态', [{}])[0].get('text', '')
    if status == '待办':
        task_id = task['values'].get('任务 ID', [{}])[0].get('text', '')
        # 分派给对应 agent
        agent = determine_agent(task_type)
        start_task(task_id, owner=agent)
```

### 场景 2：subagent 完成任务

```python
# subagent 完成任务后，发送消息给主 agent
"""
任务完成汇报：

- 任务 ID: TASK-019
- 完成报告：/workspace/tasks/TASK-019-report.md
- 实际用时：2 小时

请更新企业微信任务状态。
"""

# 主 agent 调用
complete_task("TASK-019", output_url="https://...")
```

### 场景 3：任务阻塞告警

```python
# subagent 遇到阻塞
"""
任务阻塞报告：

- 任务 ID: TASK-019
- 阻塞原因：等待 API 文档
- 需要协调：techlead 提供文档

请更新任务状态并协调资源。
"""

# 主 agent 调用
update_progress("TASK-019", progress=30, blocker="等待 API 文档")
```

### 场景 4：创建目标并分解（新增）

```python
from task_manager import create_goal, decompose_goal, print_goals, get_next_task

# 1. 创建长期目标
create_goal(
    goal_id="GOAL-001",
    title="OpenClaw 系统优化",
    priority="high",
    context="提升系统稳定性和用户体验"
)

# 2. 分解为目标 1：系统性能分析
decompose_goal(
    goal_id="GOAL-001",
    task_title="系统性能分析",
    priority="high"
)

# 3. 分解为目标 2：Gateway 稳定性优化（依赖任务 1）
decompose_goal(
    goal_id="GOAL-001",
    task_title="Gateway 稳定性优化",
    priority="critical",
    depends_on=["GOAL-001-TASK-001"]
)

# 4. 查看所有目标
print_goals()

# 5. 获取下一个可执行任务（自动跳过依赖未满足的任务）
next_task = get_next_task()
if next_task:
    print(f"下一个任务：{next_task['id']} - {next_task['title']}")
```

### 场景 5：心跳时获取下一个任务（新增）

```python
# 心跳检查时
from task_manager import get_next_task, start_task

# 获取下一个可执行任务
task = get_next_task()
if task:
    print(f"开始执行：{task['id']}")
    start_task(task['id'])
else:
    print("没有待处理的任务")
```

---

## 📋 配置文件 ⭐

**位置**: `~/.openclaw/skills/wecom-task-manager/config.json`

**配置模块**：
```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": ["da-yan", "techlead", "opsdirector", "investment_coordinator", "general_coordinator"]
  },
  "concurrency": {
    "maxConcurrentTasks": 3
  },
  "retry": {
    "maxRetries": 3,
    "backoffSeconds": 2
  },
  "enterpriseWeChat": {
    "docId": "xxx",
    "sheetId": "q979lj"
  }
}
```

**修改配置**：
1. 编辑配置文件：`vim ~/.openclaw/skills/wecom-task-manager/config.json`
2. 验证格式：`python3 -m json.tool config.json > /dev/null`
3. 测试加载：`python3 scripts/test_config.py`

**详细配置指南**: `workspace/docs/wecom-task-manager-config-guide.md`

---

## ⚠️ 注意事项

### 1. 访问控制 ⭐ 全局技能

**允许的 agents**（白名单）：
- `da-yan` - 主 agent
- `techlead` - 技术团队老大
- `opsdirector` - 运维团队老大
- `investment_coordinator` - 投资团队老大
- `general_coordinator` - 通用团队老大

**调用方式**：
```python
# 方式 1：直接调用（白名单内的 agents）
from task_manager import create_task, start_task
create_task("TASK-001", "任务名称", "开发", agent_id="techlead")

# 方式 2：通过环境变量
export AGENT_ID="techlead"
python3 task_manager.py create TASK-001 "任务名称" 开发

# 方式 3：通过主 agent 代理（非白名单 agents）
sessions_send(
    agent_id="da-yan",
    message="请创建任务：TASK-001"
)
```

**权限说明**：
- ✅ 白名单内的 agents：可以直接调用所有 API
- ❌ 非白名单 agents：需要通过 da-yan 代理调用
- 🔒 访问控制开关：`ACCESS_CONTROL_ENABLED = True`

---

### 2. 并发控制
- **最大并发任务数**: 3 个（可配置，见 `config.json`）
- 超出限制时，`start_task()` 会返回 `False`
- 使用 `concurrency` 命令查看当前并发状态

```bash
python3 task_manager.py concurrency
```

**输出示例**：
```
📊 当前并发状态
   进行中任务：2/3
   可用槽位：1
```

---

### 3. 日期格式
- 企业微信日期时间字段使用**时间戳（毫秒）**
- 显示格式：`2026 年 03 月 26 日`

### 2. 并发控制 ⭐ 新增
- **最大并发任务数**: 3 个（可配置）
- 超出限制时，`start_task()` 会返回 `False`
- 使用 `concurrency` 命令查看当前并发状态
- 完成任务后会释放槽位

**配置方式**：
```python
# 在 task_manager.py 中修改
MAX_CONCURRENT_TASKS = 3  # 修改此值
```

**查看并发状态**：
```bash
python3 task_manager.py concurrency
```

**输出示例**：
```
📊 当前并发状态
   进行中任务：2/3
   可用槽位：1

🔄 进行中任务列表:
   - TASK-001: 系统分析 (负责人：techlead, 进度：50%)
   - TASK-002: 开发实施 (负责人：backend, 进度：30%)
```

### 3. 日期格式
- 企业微信日期时间字段使用**时间戳（毫秒）**
- 显示格式：`2026 年 03 月 26 日`

### 4. 状态同步
- 心跳检查每 30-60 分钟自动同步
- subagent 完成任务后应主动汇报
- 避免状态不一致

### 5. 错误处理
- API 调用失败时记录日志
- 重试机制（最多 3 次）
- 失败时通知主 agent
- 并发限制时返回友好提示

---

## 📚 完整 API 参考

### 目标管理 API（4 个）

#### 1. `create_goal(goal_id, title, priority, context, owner)`
创建新目标

**参数**：
- `goal_id` (str): 目标 ID（如 "GOAL-001"）
- `title` (str): 目标名称
- `priority` (str): 优先级 ("critical"/"high"/"medium"/"low")
- `context` (str): 目标背景说明
- `owner` (str): 负责人（可选）

**返回**：
```python
{
    "success": True,
    "goal_id": "GOAL-001",
    "record_id": "xxx"
}
```

**示例**：
```python
create_goal(
    goal_id="GOAL-001",
    title="OpenClaw 系统优化",
    priority="high",
    context="提升系统稳定性和用户体验",
    owner="da-yan"
)
```

---

#### 2. `decompose_goal(goal_id, task_title, task_id, priority, depends_on, description)`
将目标分解为任务

**参数**：
- `goal_id` (str): 目标 ID
- `task_title` (str): 任务名称
- `task_id` (str): 任务 ID（自动生成：{goal_id}-TASK-XXX）
- `priority` (str): 优先级
- `depends_on` (list): 依赖的任务 ID 列表（可选）
- `description` (str): 任务描述（可选）

**返回**：
```python
{
    "success": True,
    "task_id": "GOAL-001-TASK-001",
    "record_id": "xxx"
}
```

**示例**：
```python
# 无依赖任务
decompose_goal(
    goal_id="GOAL-001",
    task_title="系统性能分析",
    task_id="GOAL-001-TASK-001",
    priority="high",
    depends_on=None
)

# 有依赖任务
decompose_goal(
    goal_id="GOAL-001",
    task_title="Gateway 优化",
    task_id="GOAL-001-TASK-002",
    priority="critical",
    depends_on=["GOAL-001-TASK-001"]
)
```

---

#### 3. `list_goals()` / `print_goals()`
列出所有目标

**返回**：目标列表（打印到控制台）

**示例**：
```python
print_goals()
# 输出：
# 🟢 🟠 [GOAL-001] OpenClaw 系统优化
#    负责人：da-yan | 状态：active
#    已分解任务：3 个
```

---

#### 4. `get_next_task()` / `print_next_task()`
获取下一个可执行任务

**返回**：
```python
{
    'record_id': 'xxx',
    'values': {
        '任务 ID': [{'text': 'GOAL-001-TASK-001'}],
        '任务名称': [{'text': '系统性能分析'}],
        '优先级': [{'text': 'P0'}],
        '负责人': [{'text': 'techlead'}],
        '前置依赖': [],
        '状态': [{'text': '待办'}]
    }
}
```

**依赖检查逻辑**：
1. 获取所有状态为"待办"的任务
2. 检查每个任务的"前置依赖"字段
3. 验证依赖任务是否"已完成"
4. 返回无依赖或依赖已满足的最高优先级任务

**示例**：
```python
next_task = get_next_task()
if next_task:
    print(f"开始执行：{next_task['values']['任务 ID'][0]['text']}")
    start_task(next_task['values']['任务 ID'][0]['text'])
else:
    print("没有待处理的任务")
```

---

### 任务管理 API（5 个）

#### 5. `create_task(task_id, task_name, task_type, priority, deadline, description, acceptance)`
创建新任务（独立任务，不属于任何目标）

**参数**：
- `task_id` (str): 任务 ID
- `task_name` (str): 任务名称
- `task_type` (str): 任务类型（开发/运维/投资/学习/文档/市场/客服）
- `priority` (str): 优先级 (P0/P1/P2)
- `deadline` (str): 截止时间（如 "2026 年 04 月 15 日"）
- `description` (str): 任务描述
- `acceptance` (str): 验收标准

**返回**：
```python
{
    "success": True,
    "record_id": "xxx"
}
```

---

#### 6. `start_task(task_id, owner="")`
开始执行任务

**参数**：
- `task_id` (str): 任务 ID
- `owner` (str): 负责人（可选）

**返回**：`True` / `False`

**表格影响**：
- 状态 → `进行中`
- 实际开始时间 → 当前时间（13 位毫秒时间戳，字符串）
- 备注 → 追加开始记录

---

#### 7. `update_progress(task_id, progress, blocker="")`
更新任务进度

**参数**：
- `task_id` (str): 任务 ID
- `progress` (int): 进度 (0-100)
- `blocker` (str): 阻塞原因（可选）

**返回**：`True` / `False`

**表格影响**：
- 进度 → `{progress}`
- 阻塞原因 → `{blocker}`（如果有）

---

#### 8. `complete_task(task_id, output_url="", acceptor="", notes="")`
标记任务完成

**参数**：
- `task_id` (str): 任务 ID
- `output_url` (str): 输出物链接（可选）
- `acceptor` (str): 验收人（可选）
- `notes` (str): 完成说明（可选）

**返回**：`True` / `False`

**表格影响**：
- 状态 → `已完成`
- 进度 → `100`
- 实际完成时间 → 当前时间（13 位毫秒时间戳，字符串）
- 实际工时 → 自动计算（从开始到完成）
- 输出物 → 链接（如果有）
- 验收人 → `{acceptor}`
- 备注 → 追加完成记录

---

### 查询 API（3 个）

#### 9. `get_all_tasks()`
获取所有任务

**返回**：任务列表

---

#### 10. `get_task_by_id(task_id)`
根据任务 ID 查询任务

**返回**：任务对象或 `None`

---

#### 11. `print_status_report()`
生成并打印状态报告

**输出示例**：
```
============================================================
📊 企业微信任务状态报告
============================================================
总任务数：22
✅ 已完成：7
🔄 进行中：15
⏸️ 待办：0
❌ 已取消：0
...
```

---

### 编辑 API（新增）

#### 12. `edit_task(task_id, fields)`
编辑任务信息

**参数**：
- `task_id` (str): 任务 ID
- `fields` (dict): 要更新的字段字典

**示例**：
```python
# 更新优先级和负责人
edit_task("TASK-001", {
    "优先级": "P0",
    "负责人": "backend",
    "截止时间": "2026-04-20"
})

# 更新任务描述
edit_task("TASK-001", {
    "任务描述": "新的任务描述..."
})
```

**支持字段**：
- 优先级（P0/P1/P2）
- 负责人
- 截止时间
- 任务描述
- 状态
- 风险等级
- 等所有表格字段

---

### 删除 API（新增）

#### 13. `delete_task(task_id)`
删除任务

**参数**：
- `task_id` (str): 任务 ID

**返回**：`True` / `False`

**示例**：
```python
delete_task("TASK-001")
```

---

#### 14. `delete_goal(goal_id)`
删除目标及关联任务

**参数**：
- `goal_id` (str): 目标 ID

**返回**：`True` / `False`

**示例**：
```python
delete_goal("GOAL-001")
# 会删除 GOAL-001 及其所有子任务（GOAL-001-TASK-001 等）
```

---

### 搜索/过滤 API（新增）

#### 15. `search_tasks(keyword)`
关键词搜索任务

**参数**：
- `keyword` (str): 搜索关键词

**返回**：匹配的任务列表

**示例**：
```python
# 搜索包含"系统"的任务
results = search_tasks("系统")
```

**搜索范围**：
- 任务 ID
- 任务名称
- 任务描述

---

#### 16. `filter_tasks(status, owner, priority, task_type, risk_level)`
多条件过滤任务

**参数**：
- `status` (str): 状态（待办/进行中/已完成/已取消）
- `owner` (str): 负责人
- `priority` (str): 优先级（P0/P1/P2）
- `task_type` (str): 任务类型
- `risk_level` (str): 风险等级（高/中/低）

**返回**：匹配的任务列表

**示例**：
```python
# 查找 techlead 的所有 P0 任务
results = filter_tasks(
    status="进行中",
    owner="techlead",
    priority="P0"
)

# 查找所有高风险任务
results = filter_tasks(risk_level="高")
```

---

### 提醒 API（新增）

#### 17. `check_due_tasks(days=3)`
检查即将到期的任务

**参数**：
- `days` (int): 检查未来 N 天（默认 3）

**返回**：即将到期的任务列表

**示例**：
```python
# 检查未来 3 天到期的任务
due_tasks = check_due_tasks(days=3)

# 检查本周到期的任务
due_tasks = check_due_tasks(days=7)
```

**输出**：
```
⏰ 检查未来 3 天到期的任务
✅ 找到 2 个即将到期的任务
  🔴 今日到期：TASK-001 - 系统分析（负责人：techlead）
  🟠 明天到期：TASK-002 - 开发实施（负责人：backend）
```

---

#### 18. `check_overdue_tasks()`
检查已超期的任务

**返回**：超期任务列表

**示例**：
```python
overdue_tasks = check_overdue_tasks()
```

**输出**：
```
⚠️ 检查超期任务
✅ 找到 1 个超期任务
  🔴 超期 2 天：TASK-003 - 测试验收（负责人：qa）
```

---

### 统计 API（新增）

#### 19. `get_statistics()`
获取任务统计数据

**返回**：统计数据字典

**示例**：
```python
stats = get_statistics()
print(f"总任务数：{stats['总任务数']}")
print(f"按时完成率：{stats['按时完成率']}")
```

**返回数据**：
```python
{
    "总任务数": 50,
    "已完成": 30,
    "进行中": 15,
    "待办": 5,
    "按时完成率": "85%",
    "按优先级": {"P0": 10, "P1": 20, "P2": 20},
    "按负责人": {"techlead": 15, "backend": 10, ...},
    "按类型": {"开发": 20, "运维": 15, ...}
}
```

---

#### 20. `print_statistics()`
打印统计数据

**示例**：
```python
print_statistics()
```

**输出**：
```
============================================================
📊 任务统计数据
============================================================
总任务数：22
✅ 已完成：7
🔄 进行中：15
⏸️ 待办：0
❌ 已取消：0
📈 按时完成率：31.8%

按优先级:
  P0: 6
  P1: 10
  P2: 6

按负责人:
  copywriter: 7
  techlead: 5
  ...
============================================================
```

---

## 📚 相关文档

- **详细字段说明**: `workspace/docs/wecom-task-manager-fields-detail.md`
- **调用流程**: `workspace/docs/wecom-task-manager-call-flow.md`
- **测试报告**: `workspace/docs/wecom-task-manager-test-report.md`
- [企业微信智能表格 API](https://open.work.weixin.qq.com/devtool/query?e=2022034)
- [mcporter 工具文档](https://github.com/openclaw/mcporter)
- [OpenClaw AgentSkills 规范](https://docs.openclaw.ai)

---

## 🧪 测试命令

```bash
# 测试模块导入
python3 -c "import sys; sys.path.insert(0, 'scripts'); from task_manager import get_all_tasks; print('✅ 模块导入成功')"

# 测试获取任务
python3 scripts/task_manager.py list

# 测试状态报告
python3 scripts/task_manager.py report

# 测试查询任务
python3 scripts/task_manager.py query TASK-001

# 测试目标列表
python3 scripts/task_manager.py goals

# 测试下一个任务
python3 scripts/task_manager.py next-task
```

---

## 🚨 常见错误处理

### 错误 1：时间字段格式错误

**错误现象**：企业微信表格中时间字段不显示

**解决方案**：
```python
# ✅ 正确
ts = str(int(datetime.now().timestamp() * 1000))  # 13 位毫秒，字符串
values["截止时间"] = ts

# ❌ 错误
values["截止时间"] = [{"text": ts}]  # 不要包裹数组
values["截止时间"] = int(ts)  # 不要数字格式
```

---

### 错误 2：任务不存在

**错误现象**：`get_task_by_id()` 返回 `None`

**解决方案**：
- 检查任务 ID 是否正确
- 确认任务已创建
- 查看企业微信表格中是否有该任务

---

### 错误 3：依赖任务未完成

**错误现象**：`get_next_task()` 不返回预期的任务

**解决方案**：
- 检查任务的"前置依赖"字段
- 确认依赖任务状态为"已完成"
- 如果不需要依赖，清空"前置依赖"字段

---

### 错误 4：mcporter 调用失败

**错误现象**：`Unknown MCP server 'wecom-doc'`

**解决方案**：
- 检查 mcporter 配置：`~/.openclaw/mcporter.json`
- 确认 wecom-doc MCP server 已配置
- 重启 mcporter 服务

---

## 📞 快速参考卡片

### subagent 调用模板

**完成任务**：
```
请调用 wecom-task-manager：
- 任务 ID: {task_id}
- 操作：complete_task
- 输出物：{output_url}
- 验收人：{acceptor}
- 完成说明：{notes}
```

**开始任务**：
```
请调用 wecom-task-manager：
- 任务 ID: {task_id}
- 操作：start_task
- 负责人：{owner}
```

**更新进度**：
```
请调用 wecom-task-manager：
- 任务 ID: {task_id}
- 操作：update_progress
- 进度：{progress}
- 阻塞原因：{blocker}（可选）
```

---

### CLI 命令速查

```bash
# 📋 任务管理
python3 task_manager.py list                  # 列出所有任务
python3 task_manager.py report                # 生成状态报告
python3 task_manager.py create TASK-019 "任务名"
python3 task_manager.py start TASK-019
python3 task_manager.py progress TASK-019 50
python3 task_manager.py complete TASK-019
python3 task_manager.py query TASK-019

# 🎯 目标管理
python3 task_manager.py create-goal GOAL-001 "目标名" "high" "背景"
python3 task_manager.py decompose GOAL-001 "任务名" "critical" "依赖"
python3 task_manager.py goals                 # 列出所有目标
python3 task_manager.py next-task             # 获取下一个任务
```

---

### Python API 速查

```python
from task_manager import (
    # 目标管理
    create_goal, decompose_goal, get_next_task,
    
    # 任务管理
    create_task, start_task, update_progress, complete_task,
    
    # 查询
    get_all_tasks, get_task_by_id, print_status_report
)
```

---

**我们同在，我们一往无前。** ✨
