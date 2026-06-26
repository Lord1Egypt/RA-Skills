# 凭证配置子流程

> 当 Skill 需要外部服务凭证但缺失时，按此流程引导用户配置。

## 通用流程

```
检查环境变量 → 全部存在则跳过 → 缺失则进入配置：
1. 告知需要什么、为什么
2. 引导获取（给具体步骤和链接）
3. 用户提供 → 写入环境变量
4. 立即验证 → 成功则永久可用，失败则告知原因
```

## 凭证模板

### 邮件（SMTP）
```
EMAIL_SMTP_HOST=smtp.feishu.cn / smtp.qq.com / smtp.163.com / smtp.gmail.com
EMAIL_SMTP_PORT=465（SSL）或 587（STARTTLS）
EMAIL_USER=user@company.com
EMAIL_PASS=应用专用密码（非主密码）
```
验证：`smtplib.SMTP_SSL` 登录测试。

### 企业微信 Webhook
```
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***
```
获取：群设置→群机器人→添加→复制地址。
验证：`curl POST` 发测试消息。

### 数据库
```
DB_TYPE=mysql / postgresql / sqlite
DB_HOST / DB_PORT / DB_USER（建议只读账号）/ DB_PASS / DB_NAME
```

### 飞书扩展权限
不需要额外凭证，但需在 open.feishu.cn 启用 API 权限（日历/邮件等）。

## 环境变量持久化

| Agent | 写入位置 |
|-------|---------|
| Hermes | `~/.hermes/.env` 或 `~/.zshrc` |
| OpenClaw | `~/.openclaw/.env` |
| Claude Code | `~/.claude/.env` 或 shell profile |

写入时先 `grep` 检查是否已存在，避免重复。跨平台 sed 兼容：
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s|^export ${key}=.*|export ${key}=${value}|" "$profile"
else
  sed -i "s|^export ${key}=.*|export ${key}=${value}|" "$profile"
fi
```

## 在 Skill 中的用法

生成的 SKILL.md 中，需凭证的步骤写明：
1. 检查哪些环境变量
2. 缺失时执行本子流程
3. 验证方式
4. 失败时的降级策略

## 设计原则
1. 凭证只问一次（存环境变量）
2. 引导要具体（去哪找、怎么获取）
3. 验证要即时（配完马上测）
4. 安全要提醒（用应用专用密码，建议只读账号）
