---
name: qqemail-agent
description: QQ邮箱接收与发送skill - 读取QQ邮箱中的邮件和发送邮件到其他账号
version: 1.1.0
---

# QQ邮箱邮件助手

读取QQ邮箱中的邮件和发送邮件到其他账号

## 功能
- 📬 通过 IMAP 读取 QQ 邮箱收件箱
- 📝 解析邮件内容
- 📧 通过 SMTP 发送汇总邮件

---

## 对话式配置（推荐）

用户首次使用时，直接告诉 agent **"我想配置 QQ 邮箱"**，agent 会引导你：

1. **获取授权码** → agent 给你详细步骤
2. **提供信息** → 你告诉 agent 邮箱和授权码
3. **自动配置** → agent 把配置写入 `.env`

### 配置引导话术（供 Agent 参考）

用户说"配置QQ邮箱"或类似需求时，Agent 应该：

```
你好！让我来帮你配置 QQ 邮箱。

我需要以下信息：
1. 你的 QQ 邮箱号（例如：123456789）
2. 你的授权码（不是QQ密码！）

获取授权码步骤：
1. 打开 https://mail.qq.com
2. 登录 → 设置 → 账户
3. 找到 "IMAP/SMTP 服务"，开启
4. 点击"生成授权码"，按提示完成验证
5. **授权码只显示一次，请保存！**

获取后告诉我邮箱和授权码，我帮你写入配置文件。
```

收到用户回复后，Agent 执行：

```python
import os

env_content = """# IMAP配置（接收邮件）
IMAP_HOST=imap.qq.com
IMAP_PORT=993
IMAP_USER={邮箱}
IMAP_PASS={授权码}

# SMTP配置（发送邮件）
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_USER={邮箱}
SMTP_PASS={授权码}
"""

# 写入 .env 文件
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ 配置完成！")
```

---

## 手动配置（备用）

### 安装依赖
```bash
pip install imap-tools python-dotenv
```

### 获取授权码
**重要：必须使用授权码，不是QQ密码！**

1. 打开 [QQ邮箱](https://mail.qq.com)
2. 登录 → 设置 → 账户
3. 开启 **IMAP/SMTP 服务**
4. 点击 **生成授权码**（需要手机验证）
5. **授权码只显示一次，请保存！**

### 填写配置
新建 `.env` 文件，填入以下内容：

```bash
# IMAP配置（接收邮件）
IMAP_HOST=imap.qq.com
IMAP_PORT=993
IMAP_USER=你的QQ号@qq.com
IMAP_PASS=你的授权码

# SMTP配置（发送邮件）
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_USER=你的QQ号@qq.com
SMTP_PASS=你的授权码
```

---

## 使用方法

### 读取订单邮件
```bash
python scripts/fetch_orders.py
```

### 发送邮件
```bash
python scripts/send_email.py --to "客户邮箱" --subject "主题" --body "内容"
```

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `.env` | 配置文件，填入邮箱和授权码（需手动创建） |
| `scripts/fetch_orders.py` | 读取邮件脚本 |
| `scripts/send_email.py` | 发送邮件脚本 |

---

## 技术依赖
- Python 3.7+
- imap-tools
- python-dotenv
