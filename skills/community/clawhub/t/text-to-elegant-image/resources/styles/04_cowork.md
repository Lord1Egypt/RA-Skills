## 4. Cowork 轻科技风 (Cowork Light Tech)

适用：AI 工具介绍、内部产品手册、工作方法论、企业内部分享。

**升级亮点（v3 · Apple HIG 风格）：** 对齐苹果设计语言的协作工具视觉——苹果灰白背景 `#f5f5f7`、科技蓝 `#0066cc`、1.5px 精致边框、`#1d1d1f` 苹果同款深黑文字、神经网络节点背景（72节点 `rgba(0,102,204,0.35)`）、磨砂玻璃 Hero 卡片、Eyebrow 全大写宽字距、clamp 响应式字号。

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    /* 品牌蓝（科技蓝） */
    --blue:        #0066cc;
    --blue-soft:   #0077ed;
    --blue-light:  rgba(0, 102, 204, 0.06);
    --blue-mid:    rgba(0, 102, 204, 0.18);
    --blue-mid-2:  rgba(0, 102, 204, 0.28);
    /* 背景 & 表面 */
    --bg:          #f5f5f7;
    --surface:     #ffffff;
    /* 边框 */
    --border:      rgba(0, 0, 0, 0.09);
    --border-2:    rgba(0, 0, 0, 0.14);
    --border-hover: rgba(0, 102, 204, 0.28);
    /* 文字（苹果同款深黑） */
    --text:        #1d1d1f;
    --text-2:      #6e6e73;
    --text-3:      #86868b;
    /* 圆角 */
    --radius-xs:   6px;
    --radius-sm:   10px;
    --radius:      14px;
    --radius-lg:   18px;
    --radius-xl:   20px;
    --radius-pill: 999px;
    /* 动效 */
    --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
    --ease-md:  cubic-bezier(0.4, 0, 0.2, 1);
}

body {
    background-color: var(--bg);
    color: var(--text);
    font-family: -apple-system, 'SF Pro Display', 'SF Pro Text',
                 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    -webkit-font-smoothing: antialiased;
    margin: 0; padding: 0;
    line-height: 1.6;
    /* 神经网络节点背景：72节点分布，rgba(0,102,204) 科技蓝 */
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Ccircle cx='60' cy='60' r='2.2' fill='rgba(0%2C102%2C204%2C0.35)'/%3E%3Cline x1='60' y1='60' x2='120' y2='0'   stroke='rgba(0%2C102%2C204%2C0.07)' stroke-width='1'/%3E%3Cline x1='60' y1='60' x2='0'   y2='120' stroke='rgba(0%2C102%2C204%2C0.07)' stroke-width='1'/%3E%3Cline x1='60' y1='60' x2='120' y2='120' stroke='rgba(0%2C102%2C204%2C0.05)' stroke-width='1'/%3E%3C/svg%3E");
    background-size: 120px 120px;
}

/* 遮罩层：苹果灰白渐变，让节点背景若隐若现 */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: linear-gradient(160deg, rgba(245,245,247,0.72) 0%, rgba(245,245,247,0.45) 100%);
    pointer-events: none;
    z-index: 0;
}

.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 44px 28px;
    position: relative;
    z-index: 1;
    background: var(--surface, #FFFFFF);
    border: 1px solid var(--border, rgba(0,0,0,0.09));
    border-radius: var(--radius-lg, 18px);
    box-shadow: 0 2px 24px rgba(0,0,0,0.06);
}

/* ── Hero 区：磨砂玻璃大卡片 ── */
.hero {
    text-align: center;
    padding: clamp(28px, 4vh, 44px) clamp(24px, 3vw, 40px);
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-xl);
}

/* Eyebrow：全大写 + 宽字距，建立视觉层次 */
.eyebrow {
    font-size: 0.62em;
    font-weight: 800;
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin-bottom: 10px;
}

.hero-title {
    font-size: clamp(1.9em, 4.5vw, 2.6em);
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.05em;
    line-height: 1.15;
    margin-bottom: 10px;
    word-break: keep-all;
}

/* Gradient text：标题渐变高亮（Apple HIG 同款） */
.hero-title .accent {
    background: linear-gradient(118deg, #1a4a8c 0%, #0066cc 55%, #0077ed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: var(--text-2);
    font-size: clamp(0.82em, 1.1vw, 0.95em);
    letter-spacing: 0.01em;
    line-height: 1.6;
}

/* ── 内容卡片：1.5px 精致边框 ── */
.cowork-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: clamp(20px, 2.5vh, 28px) clamp(18px, 2.5vw, 26px);
    margin-bottom: 14px;
    transition:
        border-color 0.25s var(--ease-md),
        box-shadow   0.25s var(--ease-md),
        transform    0.25s var(--ease-md);
}

/* Accent 卡片（蓝色渐变底） */
.cowork-card-accent {
    background: linear-gradient(135deg, #eef5ff 0%, #dbeafe 100%);
    border: 1.5px solid rgba(0, 102, 204, 0.20);
    border-radius: var(--radius-lg);
    padding: clamp(18px, 2.5vh, 24px) clamp(18px, 2.5vw, 28px);
    margin-bottom: 14px;
    box-shadow: 0 4px 20px rgba(0, 102, 204, 0.10);
}

/* Section title：Eyebrow 风格，全大写宽字距 */
.section-title {
    font-size: 0.62em;
    font-weight: 800;
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin: 0 0 12px;
}

.card-title {
    font-size: clamp(1.1em, 1.8vw, 1.32em);
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.03em;
    margin-bottom: 6px;
    word-break: keep-all;
    line-height: 1.3;
}

.card-desc {
    font-size: clamp(0.82em, 1.1vw, 0.92em);
    color: var(--text-2);
    line-height: 1.65;
    word-break: keep-all;
}

/* Highlight 引用块 */
.highlight {
    background: var(--blue-light);
    border-left: 3px solid var(--blue);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 14px 18px;
    font-size: 0.9em;
    color: var(--text);
    margin: 14px 0;
    line-height: 1.7;
}
.highlight strong { color: var(--blue); }

/* Badge 标签（pill 形） */
.badge {
    display: inline-block;
    background: var(--blue-light);
    color: var(--blue);
    border: 1px solid var(--blue-mid);
    border-radius: var(--radius-pill);
    padding: 3px 11px;
    font-size: 0.78em;
    font-weight: 600;
    margin: 3px 3px 3px 0;
    letter-spacing: 0.02em;
}
.badge-gray {
    display: inline-block;
    background: rgba(0,0,0,0.05);
    color: var(--text-2);
    border: 1px solid var(--border-2);
    border-radius: var(--radius-pill);
    padding: 3px 11px;
    font-size: 0.78em;
    font-weight: 500;
    margin: 3px 3px 3px 0;
}
.badge-green {
    display: inline-block;
    background: rgba(52, 199, 89, 0.08);
    color: #1a7a35;
    border: 1px solid rgba(52, 199, 89, 0.25);
    border-radius: var(--radius-pill);
    padding: 3px 11px;
    font-size: 0.78em;
    font-weight: 600;
    margin: 3px 3px 3px 0;
}

/* 分割线 */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 18px 0;
}

/* 列表：实心蓝点 */
.cowork-list { list-style: none; padding: 0; margin: 0; }
.cowork-list li {
    padding: 9px 0 9px 18px;
    border-bottom: 1px solid var(--border);
    font-size: clamp(0.82em, 1.1vw, 0.9em);
    color: var(--text-2);
    position: relative;
    line-height: 1.6;
    word-break: keep-all;
}
.cowork-list li:last-child { border-bottom: none; }
.cowork-list li::before {
    content: '';
    position: absolute;
    left: 0; top: 50%;
    transform: translateY(-50%);
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--blue);
}

/* 对比表格（两列） */
.compare-row {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}
.compare-cell {
    flex: 1;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 16px;
    font-size: 0.85em;
    color: var(--text-2);
    line-height: 1.5;
}
.compare-cell .label {
    font-size: 0.75em;
    font-weight: 700;
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}

/* 进度条 */
.progress-wrap {
    background: var(--blue-light);
    border-radius: var(--radius-xs);
    height: 5px;
    margin-top: 8px;
    overflow: hidden;
}
.progress-bar {
    height: 100%;
    border-radius: var(--radius-xs);
    background: linear-gradient(90deg, #0066cc, #0077ed);
}

/* 数字卡片（KPI 展示） */
.metric-row {
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
}
.metric-card {
    flex: 1;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 14px;
    text-align: center;
}
.metric-card .metric-value {
    font-size: clamp(1.4em, 2.2vw, 1.8em);
    font-weight: 700;
    color: var(--blue);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-card .metric-label {
    font-size: 0.72em;
    color: var(--text-3);
    font-weight: 500;
}

/* Footer */
.footer {
    text-align: center;
    color: var(--text-3);
    font-size: 0.72em;
    padding-top: 24px;
    letter-spacing: 0.08em;
    border-top: 1px solid var(--border);
    margin-top: 8px;
}
```


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #0066CC;
    --t2e-accent-soft: rgba(0,102,204,0.06);
    --t2e-bg: #F5F5F7;
    --t2e-surface: #FFFFFF;
    --t2e-text: #1D1D1F;
    --t2e-muted: #6E6E73;
    --t2e-border: rgba(0,0,0,0.09);
}
```
