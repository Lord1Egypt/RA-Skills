---
name: tapd
description: 当用户需要查询、创建或更新 TAPD 需求、任务、缺陷、评论、工作流、迭代、测试用例、Wiki、工时、发布计划，或发送企业微信通知时使用本 Skill。使用 Python 标准库调用 TAPD 开放 API，不依赖 MCP 或第三方 HTTP 库。
homepage: https://www.tapd.cn
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "bins": [], "env": ["TAPD_ACCESS_TOKEN"] },
        "primaryEnv": "TAPD_ACCESS_TOKEN",
        "install": [],
      },
  }
---

# TAPD Skill

通过 TAPD 开放 API 完成需求/任务/缺陷/评论/迭代/用例/Wiki/工时等操作。本 Skill 不依赖 MCP 服务，由 AI 根据以下说明直接构造 HTTP 请求（或使用本 Skill 附带的仅标准库 Python 脚本）。

## 何时使用

- 获取用户参与的项目列表（未指定 workspace_id 时）
- 查询、创建、更新需求（stories）或任务（tasks）
- 查询、创建、更新缺陷（bugs）
- 获取或添加、更新评论（comments）
- 获取自定义字段配置（需求/任务/迭代/测试用例）
- 获取需求/任务/缺陷中的图片下载链接或附件信息
- 获取工作流流转、状态映射、结束状态及工作项类型
- 获取需求字段中英文与候选值（get_fields_lable、get_fields_info）
- 获取项目信息、迭代列表，创建或更新迭代
- 获取需求关联的缺陷、创建需求与缺陷的关联关系（relations）
- 查询、创建、批量创建测试用例（tcases）
- 查询、创建、更新 Wiki（tapd_wikis）
- 获取用户待办（todo）
- 查询、新建、更新工时（timesheets）
- 获取发布计划（releases）、获取提交关键字（get_scm_copy_keywords）
- 发送企业微信群消息（需配置 BOT_URL）

## 环境与认证

| 变量名 | 必填 | 说明 |
|--------|------|------|
| TAPD_ACCESS_TOKEN | 二选一 | 个人访问令牌，推荐 |
| TAPD_API_USER | 二选一 | API 账号（与 TAPD_API_PASSWORD 搭配） |
| TAPD_API_PASSWORD | 二选一 | API 密码 |
| TAPD_API_BASE_URL | 可选 | API 根地址，默认 `https://api.tapd.cn` |
| TAPD_BASE_URL | 可选 | 前端地址，用于生成需求/任务/缺陷等链接，默认 `https://www.tapd.cn` |
| BOT_URL | 可选 | 企业微信机器人 webhook，仅发送群消息时需要 |
| CURRENT_USER_NICK | 可选 | 当前用户昵称，未传 nick 时用于参与项目、待办、工时等查询 |

### 请求规范

- **URL**：所有请求在 base 后追加 `?s=mcp`（若 URL 已有 query 则用 `&s=mcp`）。例如：`GET {TAPD_API_BASE_URL}/stories?s=mcp`。
- **Headers**：
  - 认证二选一：`Authorization: Bearer <TAPD_ACCESS_TOKEN>` 或 `Authorization: Basic <base64(TAPD_API_USER:TAPD_API_PASSWORD)>`
  - `Content-Type: application/json`
  - `Via: mcp`
- **Body**：POST 请求使用 JSON；GET 参数放在 query string。

## ID 规则（短号转长号）

TAPD 部分接口接受短 ID（≤9 位数字）。调用前需转为长 ID：

- 云环境（`TAPD_API_BASE_URL` 包含 `api.tapd.cn`）：前缀 `11`；否则前缀 `10`。
- 格式：`{prefix}{workspace_id}{id.zfill(9)}`。例如 workspace_id=123，短 id=456 → `1012300000456` 或 `1112300000456`。
- 多 ID 逗号分隔时，逐个转换后再用逗号拼接。

涉及 id 转换的常见场景：stories/tasks 的 id、bugs 的 id、comments 的 entry_id、get_scm_copy_keywords 的 object_id 等。

## 操作清单（API 端点与参数）

以下为语义说明与对应 HTTP 方法、端点及主要参数。详细参数见 [reference/api_reference.md](./reference/api_reference.md)。

| 能力 | 方法 | 端点 | 主要参数/说明 |
|------|------|------|----------------|
| 获取用户参与项目 | GET | workspaces/user_participant_projects | params: nick。过滤 category=organization。 |
| 获取需求或任务 | GET | stories 或 tasks | params: workspace_id, entity_type(stories/tasks), page, limit, id, name, status, fields 等。使用 custom_field_* 前先调自定义字段配置。 |
| 获取需求/任务数量 | GET | stories/count 或 tasks/count | params: workspace_id 及与列表相同的筛选条件。 |
| 创建/更新需求或任务 | POST | stories 或 tasks | body: workspace_id, name(创建必填), id(更新必填), entity_type, description 等。 |
| 获取实体自定义字段配置 | GET | {entity_type}/custom_fields_settings | entity_type: stories / tasks / iterations / tcases。params: workspace_id。 |
| 获取图片下载链接 | GET | files/get_image | params: workspace_id, image_path(必填)。 |
| 获取附件信息/下载 | GET | attachments；下载 attachments/down | params: workspace_id, entry_id, type(story/bug) 等。 |
| 获取缺陷 | GET | bugs | params: workspace_id, page, limit, id, title, status, fields 等。 |
| 获取缺陷数量 | GET | bugs/count | params: workspace_id 及筛选条件。 |
| 创建/更新缺陷 | POST | bugs | body: workspace_id, title(创建必填), id(更新必填) 等。 |
| 获取评论 | GET | comments | params: workspace_id, entry_id, entry_type, page, limit 等。 |
| 添加评论 | POST | comments | body: workspace_id, entry_id, entry_type(bug/stories/tasks 等), author, description。 |
| 更新评论 | POST | comments | body: workspace_id, id, description, change_creator。 |
| 工作流流转细则 | GET | workflows/all_transitions | params: workspace_id, system(story/bug), workitem_type_id。 |
| 工作流状态中英文映射 | GET | workflows/status_map | params: 同上。 |
| 工作流结束状态 | GET | workflows/last_steps | params: workspace_id, system, workitem_type_id, type(可选)。 |
| 工作项类型列表 | GET | workitem_types | params: workspace_id。 |
| 需求字段中英文 | GET | stories/get_fields_lable | params: workspace_id。 |
| 需求字段及候选值 | GET | stories/get_fields_info | params: workspace_id。 |
| 项目信息 | GET | workspaces/get_workspace_info | params: workspace_id。 |
| 获取迭代 | GET | iterations | params: workspace_id, id, name 等。 |
| 创建/更新迭代 | POST | iterations | body: workspace_id, name/startdate/enddate/creator(创建必填), id/current_user(更新必填) 等。 |
| 需求关联缺陷 | GET | stories/get_related_bugs | params: workspace_id, story_id。 |
| 创建需求与缺陷关联 | POST | relations | body: workspace_id, source_type, target_type, source_id, target_id。 |
| 获取测试用例 | GET | tcases | params: workspace_id, page, limit 等。 |
| 创建/更新单条用例 | POST | tcases | body: workspace_id, name 等。 |
| 批量创建用例 | POST | tcases/batch_save | body: 数组，每项含 workspace_id, name 等，最多 200 条。 |
| 获取 Wiki | GET | tapd_wikis | params: workspace_id, page, limit 等。 |
| 创建/更新 Wiki | POST | tapd_wikis | body: workspace_id, name, markdown_description, creator 等；更新带 id。 |
| 获取待办 | GET | users/todo/{user_nick}/{entity_type} | entity_type: story/bug/task。 |
| 获取工时 | GET | timesheets | params: workspace_id, entity_type, entity_id, owner, spentdate 等。 |
| 新建/更新工时 | POST | timesheets | body: workspace_id, entity_type, entity_id, timespent, owner, spentdate(新建)；更新带 id。 |
| 发布计划 | GET | releases | params: workspace_id, id, name, startdate, enddate 等。 |
| 提交关键字 | GET | svn_commits/get_scm_copy_keywords | params: workspace_id, object_id, type(story/task/bug)。 |
| 需求分类 ID | GET | story_categories | params: workspace_id, name 等。 |
| 用户信息 | GET | users/info | 用于解析当前用户 nick。 |
| 企业微信消息 | POST | BOT_URL（非 TAPD） | body: msgtype 为 markdown 或 markdown_v2，content 为消息内容；含 @ 时用 markdown，否则可用 markdown_v2。 |

## 链接格式（供返回给用户）

- 需求：`{TAPD_BASE_URL}/{workspace_id}/prong/stories/view/{id}`
- 任务：`{TAPD_BASE_URL}/{workspace_id}/prong/tasks/view/{id}`
- 缺陷：`{TAPD_BASE_URL}/{workspace_id}/bugtrace/bugs/view/{id}`
- 迭代：`{TAPD_BASE_URL}/{workspace_id}/prong/iterations/card_view/{id}`
- 测试用例：`{TAPD_BASE_URL}/{workspace_id}/sparrow/tcase/view/{id}`
- Wiki：`{TAPD_BASE_URL}/{workspace_id}/markdown_wikis/show/#{id}`

## 示例流程

### 示例 1：先取自定义字段配置再按自定义字段查需求

1. 调用 `GET {entity_type}/custom_fields_settings?workspace_id={workspace_id}`，其中 entity_type 为 `stories`（需求）或 `tasks`（任务）。
2. 从返回中确认 custom_field_* 的字段名。
3. 调用 `GET stories`（或 `tasks`），params 包含 `workspace_id`、`entity_type`、以及 `custom_field_1` 等查询条件；需要详情时加 `fields=description,...`。

### 示例 2：创建需求并填写工时

1. 调用 `POST stories`，body 含 `workspace_id`、`name`、可选 `description`、`owner`、`iteration_id` 等；记下返回的需求 id。
2. 调用 `POST timesheets`，body 含 `workspace_id`、`entity_type=story`、`entity_id`、`timespent`、`owner`、`spentdate`（YYYY-MM-DD）。

## 命令行调用方式（推荐 AI 使用）

在配置好环境变量（TAPD_ACCESS_TOKEN 或 TAPD_API_USER/TAPD_API_PASSWORD；TAPD_API_BASE_URL 可选，默认云环境）后，使用 **python3** 运行脚本（脚本仅用标准库）。输出为 JSON 到 stdout，便于解析。

```bash
# 获取用户参与的项目（nick 默认取环境变量 CURRENT_USER_NICK）
python3 {baseDir}/scripts/tapd_client_stdlib.py projects [--nick 用户昵称]

# 获取项目信息
python3 {baseDir}/scripts/tapd_client_stdlib.py workspace --workspace-id <项目ID>

# 获取需求或任务列表（--entity-type 默认 stories）
python3 {baseDir}/scripts/tapd_client_stdlib.py stories --workspace-id <项目ID> [--entity-type stories|tasks] [--limit 10] [--page 1] [--id ID] [--name 标题] [--status 状态] [--fields id,name,description]

# 获取缺陷列表
python3 {baseDir}/scripts/tapd_client_stdlib.py bugs --workspace-id <项目ID> [--limit 10] [--page 1] [--id ID] [--title 标题]

# 获取迭代列表
python3 {baseDir}/scripts/tapd_client_stdlib.py iterations --workspace-id <项目ID> [--limit 30] [--page 1] [--name 迭代名]

# 获取发布计划列表
python3 {baseDir}/scripts/tapd_client_stdlib.py releases --workspace-id <项目ID> [--limit 30] [--page 1]

# 通用 GET（任意端点，-p 可多次）
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "stories/count" -p workspace_id=<项目ID> -p entity_type=stories
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "workspaces/user_participant_projects" -p nick=用户昵称

# 通用 POST（请求体为 JSON 或 -p key=val 多组）
python3 {baseDir}/scripts/tapd_client_stdlib.py post --endpoint "stories" -b '{"workspace_id":123,"name":"需求标题","entity_type":"stories"}'
python3 {baseDir}/scripts/tapd_client_stdlib.py post --endpoint "comments" -p workspace_id=123 -p entry_id=xxx -p entry_type=stories -p author=昵称 -p description=内容
```

**说明**：未列出的能力（如评论、工作流、Wiki、工时、企业微信等）可通过 `get` / `post` 子命令配合 [reference/api_reference.md](./reference/api_reference.md) 中的端点与参数自行拼装调用。

### 安全与权限建议

- **TAPD_ACCESS_TOKEN**：建议在 TAPD 开放平台中为该技能创建**最小权限、短期有效**的令牌（仅授予所需项目/接口权限，并设置较短过期时间），避免使用高权限长期令牌。
- **BOT_URL / TAPD_API_BASE_URL**：使用前请确认 `BOT_URL`（企业微信 webhook）和自定义的 `TAPD_API_BASE_URL` 均指向**可信端点**（如 TAPD 官方 `https://api.tapd.cn` 或贵司自建 TAPD、企业微信官方 webhook 地址），避免指向不可信第三方。
- **可选加固**：若需更强安全，可在沙盒环境中运行本脚本，并限制网络仅允许访问 TAPD API 与 BOT_URL（例如通过防火墙或容器网络策略），以确认脚本仅与预期端点通信。

### API key / 环境变量

- `TAPD_ACCESS_TOKEN` 环境变量（推荐）；或使用 `TAPD_API_USER` + `TAPD_API_PASSWORD`。
- OpenClaw 中可设置 `skills.tapd.env.TAPD_ACCESS_TOKEN` 于 `~/.openclaw/openclaw.json`。

## 使用脚本（可选）

本 Skill 提供仅使用 Python 标准库的客户端脚本 [scripts/tapd_client_stdlib.py](./scripts/tapd_client_stdlib.py)，使用 **python3 {baseDir}/scripts/tapd_client_stdlib.py** 运行。可从环境变量读取配置并封装通用 request 及部分高频接口；支持上述**命令行调用**与 Python 内 import 两种方式。

## 注意事项

- 使用 custom_field_* 前必须先调用对应实体类型的 custom_fields_settings 接口获取配置。
- 任务状态仅三种：open（未开始）、progressing（进行中）、done（已完成）；需求状态需通过 get_workflows_status_map / get_stories_fields_info 获取项目配置。
- 测试用例的 precondition、steps、expectation 可传纯文本；若需富文本，由调用方自行转换为 HTML，本 Skill 不依赖 markdown 库。
