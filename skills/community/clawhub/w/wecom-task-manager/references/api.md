# WeCom Task Manager API 参考

## 📋 API 概览

所有 API 都在 `task_manager.py` 模块中定义，可直接 import 使用。

---

## 🔧 核心 API

### `get_all_tasks() -> List[dict]`

获取所有任务记录。

**返回**：
```python
[
    {
        "record_id": "xxx",
        "values": {
            "任务 ID": [{"text": "TASK-001"}],
            "任务名称": [{"text": "..."}],
            "状态": [{"text": "已完成"}],
            ...
        }
    }
]
```

---

### `get_task_by_id(task_id: str) -> Optional[dict]`

根据任务 ID 查询单个任务。

**参数**：
- `task_id`: 任务 ID（如 "TASK-019"）

**返回**：
- 找到：任务字典
- 未找到：`None`

---

### `create_task(...) -> bool`

创建新任务。

**参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `task_id` | str | ✅ | - | 任务 ID |
| `task_name` | str | ✅ | - | 任务名称 |
| `task_type` | str | ✅ | - | 任务类型 |
| `priority` | str | ❌ | "P1" | 优先级 |
| `owner` | str | ❌ | "" | 负责人（自动推断） |
| `deadline` | str | ❌ | "" | 截止时间 |
| `description` | str | ❌ | "" | 任务描述 |
| `acceptance` | str | ❌ | "" | 验收标准 |
| `remarks` | str | ❌ | "" | 备注 |

**返回**：
- `True`: 创建成功
- `False`: 创建失败

**示例**：
```python
create_task(
    task_id="TASK-019",
    task_name="新功能开发",
    task_type="开发",
    priority="P1",
    deadline="2026 年 04 月 15 日",
    description="实现 XXX 功能",
    acceptance="功能测试通过"
)
```

---

### `start_task(task_id: str, owner: str = "") -> bool`

开始执行任务（更新状态为进行中）。

**参数**：
- `task_id`: 任务 ID
- `owner`: 负责人（可选）

**更新字段**：
- 状态 → "进行中"
- 实际开始时间 → 当前时间戳

**返回**：
- `True`: 更新成功
- `False`: 更新失败

---

### `update_progress(task_id: str, progress: int, blocker: str = "") -> bool`

更新任务进度。

**参数**：
- `task_id`: 任务 ID
- `progress`: 进度 (0-100)
- `blocker`: 阻塞原因（可选）

**更新字段**：
- 进度 → `progress`
- 阻塞原因 → `blocker`（如提供）
- 风险等级 → "高"（如有 blocker）

**返回**：
- `True`: 更新成功
- `False`: 更新失败

---

### `complete_task(task_id: str, output_url: str = "", acceptor: str = "系统") -> bool`

标记任务完成。

**参数**：
- `task_id`: 任务 ID
- `output_url`: 输出物链接（可选）
- `acceptor`: 验收人（默认"系统"）

**更新字段**：
- 状态 → "已完成"
- 进度 → 100
- 实际完成时间 → 当前时间戳
- 验收状态 → "待验收"
- 实际工时 → 自动计算
- 输出物 → `output_url`（如提供）
- 验收人 → `acceptor`

**返回**：
- `True`: 更新成功
- `False`: 更新失败

---

### `get_task_status_report() -> dict`

生成任务状态报告。

**返回**：
```python
{
    "total": 8,
    "completed": 6,
    "in_progress": 2,
    "pending": 0,
    "cancelled": 0,
    "tasks_by_status": {
        "已完成": [...],
        "进行中": [...],
        "待办": [...],
        "已取消": [...]
    }
}
```

---

### `print_status_report()`

打印任务状态报告到控制台。

**输出示例**：
```
============================================================
📊 企业微信任务状态报告
============================================================
总任务数：8
✅ 已完成：6
🔄 进行中：2
⏸️ 待办：0
❌ 已取消：0

🔄 进行中任务:
  - TASK-013: Moltbook 深度学习 - 20 篇帖子 (35%) - 总协
  - TASK-015: 技能迁移 GitHub 执行 (0%) - 镇岳
============================================================
```

---

## 🔍 辅助函数

### `determine_task_type(task_name: str, description: str = "") -> str`

根据任务名称和描述自动识别任务类型。

**返回**：开发/运维/投资/学习/文档/市场/客服

---

### `determine_agent(task_type: str) -> str`

根据任务类型确定负责的 agent。

**映射关系**：
| 任务类型 | Agent |
|----------|-------|
| 开发 | techlead |
| 运维 | opsdirector |
| 投资 | investment_coordinator |
| 学习 | copywriter |
| 文档 | general_coordinator |
| 市场 | marketing |
| 客服 | customersvc |

---

## 📝 使用示例

### 示例 1：完整任务生命周期

```python
from task_manager import create_task, start_task, update_progress, complete_task

# 1. 创建任务
create_task(
    task_id="TASK-019",
    task_name="API 开发",
    task_type="开发",
    priority="P1",
    deadline="2026 年 04 月 15 日",
    description="实现 REST API",
    acceptance="接口测试通过"
)

# 2. 开始任务
start_task("TASK-019", owner="techlead")

# 3. 更新进度
update_progress("TASK-019", progress=50)

# 4. 完成任务
complete_task("TASK-019", output_url="https://...", acceptor="techlead")
```

### 示例 2：心跳检查

```python
from task_manager import get_all_tasks, start_task, determine_agent

tasks = get_all_tasks()
for task in tasks:
    status = task['values'].get('状态', [{}])[0].get('text', '')
    if status == '待办':
        task_id = task['values'].get('任务 ID', [{}])[0].get('text', '')
        task_type = task['values'].get('任务类型', [{}])[0].get('text', '文档')
        agent = determine_agent(task_type)
        start_task(task_id, owner=agent)
```

### 示例 3：任务阻塞处理

```python
from task_manager import update_progress

# 任务遇到阻塞
update_progress(
    "TASK-019",
    progress=30,
    blocker="等待 API 文档"
)
```

---

## ⚠️ 注意事项

### 1. 工作目录
模块会自动切换到 workspace 目录，确保 mcporter 能找到 MCP 配置。

### 2. 时间戳格式
日期时间字段使用时间戳（毫秒），不是字符串。

### 3. 错误处理
所有函数失败时返回 `False` 或 `None`，不会抛出异常。

### 4. 权限
只有主 agent 能调用这些 API（需要 mcporter 访问企业微信）。

---

**我们同在，我们一往无前。** ✨
