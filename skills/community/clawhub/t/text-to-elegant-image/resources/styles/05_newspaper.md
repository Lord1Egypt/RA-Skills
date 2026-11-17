## 5. 报纸/杂志风 (Newspaper)

适用：历史事件、时间轴、人物传记、深度叙事内容。

**升级亮点（v2）：** 背景加 inline SVG 细点阵纹（铅字印刷颗粒感）；报头加双线装饰；时间轴年份列加边框阴影；标签统一大写。

```css
:root {
    --bg-color: #F0EDE4;
    --text-main: #1A1A1A;
    --text-muted: #555550;
    --accent: #1A1A1A;
    --border: #C8C4BA;
    --rule: #1A1A1A;
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: "Georgia", "Songti SC", "Noto Serif CJK SC", serif;
    margin: 0; padding: 0;
    line-height: 1.8;
    /* 升级：铅字印刷颗粒纹 */
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4'%3E%3Crect width='1' height='1' x='0' y='0' fill='rgba(0%2C0%2C0%2C0.04)'/%3E%3Crect width='1' height='1' x='2' y='2' fill='rgba(0%2C0%2C0%2C0.03)'/%3E%3C/svg%3E");
    background-size: 4px 4px;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 48px 36px;
    background: var(--t2e-surface, #F0EDE4);
    border: 1px solid var(--rule, #1A1A1A);
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
/* 顶部报头 */
.masthead {
    text-align: center;
    border-top: 4px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    padding: 12px 0 10px;
    margin-bottom: 4px;
}
.masthead-date {
    font-size: 0.72em;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.masthead-title {
    font-size: 2.6em;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.1;
    font-family: "Georgia", serif;
    word-break: keep-all;
}
.masthead-sub {
    font-size: 0.82em;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    margin-top: 6px;
    font-style: italic;
}
/* 升级：双线分割 */
.rule-double {
    border: none;
    border-top: 3px double var(--rule);
    margin: 8px 0 20px;
}
.lede {
    font-size: 1.1em;
    font-style: italic;
    color: var(--text-muted);
    border-left: 3px solid var(--rule);
    padding-left: 16px;
    margin: 0 0 24px;
    line-height: 1.7;
    word-break: keep-all;
}
/* 时间轴节点 */
.np-item {
    display: flex;
    gap: 0;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 18px;
}
.np-item:last-child { border-bottom: none; padding-bottom: 0; }
/* 升级：年份列加框感 */
.np-year-col {
    flex-shrink: 0;
    width: 72px;
    padding-right: 16px;
    border-right: 2px solid var(--rule);
    margin-right: 20px;
    padding-top: 2px;
}
.np-year {
    font-size: 1.5em;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.02em;
}
.np-era {
    font-size: 0.68em;
    color: var(--text-muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.np-content {}
.np-headline {
    font-size: 1.1em;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 6px;
    letter-spacing: 0.01em;
    word-break: keep-all;
}
.np-body {
    font-size: 0.86em;
    color: #3A3A3A;
    line-height: 1.75;
    word-break: keep-all;
}
.np-tag {
    display: inline-block;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.7em;
    padding: 1px 7px;
    margin-top: 7px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.editorial {
    border: 1px solid var(--rule);
    padding: 16px 20px;
    margin-top: 24px;
    background: rgba(0,0,0,0.03);
}
.editorial-label {
    font-size: 0.68em;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: var(--text-muted);
}
.editorial-text {
    font-size: 0.88em;
    font-style: italic;
    line-height: 1.75;
    color: #333;
    word-break: keep-all;
}
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.72em;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    margin-top: 24px;
    letter-spacing: 0.08em;
    font-style: italic;
}
```

**报纸风使用要点：**
- 背景用泛黄纸张色 `#F0EDE4` + 极淡点阵纹（铅字颗粒感）
- 顶部做报头（masthead）：刊名大字 + 副标题 + 双线分割
- 时间轴：年份列 `border-right: 2px solid` 做竖线，右侧内容 `margin-left` 留间距
- 全程黑/灰/米白，靠字重和字号建立层次，禁用彩色块


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #8B1A1A;
    --t2e-accent-soft: rgba(139,26,26,0.06);
    --t2e-bg: #F0EDE4;
    --t2e-surface: #F0EDE4;
    --t2e-text: #1A1A1A;
    --t2e-muted: #555550;
    --t2e-border: #C8C4BA;
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;900&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。
