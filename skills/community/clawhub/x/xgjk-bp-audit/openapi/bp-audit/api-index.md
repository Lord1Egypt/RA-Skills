# API 索引 — bp-audit（审计所需接口）

本模块包含 8 个查询接口和 2 个受控写入接口。

## 接口列表

### 基础查询（逐级下钻）

| # | 方法 | 接口 | 说明 | 脚本 action |
|---|------|------|------|------------|
| 1 | GET | `/bp/period/getAllPeriod` | 查询所有 BP 周期列表 | `get_all_periods` |
| 2 | GET | `/bp/group/getTree` | 获取某周期下的分组树 | `get_group_tree` |
| 3 | GET | `/bp/task/v2/getSimpleTree` | 获取某分组下的任务树 | `get_task_tree` |

### 详情查询

| # | 方法 | 接口 | 说明 | 脚本 action |
|---|------|------|------|------------|
| 4 | GET | `/bp/task/v2/getGoalAndKeyResult` | 获取目标详情（含 KR 和举措） | `get_goal_detail` |
| 5 | GET | `/bp/task/v2/getKeyResult` | 获取关键成果详情（含举措） | `get_key_result_detail` |
| 6 | GET | `/bp/task/v2/getAction` | 获取关键举措详情 | `get_action_detail` |

### 搜索

| # | 方法 | 接口 | 说明 | 脚本 action |
|---|------|------|------|------------|
| 7 | GET | `/bp/task/v2/searchByName` | 按名称模糊搜索任务 | `search_task` |
| 8 | GET | `/bp/group/searchByName` | 按名称模糊搜索分组 | `search_group` |

### 写入

| # | 方法 | 接口 | 说明 | 脚本 action |
|---|------|------|------|------------|
| 9 | POST | `/bp/task/v2/addKeyResult` | 根据目标 ID 新增关键成果 | `add_key_result` |
| 10 | POST | `/bp/task/v2/addAction` | 根据成果 ID 新增关键举措 | `add_action` |

## 公共说明

- **Base URL**：`https://sg-al-cwork-web.mediportal.com.cn/open-api`
- **认证**：所有请求需携带 `appKey` Header
- **ID 精度**：所有 ID 为 Long 类型（雪花算法），必须以字符串传递，严禁数值转换

## 通用响应结构

```json
{
  "resultCode": 1,
  "resultMsg": null,
  "data": null
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `resultCode` | Integer | `1` 表示成功，其他值表示失败 |
| `resultMsg` | String | 成功时为 `null`，失败时为错误描述 |
| `data` | T | 业务数据 |

## 公共数据结构

### BaseTaskVO（任务基础结构）

`GoalAndKeyResultVO`、`KeyResultVO`、`ActionVO` 均继承此结构。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Long | 任务 ID |
| `groupId` | Long | 所属分组 ID |
| `name` | String | 任务名称 |
| `statusDesc` | String | 任务状态（草稿/未启动/进行中/已关闭） |
| `reportCycle` | String | 汇报周期，格式: `{ruleType}+{index}` |
| `planDateRange` | String | 计划时间区间，格式: `yyyy-MM-dd ~ yyyy-MM-dd` |
| `taskUsers` | List | 任务参与人列表 |
| `taskDepts` | List | 任务参与部门列表 |
| `upwardTaskList` | List | 所有向上对齐任务 |
| `downTaskList` | List | 所有向下对齐任务 |
| `fullLevelNumber` | String | 任务完整编码 |

### TaskUserVO（任务参与人）

| 字段 | 类型 | 说明 |
|------|------|------|
| `taskId` | Long | 任务 ID |
| `role` | String | 角色：`承接人` / `协办人` / `抄送人` / `监督人` / `观察人` |
| `empList` | List | 该角色下的员工列表（含 `id`、`name`） |

### SimpleTaskVO（向上/向下对齐任务）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Long | 任务 ID |
| `name` | String | 任务名称 |
| `groupInfo` | Object | 所属分组信息（含 `id`、`name`） |

## 脚本映射

所有接口通过统一脚本调用：`../../scripts/bp-audit/bp_api.py`

### 写入参数速查

#### `add_key_result`

- 必填：`--goal_id`、`--name`
- 常用可选：`--rule_type`、`--required_index`、`--plan_start_date`、`--plan_end_date`、`--owner_ids`、`--owner_dept_ids`、`--collaborator_ids`、`--copy_to_ids`、`--supervisor_ids`、`--observer_ids`、`--upward_task_id_list`、`--weight`、`--description`、`--measure_standard`、`--action_plan`、`--upload_sp_file_dtos`、`--body_json`

#### `add_action`

- 必填：`--key_result_id`、`--name`
- 常用可选：`--rule_type`、`--required_index`、`--plan_start_date`、`--plan_end_date`、`--owner_ids`、`--upward_task_id_list`、`--weight`、`--description`、`--measure_standard`、`--upload_sp_file_dtos`、`--body_json`

### 参数约束

- 多 ID 参数使用逗号分隔字符串，例如 `--owner_ids "1001,1002"`
- `--upload_sp_file_dtos` 传 JSON 数组字符串
- `--body_json` 传 JSON 对象字符串；如果与显式参数同时提供，显式参数覆盖同名字段
- 写入前应先通过详情接口确认父任务 ID，避免误挂载

### 不给 ID 时的定位路径

- 新增关键成果：`period -> search_group -> search_task(type=目标) -> get_goal_detail(可选) -> add_key_result`
- 新增关键举措：`period -> search_group -> search_task(type=关键成果) -> get_key_result_detail(可选) -> add_action`
- `search_task` 若返回多个候选，必须先让用户确认，不能自动选择
- `search_task` 无结果时，才允许用 `get_task_tree` 在已定位的 `group_id` 下兜底查找
