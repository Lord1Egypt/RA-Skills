---
name: temporal-time-manager
description: 时间管理 AI 助手 Skill，让 AI 通过对话直接管理你的任务、日程和灵感，数据同步至 aitimemg.cn 平台。
version: 1.0.1
author: PANGKAIFENG
homepage: https://www.aitimemg.cn
license: MIT
metadata:
  openclaw:
    requires:
      - mcporter
    env:
      - name: TEMPORAL_BASE_URL
        description: 你的 API 地址（默认 https://api.aitimemg.cn）
        default: "https://api.aitimemg.cn"
      - name: TEMPORAL_API_TOKEN
        description: 在 aitimemg.cn 生成的 API Token（用于身份认证）
        required: true
    data_policy:
      stores_data: true
      data_location: "阿里云（中国大陆）"
      data_shared_with_third_parties: false
      delete_account_url: "https://www.aitimemg.cn/settings"
---

# 时间管理 AI Skill

这个 Skill 让你的 AI 助手直接操作你在 [aitimemg.cn](https://www.aitimemg.cn) 的时间管理数据。

## 功能列表

| 工具名            | 说明                               |
| ----------------- | ---------------------------------- |
| `list_tasks`      | 获取所有任务                       |
| `create_task`     | 创建一个新任务                     |
| `update_task`     | 更新任务（标题、状态、截止日期等） |
| `delete_task`     | 删除指定任务                       |
| `list_schedules`  | 获取所有日程安排                   |
| `create_schedule` | 创建新日程                         |
| `update_schedule` | 更新日程                           |
| `delete_schedule` | 删除日程                           |
| `capture_idea`    | 快速捕获一条灵感/备忘              |

## 快速开始

### 1. 安装到你的 OpenClaw 机器人

```bash
openclaw skill install PANGKAIFENG/temporal-time-manager
```

### 2. 获取你的 API Token

1. 打开 [aitimemg.cn/settings](https://www.aitimemg.cn/settings)
2. 找到「🔑 API Token」板块，点击 **「生成 API Token」**
3. 复制生成的 Token（格式：`tmg_...`），**仅在生成时显示完整值，请立即保存**

### 3. 配置环境变量

在你的 OpenClaw 环境或 `.env` 文件中设置：

```bash
TEMPORAL_API_TOKEN=tmg_你的token     # 在 aitimemg.cn/settings 生成
TEMPORAL_BASE_URL=https://api.aitimemg.cn  # 可不填，默认即是
```


### 3. 开始对话

对话示例：

```
你：帮我查看今天的任务列表
助手：[调用 list_tasks] 你好，这是你今天的任务...

你：创建一个任务：明天下午3点开周会
助手：[调用 create_task] 已为你创建任务...

你：记录一个灵感：考虑接入 Notion 同步
助手：[调用 capture_idea] 已保存到你的灵感池...
```

## 使用方式（通过 mcporter）

```bash
# 列出任务
mcporter call temporal-time-manager list_tasks

# 创建任务
mcporter call temporal-time-manager create_task --args '{"title":"开会","due_date":"2026-02-28","priority":"high"}'

# 捕获灵感
mcporter call temporal-time-manager capture_idea --args '{"content":"这是一个灵感"}'
```

## 数据结构说明

### Task（任务）
- `id`: 唯一标识（UUID，调用方必须传入）
- `title`: 任务标题（必填）
- `notes`: 备注/描述
- `status`: 状态，可选值：`todo` / `done` / `abandoned`
- `group`: 四象限分类
  - `urgent_important`：重要且紧急
  - `important`：重要不紧急
  - `urgent`：紧急不重要
  - `neither`：不重要不紧急（默认）
- `executor_type`: 执行方式，可选值：`human`（纯人工）/ `ai_copilot`（AI协作）/ `ai_auto`（AI全自动）
- `project_id`: 所属项目 ID（可选）
- `created_at` / `updated_at`: 时间戳（ISO 8601，建议传入）

### Schedule（日程排班）
> 日程是"任务在某天某时段的排班记录"，与任务通过 `task_id` 关联。

- `id`: 唯一标识（UUID，调用方必须传入）
- `task_id`: 关联任务 ID（必填）
- `date`: 排班日期，格式 `YYYY-MM-DD`（必填）
- `planned_start`: 计划开始时间，**以小时为单位**（如 `9.5` = 09:30，`15.0` = 15:00）（必填）
- `planned_duration`: 计划时长，**以小时为单位**（如 `1.0` = 1小时，`1.5` = 90分钟）（必填）
- `is_all_day`: 是否全天任务（`true` 表示放入"今日待排班"槽，此时 `planned_start` 传 `0`）

### Idea（灵感/备忘）
- `id`: 唯一标识（UUID，后端自动生成）
- `content`: 内容文字（必填）
- `source`: 来源，如 `openclaw` / `feishu` / `web`（默认 `openclaw`）
- `meta`: 附加元数据（可选 JSON 对象）

