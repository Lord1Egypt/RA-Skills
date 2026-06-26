---
name: qr-generator
description: 二维码生成器 - 自定义样式、批量生成、动态二维码
---

# QR Generator

二维码生成工具，支持自定义样式和批量生成。

## 功能

- ✅ 二维码生成
- ✅ 自定义样式 (颜色/Logo)
- ✅ 批量生成
- ✅ 动态二维码
- ✅ 二维码解码

## 使用

```bash
# 生成二维码
clawhub qr generate --content "https://example.com" --output qr.png

# 自定义样式
clawhub qr generate --content "url" --color "#FF0000" --logo logo.png

# 批量生成
clawhub qr batch --input urls.txt --output ./qrs
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 10 个/月 (基础样式) |
| Pro 版 | ¥39 | 无限 + 自定义 |
| 订阅版 | ¥9/月 | Pro+ 动态二维码 |
