## 13. 清新自然绿风 (Fresh)

适用：健康、环保、生活方式、知识科普、教程攻略。

**风格亮点：** 极浅薄荷底搭配森林绿强调（#2E9E5B），纯白卡片，清爽通透有呼吸感。

```css
:root {
    --fr-bg: #F1F7F0; --fr-surface: #FBFEFA; --fr-card: #FFFFFF;
    --fr-accent: #2E9E5B; --fr-accent2: #6FB98F;
    --fr-text: #1F3A29; --fr-muted: #6B8475;
    --fr-ft: "Inter","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--fr-bg); color: var(--fr-text); font-family: var(--fr-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--fr-surface); border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; }
.fr-header { margin-bottom: 32px; }
.fr-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--fr-text); word-break: keep-all; overflow-wrap: break-word; }
.fr-title em { color: var(--fr-accent); font-style: normal; }
.fr-subtitle { color: var(--fr-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.fr-section-title { font-size: 1.15em; font-weight: 600; color: var(--fr-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--fr-accent); word-break: keep-all; }
.fr-card { background: var(--fr-card); border: 1px solid rgba(0,0,0,0.05); border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.05); padding: 18px 20px; margin: 14px 0; }
.fr-card-title { font-weight: 600; color: var(--fr-text); line-height: 1.4; margin-bottom: 6px; }
.fr-card-desc { color: var(--fr-muted); font-size: 0.88em; line-height: 1.6; }
.fr-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.06); }
.fr-item:last-child { border-bottom: none; }
.fr-num { flex: none; width: 28px; height: 28px; background: #2E9E5B; color: #fff; border-radius: 8px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.fr-item-body { flex: 1; }
.fr-item-title { color: var(--fr-text); font-weight: 500; line-height: 1.45; }
.fr-item-desc { color: var(--fr-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.fr-quote { background: rgba(46,158,91,0.10); border-left: 3px solid var(--fr-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--fr-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.fr-tag { display: inline-block; background: rgba(46,158,91,0.12); color: var(--fr-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.fr-divider { border: none; height: 1px; background: rgba(0,0,0,0.08); margin: 28px 0; }
.fr-footer { background: rgba(46,158,91,0.10); border-left: 3px solid var(--fr-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--fr-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="fr-header">
        <div class="fr-title">清新自然<br><em>森林绿</em>的呼吸感</div>
        <div class="fr-subtitle">极浅薄荷底色搭配森林绿强调，清爽通透，天然亲近自然。</div>
    </div>
    <div class="fr-quote">让内容像清晨的森林一样，干净、通透、有生机。</div>
    <div class="fr-section-title">核心特征</div>
    <div class="fr-card"><div class="fr-card-title">森林绿主调</div><div class="fr-card-desc">#2E9E5B 森林绿为核心，浅草绿点缀，饱和适中不刺眼。</div></div>
    <div class="fr-card"><div class="fr-card-title">薄荷浅底</div><div class="fr-card-desc">极浅薄荷背景衬托纯白卡片，清爽有呼吸感。</div></div>
    <div class="fr-section-title">适用场景</div>
    <div class="fr-item"><div class="fr-num">1</div><div class="fr-item-body"><div class="fr-item-title">健康 / 环保 / 生活方式</div><div class="fr-item-desc">自然亲和的调性契合绿色、健康类内容。</div></div></div>
    <div class="fr-item"><div class="fr-num">2</div><div class="fr-item-body"><div class="fr-item-title">知识科普 / 教程攻略</div><div class="fr-item-desc">清爽底色让长文阅读更轻松。</div></div></div>
    <div class="fr-divider"></div>
    <div>
        <span class="fr-tag">清新</span>
        <span class="fr-tag">森林绿</span>
        <span class="fr-tag">自然</span>
        <span class="fr-tag">呼吸感</span>
    </div>
    <div class="fr-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #2E9E5B;
    --t2e-accent-soft: rgba(46,158,91,0.12);
    --t2e-bg: #F1F7F0;
    --t2e-surface: #FFFFFF;
    --t2e-text: #1F3A29;
    --t2e-muted: #6B8475;
    --t2e-border: rgba(0,0,0,0.06);
}
```

### 点睛装饰（建议使用）

清新绿加「叶片」元素，自然气质立现：

```css
/* CSS 叶片：border-radius 单角归零即叶形，放 section-title 前或卡片角落 */
.fr-leaf { display: inline-block; width: 14px; height: 14px;
    background: linear-gradient(135deg, #6FB98F, #2E9E5B);
    border-radius: 0 70% 0 70%; margin-right: 8px; vertical-align: -2px; }
/* 背景极淡叶脉点缀 */
body { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Cpath d='M20 60c0-14 8-26 20-30-4 12-8 24-20 30z' fill='rgba(46%2C158%2C91%2C0.05)'/%3E%3C/svg%3E");
    background-size: 80px 80px; }
```

```html
<div class="fr-section-title"><span class="fr-leaf"></span>核心特征</div>
```
