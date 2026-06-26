# 数据结构定义

## todos_meta.json

元数据文件，记录统计信息：

```json
{
  "pending": 5,
  "in_progress": 2,
  "completed": 12,
  "lastUpdated": "2026-04-04T21:06:00Z"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| pending | number | 未开始数量 |
| in_progress | number | 进行中数量 |
| completed | number | 已完成数量 |
| lastUpdated | string | 最后更新时间 (ISO 8601) |

---

## 待办项结构

每个待办文件（`todos_pending.json`、`todos_in_progress.json`、`todos_completed.json`）都是数组：

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "完成项目文档",
    "createdAt": "2026-04-04T21:00:00Z",
    "status": "pending",
    "githubIssue": "https://github.com/owner/repo/issues/123",
    "paths": [
      {
        "path": "/Users/reilly/project-a",
        "branch": "main"
      },
      {
        "path": "/Users/reilly/docs",
        "branch": null
      }
    ],
    "completedAt": null
  }
]
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | UUID v4 |
| content | string | ✅ | 待办内容 |
| createdAt | string | ✅ | 创建时间 (ISO 8601) |
| status | string | ✅ | pending / in_progress / completed |
| githubIssue | string | ❌ | GitHub issue 完整链接 |
| paths | array | ❌ | 关联路径列表 |
| paths[].path | string | ✅ | 文件系统路径 |
| paths[].branch | string | ❌ | Git 分支名（非 git 项目为 null） |
| completedAt | string | ❌ | 完成时间 (ISO 8601)，仅在 completed 时有值 |

---

## 状态映射

| 状态 | 英文 | 文件 |
|------|------|------|
| 未开始 | `pending` | todos_pending.json |
| 进行中 | `in_progress` | todos_in_progress.json |
| 已完成 | `completed` | todos_completed.json |

---

## 初始化

首次使用时创建空文件：

```json
// todos_meta.json
{
  "pending": 0,
  "in_progress": 0,
  "completed": 0,
  "lastUpdated": null
}

// todos_pending.json
[]

// todos_in_progress.json
[]

// todos_completed.json
[]
```