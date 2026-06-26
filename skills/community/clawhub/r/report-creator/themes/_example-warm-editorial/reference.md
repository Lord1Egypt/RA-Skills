# Warm Editorial — 风格参考

温暖、沉稳、有质感。灵感来自高质量印刷出版物——米白纸张、棕赭墨迹、宽松的版心。适合研究报告、品牌白皮书、年度复盘。

---

## Colors / 配色

```css
:root {
  --primary:      #92400E;   /* 深琥珀棕，用于标题线、链接、强调 */
  --primary-light:#FEF3C7;   /* 淡琥珀，用于 KPI 卡片背景 */
  --accent:       #B45309;   /* 暖橙，用于高亮数字 */
  --bg:           #FDFAF6;   /* 暖米白，页面背景 */
  --surface:      #FFFFFF;   /* 纯白，卡片背景 */
  --text:         #1C1917;   /* 暖近黑，正文 */
  --text-muted:   #78716C;   /* 暖中灰，次要文字、元信息 */
  --border:       #E7E5E4;   /* 暖浅灰，边框分割线 */
  --success:      #065F46;
  --warning:      #92400E;
  --danger:       #991B1B;
}
```

**禁止使用：** 冷灰（#888）、纯蓝（#2563EB）、霓虹色、深色背景

---

## Typography / 字体

标题使用带衬线的优雅字体，正文使用可读性强的无衬线字体。

```html
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
```

```css
--font-sans: 'Source Sans 3', 'PingFang SC', system-ui, sans-serif;
--font-serif: 'Lora', 'Noto Serif SC', Georgia, serif;
/* h1/h2 使用 font-family: var(--font-serif) */
```

---

## Layout / 布局

宽松留白，阅读友好。

```css
--radius: 4px;   /* 数据元素用锐角 */
/* 卡片用 border-radius: 8px */
/* 报告最大宽度 900px，左右 padding 充足 */
```

---

## Best For / 适用场景

研究报告 · 品牌白皮书 · 年度复盘 · 内部洞察文档 · 任何需要"专业而不冷漠"气质的报告
