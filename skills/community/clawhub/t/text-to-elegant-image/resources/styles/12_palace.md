## 12. 故宫风 (Palace)

适用：中国历史、文化艺术、国风节日、文博展览。

**风格亮点：** 深棕木底、朱砂红与鎏金字，书法字体点睛（Ma Shan Zheng/ZCOOL XiaoWei，无头环境自动 fallback 到宋体），方形描边序号 + 金色渐变分割线，宫廷庄重华贵。

```css
:root {
    --pl-bg: #0E0604; --pl-surface: #160A06; --pl-card: #1A0A06;
    --pl-crimson: #C0392B; --pl-gold: #C8A45A; --pl-gold-light: #E8C87A;
    --pl-text: #F0E6C8; --pl-muted: #9A8060;
    --pl-serif: "Ma Shan Zheng","ZCOOL XiaoWei","Noto Serif SC","Source Han Serif CN","Songti SC","STSong",Georgia,serif;
}
body { background-color: var(--pl-bg); color: var(--pl-text); font-family: var(--pl-serif); line-height: 1.8; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 38px; background: var(--pl-surface); border: 1px solid rgba(200,164,90,0.22); border-radius: 4px; box-shadow: 0 0 0 4px rgba(200,164,90,0.06); }
.pl-header { margin-bottom: 34px; text-align: center; border-bottom: 1px solid rgba(200,164,90,0.25); padding-bottom: 26px; }
.pl-title { font-size: 2.3em; font-weight: 400; letter-spacing: 0.08em; line-height: 1.35; color: var(--pl-gold-light); word-break: keep-all; }
.pl-title em { color: var(--pl-crimson); font-style: normal; }
.pl-subtitle { color: var(--pl-muted); font-size: 0.95em; line-height: 1.7; margin-top: 14px; letter-spacing: 0.04em; word-break: keep-all; }
.pl-section-title { font-size: 1.25em; font-weight: 400; color: var(--pl-gold); margin: 32px 0 16px; padding-left: 14px; border-left: 3px solid var(--pl-crimson); letter-spacing: 0.06em; word-break: keep-all; }
.pl-card { background: linear-gradient(160deg,#1E0C08 0%,#120602 60%,#1A0A06 100%); border: 1px solid rgba(200,164,90,0.2); border-radius: 4px; box-shadow: 0 2px 16px rgba(0,0,0,0.4); padding: 18px 22px; margin: 14px 0; }
.pl-card-title { font-weight: 400; color: var(--pl-gold-light); line-height: 1.5; margin-bottom: 8px; letter-spacing: 0.04em; }
.pl-card-desc { color: var(--pl-muted); font-size: 0.9em; line-height: 1.7; }
.pl-item { display: flex; align-items: flex-start; gap: 14px; padding: 13px 0; border-bottom: 1px solid rgba(200,164,90,0.14); }
.pl-item:last-child { border-bottom: none; }
.pl-num { flex: none; width: 30px; height: 30px; background: linear-gradient(135deg,rgba(192,57,43,0.35),rgba(192,57,43,0.18)); color: var(--pl-gold-light); border: 1px solid rgba(192,57,43,0.45); border-radius: 3px; font-weight: 400; font-size: 0.9em; display: flex; align-items: center; justify-content: center; }
.pl-item-body { flex: 1; }
.pl-item-title { color: var(--pl-text); font-weight: 400; line-height: 1.5; letter-spacing: 0.03em; }
.pl-item-desc { color: var(--pl-muted); font-size: 0.86em; line-height: 1.7; margin-top: 4px; }
.pl-quote { background: linear-gradient(135deg,rgba(192,57,43,0.10),rgba(192,57,43,0.04)); border-left: 2.5px solid var(--pl-crimson); border-radius: 0 8px 8px 0; padding: 15px 20px; color: var(--pl-gold-light); font-size: 0.98em; line-height: 1.75; margin: 22px 0; letter-spacing: 0.03em; }
.pl-tag { display: inline-block; background: rgba(192,57,43,0.28); color: var(--pl-gold-light); border: 1px solid rgba(200,164,90,0.3); border-radius: 3px; font-size: 0.8em; font-weight: 400; padding: 4px 12px; margin: 4px 6px 4px 0; letter-spacing: 0.04em; }
.pl-divider { border: none; height: 1px; background: linear-gradient(to right,transparent,rgba(200,164,90,0.35),transparent); margin: 30px 0; }
.pl-footer { background: rgba(192,57,43,0.08); border-left: 2.5px solid var(--pl-crimson); border-radius: 6px; padding: 13px 18px; margin-top: 34px; color: var(--pl-muted); font-size: 0.8em; line-height: 1.7; letter-spacing: 0.03em; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="pl-header">
        <div class="pl-title">故宫<em>红墙</em><br>金瓦朱阁的东方气韵</div>
        <div class="pl-subtitle">深棕木底、朱砂红与鎏金字，书法字体点睛，尽显宫廷的庄重华贵。</div>
    </div>
    <div class="pl-quote">红墙金瓦，一砖一瓦皆是千年气韵。</div>
    <div class="pl-section-title">核心特征</div>
    <div class="pl-card"><div class="pl-card-title">鎏金朱红</div><div class="pl-card-desc">鎏金字配朱砂红强调，深棕木底衬托，庄重华贵。</div></div>
    <div class="pl-card"><div class="pl-card-title">书法字韵</div><div class="pl-card-desc">中文书法字体点睛，东方古典气质浓厚。</div></div>
    <div class="pl-section-title">适用场景</div>
    <div class="pl-item"><div class="pl-num">1</div><div class="pl-item-body"><div class="pl-item-title">中国历史 / 文化艺术</div><div class="pl-item-desc">宫廷气质契合传统文化题材。</div></div></div>
    <div class="pl-item"><div class="pl-num">2</div><div class="pl-item-body"><div class="pl-item-title">国风节日 / 文博展览</div><div class="pl-item-desc">庄重华贵提升仪式感。</div></div></div>
    <div class="pl-divider"></div>
    <div>
        <span class="pl-tag">故宫</span>
        <span class="pl-tag">朱砂红</span>
        <span class="pl-tag">鎏金</span>
        <span class="pl-tag">东方美学</span>
    </div>
    <div class="pl-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #C8A45A;
    --t2e-accent-soft: rgba(200,164,90,0.12);
    --t2e-bg: #0E0604;
    --t2e-surface: #1A0A06;
    --t2e-text: #F0E6C8;
    --t2e-muted: #9A8060;
    --t2e-border: rgba(200,164,90,0.22);
}
```


### 字体注入（必须）

本风格声明了特色字体，**必须**在 HTML `<head>` 中加入以下字体链接，否则无头环境渲染时会退化为系统默认字体、失去风格气质：

```html
<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
```

> 截图脚本会自动等待 `document.fonts.ready`（最多 8s），字体加载由 export_image.js 保证。若 CDN 不可达，fallback 到 CSS 字体栈中的系统字体，不阻塞出图。若 googleapis 失效可换镜像 fonts.font.im / fonts.loli.net（同路径）。

### 点睛装饰（建议使用）

故宫风加「回纹边饰 + 印章」更显宫廷气：

```css
/* 顶部回纹带：inline SVG 万字纹重复 */
.pl-fret { height: 12px; margin-bottom: 24px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='12'%3E%3Cpath d='M2 10V2h8v4H6v4H2zm12 0V6h4V2h4v8h-8z' fill='none' stroke='rgba(200%2C164%2C90%2C0.5)' stroke-width='1'/%3E%3C/svg%3E");
    background-size: 24px 12px; background-repeat: repeat-x; }
/* 朱砂印章：正方描边 + 书法字，放标题旁或 footer */
.pl-seal { display: inline-flex; align-items: center; justify-content: center;
    width: 44px; height: 44px; border: 2px solid #C0392B; border-radius: 4px;
    color: #C0392B; font-size: 1.05em; line-height: 1.1; text-align: center;
    box-shadow: inset 0 0 0 1px rgba(192,57,43,0.25); letter-spacing: 0;
    writing-mode: vertical-rl; padding: 2px; }
```

```html
<div class="pl-fret"></div>
<span class="pl-seal">御制</span>
```
