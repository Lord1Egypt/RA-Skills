# 腾讯企业邮箱 Skill 故障排查

## 常见错误一览

### 1. 认证失败：535 Authentication failed

**症状**：登录时报错 `535 Login Fail`

**原因**：
- 密码填写错误
- 账号已绑定微信，使用了登录密码而非客户端专用密码
- 账号已开启「安全登录」要求授权码

**解决方案**：
1. 登录网页版 https://exmail.qq.com
2. 进入 设置 → 微信绑定（或安全设置）
3. 生成「客户端专用密码」
4. 将该密码设置为 `EXMAIL_PASSWORD`

---

### 2. 连接被拒绝 / 超时

**症状**：`Connection refused` 或 `Connection timed out`

**原因**：
- 网络环境屏蔽了 465/993 端口
- 企业防火墙限制

**解决方案**：
- 测试连通性：
  ```bash
  # 测试 SMTP 端口
  nc -zv smtp.exmail.qq.com 465

  # 测试 IMAP 端口
  nc -zv imap.exmail.qq.com 993
  ```
- 如果在海外或特殊网络环境，改用海外服务器：
  - `hwsmtp.exmail.qq.com:465`
  - `hwimap.exmail.qq.com:993`

---

### 3. 文件夹未找到

**症状**：`Mailbox not found` 或选择文件夹失败

**原因**：文件夹名称不匹配（可能有中文或特殊格式）

**解决方案**：
```bash
python3 scripts/read_email.py --action list-folders
```
查看实际文件夹名称后使用正确的 `--folder` 参数。

---

### 4. 搜索无结果

**症状**：搜索返回 0 结果，但确认邮件存在

**可能原因**：
- 搜索语法错误
- 邮件在其他文件夹
- 中文关键词编码问题

**解决方案**：
- 先用 `ALL` 确认连接正常
- 检查语法：关键词需用双引号包裹
- 尝试英文关键词或发件人地址搜索

---

### 5. 附件下载失败

**症状**：下载命令无输出或报错

**可能原因**：
- 邮件无附件
- 权限问题无法写入目标目录
- 附件 MIME 类型未被识别

**解决方案**：
- 先用 `--action read --uid <UID>` 确认邮件有附件
- 确认保存目录有写权限
- 尝试指定绝对路径 `--save-dir /tmp/email_attachments`

---

### 6. 中文乱码

**症状**：主题、发件人或正文显示乱码

**可能原因**：邮件头部编码（GBK/GB2312）

**解决方案**：
- 脚本已内置多编码自动检测，通常自动处理
- 如仍有问题，请提交 issue 并附上邮件头部信息

---

### 7. IMAP IDLE 实时通知不可用

**症状**：无法接收实时推送

**说明**：
标准 `imaplib` 不支持 IMAP IDLE。如需实时通知，可安装第三方库：

```bash
pip3 install imapclient
```

然后使用 `IMAPClient` 替代 `imaplib`，调用 `.idle()` 方法实现长连接监听。

---

## 调试模式

在脚本中启用详细日志（临时）：

```python
import imaplib
imaplib.Debug = 4  # 0=关闭, 1-9=详细程度
```

或在命令行：
```bash
PYTHONDEBUG=1 python3 scripts/read_email.py --action list
```

---

## 获取帮助

如遇到本文档未覆盖的问题：
1. 腾讯企业邮箱官方帮助：https://exmail.qq.com/help
2. 客服中心：http://service.exmail.qq.com
