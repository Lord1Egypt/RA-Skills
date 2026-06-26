# 工作日报模板

## 目录
- [概览](#概览)
- [日报结构](#日报结构)
- [智能体展示模板](#智能体展示模板)

## 概览
工作日报每天下午5点自动生成（工作日），或用户手动触发。日报包含当日计划、完成情况、反思内容和智能体生成的工作小结。

## 日报结构

### 命令
```bash
python scripts/weekly_planner.py generate_daily_report --year <年份> --week <周次> --date "<日期>"
```

### 输出格式
```json
{
  "success": true,
  "report_info": {
    "date": "YYYY-MM-DD",
    "weekday": "周三",
    "is_weekday": true,
    "generated_at": "YYYY-MM-DD HH:MM:SS"
  },
  "summary": {
    "total_plans": 5,
    "completed": 4,
    "completion_rate": 80.0
  },
  "priority_breakdown": {
    "high": {
      "total": 2,
      "completed": 2
    },
    "medium": {
      "total": 2,
      "completed": 2
    },
    "low": {
      "total": 1,
      "completed": 0
    }
  },
  "plans": [
    {
      "id": 1,
      "task": "完成项目报告",
      "category": "work",
      "assigned_date": "YYYY-MM-DD",
      "status": "completed",
      "priority": "high"
    }
  ],
  "completions": [
    {
      "task_id": 1,
      "task": "完成项目报告",
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

## 智能体展示模板

```
📊 工作日报
日期：{date}（{weekday}）
生成时间：{generated_at}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【进度统计】
• 计划任务：{total_plans} 项
• 已完成：{completed} 项
• 完成率：{completion_rate}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【按优先级统计】
高优先级：{high_completed}/{high_total} ✓
中优先级：{medium_completed}/{medium_total} ✓
低优先级：{low_completed}/{low_total} ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【当日计划】
{循环展示 plans}
{status_emoji} ID{id} - {task}
  类别：{category} | 优先级：{priority}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【当日完成】
{循环展示 completions}
✓ {task}
  完成时间：{completed_date}
  备注：{notes}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【当日反思】
{reflection.content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【工作小结】
{智能体基于数据生成的小结，包括：
- 今日亮点
- 存在问题
- 明日建议}
```

## 智能体工作小结生成指南

### 亮点提取
基于完成率和完成的任务类型，提取今日工作的亮点：
- 高优先级任务全部完成
- 完成率超过80%
- 完成了重要或困难任务

### 问题识别
基于未完成的任务和反思内容，识别问题：
- 低优先级任务未完成
- 完成率低于预期
- 反思中提到的困难或挑战

### 明日建议
基于今日数据和反思，提出明日建议：
- 优先处理未完成任务
- 保持高效工作的方法
- 调整时间分配

## 触发条件

### 自动触发
- 时间：每天17:00
- 条件：工作日（周一至周五）
- 流程：智能体检测时间 → 调用脚本 → 生成日报 → 展示

### 手动触发
- 用户请求："生成今日工作日报"或类似表达
- 流程：理解需求 → 调用脚本 → 生成日报 → 展示

## 注意事项
1. 周末（周六、周日）也支持手动生成日报，但不会自动触发
2. 日报基于query_today的数据，确保数据准确性
3. 工作小结应由智能体根据数据智能生成，提供个性化建议
4. 如当日无记录，应友好提示并建议用户添加记录
