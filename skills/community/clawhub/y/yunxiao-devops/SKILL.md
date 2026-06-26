---
name: yunxiao-devops
description: >
  与阿里云云效（Yunxiao）DevOps 平台交互，覆盖八大核心能力：项目协作 Projex、
  代码管理 Codeup、流水线 Flow、应用交付 Appstack、制品仓库 Packages、
  测试管理 Testhub、效能洞察 Insight、知识库 Thoughts。
  当用户提到云效、Projex、Codeup、Flow、流水线、部署单、应用、版本、迭代、
  工作项、需求、缺陷、任务、测试计划、制品仓库、Yunxiao、DevOps 时使用。
  读 reference 选择：项目协作/工作项/迭代/版本/工时 → projex-guide.md；
  流水线创建/YAML → pipeline-yaml-guide.md；工作流状态 → workflow-transitions.json。
---

# 云效 DevOps Skill

## 配置

所有脚本从 `scripts/config.mjs` 读取配置，优先级：**环境变量 > `.env.local` > `~/.yunxiao-devops.json`**

**快速配置（复制示例文件）：**
```bash
cp .env.local.example .env.local
# 编辑 .env.local，填入你的 token 和 org ID
```

**必须配置：**
| 环境变量 | 说明 |
|---------|------|
| `YUNXIAO_TOKEN` | 云效 Personal Access Token（个人设置 → Access Token） |
| `YUNXIAO_ORG_ID` | 云效组织 ID（URL 中 `/organizations/` 后的字符串） |

**可选配置：**
| 环境变量 | 说明 |
|---------|------|
| `YUNXIAO_USER_ID` | 你在云效中的用户 ID（用于「我的工作项」默认值） |
| `FEISHU_USER_OPEN_ID` | 你的飞书 open_id（用于接收通知的目标用户） |
| `YUNXIAO_PROJECT_ID` | 默认项目 ID（部分脚本使用） |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 飞书 App 凭证（不设则从 `~/.openclaw/openclaw.json` 读取） |

```bash
# REST API 调用模板（token 从环境变量读取）
curl -s -X <METHOD> "https://openapi-rdc.aliyuncs.com/oapi/v1/..." \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

## 🗺️ 高频场景速查表

| 场景 | 触发词示例 | 方式 |
|------|-----------|------|
| ☀️ 每日站会 | "今天有什么任务"、"站会" | `scripts/daily-standup-card.mjs` |
| 查看我的工作项 | "查下我的工作项"、"我负责什么" | `scripts/my-workitems-card.mjs` |
| 查看工作项详情 | 粘贴云效 URL 或"看下 UHZM-5" | `scripts/workitem-card.mjs <id>` |
| 创建工作项 | "帮我建个需求/任务/缺陷" | `scripts/create-workitem-flow.mjs` |
| 工作项关联 | "把这个需求关联到任务"、"看关联项" | `scripts/workitem-relation-flow.mjs <id>` |
| ⏱️ 工时打卡 | "打卡"、"记工时"、"登记今日工时" | `scripts/effort-checkin-card.mjs` |
| 修复 Bug | "帮我修复这个 bug"、"修 UHZM-5" | `scripts/bug-fix-flow.mjs <id>` |
| 📝 最近提交 | "谁改了代码"、"看最近 commit" | `scripts/commit-activity-card.mjs` |
| 🔀 Code Review | "有没有待 Review 的 MR" | `scripts/mr-review-card.mjs` |
| 🚀 发版 | "发版"、"打 tag"、"发 v1.2.0" | `scripts/release-flow.mjs` |
| 版本管理 | "查版本"、"创建版本"、"关闭版本" | `scripts/version-release-flow.mjs` |
| 查看/触发流水线 | "流水线怎么样"、"触发流水线" | `scripts/pipeline-log-card.mjs` + REST API 触发 |
| 流水线日志 | "流水线挂了看日志"、"哪步报错了" | `scripts/pipeline-log-card.mjs` |
| 📊 迭代进展 | "这迭代完成多少了"、"站会看板" | `scripts/sprint-dashboard-card.mjs` |
| 新仓库初始化 | "建个新仓库"、"初始化仓库" | `scripts/repo-init-flow.mjs` |
| 🧪 测试用例 | "查测试用例"、"查测试计划结果" | `scripts/testcase-card.mjs` |
| 📦 应用交付 | "查应用"、"运行工作流"、"查部署单" | `scripts/appstack-card.mjs` |
| 搜索工作项 | "找本迭代未完成的需求" | REST API → projex-guide.md 工作流 E |

---

## 一、查看我的工作项

```bash
# 发飞书卡片，列出负责的工作项，支持分页
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/my-workitems-card.mjs \
  [--user <yunxiaoUserId>] [--project <projectId>] [--page <n>]
```

**翻页回调（收到 `WI_LIST_PAGE|userId|projectId|page`）：**
```bash
node scripts/my-workitems-card.mjs --user <userId> --project <projectId> --page <n> --update-msg <messageId>
```

**点击工作项查详情（收到 `WI_DETAIL|workitemId`）：**
```bash
node scripts/workitem-card.mjs <workitemId>
```

---

## 二、查看工作项详情 & 状态变更

```bash
# 发飞书卡片，展示工作项详情 + 状态变更按钮
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/workitem-card.mjs <workitemId>
```

**收到 `WI_STATUS_CHANGE|workitemId|statusId|statusName` 回调：**
1. 执行：`node scripts/workitem-card.mjs change-status <workitemId> <statusId> <statusName> <messageId>`
2. **验证**：GET 工作项确认 `status.id` 已变更

**工作流 transitions 缓存：** `references/workflow-transitions.json`
该文件存储各工作项类型的状态流转（用于卡片按钮展示）。**组织/项目不同，workflow ID 不同，需按实际情况填写。**
填写方法：调 `GET /oapi/v1/projex/organizations/{orgId}/projects/{projectId}/workitemTypes/{typeId}/workflows` 获取 workflowId，再浏览器抓包 `/projex/api/workitem/workitem/workflow/getActions/{workflowId}` 拿合法流转列表。

---

## 三、创建工作项（交互式卡片）

```bash
# 发类型选择卡片（需求/任务/缺陷 三类五种）
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/create-workitem-flow.mjs [projectId]
```

**回调处理（收到 `CREATE_` 开头）：先 ack，再执行：**
```bash
node scripts/create-workitem-flow.mjs callback "<payload>"
```

| Payload | 触发时机 |
|---------|----------|
| `CREATE_TYPE\|projectId\|typeId\|typeName` | 选类型 → 发填写表单卡片 |
| `CREATE_PRIORITY\|projectId\|typeId\|typeName\|priorityId\|label` | 选优先级 → 更新状态提示 |
| `CREATE_SERIOUS\|projectId\|typeId\|typeName\|seriousId\|label` | 选严重程度（缺陷专用） |
| `WI_DETAIL\|workitemId` | 查看已创建的工作项详情 |
| `BUGFIX_START\|workitemId` | 直接进入 Bug 修复流程 |

用户选好优先级后，直接发消息 `标题：xxx 描述：xxx`，agent 调 `submit` 提交：
```bash
node scripts/create-workitem-flow.mjs submit "标题" "描述"
```

---

## 四、迭代进展看板

```bash
# 发飞书看板卡片（自动识别当前活跃迭代）
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/sprint-dashboard-card.mjs [projectId] [sprintId]
```

展示内容：完成率进度条、待处理/进行中/已完成数量、各成员完成情况、迭代切换按钮。

**回调处理（收到 `SPRINT_SWITCH|projectId|sprintId`）：先 ack，再执行：**
```bash
node scripts/sprint-dashboard-card.mjs callback "SPRINT_SWITCH|<projectId>|<sprintId>"
```

---

## 五、Code Review（MR 列表）

```bash
# 查所有监控仓库的待 Review / 待合并 MR
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/mr-review-card.mjs [repoId]
```

展示内容：按状态分组（待合并优先），支持直接点按钮合并（自动用 squash 方式）。

**回调处理（收到 `MR_` 开头）：先 ack，再执行：**
```bash
node scripts/mr-review-card.mjs callback "MR_MERGE|<repoId>|<mrId>"
```

合并后自动 GET 验证状态，发结果通知。

---

## 六、Bug 修复全流程（端到端自动化）

从缺陷工作项到代码合并的完整自动化：

```bash
# 启动流程（发仓库选择卡片）
node /root/.openclaw/workspace/skills/yunxiao-devops/scripts/bug-fix-flow.mjs <workitemId>
```

**回调处理（收到 `BUGFIX_` 开头）：先 ack，再执行：**
```bash
node scripts/bug-fix-flow.mjs callback "<完整payload>"
```

| Payload | 触发时机 |
|---------|----------|
| `BUGFIX_SELECT_REPO\|workitemId\|repoId\|repoName\|sshUrl` | 选仓库 → 发分支选择卡片 |
| `BUGFIX_SELECT_BRANCH\|workitemId\|repoId\|repoName\|sshUrl\|baseBranch` | 选分支 → 克隆 + Claude Code 修复 |
| `BUGFIX_CONFIRM_DIFF\|workitemId\|repoId\|fixBranch\|workDir` | 确认 diff → 推送 + 创建 MR |
| `BUGFIX_REJECT_DIFF\|workitemId` | 拒绝 diff → 提示手动改 |
| `BUGFIX_CONFIRM_MERGE\|workitemId\|repoId\|mrId` | 确认合并 → 合并 MR + 工作项→已修复 |
| `BUGFIX_REJECT_MERGE\|workitemId\|mrId` | 暂不合并 |

**卡片交互设计：** 每步发新卡片（POST），上一张归档为灰色"已完成"，历史清晰可查。

---

## 七、查看 & 触发流水线

```bash
# 后台轮询流水线结果，完成后自动发飞书卡片通知
# ⚠️ 必须用 nohup + disown，否则 exec session 回收时进程会被 SIGTERM 杀掉
nohup python3 {baseDir}/scripts/poll-pipeline.py <runId> [pipelineId] \
  > /tmp/poll-pipeline-<runId>.log 2>&1 & disown $!
```

**REST API 直接触发：**
```bash
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/flow/organizations/${YUNXIAO_ORG_ID}/pipelines/<pipelineId>/runs" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" -d '{}'
```

**查流水线列表：**
```bash
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/flow/organizations/${YUNXIAO_ORG_ID}/pipelines?page=1&perPage=20" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

关键踩坑见 `references/pipeline-yaml-guide.md`。

---

## 八、搜索工作项

```bash
# 搜索工作项（不能跨项目）
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/workitems:search" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "<projectId>",
    "spaceType": "Project",
    "conditions": "{\"conditionGroups\":[[{\"fieldIdentifier\":\"assignedTo\",\"operator\":\"IN\",\"value\":[\"<userId>\"],\"className\":\"string\",\"format\":\"member\"}]]}",
    "orderBy": "gmtCreate",
    "sort": "desc",
    "page": 1,
    "perPage": 20
  }'
```

详细见 `references/projex-guide.md` 工作流 E。

---

## 九、迭代管理（REST API）

```bash
# 查询迭代列表（含工作项进展）
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${YUNXIAO_ORG_ID}/projects/<projectId>/sprints" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"

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

⚠️ 创建迭代/版本时 `owners` 必填，先用 `list_project_members` 拿 userId。

---

## 十、代码管理（Codeup）

```bash
# 查询仓库列表（分页）
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${YUNXIAO_ORG_ID}/repositories?page=1&perPage=50" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"

# 查询分支列表
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${YUNXIAO_ORG_ID}/repositories/<repoId>/branches?page=1&perPage=50" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"

# 查询待合并 MR 列表
curl -s "https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${YUNXIAO_ORG_ID}/repositories/<repoId>/changeRequests?state=TO_BE_MERGED&page=1&perPage=20" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}"
```

### MR 操作（⚠️ 踩坑记录）

**创建 MR（路径驼峰 `changeRequests`，不是下划线）：**
```bash
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${YUNXIAO_ORG_ID}/repositories/<repoId>/changeRequests" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceBranch": "<fixBranch>",
    "targetBranch": "main",
    "sourceProjectId": <repoId>,
    "targetProjectId": <repoId>,
    "title": "fix: ...",
    "workItemIds": "<workitemId>"
  }'
# ⚠️ 创建后必须 GET 验证 status 字段，错误字段名不报错但不创建 MR
```

**合并 MR（优先用 squash，merge 类型在部分仓库被禁用）：**
```bash
curl -s -X POST "https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${YUNXIAO_ORG_ID}/repositories/<repoId>/changeRequests/<mrId>/merge" \
  -H "x-yunxiao-token: ${YUNXIAO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"mergeType": "squash"}'
# ⚠️ 合并后必须 GET 确认 status == "MERGED"
```

---

## 十一、AppStack 应用交付

### 应用列表（必须传 pagination=keyset&orderBy=id，否则 500）
```bash
curl "https://openapi-rdc.aliyuncs.com/oapi/v1/appstack/organizations/<orgId>/apps:search?pagination=keyset&orderBy=id" \
  -H "x-yunxiao-token: ..."
# 返回：{ data: [...] }，app 用 name 字段（非数字 ID）标识
```

### 环境列表
```bash
curl "https://openapi-rdc.aliyuncs.com/oapi/v1/appstack/organizations/<orgId>/apps/<appName>/envs?pagination=keyset&orderBy=id" \
  -H "x-yunxiao-token: ..."
```

### 部署单列表（POST，路径是 /changeOrders/api）
```bash
curl -X POST ".../apps/<appName>/changeOrders/api" \
  -d '{"pagination":"keyset","orderBy":"id","perPage":10,"envName":"<envName>"}'
# 返回：{ records: [...], total }，状态字段是 state（不是 status）
```

### 触发工作流阶段 + 后台轮询
```bash
# 1. 触发（REST API）
POST /oapi/v1/appstack/organizations/{orgId}/apps/{appName}/releaseWorkflows/{wfSn}/releaseStages/{stageSn}:execute
body: { "params": {} }   # params 必传，空对象即可
# 返回：{ object: <executionNumber>, pipelineId, pipelineRunId }

// 2. 后台轮询（触发后立刻后台启动）
APPSTACK_PIPELINE_ID=<pipelineId> APPSTACK_PIPELINE_RUN_ID=<pipelineRunId> \
  python3 {baseDir}/scripts/poll-appstack-stage.py \
  <appName> <releaseWorkflowSn> <releaseStageSn> <executionNumber> <stageName> &
```

### 云效 URL 格式
```
# AppStack 阶段页面（正确格式）
https://devops.aliyun.com/appstack/app/{appName}/workflow/{releaseWorkflowSn}/stage/{releaseStageSn}
```

### ⚠️ 踩坑
- `GET /apps?page=1&perPage=20` → 500 错误，必须用 `?pagination=keyset&orderBy=id`
- 部署单路径是 `/changeOrders/api`（POST），不是 `/changeOrders`
- 应用 ID 是 name 字符串（如 `my-app`），不是数字
- 环境也是 name 字符串，无数字 id
- 部署单状态字段是 `state`（不是 `status`）
- 部署单详情：`GET /apps/{appName}/changeOrders/{changeOrderSn}`（用 changeOrderSn，不是 sn）

---

## 十二、全局踩坑记录

1. **MR 创建参数名**：必须用 `sourceBranch`/`targetBranch`/`sourceProjectId`（整数）/`targetProjectId`（整数）；用 `sourceRef`/`targetRef` 不报错但不创建
2. **MR 路径驼峰**：`changeRequests` 不是 `change_requests`（合并路径也一样）
3. **MR 合并类型**：优先 `squash`，`merge` 在部分仓库配置下会返回 403
4. **操作后必须 GET 验证**：任何写操作（MR/工作项/流水线）完成后必须调 GET 接口确认实际状态，不能只信 API 响应
5. **缺陷创建必传 seriousLevel**：先调 `GET /workitemTypes/{id}/fields` 查选项 ID
6. **搜索工作项不能跨项目**：`search_workitems` 必须指定单个 `spaceId`
7. **创建迭代/版本 owners 必填**：需先查项目成员拿 userId
8. **流水线 YAML 路径**：见 `references/pipeline-yaml-guide.md`（含 kubernetesCluster 等踩坑）
9. **工作项关联 API**：路径 `POST /workitems/{id}/relationRecords?relationType=ASSOCIATED&workitemId={targetId}`，参数走 **query string** 不是 body；`/relations` 路径 404；OpenAPI 只支持 `ASSOCIATED` 类型；查关联用 `GET /workitems/{id}/relationRecords?relationType=ASSOCIATED`
10. **AppStack 触发工作流**：`POST .../releaseWorkflows/{wfSn}/releaseStages/{stageSn}:execute`，body `{"params":{}}` 必传；触发后得到 `{pipelineId, pipelineRunId}` 传给 `poll-appstack-stage.py` 轮询；云效 URL：`https://devops.aliyun.com/appstack/app/{appName}/workflow/{wfSn}/stage/{stageSn}`
11. **AppStack 标识符**：应用和环境均用 `name` 字符串标识，无数字 id；部署单状态字段是 `state`（不是 `status`）；部署单详情用 `changeOrderSn`（不是 `sn`）

---

## 十三、辅助工具 & 脚本清单

| 脚本 | 用途 |
|------|------|
| `daily-standup-card.mjs` | 每日站会卡片（进行中/昨完成/流水线状态） |
| `my-workitems-card.mjs` | 我的工作项列表，分页展示 |
| `workitem-card.mjs` | 工作项详情 + 状态变更卡片 |
| `create-workitem-flow.mjs` | 创建工作项交互流程（需求/任务/缺陷，5 种类型） |
| `workitem-relation-flow.mjs` | 工作项关联查看/创建（7 种关联类型） |
| `effort-checkin-card.mjs` | 工时打卡（快捷 +2h/+4h 按钮，今日累计） |
| `bug-fix-flow.mjs` | Bug 修复全流程（选仓库→CC修复→MR→合并） |
| `commit-activity-card.mjs` | 最近提交记录（全仓库汇总/单仓库切换） |
| `mr-review-card.mjs` | 待 Review 的 MR 列表，支持直接合并 |
| `mr-action.mjs` | MR 细粒度操作 CLI：approve / merge / close / status / approve-merge |
| `release-flow.mjs` | 发版流程（选仓库→选分支→打 Tag→触发流水线） |
| `version-release-flow.mjs` | 版本管理（查列表/详情/创建/关闭版本） |
| `sprint-dashboard-card.mjs` | 迭代进展看板（完成率/成员分布/切换迭代） |
| `pipeline-log-card.mjs` | 流水线失败日志快查（最后 30 行） |
| `repo-init-flow.mjs` | 新仓库初始化（建仓+保护分支，可选 Webhook） |
| `testcase-card.mjs` | 测试用例管理（列表/计划/创建/执行结果） |
| `appstack-card.mjs` | 应用交付（应用列表/环境/工作流触发/部署单查看） |
| `poll-appstack-stage.py` | AppStack 阶段轮询，完成后发飞书通知+失败日志 |
| `poll-pipeline.py` | 后台轮询流水线，完成后自动发卡片通知 |

---

## 十四、ccuser 配置（Claude Code 专用，部署相关）

`bug-fix-flow.mjs` 的 Claude Code 自动修 Bug 功能需要以下本地配置（非必须，跳过则无法使用自动修复）：

- `/home/ccuser/.claude/settings.json` → `{"model":"claude-sonnet-4-6","alwaysThinkingEnabled":false}`
- 环境变量：`ANTHROPIC_API_KEY=<your-key>` + `ANTHROPIC_BASE_URL=<your-endpoint-or-api.anthropic.com>`
- SSH：需配置可访问 Codeup 的 SSH key

---

## 十五、参考文件索引

| 文件 | 内容 |
|------|------|
| `references/projex-guide.md` | Projex 完整工作流（项目/成员/工作项/迭代/版本/工时）+ 可运行 curl 示例 |
| `references/workflow-transitions.json` | 工作项状态流转缓存（任务/缺陷/技术需求） |
| `references/pipeline-yaml-guide.md` | 流水线 YAML 创建踩坑 |
| `references/pipeline-yaml-syntax.md` | 流水线 YAML 语法细节 |
| `references/api-docs/INDEX.md` | 全量 OpenAPI 文档索引（339 个接口） |
| `references/user-mapping.json` | 飞书↔云效用户 ID 映射（**需按团队实际成员填写**） |
| `scripts/config.mjs` | 共享配置模块（TOKEN/ORG_ID 等，所有脚本从此处 import） |
| `.env.local.example` | 配置示例文件（复制为 `.env.local` 填入实际值） |

---

## 飞书任务同步（搁置）

脚本已备好：`scripts/sync-feishu-task.mjs`。
需开通飞书应用 `task:task:write`（应用身份）权限后可用，当前搁置。
