# 小红书图文排版规范

## 📐 页面规格

**标准尺寸：**
- 宽度：375px
- 高度：667px（固定）
- 比例：9:16（小红书标准）
- 输出：750x1334px @2x（高清）

---

## 🚨 严格限制规则

### 1. 页面容器锁定

```css
.page {
  width: 375px;
  height: 667px;      /* 固定高度 */
  overflow: hidden;   /* 隐藏溢出 */
  position: relative;
  margin: 0;
  padding: 0;
}

.inner-page {
  padding: 30px 28px 35px;  /* 上 30px，左右 28px，下 35px */
  display: flex;
  flex-direction: column;
  max-height: 667px;
  box-sizing: border-box;
}
```

### 2. 内容高度分配

| 元素 | 高度范围 | 说明 |
|------|----------|------|
| Page Header | 50px | 标题 + 分隔线 |
| 信息框 | 80-120px | 根据内容量 |
| 代码块 | 60-80px | 固定行高 |
| 步骤项 | 70-90px | 每个步骤 |
| 对比列表 | 80-100px | 3-5 项 |
| 互动区 | 150px | 固定 |
| 标签区 | 80px | 固定 |

### 3. 每页内容上限

**信息框：≤3 个**
```html
<!-- 正确示例 -->
<div class="info-box">...</div>  <!-- 第 1 个 -->
<div class="info-box">...</div>  <!-- 第 2 个 -->
<div class="info-box">...</div>  <!-- 第 3 个 -->
<!-- 不要超过 3 个 -->
```

**代码块：≤2 个**
```html
<div class="code-block">...</div>  <!-- 第 1 个 -->
<div class="code-block">...</div>  <!-- 第 2 个 -->
<!-- 不要超过 2 个 -->
```

**列表项：≤6 个**
```html
<div class="list-item">...</div>  <!-- ×1 -->
<div class="list-item">...</div>  <!-- ×2 -->
<div class="list-item">...</div>  <!-- ×3 -->
<div class="list-item">...</div>  <!-- ×4 -->
<div class="list-item">...</div>  <!-- ×5 -->
<div class="list-item">...</div>  <!-- ×6 -->
<!-- 不要超过 6 个 -->
```

**总行数：≤35 行**（13px 字体）

### 4. 间距规范

```css
/* 模块间距 */
.info-box { margin-bottom: 14px; }
.code-block { margin: 12px 0; }
.step-item { margin-bottom: 12px; }
.compare-item { margin-bottom: 8px; }

/* 最后一个元素不额外留白 */
.inner-page > :last-child {
  margin-bottom: 0;
}

/* 页面标题间距 */
.page-header {
  margin-bottom: 18px;
  padding-bottom: 12px;
}
```

### 5. 字体大小范围

| 用途 | 字号 | 字重 |
|------|------|------|
| 封面大标题 | 36px | 800 |
| 封面副标题 | 16px | 500 |
| 内页标题 | 18px | 700 |
| 信息框标题 | 14px | 700 |
| 正文 | 13px | 400 |
| 代码块 | 11px | 400 |
| 标签 | 11px | 600 |
| 辅助文字 | 11px | 400 |

---

## ✅ 检查清单

生成前必须检查：

- [ ] 所有页面高度=667px（无溢出）
- [ ] 底部无多余留白（内容贴近底部）
- [ ] 无内容被截断（检查 overflow）
- [ ] 文字行数可控（每段≤3 行）
- [ ] 图片尺寸适配（最大宽度 319px）
- [ ] 对比度达标（≥4.5:1）
- [ ] 字体清晰可读（最小 11px）

---

## 🔧 内容适配策略

### 内容过多时
```
❌ 错误：压缩内容，塞进一页
✅ 正确：拆分为多页
```

**示例：**
```html
<!-- 原计划 1 页，内容过多 -->
<div class="page inner-page">
  <!-- 6 个信息框 - 太多了！ -->
</div>

<!-- 拆分为 2 页 -->
<div class="page inner-page">
  <!-- 3 个信息框 - 第 1 页 -->
</div>
<div class="page inner-page">
  <!-- 3 个信息框 - 第 2 页 -->
</div>
```

### 内容过少时
```
❌ 错误：强行拉伸，留大片空白
✅ 正确：增加示例/说明，或减少页数
```

**示例：**
```html
<!-- 内容太少，底部留白 -->
<div class="page inner-page">
  <div class="info-box">...</div>
  <div class="info-box">...</div>
  <!-- 底部大片空白 -->
</div>

<!-- 增加示例填充 -->
<div class="page inner-page">
  <div class="info-box">...</div>
  <div class="info-box">...</div>
  <div class="info-box">
    <div class="info-title">💡 示例</div>
    <div class="info-item">示例内容 1</div>
    <div class="info-item">示例内容 2</div>
  </div>
</div>
```

### 底部留白时
```
❌ 错误：忽略不管
✅ 正确：调整 padding 或增加内容
```

**调整方法：**
1. 减少页面标题间距：`margin-bottom: 18px → 15px`
2. 减少信息框间距：`margin-bottom: 14px → 12px`
3. 增加一个补充说明框

### 内容溢出时
```
❌ 错误：隐藏溢出内容
✅ 正确：删减文字或拆分页面
```

**删减技巧：**
- 删除冗余说明
- 精简列表项（6 个→4 个）
- 缩短每行文字（3 行→2 行）

---

## 🎨 视觉平衡检查

### 封面页
```
✅ 内容垂直居中
✅ 上下留白均衡
✅ 标题清晰醒目
✅ 特性标签水平排列
```

### 内页
```
✅ 内容从上到下均匀分布
✅ 模块间距一致
✅ 视觉重心稳定
✅ 无头重脚轻
```

### 最后一页
```
✅ 互动区 + 标签
✅ 底部留白≤20px
✅ 标签完整显示
✅ 无内容截断
```

---

## 📱 移动端适配

### 最小尺寸要求
- 按钮高度：≥40px
- 链接间距：≥8px
- 二维码：120x120px
- 图片最小宽度：200px

### 清晰度要求
- 输出分辨率：750x1334px @2x
- 文字边缘清晰（抗锯齿）
- 对比度≥4.5:1
- 最小字号：11px

---

## 🛠️ 调试技巧

### 1. 使用边框检查布局
```css
/* 调试时添加 */
.page {
  outline: 1px solid red;  /* 页面边界 */
}

.info-box {
  outline: 1px solid blue;  /* 模块边界 */
}
```

### 2. 检查内容高度
```javascript
// 在浏览器控制台运行
document.querySelectorAll('.page').forEach((page, i) => {
  const contentHeight = page.scrollHeight;
  console.log(`Page ${i + 1}: ${contentHeight}px / 667px`);
  if (contentHeight > 667) {
    console.warn(`⚠️ Page ${i + 1} overflows by ${contentHeight - 667}px`);
  }
});
```

### 3. 截图前预览
```bash
# 在浏览器打开 HTML 文件
open xiaohongshu-article.html

# 检查每个页面是否完整显示
# 滚动查看是否有内容被截断
```

---

## 📊 常见错误案例

### 错误 1：内容溢出
```html
<div class="page inner-page" style="height: 667px;">
  <!-- 实际内容高度 750px -->
  <div class="info-box">...</div>  <!-- ×8 个 - 太多了！ -->
</div>
<!-- ❌ 底部内容被截断 -->
```

**修复：** 拆分为 2 页

### 错误 2：底部留白
```html
<div class="page inner-page" style="height: 667px;">
  <!-- 实际内容高度 500px -->
  <div class="info-box">...</div>  <!-- ×2 个 - 太少了！ -->
</div>
<!-- ❌ 底部 167px 空白 -->
```

**修复：** 增加内容或调整间距

### 错误 3：间距不一致
```html
<div class="info-box" style="margin-bottom: 20px;">...</div>
<div class="info-box" style="margin-bottom: 10px;">...</div>
<div class="info-box" style="margin-bottom: 15px;">...</div>
<!-- ❌ 间距忽大忽小 -->
```

**修复：** 统一为 `margin-bottom: 14px`

---

## 🎯 最佳实践

1. **先规划内容量**，再决定页数
2. **使用统一间距**，保持视觉一致
3. **每页聚焦一个主题**，不要堆砌
4. **留白是设计**，但不要过多
5. **测试不同设备**，确保清晰度
6. **保存模板**，重复使用

---

*最后更新：2026-03-09*
*版本：v2.0.0*
