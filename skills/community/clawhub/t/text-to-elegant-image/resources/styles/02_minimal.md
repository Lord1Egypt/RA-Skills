## 2. 极简优雅风 (Minimalist Light)

适用：文学随笔、日记、人文知识。

**升级亮点（v2）：** 背景加 inline SVG `feTurbulence` noise filter 宣纸微噪点；分割线改为渐变淡出式；引用块加左侧渐变色条。

> **时间轴布局注意**：`.tl-left` 必须设置 `padding-right: 16px`，`.dot` 使用 `right: 0` 定位，避免圆点与年份文字重叠。正文加 `word-break: keep-all` 防止中文在尴尬位置断行。

```css
:root {
    --bg-color: #FDFDFD;
    --text-main: #2C2C2C;
    --text-muted: #8E8E8E;
    --accent: #D32F2F;
    --border: #EAEAEA;
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: "Songti SC", "Noto Serif CJK SC", "Source Han Serif CN", Georgia, serif;
    margin: 0; padding: 0;
    line-height: 1.9;
    /* 升级：inline SVG noise filter 微噪点宣纸感 */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23noise)' opacity='0.025'/%3E%3C/svg%3E");
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 60px 40px;
    background: var(--t2e-surface, #FFFFFF);
    border: 1px solid var(--t2e-border, #EAEAEA);
    border-radius: 18px;
    box-shadow: 0 2px 24px rgba(0,0,0,0.04);
}
.title-section {
    text-align: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 48px;
    margin-bottom: 40px;
}
.main-title {
    font-size: 2.2em;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
    word-break: keep-all;
}
.subtitle {
    color: var(--text-muted);
    font-size: 0.9em;
    letter-spacing: 0.12em;
}
.quote-card {
    border-left: 3px solid var(--accent);
    padding: 16px 24px;
    background: linear-gradient(to right, rgba(211,47,47,0.04), transparent);
    font-style: italic;
    color: #555;
    margin: 30px 0;
    border-radius: 0 8px 8px 0;
}
.section-title {
    font-size: 1.15em;
    font-weight: 700;
    margin: 32px 0 12px;
    color: var(--text-main);
    word-break: keep-all;
}
/* 升级：渐变淡出分割线 */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--border) 20%, var(--border) 80%, transparent);
    margin: 32px 0;
}
.divider::before { content: none; }
.divider-dot {
    text-align: center;
    color: var(--text-muted);
    margin: 32px 0;
    letter-spacing: 0.3em;
    font-size: 0.85em;
}
.divider-dot::before { content: "· · ·"; }
p, .body-text {
    word-break: keep-all;
    overflow-wrap: break-word;
}
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.8em;
    padding-top: 48px;
    border-top: 1px solid var(--border);
    margin-top: 48px;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #D32F2F;
    --t2e-accent-soft: rgba(211,47,47,0.08);
    --t2e-bg: #FDFDFD;
    --t2e-surface: #FFFFFF;
    --t2e-text: #2C2C2C;
    --t2e-muted: #8E8E8E;
    --t2e-border: #EAEAEA;
}
```
