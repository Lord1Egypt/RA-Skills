---
name: secure-storage
description: AES 加密存储，用于安全保存 API 密钥等敏感信息
version: 1.0.1
---

# Secure Storage — 加密存储

**版本**: 1.0.1  
**创建日期**: 2026-04-13  
**更新日期**: 2026-04-14

---

## 📋 功能

使用 AES 加密算法安全存储敏感信息：

| 功能 | 说明 |
|------|------|
| set | 加密存储键值对 |
| get | 解密读取值 |
| list | 列出所有已存储键名 |
| delete | 删除指定键 |

---

## 📂 文件结构

```
skills/secure-storage/
├── SKILL.md
├── skill.json
└── scripts/
    └── secure-storage.js    # 加密存储主程序
```

---

## 🔧 用法

```bash
# 存储
node skills/secure-storage/scripts/secure-storage.js set <key> <value>

# 读取
node skills/secure-storage/scripts/secure-storage.js get <key>

# 列表
node skills/secure-storage/scripts/secure-storage.js list

# 删除
node skills/secure-storage/scripts/secure-storage.js delete <key>
```

---

## 📊 触发方式

- **手动触发**（按需使用的安全工具，无需自动化）

---

## ⚠️ 注意事项

- 加密密钥从环境变量读取
- 存储文件：`.secure-storage.json`
- 不要提交加密文件到版本控制
