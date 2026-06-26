# Remnawave Robot 发布总结 🤖

**发布时间:** 2026-03-18  
**版本:** 1.0.0  
**Skill ID:** k9748nq3jny93434sykvedpnkx834n6t

---

## 📦 技能信息

**名称:** Remnawave Robot  
**描述:** Remnawave 账号全生命周期自动化管理  
**作者:** AI Assistant (小 a)  
**许可:** MIT

---

## 🎯 核心功能

### 1️⃣ 配置向导
- 交互式配置 Remnawave API 和 SMTP 邮箱
- 自动创建配置文件和邮件模板
- 一键测试配置

### 2️⃣ 账号管理
- **创建账号** - 自动创建并发送开通邮件
- **搜索账号** - 关键词搜索，显示详细信息
- **删除账号** - 安全删除，支持强制模式

### 3️⃣ 分组管理
- **同步分组** - 从 API 同步最新分组列表
- **查询分组** - 查看用户当前分组
- **添加分组** - 添加用户到分组（订阅地址不变）
- **设置分组** - 覆盖用户分组列表

---

## 📁 文件结构

```
remnawave-robot/
├── SKILL.md              # 技能说明文档
├── README.md             # 使用文档
├── PUBLISH-SUMMARY.md    # 发布总结（本文件）
├── package.json          # npm 配置
├── .gitignore            # Git 忽略文件
├── setup.js              # 配置向导
├── test-config.js        # 配置测试
├── create-account.js     # 创建账号
├── search-account.js     # 搜索账号
├── get-squads.js         # 查询分组
├── add-to-squad.js       # 添加分组
├── sync-squads.js        # 同步分组
├── delete-account.js     # 删除账号
├── config/               # 配置目录
│   ├── remnawave.json    # API 配置
│   ├── smtp.json         # 邮箱配置
│   └── remnawave-squads.json  # 分组映射
├── templates/            # 邮件模板
│   └── account-created.md
├── scripts/              # 辅助脚本
└── lib/                  # 库文件
```

---

## 🚀 安装方法

### 方式 1: 从 ClawHub 安装

```bash
clawhub install remnawave-robot
```

### 方式 2: 手动安装

```bash
cd ~/.openclaw/workspace/skills
git clone <repo-url> remnawave-robot
cd remnawave-robot
npm install
```

---

## 📖 使用指南

### 1. 配置（首次使用）

```bash
cd ~/.openclaw/workspace/skills/remnawave-robot
node setup.js
```

### 2. 测试配置

```bash
node test-config.js
```

### 3. 创建账号

```bash
node create-account.js \
  --username jim_pc \
  --email jim@codeforce.tech \
  --squad "Operations Team" \
  --cc crads@codeforce.tech
```

### 4. 搜索账号

```bash
node search-account.js jim
```

### 5. 管理分组

```bash
# 同步分组
node sync-squads.js

# 添加分组
node add-to-squad.js --username jim_pc --squad "Access Gateway"

# 查询分组
node get-squads.js --username jim_pc
```

---

## 🔧 配置说明

### Remnawave API 配置

```json
{
  "apiBaseUrl": "https://8.212.8.43",
  "apiVersion": "v1",
  "sslRejectUnauthorized": false
}
```

### SMTP 邮箱配置

```json
{
  "host": "smtp.zoho.com",
  "port": 587,
  "secure": false,
  "auth": {
    "user": "crads@codeforce.tech",
    "pass": "your_password"
  },
  "from": {
    "email": "crads@codeforce.tech",
    "name": "AI Assistant"
  }
}
```

---

## ⚠️ 重要提示

### 订阅地址不变原则

✅ **正确做法:** 使用 `PATCH /api/users` 更新分组  
❌ **错误做法:** 删除重建账号

使用本工具添加/修改分组，**订阅地址不会变化**，客户端无需重新配置。

### 安全注意事项

1. 凭证文件权限自动设置为 600
2. 不要将 `.env` 和 `config/` 提交到版本控制
3. 定期更换 API Token 和邮箱密码
4. 删除账号需使用 `--force` 确认

---

## 📊 功能测试

### 已测试功能

- ✅ 配置向导（setup.js）
- ✅ 配置测试（test-config.js）
- ✅ 搜索账号（search-account.js）
- ✅ 查询分组（get-squads.js）
- ✅ 添加分组（add-to-squad.js）
- ✅ 同步分组（sync-squads.js）
- ✅ 创建账号（create-account.js）
- ✅ 邮件发送（nodemailer）

### 测试结果

```
✅ API 连接成功
✅ SMTP 连接成功
✅ 搜索功能正常
✅ 分组更新正常（订阅地址不变）
✅ 邮件发送成功
```

---

## 🔄 更新日志

### v1.0.6 (2026-03-18 14:25) - 完全复制旧脚本

**🔴 反思:**
- 问题：重新发明轮子，没有直接复制旧代码
- 根因：思维没有跟上，总想"优化"而不是"复制"
- 教训：已验证的代码直接复制，不要重新实现！

**Bug 修复:**
- ✅ 直接复制旧脚本 send-template-email.js 的邮件发送逻辑
- ✅ 模板格式与旧模板完全一致（HTML+ 纯文本）
- ✅ 邮件发送逻辑与旧脚本 100% 一致
- ✅ 验证测试：邮件发送成功

**关键代码（与旧脚本一致）:**
```javascript
const mailOptions = {
  from: `"${smtpConfig.from.name}" <${smtpConfig.from.email}>`,
  to: to,
  subject: `【VPN】账号已创建 - 运维组 Crads`,
  text: textContent,  // 必须有
  html: htmlContent   // 必须有
};
```

### v1.0.5 (2026-03-18 14:20) - 邮件模板修复版

**🔴 问题:**
- 邮件模板格式不正确（简单的 Markdown）
- 缺少下载链接、教程链接等重要信息
- 对比旧模板发现：旧模板是完整的 HTML 格式

**Bug 修复:**
- ✅ 替换为完整的 HTML 邮件模板（带样式）
- ✅ 添加所有必需变量（tutorial_url, download_url, download_backup, appstore_url）
- ✅ 使用官方下载链接和备用链接
- ✅ 统一使用旧模板的内容和格式

**模板变量:**
```javascript
{
  recipient_name: '用户名',
  recipient_email: '邮箱',
  account_name: '账号名',
  subscription_url: '订阅地址',
  tutorial_url: '安装教程',
  download_url: 'Windows 官方下载',
  download_backup: 'Windows 备用下载',
  appstore_url: 'Mac/iOS 下载'
}
```

### v1.0.4 (2026-03-18 14:15) - 邮件发送修复版

**🔴 根因分析:**
- 问题：邮件发送失败 `553 Sender is not allowed to relay emails`
- 根因：`from` 字段格式错误 + 缺少 `text` 字段
- 对比旧脚本发现：旧脚本使用字符串格式的 `from` 字段

**Bug 修复:**
- ✅ 修复 `from` 字段格式（对象 → 字符串 `"${name}" <${email}>`）
- ✅ 添加 `text` 字段（必须与 `html` 同时存在）
- ✅ 统一使用旧脚本的邮件配置方式
- ✅ 验证测试：jung_pc 和 west_pc 邮件发送成功

**邮件配置（正确格式）:**
```javascript
{
  from: `"${config.from.name}" <${config.from.email}>`,
  text: '纯文本内容',
  html: '<h1>HTML 内容</h1>'
}
```

### v1.0.3 (2026-03-18 14:05)

### v1.0.2 (2026-03-18 14:01)

**Bug 修复:**
- ✅ 修复邮件发送失败时 messageId 未定义错误
- ✅ 改进错误输出（显示订阅地址方便手动发送）

**功能改进:**
- ✅ 邮件发送失败时自动显示订阅地址
- ✅ 支持飞书消息通知作为备用方案

### v1.0.1 (2026-03-18)

**Bug 修复:**
- ✅ 修复流量重置策略映射（WEEKLY → WEEK）
- ✅ 修复 HTTP 状态码判断（支持 200 和 201）
- ✅ 验证测试：成功创建 jung_pc 账号

### v1.0.0 (2026-03-18)

**新增功能:**
- ✅ 配置向导
- ✅ 账号创建 + 邮件发送
- ✅ 账号搜索
- ✅ 分组管理（同步/查询/添加/设置）
- ✅ 账号删除
- ✅ 配置测试

**技术特点:**
- 使用 `PATCH /api/users` 更新分组（订阅地址不变）
- 完整的错误处理
- 自动日志记录
- 安全的凭证管理

---

## 📞 支持与反馈

**问题反馈:**  
- 邮箱：crads@codeforce.tech
- ClawHub 仓库：remnawave-robot

**文档:**
- SKILL.md - 完整技能说明
- README.md - 快速开始指南

---

## 🎉 发布成功

**ClawHub 发布:** ✅ 成功  
**Skill ID:** k9748nq3jny93434sykvedpnkx834n6t  
**版本:** 1.0.0  
**时间:** 2026-03-18

**安装命令:**
```bash
clawhub install remnawave-robot
```

---

**最后更新:** 2026-03-18  
**作者:** AI Assistant (小 a)
