---
name: sn-work-record
description: Use when handling 蜀宁 OA 工时：提交、修改、查询某天工时记录、获取项目列表，或排查验证码登录与 OA 查询认证问题。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["openssl"] },
      "env": ["OA_ENC_KEY"]
    },
    "author": "chengcheng"
  }
}
---

# 蜀宁 OA 工时管理

## 快速开始

> 推荐统一入口：`/root/.agents/skills/sn-work-record/sn-work-record`
>
> 所有 Python 脚本现在都带运行时自检：即使误用系统 `python3` 启动，也会优先自动切换到依赖完整的解释器。也可通过环境变量 `SN_WORK_RECORD_PYTHON` 显式指定解释器路径。

### 登录（自动执行）
```bash
/root/.agents/skills/sn-work-record/sn-work-record login [--credentials PATH] [--base-url http://X.X.X.X:PORT]
```
或：
```bash
python scripts/sn_oa_login.py [--credentials PATH] [--base-url http://X.X.X.X:PORT]
```
→ token 输出到 stdout（可 `| tee token.txt` 保存）

### 提交工时
```bash
/root/.agents/skills/sn-work-record/sn-work-record submit 2026-04-11 --job-desc "工时描述"
```
或：
```bash
python scripts/submit_time_entry.py 2026-04-11 --job-desc "工时描述"
```
→ 内部调用 `POST /sn/timeEntry/saveOrUpdate`
> 默认优先使用凭据文件中的默认项目；支持 `--save-draft` 保存草稿，并会在直接提交时自动检查是否为工作日。

### 修改工时记录
```bash
/root/.agents/skills/sn-work-record/sn-work-record update <工时ID> --job-desc "新描述"
```
→ 内部调用 `PUT /sn/timeEntry/update`

### 查询工时列表
```bash
/root/.agents/skills/sn-work-record/sn-work-record query 2026-04-10
```
→ 内部调用 `POST /sn/timeEntry/findEveryDayList`

### 获取工时详情
```bash
/root/.agents/skills/sn-work-record/sn-work-record details <工时ID>
```
→ 内部调用 `GET /sn/timeEntry/details/<工时ID>`

> 注意：工时提交/查询/详情/修改接口统一通过完整认证会话发起，必须同时携带 `Authorization: Bearer {token}` 和 `Admin-OA-Token: {token}` 两个请求头。

### 获取项目列表
```bash
python scripts/list_projects.py [--credentials PATH] [--base-url URL]
```
列出 OA 系统所有项目，供用户选择默认项目。

## 当前脚本

- `sn-work-record`：统一 launcher，封装常用子命令入口
- `scripts/runtime_bootstrap.py`：运行时解释器自检/自动切换
- `scripts/sn_oa_login.py`：登录并输出 token
- `scripts/list_projects.py`：查询项目列表（支持 `--json`）
- `scripts/submit_time_entry.py`：提交工时或保存草稿
- `scripts/query_time_entry.py`：查询某天工时列表
- `scripts/get_time_entry_details.py`：按工时 ID 查询详情
- `scripts/update_time_entry.py`：按工时 ID 修改描述或逻辑删除
- `scripts/oa_utils.py`：公共能力（登录、认证会话、状态映射、工时提交/查询/详情/修改）

## 凭证文件格式

存放在 `memory/sn-work-record-credentials.md`：

```markdown
# 蜀宁 OA 凭证

- **账号**: <手机号>
- **密码**: <密码>
- **Base URL**: http://<IP>:<PORT>
- **默认项目ID**: <your-project-id>（可选）
- **默认项目名称**: <your-project-name>（可选）
```

支持加密存储（`.md.enc`），使用 AES-256-CBC + openssl，密钥通过 `OA_ENC_KEY` 环境变量或 `~/.openclaw/workspace/.cache/oa_enc_key` 提供。

## fillDate 格式

提交工时时 `fillDate` 使用纯日期格式 `YYYY-MM-DD` 即可（如 `2026-04-10`），API 不要求 `(周X)` 后缀。

## 默认配置

- **项目**：需通过 `list_projects.py` 脚本获取用户确认后设定，写入 `memory/sn-work-record-credentials.md`
- **时长**：8h/天
- **状态**：`10` = 草稿，`20` = 审批中，`30` = 已审批

## 对话输出与隐私约定

- 默认回复中**不要主动暴露**项目 ID、工时记录 ID、项目配置值等内部标识。
- 查询结果默认只返回：日期、项目名称、时长、描述、状态、填写时间、更新时间。
- 只有在用户**明确要求查看 ID**，或执行修改/详情/删除等操作**确实必须引用 ID** 时，才展示对应 ID。
- 编写示例、文档、响应模板时，优先使用占位符（如 `<your-project-id>`、`<record-id>`），不要写入真实配置。

## 自然语言示例

| 用户说 | 执行动作 |
|--------|---------|
| "今天填了工时" | `python scripts/submit_time_entry.py <日期> --job-desc "..."` 提交 8h 工时（默认项目） |
| "周一到周三做某个项目" | 批量提交多天 |
| "把昨天工时改成xxx" | 查昨天 → `update_time_entry.py` 修改描述 |
| "查一下今天的工时状态" | `python scripts/query_time_entry.py <日期>` 查询 |
| "看看这条工时详情" | `python scripts/get_time_entry_details.py <工时ID>` |
| "把这条工时删掉" | `python scripts/update_time_entry.py <工时ID> --delete` |

## 节假日限制

以下节假日期间**不予填写工时**（2026年官方安排）：

| 节日 | 放假日期 |
|------|---------|
| 元旦 | 2026-01-01 ~ 2026-01-03 |
| 春节 | 2026-02-15 ~ 2026-02-23 |
| 清明节 | 2026-04-04 ~ 2026-04-06 |
| 劳动节 | 2026-05-01 ~ 2026-05-05 |
| 端午节 | 2026-06-19 ~ 2026-06-21 |
| 中秋节 | 2026-09-25 ~ 2026-09-27 |
| 国庆节 | 2026-10-01 ~ 2026-10-07 |

如遇节假日区间，回复：「节假日期间无需填写工时~」并拒绝提交。

## 提交成功输出模板

```
✅ {日期}({星期})工时提交成功！

• 日期：{fillDate}
• 项目：{projectName}
• 时长：{manHour}h
• 描述：{jobDesc}
• 状态：审批中 🟢
```

修改描述成功时输出：

```
✅ {日期} 工时描述已更新！

• 日期：{fillDate}
• 新描述：{jobDesc}
• 状态：审批中 🟢
```

## 环境要求

- Python 3
- ddddocr：`pip3 install ddddocr`
- chinese_calendar：`pip3 install chinese_calendar`（用于精确判断中国工作日/节假日）
- requests：`pip3 install requests`
- 凭据文件：`memory/sn-work-record-credentials.md`（明文或 .enc 加密均可）

> 说明：脚本会优先使用依赖完整的解释器。若环境特殊，可通过 `SN_WORK_RECORD_PYTHON=/path/to/python` 显式指定解释器路径。若需要单独准备虚拟环境，推荐名称优先使用 `sn_work_record_env`（也兼容 `oa_worktime_env`、`ddddocr_env`、`.venv`、`venv` 等常见命名）。

## 首次使用

1. 运行 `python scripts/sn_oa_login.py` 完成登录
2. 运行 `python scripts/list_projects.py` 获取项目列表，选择默认项目
3. 将项目信息写入凭据文件

## 增强说明

- 公共认证头逻辑已统一收口到 `oa_utils.py`，避免不同脚本各写一套导致认证不一致
- 项目列表脚本新增 `--json`，方便调试或二次处理
- 提交、查询、详情、修改四个工时脚本都走同一套登录与认证逻辑，减少后续维护成本
- 所有入口脚本已接入 `runtime_bootstrap.py`：若当前解释器缺少依赖，会自动切换到可用解释器再执行
- 解释器优先级支持环境变量 `SN_WORK_RECORD_PYTHON` 覆盖，也会自动探测常见虚拟环境名称
- 新增 `sn-work-record` launcher，后续优先使用它作为统一入口
- 目录说明已与实际文件对齐：提交/查询/详情/修改都已提供脚本，避免再次误判
