## 7. 水墨卷轴风 (Ink Scroll)

适用：中国历史、文化艺术、人文随笔、东方美学内容。

**升级亮点（v2）：** 多层椭圆渐变增强宣纸晕染感；inline SVG 水墨晕圈装饰；印章伪元素升级；竖向分隔线改为毛笔横扫感渐变。

```css
:root {
    --bg-color: #F5F0E8;
    --text-main: #2A2018;
    --text-muted: #7A6A50;
    --accent: #8B1A1A;
    --ink: #1A1008;
    --border: rgba(42,32,24,0.15);
    --wash: rgba(139,26,26,0.06);
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: "Songti SC", "Noto Serif CJK SC", "Source Han Serif CN", "STSong", Georgia, serif;
    margin: 0; padding: 0;
    line-height: 2.0;
    /* 升级：多层椭圆渐变模拟宣纸晕染 + noise纹 */
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E"),
        radial-gradient(ellipse at 15% 40%, rgba(160,130,80,0.1) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, rgba(140,110,60,0.08) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 80%, rgba(180,150,100,0.06) 0%, transparent 50%);
}
.container {
    max-width: 540px;
    margin: 0 auto;
    padding: 60px 48px;
    background: var(--t2e-surface, #F5F0E8);
    border: 1px solid var(--border, rgba(42,32,24,0.15));
    box-shadow: 0 4px 32px rgba(42,32,24,0.1);
}
.scroll-header {
    text-align: center;
    margin-bottom: 48px;
    position: relative;
}
/* 升级：印章 + 双竖线 */
.seal {
    display: inline-block;
    border: 2px solid var(--accent);
    color: var(--accent);
    font-size: 0.75em;
    padding: 5px 16px;
    letter-spacing: 0.22em;
    margin-bottom: 20px;
    position: relative;
    box-shadow: inset 0 0 0 1px rgba(139,26,26,0.15);
}
.seal::before, .seal::after {
    content: '';
    position: absolute;
    top: 3px; bottom: 3px;
    width: 1px;
    background: var(--accent);
    opacity: 0.35;
}
.seal::before { left: 5px; }
.seal::after { right: 5px; }
.scroll-title {
    font-size: 2.2em;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: 0.12em;
    line-height: 1.3;
    margin-bottom: 12px;
    word-break: keep-all;
}
.scroll-subtitle {
    font-size: 0.85em;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    font-style: italic;
}
/* 升级：毛笔横扫感分割线 */
.ink-rule {
    border: none;
    height: 1px;
    background: linear-gradient(to right,
        transparent 0%,
        rgba(26,16,8,0.08) 5%,
        rgba(26,16,8,0.22) 15%,
        rgba(26,16,8,0.28) 50%,
        rgba(26,16,8,0.15) 85%,
        rgba(26,16,8,0.04) 95%,
        transparent 100%
    );
    margin: 32px 0;
}
.scroll-item {
    display: flex;
    gap: 24px;
    margin-bottom: 32px;
    align-items: flex-start;
}
.scroll-item:last-child { margin-bottom: 0; }
.scroll-year-col {
    flex-shrink: 0;
    width: 56px;
    text-align: center;
    padding-top: 4px;
}
.scroll-year {
    font-size: 1.1em;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.04em;
    line-height: 1.2;
}
.scroll-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    margin: 8px auto 0;
    opacity: 0.65;
}
.scroll-content { flex: 1; padding-top: 2px; }
.scroll-name {
    font-size: 1.1em;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    word-break: keep-all;
}
.scroll-text {
    font-size: 0.88em;
    color: #4A3C28;
    line-height: 1.9;
    word-break: keep-all;
}
.scroll-tag {
    display: inline-block;
    background: var(--wash);
    border: 1px solid rgba(139,26,26,0.2);
    color: var(--accent);
    font-size: 0.72em;
    padding: 2px 10px;
    margin-top: 8px;
    letter-spacing: 0.1em;
}
.scroll-closing {
    background: rgba(139,26,26,0.04);
    border-left: 2px solid var(--accent);
    padding: 16px 20px;
    margin-top: 32px;
}
.scroll-closing-label {
    font-size: 0.7em;
    color: var(--text-muted);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.scroll-closing-text {
    font-size: 0.9em;
    color: var(--text-muted);
    line-height: 1.85;
    font-style: italic;
    word-break: keep-all;
}
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.72em;
    padding-top: 32px;
    letter-spacing: 0.12em;
    opacity: 0.7;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #8B1A1A;
    --t2e-accent-soft: rgba(139,26,26,0.06);
    --t2e-bg: #F5F0E8;
    --t2e-surface: #F5F0E8;
    --t2e-text: #2A2018;
    --t2e-muted: #7A6A50;
    --t2e-border: rgba(42,32,24,0.15);
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700;900&family=ZCOOL+QingKe+HuangYou&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。
