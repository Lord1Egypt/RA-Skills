# 邮件发送工具配置说明

本文档详细说明如何配置邮件发送工具。

## 配置文件位置（重要！）

### ⚠️ 为什么不能放在工作目录？

**问题**：
- `config.json` 是一个非常通用的文件名
- 容易与其他项目的配置文件冲突
- 工作目录经常变化，配置文件可能丢失
- 多个项目可能互相覆盖

**解决方案**：使用专门的配置目录

---

## 🎯 推荐配置位置

### 1️⃣ **用户主目录**（强烈推荐）

**路径**：`~/.openclaw/mail-sender/config.json`

**完整路径**：
- **Linux/macOS**：`/home/yourusername/.openclaw/mail-sender/config.json`
- **Windows**：`C:\Users\yourusername\.openclaw\mail-sender\config.json`

**为什么推荐？**
- ✅ 不会与工作目录的其他配置文件冲突
- ✅ 集中管理 OpenClaw 相关配置
- ✅ 全局可用，不受工作目录影响
- ✅ 更安全，不容易被误删
- ✅ 不会被 Git 提交

**创建配置目录和文件**：

**Linux/macOS**：
```bash
# 创建配置目录
mkdir -p ~/.openclaw/mail-sender

# 创建配置文件
nano ~/.openclaw/mail-sender/config.json

# 或使用任何编辑器
code ~/.openclaw/mail-sender/config.json
```

**Windows (PowerShell)**：
```powershell
# 创建配置目录
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw\mail-sender"

# 创建配置文件
notepad "$env:USERPROFILE\.openclaw\mail-sender\config.json"

# 或使用 VS Code
code "$env:USERPROFILE\.openclaw\mail-sender\config.json"
```

**Windows (CMD)**：
```cmd
# 创建配置目录
mkdir "%USERPROFILE%\.openclaw\mail-sender"

# 创建配置文件
notepad "%USERPROFILE%\.openclaw\mail-sender\config.json"
```

---

### 2️⃣ **Skill 脚本目录**

**路径**：`{skill_dir}/config.json`

**完整路径**：
- `C:\Users\yourusername\.openclaw\skills\mail-sender\scripts\config.json`

**优点**：
- ✅ 与 skill 代码在一起，便于管理
- ✅ skill 更新时可以保留配置

**缺点**：
- ⚠️ skill 更新可能覆盖配置文件
- ⚠️ 不同用户共享 skill 时可能冲突

---

### 3️⃣ **当前工作目录**

**路径**：`./.mail-sender-config.json`

**注意**：使用明确的文件名 `.mail-sender-config.json`，避免与 `config.json` 冲突

**优点**：
- ✅ 项目特定的配置
- ✅ 可以随项目一起管理

**缺点**：
- ⚠️ 需要在每个项目中创建
- ⚠️ 可能被 Git 提交（需要添加到 .gitignore）

---

## 📋 配置文件查找优先级

`mail-sender` skill 按以下顺序查找配置文件：

| 优先级 | 路径 | 说明 | 推荐度 |
|--------|------|------|--------|
| 1 | 环境变量 `MAIL_CONFIG_PATH` | 用户自定义路径 | ⭐⭐⭐⭐⭐ |
| 2 | `~/.openclaw/mail-sender/config.json` | 用户主目录 | ⭐⭐⭐⭐⭐ |
| 3 | `{skill_dir}/config.json` | Skill 脚本目录 | ⭐⭐⭐ |
| 4 | `./.mail-sender-config.json` | 当前工作目录 | ⭐⭐ |
| 5 | `./config.json` | 向后兼容（会警告） | ⭐ |

**查找流程**：
1. 首先检查环境变量 `MAIL_CONFIG_PATH`
2. 然后检查 `~/.openclaw/mail-sender/config.json`
3. 接着检查 skill 脚本目录
4. 最后检查当前工作目录
5. 找到第一个存在的配置文件后停止查找

---

## 🔧 配置方式

### 方式 1：配置文件（推荐）

**配置文件内容**：
```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code_here",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_receivers": [
    "user1@example.com",
    "user2@example.com"
  ]
}
```

**使用示例**：
```python
from mail_sender import send_mail

# 自动从配置文件加载（推荐位置）
send_mail(
    subject='测试邮件',
    content='<p>内容</p>'
    # 不指定 receivers，使用配置文件中的 default_receivers
)
```

---

### 方式 2：环境变量

#### 基本环境变量

**Linux/macOS**：
```bash
export MAIL_SENDER_EMAIL="your_email@163.com"
export MAIL_SENDER_PASSWORD="your_auth_code"
export MAIL_SMTP_SERVER="smtp.163.com"
export MAIL_SMTP_PORT="465"
export MAIL_DEFAULT_RECEIVERS="user1@example.com,user2@example.com"
```

**Windows (PowerShell)**：
```powershell
$env:MAIL_SENDER_EMAIL="your_email@163.com"
$env:MAIL_SENDER_PASSWORD="your_auth_code"
$env:MAIL_SMTP_SERVER="smtp.163.com"
$env:MAIL_SMTP_PORT="465"
$env:MAIL_DEFAULT_RECEIVERS="user1@example.com,user2@example.com"
```

#### 指定配置文件路径

**Linux/macOS**：
```bash
export MAIL_CONFIG_PATH="/path/to/your/config.json"
```

**Windows (PowerShell)**：
```powershell
$env:MAIL_CONFIG_PATH="C:\path\to\your\config.json"
```

**使用示例**：
```python
from mail_sender import send_mail

# 自动从环境变量加载
send_mail(subject='测试', content='内容')
```

---

### 方式 3：代码传参（不推荐）

**仅用于测试或特殊情况**：
```python
from mail_sender import MailConfig, MailSender

config = MailConfig(
    sender_email="your_email@163.com",
    sender_password="your_auth_code",
    smtp_server="smtp.163.com",
    smtp_port=465,
    default_receivers=["user@example.com"]
)

sender = MailSender(config)
sender.send_mail(subject='测试', content='内容')
```

---

## 📁 配置文件示例

### 完整配置示例

**位置**：`~/.openclaw/mail-sender/config.json`

```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code_here",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_receivers": [
    "user1@qq.com",
    "user2@gmail.com"
  ]
}
```

### 最小配置示例

```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code_here"
}
```

**注意**：其他参数会使用默认值

---

## 🌍 环境变量示例（.env 文件）

**位置**：`~/.openclaw/mail-sender/.env`

```env
# 邮件配置
MAIL_SENDER_EMAIL=your_email@163.com
MAIL_SENDER_PASSWORD=your_auth_code_here
MAIL_SMTP_SERVER=smtp.163.com
MAIL_SMTP_PORT=465
MAIL_DEFAULT_RECEIVERS=user1@example.com,user2@example.com

# 配置文件路径（可选）
MAIL_CONFIG_PATH=/path/to/your/config.json
```

**使用**：
```bash
# 加载环境变量
source ~/.openclaw/mail-sender/.env

# 或使用 python-dotenv
python-dotenv
```

---

## 🔒 安全最佳实践

### ✅ 推荐做法

1. **使用用户主目录配置**
   ```bash
   ~/.openclaw/mail-sender/config.json
   ```

2. **使用授权码，不是登录密码**
   - 163 邮箱：设置 → POP3/SMTP/IMAP → 获取授权码
   - QQ 邮箱：设置 → 账户 → 开启 SMTP → 获取授权码

3. **设置文件权限**（Linux/macOS）
   ```bash
   chmod 600 ~/.openclaw/mail-sender/config.json
   ```

4. **添加到 .gitignore**
   ```
   # 邮件配置文件
   .mail-sender-config.json
   config.json
   .env
   ```

### ❌ 不要做

1. **不要提交到 Git**
   - 配置文件包含敏感信息

2. **不要使用登录密码**
   - 使用邮箱授权码

3. **不要在工作目录使用 config.json**
   - 容易冲突，使用 `.mail-sender-config.json`

4. **不要硬编码密码**
   - 避免在代码中直接写密码

---

## 🧪 测试配置

### 测试配置文件是否正确

```python
from mail_sender import MailConfig, MailSender

try:
    config = MailConfig()
    print(f"✅ 配置加载成功！")
    print(f"发件人: {config.sender_email}")
    print(f"SMTP: {config.smtp_server}:{config.smtp_port}")
    print(f"默认收件人: {config.default_receivers}")
    
    # 测试发送
    sender = MailSender(config)
    result = sender.send_mail(
        subject='配置测试',
        content='<p>这是一封测试邮件</p>'
    )
    
    if result['success']:
        print("✅ 邮件发送成功！")
    else:
        print(f"❌ 邮件发送失败: {result['message']}")
        
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
```

---

## 📞 故障排查

### 问题 1：找不到配置文件

**症状**：
```
ValueError: 缺少必需的邮件配置！
```

**解决**：
1. 检查配置文件是否在正确位置
2. 检查文件名是否正确
3. 检查文件权限

### 问题 2：配置文件冲突

**症状**：
```
加载了错误的配置文件
```

**解决**：
1. 使用 `~/.openclaw/mail-sender/config.json`
2. 或使用环境变量 `MAIL_CONFIG_PATH` 指定路径
3. 删除工作目录中的 `config.json`

### 问题 3：登录失败

**症状**：
```
SMTPSenderRefused: 发件人被拒绝
```

**解决**：
1. 检查是否使用授权码（不是登录密码）
2. 检查 SMTP 服务是否开启
3. 检查邮箱地址是否正确

## 常用邮箱 SMTP 配置

### 163 邮箱

```json
{
  "smtp_server": "smtp.163.com",
  "smtp_port": 465
}
```

**获取授权码**：
1. 登录 163 邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启服务
4. 获取授权码（不是登录密码）

### QQ 邮箱

```json
{
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465
}
```

**获取授权码**：
1. 登录 QQ 邮箱
2. 设置 → 账户
3. 开启 SMTP 服务
4. 获取授权码

### Gmail

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

**注意**：Gmail 需要开启"应用专用密码"

### Outlook/Hotmail

```json
{
  "smtp_server": "smtp-mail.outlook.com",
  "smtp_port": 587
}
```

## 配置参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sender_email` | string | ✅ | - | 发件人邮箱地址 |
| `sender_password` | string | ✅ | - | 邮箱密码或授权码 |
| `smtp_server` | string | ❌ | smtp.163.com | SMTP 服务器地址 |
| `smtp_port` | int | ❌ | 465 | SMTP 端口（SSL 通常为 465） |
| `default_receivers` | list | ❌ | [] | 默认收件人列表 |
| `sender_name` | string | ❌ | Wezn AI System | 发件人显示名称 |

## 安全建议

1. ✅ **使用环境变量**：最安全，避免敏感信息泄露
2. ✅ **使用授权码**：不要使用邮箱登录密码
3. ✅ **加密配置文件**：如果使用配置文件，考虑加密
4. ❌ **不要硬编码**：避免在代码中直接写密码
5. ❌ **不要提交到 Git**：配置文件不要提交到版本控制

## 故障排查

### 1. 登录失败

**原因**：
- 密码错误（需要授权码，不是登录密码）
- SMTP 服务未开启

**解决**：
- 检查是否使用授权码
- 检查邮箱 SMTP 服务是否开启

### 2. 连接超时

**原因**：
- SMTP 服务器地址错误
- 端口被防火墙拦截

**解决**：
- 检查 SMTP 服务器地址
- 尝试切换端口（465/587）
- 检查防火墙设置

### 3. 邮件被拒收

**原因**：
- 收件人地址错误
- 被标记为垃圾邮件

**解决**：
- 检查收件人地址格式
- 添加邮件头信息（已自动添加）
- 避免发送垃圾邮件内容

## 示例配置

### 完整配置示例

```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code_here",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_receivers": [
    "user1@qq.com",
    "user2@gmail.com"
  ]
}
```

### 环境变量示例（.env 文件）

```env
MAIL_SENDER_EMAIL=your_email@163.com
MAIL_SENDER_PASSWORD=your_auth_code_here
MAIL_SMTP_SERVER=smtp.163.com
MAIL_SMTP_PORT=465
MAIL_DEFAULT_RECEIVERS=user1@qq.com,user2@gmail.com
```

## Python 代码示例

### 基础使用

```python
from mail_sender import send_mail, send_markdown

# 发送 HTML 邮件
result = send_mail(
    subject='测试邮件',
    content='<h1>Hello</h1><p>这是一封测试邮件</p>',
    receivers='user@example.com'
)

# 发送 Markdown 邮件
result = send_markdown(
    subject='测试邮件',
    content='# Hello\n\n这是一封 **Markdown** 邮件',
    receivers='user@example.com'
)
```

### 多收件人

```python
# 字符串形式（逗号分隔）
send_mail(
    subject='测试邮件',
    content='内容',
    receivers='user1@example.com,user2@example.com'
)

# 列表形式
send_mail(
    subject='测试邮件',
    content='内容',
    receivers=['user1@example.com', 'user2@example.com']
)
```

### 使用默认收件人

```python
# 不指定 receivers，使用配置的默认收件人
send_mail(
    subject='测试邮件',
    content='内容'
)
```

### 自定义配置

```python
from mail_sender import MailConfig, MailSender

config = MailConfig(
    sender_email="your_email@163.com",
    sender_password="your_auth_code",
    sender_name="我的应用"
)

sender = MailSender(config)
result = sender.send_mail(
    subject='测试邮件',
    content='内容',
    receivers='user@example.com'
)
```
