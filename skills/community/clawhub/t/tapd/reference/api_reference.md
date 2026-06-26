# TAPD API 参考

本文档为 TAPD 开放 API 的端点与参数速查，配合 [SKILL.md](../SKILL.md) 使用。所有请求需在 base URL 后加 `?s=mcp`（或 `&s=mcp`），并携带认证与 `Via: mcp` 等 Header。

## 通用说明

- **Base URL**：环境变量 `TAPD_API_BASE_URL`，默认 `https://api.tapd.cn`（未设置时使用该默认值）。
- **认证**：`Authorization: Bearer <token>` 或 `Authorization: Basic <base64(user:password)>`。
- **分页**：多数列表接口支持 `page`、`limit`（如 limit 默认 10 或 30，最大 200）。
- **返回结构**：常见为 `{ "status": 1, "data": {...} 或 [...], "info": "..." }`；列表常在 `data` 下，单条如 `data.Story`、`data.Bug`、`data.Task`、`data.Iteration` 等。

---

## 项目与用户

| 方法 | 端点 | 主要参数 | 说明 |
|------|------|----------|------|
| GET | workspaces/user_participant_projects | nick | 用户参与的项目；过滤 category=organization。 |
| GET | workspaces/get_workspace_info | workspace_id | 项目信息。 |
| GET | users/info | — | 当前用户信息（含 nick）。 |

---

## 需求与任务（stories / tasks）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | stories 或 tasks | workspace_id, entity_type(stories/tasks), page, limit, id, name, status, v_status, category_id, iteration_id, owner, fields 等 | 列表；id 支持多值逗号；短 id 需转长 id。 |
| GET | stories/count 或 tasks/count | 同列表筛选条件 | 数量。 |
| POST | stories 或 tasks | workspace_id, name(创建必填), id(更新必填), entity_type, description, owner, iteration_id, priority_label 等 | 创建/更新；description 可传 HTML。 |
| GET | stories/custom_fields_settings?workspace_id= | workspace_id | 需求自定义字段配置。 |
| GET | tasks/custom_fields_settings?workspace_id= | workspace_id | 任务自定义字段配置。 |
| GET | stories/get_fields_lable?workspace_id= | workspace_id | 需求字段中英文。 |
| GET | stories/get_fields_info?workspace_id= | workspace_id | 需求字段及候选值。 |

---

## 缺陷（bugs）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | bugs | workspace_id, page, limit, id, title, status, priority_label, severity, fields 等 | 列表；id 需转长 id。 |
| GET | bugs/count | workspace_id 及筛选条件 | 数量。 |
| POST | bugs | workspace_id, title(创建必填), id(更新必填), description, status, current_owner, reporter 等 | 创建/更新。 |
| GET | bugs/custom_fields_settings?workspace_id= | workspace_id | 缺陷自定义字段配置。 |

---

## 评论（comments）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | comments | workspace_id, entry_id, entry_type(bug/stories/tasks 等), author, page, limit, order 等 | 列表。 |
| POST | comments | workspace_id, entry_id, entry_type, author, description；更新时 id, change_creator | 添加/更新评论；entry_id 短号需转长 id。 |

---

## 附件与图片

| 方法 | 端点 | 主要参数 | 说明 |
|------|------|----------|------|
| GET | files/get_image | workspace_id, image_path(必填) | 单张图片下载链接。 |
| GET | attachments | workspace_id, entry_id, type(story/bug) | 附件列表含 download_url。 |
| GET | attachments/down | workspace_id, id(附件 id) | 附件下载。 |

---

## 工作流与工作项类型

| 方法 | 端点 | 主要参数 | 说明 |
|------|------|----------|------|
| GET | workflows/all_transitions | workspace_id, system(story/bug), workitem_type_id | 流转细则。 |
| GET | workflows/status_map | workspace_id, system, workitem_type_id | 状态中英文映射。 |
| GET | workflows/last_steps | workspace_id, system, workitem_type_id, type(可选) | 结束状态。 |
| GET | workitem_types | workspace_id | 需求类别列表。 |

---

## 迭代（iterations）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | iterations | workspace_id, id, name, status 等 | 列表。 |
| POST | iterations | workspace_id, name, startdate, enddate, creator(创建)；id, current_user(更新) | 创建/更新；status: open/done。 |
| GET | iterations/custom_fields_settings?workspace_id= | workspace_id | 迭代自定义字段配置。 |

---

## 需求分类与关联

| 方法 | 端点 | 主要参数 | 说明 |
|------|------|----------|------|
| GET | story_categories | workspace_id, name | 需求分类，用于得到 category_id。 |
| GET | stories/get_related_bugs | workspace_id, story_id | 需求关联的缺陷 id。 |
| POST | relations | workspace_id, source_type, target_type, source_id, target_id | 创建需求与缺陷关联。 |

---

## 测试用例（tcases）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | tcases | workspace_id, page, limit, id, name, category_id, status 等 | 列表。 |
| GET | tcases/count | 同列表条件 | 数量。 |
| POST | tcases | workspace_id, name, category_id, status, precondition, steps, expectation 等 | 单条创建/更新。 |
| POST | tcases/batch_save | body 为数组，每项含 workspace_id, name 等 | 批量创建，最多 200 条。 |
| GET | tcases/custom_fields_settings?workspace_id= | workspace_id | 用例自定义字段配置。 |

---

## Wiki（tapd_wikis）

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | tapd_wikis | workspace_id, page, limit, id, name 等 | 列表。 |
| GET | tapd_wikis/count | 同列表条件 | 数量。 |
| POST | tapd_wikis | workspace_id, name, markdown_description, creator；更新带 id | 创建/更新。 |

---

## 待办与工时

| 方法 | 端点 | 主要参数/Body | 说明 |
|------|------|----------------|------|
| GET | users/todo/{user_nick}/{entity_type} | entity_type: story/bug/task | 用户待办。 |
| GET | timesheets | workspace_id, entity_type, entity_id, owner, spentdate, page, limit 等 | 工时列表。 |
| POST | timesheets | workspace_id, entity_type, entity_id, timespent, owner, spentdate(新建)；id(更新) | 新建/更新工时。 |

---

## 发布与提交

| 方法 | 端点 | 主要参数 | 说明 |
|------|------|----------|------|
| GET | releases | workspace_id, id, name, startdate, enddate, status 等 | 发布计划。 |
| GET | svn_commits/get_scm_copy_keywords | workspace_id, object_id, type(story/task/bug) | 提交关键字；object_id 短号需转长 id。 |

---

## 企业微信（非 TAPD API）

- **URL**：环境变量 `BOT_URL`（机器人 webhook）。
- **方法**：POST，Body JSON。
- **格式**：消息含 `@` 时用 `msgtype: markdown`、`markdown.content`；否则可用 `msgtype: markdown_v2`、`markdown_v2.content`。
