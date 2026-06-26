---
name: email-manager
description: >
  企业邮箱管理（腾讯企业邮箱）。触发场景：用户说"查邮件"、"发邮件"、"回复邮件"、"转发邮件"、
  "邮件列表"、"未读邮件"、"搜索邮件"、"邮箱统计"、"标记已读"等邮箱相关操作。
---

# Email Manager

腾讯企业邮箱 IMAP/SMTP 客户端，通过 Python 脚本管理邮件。

## 环境要求

- Python 3.8+（标准库即可，无需额外安装依赖）
- 所有命令前需设置编码：
```
$env:PYTHONIOENCODING='utf-8'
```

## 命令

### 查看邮件列表
```
python {baseDir}/scripts/email_client.py list [--folder INBOX] [--unread] [--limit 20] [--days 7]
```

### 读取邮件
```
python {baseDir}/scripts/email_client.py read --id <message_id>
```

### 发送邮件
```
python {baseDir}/scripts/email_client.py send --to "a@b.com,c@d.com" --subject "标题" --body "正文" [--cc "e@f.com"] [--html] [--attachment "path1,path2"]
```

### 回复邮件
```
python {baseDir}/scripts/email_client.py reply --id <message_id> --body "回复内容" [--all]
```

### 转发邮件
```
python {baseDir}/scripts/email_client.py forward --id <message_id> --to "a@b.com" [--body "转发说明"]
```

### 标记邮件
```
python {baseDir}/scripts/email_client.py mark --id <message_id> [--read] [--unread] [--star] [--unstar]
```

### 搜索邮件
```
python {baseDir}/scripts/email_client.py search [--query "关键词"] [--from "sender@example.com"] [--since "2026-03-01"] [--before "2026-03-13"] [--limit 20]
```

### 列出文件夹
```
python {baseDir}/scripts/email_client.py folders
```

### 邮箱统计
```
python {baseDir}/scripts/email_client.py stats
```

## 输出

所有命令输出 JSON 格式，可直接解析。

## 安装配置（首次使用必读）

安装后需要修改配置文件 `{baseDir}/config/email-config.json`，填入你自己的邮箱账号和密码：

```json
{
  "imap": {
    "host": "imap.exmail.qq.com",
    "port": 993,
    "ssl": true
  },
  "smtp": {
    "host": "smtp.exmail.qq.com",
    "port": 465,
    "ssl": true
  },
  "account": {
    "username": "你的邮箱地址",
    "password": "你的邮箱密码或应用专用密码"
  }
}
```

- `host`/`port`：根据你的邮箱服务商修改（默认为腾讯企业邮箱）
- `username`：你的邮箱地址
- `password`：邮箱密码或应用专用密码（推荐使用应用专用密码）

常见邮箱服务商配置：
| 服务商 | IMAP Host | SMTP Host | IMAP Port | SMTP Port |
|--------|-----------|-----------|-----------|-----------|
| 腾讯企业邮箱 | imap.exmail.qq.com | smtp.exmail.qq.com | 993 | 465 |
| QQ 邮箱 | imap.qq.com | smtp.qq.com | 993 | 465 |
| 163 邮箱 | imap.163.com | smtp.163.com | 993 | 465 |
| Gmail | imap.gmail.com | smtp.gmail.com | 993 | 465 |
