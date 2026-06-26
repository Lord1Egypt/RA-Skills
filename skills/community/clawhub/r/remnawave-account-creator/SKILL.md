# Remnawave 账号创建与邮件发送

**技能 ID:** remnawave-account-creator  
**版本:** 1.1.0 (2026-03-19 修复)  
**作者:** AI Assistant (小 a)  
**创建时间:** 2026-03-08  
**更新时间:** 2026-03-19  
**用途:** 自动化创建 Remnawave 账号并发送开通邮件，支持分组管理

---

## 📋 技能描述

本技能用于自动化完成 Remnawave 账号的完整开通流程：
1. 调用 Remnawave API 创建新用户
2. 自动获取订阅地址和账号信息
3. 使用预设模板发送开通邮件
4. 支持抄送功能

**适用场景:**
- 运维组需要批量创建用户账号
- 自动化用户开通流程
- 标准化账号管理

---

## 🔧 前置配置

### 1. Remnawave API 配置

创建 `~/.openclaw/workspace/config/remnawave.json`:

```json
{
  "apiBaseUrl": "https://8.212.8.43",
  "apiToken": "YOUR_API_TOKEN",
  "sslRejectUnauthorized": false,
  "_status": "已验证连接成功",
  "_userCount": 43
}
```

**获取 API Token:**
1. 登录 Remnawave 管理后台
2. 进入 API 设置页面
3. 创建新的 API Token（选择 API 角色）
4. 复制 Token 到配置文件

### 2. SMTP 邮件配置

创建 `~/.openclaw/workspace/config/smtp.json`:

```json
{
  "host": "smtp.zoho.com",
  "port": 587,
  "secure": false,
  "auth": {
    "user": "your-email@company.com",
    "pass": "YOUR_EMAIL_PASSWORD"
  },
  "tls": {
    "rejectUnauthorized": false
  },
  "from": {
    "email": "your-email@company.com",
    "name": "AI Assistant"
  }
}
```

### 3. 邮件模板配置

确保模板文件存在：
- `~/.openclaw/workspace/config/email-templates/remnawave-account-created.md`

### 4. 内部组 UUID 映射

创建 `~/.openclaw/workspace/config/remnawave-squads.json`:

```json
{
  "squads": {
    "Default-Squad": "751440da",
    "xray-default": "fe107de3",
    "QA Engineer": "1f85b65c",
    "Front-end Developer": "48a0679d",
    "TW": "25ef1b48",
    "Back-end Developer": "071aee4a",
    "Ops Debugging": "ccca8442"
  }
}
```

---

## 📖 使用方法

### 方式 1: 直接调用技能

```bash
claw skill run remnawave-account-creator \
  --username jim_pc \
  --email jim@codeforce.tech \
  --device-limit 1 \
  --traffic-gb 100 \
  --traffic-reset WEEKLY \
  --expire-days 365 \
  --squad "Ops Debugging" \
  --cc crads@codeforce.tech
```

### 方式 2: 使用脚本

```bash
cd ~/.openclaw/workspace/skills/remnawave-account-creator
node create-account.js \
  --username jim_pc \
  --email jim@codeforce.tech \
  --squad "Ops Debugging" \
  --cc crads@codeforce.tech
```

### 方式 3: 自然语言指令

直接告诉 AI 助理：
```
新增账号
账号：jim_pc
登录设备限制：1
流量限制：100G
流量重置：每周
过期时间：一年
内部分组：Ops Debugging
邮箱：jim@codeforce.tech
邮件抄送：crads@codeforce.tech
```

---

## 📋 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `username` | ✅ | 账号用户名 | `jim_pc` |
| `email` | ✅ | 用户邮箱 | `jim@codeforce.tech` |
| `device-limit` | ❌ | 设备限制（默认 1） | `1` |
| `traffic-gb` | ❌ | 流量限制 GB（默认 100） | `100` |
| `traffic-reset` | ❌ | 流量重置周期 | `每周` / `每月` / `每天` |
| `expire-days` | ❌ | 过期天数（默认 365） | `365` |
| `squad` | ❌ | 内部分组名称 | `Ops Debugging` |
| `cc` | ❌ | 邮件抄送地址 | `crads@codeforce.tech` |

**API 参数映射：**
- 流量重置：`trafficLimitStrategy` (WEEK/MONTH/DAY/NO_RESET)
- 内部分组：`activeInternalSquads` (UUID 数组)

---

## 🔄 执行流程

```
1. 读取配置文件
   ├── remnawave.json (API 配置)
   ├── smtp.json (邮件配置)
   └── remnawave-squads.json (组映射)

2. 调用 Remnawave API 创建用户
   POST /api/users
   ├── username
   ├── email
   ├── hwidDeviceLimit
   ├── trafficLimitBytes
   ├── trafficResetInterval
   ├── expireAt
   └── squadUuids

3. 解析 API 响应
   ├── subscriptionUrl (订阅地址)
   ├── shortUuid (短 UUID)
   ├── vlessUuid (VLESS UUID)
   ├── trojanPassword (Trojan 密码)
   └── ssPassword (SS 密码)

4. 渲染邮件模板
   ├── recipient_name
   ├── account_name
   ├── subscription_url
   ├── tutorial_url
   ├── download_url
   └── send_date

5. 发送邮件
   ├── 收件人：用户邮箱
   └── 抄送：指定邮箱（可选）

6. 输出结果
   ├── 账号信息
   ├── 订阅地址
   └── 邮件发送状态
```

---

## 📧 邮件模板变量

| 变量 | 说明 | 来源 |
|------|------|------|
| `{{recipient_name}}` | 收件人姓名 | username |
| `{{account_name}}` | 账号名称 | username |
| `{{subscription_url}}` | 订阅地址 | API 响应 |
| `{{tutorial_url}}` | 证书安装教程 | 固定配置 |
| `{{download_url}}` | 客户端下载 | 固定配置 |
| `{{send_date}}` | 发送日期 | 当前日期 |

---

## 🛠️ 文件结构

```
remnawave-account-creator/
├── SKILL.md                      # 技能说明（本文件）
├── create-account.js             # 主执行脚本
├── send-template-email.js        # 邮件发送脚本
└── README.md                     # 使用文档
```

---

## ⚠️ 注意事项

1. **API Token 安全**
   - 不要将 Token 提交到版本控制
   - 定期更换 Token
   - 限制 Token 权限

2. **SSL 证书**
   - 如果使用自签名证书，设置 `sslRejectUnauthorized: false`
   - 生产环境建议使用正式证书

3. **邮件发送**
   - 确保 SMTP 配置正确
   - 测试邮件发送功能
   - 注意邮件发送频率限制

4. **流量单位**
   - API 使用 bytes 为单位
   - 1GB = 1073741824 bytes

5. **日期格式**
   - API 使用 ISO 8601 格式
   - 示例：`2027-03-08T00:00:00.000Z`

---

## 🔍 故障排查

### 问题 1: API 连接失败

**症状:** `curl: (60) SSL certificate problem`

**解决:**
```json
{
  "sslRejectUnauthorized": false
}
```

### 问题 2: 邮件发送失败

**症状:** `SMTP connection failed`

**解决:**
- 检查 SMTP 配置
- 验证邮箱密码
- 确认端口和加密方式

### 问题 3: 组 UUID 找不到

**症状:** `Squad not found`

**解决:**
- 运行 `node list-squads.js` 获取最新组列表
- 更新 `remnawave-squads.json`

---

## 📝 更新日志

### v1.0.0 (2026-03-08)
- ✅ 初始版本发布
- ✅ 支持账号创建
- ✅ 支持邮件发送
- ✅ 支持抄送功能
- ✅ 支持流量重置配置
- ✅ 支持内部分组分配

---

## 📦 ClawHub 发布

**技能 Slug:** `remnawave-account-creator`
**当前版本:** 1.1.0
**发布 ID:** `k978ydgq28482dtbyr8ey5vnp58375q3`

**安装命令:**
```bash
clawhub install remnawave-account-creator --version 1.1.0
```

**更新日志 (v1.1.0 - 2026-03-19):**
- 修复 API 调用错误：更新分组端点从 `PUT /api/users/{uuid}` 改为 `PATCH /api/users`
- 修复分页参数：从 `page=1&limit=500` 改为 `page=0&size=200`
- 修复 callApi 响应解析
- 添加完整 API 参考文档

---

## 🔐 隐私设置

**访问权限:** 私密（仅作者可用）
**发布平台:** ClawHub
**作者:** AI Assistant (小 a)

---

## 📞 支持

如有问题，请联系：
- 作者：AI Assistant (小 a)
- 运维组：Crads
- 邮箱：crads@codeforce.tech
