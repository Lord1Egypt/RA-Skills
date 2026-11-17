## 8. 蒸汽朋克风 (Steampunk)

适用：工业历史、科技跃迁、机械美学、复古科技内容。纯CSS实现：齿轮、压力表、铜管、铆钉边框，无外部图片、无emoji。

```css
:root {
    --bg: #1A1008;
    --copper: #B87333;
    --copper-light: #D4944A;
    --copper-dark: #7A4A1A;
    --brass: #C8A830;
    --brass-light: #E8C840;
    --text: #E8D4A0;
    --text-muted: #A08040;
}
body {
    background-color: var(--bg);
    color: var(--text);
    font-family: "PingFang SC", "Georgia", serif;
    margin: 0; padding: 0;
    /* inline SVG 六边形蜂窝铆钉背景 */
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100'%3E%3Cpath d='M28 66L0 50V18L28 2l28 16v32z' fill='none' stroke='rgba(184%2C115%2C51%2C0.14)' stroke-width='1'/%3E%3Ccircle cx='28' cy='2' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3Ccircle cx='56' cy='18' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3Ccircle cx='56' cy='50' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3Ccircle cx='28' cy='66' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3Ccircle cx='0' cy='50' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3Ccircle cx='0' cy='18' r='2.5' fill='rgba(184%2C115%2C51%2C0.18)'/%3E%3C/svg%3E"),
        repeating-linear-gradient(
            45deg,
            transparent, transparent 8px,
            rgba(184,115,51,0.025) 8px, rgba(184,115,51,0.025) 9px
        );
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 36px 28px;
    background: var(--t2e-surface, #1E1408);
    border: 1px solid var(--t2e-border, rgba(184,115,51,0.35));
    border-radius: 6px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(184,115,51,0.1);
}
/* 铆钉边框卡片 */
.rivet-card {
    background: linear-gradient(135deg, #1E1408 0%, #150F06 50%, #1E1408 100%);
    border: 2px solid var(--copper);
    border-radius: 4px;
    padding: 28px 28px;
    margin-bottom: 16px;
    position: relative;
    box-shadow: inset 0 0 40px rgba(0,0,0,0.5), 0 4px 20px rgba(0,0,0,0.6), 0 0 0 1px rgba(184,115,51,0.25);
}
.rivet-card::before, .rivet-card::after {
    content: '';
    position: absolute;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, var(--copper-light), var(--copper-dark));
    box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.1);
}
.rivet-card::before { top: 8px; left: 8px; }
.rivet-card::after { top: 8px; right: 8px; }
.rivet-bl, .rivet-br {
    position: absolute;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, var(--copper-light), var(--copper-dark));
    box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.1);
}
.rivet-bl { bottom: 8px; left: 8px; }
.rivet-br { bottom: 8px; right: 8px; }
.card-top-bar {
    position: absolute;
    top: 0; left: 24px; right: 24px;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--brass) 20%, var(--brass-light) 50%, var(--brass) 80%, transparent);
}
/* 齿轮（clip-path 36点） */
.gear { flex-shrink: 0; position: relative; width: 48px; height: 48px; }
.gear-teeth {
    position: absolute; inset: 0;
    background: radial-gradient(circle at 40% 35%, var(--copper-light), var(--copper-dark));
    clip-path: polygon(
        50% 0%, 56% 8%, 64% 4%, 66% 13%, 75% 11%, 73% 20%,
        82% 22%, 77% 30%, 86% 35%, 78% 41%, 85% 48%, 76% 51%,
        81% 60%, 71% 60%, 72% 70%, 62% 67%, 59% 77%, 50% 72%,
        41% 77%, 38% 67%, 28% 70%, 29% 60%, 19% 60%,
        24% 51%, 15% 48%, 22% 41%, 14% 35%, 23% 30%,
        18% 22%, 27% 20%, 25% 11%, 34% 13%, 36% 4%, 44% 8%
    );
}
.gear-body {
    position: absolute; inset: 6px;
    background: radial-gradient(circle at 40% 35%, var(--copper-light), var(--copper-dark) 60%, #5A3010);
    border-radius: 50%;
}
.gear-hole {
    position: absolute; inset: 14px;
    background: var(--bg);
    border-radius: 50%;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
}
.gear-pin {
    position: absolute; inset: 19px;
    background: radial-gradient(circle at 35% 35%, #D4944A, #5A3010);
    border-radius: 50%;
}
/* 压力表（conic-gradient 刻度盘） */
.gauge { position: relative; width: 60px; height: 60px; flex-shrink: 0; }
.gauge-outer {
    position: absolute; inset: 0;
    border-radius: 50%;
    background: linear-gradient(135deg, #2A1A08, #1A0E04);
    border: 3px solid var(--copper);
    box-shadow: 0 0 0 1px var(--copper-dark), inset 0 0 12px rgba(0,0,0,0.5);
}
.gauge-scale {
    position: absolute; inset: 4px;
    border-radius: 50%;
    border: 1px solid rgba(184,115,51,0.25);
    background: repeating-conic-gradient(
        rgba(200,168,48,0.55) 0deg, rgba(200,168,48,0.55) 2deg,
        transparent 2deg, transparent 30deg
    );
}
.gauge-needle {
    position: absolute;
    bottom: 50%; left: 50%;
    width: 2px; height: 18px;
    background: linear-gradient(to top, var(--copper-dark), #FF4400);
    transform-origin: bottom center;
    transform: translateX(-50%) rotate(-40deg);
    border-radius: 1px;
}
.gauge-center {
    position: absolute; inset: 22px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, var(--copper-light), var(--copper-dark));
}
.gauge-label {
    position: absolute;
    bottom: -18px; left: 50%;
    transform: translateX(-50%);
    font-size: 0.58em;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    white-space: nowrap;
}
/* 装饰横条（铜管分割线） */
.gear-wrap { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }
.pipe-divider { display: flex; align-items: center; gap: 0; margin: 16px 0; }
.pipe-line {
    flex: 1; height: 6px;
    background: linear-gradient(to bottom,
        var(--copper-dark) 0%, var(--copper-light) 30%,
        var(--copper) 50%, var(--copper-light) 70%, var(--copper-dark) 100%
    );
    border-radius: 3px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.08);
}
.pipe-joint {
    width: 14px; height: 14px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, var(--brass-light), var(--brass), var(--copper-dark));
    box-shadow: 0 2px 4px rgba(0,0,0,0.5);
    flex-shrink: 0;
}
/* 标题与内容 */
.sp-title {
    font-size: 1.65em;
    font-weight: 700;
    color: var(--brass-light);
    text-shadow: 0 0 20px rgba(200,168,48,0.4), 0 2px 4px rgba(0,0,0,0.5);
    letter-spacing: 0.05em;
    line-height: 1.25;
    margin-bottom: 6px;
    word-break: keep-all;
}
.sp-subtitle {
    font-size: 0.8em;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    font-style: italic;
}
/* 时间轴节点 */
.sp-item { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 14px; }
.sp-year-col { flex-shrink: 0; width: 62px; text-align: center; }
.sp-year-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--copper-dark), var(--copper), var(--copper-dark));
    color: var(--brass-light);
    font-size: 0.76em;
    font-weight: 700;
    padding: 4px 6px;
    border: 1px solid var(--brass);
    letter-spacing: 0.03em;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.08);
    white-space: nowrap;
}
.sp-content { flex: 1; min-width: 0; }
.sp-name {
    font-size: 0.98em;
    font-weight: 700;
    color: var(--brass-light);
    margin-bottom: 4px;
    letter-spacing: 0.02em;
    word-break: keep-all;
}
.sp-desc {
    font-size: 0.8em;
    color: var(--text-muted);
    line-height: 1.75;
    word-break: keep-all;
    overflow-wrap: break-word;
}
.sp-tag {
    display: inline-block;
    border: 1px solid rgba(184,115,51,0.35);
    color: var(--copper-light);
    font-size: 0.66em;
    padding: 1px 8px;
    margin-top: 5px;
    letter-spacing: 0.08em;
    background: rgba(184,115,51,0.07);
}
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.68em;
    padding-top: 16px;
    letter-spacing: 0.12em;
    opacity: 0.65;
}
```

**蒸汽朋克风使用要点：**
- 背景：inline SVG 六边形蜂窝（铆钉节点）+ 斜线底纹叠加，纯CSS无图片依赖
- 卡片：`rivet-card` 四角必须放 `.rivet-bl` `.rivet-br` 子元素（`::before/after` 只做上方两角）
- 齿轮：`.gear` 内放 `.gear-teeth` / `.gear-body` / `.gear-hole` / `.gear-pin` 四层
- 压力表：`.gauge` 内放 `.gauge-outer` / `.gauge-scale` / `.gauge-needle` / `.gauge-center` 四层
- 铜管分割线：`.pipe-divider` 内放 `.pipe-joint` / `.pipe-line` 交替，节数自由
- 正文 `word-break: keep-all` 防止中文在奇怪位置断行
- 年份标签 `.sp-year-badge` 宽度自适应，不要固定宽度防止溢出


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #C8A830;
    --t2e-accent-soft: rgba(184,115,51,0.12);
    --t2e-bg: #1A1008;
    --t2e-surface: #1E1408;
    --t2e-text: #E8D4A0;
    --t2e-muted: #A08040;
    --t2e-border: rgba(184,115,51,0.35);
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。
