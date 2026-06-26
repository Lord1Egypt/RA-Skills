# szzg007-product-promotion - 使用示例

## 🚀 场景 1: 基础使用 - 提取图片并生成邮件

**用户输入:**
```
提取这个商品的图片并生成推广邮件：
https://www.themossriver.com/products/clear-pc-storage-box
```

**AI 执行流程:**
1. ✅ 访问商品网址
2. ✅ 提取商品图片 (5 张)
3. ✅ 提取商品信息 (名称、价格、特点)
4. ✅ 生成 HTML 邮件模版
5. ✅ 保存到素材库

**AI 回复:**
```
✅ 已完成商品推广邮件生成

📊 执行总结:
1. ✅ 提取商品图片 (5 张)
2. ✅ 生成 HTML 邮件模版
3. ✅ 保存到素材库

📁 生成的文件:
- /product-promotion-assets/images/clear-pc-storage-box/ (5 张图片)
- /product-promotion-assets/emails/clear-pc-storage-box.html

需要发送到指定邮箱吗？
```

---

## 🚀 场景 2: 完整流程 - 生成并发送

**用户输入:**
```
处理这个商品，生成邮件并发送到 test@example.com
https://shop.example.com/product/premium-organizer
```

**AI 执行流程:**
1. ✅ 提取商品图片
2. ✅ 生成邮件模版
3. ✅ 保存到素材库
4. ✅ 发送邮件到 test@example.com

**AI 回复:**
```
✅ 商品推广邮件已发送

📬 发送详情:
- 收件人：test@example.com
- 主题：✨ Premium Organizer | Limited Offer
- 发送时间：2026-03-17 19:00

📁 已保存到素材库:
- 图片：/product-promotion-assets/images/premium-organizer/
- 邮件：/product-promotion-assets/emails/premium-organizer.html
```

---

## 🚀 场景 3: 批量处理 (未来功能)

**用户输入:**
```
批量处理这 5 个商品，生成推广邮件
- https://shop.com/product/1
- https://shop.com/product/2
- https://shop.com/product/3
- https://shop.com/product/4
- https://shop.com/product/5
```

**AI 回复:**
```
✅ 批量处理完成 (5/5)

📊 处理结果:
| 商品 | 图片 | 邮件 | 状态 |
|------|------|------|------|
| Product 1 | 5 张 | ✅ | 完成 |
| Product 2 | 4 张 | ✅ | 完成 |
| Product 3 | 6 张 | ✅ | 完成 |
| Product 4 | 5 张 | ✅ | 完成 |
| Product 5 | 3 张 | ✅ | 完成 |

📁 素材库位置:
/product-promotion-assets/batch_20260317/

需要全部发送还是选择部分发送？
```

---

## 🚀 场景 4: 自定义模版

**用户输入:**
```
用蓝色主题模版生成这个商品的推广邮件
https://shop.com/product/blue-widget
```

**AI 回复:**
```
✅ 已使用蓝色主题模版生成推广邮件

🎨 模版选择：蓝色主题 (v2)
📁 生成文件：
- /product-promotion-assets/emails/blue-widget-blue.html

预览效果：[链接]

需要发送到指定邮箱吗？
```

---

## 🚀 场景 5: 查看素材库

**用户输入:**
```
查看我的推广素材库
```

**AI 回复:**
```
📁 推广素材库内容

**总计:** 12 个商品 | 58 张图片 | 12 封邮件

**最近生成:**
1. clear-pc-storage-box (2026-03-17 18:45)
   - 图片：5 张
   - 邮件：✅

2. premium-organizer (2026-03-17 17:30)
   - 图片：4 张
   - 邮件：✅

3. ...

需要预览某个商品的邮件吗？
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **清晰的商品网址** - 确保网址可公开访问
2. **检查提取结果** - 确认图片和价格正确
3. **测试发送** - 先发送到自己邮箱预览
4. **归档管理** - 定期整理素材库

### ⚠️ 注意事项

1. **网站兼容性** - 不同电商网站可能需要适配
2. **图片版权** - 确保有权限使用商品图片
3. **邮件合规** - 遵守目标地区的邮件营销法规
4. **发送频率** - 注意 SMTP 服务器的发送限制

---

## 📞 常见问题

### Q: 支持哪些电商网站？
A: 目前支持 Shopify、WooCommerce 等主流平台，其他平台可能需要适配。

### Q: 可以自定义邮件模版吗？
A: 可以！在 `templates/` 目录下添加新的 HTML 模版。

### Q: 如何修改 SMTP 配置？
A: 编辑 `/Users/zhuzhenguo/.openclaw/workspace-judy/email-config.env`

### Q: 支持批量处理吗？
A: 计划中功能，敬请期待。

---

**技能版本:** 1.0.0  
**最后更新:** 2026-03-17
