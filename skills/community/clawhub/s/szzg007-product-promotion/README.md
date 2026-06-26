# szzg007-product-promotion

商品推广邮件自动生成技能 - 从网址到邮件，一键完成。

## 快速开始

```bash
# 基础用法
python3 scripts/product-promotion.py <product_url>

# 指定代号
python3 scripts/product-promotion.py <product_url> --code QB2

# 带邮件发送
python3 scripts/product-promotion.py <product_url> --send-to email@example.com

# 单独发送邮件
python3 scripts/send-email.py <email.html> <to_email>

# 管理代号
python3 scripts/email-code-manager.py list
python3 scripts/email-code-manager.py generate b
python3 scripts/email-code-manager.py info QB1
```

## 代号系统

每个邮件素材都有唯一代号，方便管理和复用：

| 代号 | 系列 | 说明 |
|------|------|------|
| QY1, QY2... | 童装 (Childrenswear) | 童装产品推广 |
| QB1, QB2... | 收纳 (Box/Storage) | 收纳产品推广 |
| QA1, QA2... | 通用 (General) | 通用产品推广 |
| QH1, QH2... | 家居 (Home) | 家居产品推广 |
| QF1, QF2... | 时尚 (Fashion) | 时尚产品推广 |

**示例:** QB1 = 收纳系列第 1 号

## 完整工作流

1. **提供商品网址** → AI 自动提取图片
2. **生成邮件模版** → 专业设计，移动端友好
3. **保存到素材库** → 自动归档，方便复用
4. **发送邮件** → 可选，直接发送到目标邮箱

## 输出结构

```
/Users/zhuzhenguo/.openclaw/workspace/product-promotion-assets/
├── images/{product-id}/     # 商品图片
├── emails/{product-id}.html # 邮件模版
└── reports/{product-id}.md  # 生成报告
```

## 配置

编辑 `/Users/zhuzhenguo/.openclaw/workspace-judy/email-config.env`:

```bash
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=your_email@163.com
SMTP_PASS=your_password
```

## 示例

```bash
# 处理商品网址
python3 scripts/product-promotion.py \
  "https://www.themossriver.com/products/clear-pc-storage-box"

# 发送邮件
python3 scripts/send-email.py \
  "/Users/zhuzhenguo/.openclaw/workspace/product-promotion-assets/emails/clear-pc-storage-box.html" \
  "customer@example.com" \
  --subject "✨ Premium Storage Box | 23% OFF"
```

## 技能命名规范

所有自有技能以 `szzg007_` 前缀命名:
- `szzg007-product-promotion` ✅
- `szzg007-lead-hunter` (计划中)
- `szzg007-email-marketing` (计划中)

---

**版本:** 1.0.0  
**作者:** szzg007  
**日期:** 2026-03-17
