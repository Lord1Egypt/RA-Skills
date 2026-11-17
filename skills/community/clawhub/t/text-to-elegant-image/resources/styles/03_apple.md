## 3. Notion / Apple 质感风 (Apple Premium)

适用：效率工具、复盘总结、方法论分享。

**升级亮点（v2）：** `backdrop-filter` 毛玻璃卡片；window controls 加高光渐变；highlight 块加彩色渐变左条；tag 加 hover 感微阴影。

```css
:root {
    --bg-color: #F5F5F7;
    --card-bg: #FFFFFF;
    --text-main: #1D1D1F;
    --text-muted: #6E6E73;
    --accent: #0066CC;
    --border: rgba(0,0,0,0.06);
}
body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0; padding: 0;
    line-height: 1.7;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 40px 24px;
    background: var(--t2e-surface, #FFFFFF);
    border: 1px solid var(--t2e-border, rgba(0,0,0,0.08));
    border-radius: 20px;
    box-shadow: 0 2px 24px rgba(0,0,0,0.06);
}
.apple-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 18px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
    padding: 28px 30px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.8);
}
.window-controls {
    display: flex; gap: 8px; margin-bottom: 20px;
    align-items: center;
}
/* 升级：window controls 加高光渐变 */
.dot { width: 12px; height: 12px; border-radius: 50%; position: relative; }
.dot::after {
    content: '';
    position: absolute;
    top: 1px; left: 2px;
    width: 6px; height: 4px;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
}
.dot-red { background: radial-gradient(circle at 35% 35%, #FF7F79, #FF5F56); }
.dot-yellow { background: radial-gradient(circle at 35% 35%, #FFD76B, #FFBD2E); }
.dot-green { background: radial-gradient(circle at 35% 35%, #5DD35D, #27C93F); }
.main-title {
    font-size: 1.8em;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    word-break: keep-all;
}
.subtitle {
    color: var(--text-muted);
    font-size: 0.9em;
}
.section-title {
    font-size: 0.75em;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 24px 0 8px;
}
/* 升级：highlight 加彩色渐变左条 */
.highlight {
    background: rgba(0,102,204,0.06);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    color: var(--text-main);
    font-weight: 500;
    margin: 12px 0;
    position: relative;
    overflow: hidden;
}
.highlight::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, #0066CC, #00AAFF);
}
.tag {
    display: inline-block;
    background: rgba(0,0,0,0.05);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.8em;
    color: var(--text-muted);
    margin: 3px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
}
p, .body-text { word-break: keep-all; overflow-wrap: break-word; }
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78em;
    padding-top: 16px;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #0066CC;
    --t2e-accent-soft: rgba(0,102,204,0.08);
    --t2e-bg: #F5F5F7;
    --t2e-surface: #FFFFFF;
    --t2e-text: #1D1D1F;
    --t2e-muted: #6E6E73;
    --t2e-border: rgba(0,0,0,0.08);
}
```
