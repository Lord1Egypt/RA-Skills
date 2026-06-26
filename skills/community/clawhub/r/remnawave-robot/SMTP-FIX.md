# SMTP 邮件发送问题排查与修复

**问题时间:** 2026-03-18 14:02  
**影响:** jung_pc 和 west_pc 的开通邮件发送失败

---

## ❌ 错误现象

```
553 Sender is not allowed to relay emails
```

**当前状态:**
- ✅ SMTP 连接测试成功
- ❌ 邮件发送失败
- 🔴 根因：发件人邮箱未验证

---

## 🔍 根本原因

**Zoho SMTP 发件人验证失败**，已确认的问题：

1. ✅ **SMTP 密码正确** - 连接测试成功
2. ❌ **发件人未验证** - crads@codeforce.tech 需要在 Zoho 验证域名
3. ⚠️ **域名 DNS 记录** - 可能需要配置 SPF/DKIM

**验证步骤:**
```bash
# 运行修复脚本
./fix-zoho-smtp.sh

# 输出:
# ✅ SMTP 连接成功!
# ❌ 邮件发送失败: 553 Sender is not allowed to relay emails
```

---

## ✅ 解决方案

### 🔴 方案 1: 验证发件人域名（必须）

**这是当前问题的根本解决方案！**

**步骤:**

1. **登录 Zoho Mail 管理控制台**
   - 地址：https://mail.zoho.com
   - 账号：crads@codeforce.tech

2. **验证域名**
   - 设置 → 域名 → 添加域名
   - 或者：设置 → 邮件 → 发件人验证
   - 添加 codeforce.tech 域名

3. **配置 DNS 记录**
   - SPF 记录：`v=spf1 include:zoho.com ~all`
   - DKIM 记录：（Zoho 提供 CNAME 记录）
   - MX 记录：确保指向 Zoho

4. **等待 DNS 生效**
   - 通常需要 15 分钟 -24 小时
   - 使用 `nslookup -qt=txt codeforce.tech` 验证

5. **测试发信**
   ```bash
   cd /root/.openclaw/workspace/skills/remnawave-robot
   node test-email.js
   ```

---

### 🟡 方案 2: 使用已验证的邮箱

如果 crads@codeforce.tech 无法验证，使用其他已验证的邮箱：

**Gmail 示例:**
```json
{
  "provider": "gmail",
  "host": "smtp.gmail.com",
  "port": 587,
  "secure": false,
  "auth": {
    "user": "your@gmail.com",
    "pass": "app-password"
  },
  "from": {
    "email": "your@gmail.com",
    "name": "AI Assistant"
  }
}
```

**注意:** Gmail 需要开启两步验证并生成应用专用密码

---

### 🟡 方案 3: 重置 Zoho 邮箱密码

如果密码确实过期：

1. 登录 Zoho Mail: https://mail.zoho.com
2. 设置 → 安全 → 更改密码
3. 更新配置文件

**修改配置:**
```bash
cd /root/.openclaw/workspace/skills/remnawave-robot
vi config/smtp.json
```

**测试连接:**
```bash
node test-config.js
```

---

### 方案 2: 使用应用专用密码

如果开启了双因素认证，需要使用应用专用密码：

1. Zoho 账号 → 安全设置
2. 生成应用专用密码
3. 使用专用密码替换 SMTP 密码

---

### 方案 3: 更换发件邮箱

如果 crads@codeforce.tech 无法使用，可以：

1. 使用其他已验证的邮箱
2. 或者使用 Gmail/Outlook 等公共 SMTP

**Gmail SMTP 配置:**
```json
{
  "provider": "gmail",
  "host": "smtp.gmail.com",
  "port": 587,
  "secure": false,
  "auth": {
    "user": "your@gmail.com",
    "pass": "app-password"
  },
  "from": {
    "email": "your@gmail.com",
    "name": "AI Assistant"
  }
}
```

---

## 📋 临时解决方案

在 SMTP 修复前，使用以下方式通知用户：

### 方式 1: 飞书消息（已实现）

```bash
# 自动通过飞书发送账号信息
```

### 方式 2: 手动发送邮件

使用补发脚本：
```bash
node resend-email.js \
  --username jung_pc \
  --email jung@bydfi.com \
  --subscription-url https://46force235a-6cb1-crypto-link.datat.cc/api/sub/wBMXavTEzFbxxY57 \
  --cc crads@codeforce.tech
```

### 方式 3: 复制订阅地址直接发给用户

```
jung_pc: https://46force235a-6cb1-crypto-link.datat.cc/api/sub/wBMXavTEzFbxxY57
west_pc: https://46force235a-6cb1-crypto-link.datat.cc/api/sub/_6z3BUw1Ca5dqH0d
```

---

## 🧪 测试 SMTP 配置

**测试连接:**
```bash
node test-config.js
```

**测试发信:**
```bash
node test-email.js
```

**预期输出:**
```
✅ SMTP 连接成功
✅ 邮件发送成功
Message ID: <xxx@codeforce.tech>
```

---

## 📊 受影响账号

| 账号 | 邮箱 | 订阅地址 | 通知状态 |
|------|------|----------|----------|
| jung_pc | jung@bydfi.com | /sub/wBMXavTEzFbxxY57 | ✅ 飞书已通知 |
| west_pc | west@codeforce.tech | /sub/_6z3BUw1Ca5dqH0d | ✅ 飞书已通知 |

---

## 🔧 修复检查清单

- [ ] 登录 Zoho 验证账号状态
- [ ] 重置邮箱密码或生成应用专用密码
- [ ] 更新 config/smtp.json 配置
- [ ] 运行 node test-config.js 测试
- [ ] 运行 node test-email.js 发信测试
- [ ] 补发 jung_pc 和 west_pc 的邮件
- [ ] 更新技能到 ClawHub

---

## 📞 联系支持

如果问题持续，联系：
- Zoho 支持：support@zoho.com
- 运维组：crads@codeforce.tech

---

**最后更新:** 2026-03-18 14:05  
**状态:** 🔴 待修复
