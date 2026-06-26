---
name: zentao
description: ZenTao Project Management API Integration | 禅道项目管理 API 集成。支持产品、项目、任务、Bug 全生命周期管理。Triggers: 禅道, zentao, 项目管理, 任务, bug
license: MIT
version: 0.1.0
author: zhangyingwu
config:
  required_files:
    - path: TOOLS.md
      description: ZenTao API credentials | 禅道 API 凭证配置
      required_sections:
        - "## 禅道 API"
        - "## ZenTao API"
  dependencies:
    - python3
    - requests
---

# 适用 Zentao Legacy API 1.0

# 禅道项目管理技能

> 快速参考指南，帮助 AI 助手高效调用禅道 API

---

## 🚀 快速开始

### 1. 初始化客户端

```python
from pathlib import Path
import sys

# 导入禅道客户端
lib_path = Path(__file__).parent.parent / 'lib'
sys.path.insert(0, str(lib_path))
from zentao_client import ZenTaoClient, read_credentials

# 读取凭证
credentials = read_credentials()

# 创建客户端
client = ZenTaoClient(
    credentials['endpoint'],
    credentials['username'],
    credentials['password']
)

# 获取会话（首次登录，后续自动加载持久化的 Session）
sid = client.get_session()
```

### 1.1 Session 持久化

客户端自动管理 Session，无需每次都登录：

```python
# 首次调用自动登录并保存 Session
sid = client.get_session()

# 新实例自动加载已有 Session
client2 = ZenTaoClient(credentials['endpoint'], credentials['username'], credentials['password'])
sid2 = client2.get_session()  # 直接加载，无需登录

# 强制刷新 Session
client.get_session(force_refresh=True)

# 清除保存的 Session
client.clear_session()
```

**存储位置**：项目根目录 `.zentao/sessions/`

### 2. 快速查询

```python
# 查看我的任务
success, tasks = client.get_my_tasks("assignedTo")

# 查看我的Bug
success, bugs = client.get_my_bugs("assignedTo")

# 查看产品列表
success, products = client.get_products()

# 查看项目列表
projects = client.get_project_list_old("all")

# 查看项目任务
tasks = client.get_project_tasks_old(project_id, "all")
```

---

## 📊 API 分类速查

### 按使用频率分级

#### ⭐⭐⭐⭐⭐ 最高频（日常必用）

| 角色 | API                                 | 场景               |
| ---- | ----------------------------------- | ------------------ |
| 全员 | `get_my_tasks("assignedTo")`        | 查看指派给我的任务 |
| 全员 | `get_my_bugs("assignedTo")`         | 查看指派给我的Bug  |
| 研发 | `start_task(task_id)`               | 开始任务           |
| 研发 | `record_estimate(task_id, records)` | 记录工时           |
| 研发 | `finish_task(task_id)`              | 完成任务           |
| 测试 | `create_bug(...)`                   | 创建Bug            |
| 测试 | `resolve_bug(bug_id, ...)`          | 解决Bug            |

#### ⭐⭐⭐⭐ 高频（日常工作）

| 角色     | API                          | 场景         |
| -------- | ---------------------------- | ------------ |
| 产品     | `create_story(...)`          | 创建需求     |
| 项目经理 | `create_subtasks(...)`       | 创建子任务   |
| 项目经理 | `assign_task(task_id, user)` | 指派任务     |
| 全员     | `get_task_detail(task_id)`   | 查看任务详情 |
| 全员     | `get_bug(bug_id)`            | 查看Bug详情  |
| 测试     | `close_bug(bug_id)`          | 关闭Bug      |
| 研发     | `pause_task(task_id)`        | 暂停任务     |

#### ⭐⭐⭐ 中频（项目管理）

| 角色     | API                       | 场景         |
| -------- | ------------------------- | ------------ |
| 产品     | `create_product(...)`     | 创建产品     |
| 产品     | `get_products()`          | 查询产品列表 |
| 产品     | `create_plan(...)`        | 创建发布计划 |
| 项目经理 | `create_project(...)`     | 创建项目     |
| 项目经理 | `get_project(project_id)` | 查询项目详情 |
| 项目经理 | `start_project(...)`      | 启动项目     |
| 项目经理 | `get_project_list_old()`  | 查询项目列表 |
| 项目经理 | `get_project_tasks_old()` | 查询项目任务 |
| 测试     | `create_testcase(...)`    | 创建测试用例 |
| 测试     | `create_testtask(...)`    | 创建测试任务 |

---

## 👥 角色场景速查

### 产品经理

```python
# ========== 需求管理 ==========

# 创建需求
success, result = client.create_story(
    product_id="1",
    title="用户登录功能",
    pri="3",              # 优先级: 0-4
    estimate="8",         # 预计工时
    spec="实现用户登录功能",
    reviewer="admin"
)

# 查看我的需求
success, stories = client.get_my_stories("assignedTo")
# 类型: assignedTo(指派给我), openedBy(我创建的), reviewedBy(我评审的)

# 编辑需求
success, result = client.edit_story(story_id, title="新标题", pri="2")

# 关闭需求
success, result = client.close_story(story_id)

# ========== 产品管理 ==========

# 创建产品
success, result = client.create_product(
    name="新产品",
    code="NEW",
    po="admin",           # 产品负责人
    status="normal"
)

# 查询产品列表
success, products = client.get_products()

# 创建发布计划
success, result = client.create_plan(
    product_id="1",
    title="V1.0版本",
    begin="2026-03-01",
    end="2026-03-31"
)

# 查询发布计划
success, plans = client.get_plans(product_id)
```

### 项目经理

```python
# ========== 项目管理 ==========

# 创建项目
success, result = client.create_project(
    name="V1.0开发项目",
    begin="2026-04-01",
    end="2026-04-30",
    code="V1",
    days="22",
    products=["1"],      # 关联产品ID列表
    plans=["1"],         # 关联计划ID列表
    desc="项目描述"
)

# 查询项目详情
success, project = client.get_project("1")
print(f"项目: {project['name']}, 状态: {project['status']}")

# 启动项目 (wait → doing)
success, result = client.start_project("1")

# 关闭项目
success, result = client.close_project("1")

# ========== 项目查询 ==========

# 查询项目列表
projects = client.get_project_list_old("all")  # 状态: all, doing, done, suspended

# 查询项目任务
tasks = client.get_project_tasks_old(project_id, "all")  # 状态: all, wait, doing, done, pause, cancel

# ========== 任务分解 ==========

# 创建任务
success, result = client.create_task(
    project_id="1",       # 项目ID
    name="用户登录功能开发",
    type="devel",         # 任务类型: devel, test, design, study, discuss, ui, affair, misc
    assignedTo="dev1",
    pri="3",              # 优先级: 0-4
    estimate="8",         # 预计工时
    desc="实现用户登录功能"
)

# 批量创建任务
success, result = client.create_tasks(
    project_id="1",
    tasks=[
        {"name": "前端开发", "type": "devel", "assignedTo": "dev1", "estimate": "8", "pri": "3"},
        {"name": "后端开发", "type": "devel", "assignedTo": "dev2", "estimate": "16", "pri": "3"},
        {"name": "接口联调", "type": "devel", "assignedTo": "dev1", "estimate": "4", "pri": "3"}
    ]
)

# 创建子任务
success, result = client.create_subtasks(
    execution_id="1",     # 项目/执行ID
    parent_id="100",      # 父任务ID
    tasks=[
        {"name": "前端开发", "estimate": "8", "assignedTo": "dev1", "type": "devel", "pri": "3"},
        {"name": "后端开发", "estimate": "16", "assignedTo": "dev2", "type": "devel", "pri": "3"},
        {"name": "接口联调", "estimate": "4", "assignedTo": "dev1", "type": "devel", "pri": "3"}
    ]
)

# ========== 任务指派 ==========

# 指派任务
success, result = client.assign_task(task_id, "zhangsan", "请处理")

# ========== 任务管理 ==========

# 取消任务
success, result = client.cancel_task(task_id)

# 删除任务
success, result = client.delete_task(task_id)
```

### 研发工程师

```python
# ========== 日常查询 ==========

# 查看我的任务
success, tasks = client.get_my_tasks("assignedTo")
# 类型: assignedTo(指派给我), openedBy(我创建的), finishedBy(我完成的)

# 查看任务详情
success, task = client.get_task_detail(task_id)
print(f"状态: {task['status']}")      # wait, doing, pause, done, cancel, closed
print(f"预计: {task['estimate']}h")   # 预计工时
print(f"消耗: {task['consumed']}h")   # 已消耗工时
print(f"剩余: {task['left']}h")       # 剩余工时

# ========== 任务流转 ==========

# 开始任务 (wait → doing)
success, result = client.start_task(task_id, "开始开发")

# 记录工时
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
success, result = client.record_estimate(task_id, [
    {
        "date": today,
        "consumed": "3",      # 本次消耗
        "left": "5",          # 剩余
        "work": "完成了登录功能开发"
    }
])

# 暂停任务 (doing → pause)
success, result = client.pause_task(task_id, "等待依赖接口")

# 继续任务 (pause → doing)
success, result = client.restart_task(task_id, "依赖已就绪")

# 完成任务 (doing → done) - 重要：先记录工时left=0，再完成
client.record_estimate(task_id, [
    {"date": today, "consumed": "5", "left": "0", "work": "全部完成"}
])
success, result = client.finish_task(task_id, "开发完成")

# 关闭任务 (done → closed)
success, result = client.close_task(task_id, "已验收")

# 激活任务 (done/closed → doing)
success, result = client.activate_task(task_id, "重新开始")

# ========== Bug处理 ==========

# 查看我的Bug
success, bugs = client.get_my_bugs("assignedTo")
# 类型: assignedTo(指派给我), openedBy(我创建的), resolvedBy(我解决的)

# 查看Bug详情
success, bug = client.get_bug(bug_id)

# 解决Bug
success, result = client.resolve_bug(
    bug_id=bug_id,
    resolution="fixed",       # fixed, postponed, willnotfix, duplicate, tostory
    resolved_build="trunk",
    comment="已修复登录校验问题"
)
```

### 测试工程师

```python
# ========== Bug管理 ==========

# 创建Bug
success, result = client.create_bug(
    product_id="1",
    title="登录页面报错：500错误",
    severity="3",             # 严重程度: 1-4 (1最严重)
    pri="3",                  # 优先级: 0-4
    type="codeerror",         # 类型: codeerror, config, install, security, etc.
    steps="1.打开登录页\n2.输入账号密码\n3.点击登录\n4.出现500错误",
    assignedTo="dev1",
    project_id="1"
)

# 确认Bug
success, result = client.confirm_bug(bug_id, "确认是有效Bug")

# 指派Bug
success, result = client.assign_bug(bug_id, "dev1", "请处理")

# 关闭Bug (resolved → closed)
success, result = client.close_bug(bug_id, "验证通过")

# 激活Bug (closed → active)
success, result = client.activate_bug(bug_id, "问题重现")

# ========== 测试用例 ==========

# 创建测试用例
success, result = client.create_testcase(
    product_id="1",
    title="登录功能测试",
    case_type="feature",      # feature, performance, config, install, security, etc.
    steps="1.打开登录页\n2.输入账号密码\n3.点击登录",
    expect="登录成功"
)

# 查询测试用例
success, cases = client.get_testcases(product_id, "all")

# ========== 测试任务 ==========

# 创建测试任务
success, result = client.create_testtask(
    product_id="1",
    name="Sprint1测试",
    begin="2026-03-20",
    end="2026-03-25"
)

# 开始测试任务
success, result = client.start_testtask(task_id)

# 关闭测试任务
success, result = client.close_testtask(task_id)
```

---

## 🔄 状态流转图

### 任务状态流转

```
                    ┌─────────────┐
                    │   wait      │ 待开始
                    └──────┬──────┘
                           │ start_task()
                           ▼
                    ┌─────────────┐
           ┌───────│   doing     │ 进行中◀───────┐
           │       └──────┬──────┘               │
           │              │                      │
    pause_task()    finish_task()         activate_task()
           │              │                      │
           │              ▼                      │
           │       ┌─────────────┐               │
           │       │    done     │ 已完成        │
           │       └──────┬──────┘               │
           │              │                      │
           │       close_task()           restart_task()
           │              │                      │
           │              ▼                      │
    ┌──────┴──────┐ ┌─────────────┐              │
    │   pause     │ │   closed    │ 已关闭       │
    │   暂停      │ └─────────────┘              │
    └──────┬──────┘                              │
           │                                     │
           └─────────────────────────────────────┘
                     restart_task()

    cancel_task() ──────▶ cancel (已取消)
```

**API调用顺序**:

| 当前状态    | 目标状态 | API                      | 说明                             |
| ----------- | -------- | ------------------------ | -------------------------------- |
| wait        | doing    | `start_task(task_id)`    | 开始任务                         |
| doing       | pause    | `pause_task(task_id)`    | 暂停任务                         |
| pause       | doing    | `restart_task(task_id)`  | 继续任务                         |
| doing       | done     | `finish_task(task_id)`   | 完成任务（建议先记录工时left=0） |
| done        | closed   | `close_task(task_id)`    | 关闭任务                         |
| done/closed | doing    | `activate_task(task_id)` | 激活任务                         |
| any         | cancel   | `cancel_task(task_id)`   | 取消任务                         |

### Bug状态流转

```
    ┌─────────────┐
    │   active    │ 激活
    └──────┬──────┘
           │ resolve_bug()
           ▼
    ┌─────────────┐
    │  resolved   │ 已解决
    └──────┬──────┘
           │ close_bug()
           ▼
    ┌─────────────┐
    │   closed    │ 已关闭
    └──────┬──────┘
           │ activate_bug()
           └──────────────┐
                          ▼
                    ┌─────────────┐
                    │   active    │ 激活
                    └─────────────┘
```

**API调用顺序**:

| 当前状态 | 目标状态 | API                               | 说明    |
| -------- | -------- | --------------------------------- | ------- |
| active   | resolved | `resolve_bug(bug_id, resolution)` | 解决Bug |
| resolved | closed   | `close_bug(bug_id)`               | 关闭Bug |
| closed   | active   | `activate_bug(bug_id)`            | 激活Bug |

---

## 📝 重要注意事项

### 1. 工时记录是批量接口

```python
# ✅ 正确：一次提交多条记录
client.record_estimate(task_id, [
    {"date": "2026-03-27", "consumed": "2", "left": "6", "work": "开发"},
    {"date": "2026-03-28", "consumed": "3", "left": "3", "work": "测试"}
])

# ❌ 错误：多次调用会覆盖之前记录
client.record_estimate(task_id, [{"date": "2026-03-27", "consumed": "2", ...}])
client.record_estimate(task_id, [{"date": "2026-03-28", "consumed": "3", ...}])  # 会覆盖！
```

### 2. 完成任务前先记录工时

```python
# ✅ 正确流程
client.record_estimate(task_id, [
    {"date": "2026-03-27", "consumed": "8", "left": "0", "work": "完成"}
])
client.finish_task(task_id, "开发完成")

# ❌ 错误：直接完成任务，没有记录最终工时
client.finish_task(task_id)
```

### 3. 获取任务详情验证操作结果

```python
# 很多API返回HTML而非JSON，解析会失败，但操作实际成功
success, result = client.start_task(task_id)
# 建议：用get_task_detail验证
ok, task = client.get_task_detail(task_id)
print(f"状态: {task['status']}")  # 应为 'doing'
```

### 4. 解决Bug用专用接口

```python
# ✅ 正确：使用resolve_bug
client.resolve_bug(bug_id, "fixed", "trunk", "已修复")

# ❌ 错误：不要用edit_bug修改状态，会丢失其他字段
# client.edit_bug(bug_id, status="resolved")  # 会丢失产品、项目关联！
```

### 5. 创建子任务注意ditto

```python
# 子任务数组参数，第一个任务用实际值，后续用ditto继承
client.create_subtasks(execution_id, parent_id, [
    {"name": "前端", "estimate": "8", "assignedTo": "dev1", "type": "devel", "pri": "3"},
    {"name": "后端", "estimate": "16", "assignedTo": "dev2", "type": "devel", "pri": "3"}
    # 第二个任务会继承第一个任务的type和pri（API内部处理）
])
```

### 6. 查看我的任务/bug返回格式

```python
# get_my_tasks和get_my_bugs返回的是列表，不是字典
success, tasks = client.get_my_tasks("assignedTo")
if success:
    for task in tasks:  # tasks是列表
        print(f"[{task['id']}] {task['name']} ({task['status']})")
```

---

## 🎯 典型使用场景

### 场景1：每日站会查询

```python
# 查看我的任务
success, tasks = client.get_my_tasks("assignedTo")

# 统计状态
stats = {"wait": 0, "doing": 0, "pause": 0, "done": 0}
for task in tasks:
    status = task.get("status", "unknown")
    if status in stats:
        stats[status] += 1

print(f"我的任务: 待开始{stats['wait']}, 进行中{stats['doing']}, 暂停{stats['pause']}, 已完成{stats['done']}")
```

### 场景2：开始新任务

```python
# 1. 查看任务详情
success, task = client.get_task_detail(task_id)
print(f"任务: {task['name']}, 预计工时: {task['estimate']}h")

# 2. 开始任务
success, result = client.start_task(task_id, "开始开发")

# 3. 验证
ok, task = client.get_task_detail(task_id)
print(f"状态: {task['status']}")  # doing
```

### 场景3：每日记录工时

```python
from datetime import datetime

# 记录今天的工时
today = datetime.now().strftime("%Y-%m-%d")
success, result = client.record_estimate(task_id, [
    {
        "date": today,
        "consumed": "3",      # 今天消耗3小时
        "left": "5",          # 剩余5小时
        "work": "完成了用户登录功能开发"
    }
])

# 验证
ok, task = client.get_task_detail(task_id)
print(f"总消耗: {task['consumed']}h, 剩余: {task['left']}h")
```

### 场景4：完成任务

```python
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# 1. 记录最终工时
client.record_estimate(task_id, [
    {"date": today, "consumed": "5", "left": "0", "work": "全部完成"}
])

# 2. 完成任务
success, result = client.finish_task(task_id, "开发完成，已自测")

# 3. 验证
ok, task = client.get_task_detail(task_id)
print(f"状态: {task['status']}")        # done
print(f"完成人: {task['finishedBy']}")  # admin
```

### 场景5：提交Bug

```python
# 创建Bug
success, result = client.create_bug(
    product_id="1",
    title="登录页面500错误",
    severity="2",             # 严重
    pri="3",
    type="codeerror",
    steps="1.打开登录页\n2.输入admin/admin\n3.点击登录\n4.出现500错误",
    assignedTo="dev1",
    comment="优先处理"
)

# 查看我的Bug
success, bugs = client.get_my_bugs("openedBy")
for bug in bugs:
    print(f"[{bug['id']}] {bug['title']} ({bug['status']})")
```

### 场景6：解决和关闭Bug

```python
# 1. 查看Bug详情
success, bug = client.get_bug(bug_id)
print(f"标题: {bug['title']}, 状态: {bug['status']}")

# 2. 解决Bug
success, result = client.resolve_bug(
    bug_id=bug_id,
    resolution="fixed",
    resolved_build="trunk",
    comment="已修复登录校验逻辑"
)

# 3. 关闭Bug
success, result = client.close_bug(bug_id, "验证通过，问题已修复")

# 4. 验证
ok, bug = client.get_bug(bug_id)
print(f"状态: {bug['status']}")        # closed
print(f"关闭人: {bug['closedBy']}")
```

### 场景7：创建子任务分解

```python
# 查询父任务
tasks = client.get_project_tasks_old(project_id, "all")
parent_task_id = list(tasks.keys())[0]

# 创建子任务
success, result = client.create_subtasks(
    execution_id=project_id,
    parent_id=parent_task_id,
    tasks=[
        {"name": "前端开发", "estimate": "8", "assignedTo": "dev1"},
        {"name": "后端开发", "estimate": "16", "assignedTo": "dev2"},
        {"name": "接口联调", "estimate": "4", "assignedTo": "dev1"}
    ]
)
```

---

## 🔧 高级用法

### 批量操作

```python
# 批量创建需求
requirements = ["用户登录", "商品浏览", "购物车", "订单管理"]
for req in requirements:
    client.create_story(product_id, req, pri="3", estimate="8")

# 批量记录工时
from datetime import datetime, timedelta
today = datetime.now()
records = []
for i in range(5):
    records.append({
        "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
        "consumed": "2",
        "left": str(10 - i * 2),
        "work": f"开发进度{i*20}%"
    })
client.record_estimate(task_id, records)
```

### 状态统计

```python
# 项目任务状态统计
tasks = client.get_project_tasks_old(project_id, "all")
stats = {}
for tid, task in tasks.items():
    status = task.get("status", "unknown")
    stats[status] = stats.get(status, 0) + 1

print(f"任务统计: {stats}")
# 输出: {'wait': 5, 'doing': 3, 'done': 10, 'pause': 1, 'cancel': 2}
```

### 数据导出

```python
import json

# 导出我的任务
success, tasks = client.get_my_tasks("assignedTo")
with open("my_tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

# 导出我的Bug
success, bugs = client.get_my_bugs("assignedTo")
with open("my_bugs.json", "w", encoding="utf-8") as f:
    json.dump(bugs, f, ensure_ascii=False, indent=2)
```

---

## 📚 API完整列表

### 产品管理

| API                               | 说明         | 参数                                       |
| --------------------------------- | ------------ | ------------------------------------------ |
| `create_product(name, code, ...)` | 创建产品     | name, code, type, po, qd, rd, status, desc |
| `get_products()`                  | 查询产品列表 | -                                          |
| `get_product(product_id)`         | 查询产品详情 | product_id                                 |
| `edit_product(product_id, ...)`   | 编辑产品     | product_id, \*\*kwargs                     |
| `close_product(product_id)`       | 关闭产品     | product_id                                 |
| `delete_product(product_id)`      | 删除产品     | product_id                                 |

### 需求管理

| API                                    | 说明         | 参数                                                   |
| -------------------------------------- | ------------ | ------------------------------------------------------ |
| `create_story(product_id, title, ...)` | 创建需求     | product_id, title, pri, estimate, spec, ...            |
| `get_story(story_id)`                  | 查询需求详情 | story_id                                               |
| `get_my_stories(story_type)`           | 查询我的需求 | story_type: assignedTo, openedBy, reviewedBy, closedBy |
| `edit_story(story_id, ...)`            | 编辑需求     | story_id, \*\*kwargs                                   |
| `close_story(story_id)`                | 关闭需求     | story_id                                               |
| `activate_story(story_id)`             | 激活需求     | story_id                                               |
| `delete_story(story_id)`               | 删除需求     | story_id                                               |

### 计划管理

| API                                   | 说明         | 参数                                |
| ------------------------------------- | ------------ | ----------------------------------- |
| `create_plan(product_id, title, ...)` | 创建计划     | product_id, title, begin, end, desc |
| `get_plans(product_id)`               | 查询计划列表 | product_id                          |
| `delete_plan(plan_id)`                | 删除计划     | plan_id                             |

### 项目管理

| API                                         | 说明         | 参数                                                |
| ------------------------------------------- | ------------ | --------------------------------------------------- |
| `create_project(name, begin, end, ...)`     | 创建项目     | name, begin, end, code, days, products, plans, desc |
| `get_project(project_id)`                   | 查询项目详情 | project_id                                          |
| `start_project(project_id)`                 | 启动项目     | project_id                                          |
| `close_project(project_id)`                 | 关闭项目     | project_id                                          |
| `get_project_list_old(status)`              | 查询项目列表 | status: all, doing, done, suspended                 |
| `get_project_tasks_old(project_id, status)` | 查询项目任务 | project_id, status                                  |
| `get_project_bugs(project_id, status)`      | 查询项目Bug  | project_id, status                                  |

### 任务管理

| API                                               | 说明         | 参数                                                                |
| ------------------------------------------------- | ------------ | ------------------------------------------------------------------- |
| `create_task(project, name, type, ...)`           | 创建任务     | project, name, type, story, module, assignedTo, pri, estimate, desc |
| `create_tasks(project, tasks)`                    | 批量创建任务 | project, tasks列表                                                  |
| `get_my_tasks(task_type)`                         | 查询我的任务 | task_type: assignedTo, openedBy, finishedBy, closedBy, canceledBy   |
| `get_task_detail(task_id)`                        | 查询任务详情 | task_id                                                             |
| `create_subtasks(execution_id, parent_id, tasks)` | 创建子任务   | execution_id, parent_id, tasks列表                                  |
| `start_task(task_id, comment)`                    | 开始任务     | task_id, comment                                                    |
| `pause_task(task_id, comment)`                    | 暂停任务     | task_id, comment                                                    |
| `restart_task(task_id, comment)`                  | 继续任务     | task_id, comment                                                    |
| `finish_task(task_id, comment)`                   | 完成任务     | task_id, comment                                                    |
| `close_task(task_id, comment)`                    | 关闭任务     | task_id, comment                                                    |
| `activate_task(task_id, comment)`                 | 激活任务     | task_id, comment                                                    |
| `cancel_task(task_id)`                            | 取消任务     | task_id                                                             |
| `delete_task(task_id)`                            | 删除任务     | task_id                                                             |
| `assign_task(task_id, assigned_to, comment)`      | 指派任务     | task_id, assigned_to, comment                                       |
| `record_estimate(task_id, records)`               | 记录工时     | task_id, records列表                                                |

### Bug管理

| API                                        | 说明        | 参数                                                           |
| ------------------------------------------ | ----------- | -------------------------------------------------------------- |
| `get_my_bugs(bug_type)`                    | 查询我的Bug | bug_type: assignedTo, openedBy, resolvedBy, closedBy           |
| `get_bug(bug_id)`                          | 查询Bug详情 | bug_id                                                         |
| `create_bug(product_id, title, ...)`       | 创建Bug     | product_id, title, severity, pri, type, steps, assignedTo, ... |
| `resolve_bug(bug_id, resolution, ...)`     | 解决Bug     | bug_id, resolution, resolved_build, comment                    |
| `close_bug(bug_id, comment)`               | 关闭Bug     | bug_id, comment                                                |
| `activate_bug(bug_id, comment)`            | 激活Bug     | bug_id, comment                                                |
| `assign_bug(bug_id, assigned_to, comment)` | 指派Bug     | bug_id, assigned_to, comment                                   |
| `confirm_bug(bug_id, comment)`             | 确认Bug     | bug_id, comment                                                |
| `delete_bug(bug_id)`                       | 删除Bug     | bug_id                                                         |

### 测试管理

| API                                        | 说明         | 参数                                             |
| ------------------------------------------ | ------------ | ------------------------------------------------ |
| `get_testcases(product_id, browse_type)`   | 查询测试用例 | product_id, browse_type                          |
| `get_testcase(case_id)`                    | 查询用例详情 | case_id                                          |
| `create_testcase(product_id, title, ...)`  | 创建测试用例 | product_id, title, case_type, steps, expect, ... |
| `delete_testcase(case_id)`                 | 删除测试用例 | case_id                                          |
| `get_testsuites(product_id)`               | 查询测试套件 | product_id                                       |
| `create_testsuite(product_id, name, desc)` | 创建测试套件 | product_id, name, desc                           |
| `get_testtasks(product_id, task_type)`     | 查询测试任务 | product_id, task_type                            |
| `create_testtask(product_id, name, ...)`   | 创建测试任务 | product_id, name, begin, end, desc               |
| `start_testtask(task_id)`                  | 开始测试任务 | task_id                                          |
| `close_testtask(task_id)`                  | 关闭测试任务 | task_id                                          |

---

## 🆘 故障排查

### 常见问题

**Q: 认证失败怎么办？**

```python
# 检查凭证
credentials = read_credentials()
print(credentials)  # 确保endpoint, username, password正确

# 手动获取session
sid = client.get_session()
if not sid:
    print("认证失败，请检查用户名密码")
```

**Q: API返回success=False但操作成功？**

```python
# 很多API返回HTML而非JSON，解析会失败
# 建议：用查询接口验证操作结果
success, result = client.start_task(task_id)
# 返回False但实际成功
ok, task = client.get_task_detail(task_id)
print(task['status'])  # 验证状态是否变为doing
```

**Q: 工时记录不生效？**

```python
# 确保参数格式正确
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")  # 必须是YYYY-MM-DD格式

success, result = client.record_estimate(task_id, [
    {
        "date": today,
        "consumed": "2",  # 字符串格式
        "left": "6",      # 字符串格式
        "work": "开发中"
    }
])

# 验证
ok, task = client.get_task_detail(task_id)
print(f"消耗: {task['consumed']}, 剩余: {task['left']}")
```

**Q: 创建子任务失败？**

```python
# 确保参数完整
tasks = [
    {
        "name": "前端开发",      # 必需
        "estimate": "8",         # 必需
        "assignedTo": "admin",   # 必需
        "type": "devel",         # 可选，默认devel
        "pri": "3"               # 可选，默认3
    }
]

success, result = client.create_subtasks(
    execution_id="1",     # 项目/执行ID
    parent_id="100",      # 父任务ID
    tasks=tasks
)
```

---

## 📖 参考资料

- 禅道官网: https://www.zentao.net/
- 禅道API文档: https://www.zentao.net/book/zentaopmshelp/562.html
- 客户端源码: `lib/zentao_client.py`
- 测试报告: `docs/测试报告-工单客服系统.md`

---

## 📄 许可证

MIT License - 自由使用、修改和分发
