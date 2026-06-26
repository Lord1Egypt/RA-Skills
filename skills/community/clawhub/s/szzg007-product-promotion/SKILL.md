# szzg007-product-promotion - 商品推广邮件生成技能

**版本:** 1.0.0  
**作者:** szzg007  
**创建日期:** 2026-03-17  
**最后更新:** 2026-03-17

---

## 📋 技能描述

从商品网址自动提取图片，生成高品质邮件推广模版，并保存到素材库的完整自动化技能。

**核心能力:**
1. 🖼️ **图片提取** - 从电商网站自动提取商品图片
2. 🎨 **模版设计** - 生成有品质的 HTML 邮件推广模版
3. 📁 **素材管理** - 自动归档到推广素材库
4. 📧 **邮件发送** - 支持直接发送或保存待发送

---

## 🚀 使用方式

### 基础用法

```
"提取这个商品的图片并生成推广邮件：https://www.example.com/product/xxx"
```

### 指定代号

```
"用代号 QB2 生成这个商品的推广邮件：https://xxx.com/product/123"
```

### 带参数用法

```
"提取 https://xxx.com/product/123，生成邮件模版，保存到素材库"
```

```
"用 szzg007-product-promotion 技能处理这个商品网址：https://xxx.com/product/456"
```

### 发送邮件

```
"把刚才生成的推广邮件发送到 xxx@email.com"
```

## 🏷️ 代号系统

每个邮件素材都有唯一代号，方便管理和复用：

| 代号 | 系列 | 说明 | 示例 |
|------|------|------|------|
| QY1, QY2... | 童装 (Childrenswear) | 童装产品推广 | QY1 - 童装第 1 号 |
| QB1, QB2... | 收纳 (Box/Storage) | 收纳产品推广 | QB1 - 收纳第 1 号 |
| QA1, QA2... | 通用 (General) | 通用产品推广 | QA1 - 通用第 1 号 |
| QH1, QH2... | 家居 (Home) | 家居产品推广 | QH1 - 家居第 1 号 |
| QF1, QF2... | 时尚 (Fashion) | 时尚产品推广 | QF1 - 时尚第 1 号 |

**代号格式:** `Q` + `系列字母` + `序号`

---

## 📁 文件结构

```
/Users/zhuzhenguo/.openclaw/workspace/
├── skills/szzg007-product-promotion/
│   ├── SKILL.md              # 技能说明文档
│   ├── scripts/
│   │   ├── extract-images.py    # 图片提取脚本
│   │   ├── generate-template.py # 邮件模版生成脚本
│   │   └── send-email.py        # 邮件发送脚本
│   ├── templates/
│   │   ├── email-template-v1.html  # 邮件模版 v1
│   │   └── email-template-v2.html  # 邮件模版 v2 (可选)
│   ├── output/                # 临时输出目录
│   └── references/            # 参考资料
│
└── product-promotion-assets/   # 推广素材库
    ├── images/                # 提取的商品图片
    ├── emails/                # 生成的邮件模版
    └── reports/               # 生成报告
```

---

## 🔧 配置要求

### 邮件配置 (可选，如需发送邮件)

在 `/Users/zhuzhenguo/.openclaw/workspace-judy/email-config.env` 配置:

```bash
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=your_email@163.com
SMTP_PASS=your_password
SMTP_FROM_NAME=Your Name
```

### 环境变量 (可选)

```bash
export PRODUCT_PROMOTION_OUTPUT_DIR="/Users/zhuzhenguo/.openclaw/workspace/product-promotion-assets"
```

---

## 📊 输出格式

### 生成的文件

| 类型 | 位置 | 说明 |
|------|------|------|
| **商品图片** | `product-promotion-assets/images/{product-id}/` | 提取的所有商品图片 |
| **HTML 邮件** | `product-promotion-assets/emails/{product-id}.html` | 推广邮件模版 |
| **报告** | `product-promotion-assets/reports/{product-id}.md` | 生成报告 |

### 邮件模版特点

- 📱 移动端友好响应式设计
- 🎨 现代化渐变品牌色调
- 🖼️ 商品图片画廊展示
- 💰 价格/折扣醒目展示
- ✨ 产品特点图标化
- 🔗 清晰的 CTA 按钮

---

## 🧪 示例工作流

### 示例 1: 基础使用

```
用户：提取这个商品的图片并生成推广邮件
https://www.themossriver.com/products/clear-pc-storage-box

AI: ✅ 已完成商品推广邮件生成

📊 执行总结:
1. ✅ 提取商品图片 (5 张)
2. ✅ 生成 HTML 邮件模版
3. ✅ 保存到素材库

📁 生成的文件:
- /product-promotion-assets/images/clear-pc-storage-box/ (5 张图片)
- /product-promotion-assets/emails/clear-pc-storage-box.html

需要发送到指定邮箱吗？
```

### 示例 2: 完整流程

```
用户：处理这个商品，生成邮件并发送到 test@example.com
https://shop.example.com/product/premium-organizer

AI: ✅ 商品推广邮件已发送

📬 发送详情:
- 收件人：test@example.com
- 主题：✨ Premium Organizer | Limited Offer
- 发送时间：2026-03-17 19:00

📁 已保存到素材库:
- 图片：/product-promotion-assets/images/premium-organizer/
- 邮件：/product-promotion-assets/emails/premium-organizer.html
```

---

## 🛠️ 技术实现

### 图片提取

使用 `browser` 工具访问商品页面，通过 snapshot 获取图片链接，然后用 `curl` 下载。

### 邮件模版生成

基于预定义的 HTML 模版，动态替换:
- 商品名称
- 价格信息
- 图片 URL
- 产品特点
- 购买链接

### 邮件发送

使用 Python `smtplib` 通过配置的 SMTP 服务器发送邮件。

---

## ⚠️ 注意事项

1. **网站兼容性:** 不同电商网站结构不同，可能需要适配
2. **图片版权:** 确保有权限使用提取的商品图片
3. **邮件合规:** 遵守目标地区的邮件营销法规 (如 CAN-SPAM, GDPR)
4. **SMTP 限制:** 注意邮件服务商的发送频率限制

---

## 📝 更新日志

### v1.0.0 (2026-03-17)
- ✅ 初始版本发布
- ✅ 支持商品图片提取
- ✅ 支持 HTML 邮件模版生成
- ✅ 支持素材库自动归档
- ✅ 支持邮件发送

---

## 🎯 未来计划

- [ ] 支持多电商平台适配 (Shopify, WooCommerce, Amazon 等)
- [ ] 添加 A/B 测试模版
- [ ] 支持批量商品处理
- [ ] 集成邮件打开率追踪
- [ ] 添加 AI 文案优化

---

## 📞 支持

如有问题或建议，请联系技能作者 szzg007。
