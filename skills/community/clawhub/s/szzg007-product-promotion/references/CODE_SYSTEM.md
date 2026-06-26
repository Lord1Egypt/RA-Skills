# 邮件素材代号系统

## 📋 概述

每个邮件推广素材都有唯一的代号，用于快速识别、分类和管理。

## 🏷️ 代号规则

**格式:** `Q` + `系列字母` + `序号`

```
Q B 1
│ │ │
│ │ └─ 序号 (1, 2, 3...)
│ └─── 系列字母 (Y/B/A/H/F)
└───── 前缀 (Q = Promotion)
```

## 📊 代号分类

| 代号前缀 | 系列 | 英文 | 用途 |
|---------|------|------|------|
| **QY** | 童装 | Childrenswear | 童装产品推广 |
| **QB** | 收纳 | Box/Storage | 收纳产品推广 |
| **QA** | 通用 | General | 通用产品推广 |
| **QH** | 家居 | Home | 家居产品推广 |
| **QF** | 时尚 | Fashion | 时尚产品推广 |

## 📁 现有代号

### QB 系列 - 收纳产品

| 代号 | 名称 | 创建日期 | 产品 | 发送次数 |
|------|------|----------|------|----------|
| **QB1** | Clear Storage Box - Purple Gradient | 2026-03-17 | 透明收纳盒 | 1 |

### QY 系列 - 童装产品

| 代号 | 名称 | 创建日期 | 产品 | 发送次数 |
|------|------|----------|------|----------|
| *待创建* | - | - | - | - |

### QA 系列 - 通用产品

| 代号 | 名称 | 创建日期 | 产品 | 发送次数 |
|------|------|----------|------|----------|
| *待创建* | - | - | - | - |

### QH 系列 - 家居产品

| 代号 | 名称 | 创建日期 | 产品 | 发送次数 |
|------|------|----------|------|----------|
| *待创建* | - | - | - | - |

### QF 系列 - 时尚产品

| 代号 | 名称 | 创建日期 | 产品 | 发送次数 |
|------|------|----------|------|----------|
| *待创建* | - | - | - | - |

## 🔧 管理命令

### 列出所有代号

```bash
python3 scripts/email-code-manager.py list
```

**输出示例:**
```
============================================================
📧 邮件素材代号列表
============================================================

总计：3 个素材

QB:
----------------------------------------
  QB1    | Clear Storage Box - Purple Gradient
         | 创建：2026-03-17

QY:
----------------------------------------
  QY1    | Kids Summer Dress
         | 创建：2026-03-18
  QY2    | Children's Casual Wear
         | 创建：2026-03-19

============================================================
```

### 生成新代号

```bash
# 生成收纳系列新代号
python3 scripts/email-code-manager.py generate b

# 生成童装系列新代号
python3 scripts/email-code-manager.py generate y

# 生成通用系列新代号
python3 scripts/email-code-manager.py generate a
```

**输出示例:**
```
============================================================
✅ 新代号生成
============================================================

类型：收纳 (Box/Storage)
新代号：QB2

使用方式:
  python3 product-promotion.py <url> --code QB2
============================================================
```

### 查看代号详情

```bash
python3 scripts/email-code-manager.py info QB1
```

**输出示例:**
```
============================================================
📧 代号详情：QB1
============================================================

名称：Clear Storage Box - Purple Gradient
描述：透明收纳盒产品推广邮件 - 紫色渐变主题
版本：1.0.0
创建：2026-03-17T19:00:00+08:00
分类：product-promotion

产品信息:
  名称：Clear PC Storage Box with Removable Colorful Trays
  价格：$45.99

设计信息:
  主题：Purple Gradient
  风格：Modern Minimalist

使用统计:
  发送次数：1
  最后发送：2026-03-17T19:00:00+08:00

标签：storage, organizer, home, purple, gradient

============================================================
```

## 💡 使用示例

### 示例 1: 生成收纳产品邮件

```bash
python3 scripts/product-promotion.py \
  "https://www.themossriver.com/products/storage-box" \
  --code QB2
```

### 示例 2: 生成童装产品邮件

```bash
python3 scripts/product-promotion.py \
  "https://shop.example.com/kids-summer-dress" \
  --code QY1
```

### 示例 3: 查看素材库

```bash
# 列出所有代号
python3 scripts/email-code-manager.py list

# 查看特定代号详情
python3 scripts/email-code-manager.py info QB1
```

## 📝 元数据文件

每个代号对应一个元数据文件：

**位置:** `/Users/zhuzhenguo/.openclaw/workspace/product-promotion-assets/emails/{CODE}.meta.json`

**内容:**
```json
{
  "schema": "szzg007-email-template-meta-v1",
  "code": "QB1",
  "name": "Clear Storage Box - Purple Gradient",
  "description": "透明收纳盒产品推广邮件 - 紫色渐变主题",
  "version": "1.0.0",
  "created": "2026-03-17T19:00:00+08:00",
  "category": "product-promotion",
  "product": {...},
  "design": {...},
  "usage": {...},
  "tags": [...]
}
```

## 🎯 最佳实践

### ✅ 推荐做法

1. **按产品系列使用对应代号**
   - 童装 → QY 系列
   - 收纳 → QB 系列
   - 其他 → QA 系列

2. **及时更新元数据**
   - 每次发送后更新使用统计
   - 记录重要修改版本

3. **定期整理**
   - 查看长期未使用的代号
   - 归档过时的模版

### ⚠️ 注意事项

1. **代号唯一性** - 每个代号只能对应一个邮件模版
2. **命名一致性** - 保持代号与产品系列对应
3. **版本管理** - 重大修改时升级版本号

---

**版本:** 1.0.0  
**最后更新:** 2026-03-17
