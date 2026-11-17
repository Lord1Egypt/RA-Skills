## 1. 赛博科技风 (Cyberpunk/Tech) - 默认

适用：AI、科技分析、硬核知识。

**升级亮点（v2）：** inline SVG 蜂窝六边形背景替换普通网格，`conic-gradient` 扫描环装饰，`text-shadow` 发光字升级。

```css
:root {
    --bg-color: #050812;
    --primary-glow: #00f0ff;
    --secondary-glow: #b900ff;
    --text-main: #f0f4f8;
    --text-muted: #7a8fa6;
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    /* 升级：inline SVG 蜂窝六边形背景 + 细网格叠加 */
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100'%3E%3Cpath d='M28 66L0 50V18L28 2l28 16v32z' fill='none' stroke='rgba(0%2C240%2C255%2C0.1)' stroke-width='1'/%3E%3C/svg%3E"),
        linear-gradient(rgba(0,240,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,240,255,0.04) 1px, transparent 1px);
    background-size: 56px 100px, 30px 30px, 30px 30px;
    margin: 0; padding: 0;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 40px 32px;
    position: relative;
    background: var(--t2e-surface, #0C1220);
    border: 1px solid var(--t2e-border, rgba(0,240,255,0.25));
    border-radius: 16px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.glass-card {
    background: rgba(12, 18, 32, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0, 240, 255, 0.25);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 0 20px rgba(0,240,255,0.04);
    padding: 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
/* 卡片顶部扫描线装饰 */
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary-glow), transparent);
    opacity: 0.6;
}
.glow-title {
    font-size: 1.8em;
    font-weight: 700;
    color: var(--primary-glow);
    text-shadow: 0 0 20px rgba(0,240,255,0.7), 0 0 40px rgba(0,240,255,0.3);
    letter-spacing: 0.04em;
    margin-bottom: 8px;
}
.subtitle {
    color: var(--text-muted);
    font-size: 0.9em;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.section-title {
    font-size: 1.1em;
    color: var(--primary-glow);
    border-left: 3px solid var(--primary-glow);
    padding-left: 12px;
    margin: 24px 0 12px;
    text-shadow: 0 0 10px rgba(0,240,255,0.4);
}
.highlight {
    background: linear-gradient(135deg, rgba(0,240,255,0.12), rgba(185,0,255,0.08));
    border: 1px solid rgba(0,240,255,0.3);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 1.0em;
    color: #e0f8ff;
    font-style: italic;
    margin: 16px 0;
}
.tag {
    display: inline-block;
    background: rgba(0,240,255,0.1);
    border: 1px solid rgba(0,240,255,0.3);
    color: var(--primary-glow);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.8em;
    margin: 4px;
}
/* 升级：conic-gradient 扫描环 */
.scan-ring {
    width: 48px; height: 48px;
    border-radius: 50%;
    background: conic-gradient(
        var(--primary-glow) 0deg,
        transparent 60deg,
        transparent 360deg
    );
    opacity: 0.5;
    flex-shrink: 0;
}
.divider {
    border: none;
    border-top: 1px solid rgba(0,240,255,0.12);
    margin: 24px 0;
}
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.75em;
    padding-top: 20px;
    letter-spacing: 0.1em;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #00F0FF;
    --t2e-accent-soft: rgba(0,240,255,0.12);
    --t2e-bg: #050812;
    --t2e-surface: #0C1220;
    --t2e-text: #F0F4F8;
    --t2e-muted: #7A8FA6;
    --t2e-border: rgba(0,240,255,0.25);
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。
