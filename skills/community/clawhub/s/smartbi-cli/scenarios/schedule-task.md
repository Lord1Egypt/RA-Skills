# S1: 定时计划任务

## 触发

用户问句**同时**满足「定时特征」+「任务动作」，「是否推送」由额外语义单独判断。

| 条件 | 关键词 |
|------|--------|
| **定时特征** | 每天/每日/每周/每月/定时/按时/周期性/间隔/cron/整点/几点 |
| **任务动作** | 查询/取数/统计/导出/ETL/同步/执行 |
| **需要推送**（可选） | 发送/推送/通知/邮件/企微/钉钉 |

仅满足「任务动作」无「定时特征」→ 走 Part 1 通用流程（即时查询）。

**示例**：
- "每天9:00发送保额大于20万的保单数据"
- "每周一统计各分支行贷款余额并邮件通知"
- "每月1号自动同步客户数据到数据仓库"

## 意图解析

从问句中提取：

| 参数 | 来源 | 示例 |
|------|------|------|
| cron/timing | 时间描述 | "每天9:00"→DAY, startHour="9", startMinute="0" |
| 任务类型 | 动作关键词 | "查询/统计"→MQL取数, "导出/下载"→报表导出, "同步/ETL"→数据同步 |
| dims/metrics | 业务对象 | "分支行贷款余额"→ 需查字段树 |
| dimFilter | 过滤条件 | "保额>20万"→`"保额 > 200000"` |
| 推送渠道 | 发送方式 | "邮件/企微/钉钉/发送"→ 脚本中调用 push API；无相关词→不需要推送 |

## 执行步骤

> **严格顺序约束**：Step 3（生成脚本）→ Step 4（注入脚本到 JSON）→ Step 5（创建任务）必须**串行执行**。
> 每次工具调用拿到实际返回后再发起下一步。

```
Step 1:  获取任务可用的父目录 ID（见下方「parentFolderId 选取」章节）
         调用 catalogtree.listDescendantCatalogs（limit=1）取第一个可编辑目录
    ↓
Step 2:  [MQL 取数场景必做] 获取数据模型字段树，提取可用的维度/度量 label
         smartbi call datamodel.getDataModelTrees -d '{"modelIds":["<MODEL_ID>"]}' --agent
         从返回结果收集：
         - **维度 label**：`type=FIELD`/`LEVEL_TIME_*` 等维度节点的 label（如 "订单日期"、"产品类别"）
         - **度量 label**：`type=MEASURE`/`CALC_MEASURE` 度量节点的 label（如 "销售额"、"订单量"）
         - **MUST** 后续脚本中 MQL 的 dims/metrics/dimFilter 字段名**必须从 label 中选取**，
           禁止编造或猜测字段名，否则会触发 "没有找到层次字段: xxx" 服务端 500 错误
    ↓
Step 3:  生成 Rhino JS 脚本 → 写入 .js 文件
         模板见 references/rhino-template.md
         BASE_URL 优先从环境变量 SMARTBI_SDK_BASE_URL 获取，TOKEN 优先从 SMARTBI_TOKEN_DEV 获取
         MQL 中的 dims/metrics 必须使用 Step 2 获取到的 label 值
         **需要推送时**：脚本末尾追加 push.sendMessage 调用（见下方「推送」章节）
         **邮件推送优先使用 `sendToMail` 内置 Routine**（见下方「推送」章节），比自行拼装 HTTP 更简洁
    ↓
Step 4:  使用 inject-script 工具将脚本注入元数据模板（见下方「script 字段处理」章节）
         node scripts/inject-script.mjs task.js task_meta.json task.json
    ↓（必须等 Step 4 完成，拿到完整 task.json 后再执行 Step 5）
Step 5:  smartbi call scheduletask.createSelfDefineTask -d @task.json --agent
    ↓    返回 {"ok":true, "data": {"id": "<taskId>"}}
Step 6:  验证——调用 scheduletask.getTaskById 确认 script 非空且 parentFolderId 正确
    ↓    若 script 为空，或 parentFolderId 既不是 TASKS 本身也不是 TASKS 根下的子节点，停止并报错
Step 7:  smartbi call scheduletask.createTimeSchedule -d @schedule.json --agent
    ↓    绑定 taskId + cron，返回 scheduleId
Step 8:  smartbi call scheduletask.changeScheduleActiveStatus -d @activate.json --agent
    ↓    actived: true（请求体见下方 ### 启用）
Step 9:  验证计划——调用 scheduletask.getScheduleDtoById 确认：
         - actived=true
         若 actived=false，重试 Step 8（最多 3 次，间隔 2 秒），每次重试后重新验证
         若 3 次后 actived 仍为 false，向用户报告「计划创建成功但激活失败，请手动启用」
```

### 可并行的步骤

以下组合可在同一轮中并行调用：
- Step 1（查 parentFolderId）与 Step 7 所需的 `getCurrentUser` 可并行
- Step 6（验证任务）与 Step 7（创建计划）可合并调用（Step 5 成功后已知 taskId）

## 修改已有任务（多轮对话）

当用户通过多轮对话修改已有任务时（如"增加某列""改展示格式"）：

```
Step A: 获取已有任务——用户提供 taskId，或调用 listTasks 搜索
        smartbi call scheduletask.getTaskById -d '{"id": "<taskId>"}' --agent
        取出 script 字段内容
   ↓
Step B: 将 script 内容写入 .js 文件（还原为可读多行代码）
        按用户意图修改 .js 文件内容
   ↓
Step C: 修改元数据模板并重新注入
        node scripts/inject-script.mjs updated_task.js task_meta.json task.json
   ↓
Step D: 更新任务
        smartbi call scheduletask.updateSelfDefineTask -d @task.json --agent
```

> `updateSelfDefineTask` 的请求体与 `createSelfDefineTask` 相同，额外需要 `id` 字段。

## API 请求体

### 创建任务

```
POST /api/v1/scheduletask/task/create-self-define-task
```

```text
{
  "selfDefineTaskUpsertRequest": {
    "name": "<英文名>",
    "alias": "<中文名>",
    "desc": "<描述>",
    "parentFolderId": "<Step 1 选取的目录 ID>",
    "type": "SELFDEFINE",
    "script": "<Rhino JS 脚本>",
    "scriptVersion": "2.0"
  }
}
```

必填：`name`, `alias`, `script`, **`parentFolderId`**。Smartbi 资源为树状结构，新建任务必须指定存放目录。

### parentFolderId 选取（任务专属）

**任务（TASK）的父节点必须位于 `TASKS` 根节点下**，且父节点类型仅限 `TASKS` 或 `SELF_TREENODE`——服务端会校验类型匹配，传错会导致创建失败。

获取有效 parentFolderId 的方式（与计划选父目录同理，将根节点换为 `SCHEDULES` 即可，详见下方「创建计划」）：

将以下内容写入 `task_folder.json`：

```json
{
  "listDescendantCatalogsReq": {
    "pids": ["TASKS"],
    "types": ["DEFAULT_TREENODE"],
    "purviewType": "WRITE",
    "limit": 1
  }
}
```

```bash
smartbi call catalogtree.listDescendantCatalogs -d @task_folder.json --agent
```

- 返回列表有数据 → 取第一项的 `id` 作为 parentFolderId
- 返回空列表 → 直接使用 `"TASKS"` 作为 parentFolderId（根目录本身接受任务）

> `parentFolderId` 已在 YAML `required` 数组中。调用时缺 `parentFolderId` 服务端会报错。

### script 字段处理（MUST 使用 inject-script 工具）

**禁止手工 JSON 转义脚本**。MUST 使用 `scripts/inject-script.mjs` 工具完成转义和注入。

**工作流程**：

1. 将 Rhino JS 脚本写入 `.js` 文件（如 `task.js`），内容为原始多行 JS，无需转义
2. 将元数据模板写入 `.json` 文件（如 `task_meta.json`），`script` 字段留空字符串：

```json
{
  "selfDefineTaskUpsertRequest": {
    "name": "daily_report",
    "alias": "每日报表",
    "desc": "每天9:00发送报表",
    "parentFolderId": "<Step 1 结果>",
    "type": "SELFDEFINE",
    "script": "",
    "scriptVersion": "2.0"
  }
}
```

3. 调用工具合并：

```bash
node scripts/inject-script.mjs task.js task_meta.json task.json
```

4. 使用合并后的 `task.json` 调用 API：

```bash
smartbi call scheduletask.createSelfDefineTask -d @task.json --agent
```

> **禁止占位符**：`script` 字段必须包含实际的 Rhino JS 代码字符串，禁止使用 `"..."` 等占位符。
> 服务端会对脚本做非空校验，空内容或 `"..."` 将直接报错。

#### 工具路径

`scripts/inject-script.mjs` 位于本 skill 目录下。使用时需从 skill 根目录解析绝对路径：
- 若当前工作目录不在 skill 目录内，使用绝对路径调用
- 示例：`node /path/to/skills/smartbi-cli/scripts/inject-script.mjs task.js task_meta.json task.json`

### 创建计划

```
POST /api/v1/scheduletask/schedule/create-time-schedule
```

```text
{
  "scheduleUpsertRequest": {
    "name": "<英文名>",
    "alias": "<中文名>",
    "desc": "<描述>",
    "taskIds": "<Step 5 返回的 taskId>",
    "timeType": "DAY",
    "startHour": "9",
    "startMinute": "0",
    "cron": "0 0 9 * * ?",
    "creatUsername": "<当前用户名，必填>",
    "creatUserAuth": true,
    "actived": false,
    "retryCount": 0,
    "retryIntervalMinute": 0,
    "enableRange": false,
    "parentFolderId": "SCHEDULES"
  }
}
```

> **`cron` MUST 主动传入有效 Quartz 6 字段表达式**，不要传 `null`/省略。
> 底层在 `timeType=DAY/WEEK/MONTH` 时**不会**自动生成 cron；空 cron 会导致 `changeScheduleActiveStatus` 静默失败。
> 常用模板：
> - 每天 H 点 M 分：`0 M H * * ?`
> - 每周一 H 点 M 分：`0 M H ? * MON`
> - 每月 1 号 H 点 M 分：`0 M H 1 * ?`
> - 手工任意（BYHAND）：直接传入完整 Quartz 表达式

> **`actived` 创建时务必设置为 `false`**：创建与激活分离，避免 Hibernate 事务未提交时调度器尝试加载刚创建的计划导致激活静默失败。
> 激活通过 Step 8（`changeScheduleActiveStatus`）单独完成，再经 Step 9 验证激活结果。

**全部必填字段**（13 个，按 schema `required` 数组）：`name`, `alias`, `taskIds`, `actived`, `retryCount`, `retryIntervalMinute`, `startHour`, `startMinute`, `timeType`, `creatUserAuth`, `creatUsername`, `enableRange`, `parentFolderId`。

**关键约束（经实际调试验证）**：

| 约束 | 说明 |
|------|------|
| `startHour`/`startMinute` **始终必传** | 即使 `timeType` 为 `BYHAND` 也要传这两个字段，服务端会对空值抛 `NumberFormatException`。值为字符串 `"0"`–`"23"` / `"0"`–`"59"` |
| `cron` **MUST 主动传入** | 不要传 `null`。底层不会自动生成，空 cron 会导致激活静默失败。`DAY` = `0 {m} {h} * * ?`；`WEEK` = `0 {m} {h} ? * MON`；`MONTH` = `0 {m} {h} 1 * ?`；`BYHAND` 传入任意 Quartz 6 字段 |
| `parentFolderId` **必填** | Smartbi 资源为树状结构，必须指定计划存放的目录。计划根节点 ID 为 `SCHEDULES`，可直接使用 `"SCHEDULES"` 作为值；如需子目录，调用 `catalogtree.listDescendantCatalogs`（pids=["SCHEDULES"], types=["DEFAULT_TREENODE"], purviewType="WRITE", limit=1）取第一个可编辑子目录；空列表则直接用 `"SCHEDULES"` |
| `creatUsername` **必须用当前用户真实名称** | 不能硬编码 `"admin"`。从 `smartbi describe` 或 `context.get("userName")` 获取 |

**`timeType` 与 `cron` 推荐格式**：

| timeType | startHour/Minute | cron 推荐格式 |
|----------|:---:|:---|
| `DAY` | 必传 | `0 {minute} {hour} * * ?` |
| `WEEK` | 必传 | `0 {minute} {hour} ? * MON` |
| `MONTH` | 必传 | `0 {minute} {hour} 1 * ?` |
| `BYHAND` | 必传 | 任意有效 Quartz 6 字段 |

> `WEEK`/`MONTH` 没有独立的 `weekDay`/`monthDay` 字段，服务端按创建当天计算调度日。

### 启用计划

```
POST /api/v1/scheduletask/schedule/change-schedule-active-status
```

```json
{
  "scheduleActiveStatusRequest": {
    "scheduleId": "<Step 7 返回的 scheduleId>",
    "actived": true
  }
}
```

## 创建后验证（MUST）

任务创建（Step 5）成功后，**必须**立即调用 `scheduletask.getTaskById` 验证：

```bash
smartbi call scheduletask.getTaskById -d @task_verify.json --agent
```

其中 `task_verify.json` 内容为 `{"id": "<taskId>"}`。

检查项：
- `script` 字段**非空**且不是 `"..."` 等占位符——若为空则说明脚本未正确注入，需终止流程
- `parentFolderId` 为 TASKS 本身或 TASKS 根下的子节点
- `type` 为 `SELFDEFINE`

若验证失败，**不得**继续 Step 7/8，应向用户报告错误原因。

### 计划激活验证

计划激活验证使用 `scheduletask.getScheduleDtoById`（而非 `getScheduleById`），返回更完整的字段映射：

```bash
smartbi call scheduletask.getScheduleDtoById -d @schedule_verify.json --agent
```

检查 `actived` 字段是否为 `true`。若为 `false`，按 Step 9 重试策略处理。

## 推送（任务脚本内调用 push API）

推送由任务脚本在内部通过 HTTP 调用 push 接口实现。推送代码直接嵌入 Rhino JS 模板的末尾，复用模板中已定义的 `httpPostJson` / `TOKEN` / `BASE_URL`。

### 多渠道路由

模板内置两种推送通路，可**同时启用多个渠道**，各渠道独立 try-catch 互不阻塞：

| 渠道 | 通路 | 内容格式 | 依赖 |
|------|------|---------|------|
| 邮件 | `sendToMail` 内置 Routine | HTML | 系统 SMTP 配置 |
| 企微/钉钉/飞书（群机器人） | `pushMessage()` → push API | Markdown | webhookUrl |
| 企微企业应用 | `pushMessage("WECHAT_WORK", ...)` → push API | Markdown | **WeiXinExt** + agentId/toUsers |
| 钉钉工作通知 | `pushMessage("DINGTALK", ...)` → push API | Markdown | **DingdingExt** + toUsers |
| 系统消息 | `pushMessage()` → push API | Markdown | Smartbi 用户 ID |

群机器人模式无需扩展插件。企业应用/工作通知模式依赖对应扩展提供的系统配置（`WEIXIN_CORE`/`DINGDING_CORPID` 等）做鉴权。

### 邮件推送首选 sendToMail Routine

当用户要求"发邮件/发到邮箱"时，脚本中优先使用 `sendToMail` 内置 Routine，代码简洁且不需要拼装 HTTP。

RoutineExecutor 通过 Java 动态代理将 JS 对象属性映射到 `SendToMail.Input` 接口方法调用。属性名转换优先按 Java Bean 规范（`isHTMLText()` → `HTMLText`），未命中则回退旧规则（→ `hTMLText`），向下兼容。

因此 **MUST** 提供 `taskName`、`sendSetting`、`files`、`paramValueMap` 四个属性，`sendSetting` 内 MUST 包含 `IMailSetting` 的全部字段。缺字段则对应 getter 返回 `null`，触发 NPE。

```js
execute("sendToMail", {
    taskName: "近7天销售额趋势",
    sendSetting: {
        mailList: "qtp@smartbi.com.cn",  // 收件邮箱，多个用";"分隔
        title: "近7天销售额趋势",
        text: html,                        // 上一步拼接的 HTML
        HTMLText: true,                    // isHTMLText() → HTMLText（Java Bean 规范）
        doZip: false,
        doUnzip: false,
        picInMail: false,
        ccMailList: "",
        bccMailList: ""
    },
    files: [],
    paramValueMap: {}
});
```

如果渠道是企微/钉钉/飞书/系统消息等**非邮件**场景，再使用 push API（详见下文）。

### Agent 交互指引（MUST）

当用户问句含"发送/推送/通知"等推送关键词时，Agent **必须在生成脚本前**先向用户确认推送目标。**多渠道场景逐渠道收集，缺一不可**：

| 渠道关键词 | 需确认 | 模板中占位 | 依赖 |
|-----------|--------|-----------|------|
| 邮件/email/邮箱 | 收件人邮箱地址 | `sendToMail.sendSetting.mailList` | — |
| 企微/企业微信/微信 + 群/机器人/webhook | 群机器人 webhookUrl | `pushMessage("WECHAT_WORK", ..., {webhookUrl})` | — |
| 钉钉/DingTalk + 群/机器人/webhook | 群机器人 webhookUrl（有加签则还需 secret） | `pushMessage("DINGTALK", ..., {webhookUrl})` | — |
| 飞书/Feishu | 群机器人 webhookUrl | `pushMessage("FEISHU", ..., {webhookUrl})` | — |
| 企微/企业微信 + 应用/通知/agentId | 企微应用 agentId + 目标用户 userid（`\|` 分隔） | `pushMessage("WECHAT_WORK", ..., {agentId, toUsers})` | WeiXinExt |
| 钉钉/DingTalk + 工作通知/toUsers | 目标钉钉用户 ID（逗号分隔） | `pushMessage("DINGTALK", ..., {toUsers})` | DingdingExt |
| 系统消息/站内消息 | Smartbi 用户 ID | `pushMessage("MESSAGE", ..., recipients)` | — |

> 用户说"发到邮箱和企业微信"→ 需分别问邮箱地址和 webhookUrl。只说"通知我"但未指定渠道 → 反问希望用哪种渠道。

### 推送工作原理

```
定时计划到时 → 执行任务脚本 → 查询数据/处理逻辑
                                  │
                  格式化结果为 HTML/Markdown
                                  │
                    ▼
           脚本内调用 httpPostJson(pushUrl, TOKEN, pushBody)
           推送到目标渠道（webhook/邮件/系统消息）
```

### 脚本中调用 push API（完整示例见 rhino-template.md）

模板文件 `references/rhino-template.md` 主流程末尾已包含注释形式的多渠道推送代码段（`pushMessage()` 辅助函数 + 7 个渠道模式）。Agent 只需按用户意图取消对应渠道的注释并填入渠道专属参数（如 `webhookUrl`、`agentId`、`toUsers`）。

序列化使用 Rhino 环境中的 `Packages.smartbi.net.sf.json.JSONObject.fromObject(payload).toString()`（免去手工 JSON 拼接和转义）。

**渠道参数速查**：

| channelType | 必填参数 | 说明 |
|-------------|---------|------|
| `MAIL` | `recipients: ["a@x.com"]` | 邮箱地址列表 |
| `MESSAGE` | `recipients: ["userId"]` | Smartbi 用户 ID 列表 |
| `WECHAT_WORK` | `config.webhookUrl`（群机器人）或 `config.agentId`（应用） | 企微=企业微信=微信 |
| `DINGTALK` | `config.webhookUrl`（群机器人）或 `config.toUsers`（工作通知） | 代理需确认 secret |
| `FEISHU` | `config.webhookUrl` | 代理需确认 secret |

> 详细接口文档见 `smartbi describe push.sendMessage --agent`。

## 非 MQL 任务脚本骨架

MQL 取数任务的完整 Rhino 1.7R2 模板见 **`references/rhino-template.md`**。

```js
// 报表导出
var r = execute("exportResource", { resourceId: "<RES_ID>", format: "PDF" });
context.put("resultContent", "<p>导出完成: " + r + "</p>");

// ETL 数据同步
var user = context.get("userName");
var r = connector.remoteInvoke("ETLService", "runETLJob", [user, "<JOB_ID>"]);
context.put("resultContent", "<p>ETL 完成: " + r.getResult() + "</p>");
```
