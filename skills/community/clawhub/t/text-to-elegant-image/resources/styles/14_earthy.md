## 14. 大地原木风 (Earthy)

适用：手作、咖啡、生活美学、品牌故事、人文叙事。

**风格亮点：** 米色亚麻底搭配赤陶橙（#B5683C）与橄榄棕，奶油白卡片，温暖朴实有手作质地。

```css
:root {
    --ea-bg: #F3ECE1; --ea-surface: #FAF5EC; --ea-card: #FFFDF8;
    --ea-accent: #B5683C; --ea-accent2: #8A8B5C;
    --ea-text: #3D2E22; --ea-muted: #8A7460;
    --ea-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--ea-bg); color: var(--ea-text); font-family: var(--ea-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--ea-surface); border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; }
.ea-header { margin-bottom: 32px; }
.ea-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--ea-text); word-break: keep-all; overflow-wrap: break-word; }
.ea-title em { color: var(--ea-accent); font-style: normal; }
.ea-subtitle { color: var(--ea-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.ea-section-title { font-size: 1.15em; font-weight: 600; color: var(--ea-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--ea-accent); word-break: keep-all; }
.ea-card { background: var(--ea-card); border: 1px solid rgba(0,0,0,0.05); border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.05); padding: 18px 20px; margin: 14px 0; }
.ea-card-title { font-weight: 600; color: var(--ea-text); line-height: 1.4; margin-bottom: 6px; }
.ea-card-desc { color: var(--ea-muted); font-size: 0.88em; line-height: 1.6; }
.ea-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.ea-item:last-child { border-bottom: none; }
.ea-num { flex: none; width: 28px; height: 28px; background: #B5683C; color: #fff; border-radius: 8px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.ea-item-body { flex: 1; }
.ea-item-title { color: var(--ea-text); font-weight: 500; line-height: 1.45; }
.ea-item-desc { color: var(--ea-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.ea-quote { background: rgba(181,104,60,0.10); border-left: 3px solid var(--ea-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--ea-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.ea-tag { display: inline-block; background: rgba(181,104,60,0.12); color: var(--ea-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.ea-divider { border: none; height: 1px; background: rgba(0,0,0,0.08); margin: 28px 0; }
.ea-footer { background: rgba(181,104,60,0.10); border-left: 3px solid var(--ea-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--ea-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="ea-header">
        <div class="ea-title">大地原木<br><em>赤陶</em>的温暖质地</div>
        <div class="ea-subtitle">米色亚麻底搭配赤陶橙与橄榄棕，温暖朴实，有手作的质地感。</div>
    </div>
    <div class="ea-quote">回归土地的颜色，朴素本身就是一种高级。</div>
    <div class="ea-section-title">核心特征</div>
    <div class="ea-card"><div class="ea-card-title">赤陶橙主调</div><div class="ea-card-desc">#B5683C 赤陶橙为核心，橄榄棕辅助，暖调统一。</div></div>
    <div class="ea-card"><div class="ea-card-title">亚麻米底</div><div class="ea-card-desc">米色亚麻背景 + 奶油白卡片，温润不冷硬。</div></div>
    <div class="ea-section-title">适用场景</div>
    <div class="ea-item"><div class="ea-num">1</div><div class="ea-item-body"><div class="ea-item-title">手作 / 咖啡 / 生活美学</div><div class="ea-item-desc">温暖质地契合有温度的慢生活内容。</div></div></div>
    <div class="ea-item"><div class="ea-num">2</div><div class="ea-item-body"><div class="ea-item-title">品牌故事 / 人文叙事</div><div class="ea-item-desc">朴实调性承载真诚的表达。</div></div></div>
    <div class="ea-divider"></div>
    <div>
        <span class="ea-tag">大地色</span>
        <span class="ea-tag">赤陶橙</span>
        <span class="ea-tag">原木</span>
        <span class="ea-tag">手作感</span>
    </div>
    <div class="ea-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #B5683C;
    --t2e-accent-soft: rgba(181,104,60,0.12);
    --t2e-bg: #F3ECE1;
    --t2e-surface: #FFFDF8;
    --t2e-text: #3D2E22;
    --t2e-muted: #8A7460;
    --t2e-border: rgba(0,0,0,0.06);
}
```

### 点睛装饰（建议使用）

大地原木风加「亚麻织纹 + 手作缝线卡片」，质地感立现：

```css
/* 背景亚麻织纹：交叉细线 */
body { background-image:
    repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(138,116,96,0.04) 3px, rgba(138,116,96,0.04) 4px),
    repeating-linear-gradient(90deg, transparent, transparent 3px, rgba(138,116,96,0.04) 3px, rgba(138,116,96,0.04) 4px); }
/* 缝线卡片变体：虚线内框像手工缝边 */
.ea-stitch { position: relative; }
.ea-stitch::before { content: ''; position: absolute; inset: 6px;
    border: 1.5px dashed rgba(181,104,60,0.35); border-radius: 10px; pointer-events: none; }
```

```html
<div class="ea-card ea-stitch">…</div>
```
