# 发送邮件参考

## 概述

`qq_mail_sender` 模块提供了通过 QQ 邮箱 SMTP 服务发送邮件的功能。

## 构建消息

使用 `build_message` 函数可以创建一个带有适当编码的 `EmailMessage` 对象。

```python
msg = build_message(
    sender="your_email@qq.com",
    to="recipient@example.com",
    subject="测试主题",
    body="这是一封测试邮件"
)
```

## 发送邮件

使用 `send_email` 函数通过 QQ SMTP 发送邮件。

```python
send_email(
    to="recipient@example.com",
    subject="测试主题",
    body="这是一封测试邮件"
)
```

## 示例

### 简单文本邮件

```python
from qq_mail_sender import send_email

send_email(
    to="friend@example.com",
    subject="你好",
    body="这是一封来自 QQ 邮箱的测试邮件。"
)
```

### 带抄送和密送

```python
send_email(
    to="primary@example.com",
    cc="secondary@example.com",
    bcc="hidden@example.com",
    subject="会议通知",
    body="请于明天上午 10 点参加会议。"
)
```

### 通过命令行发送

```bash
python qq_mail_sender.py friend@example.com "测试主题" "这是一封测试邮件"
```

## 错误处理

如果凭据缺失或 SMTP 连接失败，将引发异常。建议在调用时使用 try-except 捕获异常。

```python
try:
    send_email(to, subject, body)
except Exception as e:
    print(f"发送邮件失败: {e}")
```