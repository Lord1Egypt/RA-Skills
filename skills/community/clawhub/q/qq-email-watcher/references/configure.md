# QQ邮箱监控配置指南

## 获取 IMAP 授权码

1. 登录 QQ 邮箱网页版
2. 进入「设置」→「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
4. 开启「IMAP_SSL」服务
5. 点击「生成授权码」，会收到短信验证
6. 复制授权码（格式如 `xtepatkcgckvhjhf`）

## 配置脚本

编辑 `scripts/email_watcher.py` 顶部的配置区：

```python
EMAIL = "你的QQ邮箱@qq.com"
AUTH_CODE = "你的IMAP授权码"
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993

WHITELIST_FILE = "路径/to/whitelist.json"
PROCESSED_FILE = "路径/to/processed_emails.json"
QQ_TARGET = "你的QQ OpenID"
```

## 创建白名单文件

创建 `whitelist.json`，添加需要监控的邮箱地址：

```json
["734743044@qq.com", "3678898561@qq.com"]
```

## 启动监听

```bash
python3 ~/.openclaw/workspace/skills/qq-email-watcher/scripts/email_watcher.py &
```

## 测试通知

发送测试邮件到白名单地址，检查是否收到 QQ 消息。

## 停止服务

```bash
pkill -f email_watcher.py
```
