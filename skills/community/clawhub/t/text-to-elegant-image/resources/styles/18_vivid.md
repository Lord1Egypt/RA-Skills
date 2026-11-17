## 18. 活力渐变风 (Vivid)

适用：活动、促销、潮流、年轻品牌、音乐娱乐。

**风格亮点：** 紫→粉→橙三色渐变（120°）贯穿标题、序号、强调元素，纯白衬底最大化衬托鲜活，年轻潮流张力十足。标题强调字用渐变文字裁剪。

```css
:root {
    --vv-bg: #FBF9FF; --vv-surface: #FFFFFF; --vv-card: #FFFFFF;
    --vv-accent: #7C3AED; --vv-accent2: #EC4899;
    --vv-text: #1E1B2E; --vv-muted: #6B6480;
    --vv-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--vv-bg); color: var(--vv-text); font-family: var(--vv-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--vv-surface); border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; }
.vv-header { margin-bottom: 32px; }
.vv-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--vv-text); word-break: keep-all; overflow-wrap: break-word; }
.vv-title em { color: var(--vv-accent); font-style: normal; }
.vv-subtitle { color: var(--vv-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.vv-section-title { font-size: 1.15em; font-weight: 600; color: var(--vv-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--vv-accent); word-break: keep-all; }
.vv-card { background: var(--vv-card); border: 1px solid rgba(0,0,0,0.05); border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.05); padding: 18px 20px; margin: 14px 0; }
.vv-card-title { font-weight: 600; color: var(--vv-text); line-height: 1.4; margin-bottom: 6px; }
.vv-card-desc { color: var(--vv-muted); font-size: 0.88em; line-height: 1.6; }
.vv-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.vv-item:last-child { border-bottom: none; }
.vv-num { flex: none; width: 28px; height: 28px; background: linear-gradient(120deg,#7C3AED 0%,#EC4899 55%,#F97316 100%); color: #fff; border-radius: 10px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.vv-item-body { flex: 1; }
.vv-item-title { color: var(--vv-text); font-weight: 500; line-height: 1.45; }
.vv-item-desc { color: var(--vv-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.vv-quote { background: rgba(124,58,237,0.10); border-left: 3px solid var(--vv-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--vv-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.vv-tag { display: inline-block; background: rgba(124,58,237,0.12); color: var(--vv-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.vv-divider { border: none; height: 1px; background: rgba(0,0,0,0.08); margin: 28px 0; }
.vv-footer { background: rgba(124,58,237,0.10); border-left: 3px solid var(--vv-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--vv-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
.vv-title em { background: linear-gradient(120deg,#7C3AED 0%,#EC4899 55%,#F97316 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; font-style: normal; }
.vv-section-title { border-left-color: #EC4899; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="vv-header">
        <div class="vv-title">活力<em>渐变</em><br>年轻而有张力</div>
        <div class="vv-subtitle">紫→粉→橙三色渐变，充满活力与张力，年轻潮流的视觉语言。</div>
    </div>
    <div class="vv-quote">用色彩表达能量，让每一屏都有张力。</div>
    <div class="vv-section-title">核心特征</div>
    <div class="vv-card"><div class="vv-card-title">三色渐变</div><div class="vv-card-desc">紫粉橙 120° 渐变贯穿标题、序号、强调元素。</div></div>
    <div class="vv-card"><div class="vv-card-title">纯白衬底</div><div class="vv-card-desc">纯白背景最大化衬托渐变的鲜活。</div></div>
    <div class="vv-section-title">适用场景</div>
    <div class="vv-item"><div class="vv-num">1</div><div class="vv-item-body"><div class="vv-item-title">活动 / 促销 / 潮流</div><div class="vv-item-desc">高饱和渐变抓眼球，适合营销传播。</div></div></div>
    <div class="vv-item"><div class="vv-num">2</div><div class="vv-item-body"><div class="vv-item-title">年轻品牌 / 音乐娱乐</div><div class="vv-item-desc">张力十足契合年轻受众。</div></div></div>
    <div class="vv-divider"></div>
    <div>
        <span class="vv-tag">活力</span>
        <span class="vv-tag">三色渐变</span>
        <span class="vv-tag">潮流</span>
        <span class="vv-tag">年轻</span>
    </div>
    <div class="vv-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #7C3AED;
    --t2e-accent-soft: rgba(124,58,237,0.12);
    --t2e-bg: #FBF9FF;
    --t2e-surface: #FFFFFF;
    --t2e-text: #1E1B2E;
    --t2e-muted: #6B6480;
    --t2e-border: rgba(0,0,0,0.06);
}
```

### 点睛装饰（建议使用）

活力渐变加「流体色块 + 渐变描边卡」，张力立现：

```css
/* 背景两团流体色块（blur 渐变球） */
body { position: relative; overflow-x: hidden; }
body::before, body::after { content: ''; position: fixed; border-radius: 50%;
    filter: blur(70px); z-index: -1; opacity: 0.35; }
body::before { width: 300px; height: 300px; top: -60px; right: -80px;
    background: radial-gradient(circle, #EC4899, transparent 70%); }
body::after { width: 260px; height: 260px; bottom: -50px; left: -70px;
    background: radial-gradient(circle, #7C3AED, transparent 70%); }
/* 渐变描边卡片（双层背景裁剪法，重点卡片用） */
.vv-card-hero { border: none; background:
    linear-gradient(var(--vv-card), var(--vv-card)) padding-box,
    linear-gradient(120deg, #7C3AED, #EC4899, #F97316) border-box;
    border: 2px solid transparent; }
```

```html
<div class="vv-card vv-card-hero">…</div>
```
