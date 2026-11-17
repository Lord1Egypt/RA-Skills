## 17. 暗色极简风 (Carbon)

适用：技术文档、开发者内容、数据报告、专业分析。

**风格亮点：** 炭灰深底（#14161A 三档递进）搭配冷调蓝绿（#4FB8C4），克制冷静，暗色护眼，技术专业感强。

```css
:root {
    --cb-bg: #14161A; --cb-surface: #1A1D23; --cb-card: #20242B;
    --cb-accent: #4FB8C4; --cb-accent2: #6CCFA8;
    --cb-text: #D6DAE0; --cb-muted: #8A929E;
    --cb-ft: "Inter","SF Mono","PingFang SC","Helvetica Neue",sans-serif;
}
body { background-color: var(--cb-bg); color: var(--cb-text); font-family: var(--cb-ft); line-height: 1.7; -webkit-font-smoothing: antialiased; }
.container { max-width: 560px; margin: 0 auto; padding: 48px 36px; background: var(--cb-surface); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; }
.cb-header { margin-bottom: 32px; }
.cb-title { font-size: 2.1em; font-weight: 700; letter-spacing: -0.01em; line-height: 1.25; color: var(--cb-text); word-break: keep-all; overflow-wrap: break-word; }
.cb-title em { color: var(--cb-accent); font-style: normal; }
.cb-subtitle { color: var(--cb-muted); font-size: 0.95em; line-height: 1.65; margin-top: 12px; word-break: keep-all; overflow-wrap: break-word; }
.cb-section-title { font-size: 1.15em; font-weight: 600; color: var(--cb-text); margin: 30px 0 14px; padding-left: 12px; border-left: 4px solid var(--cb-accent); word-break: keep-all; }
.cb-card { background: var(--cb-card); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; box-shadow: 0 2px 14px rgba(0,0,0,0.3); padding: 18px 20px; margin: 14px 0; }
.cb-card-title { font-weight: 600; color: var(--cb-text); line-height: 1.4; margin-bottom: 6px; }
.cb-card-desc { color: var(--cb-muted); font-size: 0.88em; line-height: 1.6; }
.cb-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.07); }
.cb-item:last-child { border-bottom: none; }
.cb-num { flex: none; width: 28px; height: 28px; background: rgba(79,184,196,0.16); color: var(--cb-accent); border-radius: 8px; font-weight: 700; font-size: 0.82em; display: flex; align-items: center; justify-content: center; }
.cb-item-body { flex: 1; }
.cb-item-title { color: var(--cb-text); font-weight: 500; line-height: 1.45; }
.cb-item-desc { color: var(--cb-muted); font-size: 0.84em; line-height: 1.6; margin-top: 3px; }
.cb-quote { background: rgba(79,184,196,0.10); border-left: 3px solid var(--cb-accent); border-radius: 0 10px 10px 0; padding: 14px 18px; color: var(--cb-text); font-size: 0.95em; line-height: 1.65; margin: 20px 0; }
.cb-tag { display: inline-block; background: rgba(79,184,196,0.14); color: var(--cb-accent); border-radius: 7px; font-size: 0.78em; font-weight: 600; padding: 3px 10px; margin: 4px 6px 4px 0; }
.cb-divider { border: none; height: 1px; background: rgba(255,255,255,0.1); margin: 28px 0; }
.cb-footer { background: rgba(79,184,196,0.08); border-left: 3px solid var(--cb-accent); border-radius: 10px; padding: 12px 16px; margin-top: 32px; color: var(--cb-muted); font-size: 0.8em; line-height: 1.65; }
p { word-break: keep-all; overflow-wrap: break-word; }
```

**HTML 结构示例：**

```html
<div class="container">
    <div class="cb-header">
        <div class="cb-title">暗色极简<br><em>克制</em>的技术美感</div>
        <div class="cb-subtitle">炭灰深底搭配冷调蓝绿，克制冷静，适合技术与专业场景。</div>
    </div>
    <div class="cb-quote">少即是多。深色是专注，蓝绿是理性。</div>
    <div class="cb-section-title">核心特征</div>
    <div class="cb-card"><div class="cb-card-title">炭灰深底</div><div class="cb-card-desc">#14161A 炭灰三档递进，层次清晰不刺眼。</div></div>
    <div class="cb-card"><div class="cb-card-title">冷调蓝绿</div><div class="cb-card-desc">#4FB8C4 克制的强调色，理性专业。</div></div>
    <div class="cb-section-title">适用场景</div>
    <div class="cb-item"><div class="cb-num">1</div><div class="cb-item-body"><div class="cb-item-title">技术文档 / 开发者内容</div><div class="cb-item-desc">暗色护眼，契合工程师审美。</div></div></div>
    <div class="cb-item"><div class="cb-num">2</div><div class="cb-item-body"><div class="cb-item-title">数据报告 / 专业分析</div><div class="cb-item-desc">冷静调性突出严肃内容。</div></div></div>
    <div class="cb-divider"></div>
    <div>
        <span class="cb-tag">暗色</span>
        <span class="cb-tag">极简</span>
        <span class="cb-tag">蓝绿</span>
        <span class="cb-tag">技术感</span>
    </div>
    <div class="cb-footer">text-to-elegant-image @ claude-4.8-opus</div>
</div>
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #4FB8C4;
    --t2e-accent-soft: rgba(79,184,196,0.14);
    --t2e-bg: #14161A;
    --t2e-surface: #20242B;
    --t2e-text: #D6DAE0;
    --t2e-muted: #8A929E;
    --t2e-border: rgba(255,255,255,0.08);
}
```

### 点睛装饰（建议使用）

暗色极简加「终端行号 + 状态点」，开发者气质立现：

```css
/* 卡片左侧行号栏（等宽字体） */
.cb-lined { display: flex; gap: 14px; }
.cb-lineno { flex: none; font-family: "SF Mono", "Courier New", monospace;
    font-size: 0.72em; color: rgba(138,146,158,0.4); text-align: right;
    line-height: 1.9; user-select: none; padding-top: 2px; }
/* 状态指示点：放 section-title 前，terminal prompt 感 */
.cb-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: #4FB8C4; box-shadow: 0 0 8px rgba(79,184,196,0.6); margin-right: 8px; }
/* 背景极淡网格 */
body { background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 24px 24px; }
```

```html
<div class="cb-section-title"><span class="cb-dot"></span>核心特征</div>
```
