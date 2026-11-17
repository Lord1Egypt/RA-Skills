# 微信公众号文章模板代码规范

> 适用场景：公众号原生编辑器 HTML 模式排版 / 第三方编辑器导出优化 / 自动化排版工具输出校验
>
> **⚠️ 重要勘误（2026-08-02）**：经实测验证，`<div>` 标签在公众号编辑器中**不可靠、会被过滤或被转为 `<section>`**，排版容器的唯一安全选择是 **`<section>`**。下文所有示例已据此修正；原版中"`<div>` 同样保留"的说法不成立，以本文修改后版本为准。

---

## 1. 公众号原生编辑器支持的基础 HTML 标签与排版规则

### 1.1 段落与换行 — `<p>` `<br>`

| 属性 | 说明 |
|------|------|
| **用途** | 段落、换行 |
| **安全样式** | `font-size`、`color`、`line-height`、`text-align`、`letter-spacing`、`class` |
| **注意事项** | 公众号会在段落外层自动包裹 `<section>`；行高默认约 **1.6–1.8**，如需精确控制请显式声明 `line-height` |

```html
<!-- 推荐写法 -->
<p style="font-size:15px; color:#333; line-height:1.8; text-align:justify; letter-spacing:0.5px;">
  正文内容...
</p>
```

### 1.2 行内装饰 — `<span>`

| 属性 | 说明 |
|------|------|
| **用途** | 行内高亮、局部样式、关键词标注 |
| **安全样式** | `color`、`font-weight`、`background`、`text-decoration`、`border-bottom` |
| **推荐场景** | 文本高亮（荧光笔效果）、加粗替代（语义不强时）、自定义下划线 |

```html
<!-- 高亮标记 -->
<span style="background:linear-gradient(transparent 60%, #FFE066 60%); font-weight:600;">
  重点内容
</span>

<!-- 自定义下划线 -->
<span style="border-bottom:2px solid #1890ff; padding-bottom:2px;">
  链接式强调
</span>
```

### 1.3 语义/强调标签

| 标签 | 语义 | 安全样式 |
|------|------|----------|
| `<strong>` / `<b>` | 加粗 | 继承 `style` |
| `<em>` / `<i>` | 斜体 | 继承 `style` |
| `<u>` | 下划线 | 继承 `style` |
| `<s>` / `<del>` | 删除线 | 建议用 `text-decoration: line-through` 替代以精确控制 |

```html
<strong style="color:#e33;">强烈建议</strong>
<em style="font-style:normal; background:#f0f0f0;">高亮斜体替代方案</em>
<span style="text-decoration:line-through; color:#999;">原价 ¥199</span>
```

### 1.4 标题 — `<h1>` `<h2>` `<h3>`

| 属性 | 说明 |
|------|------|
| **安全样式** | `font-size`、`color`、`text-align`、`font-weight`、`letter-spacing`、`margin` |
| **注意事项** | 编辑器可能自动转换为 `class="rich_media_title"` 的 `<h2>` 或 `<h1>`；在编辑器内可直接使用 |

```html
<h2 style="font-size:20px; color:#222; text-align:center; font-weight:700; letter-spacing:1px; margin:24px 0 16px;">
  二级标题
</h2>

<h3 style="font-size:17px; color:#444; border-left:3px solid #1890ff; padding-left:12px; margin:20px 0 12px;">
  带装饰的三级标题
</h3>
```

### 1.5 列表 — `<ul>` `<ol>` `<li>`

| 属性 | 说明 |
|------|------|
| **安全样式** | `font-size`、`color`、`line-height`、`padding-left` |
| **注意事项** | 列表符号（圆点/数字）会被保留；支持自定义 `list-style-type` |

```html
<ul style="font-size:15px; color:#555; line-height:2; padding-left:20px;">
  <li style="margin-bottom:8px;">无序列表项 1</li>
  <li>无序列表项 2</li>
</ul>

<ol style="font-size:15px; color:#555; line-height:2; padding-left:20px; list-style-type:decimal;">
  <li style="margin-bottom:8px;">有序列表项 1</li>
  <li>有序列表项 2</li>
</ol>
```

### 1.6 引用 — `<blockquote>`

| 属性 | 说明 |
|------|------|
| **安全样式** | `border-left`、`background`、`padding`、`margin`、`color` |
| **替代方案** | 也可使用微信官方组件 `mp-common-blockquote` |

```html
<blockquote style="border-left:4px solid #1890ff; background:#f7f9fc; padding:12px 16px; margin:16px 0; color:#666; font-size:14px;">
  引用或金句内容
</blockquote>
```

### 1.7 代码 — `<code>` `<pre>`

| 属性 | 说明 |
|------|------|
| **安全样式** | `font-family`(等宽字体)、`background`、`border-radius`、`padding` |
| **风险提示** | 超长代码行可能被强制换行，**不建议大面积使用 `<pre>`** |

```html
<!-- 行内代码 -->
<code style="font-family:Menlo, monospace; background:#f5f5f5; padding:2px 6px; border-radius:3px; font-size:13px; color:#e33;">
  npm install
</code>

<!-- 代码块（仅限短代码） -->
<pre style="background:#2d2d2d; color:#f8f8f2; padding:16px; border-radius:6px; font-size:13px; line-height:1.6; overflow-x:auto; white-space:pre-wrap;">
<code>const msg = "Hello WeChat";</code>
</pre>
```

### 1.8 图片 — `<img>`

| 属性 | 说明 |
|------|------|
| **安全属性** | `src`、`data-src`、`data-w`、`data-h`、`style` |
| **安全样式** | `width` / `max-width`、`height`、`border-radius`、`box-shadow`、`object-fit` |
| **注意事项** | **宽度建议 `max-width: 100%`**，避免溢出；上传后微信会替换为 CDN 链接并附加 `data-imgfileid` |

```html
<img
  src="https://mmbiz.qpic.cn/xxx"
  data-src="https://mmbiz.qpic.cn/xxx"
  data-w="1080"
  data-h="720"
  style="display:block; max-width:100%; height:auto; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.1); margin:16px auto;"
  alt="图片描述"
/>
```

### 1.9 超链接 — `<a>`

| 属性 | 说明 |
|------|------|
| **安全属性** | `href`、`target="_blank"`、`style` |
| **推荐场景** | 文内目录跳转（锚点）、外部链接、阅读原文链接 |
| **注意事项** | 公众号会自动添加跳转鉴权层 |

```html
<!-- 外部链接 -->
<a href="https://example.com" target="_blank" style="color:#1890ff; text-decoration:none; border-bottom:1px solid #1890ff;">
  查看原文
</a>

<!-- 目录锚点 -->
<a href="#section-1" style="color:#333; text-decoration:none;">一、核心规则</a>
```

### 1.10 表格 — `<table>` `<thead>` `<tbody>` `<tr>` `<td>`

| 属性 | 说明 |
|------|------|
| **安全样式** | `border`、`padding`、`text-align`、`background`、`font-size`、`width` |
| **限制** | **仅支持简单表格**，`colspan`/`rowspan` 等复杂跨行跨列表现不佳 |

```html
<table style="width:100%; border-collapse:collapse; font-size:14px; margin:16px 0;">
  <thead>
    <tr style="background:#f5f5f5;">
      <td style="padding:10px 12px; border:1px solid #e8e8e8; font-weight:600;">标签</td>
      <td style="padding:10px 12px; border:1px solid #e8e8e8; font-weight:600;">说明</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:10px 12px; border:1px solid #e8e8e8;">p</td>
      <td style="padding:10px 12px; border:1px solid #e8e8e8;">段落</td>
    </tr>
  </tbody>
</table>
```

### 1.11 结构与容器 — `<section>` 

| 属性 | 说明 |
|------|------|
| **安全样式** | 任意常用 CSS 布局属性 |
| **注意事项** | 微信编辑器大量使用 `<section>` 包裹内容块；**`<div>` 不可靠**——会被编辑器过滤或自动转为 `<section>`，排版容器**强制使用 `<section>`** |

```html
<section style="margin:24px 0; padding:20px; background:linear-gradient(135deg, #667eea, #764ba2); border-radius:12px; color:#fff;">
  <h2 style="color:#fff;">卡片标题</h2>
  <p>卡片内容描述</p>
</section>
```

---

## 2. 安全 CSS 属性白名单

> 以下属性经实测在公众号环境下可正常渲染，超出此范围的属性建议通过内联 `style` 逐一验证。

### 2.1 文字样式

| 属性 | 推荐值示例 |
|------|----------|
| `font-size` | `14px`—`22px`（正文建议 `15px`） |
| `font-family` | `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` |
| `font-weight` | `400` / `600` / `700` |
| `color` | `#333`（正文）、`#999`（辅助）、`#1890ff`（链接） |
| `letter-spacing` | `0.5px`—`2px` |
| `line-height` | `1.6`—`2.0`（正文建议 `1.8`） |
| `text-align` | `left` / `center` / `right` / `justify` |
| `text-decoration` | `underline` / `line-through` / `none` |
| `text-indent` | `2em`（首行缩进） |

### 2.2 盒模型

| 属性 | 推荐值示例 |
|------|----------|
| `margin` / `margin-top` / `margin-bottom` | `0`—`40px` |
| `padding` | `4px`—`32px` |
| `border` / `border-left` / `border-bottom` | `1px solid #e8e8e8` |
| `border-radius` | `4px`—`16px` |
| `box-shadow` | `0 2px 12px rgba(0,0,0,0.08)` |
| `background` / `background-color` | `#f5f5f5` / 渐变色 |
| `background-image` | **支持 base64**，适合装饰分割线、背景纹理 |
| `width` / `max-width` | `100%`（常用上限） |
| `height` / `max-height` | 按需使用 |

### 2.3 布局

| 属性 | 说明 |
|------|------|
| `display` | `block` / `inline` / `inline-block` / `flex` |
| `flex-direction` | `row` / `column` |
| `flex-wrap` | `nowrap` / `wrap` |
| `justify-content` | `center` / `space-between` / `space-around` |
| `align-items` | `center` / `flex-start` / `flex-end` |
| `gap` | 元素间距（`8px`—`20px`） |
| `float` | **慎用**，可能导致排版错乱 |
| `vertical-align` | `middle` / `top` / `bottom` |

```html
<!-- Flex 横向卡片布局示例 -->
<section style="display:flex; justify-content:space-between; align-items:center; gap:12px; margin:16px 0;">
  <section style="flex:1; background:#f0f7ff; padding:16px; border-radius:8px; text-align:center;">
    <strong style="font-size:20px; color:#1890ff;">128</strong>
    <p style="font-size:13px; color:#999; margin:4px 0 0;">文章数</p>
  </section>
  <section style="flex:1; background:#f6ffed; padding:16px; border-radius:8px; text-align:center;">
    <strong style="font-size:20px; color:#52c41a;">12.8k</strong>
    <p style="font-size:13px; color:#999; margin:4px 0 0;">阅读量</p>
  </section>
</section>
```

### 2.4 图像与动效

| 属性 | 说明 |
|------|------|
| `object-fit` | `cover` / `contain`，控制图片填充方式 |
| `border-radius` | 圆形头像 `50%` |
| `filter: brightness()` | 明暗调节 |
| `filter: contrast()` | 对比度调节 |
| `transition` / `animation` | **仅简单动效可用**；复杂动画通常被公众号过滤忽略，**不建议依赖** |

---

## 3. 会被过滤或失效的内容（红线）

> 以下内容在公众号正文中**确定会被移除或失效**，排版时必须避免。

### 3.1 脚本与事件 — **绝对禁止**

| 禁止项 | 说明 |
|--------|------|
| `<script>` 标签及其内容 | 完全移除 |
| 内联事件 | `onclick` / `onload` / `onerror` / `onmouseover` 等全部剥离 |
| 外链 CSS | `<link rel="stylesheet">` 失效 |
| 外链 JS | `<script src="...">` 移除 |

### 3.2 定位与层级 — **确定失效**

| 失效项 | 表现 |
|--------|------|
| `position: fixed` | 失效，退化为 `static` |
| `position: sticky` | 失效 |
| `z-index` 极高值 | 浮层效果不生效 |
| 全屏遮罩 `overlay` | 不生效或被移除 |

### 3.3 富媒体与外部资源 — **有限支持**

| 类别 | 规则 |
|------|------|
| 复杂 SVG | 可能被过滤或仅保留基本图形 |
| Canvas | 移除 |
| 非腾讯源音视频 | 不显示 |
| 指向非腾讯视频的 `<iframe>` | 移除 |
| 表单元素 | `input` / `textarea` / `button` / `select` — 正文中**通常被移除** |

---

## 4. 快速自检清单

在提交文章前，按以下项目逐项检查：

- [ ] 所有样式使用 **内联 `style` 属性**，无 `<style>` 标签、无外链 CSS
- [ ] 无 `<script>` 标签、无内联事件（`onclick` 等）
- [ ] 图片宽度 `max-width: 100%`，不超出移动端视口
- [ ] 正文字号 ≥ `14px`（移动端可读性底线）
- [ ] 无 `position: fixed/sticky`
- [ ] 无表单元素（`input` / `button` 等）
- [ ] 表格结构简单，无 `colspan` / `rowspan` 跨列
- [ ] 链接使用 `target="_blank"`
- [ ] Flex 布局有明确的 `gap` 或 `padding` 防止元素粘连

---

## 5. 推荐全局样式初始化

粘贴到编辑器 HTML 模式前，可在最外层容器统一设置基础样式：

```html
<section style="
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
  font-size: 15px;
  color: #333333;
  line-height: 1.8;
  letter-spacing: 0.5px;
  text-align: justify;
  max-width: 100%;
  word-break: break-all;
  box-sizing: border-box;
">
  <!-- 文章正文内容 -->
</section>
```

---

> **版本**：v2.0 \| **最后更新**：2026-08-02 \| **维护者**：AI Engineer
