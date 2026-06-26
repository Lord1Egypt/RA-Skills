# 查询结果格式规范

## 目录
- [概览](#概览)
- [今日查询](#今日查询)
- [本周查询](#本周查询)
- [按类别查询](#按类别查询)

## 概览
查询功能返回结构化的 JSON 数据，智能体根据这些数据生成用户友好的展示内容。以下为各查询功能的输出格式规范。

## 今日查询

### 命令
```bash
python scripts/weekly_planner.py query_today --year <年份> --week <周次> --date "<日期>"
```

### 输出格式
```json
{
  "success": true,
  "date": "YYYY-MM-DD",
  "summary": {
    "total_plans": 3,
    "completed": 2,
    "completion_rate": 66.67
  },
  "plans": [
    {
      "id": 1,
      "task": "完成任务A",
      "category": "work",
      "assigned_date": "YYYY-MM-DD",
      "status": "completed",
      "priority": "high",
      "created_at": "YYYY-MM-DDTHH:MM:SS",
      "updated_at": null,
      "deleted": false
    }
  ],
  "completions": [
    {
      "task_id": 1,
      "task": "完成任务A",
      "category": "work",
      "assigned_date": "YYYY-MM-DD",
      "completed_date": "YYYY-MM-DDTHH:MM:SS",
      "notes": "提前完成",
      "progress": 100
    }
  ],
  "reflection": {
    "date": "YYYY-MM-DD",
    "content": "今天工作效率很高...",
    "created_at": "YYYY-MM-DDTHH:MM:SS"
  }
}
```

### 智能体展示模板
```
今日情况（{date}）

【进度统计】
- 计划任务：{total_plans} 项
- 已完成：{completed} 项
- 完成率：{completion_rate}%

【今日计划】
{循环展示 plans}
✓ ID{id} - {task} [{category}] - {status}
  优先级：{priority}

【完成记录】
{循环展示 completions}
✓ {task}（完成于 {completed_date}）
  备注：{notes}

【今日反思】
{reflection.content}
```

## 本周查询

### 命令
```bash
python scripts/weekly_planner.py query_week --year <年份> --week <周次>
```

### 输出格式
```json
{
  "success": true,
  "year": 2025,
  "week": 12,
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "summary": {
    "total_plans": 15,
    "completed": 12,
    "completion_rate": 80.0
  },
  "daily_data": {
    "YYYY-MM-DD": {
      "plans": [...],
      "completions": [...],
      "reflections": [...]
    }
  },
  "reflections": [...]
}
```

### 智能体展示模板
```
本周情况（{start_date} 至 {end_date}）

【本周概览】
- 总任务数：{total_plans} 项
- 已完成：{completed} 项
- 完成率：{completion_rate}%

【每日记录】
{循环 daily_data}

📅 {date}
  计划：{plans.length} 项，完成 {completions.length} 项
  反思：{reflections.length} 条

【全部反思】
{循环 reflections}
{date}: {content}
```

## 按类别查询

### 命令
```bash
python scripts/weekly_planner.py query_by_category --year <年份> --week <周次> --category "<类别>"
```

### 输出格式
```json
{
  "success": true,
  "category": "work",
  "summary": {
    "total": 8,
    "completed": 7,
    "completion_rate": 87.5
  },
  "plans": [...],
  "completions": [...]
}
```

### 智能体展示模板
```
{category} 类别任务

【统计】
- 总数：{total} 项
- 已完成：{completed} 项
- 完成率：{completion_rate}%

【任务列表】
{循环 plans}
{status} ID{id} - {task}
  日期：{assigned_date}

【完成记录】
{循环 completions}
✓ {task}（{completed_date}）
  备注：{notes}
```

## 注意事项
1. 查询结果中已删除的任务（deleted=true）会被自动过滤
2. completion_rate 保留两位小数
3. 智能体应根据数据内容动态调整展示格式
4. 对于空数据（如无计划、无反思），应友好提示
