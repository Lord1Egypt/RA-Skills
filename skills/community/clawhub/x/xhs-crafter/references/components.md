# Components Specification

> xhs-crafter 组件规范——字体、排版、间距、容器
> 画布基准：1080 × 1440（3:4）

---

## 一、Font Stacks

### Editorial Magazine

```css
:root {
  --serif-zh: "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
  --serif-en: "Playfair Display", "Noto Serif SC", serif;
  --sans-zh:  "Noto Sans SC", "Source Han Sans SC", "PingFang SC", sans-serif;
  --sans-en:  "Inter", "Noto Sans SC", sans-serif;
  --mono:     "IBM Plex Mono", "JetBrains Mono", monospace;
}
```

### Swiss International

```css
:root {
  --sans:    "Inter", "Noto Sans SC", sans-serif;
  --sans-zh: "Noto Sans SC", "Source Han Sans SC", "PingFang SC", sans-serif;
  --mono:    "IBM Plex Mono", "JetBrains Mono", monospace;
}
```

### 加载方式（Google Fonts）

```
Editorial:
  Noto Serif SC:wght@400;500;700
  Playfair Display:ital,wght@0,400;0,500;0,700;1,400;1,500
  Noto Sans SC:wght@400;500;700
  Inter:wght@400;500;600
  IBM Plex Mono:wght@400;500

Swiss:
  Inter:wght@200;300;400;500;600
  Noto Sans SC:wght@400;500;700
  IBM Plex Mono:wght@400;500
```

---

## 二、Type Scale

### 字重铁律："越大越轻"

字号越大，字重越轻；字号越小，字重越重。这是印刷行业的百年传统——大标题用轻字重保持优雅，小文字用重字重保证可读。

| 字号范围 | 字重 | 原因 |
|---------|------|------|
| ≥110px（Display/XL） | 500 | 大字号本身已有视觉重量，500足够醒目 |
| 60-80px（MD/Pull Quote） | 500 | 中等字号需要适度加粗维持存在感 |
| 32-46px（Lead/Body/Sub） | 400 | 阅读字号，400最舒适 |
| 24-26px（Kicker/Meta/Label） | 500 | 小字号必须加粗才能在缩放后可读 |

**反模式**：
- 大标题用 700/900 字重 → 像PPT不像杂志
- 正文用 300 字重 → 手机端模糊不可读
- Swiss 大标题用 600 → 破坏极简感，Swiss 大标题必须 ≤300

### Editorial Magazine（3:4 默认 1080×1440）

> **权威定义**：本文档为字号/间距的唯一权威来源，模板必须与本文档保持一致。

| Role | Class | Size | Weight | Tracking | Family |
|------|-------|------|--------|----------|--------|
| Display | `.h-display` | 136px | 500 | +.04em | serif-zh |
| Section title | `.h-xl` | 110px | 500 | +.03em | serif-zh |
| Mid title | `.h-md` | 60px | 500 | +.02em | serif-zh |
| Subtitle | `.h-sub` | 46px | 400 italic | normal | serif-en |
| Pull quote | `.pullquote` | 80px | 500 italic | normal | serif-zh |
| Lead | `.lead` | 34px | 400 | normal | serif-zh |
| Body | `.body` | 32px | 400 | normal | serif-zh |
| Kicker | `.kicker` | 26px | 500 | +.22em | mono |
| Meta | `.meta` | 24px | 500 | +.20em | mono |
| Label | `.label` | 24px | 500 | +.20em | mono |
| Stat number | `.stat-nb` | 72px | 500 | normal | serif-zh |
| Step title | `.step-title` | 34px | 500 | normal | serif-zh |
| Step desc | `.step-desc` | 28px | 400 | normal | serif-zh |
| Ledger title | `.ledger-title` | 30px | 500 | normal | serif-zh |

**CSS 示例：**

```css
.h-display {
  font-family: var(--serif-zh);
  font-size: 136px;
  font-weight: 500;
  letter-spacing: .04em;
  line-height: 1.1;
  color: var(--ink);
}

.h-xl {
  font-family: var(--serif-zh);
  font-size: 110px;
  font-weight: 500;
  letter-spacing: .03em;
  line-height: 1.15;
  color: var(--ink);
}

.h-md {
  font-family: var(--serif-zh);
  font-size: 60px;
  font-weight: 500;
  letter-spacing: .02em;
  line-height: 1.2;
  color: var(--ink);
}

.h-sub {
  font-family: var(--serif-en);
  font-size: 46px;
  font-weight: 400;
  font-style: italic;
  letter-spacing: normal;
  line-height: 1.3;
  color: var(--muted);
}

.pullquote {
  font-family: var(--serif-zh);
  font-size: 80px;
  font-weight: 500;
  font-style: italic;
  letter-spacing: normal;
  line-height: 1.25;
  color: var(--ink);
}

.lead {
  font-family: var(--serif-zh);
  font-size: 34px;
  font-weight: 400;
  letter-spacing: normal;
  line-height: 1.7;
  color: var(--ink);
}

.body {
  font-family: var(--serif-zh);
  font-size: 32px;
  font-weight: 400;
  letter-spacing: normal;
  line-height: 1.8;
  color: var(--ink);
}

.kicker {
  font-family: var(--mono);
  font-size: 26px;
  font-weight: 500;
  letter-spacing: .22em;
  text-transform: uppercase;
  line-height: 1.4;
  color: var(--accent);
}

.meta {
  font-family: var(--mono);
  font-size: 24px;
  font-weight: 500;
  letter-spacing: .20em;
  text-transform: uppercase;
  line-height: 1.4;
  color: var(--muted);
}
```

### 封面/封底满铺图页标题颜色

封面和封底使用满铺背景图时，标题必须使用纯白色 + text-shadow，确保与任何背景图都有足够对比度：

```css
.hero-content .h-display { color: #ffffff; text-shadow: 0 2px 16px rgba(0,0,0,.45); }
.hero-content .h-xl { color: #ffffff; text-shadow: 0 2px 12px rgba(0,0,0,.35); }
```

**硬规则**：
- 满铺图页标题禁止使用 `#ece2cf`（暖米色）——与暖调背景图太接近
- 必须使用 `#ffffff`（纯白）+ `text-shadow` 确保可读性
- text-shadow 不可省略——纯白字在亮色区域仍需阴影托底

---

### Swiss International（3:4 默认 1080×1440）

| Role | Class | Size | Weight | Family |
|------|-------|------|--------|--------|
| Hero | `.h-hero` | 240px | 200 | sans |
| Statement | `.h-statement` | 180px | 200 | sans |
| Section title | `.h-xl` | 128px | 300 | sans |
| Mid title | `.h-md` | 60px | 400 | sans |
| Mega number | `.num-mega` | 216px | 200 | sans |
| XL number | `.num-xl` | 156px | 200 | sans |
| Lead | `.lead` | 34px | 400 | sans-zh |
| Body | `.body` | 32px | 400 | sans-zh |
| Category | `.t-cat` | 26px | 600 | sans |
| Meta | `.t-meta` | 24px | 500 | mono |

**CSS 示例：**

```css
.h-hero {
  font-family: var(--sans);
  font-size: 240px;
  font-weight: 200;
  line-height: .9;
  letter-spacing: -.03em;
  color: var(--ink);
}

.h-statement {
  font-family: var(--sans);
  font-size: 180px;
  font-weight: 200;
  line-height: .92;
  letter-spacing: -.02em;
  color: var(--ink);
}

.h-xl {
  font-family: var(--sans);
  font-size: 128px;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -.02em;
  color: var(--ink);
}

.h-md {
  font-family: var(--sans);
  font-size: 60px;
  font-weight: 400;
  line-height: 1.15;
  letter-spacing: normal;
  color: var(--ink);
}

.num-mega {
  font-family: var(--sans);
  font-size: 216px;
  font-weight: 200;
  line-height: .9;
  letter-spacing: -.03em;
  color: var(--accent);
}

.num-xl {
  font-family: var(--sans);
  font-size: 156px;
  font-weight: 200;
  line-height: .9;
  letter-spacing: -.02em;
  color: var(--accent);
}

.lead {
  font-family: var(--sans-zh);
  font-size: 34px;
  font-weight: 400;
  line-height: 1.7;
  letter-spacing: normal;
  color: var(--ink);
}

.body {
  font-family: var(--sans-zh);
  font-size: 32px;
  font-weight: 400;
  line-height: 1.75;
  letter-spacing: normal;
  color: var(--ink);
}

.t-cat {
  font-family: var(--sans);
  font-size: 26px;
  font-weight: 600;
  letter-spacing: .12em;
  text-transform: uppercase;
  line-height: 1.4;
  color: var(--accent);
}

.t-meta {
  font-family: var(--mono);
  font-size: 24px;
  font-weight: 500;
  letter-spacing: .08em;
  text-transform: uppercase;
  line-height: 1.4;
  color: var(--grey-3);
}
```

---

## 三、Chinese Title Length Bands

中文标题字数与字号的映射关系——字数越多，字号越小，保证标题不换行或至多换一行。

### 标题一致性铁律

**同一套卡片中，所有内容页主标题必须使用同一字号 class。**

| 页面类型 | Editorial | Swiss | 说明 |
|---------|-----------|-------|------|
| 封面 (P01) | `.h-display` 136px | `.h-hero`/`.h-statement` | 允许更大字号 |
| 内容页 (P02-P08) | `.h-xl` 110px | `.h-xl` 128px | **必须统一** |
| 封底 (P09) | `.h-display` 136px | 视设计而定 | 与封面同级，形成"书挡" |

**适配方法**：标题太长时拆为两行（`<br>`），太短时加副标题增加视觉重量。**不得降级到 `.h-md`**。

**反模式**：不同内容页混用 `.h-xl` 和 `.h-md` → 视觉不统一，用户一眼看出不一致。

### Editorial Magazine

| 字数范围 | 推荐字号 | 使用 Class | 备注 |
|----------|----------|------------|------|
| 1–3 字 | 136px | `.h-display` | 单字 / 双字标题，最大冲击 |
| 4–6 字 | 110px | `.h-xl` | 常规章节标题 |
| 7–10 字 | 60px | `.h-md` | 中等长度标题 |
| 11–16 字 | 46px | `.h-sub` | 长标题，降级为副标题尺度 |
| 17+ 字 | 34px | `.lead` | 超长标题，按 lead 处理 |

### Swiss International

| 字数范围 | 推荐字号 | 使用 Class | 备注 |
|----------|----------|------------|------|
| 1–2 字 | 240px | `.h-hero` | 极简冲击，1–2 字 |
| 3–4 字 | 180px | `.h-statement` | 声明式标题 |
| 5–8 字 | 128px | `.h-xl` | 章节标题 |
| 9–14 字 | 60px | `.h-md` | 中等标题 |
| 15+ 字 | 32px | `.lead` | 长标题降级 |

> **硬规则**：标题最多换行 2 次。如果预估会超过 2 行，必须降级到下一档字号。

---

## 四、Minimum Readable Sizes（Mobile-Safe）

在 1080×1440 画布上，以下尺寸保证在手机端缩放后仍可读（约 360×480 逻辑像素下）。

| 角色 | 最小字号 | 说明 |
|------|----------|------|
| Body 正文 | 24px | 绝对底线，推荐 26px |
| Lead 导语 | 28px | 正文与标题的过渡 |
| Caption 图注 | 20px | 辅助信息，可略小 |
| Label 标签 | 20px | 按钮 / 标签文字 |
| Cell title 卡片标题 | 24px | 卡片内主标题 |
| Number annotation 数字注释 | 22px | 大数字旁的说明文字 |

> **硬规则**：任何文字不得低于 18px。18px 仅用于 meta 类辅助信息，且必须使用高对比度（ink 色）。

---

## 五、Image Container Ratios

### 可用比例

| Class | 比例 | padding-bottom | 典型用途 |
|-------|------|----------------|----------|
| `.r-3x4` | 3:4 | 133.33% | 小红书原生比例，人像、产品 |
| `.r-1x1` | 1:1 | 100% | 头像、图标、方形产品 |
| `.r-4x3` | 4:3 | 75% | 横版产品、场景 |
| `.r-3x2` | 3:2 | 66.67% | 经典横版，风景 |
| `.r-16x9` | 16:9 | 56.25% | 视频截图、宽屏 |
| `.r-16x10` | 16:10 | 62.5% | 笔记本屏幕截图 |
| `.r-21x9` | 21:9 | 42.86% | 超宽屏、电影感 |

**CSS 实现：**

```css
.r-3x4  { aspect-ratio: 3 / 4; }
.r-1x1  { aspect-ratio: 1 / 1; }
.r-4x3  { aspect-ratio: 4 / 3; }
.r-3x2  { aspect-ratio: 3 / 2; }
.r-16x9 { aspect-ratio: 16 / 9; }
.r-16x10{ aspect-ratio: 16 / 10; }
.r-21x9 { aspect-ratio: 21 / 9; }
```

### 使用指引

- **小红书卡片内嵌图**：优先 `.r-3x4`（与卡片比例一致）或 `.r-4x3`（横版内容）。
- **截图展示**：桌面用 `.r-16x10`，移动端用 `.r-3x4` 或 `.r-9x16`。
- **产品图**：`.r-1x1` 或 `.r-3x4`。
- **风景 / 场景**：`.r-3x2` 或 `.r-16x9`。
- **同一卡片内**：所有图片比例必须统一，禁止混用不同比例。

> **硬规则**：图片容器必须使用 aspect-ratio，禁止用固定高度。图片用 `object-fit: cover` 填充。

---

## 六、Spacing Tokens（Swiss）

Swiss 体系使用 8px 基础网格的间距 token。

| Token | 值 | 典型用途 |
|-------|----|----------|
| `--sp-3` | 8px | 图标与文字间距、内联元素间距 |
| `--sp-4` | 12px | 紧凑内边距、标签内间距 |
| `--sp-5` | 16px | 小卡片内边距、列表项间距 |
| `--sp-6` | 24px | 标准内边距、段落间距 |
| `--sp-7` | 32px | 区块间距、卡片内边距 |
| `--sp-8` | 40px | 大区块间距 |
| `--sp-9` | 48px | 章节间距 |
| `--sp-10` | 64px | 大章节间距 |
| `--sp-11` | 80px | 页面级间距 |
| `--sp-12` | 120px | 重大分隔 |
| `--sp-13` | 160px | 页面顶部 / 底部留白 |

**CSS 定义：**

```css
:root {
  --sp-3:  8px;
  --sp-4:  12px;
  --sp-5:  16px;
  --sp-6:  24px;
  --sp-7:  32px;
  --sp-8:  40px;
  --sp-9:  48px;
  --sp-10: 64px;
  --sp-11: 80px;
  --sp-12: 120px;
  --sp-13: 160px;
}
```

### 使用规则

1. **所有间距必须使用 token**，禁止硬编码像素值。
2. **同一层级元素间距一致**——所有段落间距用同一个 token。
3. **间距递增**——从内到外，token 序号递增（如卡片内 --sp-6，卡片间 --sp-8）。
4. **Editorial 体系**同样可使用这些 token，但允许更灵活的微调（如行首缩进 2em）。

---

## 七、Card Fills（Swiss Only）

Swiss 体系的卡片填充样式，**互斥使用**——一张卡片只能选择一种 fill。

### 可用 Fill

| Class | 效果 | 适用场景 |
|-------|------|----------|
| `.card-ink` | 背景为 ink 色，文字为 paper 色 | 强调卡片、数据高亮 |
| `.card-accent` | 背景为 accent 色，文字为 accent-on 色 | CTA 卡片、关键指标 |
| `.card-fill` | 背景为 grey-1 色，文字为 ink 色 | 次级信息卡片、引用块 |
| `.card-outlined` | 无背景，1px grey-2 边框，文字为 ink 色 | 轻量卡片、列表项 |

**CSS 实现：**

```css
.card-ink {
  background: var(--ink);
  color: var(--paper);
  padding: var(--sp-7);
}

.card-accent {
  background: var(--accent);
  color: var(--accent-on);
  padding: var(--sp-7);
}

.card-fill {
  background: var(--grey-1);
  color: var(--ink);
  padding: var(--sp-7);
}

.card-outlined {
  background: transparent;
  border: 1px solid var(--grey-2);
  color: var(--ink);
  padding: var(--sp-7);
}
```

### 硬规则

1. **互斥**：一张卡片只用一种 fill，禁止组合（如 `.card-ink.card-accent`）。
2. **card-accent 面积控制**：单张卡片内 accent 填充面积 ≤ 30%。
3. **card-ink 内禁止使用 muted 色**——ink 背景上只有 paper 和 accent-on 可读。
4. **card-outlined 不加 background**——透明背景是设计意图，不是遗漏。
5. **同一组卡片 fill 必须统一**——禁止同一组内混用不同 fill。

---

## 八、Screenshot Containers

### .frame-shot

截图容器组件，支持多种参数组合。

**参数：**

| 参数 | 值 | 说明 |
|------|----|------|
| `ratio` | `3x4` / `1x1` / `4x3` / `3x2` / `16x9` / `16x10` / `21x9` | 容器比例 |
| `corners` | `sq` / `sm` / `md` | 圆角大小：sq=0, sm=4px, md=12px |
| `shadow` | `none` / `soft` / `ed` | 阴影：none=无, soft=柔和扩散, ed=硬边投影 |
| `bg` | `paper` / `grid` / `dot` / `grey-1` / `ink` | 容器背景 |
| `inset` | `none` / `sub` / `bal` | 内边距：none=0, sub=8px, bal=24px |

**CSS 实现：**

```css
.frame-shot {
  overflow: hidden;
  position: relative;
}

/* ── corners ── */
.frame-shot[data-corners="sq"] { border-radius: 0; }
.frame-shot[data-corners="sm"] { border-radius: 4px; }
.frame-shot[data-corners="md"] { border-radius: 12px; }

/* ── shadow ── */
.frame-shot[data-shadow="none"] { box-shadow: none; }
.frame-shot[data-shadow="soft"] { box-shadow: 0 8px 32px rgba(0,0,0,.12); }
.frame-shot[data-shadow="ed"]   { box-shadow: 4px 4px 0 rgba(0,0,0,.15); }

/* ── bg ── */
.frame-shot[data-bg="paper"] { background: var(--paper); }
.frame-shot[data-bg="grid"]  {
  background-image:
    linear-gradient(var(--line) 1px, transparent 1px),
    linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size: 24px 24px;
  background-color: var(--paper);
}
.frame-shot[data-bg="dot"]   {
  background-image: radial-gradient(circle, var(--line) 1px, transparent 1px);
  background-size: 16px 16px;
  background-color: var(--paper);
}
.frame-shot[data-bg="grey-1"]{ background: var(--grey-1); }
.frame-shot[data-bg="ink"]   { background: var(--ink); }

/* ── inset ── */
.frame-shot[data-inset="none"] { padding: 0; }
.frame-shot[data-inset="sub"]  { padding: 8px; }
.frame-shot[data-inset="bal"]  { padding: 24px; }
```

---

### Device Wrappers

设备外壳容器，模拟浏览器或手机边框。

#### .device-browser

```css
.device-browser {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--grey-2);
  background: var(--paper);
}

.device-browser::before {
  content: "";
  display: block;
  height: 40px;
  background: var(--grey-1);
  border-bottom: 1px solid var(--grey-2);
  /* 三个圆点模拟浏览器控件 */
  background-image:
    radial-gradient(circle at 20px 20px, var(--grey-3) 4px, transparent 4px),
    radial-gradient(circle at 40px 20px, var(--grey-3) 4px, transparent 4px),
    radial-gradient(circle at 60px 20px, var(--grey-3) 4px, transparent 4px);
  background-repeat: no-repeat;
}
```

#### .device-phone

```css
.device-phone {
  border-radius: 32px;
  overflow: hidden;
  border: 3px solid var(--ink);
  background: var(--paper);
}

.device-phone::before {
  content: "";
  display: block;
  height: 28px;
  background: var(--ink);
  /* 顶部刘海 */
  clip-path: polygon(0 0, 100% 0, 100% 100%, 55% 100%, 50% 60%, 45% 100%, 0 100%);
}
```

---

### Style-Locked Defaults

不同体系下截图容器的默认参数锁定：

| 参数 | Swiss 默认 | Editorial 默认 |
|------|------------|----------------|
| `corners` | `sq` | `md` |
| `shadow` | `ed` | `soft` |
| `bg` | `paper` | `paper` |
| `inset` | `none` | `sub` |

**说明：**

- **Swiss**：方角 + 硬边投影 = 理性、精确。
- **Editorial**：圆角 + 柔和阴影 = 温润、纸感。

> **硬规则**：除非用户明确要求，否则不修改体系默认值。如需覆盖，必须同时说明原因。

---

## 九、使用速查

### 按体系选择组件

| 需求 | Editorial | Swiss |
|------|-----------|-------|
| 标题字体 | serif-zh / serif-en | sans |
| 正文字体 | serif-zh | sans-zh |
| 辅助字体 | mono | mono |
| 间距体系 | 灵活（可用 em） | 严格 token |
| 卡片填充 | 无 fill 体系 | card-ink / card-accent / card-fill / card-outlined |
| 截图圆角 | md（12px） | sq（0px） |
| 截图阴影 | soft | ed |
| 配色变量 | paper / paper-2 / ink / muted / line / accent / accent-soft | paper / ink / grey-1 / grey-2 / grey-3 / accent / accent-on |

### 组合禁忌

| 禁止 | 原因 |
|------|------|
| Editorial 字体 + Swiss 间距 token | 体系不匹配，视觉不协调 |
| Swiss fill + Editorial 配色变量 | 变量名不兼容 |
| 同一卡片混用不同 ratio 图片 | 视觉节奏断裂 |
| card-accent + 大面积 accent-soft | 双重强调 = 无强调 |
| .h-hero 用于超过 2 字的标题 | 字号过大，换行后失去冲击力 |
| .num-mega 使用 ink 色 | 大数字必须用 accent 色，否则无视觉锚点 |
