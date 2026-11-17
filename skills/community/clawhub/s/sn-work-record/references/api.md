# 蜀宁 OA 工时系统 - API 参考

## 系统信息

| 项目 | 值 |
|------|-----|
| baseURL | `None`（通过 `--base-url` 参数或凭据文件指定） |
| API 前缀 | /sn/* |
| 凭据文件 | memory/sn-work-record-credentials.md |
| 登录脚本 | scripts/sn_oa_login.py |
| baseURL 参数 | `--base-url` 或凭据文件中的 Base URL 字段 |

## 登录

**推荐用 `scripts/sn_oa_login.py`**：默认 ddddocr 自动识别；也可拆成「取图 + 提交」两阶段，把识别交给使用者当前 agent 的多模态模型。

```bash
python scripts/sn_oa_login.py --fetch-only                                  # 取图，输出 uuid/image_path/data_url
python scripts/sn_oa_login.py --submit --uuid <uuid> --code <答案>          # 提交；被拒则自动回退 ddddocr
```

手动流程：
1. `GET /sn/captchaImage` → 获取 base64 PNG + uuid（`img` 实为 data URL，前缀 image/png 但字节是 JPEG）
2. ddddocr 识别算术题，预处理（放大3倍灰度），使用严格匹配的单次四则运算计算答案；不执行识别文本，非法或过长输入拒绝
3. `GET /sn/passWord/encryption?passWord=<密码>` → 加密密码
4. `POST /sn/login` → `{ "username", "password", "code", "uuid" }` → 返回 `{ "code": 200, "data": { "token": "..." } }`

> 验证码按 `uuid` 校验，不绑定 HTTP 会话，因此取图与提交可以跨进程执行。验证码错误时服务端返回 `code=500, msg=验证码不正确`，可据此区分「验证码被拒」与其他登录失败。

## 项目接口

### 获取项目下拉列表
```
POST /sn/project/timeFeeDropDownPageList
Body: {"page": 1, "size": 8000}
```
返回 `data.content` 中的 `id`、`projectBoName`、`projectPmName`、`boToPmStatus`。当前工时前端按 `boToPmStatus == 1` 使用 `projectPmName`，否则使用 `projectBoName`；选中项目后复制其属性，不是独立 UI 选项。当前账号可见列表若达到分页边界或与 totalElements 不符，禁止当成完整目录。

### 工时业务字典（前端源码与 live 只读验证）
```text
POST /sn/system/dict/data/typeList
Body: ["sn_fill_type", "sn_fee_request_project_type", "sn_job_type"]
```
返回 `data` 数组：`dictType`、`dictValue`、`dictLabel`。对应填报类型、项目阶段、工作类型。原始 JSON 数组，不是 `{dictTypeList: ...}`。前端模块 `066e` 与 `f155` 证明端点和字段；工时 chunk 证明使用这三个字典。运行时查询，不使用取证快照作默认。

- 填报：1 工作、2 事假、3 公休假。
- 阶段：0 商务、1 研发/交付；boToPmStatus=0 的商机排除阶段 1。
- 工作类型：11 项目管理、1 销售、2 售前、4 调研、3 设计、5 开发、6 测试、7 实施、8 运维、9 财务、10 行政。

取证时间 2026-10-10；资源 SHA-256、脱敏结果见 `oa-options-evidence.json`，选择与限制见 `personal-settings.md`。字典为当前系统值，项目/属性为当前认证账号可见值。

---

## 报销与费用申请接口

### 查询申请列表
```http
POST /sn/feeRequest/findPageList
Body: {"page": 1, "size": 20, "total": 0, "startTime": "", "endTime": ""}
```
返回 `data.content`，主要字段有：`id`、`feeType`、`sumAmount`、`projectName`、`state`、`procInsId`、`createdTime`、`updatedTime`、`rejectReason`、`reimburseCompany`。

`startTime` / `endTime` 为空表示不筛选；非空必须为 `yyyy-MM-dd HH:mm:ss`。按整日筛选时传当天 `00:00:00` 至 `23:59:59`，不要按 CLI 参数名推断接口接受纯日期。监控目标申请时不要筛选“审批中”，否则通过后会从结果消失；在完整结果中按申请 ID 匹配，并处理分页与未找到的异常。

状态：`-1` 已撤回、`0` 已作废、`10` 待提交、`20` 审批中、`30` 已通过、`40` 已驳回。

费用类型：`1` 报销、`2` 备用金、`3` 补助、`4` 外采、`5` 其它、`6` 备用金抵扣。报销公司：`1` 蜀宁、`2` 天域智慧。

### 获取申请详情
```http
GET /sn/feeRequest/details/<申请ID>
```
返回申请主信息与 `detailList` 费用明细。

### 获取审批流程
```http
GET /sn/workflow/process/detail?procInsId=<流程实例ID>
```
当前审批节点可从 `data.historyProcNodeList` 中筛选 `activityType == "userTask"` 且 `endTime` 为空的记录；`activityName` 是节点名，`assigneeName` 是当前审批人。

推荐脚本：
```bash
python scripts/query_fee_requests.py
python scripts/query_fee_requests.py --state 审批中 --with-progress
```

---

## 选项与个人设置

只读选项入口：`scripts/oa_options.py`，通过已验证的项目下拉和业务字典接口读取当前账号选项。`submit_time_entry.py` 接受精确中文标签或验证代码，所有已保存默认代码也必须重新通过 live 选项验证；名称及 boToPmStatus 从项目派生。`--preview` 使用相同提交前解析路径，不调用保存接口、不改个人设置，`--json` 默认输出名称/时长/描述，显式 `--include-codes` 才显示内部代码。提交入口当前仅支持普通工作，事假/公休假等休假提交未实现、明确拒绝。见 [选择、确认与重复提交边界](personal-settings.md)。示例中的代码均为占位符，没有隐式默认项目、8h 或 1/1/5。

## 工时接口

### 工作日限制

工时仅允许在**工作日**提交，使用 `chinese_calendar.is_workday()` 判断。

该函数已自动处理以下情况：
- 法定节假日（如清明、国庆）→ 非工作日
- 调休补班（周六日上班）→ 工作日

**Agent 代码检查示例**：

```python
from oa_utils import is_workday

if not is_workday("2026-04-05"):
    print("非工作日，无需填写工时~")
    return  # 拒绝提交
```

---

### 查询某天工时列表
```
POST /sn/timeEntry/findEveryDayList
Body: {"fillDate": "2026-04-10"}
Headers:
  Authorization: Bearer <token>
  Admin-OA-Token: <token>
  Content-Type: application/json
```
返回 `{ "code": "200", "data": [{ id, fillDate, projectName, jobDesc, state, manHour, ... }] }`

> **注意**：查询接口不能只带 Bearer token，必须同时带 `Authorization` 和 `Admin-OA-Token`，否则会返回 401。

### 获取工时详情
```
GET /sn/timeEntry/details/<工时ID>
Headers:
  Authorization: Bearer <token>
  Admin-OA-Token: <token>
```
返回 `{ "code": "200", "data": { id, jobDesc, state, fillDate, ... } }`

### 保存/提交工时
```
POST /sn/timeEntry/saveOrUpdate
Headers:
  Authorization: Bearer <token>
  Admin-OA-Token: <token>
  Content-Type: application/json
Body: {
  "timeEntryList": [{
    "fillDate": "2026-04-10",
    "projectName": "<your-project-name>",
    "projectId": "<your-project-id>",
    "projectPhase": "<confirmed-code>",
    "workType": "<confirmed-code>",
    "manHour": "<confirmed-positive-hours: number>",
    "jobDesc": "工作描述",
    "boToPmStatus": "<derived-project-integer: number>",
    "fillType": "<confirmed-code>"
  }],
  "saveOrSubmit": 1    // 1=直接提交，0=仅保存草稿
}
```
> **注意**: `fillDate` 使用纯日期格式 `YYYY-MM-DD` 即可，API 不要求 `(周X)` 后缀。
> **安全入口**：此处是 OA 原始协议，不是绕过去重保护的执行建议。公共 `oa_utils.submit_time_entry()` 必须先核对同日记录、持有本地锁、持久保存意图并在写后只读核实；状态/字段不确定不会报成功，不自动重发。草稿真实写入暂时 fail-closed，仅支持 `--save-draft --preview`。详见 [提交保护](submission-idempotency.md)。
>
> **注意**: 提交接口与查询/详情/修改一样，也建议统一带完整认证头，避免会话不一致。

### 修改工时描述 / 逻辑删除
```
PUT /sn/timeEntry/update
Headers:
  Authorization: Bearer <token>
  Admin-OA-Token: <token>
Body: {"id": "<工时ID>", "jobDesc": "新描述"}
```
删除/恢复暂禁：服务端无可靠恢复契约，不提供可执行删除示例。
- **方法：PUT**（不是 POST）
- 审批中(20)的直接更新可能被服务端拒绝；不能假定所有记录都支持该路径。
- 对明确授权的撤回重提，使用下面的独立流程；旧接口失败不得自动触发撤回。
- 公共 API 对任何非空 `is_deleted` 在网络前拒绝；不得自行构造删除或恢复请求。

## 状态值

| 值 | 含义 |
|----|------|
| `-1` | 已撤回 |
| `10` | 草稿 |
| `20` | 审批中 |
| `30` | 已审批 |

## 工时修改工作流程

当前页面对审批中工时的修改流程已由用户提供的 HAR 确认。此处仅保存脱敏协议，不随包发布原 HAR、认证头、账号或真实记录标识。

1. `POST /sn/timeEntry/findEveryDayList` → 核对日期、原 ID、普通工作类型、审批中状态和所有不可变字段。
2. 用户明确授权撤回并重新提交后：`POST /sn/workflow/task/stopProcess`，请求体 `{"procInsId":"<current-record-process-id>"}`。
3. 只读查询，确认仍为同一记录，状态从 `20` 变为 `-1`，描述和其他业务字段未被并发改变。
4. `POST /sn/timeEntry/saveOrUpdate`：`timeEntryList` 中必须保留原 `id`，仅修改已授权的 `jobDesc`，并使用 `saveOrSubmit: 1` 重新提交。此修改请求与不带 ID 的普通新建请求不同；不得调用普通新建入口绕过同日保护。
5. 只读查询/详情核实：仍只有原记录，ID、日期、项目、时长、类型、阶段等保持一致，新描述精确匹配且状态为 `20`、未删除，才可报告成功。

HAR 页面请求使用 `YYYY-MM-DD(周X)` 日期展示形式；它来自原记录日期，不能把后缀当成新日期。普通新建提交仍使用纯日期。撤回与重提均为有副作用的写操作，不自动重登、重发或跟随重定向；超时/中断后遵循独立持久修改意图，只读核实，不能重新执行整条链路。

脚本入口与限制详见 [修改与撤回重提](amendment-workflow.md)。旧 `PUT` 描述更新仍独立存在；逻辑删除/恢复暂禁，不自动升级成上述流程。

## 推荐脚本

- 提交工时：`python scripts/submit_time_entry.py 2026-04-11 --job-desc "工时描述"`
- 草稿只读预览（需完整已确认字段）：`python scripts/submit_time_entry.py <confirmed-date> --job-desc "<confirmed-description>" --save-draft --preview`；真实草稿写入暂不支持
- 查询某天工时：`python scripts/query_time_entry.py 2026-04-10`
- 查询工时详情：`python scripts/get_time_entry_details.py <工时ID>`
- 修改只读预览：`python scripts/update_time_entry.py <record-id> --job-desc "<new-description>" --preview`
- 明确授权后撤回并重提：`python scripts/update_time_entry.py <record-id> --job-desc "<new-description>" --withdraw-resubmit`
- 旧接口直接更新：`python scripts/update_time_entry.py <record-id> --job-desc "<new-description>"`（被拒绝后不得自动撤回）
- 逻辑删除/原 ID 恢复：暂禁，CLI / 公共 API 在任何网络前拒绝，无布尔绕过开关；见 [删除与恢复限制](deletion-recovery.md)。

> `submit_time_entry.py` 已补齐；提交/查询/详情/修改脚本都应复用 `oa_utils.py` 中的登录与认证会话能力。

## 凭据文件格式

```markdown
# 蜀宁 OA 凭证

- **账号**: <手机号>
- **密码**: <密码>
- **Base URL**: http://<IP>:<PORT>

```

支持明文（`.md`）和加密（`.md.enc`，AES-256-CBC + openssl）两种格式。加密密钥通过环境变量 `OA_ENC_KEY` 或 `~/.openclaw/workspace/.cache/oa_enc_key` 文件提供。

## 对话输出约定

- 面向用户汇报查询结果时，默认不要主动返回 `projectId`、工时记录 `id` 等内部标识。
- 默认展示字段以业务可读信息为主：日期、项目名称、时长、描述、状态、填写时间、更新时间。
- 仅当用户明确要求查看，或后续修改/详情/删除操作必须用到时，再返回对应 ID。
- 文档示例与测试示例优先使用占位符，避免写入真实项目配置。

## 典型响应

```
查询列表: {"code":"200","data":[{"id":"...","jobDesc":"...","state":"20"}]}
修改:     {"code":"200","isOk":true,"data":{"jobDesc":"新描述"}}
提交:     {"code":"200","data":true}
```
