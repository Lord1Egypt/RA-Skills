# WeChat公众号编辑器 CSS 兼容性参考

## 测试背景

通过实际在公众号编辑器中粘贴 HTML 内容，验证哪些 CSS 属性能被保留、哪些会被过滤。以下结论基于真实测试，非理论推测。

## 标签兼容性

| HTML 标签 | 公众号支持 | 说明 |
|-----------|-----------|------|
| `<section>` | ✅ 最佳 | background-color、border、padding 等全部保留。**首选容器标签**。 |
| `<p>` | ✅ 好 | 基础排版标签，内联样式保留。 |
| `<span>` | ✅ 好 | 行内样式保留，适合文字强调。 |
| `<table>` | ✅ 好 | 多列布局首选，background-color 保留。记得加 `border-collapse:collapse`。 |
| `<h1>`-`<h6>` | ✅ 好 | 标题标签，内联样式保留。 |
| `<blockquote>` | ⚠️ 一般 | 部分样式可能被修改，建议用 `<section>` 替代。 |
| `<div>` | ❌ 差 | **background-color 会被剥离**。这是最常见的格式丢失原因。 |
| `<br>` | ✅ 好 | 换行保留。 |
| `<strong>`/`<b>` | ✅ 好 | 加粗保留。 |
| `<em>`/`<i>` | ✅ 好 | 斜体保留。 |

## CSS 属性兼容性

### ✅ 完全兼容（粘贴后保留）

| 属性 | 说明 |
|------|------|
| `background-color` | 背景色，必须用在 `<section>` 或 `<table>` 上 |
| `color` | 文字颜色 |
| `font-size` | 字号 |
| `font-weight` | 字重 |
| `font-style` | 字体样式（italic 等） |
| `line-height` | 行高 |
| `text-align` | 对齐方式 |
| `letter-spacing` | 字间距 |
| `padding` | 内边距 |
| `margin` | 外边距 |
| `border` | 边框 |
| `border-radius` | 圆角 |
| `border-left` | 左边框（用于引用块装饰） |
| `border-collapse` | 表格边框合并 |
| `width` | 宽度 |
| `vertical-align` | 垂直对齐（表格单元格） |

### ❌ 被过滤（粘贴后丢失）

| 属性 | 后果 | 替代方案 |
|------|------|---------|
| `display:flex` | 布局塌掉，元素堆叠 | 用 `<table>` 布局 |
| `linear-gradient` | 背景变透明 | 用纯色 `background-color` |
| `box-shadow` | 阴影消失 | 用 `border` 替代视觉层次 |
| `background:` (shorthand) | 部分情况丢失 | 用 `background-color:` |
| `position` | 定位失效 | 不使用绝对/相对定位 |
| `transform` | 变换失效 | 不使用 |
| `animation` | 动画失效 | 不使用 |
| `opacity` | 可能被过滤 | 不使用 |
| `::before`/`::after` | 伪元素全部丢失 | 用真实 HTML 元素替代 |

## 复制函数兼容性

### `file://` 协议下（本地 HTML 文件）

| API | 可用性 | 说明 |
|-----|--------|------|
| `document.execCommand('copy')` | ✅ 可用 | **首选方案**，在 file:// 下正常工作 |
| `navigator.clipboard.write()` | ❌ 不可用 | 需要 secure context (HTTPS/localhost) |
| `ClipboardItem` | ❌ 不可用 | 同上 |

### 复制函数最佳实践

```javascript
function copyArticle(id, btn) {
  var el = document.getElementById(id);
  var range = document.createRange();
  range.selectNodeContents(el);
  var sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  var ok = document.execCommand('copy');
  sel.removeAllRanges();
  // 更新按钮状态...
}
```

关键点：
- `onclick` 传 `this` 参数，不依赖全局 `event` 对象
- 用 `range.selectNodeContents(el)` 选中元素内容
- `execCommand('copy')` 复制选中内容到剪贴板（保留 HTML 格式）
- 复制后立即 `sel.removeAllRanges()` 清除选区

## 常见问题排查

### 问题：粘贴后背景色消失
**原因**：用了 `<div>` 标签
**解决**：改成 `<section>`

### 问题：粘贴后布局错乱
**原因**：用了 `display:flex`
**解决**：改成 `<table>` 布局

### 问题：粘贴后卡片/方框消失
**原因**：用了渐变背景或阴影
**解决**：渐变改纯色，去掉阴影，用 border 替代

### 问题：复制按钮点击无反应
**原因**：用了 `ClipboardItem` API（file:// 下不可用）
**解决**：改用 `document.execCommand('copy')`

### 问题：复制后只有部分内容有格式
**原因**：部分标签用了不兼容的 CSS
**解决**：检查所有元素的 style 属性，确保没有 flex/gradient/box-shadow
