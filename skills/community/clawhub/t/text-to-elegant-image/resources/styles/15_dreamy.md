## 15. 优雅紫梦幻风 (Dreamy)

适用：美妆、时尚、情感、活动海报、邀请函。

**风格亮点：** 极浅薰衣草底搭配品紫渐变（#8B5CF6→#C084FC），纯白卡片，梦幻优雅浪漫。序号用紫色渐变球。

```css
:root {
    --dr-bg: #F6F2FB; --dr-surface: #FCFAFE; --dr-card: #FFFFFF;
    --dr-accent: #8B5CF6; --dr-accent2: #C084FC;
    --dr-text: #2E2541; --dr-muted: #7C7295;
    --dr-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--dr-bg); color: var(--dr-text); font-family: var(--dr-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--dr-surface); border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; }
.dr-header { margin-bottom: 32px; }
.dr-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--dr-text); word-break: keep-all; overflow-wrap: break-word; }
.dr-title em { color: var(--dr-accent); font-style: normal; }
.dr-subtitle { color: var(--dr-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.dr-section-title { font-size: 1.15em; font-weight: 600; color: var(--dr-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--dr-accent); word-break: keep-all; }
.dr-card { background: var(--dr-card); border: 1px solid rgba(0,0,0,0.05); border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.05); padding: 18px 20px; margin: 14px 0; }
.dr-card-title { font-weight: 600; color: var(--dr-text); line-height: 1.4; margin-bottom: 6px; }
.dr-card-desc { color: var(--dr-muted); font-size: 0.88em; line-height: 1.6; }
.dr-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.dr-item:last-child { border-bottom: none; }
.dr-num { flex: none; width: 28px; height: 28px; background: linear-gradient(135deg,#8B5CF6,#C084FC); color: #fff; border-radius: 12px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.dr-item-body { flex: 1; }
.dr-item-title { color: var(--dr-text); font-weight: 500; line-height: 1.45; }
.dr-item-desc { color: var(--dr-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.dr-quote { background: rgba(139,92,246,0.10); border-left: 3px solid var(--dr-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--dr-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.dr-tag { display: inline-block; background: rgba(139,92,246,0.12); color: var(--dr-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.dr-divider { border: none; height: 1px; background: rgba(0,0,0,0.08); margin: 28px 0; }
.dr-footer { background: rgba(139,92,246,0.10); border-left: 3px solid var(--dr-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--dr-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="dr-header">
        <div class="dr-title">优雅紫梦幻<br><em>薰衣草</em>般的柔和</div>
        <div class="dr-subtitle">极浅薰衣草底搭配品紫渐变，梦幻优雅，浪漫而不失质感。</div>
    </div>
    <div class="dr-quote">优雅是一种气质，紫色是它的颜色。</div>
    <div class="dr-section-title">核心特征</div>
    <div class="dr-card"><div class="dr-card-title">品紫渐变</div><div class="dr-card-desc">#8B5CF6 品紫到浅紫渐变，梦幻有层次。</div></div>
    <div class="dr-card"><div class="dr-card-title">薰衣草浅底</div><div class="dr-card-desc">极浅薰衣草背景，纯白卡片，柔和舒适。</div></div>
    <div class="dr-section-title">适用场景</div>
    <div class="dr-item"><div class="dr-num">1</div><div class="dr-item-body"><div class="dr-item-title">美妆 / 时尚 / 情感</div><div class="dr-item-desc">浪漫梦幻契合女性向、情感类内容。</div></div></div>
    <div class="dr-item"><div class="dr-num">2</div><div class="dr-item-body"><div class="dr-item-title">活动海报 / 邀请函</div><div class="dr-item-desc">优雅调性提升仪式感。</div></div></div>
    <div class="dr-divider"></div>
    <div>
        <span class="dr-tag">梦幻</span>
        <span class="dr-tag">品紫</span>
        <span class="dr-tag">薰衣草</span>
        <span class="dr-tag">优雅</span>
    </div>
    <div class="dr-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #8B5CF6;
    --t2e-accent-soft: rgba(139,92,246,0.12);
    --t2e-bg: #F6F2FB;
    --t2e-surface: #FFFFFF;
    --t2e-text: #2E2541;
    --t2e-muted: #7C7295;
    --t2e-border: rgba(0,0,0,0.06);
}
```

### 点睛装饰（建议使用）

优雅紫加「星光 + 柔光晕」，梦幻感立现：

```css
/* 背景四角星星光点缀 */
body { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cpath d='M30 20l2 6 6 2-6 2-2 6-2-6-6-2 6-2zM90 80l1.5 4.5L96 86l-4.5 1.5L90 92l-1.5-4.5L84 86l4.5-1.5z' fill='rgba(139%2C92%2C246%2C0.14)'/%3E%3C/svg%3E");
    background-size: 120px 120px; }
/* 标题柔光晕 */
.dr-title em { text-shadow: 0 0 24px rgba(192,132,252,0.45); }
/* 卡片顶部渐变细线 */
.dr-card { position: relative; overflow: hidden; }
.dr-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #C084FC, transparent); opacity: 0.6; }
```
