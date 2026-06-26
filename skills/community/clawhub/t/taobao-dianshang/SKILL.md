---
name: taobao-publish-shangpin
description: 淘宝/千牛商家商品自动发布技能。当用户说"发布商品"、"上架商品"、"商品上架"时使用。支持根据商品图片自动识别并填写商品信息。流程包括：打开千牛工作台→进入商品发布页面→上传商品图片→填写商品信息（标题、价格、库存、属性等）→发布商品。
---

# 淘宝商品发布技能 (taobao-publish-shangpin)

## 功能说明

自动化淘宝/千牛商家商品发布流程，减少手动填写工作。

## 工作流程

### 1. 打开发布页面
```
browser(action="open", url="https://myseller.taobao.com/home.htm/PublishProduct/index")
```

### 2. 点击"以图发品"（推荐）

在千牛工作台左侧点击"商品" → "发布商品"，然后选择"以图发品"标签。

**从图片空间上传图片：**
1. 点击"从图片空间上传"
2. 在弹出的图片选择器中勾选已上传的图片
3. 点击"确定"
4. 点击"确认，下一步"

### 3. 选择正确类目

如果AI识别的类目不正确：
1. 点击"切换类目"
2. 在类目选择器中找到"手办/手办景品"（潮玩模玩/动漫娱乐周边/三坑娃圈>>手办/兵人/扭蛋>>手办/手办景品）
3. 点击"确定"

### 4. 填写商品信息

**已验证可自动填写的字段：**
| 字段 | ref格式 | 操作方式 |
|------|---------|----------|
| 宝贝标题 | xxx_97 | type |
| 价格（一口价） | xxx_189 | type |
| 总库存 | xxx_194 | type |
| 角色名 | xxx_144 | type |
| 适用年龄 | xxx_154 | type（数字） |

**操作示例：**
```
browser(action="act", targetId="2", ref="14_97", kind="type", text="原创设计精灵少女手办 星空梦境治愈系桌面摆件 三坑娃圈手办")
browser(action="act", targetId="2", ref="14_189", kind="type", text="99")
browser(action="act", targetId="2", ref="14_194", kind="type", text="100")
```

### 5. 下拉框处理（✅ 已攻克）

淘宝的 combobox 组件（如"出售状态"、"适用年龄"、"品牌"）使用 React Portal 渲染，常规 type/click 无法选中选项。

**✅ 已验证有效方案 — JavaScript evaluate 直接点击 DOM：**

```javascript
// 第1步：点击 combobox 展开下拉选项
browser(action="act", targetId="2", ref="8_121", kind="click")

// 第2步：用 evaluate 遍历 DOM 找到目标文字并点击
browser(action="act", targetId="2", kind="evaluate",
  fn="() => { const allEls = document.querySelectorAll('div, span, li'); for (const el of allEls) { if (el.textContent.trim() === '现货') { el.click(); return 'clicked: ' + el.textContent; } } return 'not found'; }"
)
```

**原理：** evaluate 直接在页面执行 JS，遍历所有 div/span/li 元素，匹配文字后触发 click。绕过 React Portal 的渲染限制。

**适用场景：** 所有淘宝 combobox/下拉框/选择器（出售状态、适用年龄、品牌、类目选择器等）

**操作模板（替换文字即可）：**
```javascript
browser(action="act", targetId="<当前tabId>", ref="<combobox_ref>", kind="click")
// 等待1秒让下拉展开
browser(action="act", targetId="<当前tabId>", kind="evaluate",
  fn="() => { const allEls = document.querySelectorAll('div, span, li'); for (const el of allEls) { if (el.textContent.trim() === '<目标文字>') { el.click(); return 'clicked'; } } return 'not found'; }"
)
```

**备选方案（如果 evaluate 不可用）：**
1. 点击下拉框展开选项
2. 使用键盘 ArrowDown 移动到目标项 + Enter 确认
3. 或者记录 ref 后尝试直接 type 输入文字

### 6. 提交或保存草稿

```
# 提交
browser(action="act", ref="xxx_293", kind="click")  # 提交宝贝信息

# 保存草稿
browser(action="act", ref="xxx_295", kind="click")  # 保存草稿
```

## 常用 URL

| 页面 | URL |
|------|-----|
| 千牛卖家中心 | https://myseller.taobao.com/home.htm/QnworkbenchHome/ |
| 商品发布页 | https://myseller.taobao.com/home.htm/PublishProduct/index |
| 以图发品 | https://item.upload.taobao.com/sell/ai/category.htm |
| 图片素材中心 | https://suc.taobao.com |

## 商品信息模板

根据精灵少女手办图片（你发的图），建议填写：

| 字段 | 建议值 |
|------|--------|
| 标题 | 原创设计精灵少女手办 星空梦境治愈系桌面摆件 三坑娃圈手办 |
| 价格 | 99 |
| 库存 | 100 |
| 角色名 | 精灵少女 |
| 出售状态 | 现货 |
| 适用年龄 | 15 |
| 类目 | 手办/手办景品 |

## 注意事项

1. **下拉框**：✅ 已解决。使用 `evaluate` + JS DOM 遍历点击，可自动化所有 combobox 下拉框
2. **图片上传**：优先使用"从图片空间上传"，自动化工具可操作图片选择器
3. **草稿保存**：遇到问题时先保存草稿，避免数据丢失
4. **物流模板**：需提前在千牛设置好运费模板
5. **浏览器限制**：部分对话框（如类目选择器）可能需要用户配合点击，可尝试 evaluate 方案

## 错误排查

| 问题 | 解决方案 |
|------|----------|
| 页面加载慢 | 等待几秒后重试 snapshot |
| 点击无反应 | 尝试刷新页面或使用不同的 ref |
| 对话框无法操作 | 检查是否在 iframe 内，尝试切换 targetId |
| 上传失败 | 检查浏览器安全限制，尝试手动上传后继续 |
