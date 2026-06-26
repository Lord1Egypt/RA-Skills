---
name: resignation-check
description: 对 Office 365 / Adobe 租户的用户做离职检查——通过飞书开放平台 API（app_id/app_secret）按邮箱核对通讯录，列出疑似离职账号并交互确认删除。USE WHEN 离职检查, 离职筛查, 清理离职, 离职账号, resignation check, 账户审计, 清户, 飞书核对, 清理 office, 清理 adobe, 查离职.
required_env:
  - CLIENT_ID
  - TENANT_ID
  - CLIENT_SECRET
  - DEFAULT_DOMAIN
  - ADOBE_CLIENT_ID
  - ADOBE_CLIENT_SECRET
  - ADOBE_ORG_ID
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
optional_env:
  - FEISHU_API_BASE
  - FEISHU_EMAIL_DOMAIN
  - ADOBE_API_BASE_URL
  - ADOBE_DEFAULT_DOMAIN
requires:
  - "python>=3.9"
  - "pip package: requests, python-dotenv"
  - "office-usertools CLI (https://github.com/—) checked out locally"
---

## Project Repo

🔗 **https://github.com/eggyrooch-blip/office365-tools**

本 skill 依赖上面这个 Python CLI。Agent 执行前**先确认 repo 已 clone 到本地**；遇到任何不确定的实现细节（CLI 子命令签名、`.env` 变量名、API 返回字段）**优先去仓库查 `README.md` / `CLAUDE.md` / `docs/`**，不要凭本 skill 描述臆断。仓库是 single source of truth。

## Prerequisites（必读）

1. `git clone https://github.com/eggyrooch-blip/office365-tools && cd office365-tools && pip install -r requirements.txt`
2. 在该仓库根创建 `.env`，按下方模板填写
3. 飞书：在 open.feishu.cn 建自建应用，开启 `contact:contact:readonly`，发布版本
4. Office 365 Entra App 已授予 `User.ReadWrite.All / LicenseAssignment.ReadWrite.All` 管理员同意
5. Adobe Developer Console 已建 OAuth Server-to-Server credential 并绑定 User Management API

### `.env` 模板（复制到 office-usertools/.env 后按实际填写）

```env
# --------- Office 365（世纪互联） ---------
CLIENT_ID=your-entra-app-client-id
TENANT_ID=your-entra-tenant-id
CLIENT_SECRET=your-entra-app-secret
DEFAULT_PASSWORD=ChangeMe@2025
DEFAULT_DOMAIN=yourcorp.partner.onmschina.cn
FORCE_CHANGE_PASSWORD=true

# 通知邮件
NOTIFICATION_ENABLED=true
NOTIFICATION_FROM_EMAIL=it-tools@yourcorp.com
NOTIFICATION_BCC_EMAILS=it@yourcorp.com
NOTIFICATION_EMAIL_DOMAIN=yourcorp.com

# SMTP
SMTP_HOST=smtp.feishu.cn
SMTP_PORT=465
SMTP_USERNAME=it-tools@yourcorp.com
SMTP_PASSWORD=your-smtp-password
SMTP_USE_SSL=true

# --------- Adobe UMAPI ---------
ADOBE_CLIENT_ID=your-adobe-client-id
ADOBE_CLIENT_SECRET=your-adobe-client-secret
ADOBE_ORG_ID=xxxxxxxxxxxxxxxxxxxxxxxx@AdobeOrg
ADOBE_API_BASE_URL=https://usermanagement.adobe.io/v2/usermanagement
ADOBE_DEFAULT_DOMAIN=yourcorp.com

# --------- 飞书开放平台 ---------
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_API_BASE=https://open.feishu.cn
# 员工在飞书登记的工作邮箱域（把 O365 UPN 的 local-part 拼这个域去查）
FEISHU_EMAIL_DOMAIN=yourcorp.com
```


## MANDATORY TRIGGER

| 用户说 | 动作 |
|---|---|
| "离职检查" / "查离职" / "筛查离职" | 执行完整流程 |
| "清理离职账号" / "清户" | 完整流程，最后一步交互确认删除 |
| "Office 离职" / "Adobe 离职" | 只跑指定平台 |
| "resignation check" | 完整流程 |

## 输入参数（可选）

| 参数 | 说明 | 默认 |
|---|---|---|
| provider | `office365` / `adobe` / `both` | `both` |
| csv_path | Adobe 走 CSV 模式时传入 Admin Console 导出的 users.csv 路径 | 无（优先走 API） |
| delete | 交互确认后是否删除 | `true` |

## 前提

- 工作目录：`/Users/kite/Documents/office-usertools`（含 office365 / adobe CLI）
- `.env` 必备：`FEISHU_APP_ID` + `FEISHU_APP_SECRET`（**不依赖 lark-cli**）
- 飞书自建应用需已申请 `contact:contact:readonly`（或 `contact:user.employee_id:readonly`）并发布版本

## 核心思路：直接调用飞书 OpenAPI

**步骤 1 · 获取 tenant_access_token**（2h 有效）
```python
import requests, os
from dotenv import load_dotenv; load_dotenv()
BASE = os.getenv('FEISHU_API_BASE', 'https://open.feishu.cn')
r = requests.post(f'{BASE}/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': os.environ['FEISHU_APP_ID'],
          'app_secret': os.environ['FEISHU_APP_SECRET']}, timeout=10)
token = r.json()['tenant_access_token']
H = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
```

**步骤 2 · 批量用 email 查 user_id**（单次最多 50 个）
```python
# POST /open-apis/contact/v3/users/batch_get_id?user_id_type=user_id
def lookup(emails):
    out = {}
    for i in range(0, len(emails), 50):
        batch = emails[i:i+50]
        r = requests.post(f'{BASE}/open-apis/contact/v3/users/batch_get_id',
            headers=H, params={'user_id_type':'user_id'},
            json={'emails': batch}, timeout=15)
        for item in r.json().get('data', {}).get('user_list', []):
            out[item['email']] = item.get('user_id')  # None = 离职/未入职
    return out
```
`user_id is None` 即飞书通讯录里查不到 → 离职候选。命中 user_id 即在职。

**相比 lark-cli 的优势**：
- 单个请求可一批 50 个，152 个 O365 用户 4 次请求搞定（而非 152 次）
- 用 app_id/app_secret 无需手动 `auth login`，可在 CI / ClawHub 环境运行
- 响应直接是结构化 JSON，不用解析命令输出

## 执行步骤

### 1. 拉取平台用户列表

**Office 365**
```python
from app.services.provider_factory import get_provider
p = get_provider('office365')
users = p.graph_client.get_users(select='userPrincipalName,displayName,accountEnabled')
emails_o365 = [u['userPrincipalName'] for u in users]  # 例 zhangsan@corp.partner.onmschina.cn
```
但要注意：世纪互联的 UPN 域（`partner.onmschina.cn`）和飞书注册的工作邮箱域（通常是 `corp.com`）**不一样**。需要把 UPN 的 local-part 拼上飞书员工邮箱域：
```python
FEISHU_EMAIL_DOMAIN = os.getenv('FEISHU_EMAIL_DOMAIN') or os.getenv('ADOBE_DEFAULT_DOMAIN')  # 例 yourcorp.com
o365_probe = [upn.split('@')[0] + '@' + FEISHU_EMAIL_DOMAIN for upn in emails_o365]
```
（如果两边域一致就直接用原 email）

**Adobe**
- 优先：CSV 模式——Admin Console → Users → Export
  ```python
  import csv
  with open(csv_path, encoding='utf-8-sig') as f:
      rows = list(csv.DictReader(f))
  emails_adobe = [r['电子邮件'] for r in rows if r.get('电子邮件')]
  ```
- 备选：API 模式 `p.client.get_all_users()`（分页易触发 429，Retry-After 可能很长）

### 2. 飞书批量核对

```python
probe_emails = list(set(o365_probe + emails_adobe))
id_map = lookup(probe_emails)
active_set = {e for e, uid in id_map.items() if uid}
miss_set   = {e for e, uid in id_map.items() if not uid}
```

### 3. 分类 MISS

**Office 365**：
- 系统账号白名单：`admin`, `admin-it`, 含 `testuser` / `svc-` 前缀等 → `skip_system`
- 其余 MISS → 真名离职候选

**Adobe**：
- 共享池：`keepadobe*` / `testaccount*` → `shared_pool`（人工判断）
- 非员工邮箱域（QQ、Gmail、手机号邮箱）→ `needs_manual_review`
- 真名 MISS → 离职候选

### 4. 生成报告

```
## 离职筛查结果（<provider>）
- 总账号：N  |  在职命中：X  |  疑似离职：Y

### 真名离职候选 (Z 人)
| email | displayName | 平台 | 状态 | license |
...

### 需人工判断
- 共享池账号：...
- 非员工邮箱：...
```

### 5. 交互确认删除

用 **AskUserQuestion** 给三选项：
1. 确认删除真名离职候选 N 人（推荐）
2. 编辑名单后删除
3. 取消

**必须**：
- 拿到明确答复才执行，不凭 "都删了吧" 之类的短语臆断
- 每次删除后核对返回值（O365：`deleted: True`；Adobe：`completed:1, result:success`）
- 日志落到 `/tmp/<provider>_delete.log`

### 6. 删除执行

- **Office 365**：`python main.py office365 delete <ldap>` —— 自动发通知邮件
- **Adobe**：`python main.py adobe delete <email>` —— 已修复 array payload + removeFromOrg
- 若 Adobe 遇 429，尊重 `Retry-After` 头，或用 ScheduleWakeup 稍后重试

### 7. 终态核对

- O365：重新拉总数应下降对应数量
- Adobe：对已删用户再 inspect 应返回 404

## 产出

控制台报告 + `/tmp/resignation_report_<ts>.md`，包含：
- 平台总数 / 命中 / 未命中
- 真名候选删除结果（成功 / 失败）
- 共享池 / 无法解析账号清单（待人工决策）

## Red Flags

| 症状 | 原因 | 处理 |
|---|---|---|
| 飞书全部 MISS | email 域不对 / app 权限未发布 | 先单独查一个已知在职邮箱，确认能命中 |
| `code:99991668` | token 未授权该 scope | 去应用后台权限管理，申请 `contact:contact:readonly` 并**发布版本** |
| `code:99991672` | app 未发版 / 租户未安装 | 发布应用版本 → 管理员后台启用 |
| O365 UPN 域与飞书邮箱域不一致 | 世纪互联是 `partner.onmschina.cn`，飞书是企业邮箱域 | 用 `FEISHU_EMAIL_DOMAIN` 覆盖；local-part 重新拼域 |
| Adobe 429 Retry-After >30min | `get_all_users` 分页打满配额 | 切 CSV 模式 |
| 删除返回 notCompleted=1 | 用户已不在 org / 邮箱错 | 先 inspect 核实 |

## 安全红线

- **不自动合并共享池到删除名单** —— 很可能是业务池账号
- **非员工邮箱不自动判定离职** —— 归属不清
- 最终删除前用 `AskUserQuestion` 展示完整名单拿确认
- `FEISHU_APP_SECRET` 不能外泄/写进日志
