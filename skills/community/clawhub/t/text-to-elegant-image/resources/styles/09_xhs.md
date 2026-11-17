## 9. 小红书风 (XiaoHongShu / REDNote)

适用：知识分享、生活攻略、干货笔记、好物推荐、任何想在小红书传播的内容。

**两种模式，由用户指定；未指定时默认模式 A：**

| 模式 | 触发词 | 气质 |
|------|-------|------|
| **A — 简洁正式** | "简单"/"正式"/"干净"/"知识感" | 呼吸感强，像写得好的知识笔记 |
| **B — 丰富活泼** | "活泼"/"丰富"/"可爱"/"生活"/"有趣" | 轻快温暖，像让人想收藏的生活攻略 |

**共用设计原则：**
- 背景白/极淡暖粉，**不用深色背景**
- 主色调：柔和珊瑚红 `#FF6B8A`（降饱和度，不用官方高饱和 `#FF2442`）
- 标题用红色，正文用深灰，靠色块和间距分层
- 严禁 emoji，序号用 CSS 圆圈或数字下划线

---

### 模式 A — 简洁正式 CSS（v3）

**主色调：** 小红书官方红 `#FF2442`（用户确认，锁定）  
**v2→v3 变更：** `#FF6B8A` → `#FF2442`，卡片底色调整为 `#FFF5F7`。  
**v2 优化（保留）：** MagicPattern 背景斜纹；加深边框；序号gap加大；标题横线加长渐变；Footer渐变分割线。

```css
:root {
    --bg: #FFFFFF;
    --text-main: #1A1A1A;
    --text-sub: #555555;
    --text-muted: #999999;
    --accent: #FF2442;
    --accent-light: rgba(255, 36, 66, 0.08);
    --accent-border: rgba(255, 36, 66, 0.28);
    --border: rgba(0, 0, 0, 0.06);
}
body {
    background: var(--bg);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    margin: 0; padding: 0;
    line-height: 1.8;
    /* MagicPattern: 极淡45度斜纹，增加纸张质感 */
    background-image: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 12px,
        rgba(255, 36, 66, 0.025) 12px,
        rgba(255, 36, 66, 0.025) 13px
    );
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 48px 36px;
    background: var(--t2e-surface, #FFF5F7);
    border: 1px solid var(--t2e-border, rgba(255,36,66,0.28));
    border-radius: 20px;
    box-shadow: 0 4px 28px rgba(255,36,66,0.08);
}
/* 标题区 */
.xhs-header {
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--accent-border);
}
.xhs-title {
    font-size: 2em;
    font-weight: 800;
    color: var(--accent);
    line-height: 1.25;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
    word-break: keep-all;
    overflow-wrap: break-word;
}
/* 标题下方装饰线（加长到48px，更有分量） */
.xhs-title-line {
    width: 48px;
    height: 3px;
    background: linear-gradient(to right, var(--accent), rgba(255,36,66,0.3));
    border-radius: 2px;
    margin: 10px 0 12px;
}
.xhs-subtitle {
    font-size: 0.88em;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    word-break: keep-all;
}
/* 内容卡片（简洁版：加深边框 + 微粉底） */
.xhs-card {
    background: #FFF5F7;
    border: 1px solid var(--accent-border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.xhs-card-title {
    font-size: 1.0em;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 6px;
    word-break: keep-all;
    overflow-wrap: break-word;
    display: flex;
    align-items: baseline;
    gap: 12px; /* 加大序号与标题间距 */
}
/* 序号：数字 + 渐变下划线（简洁版） */
.xhs-num {
    font-size: 0.9em;
    font-weight: 700;
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
    line-height: 1;
    padding-bottom: 1px;
    flex-shrink: 0;
    min-width: 16px;
    text-align: center;
}
.xhs-card-body {
    font-size: 0.86em;
    color: var(--text-sub);
    line-height: 1.8;
    word-break: keep-all;
    overflow-wrap: break-word;
}
/* 高亮引用 */
.xhs-quote {
    background: var(--accent-light);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.88em;
    color: var(--text-sub);
    font-style: italic;
    line-height: 1.75;
    margin: 14px 0;
    word-break: keep-all;
}
/* 标签（简洁版：方形pill粉边） */
.xhs-tag {
    display: inline-block;
    background: rgba(255,107,138,0.06);
    color: var(--text-muted);
    border: 1px solid rgba(255,107,138,0.2);
    border-radius: 4px;
    padding: 2px 9px;
    font-size: 0.75em;
    margin: 3px 3px 0 0;
    letter-spacing: 0.02em;
}
/* 分割线（简洁版：渐变淡出） */
.xhs-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--accent-border) 20%, var(--accent-border) 80%, transparent);
    margin: 18px 0;
}
/* Footer（简洁版：渐变分割线 + 账号名） */
.xhs-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.75em;
    padding-top: 20px;
    margin-top: 24px;
    letter-spacing: 0.06em;
    border-top: none;
    position: relative;
}
.xhs-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--accent-border), transparent);
}
p, li { word-break: keep-all; overflow-wrap: break-word; }
```

---

### 模式 B — 丰富活泼 CSS（v3）

**主色调：** 小红书官方红 `#FF2442`（用户确认，锁定）  
**v2→v3 变更：** `#FF6B8A` → `#FF2442`，背景/卡片底色跟随调整。  
**v2 优化（保留）：** Hero Patterns 圆点纹；Glassmorphism毛玻璃；padding收紧；Footer渐变分割线。

```css
:root {
    --bg: #FFF5F7;
    --card-bg: rgba(255, 230, 235, 0.85); /* 毛玻璃用半透明 */
    --text-main: #1A1A1A;
    --text-sub: #555555;
    --text-muted: #999999;
    --accent: #FF2442;
    --accent-light: rgba(255, 36, 66, 0.10);
    --accent-mid: rgba(255, 36, 66, 0.25);
    --border: rgba(255, 36, 66, 0.18);
}
body {
    background: var(--bg);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    margin: 0; padding: 0;
    line-height: 1.8;
    /* Hero Patterns: 极细圆点纹（手账纸质感） */
    background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='10' cy='10' r='1.2' fill='rgba(255%2C36%2C66%2C0.12)'/%3E%3C/svg%3E");
    background-size: 20px 20px;
}
.container {
    max-width: 560px;
    margin: 0 auto;
    padding: 44px 32px;
    background: var(--t2e-surface, #FFF5F7);
    border: 1px solid var(--t2e-border, rgba(255,36,66,0.28));
    border-radius: 20px;
    box-shadow: 0 4px 28px rgba(255,36,66,0.08);
}
/* 标题区（活泼版） */
.xhs-header {
    text-align: center;
    margin-bottom: 24px;
}
.xhs-title {
    font-size: 2.1em;
    font-weight: 800;
    color: var(--accent);
    line-height: 1.25;
    letter-spacing: -0.01em;
    margin-bottom: 6px;
    word-break: keep-all;
    overflow-wrap: break-word;
}
/* 标题下三段渐变横线装饰 */
.xhs-wave {
    display: flex;
    justify-content: center;
    gap: 4px;
    margin: 10px auto 14px;
}
.xhs-wave span {
    display: inline-block;
    width: 28px;
    height: 4px;
    border-radius: 2px;
}
.xhs-wave span:nth-child(1) { background: var(--accent); opacity: 0.9; }
.xhs-wave span:nth-child(2) { background: var(--accent); opacity: 0.5; width: 14px; }
.xhs-wave span:nth-child(3) { background: var(--accent); opacity: 0.25; width: 7px; }
.xhs-subtitle {
    font-size: 0.88em;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    word-break: keep-all;
}
/* 内容卡片（活泼版：Glassmorphism毛玻璃 + 大圆角 + 微阴影） */
.xhs-card {
    background: var(--card-bg);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 107, 138, 0.22);
    border-radius: 20px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 2px 16px rgba(255, 107, 138, 0.10), inset 0 1px 0 rgba(255,255,255,0.6);
}
.xhs-card-title {
    font-size: 1.0em;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 10px; /* 加大标题与正文间距 */
    word-break: keep-all;
    overflow-wrap: break-word;
    display: flex;
    align-items: center;
    gap: 12px; /* 加大序号与标题间距 */
}
/* 序号：实心圆圈（活泼版） */
.xhs-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--accent);
    color: #FFFFFF;
    font-size: 0.72em;
    font-weight: 700;
    flex-shrink: 0;
    line-height: 1;
}
.xhs-card-body {
    font-size: 0.86em;
    color: var(--text-sub);
    line-height: 1.8;
    word-break: keep-all;
    overflow-wrap: break-word;
}
/* 高亮引用（活泼版） */
.xhs-quote {
    background: rgba(255, 107, 138, 0.08);
    border: 1px dashed var(--accent-mid);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.88em;
    color: var(--text-sub);
    font-style: italic;
    line-height: 1.75;
    margin: 14px 0;
    word-break: keep-all;
    text-align: center;
}
/* 标签（活泼版：pill形粉底红字） */
.xhs-tag {
    display: inline-block;
    background: rgba(255, 107, 138, 0.12);
    color: var(--accent);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75em;
    font-weight: 600;
    margin: 3px 3px 0 0;
    letter-spacing: 0.02em;
    box-shadow: 0 1px 4px rgba(255, 107, 138, 0.15);
}
/* 分割线（活泼版：渐变淡出） */
.xhs-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right,
        transparent,
        var(--accent-mid) 20%,
        var(--accent-mid) 80%,
        transparent
    );
    margin: 20px 0;
}
/* Footer（活泼版：渐变分割线 + 引导语 + 账号名） */
.xhs-footer {
    text-align: center;
    padding-top: 20px;
    margin-top: 16px;
    position: relative;
}
.xhs-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 15%; right: 15%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--accent-mid), transparent);
}
.xhs-footer-guide {
    font-size: 0.82em;
    color: var(--accent);
    font-weight: 600;
    margin-bottom: 6px;
    letter-spacing: 0.04em;
}
.xhs-footer-account {
    font-size: 0.72em;
    color: var(--text-muted);
    letter-spacing: 0.08em;
}
p, li { word-break: keep-all; overflow-wrap: break-word; }
```

**小红书风使用要点（v2）：**
- 未指定模式时默认**模式 A（简洁正式）**，生成后告知用户可切换"活泼版"
- 序号组件：模式A用 `.xhs-num`（数字+下划线），模式B用 `.xhs-num`（实心圆圈）——两种模式 class 名相同，CSS 实现不同
- 标题区：模式A用 `.xhs-title-line`（渐变横线 48px），模式B用 `.xhs-wave`（三段渐变横线居中）
- Footer：模式A `::before` 渐变分割线 + 账号名；模式B `::before` 渐变分割线 + 引导语（不超过12字）+ 账号名
- 严禁 emoji，所有装饰靠 CSS 实现
- **主色调**：两种模式统一用小红书官方红 `#FF2442`（已由用户确认锁定，勿随意改回柔和版）
- 背景：模式A白底 + MagicPattern 淡红斜纹；模式B `#FFF5F7` + Hero Patterns 圆点纹
- 卡片：模式A微粉底 `#FFF5F7` + 加深边框；模式B Glassmorphism 半透明毛玻璃 + 大圆角


### 组件变量映射（必须随风格 CSS 一起复制）

使用 `resources/components.css` 可视化组件时，把下面的变量映射与风格 CSS 一并放入 `<style>`（组件取色契约，7 变量）：

```css
:root {
    --t2e-accent: #FF2442;
    --t2e-accent-soft: rgba(255,36,66,0.08);
    --t2e-bg: #FFFFFF;
    --t2e-surface: #FFF5F7;
    --t2e-text: #1A1A1A;
    --t2e-muted: #999999;
    --t2e-border: rgba(255,36,66,0.28);
}
```
