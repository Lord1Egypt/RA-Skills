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

**推荐用 `scripts/sn_oa_login.py`**，自动处理验证码识别（ddddocr + 预处理 + eval）。

手动流程：
1. `GET /sn/captchaImage` → 获取 base64 PNG + uuid
2. ddddocr 识别算术题，预处理（放大3倍灰度），清理非数字运算符后 `eval()` 求值
3. `GET /sn/passWord/encryption?passWord=<密码>` → 加密密码
4. `POST /sn/login` → `{ "username", "password", "code", "uuid" }` → 返回 `{ "code": 200, "data": { "token": "..." } }`

## 项目接口

### 获取项目下拉列表
```
POST /sn/project/timeFeeDropDownPageList
Body: {"page": 1, "size": 8000}
```
返回 `{ "code": "200", "data": { "content": [{ "id": "...", "projectBoName": "..." }, ...] } }`（注意字段名为 `projectBoName`）

---

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
    "projectPhase": "1",
    "workType": "5",
    "manHour": 8,
    "jobDesc": "工作描述",
    "boToPmStatus": 1,
    "fillType": "1"
  }],
  "saveOrSubmit": 1    // 1=直接提交，0=仅保存草稿
}
```
> **注意**: `fillDate` 使用纯日期格式 `YYYY-MM-DD` 即可，API 不要求 `(周X)` 后缀。
> **注意**: 提交接口与查询/详情/修改一样，也建议统一带完整认证头，避免会话不一致。

### 修改工时描述 / 逻辑删除
```
PUT /sn/timeEntry/update
Headers:
  Authorization: Bearer <token>
  Admin-OA-Token: <token>
Body: {"id": "<工时ID>", "jobDesc": "新描述"}
```
逻辑删除示例：
```
PUT /sn/timeEntry/update
Body: {"id": "<工时ID>", "isDeleted": 1}
```
- **方法：PUT**（不是 POST）
- 审批中(20)可直接修改，无需撤回
- 修改后状态自动变回审批中(20)
- 删除工时使用同一接口，设置 `isDeleted=1`

## 状态值

| 值 | 含义 |
|----|------|
| `10` | 草稿 |
| `20` | 审批中 |
| `30` | 已审批 |

## 工时修改工作流程

1. `POST /sn/timeEntry/findEveryDayList` → 找到目标工时 ID
2. `PUT /sn/timeEntry/update` → 修改描述或删除
3. `GET /sn/timeEntry/details/<id>` → 验证

## 推荐脚本

- 提交工时：`python scripts/submit_time_entry.py 2026-04-11 --job-desc "工时描述"`
- 保存草稿：`python scripts/submit_time_entry.py 2026-04-11 --job-desc "工时描述" --save-draft`
- 查询某天工时：`python scripts/query_time_entry.py 2026-04-10`
- 查询工时详情：`python scripts/get_time_entry_details.py <工时ID>`
- 修改描述：`python scripts/update_time_entry.py <工时ID> --job-desc "新描述"`
- 逻辑删除：`python scripts/update_time_entry.py <工时ID> --delete`

> `submit_time_entry.py` 已补齐；提交/查询/详情/修改脚本都应复用 `oa_utils.py` 中的登录与认证会话能力。

## 凭据文件格式

```markdown
# 蜀宁 OA 凭证

- **账号**: <手机号>
- **密码**: <密码>
- **Base URL**: http://<IP>:<PORT>
- **默认项目ID**: <your-project-id>（可选，首次使用后设置）
- **默认项目名称**: <your-project-name>（可选，首次使用后设置）
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
