# 腾讯企业邮箱服务器配置完整说明

## 标准服务器（国内用户）

| 协议 | 服务器地址 | SSL 端口 | 普通端口 |
|------|-----------|---------|---------|
| IMAP（收信）| `imap.exmail.qq.com` | **993** | 143 |
| SMTP（发信）| `smtp.exmail.qq.com` | **465** | 25 |
| POP3（收信）| `pop.exmail.qq.com` | **995** | 110 |

> ⚠️ 腾讯企业邮箱已强制要求使用 SSL 加密，**不再支持非 SSL 登录**。

---

## 海外用户服务器

| 协议 | 服务器地址 | SSL 端口 |
|------|-----------|---------|
| IMAP | `hwimap.exmail.qq.com` | 993 |
| SMTP | `hwsmtp.exmail.qq.com` | 465 |
| POP3 | `hwpop.exmail.qq.com` | 995 |

修改方式：在 `scripts/send_email.py` 和 `scripts/read_email.py` 中取消对应行的注释。

---

## 认证说明

### 普通账号（未绑定微信）
- 用户名：完整邮箱地址（如 `user@company.com`）
- 密码：邮箱登录密码

### 已绑定微信的账号
由于绑定微信后无法直接使用邮箱密码登录客户端，需要生成「**客户端专用密码**」：

1. 登录 https://exmail.qq.com
2. 设置 → 微信绑定
3. 点击「生成新密码」
4. 将生成的授权码作为 `EXMAIL_PASSWORD` 使用

---

## IMAP 搜索语法参考

腾讯企业邮箱 IMAP 支持标准 RFC 3501 搜索语法：

### 基础条件
| 条件 | 说明 | 示例 |
|------|------|------|
| `ALL` | 所有邮件 | `ALL` |
| `UNSEEN` | 未读邮件 | `UNSEEN` |
| `SEEN` | 已读邮件 | `SEEN` |
| `FLAGGED` | 星标邮件 | `FLAGGED` |
| `FROM "x"` | 按发件人 | `FROM "boss@company.com"` |
| `TO "x"` | 按收件人 | `TO "me@company.com"` |
| `SUBJECT "x"` | 按主题关键词 | `SUBJECT "合同"` |
| `BODY "x"` | 按正文关键词 | `BODY "项目进展"` |
| `SINCE d-Mon-yyyy` | 某日期之后 | `SINCE 01-Mar-2025` |
| `BEFORE d-Mon-yyyy` | 某日期之前 | `BEFORE 31-Mar-2025` |
| `ON d-Mon-yyyy` | 某一天 | `ON 15-Mar-2025` |
| `LARGER n` | 大于 n 字节 | `LARGER 1000000` |
| `SMALLER n` | 小于 n 字节 | `SMALLER 50000` |

### 组合条件（AND 逻辑）
```
FROM "boss@company.com" UNSEEN
SUBJECT "合同" SINCE 01-Jan-2025
FROM "finance" SUBJECT "报销" UNSEEN
```

---

## IMAP 文件夹名称

| 中文名 | IMAP 文件夹名 |
|--------|-------------|
| 收件箱 | `INBOX` |
| 已发送 | `Sent Messages` |
| 草稿箱 | `Drafts` |
| 已删除 | `Deleted Messages` |
| 垃圾邮件 | `Junk` |
| 星标邮件 | `Starred` |

> 使用 `--action list-folders` 查看实际文件夹列表。

---

## 附件大小限制

- 单封邮件：最大 **50MB**
- 单个附件：最大 **50MB**
- 超过限制建议使用企业微信文件传输或云盘分享链接
