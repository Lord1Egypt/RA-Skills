# Sendflare Skill

通过 Sendflare SDK 发送电子邮件和管理联系人的 OpenClaw Skill。

## 功能特点

- 📧 发送电子邮件（支持 CC/BCC）
- 👥 获取联系人列表
- ➕ 保存/更新联系人
- ❌ 删除联系人
- 🔒 安全的 API 认证
- 📝 完整的 TypeScript 类型定义

## 安装

```bash
# 从 ClawHub 安装
clawhub install sendflare-skill

# 或手动安装
git clone <repo-url> ~/.agents/skills/sendflare-skill
```

## 配置

使用前需要配置 Sendflare API Token：

```json
{
  "apiToken": "your-Sendflare-api-token"
}
```

## 使用方法

### 发送邮件

```
发送邮件给 test@example.com，主题：会议通知，内容：明天下午 3 点开会
```

### 获取联系人列表

```
获取联系人列表
```

### 保存联系人

```
保存联系人 john@example.com，姓名：John Doe
```

### 删除联系人

```
删除联系人 john@example.com
```

## 开发

```bash
# 安装依赖
npm install

# 编译 TypeScript
npm run build

# 监听模式
npm run watch
```

## 许可证

MIT
