## 6. Bloomberg 终端风 (Bloomberg Terminal)

适用：数据报告、指标对比、金融分析、科技数字内容。

**升级亮点（v2）：** 年份数字加橙色左侧光条；发光文字 `text-shadow` 增强；加扫描线背景纹理；tag 加渐变边框。

```css
:root {
    --bg-color: #0A0A0A;
    --panel-bg: #111111;
    --text-main: #FF6B00;
    --text-white: #E8E8E8;
    --text-muted: #555555;
    --accent: #FF6B00;
    --accent-dim: rgba(255,107,0,0.12);
    --green: #00CC44;
    --border: rgba(255,107,0,0.18);
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: "Courier New", "Courier", "Lucida Console", monospace;
    margin: 0; padding: 0;
    line-height: 1.6;
    /* 升级：CRT扫描线纹理 */
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.15) 2px,
        rgba(0,0,0,0.15) 3px
    );
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 32px 28px;
    background: var(--t2e-surface, #111111);
    border: 1px solid var(--border, rgba(255,107,0,0.18));
    box-shadow: 0 0 32px rgba(255,107,0,0.06), 0 8px 32px rgba(0,0,0,0.4);
}
.terminal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.terminal-id { font-size: 0.75em; color: var(--text-muted); letter-spacing: 0.1em; }
.terminal-title {
    font-size: 0.85em;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-shadow: 0 0 8px rgba(255,107,0,0.5);
}
.terminal-status { font-size: 0.72em; color: var(--green); letter-spacing: 0.08em; }

.bb-headline {
    font-size: 1.4em;
    font-weight: 700;
    color: var(--text-white);
    letter-spacing: 0.04em;
    line-height: 1.3;
    margin-bottom: 4px;
    text-transform: uppercase;
    word-break: keep-all;
}
.bb-subhead {
    font-size: 0.78em;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    margin-bottom: 20px;
}
.bb-rule { border: none; border-top: 1px solid var(--border); margin: 16px 0; }

/* 升级：年份加橙色左侧光条 */
.bb-row {
    display: flex;
    align-items: flex-start;
    gap: 0;
    padding: 12px 0 12px 12px;
    border-bottom: 1px solid rgba(255,107,0,0.08);
    border-left: 2px solid rgba(255,107,0,0.3);
    margin-left: -12px;
    margin-bottom: 4px;
}
.bb-row:last-child { border-bottom: none; }
.bb-num {
    flex-shrink: 0;
    width: 80px;
    font-size: 1.6em;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.02em;
    line-height: 1;
    padding-top: 2px;
    /* 升级：数字发光 */
    text-shadow: 0 0 12px rgba(255,107,0,0.6), 0 0 24px rgba(255,107,0,0.2);
}
.bb-right { flex: 1; }
.bb-label {
    font-size: 0.85em;
    color: var(--text-white);
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.bb-desc {
    font-size: 0.78em;
    color: var(--text-muted);
    line-height: 1.65;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    word-break: keep-all;
}
/* 升级：tag 加渐变边框效果 */
.bb-tag {
    display: inline-block;
    background: var(--accent-dim);
    color: var(--accent);
    font-size: 0.68em;
    padding: 1px 8px;
    margin-top: 6px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid var(--accent);
    box-shadow: 0 0 6px rgba(255,107,0,0.2);
}
.bb-analysis {
    background: var(--panel-bg);
    border: 1px solid var(--border);
    padding: 14px 16px;
    margin-top: 16px;
}
.bb-analysis-label {
    font-size: 0.68em;
    color: var(--accent);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 8px;
    text-shadow: 0 0 6px rgba(255,107,0,0.4);
}
.bb-analysis-text {
    font-size: 0.78em;
    color: var(--text-muted);
    line-height: 1.7;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    word-break: keep-all;
}
.bb-analysis-text strong { color: var(--text-white); }
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.68em;
    padding-top: 16px;
    letter-spacing: 0.12em;
    font-family: "Courier New", monospace;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #FF6B00;
    --t2e-accent-soft: rgba(255,107,0,0.12);
    --t2e-bg: #0A0A0A;
    --t2e-surface: #111111;
    --t2e-text: #E8E8E8;
    --t2e-muted: #777777;
    --t2e-border: rgba(255,107,0,0.18);
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。
