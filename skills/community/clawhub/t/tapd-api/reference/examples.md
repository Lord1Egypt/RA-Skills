# TAPD API 使用示例

## 1. 基础查询

### 获取需求列表

```bash
# Shell 方式
./scripts/tapd-api.sh stories 20

# Python 方式
python3 scripts/tapd_oauth_client.py stories --limit 20
```

```python
# Python 代码
from scripts.tapd_oauth_client import TapdOAuthClient

client = TapdOAuthClient()
stories = client.get_stories(limit=20)

for story in stories:
    print(f"{story['id']}: {story['name']}")
```

### 获取需求详情

```bash
# Shell
./scripts/tapd-api.sh story 1112345678001000001

# Python CLI
python3 scripts/tapd_oauth_client.py story --id 1112345678001000001
```

```python
# Python 代码
story = client.get_story("1112345678001000001")
print(f"标题: {story['name']}")
print(f"状态: {story['status']}")
print(f"描述: {story['description']}")
```

## 2. 过滤查询

### 按状态过滤

```bash
# 获取进行中的需求
./scripts/tapd-api.sh stories 50 | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data['data']:
    s = item['Story']
    if s['status'] == 'status_3':
        print(f\"{s['id']}: {s['name']}\")
"
```

```python
# Python 方式更简单
stories = client.get_stories(status="status_3", limit=100)
for story in stories:
    print(f"{story['id']}: {story['name']}")
```

### 按优先级过滤

```python
# 获取高优先级需求
high_priority_stories = [
    s for s in client.get_stories(limit=100)
    if s.get('priority') == '4'
]

for story in high_priority_stories:
    print(f"[HIGH] {story['name']}")
```

### 按负责人过滤

```python
# 获取我的需求
my_stories = client.get_stories(owner="张三", limit=50)

for story in my_stories:
    print(f"{story['name']} - {story['status']}")
```

## 3. 创建和更新

### 创建需求

```python
new_story = client.create_story(
    name="【新功能】实现用户登录功能",
    description="""需求描述：
    1. 支持邮箱登录
    2. 支持手机号登录
    3. 支持记住密码
    4. 登录失败3次锁定30分钟
    
    技术要求：
    - 使用 JWT Token
    - 前端使用 React
    - 后端使用 Node.js + Express
    """,
    priority="4",  # High
    iteration_id="1112345678001000002"
)

print(f"创建成功: {new_story['id']}")
print(f"查看链接: https://www.tapd.cn/12345678/prong/stories/view/{new_story['id']}")
```

### 更新需求状态

```python
# 更新为进行中
updated_story = client.update_story(
    story_id="1112345678001000001",
    status="status_3",
    owner="张三"
)

print(f"状态已更新: {updated_story['status']}")
```

### 批量更新

```python
# 将所有规划中的需求移到待实现
planning_stories = client.get_stories(status="planning", limit=100)

for story in planning_stories:
    client.update_story(
        story_id=story['id'],
        status="status_2"  # 待实现
    )
    print(f"已更新: {story['name']}")
```

## 4. 任务和缺陷

### 获取任务列表

```python
tasks = client.get_tasks(limit=20)

for task in tasks:
    print(f"[{task['status']}] {task['name']} - {task['owner']}")
```

### 获取缺陷列表

```python
bugs = client.get_bugs(limit=20)

for bug in bugs:
    priority_label = bug.get('priority_label', bug.get('priority'))
    print(f"[{priority_label}] {bug['title']}")
```

## 5. 迭代管理

### 获取迭代列表

```python
iterations = client.get_iterations(limit=10)

for iteration in iterations:
    print(f"{iteration['name']}")
    print(f"  开始: {iteration['startdate']}")
    print(f"  结束: {iteration['enddate']}")
    print(f"  状态: {iteration['status']}")
```

### 获取迭代下的需求

```python
iteration_id = "1112345678001000002"
stories_in_iteration = client.get_stories(
    iteration_id=iteration_id,
    limit=100
)

print(f"迭代需求数量: {len(stories_in_iteration)}")
for story in stories_in_iteration:
    print(f"  - {story['name']}")
```

## 6. 高级用法

### Token 缓存

```python
# Token 自动缓存到 ~/.tapd_token_cache.json
# 2 小时内不会重复请求

# 查看缓存
import json
with open("~/.tapd_token_cache.json") as f:
    cache = json.load(f)
    print(f"Token: {cache['access_token'][:20]}...")
    print(f"过期时间: {cache['expires_at']}")
```

### 多工作空间

```python
# 使用默认工作空间（项目A）
stories_vango = client.get_stories(limit=10)

# 切换到项目B项目
stories_quantum = client.get_stories(
    workspace_id="87654321",
    limit=10
)
```

### 分页查询

```python
all_stories = []
page = 1
per_page = 100

while True:
    stories = client.get_stories(limit=per_page, page=page)
    if not stories:
        break
    
    all_stories.extend(stories)
    page += 1

print(f"总共获取 {len(all_stories)} 条需求")
```

### 错误处理

```python
try:
    story = client.get_story("invalid_id")
except Exception as e:
    print(f"错误: {e}")
    # 处理错误
```

## 7. 实用工具函数

### 需求统计

```python
def count_stories_by_status(workspace_id=None):
    """按状态统计需求数量"""
    stories = client.get_stories(workspace_id=workspace_id, limit=1000)
    
    status_count = {}
    for story in stories:
        status = story['status']
        status_count[status] = status_count.get(status, 0) + 1
    
    return status_count

# 使用
stats = count_stories_by_status()
for status, count in stats.items():
    print(f"{status}: {count}")
```

### 需求搜索

```python
def search_stories(keyword, workspace_id=None):
    """搜索需求（按标题）"""
    all_stories = client.get_stories(workspace_id=workspace_id, limit=1000)
    
    return [
        s for s in all_stories
        if keyword.lower() in s['name'].lower()
    ]

# 使用
results = search_stories("登录")
for story in results:
    print(f"{story['id']}: {story['name']}")
```

### 需求导出

```python
import csv

def export_stories_to_csv(filename="stories.csv", workspace_id=None):
    """导出需求到 CSV"""
    stories = client.get_stories(workspace_id=workspace_id, limit=1000)
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'ID', '标题', '状态', '负责人', '优先级', '创建时间'
        ])
        writer.writeheader()
        
        for story in stories:
            writer.writerow({
                'ID': story['id'],
                '标题': story['name'],
                '状态': story['status'],
                '负责人': story['owner'],
                '优先级': story.get('priority_label', story.get('priority')),
                '创建时间': story['created']
            })
    
    print(f"已导出 {len(stories)} 条需求到 {filename}")

# 使用
export_stories_to_csv()
```

## 8. 集成到 OpenClaw 工作流

### 配合 Cursor CLI 自动化开发

```python
# 1. 获取待开发需求
todo_stories = client.get_stories(status="status_2", limit=10)

for story in todo_stories:
    print(f"需求: {story['name']}")
    
    # 2. 更新为进行中
    client.update_story(story_id=story['id'], status="status_3")
    
    # 3. 调用 Cursor Agent 开发
    # (在 OpenClaw 中执行)
    # exec(f"agent 'implement TAPD story {story['id']}: {story['name']}'")
    
    # 4. 完成后更新为待验收
    # client.update_story(story_id=story['id'], status="status_4")
```

### 每日报告生成

```python
from datetime import datetime

def generate_daily_report():
    """生成每日工作报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 今日创建的需求
    all_stories = client.get_stories(limit=1000)
    today_stories = [s for s in all_stories if s['created'].startswith(today)]
    
    # 今日完成的需求
    resolved_stories = [s for s in all_stories 
                       if s['status'] == 'resolved' 
                       and s['modified'].startswith(today)]
    
    report = f"""
# TAPD 每日报告 ({today})

## 新建需求 ({len(today_stories)})
{chr(10).join(f"- {s['name']}" for s in today_stories)}

## 完成需求 ({len(resolved_stories)})
{chr(10).join(f"- {s['name']}" for s in resolved_stories)}
"""
    
    print(report)
    return report

# 使用
report = generate_daily_report()
```

---

更多示例请查看 [SKILL.md](../SKILL.md)
