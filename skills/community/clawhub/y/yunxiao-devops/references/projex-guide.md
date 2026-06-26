# Projex 指南

## 适用范围

当用户要做以下事情时，优先读本文件：

- 查找或识别项目
- 查询项目成员、角色、权限范围
- 查询 / 创建 / 更新工作项（需求、任务、缺陷、风险等）
- 查询 / 创建迭代（Sprint）
- 查询 / 创建版本（Version）
- 查询 / 登记工时
- 给工作项补评论、补上下文、补负责人

如果任务涉及代码库、MR、分支，转去 Codeup 章节；如果涉及流水线、部署、日志，转去 Flow / Appstack 章节。

---

## 一、对象模型

Projex 可以先按 6 类对象理解：

1. **项目（Project）**
   - 入口对象
   - 后续大多数操作都需要 projectId / spaceId

2. **项目成员 / 角色（Member / Role）**
   - 决定谁在项目里、谁是什么权限
   - 常用于指派、筛负责人、确认 owner

3. **工作项（Workitem）**
   - 包括需求 Req、任务 Task、缺陷 Bug、风险 Risk 等
   - 是最常见的日常操作对象

4. **迭代（Sprint）**
   - 用于阶段性规划和归类工作项

5. **版本（Version）**
   - 用于里程碑 / 发布计划管理

6. **工时（Effort）**
   - 包括实际工时明细

---

## 二、核心 ID / 参数概念

### 1. 组织 ID

当前默认组织：

- `organizationId = ${YUNXIAO_ORG_ID}`

### 2. 项目 ID vs 项目编码

项目常有两个可见标识：

- `id`：API 真正使用的项目唯一标识
- `customCode`：项目编号（如 `UHZM`）

规则：

- API 调用优先用 **项目 ID**
- 面向用户展示时，可以同时带上项目名称 + 编号

### 3. `spaceId` / `spaceType`

很多工作项接口不是直接传 `projectId`，而是传：

- `spaceId` = 项目 ID
- `spaceType` = `Project`

默认先按项目处理，不要假设是 Program。

### 4. 工作项类型 ID

创建工作项时需要 `workitemTypeId`，不要只凭中文名称硬写。优先来源：

- 已知项目常量
- 或调用 `list_all_workitem_types`

---

## 三、标准工作流

## 工作流 A：先定位项目

适用：用户说“某个项目”“帮我看这个项目”“在云效里建个项目任务”但没给 projectId。

步骤：

1. `search_projects`
   - 按名称 / 编号搜项目
2. 如果命中多个：整理候选项
   - 名称
   - customCode
   - id
   - 状态
3. 明确目标项目后，再继续后续动作
4. 后续工作项接口统一使用：
   - `spaceId = <projectId>`
   - `spaceType = "Project"`

### 示例

```bash
# 搜索项目
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects:search" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"conditions":"{\"conditionGroups":[[{\"fieldIdentifier\":\"name\",\"operator\":\"CONTAINS\",\"value\":[\"<关键词>\"],\"className\":\"string\",\"format\":\"input\"}]]}","orderBy":"gmtCreate","sort":"desc","page":1,"perPage":20}'
```

---

## 工作流 B：查询项目成员 / 角色

适用：

- 想知道谁在项目里
- 想找负责人 / 管理员 / 某角色成员
- 创建迭代 / 版本前需要 owners
- 创建工作项前需要 assignedTo 候选

步骤：

1. `list_all_project_roles`
   - 先看组织下角色定义
2. `list_project_members`
   - 结合 `roleId` 或名字过滤
3. 需要 owner / assignee 时，优先从这里选真实 userId

### 关键规则

- **不要猜 userId**
- `owners`、`assignedTo`、`participants`、`trackers` 这类字段都应该先查成员

### 示例

```bash
# 查询项目成员
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/members" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

---

## 工作流 C：创建工作项

适用：创建需求 / 任务 / 缺陷 / 风险 / 用户反馈等。

### 推荐顺序

1. 确认项目
   - `spaceId`
   - `spaceType=Project`
2. 确认工作项类型
   - 优先查 `list_all_workitem_types`
3. **必要时查字段配置**
   - `get_workitem_type_field_config`
4. 准备创建 payload
5. 调 `create_work_item`

### 强规则：先查字段配置，再写复杂字段

如果要写以下字段，先查 `get_workitem_type_field_config`：

- `status`
- `priority`
- 自定义字段
- 多选字段
- 用户字段
- 版本 / 迭代 / 标签相关字段

原因：

- 很多字段写入值不是中文名，而是 **ID / identifier**
- 同一个组织、不同模板、不同项目，字段配置可能不同

### create_work_item 常用字段

- `spaceId`：项目 ID
- `subject`：标题
- `workitemTypeId`：工作项类型 ID
- `assignedTo`：负责人 userId
- `description`：描述
- `sprint`：迭代 ID
- `participants`：参与人 userId 列表
- `trackers`：抄送人 userId 列表
- `verifier`：验证人 userId
- `versions`：版本 ID 列表
- `customFieldValues`：扩展字段 map

### 示例：创建任务

```bash
# 创建工作项
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "<projectId>",
    "spaceType": "Project",
    "subject": "任务标题",
    "workitemTypeId": "<typeId>",
    "assignedTo": "<userId>",
    "description": "任务描述"
  }'
```

---

## 工作流 D0：查询工作项可用状态

适用：更新状态前，先搞清楚该工作项类型有哪些合法状态 ID。

```bash
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/workitemTypes/<workitemTypeId>/workflows" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

返回 `statuses` 数组，每条有 `displayName`（中文名）和 `id`（写入时用这个）。

### 已知状态 ID（缺陷类型）

| 状态 | id |
|------|----|
| 待确认 | 28 |
| 处理中 | 100010 |
| 已修复 | 29 |
| 再次打开 | 30 |
| 暂不修复 | 31 |
| 已关闭 | 100085 |

---

## 工作流 D：更新工作项

适用：

- 改标题
- 改状态
- 改负责人
- 改优先级
- 关联迭代 / 版本
- 更新自定义字段

### 推荐顺序

1. `get_work_item` 或 `search_workitems`
   - 先拿到 workitemId 和当前状态
2. 如果涉及状态 / 优先级 / 自定义字段：
   - 先 `get_workitem_type_field_config`
3. 调 `update_work_item`

### 强规则

- `update_work_item` 的 body 本质上就是字段 map
- 字段名和值都必须和当前工作项类型配置匹配
- 不确定时，**先查字段配置，不要盲写**

### 示例：更新状态 / 负责人

```bash
# 更新工作项
curl -s -X PUT "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"status": "<statusId>", "assignedTo": "<userId>"}'
```

### 示例：只改标题

```bash
# 更新工作项
curl -s -X PUT "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"subject": "新标题"}'
```

---

## 工作流 E：搜索工作项

适用：

- 查某项目下的任务 / 需求 / 缺陷
- 查某人负责的工作项
- 查某迭代 / 某状态 / 某优先级的事项

### 核心规则

- `search_workitems` **不能跨多个项目搜**
- 一次搜索只针对一个 `spaceId`
- 条件建议从少到多，先缩项目，再加过滤

### 常见过滤方向

- 标题包含关键词
- 类型（Req / Task / Bug）
- 状态
- 指派人
- 迭代
- 创建时间 / 更新时间

### conditions 格式

官方接口里 `conditions` 更接近 **JSON 字符串**，不是随便塞数组。建议按官方格式组装：

```json
{"conditionGroups":[[
  {"fieldIdentifier":"subject","operator":"CONTAINS","value":["Projex"],"toValue":null,"className":"string","format":"input"}
]]}
```

### 示例：查标题包含 Projex 的任务

```bash
# 搜索工作项
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems:search" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "<projectId>",
    "spaceType": "Project",
    "conditions": "{\"conditionGroups\":[[{\"fieldIdentifier\":\"subject\",\"operator\":\"CONTAINS\",\"value\":[\"Projex\"],\"toValue\":null,\"className\":\"string\",\"format\":\"input\"}]]}",
    "orderBy": "gmtCreate",
    "sort": "desc",
    "page": 1,
    "perPage": 20
  }'
```

---

## 工作流 F：添加评论

适用：

- 给工作项补上下文
- 回填执行结果
- 记录分析结论
- @ 相关人前的准备（如果后续系统支持）

### 示例

```bash
# 添加工作项评论
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/comments" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"content": {"htmlValue": "<p>评论内容</p>", "jsonMLValue": []}}'
```

---

## 工作流 G：创建 / 查询迭代

适用：

- 查询项目有哪些 Sprint
- 创建新的开发迭代
- 为工作项找可挂载的 sprintId

### 关键规则

- 创建迭代时，`owners` 是必填
- 所以创建前通常先查项目成员

### 查询迭代

```bash
# 查询迭代列表
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/sprints" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

### 创建迭代

```bash
# 创建迭代
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/sprints" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sprint 1",
    "startDate": "2026-03-18",
    "endDate": "2026-04-01",
    "owners": ["<userId>"]
  }'
```

---

## 工作流 H：创建 / 查询版本

适用：

- 管理发布计划
- 给工作项挂版本
- 维护里程碑节奏

### 关键规则

- 创建版本时，`owners` 是必填
- 所以同样建议先查项目成员

### 查询版本

```bash
# 查询版本列表
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/versions" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

### 创建版本

```bash
# 创建版本
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/versions" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "v1.0.0",
    "startDate": "2026-03-18",
    "endDate": "2026-04-15",
    "owners": ["<userId>"],
    "description": "版本描述"
  }'
```

---

## 工作流 I：查询 / 登记工时

适用：

- 查某个工作项已经记录了多少实际工时
- 补登记当天工作量

### 关键规则

- `create_effort_record` 需要：
  - `actualTime`
  - `gmtStart`
  - `gmtEnd`
- 不是简单的 `recordDate`

### 查询工时

```bash
# 查询实际工时
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/effortRecords" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

### 登记工时

```bash
# 登记实际工时
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/effortRecords" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "actualTime": 120,
    "gmtStart": "2026-03-17T09:00:00+08:00",
    "gmtEnd": "2026-03-17T11:00:00+08:00",
    "description": "完成功能开发"
  }'
```

---

## 四、字段与坑点

## 1. 字段名不是总能靠猜

尤其是：

- `status`
- `priority`
- 自定义字段
- 某些 list / multiList 字段

很多时候：

- 展示给人看的是中文名
- API 真正要写的是 `id` / `identifier`

所以：

- **复杂写操作前先查字段配置**

## 2. 工作项关联关系（CreateWorkitemRelationRecord）

关联两个工作项（支持：需求、任务、缺陷、线上故障、风险等互联）。

**关键踩坑：** 参数必须用 query string，不是 body。

```bash
# 查当前工作项支持的关联类型
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/relationWorkitemTypes" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"

# 创建关联（query string 传参，body 传 {}）
curl -s -X POST \
  "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/relationRecords?relationType=ASSOCIATED&workitemId=<targetWorkitemId>" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}'
# 返回 {"id":"<relationRecordId>"} 表示成功

# 查已有关联
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems/<workitemId>/relationRecords?relationType=ASSOCIATED" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

**relationType 可选值：** `ASSOCIATED`（目前 OpenAPI 支持的类型）

---

## 3. 创建迭代 / 版本时 owners 必填

这两个接口都不是只填名字就行，必须给 owner userId 列表。

## 3. 搜工作项的 conditions 要贴官方格式

不要把 `conditions` 当成普通数组；更稳的是传官方的 JSON 字符串格式。

## 4. 用户相关字段尽量先查成员

包括：

- `assignedTo`
- `owners`
- `participants`
- `trackers`
- `verifier`

都应先从 `list_project_members` 结果里选。

## 5. 工作项搜索不能跨项目

先缩定项目，再搜工作项。

---

## 五、推荐执行策略

当用户提出 Projex 请求时，优先按这个策略执行：

1. **先确认项目**
2. **再确认对象类型**（工作项 / 迭代 / 版本 / 工时）
3. **涉及写操作时优先查配置 / 成员 / 类型**
4. **最后再创建或更新**

一句话：

> Projex 最稳的方式不是“直接写”，而是“先识别上下文，再查配置，再写入”。
