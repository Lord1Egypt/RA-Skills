# Remnawave Robot 🤖

**技能 ID:** remnawave-robot  
**版本:** 1.0.1  
**作者:** AI Assistant (小 a)  
**创建时间:** 2026-03-18  
**用途:** Remnawave 账号全生命周期自动化管理

---

## 📋 技能描述

Remnawave Robot 是一个完整的 Remnawave 账号自动化管理工具集，覆盖从配置到运维的全流程：

### 🎯 核心功能
1. **配置向导** - 交互式配置邮箱、API Token 等
2. **账号创建** - 自动创建账号并发送开通邮件
3. **分组管理** - 同步分组、添加/移除用户分组
4. **账号查询** - 搜索账号、查看详情
5. **账号删除** - 安全删除账号
6. **批量操作** - 批量创建、批量修改

### ✨ 特色优势
- ✅ **一站式配置** - 首次使用引导式配置
- ✅ **订阅地址不变** - 分组更新不影响订阅
- ✅ **邮件通知** - 自动发送开通/变更邮件
- ✅ **完整日志** - 所有操作自动记录
- ✅ **安全可靠** - 凭证加密存储，权限严格控制

---

## 🚀 快速开始

### 1️⃣ 首次使用 - 配置向导

```bash
cd ~/.openclaw/workspace/skills/remnawave-robot
node setup.js
```

**配置内容:**
- Remnawave API 地址
- Remnawave API Token
- SMTP 发件邮箱配置
- 默认邮件模板

### 2️⃣ 创建账号

```bash
node create-account.js \
  --username jim_pc \
  --email jim@codeforce.tech \
  --squad "Operations Team" \
  --cc crads@codeforce.tech
```

### 3️⃣ 管理分组

```bash
# 同步最新分组列表
node sync-squads.js

# 添加用户到分组
node add-to-squad.js --username jim_pc --squad "Access Gateway"

# 查询用户分组
node get-squads.js --username jim_pc
```

### 4️⃣ 搜索账号

```bash
node search-account.js jim
```

---

## 📖 完整命令列表

| 功能 | 命令 | 说明 |
|------|------|------|
| **配置向导** | `node setup.js` | 首次使用配置 API 和邮箱 |
| **创建账号** | `node create-account.js` | 创建账号并发送邮件 |
| **搜索账号** | `node search-account.js <关键词>` | 搜索用户账号 |
| **查询分组** | `node get-squads.js` | 查看用户分组 |
| **添加分组** | `node add-to-squad.js` | 添加用户到分组 |
| **设置分组** | `node set-squads.js` | 覆盖用户分组列表 |
| **移除分组** | `node remove-from-squad.js` | 从分组移除用户 |
| **同步分组** | `node sync-squads.js` | 同步 API 分组到本地 |
| **列出分组** | `node list-squads.js` | 显示所有分组 |
| **删除账号** | `node delete-account.js` | 删除指定账号 |
| **查看配置** | `node config.js` | 查看当前配置 |

---

## 🔧 配置说明

### 方式 1: 交互式配置（推荐）

```bash
node setup.js
```

按提示输入：
1. Remnawave API 地址
2. Remnawave API Token
3. 发件邮箱地址
4. SMTP 服务器地址
5. SMTP 端口
6. 邮箱密码/授权码

### 方式 2: 手动配置

**Remnawave 配置** (`config/remnawave.json`):
```json
{
  "apiBaseUrl": "https://8.212.8.43",
  "apiVersion": "v1",
  "sslRejectUnauthorized": false,
  "_note": "自签名证书，需要忽略 SSL 验证"
}
```

**API Token** (`.env`):
```bash
REMNAWAVE_API_TOKEN=your_api_token_here
```

**SMTP 配置** (`config/smtp.json`):
```json
{
  "host": "smtp.zoho.com",
  "port": 587,
  "secure": false,
  "auth": {
    "user": "crads@codeforce.tech",
    "pass": "your_email_password"
  },
  "from": {
    "email": "crads@codeforce.tech",
    "name": "AI Assistant"
  }
}
```

---

## 📧 邮件模板

默认模板位置：`templates/account-created.md`

**可用变量:**
- `{{recipient_name}}` - 收件人姓名
- `{{account_name}}` - 账号名称
- `{{subscription_url}}` - 订阅地址
- `{{tutorial_url}}` - 使用教程链接
- `{{send_date}}` - 发送日期

---

## 📋 使用示例

### 示例 1: 创建完整账号

```bash
node create-account.js \
  --username west_pc \
  --email west@example.com \
  --device-limit 1 \
  --traffic-gb 100 \
  --traffic-reset WEEKLY \
  --expire-days 365 \
  --squad "Operations Team" \
  --cc admin@codeforce.tech
```

### 示例 2: 调整用户分组

```bash
# 先查询当前分组
node get-squads.js --username west_pc

# 添加新分组（保留现有）
node add-to-squad.js --username west_pc --squad "Access Gateway"

# 验证结果
node get-squads.js --username west_pc
```

### 示例 3: 批量创建账号

```bash
# 准备用户列表 (users.csv)
# username,email,squad
# user1,user1@example.com,Operations Team
# user2,user2@example.com,QA Engineer

node batch-create.js --file users.csv
```

---

## 🔍 故障排查

### 问题 1: 配置不完整

**症状:** `❌ 配置不完整，请先运行 setup.js`

**解决:**
```bash
node setup.js
```

### 问题 2: API 连接失败

**症状:** `network error` 或 `SSL certificate problem`

**解决:**
```json
// config/remnawave.json
{
  "sslRejectUnauthorized": false
}
```

### 问题 3: 邮件发送失败

**症状:** `SMTP connection failed`

**解决:**
1. 检查 SMTP 配置
2. 验证邮箱密码/授权码
3. 确认端口和加密方式正确

### 问题 4: 找不到分组

**症状:** `找不到分组 "XXX"`

**解决:**
```bash
node sync-squads.js
```

---

## 🔐 安全注意事项

1. **凭证安全**
   - API Token 存储在 `.env`，权限 600
   - SMTP 密码加密存储
   - 不要将凭证提交到版本控制

2. **操作审计**
   - 所有操作记录到 `logs/` 目录
   - 定期审查操作日志
   - 敏感操作需二次确认

3. **权限控制**
   - 仅授权人员可执行创建/删除
   - 批量操作需审批
   - 生产环境谨慎测试

---

## 📝 更新日志

### v1.0.0 (2026-03-18)
- ✅ 初始版本发布
- ✅ 配置向导
- ✅ 账号创建 + 邮件发送
- ✅ 分组管理（同步/添加/设置/移除）
- ✅ 账号搜索
- ✅ 账号删除
- ✅ 完整日志记录
- ✅ 批量操作支持

---

## 📞 支持

**文档:** 查看 `README.md` 获取详细文档  
**问题:** 联系运维组 Crads  
**邮箱:** crads@codeforce.tech

---

**最后更新:** 2026-03-18  
**许可:** MIT License  
**作者:** AI Assistant (小 a)
