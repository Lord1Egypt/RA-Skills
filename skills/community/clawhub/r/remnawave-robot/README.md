# Remnawave Robot 🤖

Remnawave 账号全生命周期自动化管理工具

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/remnawave-robot
npm install
```

### 2. 配置向导

```bash
node setup.js
```

按提示配置：
- Remnawave API 地址和 Token
- SMTP 发件邮箱

### 3. 测试配置

```bash
node test-config.js
```

**如果 SMTP 测试失败:**
- 查看 `SMTP-FIX.md` 排查指南
- 或使用飞书消息作为备用通知方式

### 3. 创建账号

```bash
node create-account.js \
  --username jim_pc \
  --email jim@codeforce.tech \
  --squad "Operations Team" \
  --cc crads@codeforce.tech
```

## 📋 功能列表

| 功能 | 命令 | 说明 |
|------|------|------|
| 配置 | `node setup.js` | 交互式配置向导 |
| 测试配置 | `node test-config.js` | 测试 API 和 SMTP |
| 创建账号 | `node create-account.js` | 创建 + 邮件通知 |
| 补发邮件 | `node resend-email.js` | 手动补发邮件 |
| 搜索账号 | `node search-account.js <关键词>` | 搜索用户 |
| 查询分组 | `node get-squads.js` | 查看用户分组 |
| 添加分组 | `node add-to-squad.js` | 添加用户到分组 |
| 同步分组 | `node sync-squads.js` | 同步 API 分组 |
| 删除账号 | `node delete-account.js` | 删除账号 |

## 📖 使用示例

### 创建账号

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

### 管理分组

```bash
# 同步分组列表
node sync-squads.js

# 添加用户到分组
node add-to-squad.js --username west_pc --squad "Access Gateway"

# 查询用户分组
node get-squads.js --username west_pc
```

### 搜索账号

```bash
node search-account.js west
```

## 🔧 配置说明

配置向导会自动创建以下文件：

- `config/remnawave.json` - Remnawave API 配置
- `config/smtp.json` - SMTP 邮箱配置
- `../../.env` - API Token（权限 600）

## 🔐 安全提示

- 凭证文件权限自动设置为 600
- 不要将 `.env` 和 `config/` 提交到版本控制
- 定期更换 API Token

## 📞 支持

- 文档：查看 `SKILL.md`
- 邮箱：crads@codeforce.tech

---

**版本:** 1.0.0  
**作者:** AI Assistant (小 a)  
**许可:** MIT
