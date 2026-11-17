---
description: HTML代码生成器严格工作规范
alwaysApply: true
---

# HTML代码生成器严格工作规范

## 0. 核心原则（最高优先级）

> ⚠️ **微信公众号会过滤 `<style>` 标签和 CSS 类选择器，以下规则必须严格遵守：**

- ❌ **禁止使用 `<style>` 标签** — 微信编辑器会删除所有 `<style>` 块，导致样式全部丢失
- ❌ **禁止使用 CSS 类选择器** — 不用 `class="xxx"`，微信不认 CSS 类
- ✅ **所有样式必须写在 `style=""` 属性里** — 每个元素的样式都内联
- ✅ **容器宽度用 `100%`** — 不用固定宽度（如 677px）+ 居中，微信自带内容宽度
- ✅ **用固定像素值（px）** — `clamp()` 在微信渲染器中部分不兼容，建议用固定 px 值

```html
<!-- ❌ 错误：依赖 <style> 和 CSS 类 -->
<style>.container { width: 677px; }</style>
<div class="container">内容</div>

<!-- ✅ 正确：完全内联，宽度 100% -->
<div style="width:100%; padding:0; box-sizing:border-box;">内容</div>
```

---

## 1. 基础结构

**单 html 文件，文件名 YYYYMMDD_HHMMSS_related_name.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标题</title>
</head>
<body style="font-family:'Microsoft YaHei','PingFang SC',Arial,sans-serif; color:#333; line-height:1.6; margin:0; padding:0;">
    <div style="width:100%; padding:0; box-sizing:border-box;">
        <!-- 内容直接放置段落元素，禁止嵌套额外容器 -->
    </div>
</body>
</html>
```

---

## 2. 容器规范

### 文章容器（宽度 100%）

```html
<!-- 外层容器 -->
<div style="width:100%; padding:0; box-sizing:border-box; background-color:#fff;">
    <!-- 内容区域 -->
    <div style="padding:0; margin:0;">
        <!-- 段落、标题等元素直接放置 -->
    </div>
</div>
```

### 图文卡片（贴图、小绿书、小红书）容器（宽度 375px）

```html
<div style="width:375px; max-width:100%; margin:0 auto; padding:0; box-sizing:border-box;">
    <!-- 卡片内容 -->
</div>
```

---

## 3. 字体规范

所有字号直接写在元素的 `style` 属性中：

```html
<!-- 正文 -->
<p style="font-size:16px; line-height:1.8;">正文内容</p>

<!-- 一级标题 -->
<h1 style="font-size:20px; font-weight:bold; text-align:center;">一、标题</h1>

<!-- 二级标题 -->
<h2 style="font-size:18px; font-weight:bold;">1.1 标题</h2>

<!-- 三级标题 -->
<h3 style="font-size:16px; font-weight:bold;">1.1.1 标题</h3>

<!-- 辅助文字 -->
<p style="font-size:15px; color:#666;">辅助说明文字</p>

<!-- 注释说明 -->
<p style="font-size:14px; color:#999;">注释或备注文字</p>
```

**字体规则：**
- ✅ 标题编号：H1 用"一、二、三"，H2 用"1.1、1.2"，H3 用"1.1.1"
- ✅ 若文章仅有一级标题，字号使用 h3 样式；仅有二级标题，一级用 h2 样式，二级用 h3 样式

---

## 4. 配色规范

### 4.1 色彩数量限制

- ✅ 主色调 1 个：品牌色或主题色
- ✅ 辅助色 1-2 个：与主色调协调的补充色
- ✅ 强调色 1 个：用于重点元素
- ✅ 中性色 2-3 个：灰度系列（文本、背景、边框）
- ❌ 严禁超过 5 种主体颜色（不含黑白灰）
- ❌ 绝对禁止紫色及紫色渐变（特殊场景除外）

### 4.2 色彩使用原则

**主色调（Primary Color）**
- 作用：定义页面整体风格基调，建立品牌识别
- 应用场景：大面积背景、主要容器、标题区域

**辅助色（Secondary Color）**
- 作用：丰富视觉层次，形成对比但不喧宾夺主
- 应用场景：卡片背景、次级区块

**强调色（Accent Color）**
- 作用：吸引注意力，突出重要信息
- 应用场景：重要数据、状态提示、高亮标注

**中性色（Neutral Colors）**
- 作用：保证内容可读性，提供视觉缓冲
- 说明：不占主体颜色配额，确保对比度达标

### 4.3 配色策略

根据文章场景选择色彩方向：

| 场景 | 色彩方向 | 说明 |
|------|----------|------|
| 专业 / 商务 | 冷色调（蓝、绿、灰） | 传递稳重可靠 |
| 营销 / 转化 | 暖色调（红、橙、黄） | 激发行动欲望 |
| 自然 / 健康 | 绿色系 | 传递生态安全感 |
| 简约 / 设计 | 黑白灰 + 少量强调色 | 体现专业性 |
| 活力 / 创意 | 高饱和度色彩 | 展现个性活力 |

### 4.4 渐变使用规范

- ✅ 允许：同色系渐变（深→浅）、邻近色渐变（色相环 ±60°）
- ✅ 允许：透明度渐变（同色不同透明度）
- ❌ 禁止：跨越色相环的对比色渐变（视觉冲突）
- ❌ 禁止：超过 2 种颜色的多色渐变（过于花哨）
- 角度建议：`90deg`（垂直）、`135deg`（对角）、`180deg`（水平）

### 4.5 对比度要求（无障碍标准）

- 正文文字与背景对比度 ≥ 4.5:1
- 标题文字与背景对比度 ≥ 3:1
- 重点元素与背景对比度 ≥ 3:1

---

## 5. 布局规范

文本字体大小一般不要低于 15px（表格、备注、说明等以及其它本身有需要小的文本除外）

```html
<!-- Flex 布局 -->
<div style="display:flex; gap:16px;">
    <div style="flex:1;">内容A</div>
    <div style="flex:1;">内容B</div>
</div>

<!-- Grid 自适应 -->
<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px;">
    <div>项目1</div>
    <div>项目2</div>
</div>

<!-- 卡片 -->
<div style="padding:16px; border-radius:8px; background-color:#f9f9f9;">卡片内容</div>
```

**布局限制：**
- ❌ 禁止 `position: absolute` / `position: fixed`
- ✅ 只能使用 `position: relative`
- ❌ 禁止 `top` `left` `right` `bottom` 定位
- ❌ 禁止 `float`

---

## 6. 标题规范

- 页面已有 `<title>` 标签展示标题，内容区域**严格禁止**重复输出**页面主标题**（即与 `<title>` 内容相同或相近的标题文字）
- ❌ 内容区域禁止输出 `<header>` 标签
- ❌ 内容区域禁止输出主标题或主标题相关描述
- ❌ 内容区域禁止用左边框（`border-left`）装饰任何级别的段落标题
- ❌ 内容区域禁止在段落标题下面用横线装饰

---

## 7. 文章内容规范

### 内容输出规则（严格执行）

- ✅ 容器内直接放置段落元素（`<p>`、`<section>` 等），中间不得嵌套 wrapper / inner 等额外容器
- ✅ 标题编号使用文字序号，使用主题色文字颜色或渐变背景标注，宽度自适应标题内容

### 段落边距规则（严格执行）

**边距规则说明：**
- ✅ 无背景色的段落 / 标题：只允许设置 `padding-top` 和 `padding-bottom`
- ✅ 有 `background-color` 的段落：四个方向均可设置 `padding`
- ❌ 无背景色的段落 / 标题：严禁设置 `padding-left` 和 `padding-right`

**代码示例：**

```html
<div style="width:100%; padding:0; box-sizing:border-box;">

    <!--
     ✅ 无背景色段落，无左右内边距
     ✅ 遵循「标题规范」：禁止输出 <header> 标签及页面主标题
     -->
    <h2 style="font-size:18px; font-weight:bold; padding-top:16px; padding-bottom:8px;">一、标题</h2>
    <p style="font-size:16px; line-height:1.8; padding-top:8px; padding-bottom:8px;">正文内容正文内容正文内容</p>

    <!-- ✅ 有背景色段落，可设置四方向内边距 -->
    <section style="background-color:#f0f7ff; padding:16px; border-radius:8px;">
        <p style="font-size:16px; line-height:1.8;">高亮内容</p>
    </section>

</div>
```

### 表格规范

```html
<table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead>
        <tr>
            <th style="background-color:#d6eaf8; padding:8px; text-align:left; font-size:14px;">列标题</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:8px; border-bottom:1px solid #eee; font-size:14px;">内容</td>
        </tr>
        <tr>
            <td style="padding:8px; border-bottom:1px solid #eee; font-size:14px; background-color:#f9f9f9;">偶数行内容</td>
        </tr>
    </tbody>
</table>
```

---

## 8. 图文卡片（贴图、小绿书、小红书）（分页）规范

**宽度 375px，默认 3:4 竖图比例，高度 500px**

### 尺寸对照

| 比例 | 高度计算 | 示例（375px） |
|------|----------|--------------|
| 1:1  | 宽 × 1   | 375px        |
| 3:4  | 宽 × 4/3 | 500px        |
| 4:3  | 宽 × 3/4 | 281px        |

### HTML 结构规则

- ✅ 文字内容只用 `<p>` 标签（JS 分页依赖此标签）
- ✅ 分页容器直接子元素只能是扁平块级元素
- ❌ 禁止在分页容器内套 wrapper / inner 等额外容器
- ❌ 禁止用 `<div>` 承载纯文字内容

```html
<!-- ✅ 正确 -->
<div style="width:375px; max-width:100%; height:500px; display:flex; flex-direction:column; box-sizing:border-box; overflow:hidden; outline:1px solid #f5f5f5;">
    <p style="font-size:18px; font-weight:bold;">标题文字</p>
    <p style="font-size:16px; line-height:1.6;">正文段落</p>
    <img style="width:100%; height:auto; max-height:40%; object-fit:cover;" src="..." alt="...">
</div>

<!-- ❌ 错误 -->
<div style="width:375px; height:500px;">
    <div>
        <p>内容</p>
    </div>
</div>
```

### 自动分页脚本（放在 `</body>` 前）

> ⚠️ 分页脚本依赖 `class="pagination"` 选择器，此处为 JS 运行时例外，允许使用 class。

```html
<div class="pagination" style="width:375px; max-width:100%; height:500px; display:flex; flex-direction:column; box-sizing:border-box; overflow:hidden; outline:1px solid #f5f5f5;">
    <p style="font-size:18px; font-weight:bold;">标题文字</p>
    <p style="font-size:16px; line-height:1.6;">正文段落</p>
</div>
```

```javascript
(function() {
    var pages = document.querySelectorAll('.pagination');
    if (!pages.length) return;
    var pageHeight = pages[0].offsetHeight;

    function getOrCreateNextPage(page) {
        var next = page.nextElementSibling;
        if (!next || !next.classList.contains('pagination')) {
            next = document.createElement('div');
            next.className = page.className;
            next.setAttribute('style', page.getAttribute('style'));
            page.parentNode.insertBefore(next, page.nextSibling);
        }
        return next;
    }

    function isUnsplittable(el) {
        return ['IMG','TABLE','UL','OL','DIV'].includes(el.tagName);
    }

    function splitElement(el, page) {
        if (isUnsplittable(el) || el.tagName !== 'P') return false;
        var text = el.textContent;
        if (!text.trim()) { el.remove(); return true; }
        var pageTop = page.getBoundingClientRect().top;
        var lo = 0, hi = text.length;
        while (lo < hi - 1) {
            var mid = Math.floor((lo + hi) / 2);
            el.textContent = text.slice(0, mid);
            el.getBoundingClientRect().bottom - pageTop > pageHeight ? hi = mid : lo = mid;
        }
        var firstPart = text.slice(0, lo), secondPart = text.slice(lo);
        if (!firstPart.trim()) { el.textContent = text; return false; }
        el.textContent = firstPart;
        if (secondPart.trim()) {
            var next = getOrCreateNextPage(page);
            var newEl = document.createElement('P');
            newEl.setAttribute('style', el.getAttribute('style'));
            newEl.textContent = secondPart;
            next.appendChild(newEl);
        }
        return true;
    }

    var maxIter = 10000, count = 0, i = 0;
    while (i < document.querySelectorAll('.pagination').length && count < maxIter) {
        count++;
        var page = document.querySelectorAll('.pagination')[i];
        Array.from(page.children).forEach(function(c) {
            if (!c.textContent.trim() && c.tagName !== 'IMG') c.remove();
        });
        if (page.scrollHeight > pageHeight) {
            var children = Array.from(page.children), handled = false;
            var pageTop = page.getBoundingClientRect().top;
            for (var j = 0; j < children.length; j++) {
                if (children[j].getBoundingClientRect().bottom - pageTop > pageHeight) {
                    if (!splitElement(children[j], page)) {
                        getOrCreateNextPage(page).appendChild(children[j]);
                    }
                    handled = true; break;
                }
            }
            if (!handled) i++;
        } else { i++; }
    }
})();
```

---

## 9. CSS 限制

| 禁止 | 替代方案 |
|------|----------|
| `<style>` 标签 | 所有样式写在 `style=""` 属性中 |
| `class="xxx"` 类选择器 | 内联 `style=""` 属性 |
| `:hover` `:active` `:focus` `::before` `::after` | CSS 渐变背景 / 实际 `<div>` 元素 |
| `backdrop-filter` | 半透明背景 `rgba` |
| `filter` | `box-shadow` / `text-shadow` |
| `position: absolute/fixed` | `position: relative` |
| `top/left/right/bottom` 定位 | Flex / Grid 布局 |
| `float` | Flex / Grid 布局 |
| 固定宽度（如 `width:677px`）+ 居中 | `width:100%` |

---

## 10. HTML 标签限制

| 禁止 | 替代 |
|------|------|
| `<button>` | `<div>` |
| `<i>` + Font Awesome | Emoji 或内联 SVG |
| `<form>` `<input>` `<label>` | — |
| `<iframe>` `<embed>` | — |

---

## 11. JavaScript 限制

- ❌ 禁止所有事件监听器（`addEventListener`、`onclick`、`onload` 等）
- ✅ 允许用于初始化渲染（图表初始化、DOM 操作）
- ⚠️ JavaScript 中设置样式属性必须使用固定值，不能使用 `clamp()`

```javascript
/* ❌ 错误：JS 中不能用 clamp() */
element.style.fontSize = 'clamp(16px, 1.4vw, 18px)';

/* ✅ 正确：JS 中使用固定值 */
element.style.fontSize = '16px';
```
