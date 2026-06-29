---
name: wechat-article-html
description: 将 Markdown 文章转换为微信公众号兼容的纯 HTML 格式。当用户要求"转成微信格式"、"生成公众号文章 HTML"、"排版到微信草稿箱"、"微信粘贴格式"时触发。输出带内联样式的纯 HTML，微信编辑器可直接渲染，无需额外适配。支持标题、段落、列表、粗体、行内代码、表格、引用块、代码块、配图的完整转换。
---

# 微信公众号文章 HTML 转换器

将 Markdown 源文件转换为微信公众号编辑器兼容的纯 HTML 格式。

## 转换规则（强制）

所有 Markdown 语法必须转为带内联样式的 HTML 标签。禁止输出任何残留 Markdown 语法。

### 标题映射

| Markdown | HTML |
|----------|------|
| `# 标题` | `<h1 style="margin:1.5em 0 0.5em;font-weight:700;">标题</h1>` |
| `## 标题` | `<h2 style="margin:1.5em 0 0.5em;font-weight:700;">标题</h2>` |
| `### 标题` | `<h3 style="margin:1.5em 0 0.5em;font-weight:700;">标题</h3>` |
| `#### 标题` | `<h4 style="margin:1.5em 0 0.5em;font-weight:700;">标题</h4>` |

### 正文段落

```
<p style="margin:10px 0;font-size:14px;line-height:1.8;">内容</p>
```

### 列表

```html
<ul style="margin:10px 0;padding-left:24px;">
  <li style="margin:4px 0;">内容</li>
</ul>
```

有序列表用 `<ol style="margin:10px 0;padding-left:24px;">`。

### 粗体

`**文字**` → `<strong>文字</strong>`

### 行内代码

`` `代码` `` → `<code style="background:#f6f8fa;color:#005cc5;padding:1px 4px;border-radius:3px;font-size:0.9em;">代码</code>`

### 表格

```html
<table style="border-collapse:collapse;width:100%;font-size:14px;line-height:1.6;margin:10px 0;">
  <thead>
    <tr>
      <th style="background:#f6f8fa;border:1px solid #d0d7de;padding:6px 12px;text-align:left;font-weight:600;">表头</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #d0d7de;padding:6px 12px;">内容</td>
    </tr>
  </tbody>
</table>
```

### 引用块

```html
<blockquote style="background:#f6f8fa;border-left:4px solid #0969da;margin:16px 0;padding:12px 20px;color:#1f2328;">
  <p style="margin:0;font-size:14px;line-height:1.8;">引用内容</p>
</blockquote>
```

### 代码块

代码块使用 `<section>` + 每行一个 `<p>` 的结构（微信编辑器会吞掉 `<pre>`/`<code>` 的空白和换行）：

```html
<section style="background:#282c34;color:#abb2bf;border-radius:6px;padding:12px 16px;margin:10px 0;overflow-x:auto;">
  <p style="margin:0;padding:0;font-size:14px;line-height:1.6;">第一行代码</p>
  <p style="margin:0;padding:0;font-size:14px;line-height:1.6;">第二行代码</p>
</section>
```

#### 代码块语法高亮配色（GitHub Dark × #282c34）

| 元素 | CSS color 值 |
|------|-------------|
| 基础文本 | `#ffffff` |
| 关键字 | `#ff7b72` |
| 函数名 | `#d2a8ff` |
| 字符串 | `#a5d6ff` |
| 数字 | `#79c0ff` |
| 注释 | `#8b949e` |
| 内置命令 | `#7ee787` |
| 类名 | `#f0883e` |

行首缩进用 `&nbsp;` 替换空格。注释行单独加 `color:#8b949e`。

### 配图

```html
<figure style="text-align:center;margin:20px 0;">
  <img src="CDN_URL" style="max-width:100%;border-radius:8px;" alt="图片说明">
  <figcaption style="margin-top:8px;font-size:13px;color:#666;text-align:center;"></figcaption>
</figure>
```

配图位置：引言 blockquote 后面。

### 链接

`[文字](url)` → 纯文本「文字」（去掉链接语法，保留文字）

### 删除项

- YAML front matter（`---` 开头的元数据块）
- `---` 分隔线
- 本地图片路径（替换为 CDN URL）

## 工作流程

1. 读取源 Markdown 文件
2. 按上述规则逐行转换为 HTML
3. `<section>` 代码块原样保留（已是正确 HTML）
4. 配图用 `<figure>` 包裹，CDN URL 替换本地路径
5. 输出 `*_for_paste.html` 文件，供用户复制粘贴到微信草稿箱

## 关键字上色（可选）

用户可指定关键字上色方案。默认配色：

| 颜色 | 色值 | 用途 |
|------|------|------|
| 🔴 红 | `#d73a49` | 核心概念 |
| 🟣 紫 | `#6f42c1` | 工具/命令 |
| 🔵 蓝 | `#005cc5` | 参数/文件名 |
| 🟠 橙 | `#e36209` | 关键数值/信号 |

## 注意事项

- 禁止使用 `<pre>` / `<code>` 包裹代码块（微信会吞掉空白）
- 每行代码必须是独立的 `<p>` 元素
- 中文内容原样保留，不做任何修改或扩展
- 输出文件编码必须为 UTF-8（`ensure_ascii=False`）
