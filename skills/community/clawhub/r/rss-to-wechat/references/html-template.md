# RSS to WeChat HTML 模板

## 基础结构

```html
<section style="background:#f5f5f0;padding:20px 15px;">

<!-- 头部品牌 Logo -->
<section style="background:#c41e3a;padding:20px 25px;margin-bottom:15px;border-radius:10px;text-align:center;">
<p style="display:flex;align-items:center;justify-content:center;gap:15px;margin-bottom:8px;">
<svg width="50" height="50" viewBox="0 0 140 140" style="display:inline-block;">
<circle cx="70" cy="70" r="70" fill="rgba(255,255,255,0.15)"/>
<path d="M40 110 L70 20 L100 110 M48 85 L92 85" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="70" cy="25" r="6" fill="#fff"/>
<line x1="70" y1="40" x2="70" y2="110" stroke="#fff" stroke-width="8" stroke-linecap="round"/>
</svg>
<span style="font-size:32px;font-weight:900;color:#fff;letter-spacing:4px;">AI晚知道</span>
</p>
<p style="font-size:13px;color:rgba(255,255,255,0.85);font-style:italic;font-family:Georgia,serif;">"All the AI News That's Fit to Read"</p>
</section>

<!-- 日期栏 -->
<section style="background:#fff;padding:15px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);text-align:center;">
<p style="font-size:14px;color:#666;border-bottom:1px solid #eee;padding-bottom:10px;">{{DATE}}</p>
<p style="font-size:12px;color:#999;margin-top:8px;">精选</p>
</section>

<!-- 标题 -->
<section style="background:#fff;padding:25px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
<p style="font-size:24px;font-weight:bold;color:#c41e3a;line-height:1.4;margin-bottom:12px;">{{TITLE}}</p>
<p style="font-size:13px;color:#999;">来源：{{AUTHOR}} | 发布时间：{{PUBLISHED}}</p>
</section>

<!-- 核心观点 -->
<section style="background:#fff;padding:20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
<p style="font-size:11px;color:#c41e3a;letter-spacing:2px;border-bottom:1px solid #eee;padding-bottom:8px;margin-bottom:12px;">核心观点 · TL;DR</p>
<p style="font-size:14px;color:#444;line-height:1.8;border-left:3px solid #c41e3a;padding-left:12px;">
{{SUMMARY}}
</p>
</section>

<!-- 详细内容 -->
<section style="background:#fff;padding:20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
<p style="font-size:11px;color:#c41e3a;letter-spacing:2px;border-bottom:1px solid #eee;padding-bottom:8px;margin-bottom:12px;">详细内容 · DETAILS</p>

{{CONTENT_SECTIONS}}

</section>

<!-- 原文链接 -->
<section style="background:#fff;padding:15px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);text-align:center;">
<p style="font-size:12px;color:#999;">原文链接</p>
<p style="font-size:11px;color:#1a5fb4;word-break:break-all;margin-top:5px;">{{URL}}</p>
</section>

</section>
```

## 内容段落模板

### 标题 + 段落
```html
<p style="font-size:18px;font-weight:bold;color:#1a1a1a;margin-bottom:10px;margin-top:20px;">{{SECTION_TITLE}}</p>

<p style="font-size:14px;color:#444;line-height:1.8;margin-bottom:15px;">
{{PARAGRAPH_TEXT}}
</p>
```

### 要点列表
```html
<p style="background:#fafafa;padding:10px;border-radius:4px;margin-bottom:8px;">
<span style="font-size:13px;color:#666;">• {{POINT_TEXT}}</span>
</p>
```

### 高亮框
```html
<p style="background:#f0f7ff;padding:12px;border-radius:4px;margin-bottom:10px;border-left:3px solid #1a5fb4;">
<span style="font-size:14px;font-weight:bold;color:#1a5fb4;">{{HIGHLIGHT_TITLE}}</span><br/>
<span style="font-size:13px;color:#1a5fb4;">{{HIGHLIGHT_TEXT}}</span>
</p>
```

### 警告框
```html
<p style="background:#fff8f8;border:1px solid #ffe0e0;padding:12px;border-radius:4px;margin-bottom:15px;">
<span style="color:#c41e3a;font-weight:bold;">⚠️ {{WARNING_TITLE}}</span><br/>
<span style="font-size:13px;color:#666;">{{WARNING_TEXT}}</span>
</p>
```

### 引用
```html
<p style="background:#fafafa;padding:15px;border-left:3px solid #c41e3a;margin:15px 0;font-style:italic;color:#666;">
"{{QUOTE_TEXT}}"
</p>
```

## 样式规范

### 颜色
- 主色：`#c41e3a`（红色）
- 背景：`#f5f5f0`（米色）
- 文字：`#444`（深灰）
- 次要文字：`#666`、`#999`
- 高亮：`#1a5fb4`（蓝色）

### 字号
- 大标题：24px
- 章节标题：18px
- 小标题：16px
- 正文：14px
- 辅助文字：13px、12px、11px

### 间距
- 段落间距：`margin-bottom:15px`
- 小间距：`margin-bottom:10px`
- 大间距：`margin-top:20px`

## 注意事项

1. **禁止使用**：
   - `<div>` 标签（用 `<section>` 或 `<p>`）
   - `class` 和 `id` 属性
   - 相对链接 `<a href="/...">`
   - 外部 CSS

2. **必须使用**：
   - 内联样式 `style="..."`
   - `<strong>` 和 `<em>` 标签
   - `<br/>` 换行
   - 完整 URL

3. **内容要求**：
   - 核心观点简洁明了（1-2 句话）
   - 详细内容分段落，每段不超过 3-4 句
   - 使用要点列表增强可读性
   - 适当使用高亮框和警告框
