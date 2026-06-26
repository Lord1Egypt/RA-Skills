---
name: user-provision
description: 在 Office 365（世纪互联）与 Adobe Creative Cloud 批量或单人开户——自动授权、重置密码、发通知邮件。两侧相互独立，用户可选一个或两个。USE WHEN 新增用户, 开户, 新员工开账号, 建账号, 批量开户, provision user, 加 office, 加 adobe, 给 XX 开账号.
required_env:
  - CLIENT_ID
  - TENANT_ID
  - CLIENT_SECRET
  - DEFAULT_PASSWORD
  - DEFAULT_DOMAIN
  - ADOBE_CLIENT_ID
  - ADOBE_CLIENT_SECRET
  - ADOBE_ORG_ID
optional_env:
  - FORCE_CHANGE_PASSWORD
  - NOTIFICATION_ENABLED
  - NOTIFICATION_FROM_EMAIL
  - NOTIFICATION_BCC_EMAILS
  - NOTIFICATION_EMAIL_DOMAIN
  - SMTP_HOST
  - SMTP_PORT
  - SMTP_USERNAME
  - SMTP_PASSWORD
  - SMTP_USE_SSL
  - ADOBE_API_BASE_URL
  - ADOBE_DEFAULT_DOMAIN
requires:
  - "python>=3.9"
  - "pip package: requests, python-dotenv"
  - "office-usertools CLI checked out locally"
---

## Project Repo

🔗 **https://github.com/eggyrooch-blip/office365-tools**

本 skill 依赖上面这个 Python CLI。Agent 执行前**先确认 repo 已 clone 到本地**；遇到任何不确定的实现细节（CLI 子命令签名、`.env` 变量名、产品 ID、Adobe 用户类型）**优先去仓库查 `README.md` / `CLAUDE.md` / `docs/`**，不要凭本 skill 描述臆断。仓库是 single source of truth。

## Prerequisites（必读）

1. `git clone https://github.com/eggyrooch-blip/office365-tools && cd office365-tools && pip install -r requirements.txt`
2. 在该仓库根创建 `.env`，按下方模板填写
3. Office 365：Entra App 已授予 `User.ReadWrite.All / LicenseAssignment.ReadWrite.All / User-PasswordProfile.ReadWrite.All` 管理员同意
4. Adobe：Developer Console 已建 OAuth Server-to-Server credential 绑定 User Management API
5. 首次运行：`python main.py office365 init` 和 `python main.py adobe init --force-default`（选默认产品，例如 All Apps）

### `.env` 模板（复制到 office-usertools/.env 后按实际填写）

```env
# --------- Office 365（世纪互联） ---------
CLIENT_ID=your-entra-app-client-id
TENANT_ID=your-entra-tenant-id
CLIENT_SECRET=your-entra-app-secret
DEFAULT_PASSWORD=ChangeMe@2025
DEFAULT_DOMAIN=yourcorp.partner.onmschina.cn
FORCE_CHANGE_PASSWORD=true

# 通知邮件（推荐开启）
NOTIFICATION_ENABLED=true
NOTIFICATION_FROM_EMAIL=it-tools@yourcorp.com
NOTIFICATION_BCC_EMAILS=it@yourcorp.com
NOTIFICATION_EMAIL_DOMAIN=yourcorp.com

# SMTP（示例：飞书邮箱）
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
```


## MANDATORY TRIGGER

| 用户说 | 动作 |
|---|---|
| "给 XX 开账号" / "新建用户" / "新增用户" | 询问 provider 后执行 |
| "新员工开账号" / "入职开账号" | 同时 O365 + Adobe |
| "给 XX 开 Office" / "加 Office" | 仅 O365 |
| "给 XX 开 Adobe" / "加 Adobe" | 仅 Adobe（默认 All Apps） |
| "批量开户" | 需要列表（CSV 或粘贴），批量执行 |

## 输入参数

| 参数 | 必填 | 说明 |
|---|---|---|
| **identifier** (LDAP) | ✅ | 用户名前缀，如 `zhangsan01` |
| **provider** | ✅ | `office365` / `adobe` / `both` |
| **display_name / 姓名** | 建议 | 若无则从 LDAP 自动拆分 |
| **product** | 可选 | O365: SKU Part Number；Adobe: Profile ID 或别名 `cc` / `ps` / `acrobat`；**Adobe 默认 All Apps** |
| **force_change_password** | 可选 | O365 首次登录强制改密，默认 `true` |
| **country** | 可选 | 默认 `CN` |

## 前提 & 环境

- 工作目录：`/Users/kite/Documents/office-usertools`（或通过 `OFFICE_USERTOOLS_PATH` 环境变量指定）
- `.env` 配齐 O365 + Adobe 凭据（见下方"环境变量清单"）
- 首次使用先跑：
  ```bash
  python main.py office365 init
  python main.py adobe init --force-default   # 选 All Apps 作为默认
  ```

## 执行步骤

### 1. 信息收集

若用户只说了名字没说 provider/LDAP，用 **AskUserQuestion** 一次拿齐：
- provider（O365 / Adobe / 两个）
- LDAP（全组织唯一，一般拼音 + 数字后缀）
- 显示名 / 中文名
- Adobe 产品（默认走 All Apps 时不问）

### 2. Office 365 创建

```bash
python main.py office365 create <ldap> --display-name "<中文名>" [--product O365_BUSINESS]
```
- 未指定 `--product` 时用 state 里 init 设置的默认 license
- CLI 会：创建用户 → 分配 license → 按 `.env` 的 SMTP 发通知邮件（含初始密码）
- 成功返回字段里应有 `id`、`userPrincipalName`、`password`

### 3. Adobe 创建

```bash
python main.py adobe create <ldap>@<domain> [--product cc|ps|acrobat]
```
- **默认产品 = All Apps Configuration**（已缓存到 state/adobe_state.json preferences）
- `--product cc` / `all` → All Apps
- `--product ps` → Photoshop
- `--product acrobat` → Acrobat Pro
- 未指定时自动走默认
- 底层命令：`addAdobeID` + `add group` 一次请求完成邀请与授权
- 期望返回：`{"completed":1, "result":"success"}`

**注意**：
- Adobe 以邀请机制运作（addAdobeID），新账号会收到 Adobe 邀请邮件；若邮箱域不是本 org 的 federatedID/enterpriseID claimed domain，必须走 adobeID 类型
- 已知 `yourcorp.com` 是 adobeID 路径（非 org 声明域）

### 4. 双平台同时创建

若 provider=both，顺序执行 O365 → Adobe。任何一侧失败都继续但最后汇总：
```
✅ Office 365: zhangsan01@yourcorp.partner.onmschina.cn (密码已邮件发送)
✅ Adobe: zhangsan01@yourcorp.com (All Apps, 邀请已发)
```
失败项标 `❌` 并保留错误信息，让用户决定补救。

### 5. 结果验证

对每一侧用 `inspect` 验证：
```bash
python main.py office365 inspect <ldap> --json
python main.py adobe inspect <ldap>@yourcorp.com --json
```

### 6. 交付产出

给用户一份摘要：
- 账号清单（LDAP + email + 初始密码 / 邀请说明）
- 已授权产品
- 首次登录链接（O365: https://portal.partner.microsoftonline.cn；Adobe: https://creativecloud.adobe.com）

## 环境变量清单（.env）

**Office 365（世纪互联）**
```
CLIENT_ID=<Entra App Client ID>
TENANT_ID=<Entra Tenant ID>
CLIENT_SECRET=<Entra App Secret>
DEFAULT_PASSWORD=<初始密码>
DEFAULT_DOMAIN=<租户域，如 yourcorp.partner.onmschina.cn>
FORCE_CHANGE_PASSWORD=true

# 通知邮件（可选）
NOTIFICATION_ENABLED=true
NOTIFICATION_FROM_EMAIL=<发件邮箱>
NOTIFICATION_BCC_EMAILS=<抄送>
NOTIFICATION_EMAIL_DOMAIN=<用户收件邮箱域>

# SMTP（飞书邮箱示例）
SMTP_HOST=smtp.feishu.cn
SMTP_PORT=465
SMTP_USERNAME=<发件邮箱>
SMTP_PASSWORD=<SMTP 密码>
SMTP_USE_SSL=true
```

**Adobe UMAPI**
```
ADOBE_CLIENT_ID=<Adobe Developer Console Client ID>
ADOBE_CLIENT_SECRET=<Client Secret>
ADOBE_ORG_ID=<IMS Org ID，格式 xxx@AdobeOrg>
ADOBE_TECH_ACCOUNT_ID=<Technical Account ID，可选>
ADOBE_API_BASE_URL=https://usermanagement.adobe.io/v2/usermanagement
ADOBE_DEFAULT_DOMAIN=yourcorp.com
```

## Red Flags

| 症状 | 原因 | 处理 |
|---|---|---|
| O365 `Insufficient privileges` | App 权限未授予管理员同意 | 去 Entra → API 权限 → 授予管理员同意 |
| O365 `License not available` | license 池用完 | 购买或回收，不要硬删其他人 |
| Adobe `error.group.license_quota_exceeded` | 产品座位不够 | 报告给用户，不要默默降级到其他产品 |
| Adobe `error.domain.trust.nonexistent` | 尝试用 federatedID 但域名未被本 org 声明 | 改用 adobeID 类型（默认就是） |
| Adobe 429 Retry-After >30min | get_all_users 打满配额 | 本 skill 不需要 get_all_users；若被调用了说明走错了路径 |

## 安全红线

- **不覆盖已有用户**：如果 inspect 返回 200，先用 AskUserQuestion 确认是"重置"还是"跳过"
- **初始密码不回显到日志**：只出现在邮件正文，控制台输出做脱敏
- **LDAP 不自作主张生成**：必须用户明确给出，否则询问
- **Adobe 默认 All Apps 前显示座位余量**：避免无意触发 quota 失败
