# 飞书 + 邮件发送配置

## 飞书（Feishu/Lark）

### 环境变量

```bash
FEISHU_CHAT_ID=oc_xxxx  # 飞书群会话 ID 或用户 open_id
```

### 获取 Chat ID

- **群聊**：在飞书群设置 → 群信息 → 基本信息 → 群 ID
- **单聊**：直接使用用户的 `open_id`（以 `ou_` 开头）

### 消息卡片格式

摘要消息为 Markdown 格式，包含：
- 采集时间、主机总数、主机组数
- 重点关注列表（内存占用≥60% 或 CPU≥60% 的主机，最多20条）
- 告警着色（红色=≥80%，橙色=≥60%，黄色=≥40%）

---

## 邮件发送

### 环境变量

```bash
SMTP_HOST=smtp.example.com
SMTP_PORT=465          # SSL 端口，通常 465
SMTP_FROM=alarm@example.com
SMTP_TOKEN=your_smtp_token  # 163邮箱用授权码，其他邮箱用密码
TARGET_EMAIL=admin@example.com
```

### 常见 SMTP 配置

| 邮箱 | SMTP_HOST | PORT | 说明 |
|------|-----------|------|------|
| 163 | `smtp.163.com` | 465 | 用授权码（非登录密码） |
| QQ | `smtp.qq.com` | 465 | 用授权码 |
| Gmail | `smtp.gmail.com` | 587 | 用应用专用密码 |

### 发送内容

- **主题**：服务器监控报告 `YYYY-MM-DD HH:MM`
- **正文**：HTML 格式的摘要（与飞书卡片内容一致）
- **附件**：`zabbix_monitor.xlsx`（Excel 报告）

### 跳过邮件

如果不想发送邮件，只填 `FEISHU_CHAT_ID` 而不填 `SMTP_*`，则只发飞书不发邮件。
