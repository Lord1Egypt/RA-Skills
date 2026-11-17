## 10. 莫兰迪高级灰风 (Morandi)

适用：品牌方法论、复盘总结、人文随笔、生活美学。

**风格亮点：** 低饱和大地灰调（灰绿/灰褐/藕粉），柔和阴影，中等圆角，无强对比，整体安静高级。强调色为莫兰迪灰绿。

```css
/* === 莫兰迪高级灰风 === */
:root {
    --mo-bg: #E8E4DD;
    --mo-surface: #F4F1EC;
    --mo-card: #FBFAF7;
    --mo-accent: #7C8B7E;
    --mo-accent2: #9A8C82;
    --mo-text: #4A453E;
    --mo-muted: #94897C;
    --mo-border: rgba(74,69,62,0.12);
    --mo-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body {
    background-color: var(--mo-bg);
    color: var(--mo-text);
    font-family: var(--mo-ft);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 48px 36px;
    background: var(--mo-surface);
    border: 1px solid rgba(74,69,62,0.08);
    border-radius: 18px;
}
.mo-header { margin-bottom: 32px; }
.mo-title {
    font-size: 2.1em;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25;
    color: var(--mo-text);
    word-break: keep-all; overflow-wrap: break-word;
}
.mo-subtitle {
    color: var(--mo-muted);
    font-size: 0.95em;
    line-height: 1.65;
    margin-top: 12px;
    word-break: keep-all; overflow-wrap: break-word;
}
.mo-section-title {
    font-size: 1.15em;
    font-weight: 600;
    color: var(--mo-text);
    margin: 30px 0 14px;
    padding-left: 12px;
    border-left: 4px solid var(--mo-accent);
    word-break: keep-all;
}
.mo-card {
    background: var(--mo-card);
    border: 1px solid rgba(74,69,62,0.07);
    border-radius: 14px;
    box-shadow: 0 2px 14px rgba(74,69,62,0.06);
    padding: 18px 20px;
    margin: 14px 0;
}
.mo-card-title {
    font-weight: 600;
    color: var(--mo-text);
    line-height: 1.4;
    margin-bottom: 6px;
}
.mo-card-desc {
    color: var(--mo-muted);
    font-size: 0.88em;
    line-height: 1.6;
}
.mo-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(74,69,62,0.07);
}
.mo-item:last-child { border-bottom: none; }
.mo-num {
    flex: none;
    width: 26px; height: 26px;
    background: var(--mo-accent);
    color: #fff;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.82em;
    display: flex; align-items: center; justify-content: center;
}
.mo-item-body { flex: 1; }
.mo-item-title { color: var(--mo-text); font-weight: 500; line-height: 1.45; }
.mo-item-desc { color: var(--mo-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.mo-quote {
    background: rgba(124,139,126,0.08);
    border-left: 3px solid var(--mo-accent);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    color: var(--mo-text);
    font-size: 0.95em;
    line-height: 1.65;
    margin: 20px 0;
}
.mo-tag {
    display: inline-block;
    background: rgba(124,139,126,0.14);
    color: var(--mo-accent);
    border-radius: 7px;
    font-size: 0.78em;
    font-weight: 600;
    padding: 3px 10px;
    margin: 4px 6px 4px 0;
}
.mo-divider { border: none; height: 1px; background: rgba(74,69,62,0.1); margin: 28px 0; }
.mo-footer {
    background: rgba(124,139,126,0.08);
    border-left: 3px solid var(--mo-accent);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 32px;
    color: var(--mo-muted);
    font-size: 0.8em;
    line-height: 1.65;
}
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="mo-header">
        <div class="mo-title">莫兰迪高级灰<br>安静而克制的美学</div>
        <div class="mo-subtitle">低饱和大地灰调，柔和阴影，无强对比——整体呈现一种沉静的高级质感。</div>
    </div>

    <div class="mo-quote">好的设计不是被注意到，而是被感受到。留白与克制，本身就是一种表达。</div>

    <div class="mo-section-title">核心特征</div>
    <div class="mo-card">
        <div class="mo-card-title">灰调配色</div>
        <div class="mo-card-desc">灰绿、灰褐、藕粉为主，饱和度统一压低，避免任何刺眼的高对比。</div>
    </div>
    <div class="mo-card">
        <div class="mo-card-title">柔和层次</div>
        <div class="mo-card-desc">用极淡的阴影和中等圆角营造安静的层次感，而非强边框。</div>
    </div>

    <div class="mo-section-title">适用场景</div>
    <div class="mo-item">
        <div class="mo-num">1</div>
        <div class="mo-item-body">
            <div class="mo-item-title">品牌方法论 / 复盘总结</div>
            <div class="mo-item-desc">安静高级的气质适合承载严肃、克制的内容表达。</div>
        </div>
    </div>
    <div class="mo-item">
        <div class="mo-num">2</div>
        <div class="mo-item-body">
            <div class="mo-item-title">人文随笔 / 生活美学</div>
            <div class="mo-item-desc">低饱和调性天然契合慢节奏、有温度的文字。</div>
        </div>
    </div>

    <div class="mo-divider"></div>
    <div>
        <span class="mo-tag">高级灰</span>
        <span class="mo-tag">低饱和</span>
        <span class="mo-tag">留白克制</span>
        <span class="mo-tag">莫兰迪青</span>
    </div>

    <div class="mo-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #7C8B7E;
    --t2e-accent-soft: rgba(124,139,126,0.12);
    --t2e-bg: #E8E4DD;
    --t2e-surface: #FBFAF7;
    --t2e-text: #4A453E;
    --t2e-muted: #94897C;
    --t2e-border: rgba(74,69,62,0.12);
}
```

### 点睛装饰（建议使用）

莫兰迪的辨识度来自「色卡」语言。在 header 下方放一条莫兰迪色卡条，瞬间点题：

```css
/* 莫兰迪色卡条：五格低饱和色块，放 header 下方 */
.mo-palette { display: flex; gap: 6px; margin: 18px 0 6px; }
.mo-palette span { flex: 1; height: 14px; border-radius: 4px; opacity: 0.85; }
.mo-palette span:nth-child(1) { background: #7C8B7E; }
.mo-palette span:nth-child(2) { background: #9A8C82; }
.mo-palette span:nth-child(3) { background: #B8A99A; }
.mo-palette span:nth-child(4) { background: #A8B0A6; }
.mo-palette span:nth-child(5) { background: #C4B5AD; }
/* 背景加极淡织物噪点 */
body { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' opacity='0.02'/%3E%3C/svg%3E"); }
```

```html
<div class="mo-palette"><span></span><span></span><span></span><span></span><span></span></div>
```
