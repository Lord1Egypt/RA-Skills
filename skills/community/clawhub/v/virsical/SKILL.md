---
name: virsical
display_name: Virsical办公助手
description: |
  Virsical 威思客智慧空间管理平台集成技能。适用于查询或预订会议、创建工单报修、查询访客记录。触发关键词：威思客、virsical、会议预订、工单报修、访客查询、meeting room booking、room reservation、visitor management、work order、facility management 等。支持中英双语交互。
disable: false
version: 1.0.5
---

# Virsical（威思客）智慧空间管理平台

## 概述

Virsical 是企业智慧空间管理平台，提供会议室预订、访客管理、工单报修等功能。
此技能通过 Python 脚本封装了完整的 OAuth2 认证流程和 REST API（含请求签名），以用户身份执行所有操作。

Base URL 不可硬编码，通过以下命令运行时获取：
```bash
python -c "from scripts.config import get_config; cfg = get_config(); print(cfg.base_url)"
```
所有时间使用 CST（UTC+8）时区。

## 执行原则

**每次执行业务操作前，必须完成三步预检：配置 → 认证 → License。** 使用 `session.ensure_ready(scene)` 一站式完成，
任一步失败则向用户展示阻断原因及下一步操作指引，不要继续执行业务请求。Token 在过期前 10 分钟自动刷新，无需用户干预。

**登录方式**：优先使用 Agent 授权码登录。首次使用或未登录时，提示用户按以下步骤获取授权码：打开浏览器访问威思客系统（https://www.virsical.com/guide.html），登录后点击右上角用户信息，找到「Agent授权码」并复制(Agent授权码属于敏感凭证，请不要发送给他人)；拿到授权码后调用 `exchange_agent_code_for_token(auth_code, cfg, tm)` 换取并保存 token。保留本地 OAuth 回调登录作为备用方案。

**语言自适应**：检测用户输入语言，所有面向用户的回复（引导语、提示信息、错误说明、表格标题、列名、状态描述、确认问题等）均使用与用户相同的语言。用户用中文则中文回复，用户用英文则英文回复。Python 脚本 `print` 输出的固定中文文本视为技术调试内容，无需翻译。

**呈现原则**：不要输出原始 API 响应的完整 JSON。提取关键信息以 Markdown 表格或列表等可读方式呈现。表格标题、列名、状态标签等须匹配用户语言。
---

### 🚫 功能边界（重要！必须遵守）

**核心原则：** 当用户询问的功能不在当前技能支持范围内时，**严禁猜测或尝试实现不存在的功能/接口**。应直接告知用户该功能不可用，并明确说明当前支持的功能范围。

---

**当前技能支持的功能：**

| 场景 | 支持的功能 | 不支持的功能 |
|------|-----------|-------------|
| 会议室管理 | 查询可用会议室、预订会议室、查看我的会议 | 修改预订、删除预订、会议室管理后台等 |
| 访客管理 | 查询访客记录 | 创建访客邀请、修改访客信息、删除访客记录等 |
| 工单报修 | 创建工单 | 查询工单列表、修改工单、删除工单、工单状态变更等 |

---

**如何回复用户：**

- 若用户询问不支持的功能，回复模板（中文）：
  > "抱歉，当前技能不支持「{用户询问的功能}」。本技能仅支持：查询/预订会议室、查看我的会议、查询访客记录、创建工单。如需其他功能，请登录 Virsical 网页端操作。"

- 若用户询问不支持的功能，回复模板（英文）：
  > "Sorry, this skill does not support「{user's requested feature}」. This skill only supports: query/book meeting rooms, view my meetings, query visitor records, create work orders. For other features, please log in to Virsical web portal."

---

**示例：**
- 用户问："如何查询工单列表？" → 回复："抱歉，当前技能不支持查询工单列表，只支持创建工单。如需查看工单，请登录 Virsical 网页端操作。"
- 用户问："怎么删除会议预订？" → 回复："抱歉，当前技能不支持删除会议预订，只支持查询和预订会议室。如需修改或删除预订，请登录 Virsical 网页端操作。"

## 预检与认证

### 一站式预检

`session.ensure_ready(scene)` 是统一的预检入口，依次检查：

1. 配置：Base URL 等基础配置是否完整
2. 认证：Token 是否存在且有效（本地 + 服务端双重验证）
3. License：用户是否拥有目标场景的产品许可

```bash
python -c "from scripts.session import ensure_ready; import json; result = ensure_ready('<scene>'); print(json.dumps(result, ensure_ascii=False, indent=2))"
```

返回值中 `ready` 为 `true` 方可继续。若 `ready` 为 `false`，根据 `step` 字段判断阻断位置并引导用户：

| step | 含义 | 处理方式 |
|------|------|---------|
| `auth` | 需要登录 | 按以下步骤引导用户获取授权码：1）打开浏览器访问威思客系统（https://www.virsical.com/guide.html）；2）登录后点击右上角用户信息，找到「Agent授权码」并复制；3）将授权码粘贴到当前对话。收到授权码后执行 Agent 授权码登录 |
| `license` | 无权限 | 告知用户缺少的目标场景许可，停止操作 |

### 配置说明

OAuth 凭证已使用固定值，无需用户配置。Base URL 通过 config 获取，不可硬编码。

```bash
# 查看当前配置
python -c "from scripts.config import get_config; cfg = get_config(); print(f'Base URL: {cfg.base_url}')"
```

### 登录

登录前先执行智能预检——仅在 `should_login` 为 `true` 时才发起登录：

```bash
python -c "from scripts.config import get_config, reset_config; reset_config(); from scripts.auth_manager import TokenManager, check_token_before_login; import json; cfg = get_config(); tm = TokenManager(cfg); result = check_token_before_login(tm); print(json.dumps(result, ensure_ascii=False))"
```

**Agent 授权码登录**（推荐）：当 `ensure_ready` 返回 `step=auth` 时，执行以下流程：

1. 向用户提示：「请按以下步骤获取授权码：
   - 打开浏览器，访问威思客系统：https://www.virsical.com/guide.html
   - 登录您的账号后，点击右上角的用户信息，找到「Agent授权码」，复制授权码
   - 将授权码粘贴到这里 👇」
2. 用户粘贴授权码到对话中
3. 调用 `exchange_agent_code_for_token(auth_code, cfg, tm)` 换取 token 并保存
4. 成功后友好提示「登录成功！欢迎，{realname}」（优先使用 token 中的 `realname`，其次 `username`）

Agent 授权码登录命令：

```bash
# 使用授权码登录（auth_code 为用户粘贴的授权码）
python -c "from scripts.config import get_config, reset_config; reset_config(); from scripts.auth_manager import TokenManager, exchange_agent_code_for_token; import json; cfg = get_config(); tm = TokenManager(cfg); result = exchange_agent_code_for_token('<auth_code>', cfg, tm); print(json.dumps(result, ensure_ascii=False))"
```

**本地 OAuth 登录**（备用）：`local_login(cfg, tm)` — 启动本地回调服务器并自动打开浏览器，**默认阻塞等待**回调完成（最多 10 分钟）。

**不要重复登录。** Token 会在过期前 10 分钟自动刷新；API 返回 401 时自动尝试刷新并重试一次，刷新失败才提示重新登录。

### Agent 认证配置

Agent 授权码登录通过 `getAgentToken` 接口换取 token，无需额外配置即可使用。可选配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `VIRSICAL_AGENT_AUTH_BASE_URL` | Agent 认证服务地址 | 同 Base URL（通过 config 获取） |

### License 与场景对应

| 产品码 | 场景标识 | 场景名称 | 涉及工作流 |
|--------|---------|---------|-----------|
| `smt` | `meeting` | 会议管理 | 会议室查询/预订/我的会议 |
| `vst` | `visitor` | 访客管理 | 访客查询 |
| `fm` | `requirement` | 报事报修 | 工单创建 |

无 license 时明确告知用户对应场景的许可缺失，联系管理员开通。

## 工作流

> 具体可执行命令参见 `references/commands.md`。每个命令前已确保通过 `ensure_ready(scene)` 预检。

### 会议室查询（scene: meeting）

当用户想查看可用会议室时，调用 `meeting.query_available_rooms(capacity_min, capacity_max)`。
该函数合并了详情接口和占用状态接口，自动按区域分组、显示容量分布、标注设备信息和今日空闲时段。

- 用户指定人数范围时传 `capacity_min` / `capacity_max` 自动筛选
- 也可直接用 `meeting.check_room_occupancy(start_time, end_time, ...)` 按时间段查询

**呈现策略**：Markdown 表格（区域 | 会议室 | 容量），顶部显示容量分布汇总。

### 会议室预订（scene: meeting）

调用 `meeting.book_meeting(room_id, title, start_time, end_time, ...)`。

**title 默认值**：如果用户未指定会议标题，或标题为空/为占位值（如"会议"/"Meeting"），**禁止手动构造 title，直接调用 `book_meeting` 时不传 `title` 参数（或传 `None`）**，函数内部会自动根据 token 中的 `realname` 生成 `"{realname}的会议"`（中文）或 `"{realname}'s Meeting"`（英文）。切勿使用 `ensure_ready` 返回的 `username`（UUID）手动拼接标题。

预订流程：
1. 向用户确认：偏好（名称/容量/位置）、时间（ISO 8601 格式如 `2026-06-02T14:00:00+08:00`）、会议标题（可选，不提供则自动生成）
2. 先查询目标时段会议室占用状态，展示可用选项
3. 执行预订——`room_id` 支持名称或 ID 匹配
4. 反馈结果：成功则告知详情；冲突则展示原因并建议可用替代会议室

### 我的会议（scene: meeting）

调用 `meeting.list_meetings()` 查询当前用户的会议列表。

### 访客查询（scene: visitor）

调用 `visitor.list_visitors(visitor_name)` 查询访客记录，默认查过去 30 天到未来 30 天。
结果包含访客姓名、到访时间、邀请人、状态（已签到/已签出/审批中等）、联系电话。

### 工单创建（scene: requirement）

调用 `requirement.create_requirement(project_id, content, requirement_type_id, priority)`。

创建流程：
1. 调用 `requirement.get_requirement_params()` 获取可选项目、工单类型、优先级列表
2. 引导用户从参数列表中选择项目 ID、工单类型 ID、优先级。如果用户描述中已明确包含报修信息（如设备故障、不制冷等），且只有单个项目/类型可选，则直接推断执行，无需逐项确认
3. 执行创建——所有 ID 参数为整数，优先级 ID 通过 `get_requirement_params()` 返回的 `priority` 列表中的 `priorityName` 对应匹配获取

**优先级处理规则**：
- 优先级 ID 从 `get_requirement_params()` 接口返回的 `data.priority` 列表动态获取，根据 `priorityName` 匹配对应的 `id`
- 支持传入优先级 ID（整数/字符串）或别名（"high"/"medium"/"low"）
- 别名映射："high"→"紧急", "medium"→"普通", "low"→"预约"

**呈现规范**：工单创建成功后，**必须以 Markdown 表格**呈现。字段标签根据用户语言选择对应版本：

**中文呈现：**

| 字段 | 内容 |
|------|------|
| **工单编号** | `{data.requirementNo}` |
| **项目** | `{data.projectName}` |
| **类型** | `{data.typeName}` |
| **优先级** | `{data.priorityName}` |
| **内容** | `{data.content}` |
| **状态** | ✅ 已创建 |

**英文呈现：**

| Field | Details |
|------|------|
| **Ticket No.** | `{data.requirementNo}` |
| **Project** | `{data.projectName}` |
| **Type** | `{data.typeName}` |
| **Priority** | `{data.priorityName}` |
| **Description** | `{data.content}` |
| **Status** | ✅ Created |

`data` 字段直接取自 `create_requirement` 返回结果中的 `data` 对象。

### 登出

当用户明确要求登出时，调用 `TokenManager.logout()` 清除本地 token 并调用服务端登出接口。

## 时间格式

| 用途 | 格式 | 示例 |
|------|------|------|
| 会议室时间 | ISO 8601 + 时区 | `2026-06-02T14:00:00+08:00` |
| 访客时间 | 毫秒 Unix 时间戳 | `1717335600000` |

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| Token 无效/过期 | 自动刷新或引导重新登录 |
| 签名错误（101040/101043） | 检查系统时钟是否准确 |
| 业务错误 | 查阅 `references/error_codes.md` 向用户解释 |
| 网络错误 | 提示检查网络，建议稍后重试 |

## 参考资源

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| `references/commands.md` | 所有可执行命令片段 | 需要复制粘贴命令时 |
| `references/api_reference.md` | 完整 API 接口文档 | 需要了解具体 API 参数/响应时 |
| `references/error_codes.md` | 错误码映射表 | API 返回未知错误码时 |
| `references/auth_flow.md` | OAuth2 认证流程详解 | 调试认证问题 |
| `references/signature.md` | 请求签名算法 | 调试签名问题 |

## 脚本结构

```
virsical/
├── SKILL.md                  # 本文件
├── scripts/
│   ├── config.py             # 配置管理（Base URL 等）
│   ├── auth_manager.py       # OAuth2 认证（登录/登出/token管理/刷新）
│   ├── virsical_client.py    # HTTP 客户端（自动认证/签名/401重试）
│   ├── session.py            # 统一会话管理（一站式预检）
│   ├── cli.py                # 统一命令行入口
│   ├── meeting.py            # 会议室查询/预订/列表
│   ├── visitor.py            # 访客查询
│   ├── requirement.py        # 工单参数/创建
│   ├── license.py            # License 权限检查
│   └── data/                 # 运行时数据（token 等）
└── references/
    ├── commands.md           # 可执行命令参考
    ├── api_reference.md      # API 接口文档
    ├── error_codes.md        # 错误码说明
    ├── auth_flow.md          # 认证流程详解
    └── signature.md          # 签名算法详解
```
