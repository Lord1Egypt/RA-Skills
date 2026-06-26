---
name: Work Todo
slug: work-todo
version: 1.0.0
description: "管理工作待办事项，支持添加、查看、完成、删除待办"
metadata: {"emoji": "📋"}
---

# Work Todo - 工作待办管理

## 数据存储

- **位置**: `~/.openclaw/workspace/shared/work-todo/lwork/todos.json`
- **格式**: JSON 文件，存储待办列表

## 数据结构

```json
{
  "todos": [
    {
      "id": "202603231030",
      "content": "设计稿提交",
      "task_name": "设计稿提交",
      "task_description": "提交三亚一期项目的设计稿终稿",
      "start_date": "2026-03-23",
      "due_date": "2026-03-31",
      "project": "三亚一期",
      "project_alias": "",
      "project_location": "三亚",
      "status": "进行中",
      "progress": [],
      "created": "2026-03-23T10:30:00+08:00",
      "completed": null,
      "completion_date": null,
      "assessment": null
    }
  ]
}
```

**字段说明**:
- `id`: 唯一标识，使用时间戳前10位
- `content`: 待办内容（简短描述）
- `task_name`: 任务名称（概括这个任务）
- `task_description`: 任务说明（详细描述）
- `start_date`: 开始日期（用户未说明时=创建时间）
- `due_date`: 截止日期（用户未说明时=长期任务）
- `project`: 项目名称
- `project_alias`: 项目别名
- `project_location`: 项目地点
- `status`: 状态（进行中/暂缓/已完成）
- `progress`: 进展记录数组，每项 {date, content}
- `created`: 创建时间
- `completed`: 完成时间（ISO格式，带时间）
- `completion_date`: 完成日期（仅日期，格式 YYYY-MM-DD，用户录入完成时未说明则默认为当天）
- `assessment`: 考核结果
  - `按时完成`: 截止日期之前或当天完成，绿色
  - `延误X天`: 截止日期之后完成，红色（X为延误天数）

## 项目列表

### 项目名称 → 别名 → 地点

| 项目名称 | 项目别名 | 项目地点 |
|---------|---------|---------|
| 三亚一期 | - | 三亚 |
| 三亚二期 | - | 三亚 |
| 三亚三期 | - | 三亚 |
| 洛阳项目 | 国润汽车产业园 | 洛阳 |
| 东润城樟园 | 东润城10号地、樟园 | 东润城 |
| 东润城润园 | 东润城8号地、润园 | 东润城 |
| 东润城璞园 | 东润城6号地、璞园 | 东润城 |
| 乐东1号地 | 麓鸣海、依山揽海雅居 | 乐东 |
| 乐东3号地 | - | 乐东 |
| 乐东4号地 | - | 乐东 |
| 新密云境花园 | 云境花园、云麓之城云境花园 | 新密 |
| 云麓之城北园 | 北园 | 新密 |
| 云麓之城南园 | 南园 | 新密 |

## 核心操作

### 1. 读取待办

```python
import json
from pathlib import Path

TODO_FILE = Path("~/.openclaw/workspace/shared/work-todo/lwork/todos.json").expanduser()

def load_todos():
    if not TODO_FILE.exists():
        return {"todos": []}
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### 2. 保存待办

```python
def save_todos(data):
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

### 3. 添加待办

```python
from datetime import datetime
import re

# 项目映射表
PROJECTS = {
    "三亚一期": {"alias": [], "location": "三亚"},
    "三亚二期": {"alias": [], "location": "三亚"},
    "三亚三期": {"alias": [], "location": "三亚"},
    "洛阳项目": {"alias": ["国润汽车产业园"], "location": "洛阳"},
    "东润城樟园": {"alias": ["东润城10号地", "樟园"], "location": "东润城"},
    "东润城润园": {"alias": ["东润城8号地", "润园"], "location": "东润城"},
    "东润城璞园": {"alias": ["东润城6号地", "璞园"], "location": "东润城"},
    "乐东1号地": {"alias": ["麓鸣海", "依山揽海雅居"], "location": "乐东"},
    "乐东3号地": {"alias": [], "location": "乐东"},
    "乐东4号地": {"alias": [], "location": "乐东"},
    "新密云境花园": {"alias": ["云境花园", "云麓之城云境花园"], "location": "新密"},
    "云麓之城北园": {"alias": ["北园"], "location": "新密"},
    "云麓之城南园": {"alias": ["南园"], "location": "新密"},
}

def find_project(name):
    """根据名称或别名查找项目信息"""
    name = name.strip()
    
    # 直接匹配
    if name in PROJECTS:
        return name, PROJECTS[name]
    
    # 别名匹配
    for proj, info in PROJECTS.items():
        if name in info["alias"]:
            return proj, info
    
    return None, None

def parse_date(text, default_today=False):
    """解析自然语言日期"""
    from datetime import datetime, timedelta
    
    if not text:
        return None
    
    text = text.strip().lower()
    today = datetime.now().date()
    
    if text == "今天":
        return today.strftime("%Y-%m-%d")
    elif text == "明天":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif text == "后天":
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    elif "天后" in text:
        days = int(re.search(r"(\d+)天", text).group(1))
        return (today + timedelta(days=days)).strftime("%Y-%m-%d")
    elif re.match(r"(\d+)月(\d+)日", text):
        m = re.match(r"(\d+)月(\d+)日", text)
        month, day = int(m.group(1)), int(m.group(2))
        year = today.year
        if month < today.month or (month == today.month and day < today.day):
            year += 1
        return f"{year}-{month:02d}-{day:02d}"
    
    # 直接返回（可能是具体日期）
    return text

def add_todo(content, task_name=None, task_description=None, project_name=None, due_date=None, start_date=None, status="进行中"):
    """添加待办"""
    data = load_todos()
    
    # 生成 ID
    todo_id = datetime.now().strftime("%Y%m%d%H%M")[:10]
    
    # 处理项目信息
    project = project_name
    project_alias = ""
    project_location = ""
    
    if project_name:
        proj, info = find_project(project_name)
        if proj:
            project = proj
            project_alias = project_name if project_name != proj else ""
            project_location = info["location"]
    
    # 处理日期
    if start_date:
        start_date = parse_date(start_date)
    else:
        start_date = datetime.now().date().strftime("%Y-%m-%d")
    
    if due_date:
        due_date = parse_date(due_date)
    else:
        due_date = "长期任务"
    
    todo = {
        "id": todo_id,
        "content": content,
        "task_name": task_name or content,  # 默认等于content
        "task_description": task_description or "",  # 可选详细说明
        "start_date": start_date,
        "due_date": due_date,
        "project": project or "",
        "project_alias": project_alias,
        "project_location": project_location,
        "status": status,
        "progress": [],
        "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "completed": None,
        "completion_date": None
    }
    
    data["todos"].append(todo)
    save_todos(data)
    
    return todo
```

### 4. 更新状态

```python
from datetime import datetime

def update_status(todo_id, new_status, completion_date=None):
    """更新待办状态
    
    Args:
        todo_id: 待办ID
        new_status: 新状态（进行中/暂缓/已完成）
        completion_date: 完成日期（用户未说明时默认为当天）
    """
    data = load_todos()
    
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["status"] = new_status
            if new_status == "已完成":
                # 用户未说明完成时间，则默认为当天
                if completion_date is None:
                    completion_date = datetime.now().date().strftime("%Y-%m-%d")
                todo["completed"] = f"{completion_date}T00:00:00+08:00"
                todo["completion_date"] = completion_date
                
                # 计算考核结果
                if todo.get("due_date") and todo["due_date"] != "长期任务":
                    due = datetime.strptime(todo["due_date"], "%Y-%m-%d").date()
                    complete = datetime.strptime(completion_date, "%Y-%m-%d").date()
                    days_diff = (complete - due).days
                    
                    if days_diff <= 0:
                        todo["assessment"] = "按时完成"
                    else:
                        todo["assessment"] = f"延误{days_diff}天"
                else:
                    # 长期任务无考核
                    todo["assessment"] = None
            break
    
    save_todos(data)
```

### 4.1 计算考核结果（独立函数）

```python
def calculate_assessment(due_date, completion_date):
    """计算考核结果
    
    Args:
        due_date: 截止日期（YYYY-MM-DD）
        completion_date: 完成日期（YYYY-MM-DD）
    
    Returns:
        按时完成 / 延误X天
    """
    if not due_date or due_date == "长期任务":
        return None
    
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    complete = datetime.strptime(completion_date, "%Y-%m-%d").date()
    days_diff = (complete - due).days
    
    if days_diff <= 0:
        return "按时完成"
    else:
        return f"延误{days_diff}天"
```

### 5. 添加进展

```python
from datetime import datetime, timedelta
import re

def parse_progress_date(text):
    """将自然语言日期转换为具体日期
    
    支持：今天、昨天、前天、明天、后天、X月X日等
    """
    if not text:
        return text
    
    text = text.strip().lower()
    today = datetime.now()
    
    # 今天 -> 4月2日 格式
    if "今天" in text:
        text = text.replace("今天", f"{today.month}月{today.day}日")
    # 昨天 -> 4月1日
    if "昨天" in text:
        yesterday = today - timedelta(days=1)
        text = text.replace("昨天", f"{yesterday.month}月{yesterday.day}日")
    # 前天 -> 4月1日
    if "前天" in text:
        day_before = today - timedelta(days=2)
        text = text.replace("前天", f"{day_before.month}月{day_before.day}日")
    # 明天 -> 4月3日
    if "明天" in text:
        tomorrow = today + timedelta(days=1)
        text = text.replace("明天", f"{tomorrow.month}月{tomorrow.day}日")
    # 后天 -> 4月4日
    if "后天" in text:
        day_after = today + timedelta(days=2)
        text = text.replace("后天", f"{day_after.month}月{day_after.day}日")
    
    # X月X日 格式转换为 mm-dd
    # 如 "3月21日" -> "03-21"
    def convert_md(m):
        month, day = int(m.group(1)), int(m.group(2))
        return f"{month:02d}-{day:02d}"
    
    text = re.sub(r"(\d{1,2})月(\d{1,2})日", convert_md, text)
    
    return text

def add_progress(todo_id, progress_content):
    """添加进展记录
    
    自动将自然语言日期转换为具体日期格式
    """
    data = load_todos()
    
    # 转换日期
    progress_content = parse_progress_date(progress_content)
    
    # 生成日期时间戳
    date_str = datetime.now().strftime("%y%m%d%H")
    
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            # 检查 progress 类型
            prog = todo.get("progress")
            if isinstance(prog, str):
                # 字符串格式：追加新进展
                new_prog = prog + "\n" + date_str + "-" + progress_content
                todo["progress"] = new_prog
            elif isinstance(prog, list):
                # 列表格式：追加新进展
                todo["progress"].append({
                    "date": date_str,
                    "content": progress_content
                })
            else:
                # 首次添加
                todo["progress"] = date_str + "-" + progress_content
            break
    
    save_todos(data)
```

### 6. 删除待办

```python
def delete_todo(todo_id):
    """删除待办"""
    data = load_todos()
    data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
    save_todos(data)
```

### 7. 列出待办

```python
def list_todos(status=None, project=None):
    """列出待办"""
    data = load_todos()
    todos = data["todos"]
    
    if status:
        todos = [t for t in todos if t["status"] == status]
    
    if project:
        todos = [t for t in todos if t["project"] == project]
    
    # 排序：按项目、状态
    todos.sort(key=lambda t: (t["status"] == "已完成", t.get("project", "")))
    
    return todos
```

## 交互示例

### 添加待办

用户说「帮我记一下，三亚一期的设计稿下周提交」：
1. 解析内容：设计稿下周提交
2. 任务名称：设计稿提交
3. 解析项目：三亚一期 → 项目地点：三亚
4. 解析截止日期：下周（计算具体日期）
5. 开始日期默认今天
6. 状态默认进行中

用户说「记录一个长期任务，洛阳项目的规划审批，是关于国润汽车产业园的规划审批」：
1. 内容：规划审批
2. 任务名称：规划审批
3. 任务说明：关于国润汽车产业园的规划审批
4. 项目：洛阳项目 → 别名：国润汽车产业园 → 地点：洛阳
5. 截止日期：长期任务

### 查看待办

用户说「看看洛阳项目的待办」：
1. 按项目筛选
2. 展示该项目的所有待办

### 更新进展

用户说「三亚一期的设计稿有进展了，今天确认了方案」：
1. 查找对应待办
2. 添加进展记录：{date: "2026-03-23-10", content: "今天确认了方案"}

### 完成待办

用户说「标记三亚一期的设计稿完成」：
1. 查找对应待办
2. 更新状态为已完成
3. 用户未说明完成时间，则默认设置为当天日期（completion_date 为今天，completed 为今天 00:00:00）

用户说「标记三亚一期的设计稿完成了，完成时间是3月20日」：
1. 查找对应待办
2. 更新状态为已完成
3. 设置 completion_date = "2026-03-20"，completed = "2026-03-20T00:00:00+08:00"

## 注意事项

- ID 使用时间戳前10位
- 日期格式：YYYY-MM-DD（具体日期）或"长期任务"
- 进展记录格式：{date: "YYYY-mm-dd-HH", content: "..."}
- 项目名称必须从列表中选择，别名自动转换
- 任务名称默认等于内容，任务说明为可选项

## 每日工作汇报格式（2026年4月3日更新）

### 分类逻辑

当列任务清单/今日任务/未完成任务给用户时，按以下分类和顺序列出所有进行中任务：

1. **【已延误】**：截止日期早于今天的进行中任务
   - 显示格式：`★ 任务名 | 项目 | 延误X天`
   - 任务下列出最新进展
   
2. **【今日截止 · 已完成】**：今日到期且已完成的任务
   - 显示格式：`✓ 任务名 | 项目`
   
3. **【今日截止 · 进行中】**：今日到期但进行中的任务
   - 显示格式：`★ 任务名 | 项目`
   - 任务下列出最新进展
   
4. **【近期截止（X月X日-X月X日）】**：截止日期晚于今天但在7天内
   - 显示格式：`★ 任务名 | 项目 | 截止X月X日`
   - 任务下列出最新进展
   
5. **【远期截止（X月X日及以后）】**：截止日期超过7天
   - 显示格式：`★ 任务名 | 项目 | 截止X月X日`
   - 任务下列出最新进展

### 展示规则

- 只显示最新的进展（最近添加的一条）
- 已延误任务标题后显示延误天数
- 任务按项目分组显示
- 任务列表最后显示"共 X 项进行中任务"统计

### 考核字段

每个任务新增 `assessment` 字段：
- `按时完成`：截止日期之前或当天完成，绿色
- `延误X天`：截止日期之后完成，红色（X为延误天数）
- 进行中任务默认 `null`

任务完成时自动计算考核结果。

### 任务分解

支持将一个任务按具体内容拆分为多个独立任务：
- 每个子任务独立 ID
- 项目保持一致
- 截止日期可单独调整

## 输出格式规范

当列出任务时使用以下格式：

1. 分类标题用【】包裹
2. 任务使用 `★` 符号，已完成用 `✓`
3. 进展使用引用格式 `> `（仅包裹进展内容）
4. 每个分类之间用 `---` 分隔

**注意：进展的引用格式每一项后面加空行，避免飞书错误解析。**

格式示例：

---

【已延误】
★ 任务名 | 项目 | 延误3天
> 进展内容

---

【今日截止 · 已完成】
✓ 任务名 | 项目

---

【今日截止 · 进行中】
★ 任务名 | 项目
> 进展内容

---

【近期截止（4月3日-4月9日）】
★ 任务名 | 项目 | 截止4月5日
> 进展内容

---

【远期截止（4月10日及以后）】
★ 任务名 | 项目 | 截止4月15日
> 进展内容

---

共 16 项进行中任务

---

## 截止日期显示

截止日期显示为"x月x日截止"格式，如"截止4月3日"。不显示项目地点。

---

## 添加进展时的日期转换

添加进展时，系统会自动将自然语言日期转换为"x月x日"格式：

| 输入 | 转换为 |
|------|--------|
| 今天 | 4月2日 |
| 昨天 | 4月1日 |
| 明天 | 4月3日 |
| 前天 | 3月31日 |
| 后天 | 4月4日 |
| 4月1日 | 4月1日 |

**进展记录中不展示日期时间戳前缀**（如 26040209-），只展示内容。

格式示例：

---

**分类标题**
- **任务内容** | 项目 | 备注
  > 最新进展

**近期截止 (4月3日-4月9日)**
- **任务** | 项目 | 截止日期
  > 进展

---

**重要：添加进展时的格式要求**

每条进展记录格式：`YYMMDDHH-内容`

多条进展之间必须用**换行符 `\n`** 分隔，不能直接拼接。

正确示例：
```
progress = "26032121-3月21日方案已确定\n26033118-已确认下沉庭院用PC砖"
```

错误示例（会显示重复）：
```
progress = "26032121-3月21日方案已确定26033118-已确认下沉庭院用PC砖"
```

### 自动日期转换

添加进展时，系统会自动将自然语言日期转换为具体日期：

| 输入 | 转换为 |
|------|--------|
| 今天 | 当前日期（如 04-02） |
| 昨天 | 昨天日期（如 04-01） |
| 前天 | 前天日期（如 03-31） |
| 明天 | 明天日期（如 04-03） |
| 后天 | 后天日期（如 04-04） |
| 3月21日 | 03-21 |

示例：
- 输入：「今天确认了方案」→ 自动转换为「04-02-10-确认了方案」
- 输入：「昨天与王总沟通」→ 自动转换为「04-01-10-与王总沟通」

---

## 飞书显示格式问题总结

### 问题描述
使用引用格式（`> 内容`）时，飞书错误地将下一个任务标题也解析为引用内容的一部分。

### 原因推测
飞书markdown解析器在处理连续行时，可能将下一行的内容也当作引用的延续。特别是在多行任务列表中，如果没有适当的分隔，下一个任务标题会被错误地包含在引用块内。

### 解决方案
在每个任务的引用进展后，加一个空行。这样可以避免飞书将下一行的任务标题错误解析为引用内容的一部分。

正确格式：
```
★ 任务A | 项目
> 进展内容A

★ 任务B | 项目
> 进展内容B
```
