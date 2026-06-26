---
name: password-manager
description: 密码管理器 - 安全存储、随机生成、自动填充
---

# Password Manager

密码管理工具，安全存储和生成密码。

## 功能

- ✅ 密码加密存储
- ✅ 随机密码生成
- ✅ 密码强度检测
- ✅ 自动填充
- ✅ 密码泄露检测

## 使用

```bash
# 生成密码
clawhub pass generate --length 16 --symbols

# 存储密码
clawhub pass add --site github.com --username user

# 获取密码
clawhub pass get --site github.com

# 检测强度
clawhub pass check --password "mypassword"
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 10 个密码 |
| Pro 版 | ¥49 | 无限密码 |
| 订阅版 | ¥12/月 | Pro+ 云同步 |
