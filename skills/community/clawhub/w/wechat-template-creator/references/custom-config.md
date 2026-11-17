# 微信公众号排版自定义配置参考

本文档定义了"完全自定义模式"下用户可以配置的所有排版要素，以及对应的 CSS 内联样式写法。

**核心原则**：微信公众号编辑器不支持外部 CSS 和 class 属性，所有样式必须使用内联 `style` 属性。不支持 CSS 伪元素（::before, ::after），需使用实际 HTML 元素实现装饰效果。

> **📋 权威规范**：本文档为自定义模式的配置参考；完整的 HTML 代码规范约束（红线、白名单、自检清单）请查看 `references/wechat-html-spec.md`。

---

## 公众号编辑器限制与红线（强制遵守）

以下内容在公众号正文中**确定会被移除或失效**，排版时必须避免：

| 类别 | 禁止/失效项 |
|------|------------|
| 脚本 | `<script>` 标签及内联事件（onclick 等）完全移除 |
| 外部资源 | `<link rel="stylesheet">`、外链 JS 失效 |
| 定位 | `position: fixed` / `position: sticky` 失效 |
| 富媒体 | Canvas 移除、非腾讯源音视频不显示、`<iframe>` 移除 |
| 表单 | `input` / `textarea` / `button` / `select` 通常被移除 |
| 伪元素 | `::before` / `::after` 不支持 |
| **容器标签** | **`<div>` 不可靠，会被编辑器过滤或自动转换，强制使用 `<section>`** |
| 表格 | 仅支持简单表格，`colspan` / `rowspan` 表现不佳；请使用 `<td style="font-weight:600;">` 替代 `<th>` |
| SVG | 复杂 SVG 可能被过滤，仅保留基本图形 |

### 图片规范

```html
<img src="..." style="display:block;max-width:100%;height:auto;border-radius:8px;margin:16px auto;">
```

### 全局字体与基线

推荐的全局容器样式（包裹整个模板）：

```html
<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei','Helvetica Neue',sans-serif;font-size:17px;box-sizing:border-box;color:#333;line-height:1.8;letter-spacing:0.5px;max-width:100%;word-break:break-all;">
```

> **移动优先原则**：正文默认 17px，确保在 375px 宽度的移动端屏幕上清晰可读。所有容器添加 `box-sizing:border-box` 防止 padding 撑破宽度。

### 自检清单

- [ ] 所有样式使用内联 `style`，无 `<style>` 标签、无外链 CSS
- [ ] 无 `<script>` 标签、无内联事件
- [ ] **无 `<div>` 标签，所有容器均为 `<section>`**
- [ ] 图片 `max-width:100%; display:block; height:auto;`
- [ ] 正文字号默认 17px，辅助文字 ≥ 13px
- [ ] 无 `position: fixed/sticky`
- [ ] 无表单元素
- [ ] 表格使用 `<td style="font-weight:600;">` 而非 `<th>`，结构简单
- [ ] 链接使用 `target="_blank"`
- [ ] 全局容器包含标准 font-family、`word-break:break-all` 和 `box-sizing:border-box`
- [ ] **移动优先**：列表 `padding-left ≥ 32px`，表格字号 ≥ 15px，代码字号 ≥ 14px

---

## 1. 正文字体及字体大小

**配置项**：
- 字体族：`font-family`
- 字号：`font-size`
- 行高：`line-height`
- 字重：`font-weight`
- 颜色：`color`
- 字间距：`letter-spacing`
- 对齐方式：`text-align`（left | center | justify）

**预设选项**：

| 风格 | font-family | font-size | line-height | color |
|------|-------------|-----------|-------------|-------|
| 现代简约 | 默认系统字体 | 17px | 1.8 | #333 |
| 经典宋体 | "宋体",SimSun,serif | 17px | 1.85 | #3e3e3e |
| 优雅黑体 | "微软雅黑","Helvetica Neue",sans-serif | 17px | 1.9 | #444 |
| 小巧精致 | 默认系统字体 | 16px | 1.85 | #555 |
| 大气疏朗 | "PingFang SC","微软雅黑",sans-serif | 18px | 2.0 | #2e2e2e |

> **移动优先**：正文默认 17px，确保移动端阅读体验。如用户无特殊需求，推荐使用 17px。

**CSS 模板**：
```html
<p style="font-family:PingFang SC,微软雅黑,sans-serif;font-size:17px;color:#333;line-height:1.85;margin:0 0 16px;text-align:justify;letter-spacing:0.5px;">
  正文内容
</p>
```

---

## 2. 二级标题装饰

**配置项**：
- 字体大小：`font-size`
- 字重：`font-weight`
- 颜色：`color`
- 装饰类型：左侧色条 | 底部横线 | 背景色块 | 编号前缀 | 图标装饰 | 全宽色带 | 双线装饰
- 装饰颜色：`border-color` / `background`
- 对齐方式：`text-align`

**装饰类型 CSS 模板**：

### a) 左侧色条
```html
<h2 style="font-size:20px;font-weight:700;color:#333;padding-left:14px;border-left:4px solid {{主色}};margin:30px 0 14px;line-height:1.4;">
  标题内容
</h2>
```

### b) 底部横线
```html
<h2 style="font-size:20px;font-weight:700;color:#333;padding-bottom:8px;border-bottom:2px solid {{主色}};margin:28px 0 14px;line-height:1.4;">
  标题内容
</h2>
```

### c) 背景色块
```html
<h2 style="font-size:19px;font-weight:700;color:#fff;background:{{主色}};padding:10px 16px;margin:28px 0 14px;border-radius:4px;line-height:1.4;">
  标题内容
</h2>
```

### d) 编号前缀
```html
<h2 style="font-size:20px;font-weight:700;color:#333;margin:28px 0 14px;line-height:1.4;">
  <span style="display:inline-block;background:{{主色}};color:#fff;width:28px;height:28px;text-align:center;line-height:28px;border-radius:50%;font-size:14px;margin-right:8px;vertical-align:middle;">01</span>标题内容
</h2>
```

### e) 图标装饰
```html
<h2 style="font-size:20px;font-weight:700;color:#333;margin:28px 0 14px;line-height:1.4;">
  <span style="display:inline-block;width:8px;height:8px;background:{{主色}};border-radius:50%;margin-right:8px;vertical-align:middle;"></span>标题内容
</h2>
```

### f) 全宽色带
```html
<h2 style="font-size:20px;font-weight:700;color:#333;margin:28px 0 14px;padding:8px 16px;background:linear-gradient(90deg,{{主色}}15,transparent 15%);line-height:1.4;">
  标题内容
</h2>
```

### g) 双线装饰
```html
<section style="text-align:center;margin:24px 0 10px;">
  <span style="display:inline-block;width:30px;border-top:2px solid {{主色}};vertical-align:middle;"></span>
  <h2 style="display:inline-block;font-size:18px;font-weight:700;color:#333;margin:0 12px;vertical-align:middle;line-height:1.4;">标题内容</h2>
  <span style="display:inline-block;width:30px;border-top:2px solid {{主色}};vertical-align:middle;"></span>
</section>
```

---

## 3. 段落间距与间隔样式

**配置项**：
- 段间距：`margin-bottom`
- 段落分隔线类型：无 | 虚线 | 实线 | 渐变线 | SVG 装饰分隔 | 符号分隔
- 段落分隔线颜色：`border-color`
- 段落分隔线宽度：`border-width`

**分隔线 CSS 模板**：

### a) 虚线分隔
```html
<section style="text-align:center;margin:20px 0;border-top:1px dashed {{辅色}};"></section>
```

### b) 渐变分隔
```html
<section style="text-align:center;margin:24px 0;height:1px;background:linear-gradient(90deg,transparent,{{主色}},transparent);"></section>
```

### c) 三点分隔
```html
<section style="text-align:center;margin:24px 0;">
  <span style="display:inline-block;width:5px;height:5px;background:{{主色}};border-radius:50%;margin:0 5px;"></span>
  <span style="display:inline-block;width:5px;height:5px;background:{{辅色}};border-radius:50%;margin:0 5px;"></span>
  <span style="display:inline-block;width:5px;height:5px;background:{{主色}};border-radius:50%;margin:0 5px;"></span>
</section>
```

### d) SVG 波形分隔
```html
<section style="text-align:center;margin:24px 0;">
  <svg width="200" height="20" style="display:inline-block;">
    <line x1="0" y1="10" x2="80" y2="10" stroke="{{主色}}" stroke-width="1" stroke-dasharray="4,4" opacity="0.4"/>
    <circle cx="100" cy="10" r="2" fill="{{主色}}"/>
    <line x1="110" y1="10" x2="200" y2="10" stroke="{{主色}}" stroke-width="1" stroke-dasharray="4,4" opacity="0.4"/>
  </svg>
</section>
```

### e) 符号分隔
```html
<section style="text-align:center;margin:24px 0;font-size:18px;color:{{辅色}};letter-spacing:12px;">
  · · ·
</section>
```

---

## 4. 头部样式

**配置项**：
- 标题装饰线/图形
- 头部背景色/渐变
- 头部 margin/padding
- 日期/作者显示样式
- 分类标签样式

**常用头部 CSS 模板**：

### a) 简约型
```html
<section style="text-align:center;padding:30px 0 20px;margin-bottom:16px;">
  <h1 style="font-size:24px;font-weight:700;color:#1a1a1a;margin:0 0 12px;line-height:1.5;">{{标题}}</h1>
  <section style="font-size:13px;color:#999;letter-spacing:2px;">
    <span>{{作者}}</span><span style="margin:0 10px;">|</span><span>{{日期}}</span>
  </section>
</section>
```

### b) 装饰型
```html
<section style="text-align:center;padding:24px 20px;background:linear-gradient(180deg,{{浅色背景}} 0%,#fff 100%);border-radius:12px;margin-bottom:20px;">
  <section style="width:40px;height:3px;background:{{主色}};margin:0 auto 16px;border-radius:2px;"></section>
  <h1 style="font-size:24px;font-weight:700;color:#1a1a1a;margin:0 0 10px;line-height:1.5;">{{标题}}</h1>
  <p style="font-size:12px;color:{{辅色}};letter-spacing:3px;margin:0;">{{副标题/分类}}</p>
</section>
```

### c) 卡片型
```html
<section style="background:{{主色}};padding:20px 24px;border-radius:8px;margin-bottom:20px;text-align:center;">
  <p style="font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:4px;margin:0 0 8px;">{{栏目标签}}</p>
  <h1 style="font-size:22px;font-weight:700;color:#fff;margin:0 0 8px;line-height:1.5;">{{标题}}</h1>
  <p style="font-size:12px;color:rgba(255,255,255,0.6);margin:0;">{{作者}} · {{日期}}</p>
</section>
```

---

## 5. 底部样式

**配置项**：
- 二维码区域样式（边框、圆角、阴影、尺寸）
- 二维码引导文字
- 公众号名称展示
- Slogan 展示
- 免责声明区样式
- 底部纹路/装饰

**底部 CSS 模板**：

### a) 标准型
```html
<section style="text-align:center;padding:24px 0 16px;margin-top:24px;border-top:1px solid #e8e8e8;">
  <p style="font-size:14px;color:{{主色}};font-weight:700;margin:0 0 4px;">{{公众号名称}}</p>
  <p style="font-size:12px;color:#999;margin:0 0 16px;">{{Slogan}}</p>
  <section style="margin:12px 0;">
    <img src="{{二维码URL}}" style="width:110px;height:110px;border:1px solid #eee;padding:4px;border-radius:4px;">
  </section>
  <p style="font-size:12px;color:#999;margin:0;">长按识别二维码，关注我们</p>
</section>
```

### b) 卡片型
```html
<section style="background:{{浅色背景}};padding:20px;border-radius:10px;margin-top:24px;text-align:center;">
  <p style="font-size:14px;font-weight:700;color:{{主色}};margin:0 0 4px;">{{公众号名称}}</p>
  <p style="font-size:12px;color:{{辅色}};margin:0 0 14px;">{{Slogan}}</p>
  <section style="display:inline-block;background:#fff;padding:8px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
    <img src="{{二维码URL}}" style="width:100px;height:100px;">
  </section>
  <p style="font-size:12px;color:{{辅色}};margin:10px 0 0;">扫码关注，获取更多内容</p>
</section>
```

### c) 左右布局型
```html
<section style="display:flex;align-items:center;justify-content:center;padding:20px;margin-top:24px;border-top:2px solid {{主色}};">
  <section>
    <img src="{{二维码URL}}" style="width:90px;height:90px;border:1px solid #eee;padding:3px;">
  </section>
  <section style="margin-left:16px;text-align:left;">
    <p style="font-size:14px;color:{{主色}};font-weight:700;margin:0 0 4px;">{{公众号名称}}</p>
    <p style="font-size:12px;color:#999;margin:0 0 4px;">{{Slogan}}</p>
    <p style="font-size:11px;color:#bbb;margin:0;">← 长按识别关注</p>
  </section>
</section>
```

### 免责声明模板
```html
<section style="margin-top:16px;padding:10px 14px;background:#f8f8f8;border-radius:4px;">
  <p style="font-size:11px;color:#bbb;margin:0;line-height:1.6;">
    <strong>免责声明：</strong>本文内容仅供参考，不构成任何专业建议。
  </p>
</section>
```

---

## 6. 划重点/强调样式

**配置项**：
- 强调类型：高亮色底 | 加粗变色 | 下划线 | 背景色块 | 边框色块 | 渐变底色
- 高亮色：`background`
- 文字色：`color`
- 圆角大小：`border-radius`
- 内边距：`padding`

**CSS 模板**：

### a) 荧光笔高亮
```html
<span style="background:linear-gradient(180deg,transparent 60%,{{高亮色}} 60%);padding:0 4px;font-weight:700;">重点文字</span>
```

### b) 加粗变色
```html
<span style="color:{{主色}};font-weight:700;">重点文字</span>
```

### c) 背景色块（整段）
```html
<p style="background:{{浅色背景}};padding:12px 16px;border-radius:6px;border-left:3px solid {{主色}};font-size:17px;color:{{主色}};font-weight:600;line-height:1.8;margin:16px 0;">
  💡 重点内容段落
</p>
```

### d) 下划线强调
```html
<span style="border-bottom:3px solid {{高亮色}};padding-bottom:2px;font-weight:700;">重点文字</span>
```

---

## 7. 引用块样式

**配置项**：
- 边框样式：左侧色条 | 全边框 | 顶底边框
- 边框颜色：`border-color`
- 背景色：`background`
- 左侧缩进：`padding-left` / `border-left-width`
- 圆角：`border-radius`
- 引用符号（使用 emoji 或 HTML 实体）

**CSS 模板**：

### a) 经典左色条
```html
<blockquote style="background:#f8f9fa;border-left:3px solid {{主色}};margin:16px 0;padding:14px 18px;border-radius:0 6px 6px 0;">
  <p style="margin:0;font-size:16px;color:#555;line-height:1.8;">引用内容</p>
</blockquote>
```

### b) 全边框卡片
```html
<blockquote style="background:#fafafa;border:1px solid #e0e0e0;border-radius:8px;margin:16px 0;padding:16px 20px;">
  <p style="margin:0;font-size:16px;color:#555;line-height:1.8;">引用内容</p>
</blockquote>
```

### c) 引号装饰
```html
<blockquote style="margin:20px 0;padding:0 0 0 16px;border-left:2px solid {{主色}};">
  <p style="margin:0;font-size:18px;color:{{主色}};line-height:1;opacity:0.3;">"</p>
  <p style="margin:0;font-size:16px;color:#555;line-height:1.8;">引用内容</p>
</blockquote>
```

---

## 8. 代码块样式

**配置项**：
- 背景色：`background`（深色主题 | 浅色主题 | 自定义色）
- 文字色：`color`
- 代码字体：`font-family`
- 字号：`font-size`
- 左侧装饰线：`border-left`
- 语言标签：使用 HTML 元素
- 语法高亮配色方案

**预设配色方案**：

| 方案 | 背景 | 文字 | 关键字 | 字符串 | 注释 | 函数 |
|------|------|------|--------|--------|------|------|
| VS Code Dark | #1e1e1e | #d4d4d4 | #569cd6 | #ce9178 | #6a9955 | #dcdcaa |
| Monokai | #272822 | #f8f8f2 | #66d9ef | #e6db74 | #75715e | #a6e22e |
| 简约灰 | #f5f5f5 | #333 | #0366d6 | #d73a49 | #6a737d | #6f42c1 |
| Dracula | #282a36 | #f8f8f2 | #ff79c6 | #f1fa8c | #6272a4 | #50fa7b |

**CSS 模板（深色）**：
```html
<pre style="background:#1e1e1e;color:#d4d4d4;padding:18px 20px;border-radius:8px;font-size:14px;line-height:1.7;overflow-x:auto;margin:16px 0;font-family:Courier New,monospace;white-space:pre-wrap;word-break:break-all;">
<code>// 你的代码</code>
</pre>
```

**CSS 模板（浅色）**：
```html
<pre style="background:#f6f8fa;color:#333;padding:16px 20px;border-radius:8px;font-size:14px;line-height:1.7;overflow-x:auto;margin:16px 0;border:1px solid #e8e8e8;font-family:Courier New,monospace;white-space:pre-wrap;">
<code>// 你的代码</code>
</pre>
```

---

## 9. 表格样式

**配置项**：
- 表头背景色：`background`
- 表头文字色：`color`
- 表头字重：`font-weight`
- 边框样式：全边框 | 仅水平线 | 无线框
- 边框颜色：`border-color`
- 斑马纹行背景
- 单元格内边距：`padding`
- 对齐方式：`text-align`

**CSS 模板**：

### a) 经典全边框
```html
<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;border:1px solid #e0e0e0;">
  <thead>
    <tr style="background:{{主色}};color:#fff;">
      <td style="padding:12px 10px;text-align:left;font-weight:600;border:1px solid rgba(255,255,255,0.2);">列1</td>
      <td style="padding:12px 10px;text-align:center;font-weight:600;border:1px solid rgba(255,255,255,0.2);">列2</td>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#fff;">
      <td style="padding:10px 10px;border:1px solid #e0e0e0;">数据</td>
      <td style="padding:10px 10px;text-align:center;border:1px solid #e0e0e0;">数据</td>
    </tr>
    <tr style="background:#f8f9fa;">
      <td style="padding:10px 10px;border:1px solid #e0e0e0;">数据</td>
      <td style="padding:10px 10px;text-align:center;border:1px solid #e0e0e0;">数据</td>
    </tr>
  </tbody>
</table>
```

### b) 极简水平线
```html
<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;border-top:2px solid {{主色}};border-bottom:2px solid {{主色}};">
  <thead>
    <tr style="border-bottom:1px solid #e0e0e0;">
      <td style="padding:12px 10px;text-align:left;font-weight:600;">列1</td>
      <td style="padding:12px 10px;text-align:center;font-weight:600;">列2</td>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid #f0f0f0;">
      <td style="padding:10px 10px;">数据</td>
      <td style="padding:10px 10px;text-align:center;">数据</td>
    </tr>
  </tbody>
</table>
```

---

## 10. 列表样式

**配置项**：
- 列表符号类型：圆点 ▸ | 方块 ■ | 对勾 ✓ | 数字 1.2.3. | 中文数字 | 自定义 emoji | 空心圆 ○
- 符号颜色：`color`
- 行距：`line-height`
- 项间距：`padding` / `margin`
- 是否有底部分隔线

> **移动优先**：列表 `padding-left` 必须 ≥ 32px，确保编号/符号在移动端不被压缩。自定义标签字号 ≥ 14px，标签尺寸 ≥ 24px。

**CSS 模板**：

### a) 实心圆点
```html
<ul style="padding-left:0;margin:16px 0;list-style:none;">
  <li style="padding:8px 0 8px 24px;font-size:17px;color:#444;line-height:1.8;position:relative;">
    <span style="display:inline-block;width:8px;height:8px;background:{{主色}};border-radius:50%;position:absolute;left:4px;top:16px;"></span>列表项
  </li>
</ul>
```

### b) 方块
```html
<ul style="padding-left:0;margin:16px 0;list-style:none;">
  <li style="padding:8px 0 8px 24px;font-size:17px;color:#444;line-height:1.8;position:relative;">
    <span style="display:inline-block;width:8px;height:8px;background:{{主色}};position:absolute;left:4px;top:16px;"></span>列表项
  </li>
</ul>
```

### c) 对勾
```html
<ul style="padding-left:0;margin:16px 0;list-style:none;">
  <li style="padding:8px 0 8px 28px;font-size:17px;color:#444;line-height:1.8;position:relative;">
    <span style="color:{{主色}};font-weight:700;position:absolute;left:0;top:8px;font-size:16px;">✓</span>列表项
  </li>
</ul>
```

### d) 数字序号
```html
<ol style="padding-left:0;margin:16px 0;list-style:none;">
  <li style="padding:8px 0 8px 36px;font-size:17px;color:#444;line-height:1.8;position:relative;">
    <span style="position:absolute;left:0;top:8px;width:24px;height:24px;background:{{主色}};color:#fff;border-radius:50%;text-align:center;line-height:24px;font-size:14px;font-weight:700;">1</span>列表项
  </li>
</ol>
```

### e) 中文数字
```html
<ol style="padding-left:0;margin:16px 0;list-style:none;">
  <li style="padding:8px 0 8px 48px;font-size:17px;color:#444;line-height:1.8;position:relative;">
    <span style="position:absolute;left:0;top:8px;background:{{主色}};color:#fff;padding:4px 10px;border-radius:4px;font-size:14px;">第一步</span>列表项
  </li>
</ol>
```

### f) 原生列表（推荐移动端使用）
```html
<ul style="font-size:17px;color:#444;line-height:2;padding-left:32px;margin:16px 0;">
  <li style="margin-bottom:8px;">列表项</li>
</ul>

<ol style="font-size:17px;color:#444;line-height:2;padding-left:32px;list-style-type:decimal;margin:16px 0;">
  <li style="margin-bottom:8px;">列表项</li>
</ol>
```

---

## 配置选项速查表

在自定义模式中，列出以下选项供用户逐项选择：

| 序号 | 排版要素 | 选项数量 | 关键参数 |
|------|----------|----------|----------|
| 1 | 正文字体大小 | 5 | 字体族、字号、行高、颜色 |
| 2 | 二级标题装饰 | 7 | 左侧色条/底部横线/背景色块/编号/图标/全宽色带/双线 |
| 3 | 段落间距样式 | 5 | 无/虚线/渐变/三点/SVG波形/符号 |
| 4 | 头部样式 | 3 | 简约/装饰/卡片 |
| 5 | 底部样式 | 3 | 标准/卡片/左右布局 |
| 6 | 划重点样式 | 4 | 荧光笔/加粗变色/背景色块/下划线 |
| 7 | 引用块样式 | 3 | 左色条/全边框/引号 |
| 8 | 代码样式 | 4 | VS Code/浅色/Monokai/Dracula |
| 9 | 表格样式 | 2 | 全边框/极简水平线 |
| 10 | 列表样式 | 5 | 圆点/方块/对勾/数字/中文数字 |
