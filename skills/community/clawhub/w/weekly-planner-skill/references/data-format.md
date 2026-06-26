# 周计划数据格式说明

## 目录
- [概览](#概览)
- [数据结构](#数据结构)
- [字段说明](#字段说明)
- [完整示例](#完整示例)
- [验证规则](#验证规则)

## 概览
周计划数据采用 JSON 格式存储，每周一个文件。文件命名规则：`week-{year}-W{week:02d}.json`（如 `week-2025-W12.json`）。

## 数据结构

```json
{
  "year": "年份（整数）",
  "week": "周次（整数，1-53）",
  "start_date": "周开始日期（YYYY-MM-DD格式，周一）",
  "end_date": "周结束日期（YYYY-MM-DD格式，周日）",
  "plans": [
    {
      "id": "任务ID（整数，从1开始递增）",
      "task": "任务描述（字符串）",
      "category": "任务类别（字符串：work/study/health/other）",
      "assigned_date": "分配日期（YYYY-MM-DD格式）",
      "status": "状态（字符串：pending/completed）",
      "priority": "优先级（字符串：high/medium/low）",
      "created_at": "创建时间（ISO8601格式）",
      "updated_at": "更新时间（ISO8601格式，可选）",
      "deleted": "是否已删除（布尔值，默认false）"
    }
  ],
  "completions": [
    {
      "task_id": "关联的任务ID（整数）",
      "task": "任务描述（字符串）",
      "category": "任务类别（字符串）",
      "assigned_date": "原分配日期（YYYY-MM-DD格式）",
      "completed_date": "完成时间（ISO8601格式）",
      "notes": "完成备注（字符串，可选）"
    }
  ],
  "reflections": [
    {
      "date": "日期（YYYY-MM-DD格式）",
      "content": "反思内容（字符串）",
      "created_at": "创建时间（ISO8601格式）",
      "updated_at": "更新时间（ISO8601格式，可选）"
    }
  ]
}
```

## 字段说明

### 顶层字段
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| year | integer | 是 | 年份，如2025 |
| week | integer | 是 | 周次，1-53（ISO周次标准） |
| start_date | string | 是 | 周一日期，格式YYYY-MM-DD |
| end_date | string | 是 | 周日日期，格式YYYY-MM-DD |
| plans | array | 是 | 计划任务列表 |
| completions | array | 是 | 完成记录列表 |
| reflections | array | 是 | 反思记录列表 |

### plans 数组元素字段
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | integer | 是 | 任务唯一标识，从1开始递增 |
| task | string | 是 | 任务描述 |
| category | string | 是 | 任务类别，可选值：work, study, health, other |
| assigned_date | string | 是 | 分配日期，格式YYYY-MM-DD，需在周范围内 |
| status | string | 是 | 状态，可选值：pending, completed |
| priority | string | 否 | 优先级，可选值：high, medium, low，默认medium |
| created_at | string | 是 | 创建时间，ISO8601格式 |
| updated_at | string | 否 | 最后更新时间，ISO8601格式，修改计划时自动更新 |
| deleted | boolean | 否 | 是否已删除，默认false。软删除标记，保留数据但不在查询中显示 |
| priority | string | 否 | 优先级，可选值：high, medium, low，默认medium |
| created_at | string | 是 | 创建时间，ISO8601格式 |

### completions 数组元素字段
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| task_id | integer | 是 | 关联的plans中的任务ID |
| task | string | 是 | 任务描述（复制自plans） |
| category | string | 是 | 任务类别（复制自plans） |
| assigned_date | string | 是 | 原分配日期（复制自plans） |
| completed_date | string | 是 | 实际完成时间，ISO8601格式 |
| notes | string | 否 | 完成备注，可记录进度、问题等 |

### reflections 数组元素字段
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| date | string | 是 | 反思日期，格式YYYY-MM-DD |
| content | string | 是 | 反思内容 |
| created_at | string | 是 | 创建时间，ISO8601格式 |
| updated_at | string | 否 | 最后更新时间，ISO8601格式 |

## 完整示例

```json
{
  "year": 2025,
  "week": 12,
  "start_date": "2025-03-17",
  "end_date": "2025-03-23",
  "plans": [
    {
      "id": 1,
      "task": "完成项目报告",
      "category": "work",
      "assigned_date": "2025-03-17",
      "status": "completed",
      "priority": "high",
      "created_at": "2025-03-17T10:00:00"
    },
    {
      "id": 2,
      "task": "学习Python高级特性",
      "category": "study",
      "assigned_date": "2025-03-18",
      "status": "pending",
      "priority": "medium",
      "created_at": "2025-03-17T10:05:00"
    },
    {
      "id": 3,
      "task": "跑步30分钟",
      "category": "health",
      "assigned_date": "2025-03-17",
      "status": "completed",
      "priority": "medium",
      "created_at": "2025-03-17T10:10:00"
    }
  ],
  "completions": [
    {
      "task_id": 1,
      "task": "完成项目报告",
      "category": "work",
      "assigned_date": "2025-03-17",
      "completed_date": "2025-03-17T15:30:00",
      "notes": "提前完成，质量良好"
    },
    {
      "task_id": 3,
      "task": "跑步30分钟",
      "category": "health",
      "assigned_date": "2025-03-17",
      "completed_date": "2025-03-17T07:00:00",
      "notes": ""
    }
  ],
  "reflections": [
    {
      "date": "2025-03-17",
      "content": "今天工作效率很高，上午完成了项目报告。早起跑步让我精力充沛。",
      "created_at": "2025-03-17T22:00:00"
    },
    {
      "date": "2025-03-18",
      "content": "下午有些分心，需要提高专注力。明天尝试番茄工作法。",
      "created_at": "2025-03-18T21:30:00"
    }
  ]
}
```

## 验证规则

### 必需字段检查
- 所有顶层字段必须存在
- 每个任务必须包含 id, task, category, assigned_date, status, created_at
- 完成记录必须包含 task_id, task, category, assigned_date, completed_date
- 反思记录必须包含 date, content, created_at

### 格式验证
- 年份：4位数字，如 2025
- 周次：1-53 范围内的整数
- 日期：YYYY-MM-DD 格式（如 2025-03-17）
- ISO8601时间：YYYY-MM-DDTHH:MM:SS 格式（如 2025-03-17T10:00:00）

### 逻辑验证
- assigned_date 必须在 start_date 和 end_date 范围内
- task_id 必须存在于 plans 数组中
- status 只能是 pending 或 completed
- category 只能是 work, study, health, other
- priority 只能是 high, medium, low

### 数据一致性
- completions 中的 task 必须与 plans 中的 task 保持一致
- completions 中的 category 和 assigned_date 必须与 plans 中的对应字段一致
- 同一周内任务ID必须唯一且连续（从1开始）
