---
name: contact-manager
description: 联系人管理 - 名片存储、分组管理、快速搜索
---

# Contact Manager

联系人管理工具，高效管理人脉资源。

## 功能

- ✅ 名片存储
- ✅ 分组管理
- ✅ 快速搜索
- ✅ 批量导入导出
- ✅ 生日提醒

## 使用

```bash
# 添加联系人
clawhub contact add --name "张三" --phone "13800138000" --email "zhang@example.com"

# 搜索联系人
clawhub contact search --query "张三"

# 分组管理
clawhub contact group --add "同事" --contacts 1,2,3

# 导出联系人
clawhub contact export --format csv --output contacts.csv
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 100 个联系人 |
| Pro 版 | ¥39 | 无限联系人 |
| 订阅版 | ¥9/月 | Pro+ 云同步 |
