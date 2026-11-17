## 11. 玻璃拟态风 (Glassmorphism)

适用：SaaS 产品官网、活动页、功能介绍、数据展示。

**风格亮点：** 彩色渐变背景 + 半透明磨砂卡片（backdrop-filter blur）+ 细白描边 + 柔和大阴影，卡片浮在渐变上。**注意：渐变必须铺在 body，容器/卡片半透明才能透出彩色。**

```css
/* === 玻璃拟态风 === */
:root {
    --gl-accent: #6D5EF7;
    --gl-accent2: #4EC8E8;
    --gl-text: #1F2433;
    --gl-muted: #5B6072;
    --gl-glass: rgba(255,255,255,0.55);
    --gl-glass-strong: rgba(255,255,255,0.72);
    --gl-border: rgba(255,255,255,0.6);
    --gl-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body {
    /* 渐变铺 body，容器/卡片半透明才能透出彩色 */
    background: linear-gradient(135deg,#E6E9FF 0%,#F3E9FF 35%,#E9F7FF 70%,#FFF0F7 100%);
    background-attachment: fixed;
    color: var(--gl-text);
    font-family: var(--gl-ft);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
    padding: 28px 0;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 44px 34px;
    background: var(--gl-glass);
    backdrop-filter: blur(22px) saturate(1.5);
    -webkit-backdrop-filter: blur(22px) saturate(1.5);
    border: 1px solid var(--gl-border);
    border-radius: 24px;
    box-shadow: 0 8px 40px rgba(80,70,160,0.16);
}
.gl-header { margin-bottom: 30px; }
.gl-title {
    font-size: 2.1em;
    font-weight: 700;
    letter-spacing: -0.015em;
    line-height: 1.22;
    color: var(--gl-text);
    word-break: keep-all; overflow-wrap: break-word;
}
.gl-title em { color: var(--gl-accent); font-style: normal; }
.gl-subtitle {
    color: var(--gl-muted);
    font-size: 0.95em;
    line-height: 1.65;
    margin-top: 12px;
    word-break: keep-all; overflow-wrap: break-word;
}
.gl-section-title {
    font-size: 1.15em;
    font-weight: 700;
    color: var(--gl-text);
    margin: 30px 0 14px;
    word-break: keep-all;
}
.gl-card {
    background: var(--gl-glass-strong);
    backdrop-filter: blur(16px) saturate(1.4);
    -webkit-backdrop-filter: blur(16px) saturate(1.4);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(80,70,160,0.12);
    padding: 18px 20px;
    margin: 14px 0;
}
.gl-card-title { font-weight: 600; color: var(--gl-text); line-height: 1.4; margin-bottom: 6px; }
.gl-card-desc { color: var(--gl-muted); font-size: 0.88em; line-height: 1.6; }
.gl-item {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.45);
}
.gl-item:last-child { border-bottom: none; }
.gl-num {
    flex: none;
    width: 28px; height: 28px;
    background: linear-gradient(135deg,#6D5EF7,#4EC8E8);
    color: #fff;
    border-radius: 12px;
    font-weight: 700; font-size: 0.82em;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 10px rgba(109,94,247,0.4);
}
.gl-item-body { flex: 1; }
.gl-item-title { color: var(--gl-text); font-weight: 500; line-height: 1.45; }
.gl-item-desc { color: var(--gl-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.gl-quote {
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-left: 3px solid var(--gl-accent);
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    color: var(--gl-text);
    font-size: 0.95em; line-height: 1.65;
    margin: 20px 0;
}
.gl-tag {
    display: inline-block;
    background: rgba(109,94,247,0.12);
    color: var(--gl-accent);
    border-radius: 8px;
    font-size: 0.78em; font-weight: 600;
    padding: 3px 10px; margin: 4px 6px 4px 0;
}
.gl-divider { border: none; height: 1px; background: rgba(255,255,255,0.5); margin: 28px 0; }
.gl-footer {
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-left: 3px solid var(--gl-accent);
    border-radius: 12px;
    padding: 12px 16px;
    margin-top: 32px;
    color: var(--gl-muted);
    font-size: 0.8em; line-height: 1.65;
}
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="gl-header">
        <div class="gl-title">玻璃拟态<br><em>通透</em>而有层次的现代质感</div>
        <div class="gl-subtitle">彩色渐变背景 + 半透明磨砂卡片，细白描边与柔和大阴影，卡片仿佛浮在渐变之上。</div>
    </div>

    <div class="gl-quote">通透，是现代产品设计的语言。让内容浮起来，让层次自然呼吸。</div>

    <div class="gl-section-title">核心特征</div>
    <div class="gl-card">
        <div class="gl-card-title">磨砂玻璃卡片</div>
        <div class="gl-card-desc">backdrop-filter 模糊背景，半透明白面透出底层彩色渐变，通透有层次。</div>
    </div>
    <div class="gl-card">
        <div class="gl-card-title">细白描边 + 柔阴影</div>
        <div class="gl-card-desc">细腻白色边框勾勒玻璃边缘，大范围柔和阴影让卡片"浮"起来。</div>
    </div>

    <div class="gl-section-title">适用场景</div>
    <div class="gl-item">
        <div class="gl-num">1</div>
        <div class="gl-item-body">
            <div class="gl-item-title">SaaS 产品官网 / 活动页</div>
            <div class="gl-item-desc">现代通透质感天然契合科技产品的调性。</div>
        </div>
    </div>
    <div class="gl-item">
        <div class="gl-num">2</div>
        <div class="gl-item-body">
            <div class="gl-item-title">功能介绍 / 数据展示</div>
            <div class="gl-item-desc">半透卡片让多模块信息层次清晰不拥挤。</div>
        </div>
    </div>

    <div class="gl-divider"></div>
    <div>
        <span class="gl-tag">玻璃拟态</span>
        <span class="gl-tag">彩色渐变</span>
        <span class="gl-tag">磨砂通透</span>
        <span class="gl-tag">SaaS 质感</span>
    </div>

    <div class="gl-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #6D5EF7;
    --t2e-accent-soft: rgba(109,94,247,0.12);
    --t2e-bg: #EDEBFF;
    --t2e-surface: rgba(255,255,255,0.72);
    --t2e-text: #1F2433;
    --t2e-muted: #5B6072;
    --t2e-border: rgba(255,255,255,0.6);
}
```

### 点睛装饰（建议使用）

玻璃拟态的灵魂是「卡片浮在光斑上」。在 body 加两颗大光斑渐变球，毛玻璃卡片的 blur 才有内容可透：

```css
/* 光斑渐变球：fixed 定位在 body 层，被卡片 backdrop-filter 模糊后产生流光感 */
body { position: relative; overflow-x: hidden; }
body::before, body::after {
    content: ''; position: fixed; border-radius: 50%; filter: blur(60px); z-index: -1;
}
body::before { width: 320px; height: 320px; top: -80px; left: -60px;
    background: radial-gradient(circle, rgba(109,94,247,0.45), transparent 70%); }
body::after { width: 280px; height: 280px; bottom: -60px; right: -50px;
    background: radial-gradient(circle, rgba(78,200,232,0.4), transparent 70%); }
```
