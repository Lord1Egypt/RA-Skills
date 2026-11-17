## 16. 马卡龙粉彩风 (Macaron)

适用：甜品、母婴、生活分享、节日祝福、好物种草。

**风格亮点：** 奶油粉底搭配低饱和珊瑚粉（#EB6F8E），纯白卡片，大圆角，甜美柔和可爱不腻。

```css
:root {
    --ma-bg: #FDF2F4; --ma-surface: #FFFAFB; --ma-card: #FFFFFF;
    --ma-accent: #EB6F8E; --ma-accent2: #F5A9C0;
    --ma-text: #4A2F38; --ma-muted: #9C7B85;
    --ma-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--ma-bg); color: var(--ma-text); font-family: var(--ma-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--ma-surface); border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; }
.ma-header { margin-bottom: 32px; }
.ma-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--ma-text); word-break: keep-all; overflow-wrap: break-word; }
.ma-title em { color: var(--ma-accent); font-style: normal; }
.ma-subtitle { color: var(--ma-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.ma-section-title { font-size: 1.15em; font-weight: 600; color: var(--ma-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--ma-accent); word-break: keep-all; }
.ma-card { background: var(--ma-card); border: 1px solid rgba(0,0,0,0.05); border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.05); padding: 18px 20px; margin: 14px 0; }
.ma-card-title { font-weight: 600; color: var(--ma-text); line-height: 1.4; margin-bottom: 6px; }
.ma-card-desc { color: var(--ma-muted); font-size: 0.88em; line-height: 1.6; }
.ma-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.ma-item:last-child { border-bottom: none; }
.ma-num { flex: none; width: 28px; height: 28px; background: #EB6F8E; color: #fff; border-radius: 14px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.ma-item-body { flex: 1; }
.ma-item-title { color: var(--ma-text); font-weight: 500; line-height: 1.45; }
.ma-item-desc { color: var(--ma-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.ma-quote { background: rgba(235,111,142,0.10); border-left: 3px solid var(--ma-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--ma-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.ma-tag { display: inline-block; background: rgba(235,111,142,0.13); color: var(--ma-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.ma-divider { border: none; height: 1px; background: rgba(0,0,0,0.08); margin: 28px 0; }
.ma-footer { background: rgba(235,111,142,0.10); border-left: 3px solid var(--ma-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--ma-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="ma-header">
        <div class="ma-title">马卡龙粉彩<br><em>珊瑚粉</em>的甜美</div>
        <div class="ma-subtitle">奶油粉底搭配低饱和珊瑚粉，甜美柔和，可爱而不腻。</div>
    </div>
    <div class="ma-quote">一点点甜，一点点软，就是恰到好处的可爱。</div>
    <div class="ma-section-title">核心特征</div>
    <div class="ma-card"><div class="ma-card-title">珊瑚粉主调</div><div class="ma-card-desc">#EB6F8E 珊瑚粉低饱和不刺眼，樱粉点缀。</div></div>
    <div class="ma-card"><div class="ma-card-title">奶油粉底</div><div class="ma-card-desc">极浅奶油粉背景，圆润大圆角，甜而不腻。</div></div>
    <div class="ma-section-title">适用场景</div>
    <div class="ma-item"><div class="ma-num">1</div><div class="ma-item-body"><div class="ma-item-title">甜品 / 母婴 / 生活分享</div><div class="ma-item-desc">甜美调性契合温柔、可爱的内容。</div></div></div>
    <div class="ma-item"><div class="ma-num">2</div><div class="ma-item-body"><div class="ma-item-title">节日祝福 / 好物种草</div><div class="ma-item-desc">粉彩色系提升亲和力。</div></div></div>
    <div class="ma-divider"></div>
    <div>
        <span class="ma-tag">马卡龙</span>
        <span class="ma-tag">珊瑚粉</span>
        <span class="ma-tag">甜美</span>
        <span class="ma-tag">粉彩</span>
    </div>
    <div class="ma-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #EB6F8E;
    --t2e-accent-soft: rgba(235,111,142,0.12);
    --t2e-bg: #FDF2F4;
    --t2e-surface: #FFFFFF;
    --t2e-text: #4A2F38;
    --t2e-muted: #9C7B85;
    --t2e-border: rgba(0,0,0,0.06);
}
```

### 点睛装饰（建议使用）

马卡龙风加「波点 + 糖粒序号」，甜美感立现：

```css
/* 背景波点（双色错位） */
body { background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28'%3E%3Ccircle cx='7' cy='7' r='2' fill='rgba(235%2C111%2C142%2C0.10)'/%3E%3Ccircle cx='21' cy='21' r='1.5' fill='rgba(245%2C169%2C192%2C0.14)'/%3E%3C/svg%3E");
    background-size: 28px 28px; }
/* 序号变糖粒：双色渐变 + 内高光 */
.ma-num { background: linear-gradient(135deg, #F5A9C0, #EB6F8E); border-radius: 50%;
    box-shadow: inset 0 2px 3px rgba(255,255,255,0.5), 0 2px 6px rgba(235,111,142,0.3); }
/* 卡片底部波浪线装饰 */
.ma-wave-line { height: 6px; margin-top: 4px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='6'%3E%3Cpath d='M0 3q3-3 6 0t6 0 6 0 6 0' fill='none' stroke='rgba(235%2C111%2C142%2C0.3)' stroke-width='1.5'/%3E%3C/svg%3E");
    background-size: 24px 6px; background-repeat: repeat-x; }
```
