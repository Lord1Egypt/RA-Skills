# Design System v7 (Dual Style + Theme Variables)

2 visual modes × 9 themes × CSS variable system + font three-tier division + spacing tokens + card classes + image ratios. Consolidated from 4 reference files.

---

## Phase 0: The Three Constraints (不可协商)

**All modes must obey. Style can vary, constraints are constant.**

### Constraint 1: 克制 (Restraint)

- Brand/accent color covers **≤ 5% of document surface area**
- Brand color is for: title left-bar, tags, CTA buttons, accent numbers only
- More than 5% brand color = ornament, not design
- **Single accent principle**: one chromatic color per design. No second chromatic color (exception: breaking-change badges registered as `--breaking-*` tokens)

### Constraint 2: 呼吸 (Breathing)

- Card spacing ≥ 2× content spacing (gap between cards > gap within cards)
- Section title margin-bottom ≥ 2× margin-above
- Whisper shadow only: `0 4pt 24pt rgba(0,0,0,0.05)`, never hard drop shadows
- Ring shadow for emphasis: `0 0 0 1pt var(--accent)`, not box-shadow with offset > 4px
- Border width: 0.5pt, border-radius: 8pt minimum for cards

### Constraint 3: 温度 (Warmth)

- **All grays must have warm undertone** (R ≈ G > B in RGB). No cool blue-grays.
- Forbidden: `#94A3B8`, `#CBD5E1`, `#E2E8F0`, `#F1F5F9`, `#F8FAFC`
- Required warm gray scale:
  ```css
  --near-black: #141413;   /* warm olive undertone */
  --dark-warm:  #3d3d3a;   /* secondary text */
  --olive:      #504e49;   /* subtext, descriptions */
  --stone:      #6b6a64;   /* tertiary, dates, metadata */
  --border:     #e8e6dc;   /* warm border */
  --parchment:  #f5f4ed;   /* warm cream background */
  --ivory:      #faf9f5;   /* card background */
  ```
- **Never** `#FFFFFF` as page background. Use `--paper` (theme variable) or `--parchment`.
- **Never** `#000000` as text color. Use `--ink` (theme variable) or `--near-black`.

### Serif Weight Lock

- Serif headings: weight 500 only. **Forbidden**: weight 600/700/900 on serif fonts
- Serif body: weight 400 only

### Anti-Slop Rules (8 Red Lines)

```
🚫 禁止连续三张配图用相同布局
🚫 禁止所有卡片居中排列（至少一张不对称）
🚫 禁止品牌色大面积铺底（≤5%面积）
🚫 禁止纯白背景（必须用暖色底）
🚫 禁止冷蓝灰色系（#94A3B8 这类）
🚫 禁止衬线体 font-weight: 700
🚫 禁止硬投影（box-shadow 偏移量 > 4px）
🚫 禁止 rgba 背景色标签（用 solid hex 替代）
```

---

## Phase 0.5: Dual Style System

Two visual stances — any topic can be rendered in either mode. Pick by editorial intent ("feature story" vs "release note"), not by topic lookup.

### Mode A: Editorial Magazine (杂志社论风)

**Visual anchors**: Serif/Songti display title + quiet sans body · Warm paper background · Atmosphere layer (grain/wash/gradient) · Magazine structure (columns, pull-quotes, marginalia) · Large purposeful whitespace · Fine rules (0.5pt)

**Good fits**: humanistic, cultural, narrative, reflective — also workplace essays, AI think-pieces, product retrospectives

**Themes**: 墨水经典, 森林墨, 牛皮纸, 沙丘, 莫兰迪, or any Brand DNA palette

### Mode B: Swiss International (瑞士国际主义风)

**Visual anchors**: Full sans-serif (Inter / Noto Sans SC), no serif · Light paper + near-black · Grid/dot matrix background · One high-saturation accent only · Strict left-aligned grid, hairline rules · Card-fill matrices, KPI towers, h-bar charts

**Good fits**: tech products, data reports, engineering, design, annual summaries

**Themes**: 克莱因蓝, 柠檬黄, 柠檬绿, 安全橙

### Style Identity Test

**Swiss** (ALL four must hold):
1. Every display title (≥48px) has font-weight ≤ 400
2. No serif family loaded. No `font-family: serif`
3. Separators are hairline rules or grid gutters, not card borders + drop shadows
4. Exactly one accent palette. No mixed accents

**Editorial** (ALL three must hold):
1. Background has atmosphere layer beyond flat fill (grain, gradient, wash)
2. Display title uses serif-zh family (Noto Serif SC / 汇文明朝体 / TsangerJinKai02)
3. Contains at least one: large photo well, serif pull-quote, marginalia column, or ledger

### Aesthetic Guardrails

- **Palette Lock**: Swiss → only 4 Swiss themes; Editorial → only 5 Editorial themes
- **Single Accent (Swiss)**: One chromatic accent per design set. No mixing
- **No Cross-Mode Mixing**: Swiss theme variables ≠ Editorial theme variables
- **Custom color**: Allow only with explicit brand hex + brand context → register as `--brand-accent`

---

## Theme CSS Variable System (主题变量系统)

每个主题由 6 个 CSS 变量定义。切换主题 = 替换 `:root`。所有 HTML 模板必须引用 `var(--xxx)` 获取颜色。

### 变量定义

```css
:root {
  --ink: #141413;        /* primary text — 主文字色 */
  --paper: #f5f4ed;      /* primary background — 主背景色 */
  --accent: #002FA7;     /* chromatic accent — 强调色 */
  --accent-on: #ffffff;  /* text on accent — 强调色上的文字 */
  --grey-1: #f0f0ee;     /* light block background — 浅色块背景 */
  --grey-2: #d4d4d2;     /* mid grey dividers — 中灰分隔线 */
}
```

### Editorial 主题 (5 个)

#### 1. 墨水经典 Ink Classic

```css
:root {
  --ink: #141413;
  --paper: #f5f4ed;
  --accent: #1B365D;
  --accent-on: #ffffff;
  --grey-1: #e8e6dc;
  --grey-2: #d4d2c8;
}
```

**气质**: 克制、经典、纸墨感。默认 Editorial 主题。

#### 2. 森林墨 Forest Ink

```css
:root {
  --ink: #1a2e1f;
  --paper: #f5f1e8;
  --accent: #2D5A3A;
  --accent-on: #ffffff;
  --grey-1: #e5e0d4;
  --grey-2: #c8c0b0;
}
```

**气质**: 自然、沉稳、林间书卷。

#### 3. 牛皮纸 Kraft Paper

```css
:root {
  --ink: #2a1e13;
  --paper: #eedfc7;
  --accent: #8B6F47;
  --accent-on: #ffffff;
  --grey-1: #e0d4bc;
  --grey-2: #c4b898;
}
```

**气质**: 手工、质朴、旧书质感。

#### 4. 沙丘 Dune

```css
:root {
  --ink: #1f1a14;
  --paper: #f0e6d2;
  --accent: #C17F59;
  --accent-on: #ffffff;
  --grey-1: #e4dac6;
  --grey-2: #c8bca4;
}
```

**气质**: 沙漠、温暖、旅行文学。

#### 5. 莫兰迪 Morandi

```css
:root {
  --ink: #3D3529;
  --paper: #F5F0E8;
  --accent: #8B7E74;
  --accent-on: #ffffff;
  --grey-1: #e8e2d8;
  --grey-2: #ccc4b8;
}
```

**气质**: 低饱和、高级灰、艺术评论。

### Swiss 主题 (4 个)

#### 1. 克莱因蓝 IKB

```css
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --accent-on: #ffffff;
  --grey-1: #f0f0ee;
  --grey-2: #d4d4d2;
}
```

**气质**: 学术、理性、AI/科技/设计。Swiss 默认主题。

#### 2. 柠檬黄 Lemon

```css
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #FFD500;
  --accent-on: #0a0a0a;
  --grey-1: #f0f0ee;
  --grey-2: #d4d4d2;
}
```

**气质**: 活力、年轻、消费/零售。

#### 3. 柠檬绿 Lemon Green

```css
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #C5E803;
  --accent-on: #0a0a0a;
  --grey-1: #f0f0ee;
  --grey-2: #d4d4d2;
}
```

**气质**: 未来、新兴、环保/Gen-Z。

#### 4. 安全橙 Safety Orange

```css
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #FF6B35;
  --accent-on: #ffffff;
  --grey-1: #f0f0ee;
  --grey-2: #d4d4d2;
}
```

**气质**: 工业、紧迫、汽车/制造。

### Swiss 附加灰阶变量

Swiss 主题额外使用一个三级灰（secondary text），不在 6 变量体系内但模板可能引用：

```css
--grey-3: #737373;   /* dark grey, secondary text */
```

### 硬规则 (Hard Rules)

```
🚫 所有 HTML 模板必须使用 var(--ink)、var(--paper) 等变量引用颜色
🚫 禁止在模板中硬编码主题色的 hex 值
✅ 唯一例外：非主题色（如照片遮罩 rgba）可以硬编码
🚫 禁止跨模式混用主题（Swiss 模板不能套 Editorial 主题变量）
```

---

## Font Three-Tier Division (字体三级分工)

核心洞察来自归藏：**衬线 = 观点，无衬线 = 信息，等宽 = 元数据**。读者无需思考——眼睛自动识别角色。

### Editorial 字体类 (640px 画布)

| 角色 | Class | 字号 | 字重 | 字距 | 字体族 | 语义 |
|------|-------|------|------|------|--------|------|
| 展示标题 | `.h-display` | 40-44px | 500 | +0.04em | serif-zh | 观点/核心论断 |
| 章节标题 | `.h-xl` | 28-32px | 500 | +0.03em | serif-zh | 观点/章节主张 |
| 中标题 | `.h-md` | 20-24px | 500 | +0.02em | serif-zh | 观点/小节标题 |
| 副标题 | `.h-sub` | 16-18px | 400 italic | normal | serif-en | 观点/辅助主张 |
| 引用 | `.pullquote` | 28-32px | 500 italic | normal | serif-zh | 观点/引用 |
| 导语 | `.lead` | 16-18px | 400 | normal | serif-zh | 信息/导语 |
| 正文 | `.body` | 14-16px | 400 | normal | serif-zh | 信息/正文 |
| 分类标签 | `.kicker` | 11-12px | 500 | +0.22em | mono | 元数据/分类标签 |
| 来源日期 | `.meta` | 10-11px | 500 | +0.20em | mono | 元数据/来源日期 |
| 标注 | `.label` | 10-11px | 500 | +0.20em | mono | 元数据/标注 |

### Swiss 字体类 (640px 画布)

| 角色 | Class | 字号 | 字重 | 字体族 | 语义 |
|------|-------|------|------|--------|------|
| 英雄标题 | `.h-hero` | 48-56px | 200-300 | sans | 信息/核心数据 |
| 声明 | `.h-statement` | 36-44px | 200-300 | sans | 信息/声明 |
| 章节标题 | `.h-xl` | 24-28px | 300-400 | sans | 信息/章节 |
| 中标题 | `.h-md` | 18-20px | 400 | sans | 信息/小节 |
| 超大数字 | `.num-mega` | 40-48px | 200-300 | sans | 信息/大数字 |
| 大数字 | `.num-xl` | 32-36px | 200-300 | sans | 信息/数据 |
| 导语 | `.lead` | 16-18px | 400 | sans-zh | 信息/导语 |
| 正文 | `.body` | 14-16px | 400 | sans-zh | 信息/正文 |
| 分类 | `.t-cat` | 12-13px | 600 | sans | 元数据/分类 |
| 来源 | `.t-meta` | 10-11px | 500 | mono | 元数据/来源 |

### Font Stacks (字体栈)

**Editorial:**

| 变量 | 字体栈 | 用途 |
|------|--------|------|
| `--serif-zh` | Noto Serif SC, Songti SC, STSong | 展示标题 |
| `--serif-en` | Playfair Display | 英文副标题、引用（italic） |
| `--sans-zh` | Noto Sans SC, PingFang SC | 工具文字、回退 |
| `--sans-en` | Inter | 混排中的拉丁正文 |
| `--mono` | IBM Plex Mono, JetBrains Mono | 标签、元数据、kicker |

**Swiss:**

| 变量 | 字体栈 | 用途 |
|------|--------|------|
| `--sans` | Inter, Helvetica Neue, Helvetica | 所有标题和英文 |
| `--sans-zh` | Noto Sans SC, PingFang SC | 中文正文 |
| `--mono` | IBM Plex Mono, JetBrains Mono | 标签、标注、t-meta |

### 字体硬规则

```
🚫 Swiss 模板禁止加载任何衬线字体
🚫 Editorial 模板禁止丢失衬线展示字体族
🚫 Editorial 正文和导语默认使用 serif-zh（不是 sans）
🚫 字号越大，字重越轻。44px+ 使用 600+ 字重 = 立即降级
```

### The Larger The Lighter

大字 → 轻字重；小字 → 重字重。这是"高级感"最有效的单条规则。44px+ 标题用 600+ 字重读起来是"普通落地页"，不是"杂志"。

### CJK Letter-Spacing

- Chinese body text with serif: `letter-spacing: 0.3pt`
- Chinese display text (24px+): `letter-spacing: 0.2-1pt`
- English body: `letter-spacing: 0`
- Small labels (< 10pt): `+0.2 to +0.5pt`

### Cover Type Scale (900×383 画布) — 使用字体类

封面和封底是 900×383 画布，比正文 640px 宽 40%，字号需要更大才能在手机缩略图中可读。

| 角色 | Class | 字号 | 字重 | 字距 | 字体族 |
|------|-------|------|------|------|--------|
| 封面标题 | `.h-display` | 44-52px | 300-400 | +0.03em | serif-zh / sans |
| 封面副标题 | `.h-sub` | 15-18px | 400 | normal | serif-en / sans |
| 封面元数据 | `.meta` | 11-13px | 500 | +0.15em | mono |
| 封面眉标 | `.kicker` | 12-13px | 500 | +0.20em | mono |

**硬规则**: 封面标题最小 44px · 封底标题最小 28px · 封面/封底必须照片背景

### Local Font Registry

| Font Name | CSS Name | Category |
|-----------|---------|----------|
| 汇文明朝体 | `'汇文明朝体'` | Serif/明朝 — elegant, scholarly |
| 宋徽宗瘦金体 | `'宋徽宗瘦金体'` | Calligraphy — extreme thin strokes |
| 方正小标宋 | `'方正小标宋简体'` | Song — official, authoritative |
| 楷体 | `'楷体-GB2312'` | Kai — handwritten, warm |
| 仿宋 | `'仿宋－GB2312'` | Fang — classical, formal |
| 不坑盒子 | `'不坑盒子'` | Creative — playful |
| Noto Serif SC | `'Noto Serif SC'` | Serif — clean, universal |
| Noto Sans SC | `'Noto Sans SC'` | Sans — clean, universal |
| Source Han Serif SC Heavy | `'Source Han Serif SC Heavy'` | Serif — elegant, powerful |
| TsangerJinKai02 | `'TsangerJinKai02'` | Kai/Serif — restrained, Kami default |
| Inter | `'Inter'` | Sans — Swiss default, modern |
| Playfair Display | `'Playfair Display'` | Serif-en — italic subtitles, pull quotes |
| IBM Plex Mono | `'IBM Plex Mono'` | Mono — labels, metadata |
| JetBrains Mono | `'JetBrains Mono'` | Mono — labels, metadata |

---

## Chinese Title Length Bands (标题长度→字号硬映射)

中文字符视觉密度远高于拉丁字母。先选长度区间，再定字号。**先缩短文案，绝不缩小到低于正文字号。**

### 640px 画布

| 标题形态 | Editorial `.h-display` | Swiss `.h-hero` |
|---------|----------------------|-----------------|
| 1 行，≤6 字 | 44px（默认） | 56px（默认） |
| 1 行，7-10 字 | 36px | 44px |
| 2 行，每行 ≤8 字 | 32px | 36px |
| 2 行，任一行 9-12 字 | 28px | 32px |
| 3 行（罕见） | 24px | 28px |

### 900×383 封面画布

| 标题形态 | Editorial 封面标题 | Swiss 封面标题 |
|---------|------------------|---------------|
| 1 行，≤6 字 | 52px | 56px |
| 1 行，7-10 字 | 44px | 48px |
| 2 行，每行 ≤8 字 | 40px | 44px |
| 2 行，任一行 9-12 字 | 36px | 40px |
| 3 行 | 32px | 36px |

### 硬规则

```
🚫 如果标题仍然放不下，缩短文案，不要缩小字号
🚫 正文最小可读字号：640px 画布 14px，900px 画布 15px
🚫 禁止为迁就长标题而缩小正文字号
```

---

## Swiss Card Class System (Swiss 卡片类系统)

Swiss 模式提供 4 种互斥卡片类。**同一节点上禁止组合使用。**

| Class | 填充 | 文字色 | 用途 |
|-------|------|--------|------|
| `.card-ink` | 实色 `var(--ink)` | `var(--paper)` | 每组一张声明卡 |
| `.card-accent` | `var(--accent)` | `var(--accent-on)` | 每张海报最多一张强调卡 |
| `.card-fill` | `var(--grey-1)` | `var(--ink)` | 矩阵/速查/要点网格的主力卡 |
| `.card-outlined` | 透明 + 1px `var(--grey-2)` 边框 | `var(--ink)` | 轻量级，无视觉重量 |

### 卡片规则

```
✅ 多卡网格中每个格子必须使用相同的卡片类
✅ 例外：允许一张 .card-accent 高亮卡突出一个项目
🚫 同一网格中混用 .card-fill 和 .card-outlined = 糟糕的模板
🚫 Editorial 模板不提供卡片类。Editorial 通过字体、标线、
   账本行和分栏结构表达层级——不是卡片背景
```

---

## Standard Image Ratio Classes (标准图片比例类)

| Class | 比例 | 用途 |
|-------|------|------|
| `.r-3x4` | 3:4 | 竖版封面、田野笔记照片 |
| `.r-1x1` | 1:1 | 方形人像、产品物件 |
| `.r-4x3` | 4:3 | 经典社论照片 |
| `.r-3x2` | 3:2 | 杂志内文配图 |
| `.r-16x9` | 16:9 | 风景照片、信息图 |
| `.r-21x9` | 21:9 | 微信 21:9 英雄图 |

### 硬规则

```
🚫 必须使用标准比例类，禁止写临时 aspect-ratio: 2592/1798
```

---

## Spacing Token System (间距令牌系统)

| Token | 值 | 用途 |
|-------|----|------|
| `--sp-3` | 8px | 紧凑芯片间距、行内元数据 |
| `--sp-4` | 12px | 卡片内间距、密集列表行 |
| `--sp-5` | 16px | 正文块底部间距 |
| `--sp-6` | 24px | 卡片内边距（紧凑）、网格间距（紧密） |
| `--sp-7` | 32px | 默认网格间距 |
| `--sp-8` | 40px | 卡片内边距（默认）、章节间距 |
| `--sp-9` | 48px | 章节间距（默认） |
| `--sp-10` | 64px | 内容块之间的主要分隔 |
| `--sp-12` | 96px | 海报外边距 |

### 硬规则

```
🚫 只使用此间距刻度中的值，禁止任意 px 间距
```

---

## Color Rules (色彩规则)

### Editorial 主题色映射

| 主题 | --paper | --ink | --accent | --accent-on | --grey-1 | --grey-2 |
|------|---------|-------|----------|-------------|----------|----------|
| 墨水经典 | #f5f4ed | #141413 | #1B365D | #ffffff | #e8e6dc | #d4d2c8 |
| 森林墨 | #f5f1e8 | #1a2e1f | #2D5A3A | #ffffff | #e5e0d4 | #c8c0b0 |
| 牛皮纸 | #eedfc7 | #2a1e13 | #8B6F47 | #ffffff | #e0d4bc | #c4b898 |
| 沙丘 | #f0e6d2 | #1f1a14 | #C17F59 | #ffffff | #e4dac6 | #c8bca4 |
| 莫兰迪 | #F5F0E8 | #3D3529 | #8B7E74 | #ffffff | #e8e2d8 | #ccc4b8 |

### Swiss 主题色映射

| 主题 | --paper | --ink | --accent | --accent-on | --grey-1 | --grey-2 |
|------|---------|-------|----------|-------------|----------|----------|
| 克莱因蓝 | #fafaf8 | #0a0a0a | #002FA7 | #ffffff | #f0f0ee | #d4d4d2 |
| 柠檬黄 | #fafaf8 | #0a0a0a | #FFD500 | #0a0a0a | #f0f0ee | #d4d4d2 |
| 柠檬绿 | #fafaf8 | #0a0a0a | #C5E803 | #0a0a0a | #f0f0ee | #d4d4d2 |
| 安全橙 | #fafaf8 | #0a0a0a | #FF6B35 | #ffffff | #f0f0ee | #d4d4d2 |

### Kami 扩展令牌系统 (Editorial 模式，kami 变体)

```css
:root {
  /* 6 核心变量由墨水经典主题提供 */
  --kami-brand: var(--accent); --kami-brand-light: #2D5A8A;
  --kami-parchment: var(--paper); --kami-ivory: #faf9f5;
  --kami-warm-sand: var(--grey-1); --kami-dark-surface: #30302e; --kami-deep-dark: var(--ink);
  --kami-near-black: var(--ink); --kami-dark-warm: #3d3d3a;
  --kami-olive: #504e49; --kami-stone: #6b6a64;
  --kami-border: var(--grey-1); --kami-border-soft: #e5e3d8;
  --kami-brand-tint: #EEF2F7; --kami-tag-bg: #E4ECF5;
  --kami-breaking-bg: #f0e0d8; --kami-breaking-fg: #8b4513;
}
```

### Color Application Rules

- **60-30-10**: 60% background (`var(--paper)`), 30% card/section (`var(--grey-1)`), 10% accent highlights (`var(--accent)`)
- Never > 4 accent colors in one design
- Dark text on light bg: never pure #000. Use `var(--ink)`. Light text on dark bg: never pure #FFF
- Accents must pass WCAG AA contrast

### Image-Text Conflict Bans (5 rules)

1. **Quiet zone test**: Photo must have low-detail area for text. No quiet zone → use framed-photo layout
2. **Subject mapping**: Identify photo focal point, place text in safe zones only
3. **object-position discipline**: Set inline on every `<img>` (face: `center 30%`, mid-body: `center 62%`, sky: `center 70%`)
4. **Thumbnail test**: Downscale to 360px wide — if title illegible, move/swap/tint
5. **No full-canvas falloffs**: If tint needed, apply only around text area, matching image color temperature

---

## Brand DNA Registry

| Brand | Detection Signals | Palette | Font Override | Layout Traits |
|-------|------------------|---------|---------------|---------------|
| **The Economist** | economist.com, "经济学人" | eco-red #E3120B | 方正小标宋 + 汇文明朝体 | Thick rules, no radius, mobile-first 640px |
| **WeChat / 微信** | mp.weixin.qq.com, "公众号" | WeChat green #07C160 | Noto Sans SC | Rounded cards, loose spacing, 578px |
| **Apple** | apple.com, "苹果" | Pure white + black | SF Pro / PingFang SC | Large whitespace, centered, hero image |
| **36Kr** | 36kr.com, "36氪" | 36Kr blue + dark | Source Han Sans | Dense, compact, tech-news |
| **People's Daily** | people.com.cn, "人民日报" | Red #DE2910 + gold #FFDE00 | 方正小标宋 + 仿宋 | Formal, symmetrical |
| **Xiaohongshu** | xiaohongshu.com, "小红书" | XHS red #FF2442 | Noto Sans SC | Card waterfall, photo-heavy |
| **Zhihu** | zhihu.com, "知乎" | Zhihu blue #0066FF | Noto Sans SC | Q&A layout, long-form |
| **GitHub** | github.com, "GitHub" | Dark bg + green accent | Monospace-heavy | Code blocks, repo stats |
| **Notion** | notion.so, "Notion" | Off-white + minimal | System UI | Block-based, toggle lists |
| **Kami / 纸墨** | tw93/kami, "Kami", "纸墨风" | kami-parchment + ink-blue #1B365D | TsangerJinKai02 | Kami Ten Invariants apply |
| **ByteDance / 字节** | bytedance.com, "字节跳动", "抖音" | 字节蓝 #325AB4 | Noto Sans SC | 紧凑卡片、数据密集 |
| **少数派 / sspai** | sspai.com, "少数派" | sspai-red #D93A31 | Noto Sans SC | 长文排版、留白舒适 |
| **极客时间** | time.geekbang.org, "极客时间" | 极客蓝 #3564D9 | Noto Sans SC | 知识卡片、步骤清晰 |

---

## Brand Profile System

Four-layer priority resolution for visual identity:

```
┌──────────────────────────────────────────────┐
│  Layer 1: Explicit Prompt                    │  ← --palette / --style / --layout
│  (Highest priority, always wins)             │
├──────────────────────────────────────────────┤
│  Layer 2: Brand DNA Auto-Detection           │  ← URL/keyword scan
│  (Auto-applied when content source detected) │
├──────────────────────────────────────────────┤
│  Layer 3: User Brand Profile                 │  ← ~/.config/react-design-draft/brand.md
│  (Persistent user preferences)               │
├──────────────────────────────────────────────┤
│  Layer 4: Dual-Style Auto-Selection          │  ← Editorial vs Swiss matching
│  (Lowest priority, default fallback)         │
└──────────────────────────────────────────────┘
```

**User Brand Profile** (`~/.config/react-design-draft/brand.md`): Define default colors, typography, layout preferences, brand rules. Partial override — only defined dimensions apply.

**Application rules**: Never silently override user intent · Always inform user of applied layers · Partial application is fine · User can always override with explicit flags · When Layer 2 and Layer 3 conflict, ask user

---

## Layout Types (Multi-Illustration)

> ⚠️ 本节列出布局类型名称供参考，具体的布局配方（recipe）已迁移至 `assets.md` 中的 Recipe System。

| Layout | Content Type | When to Use |
|--------|-------------|-------------|
| **hero-center** | 封面/封底/宣言 | Article cover, manifesto, section divider |
| **single-focus** | 金句/判断 | Key quote, single assertion, judgment |
| **grid-cards** | 规则/案例 | 3-12 parallel items, equal weight |
| **vertical-list** | 清单 | Checklist, ordered items, red-lines |
| **dense-grid** | 速查表 | Compact reference, number+name+example |
| **flow-chart** | 逻辑链/流程 | Causal chain, argument structure, process |
| **timeline** | 版本演进 | Chronological events, version history |
| **split-comparison** | 读者匹配/认知纠偏 | 2-3 way comparison, pros/cons |
| **binary-comparison** | 对比 | Strict A vs B with shared criteria |
| **center-stack** | 封底/关注引导 | Article ending, CTA, brand close |

---

## Keyword Shortcuts

User phrases auto-map to Layout × Mode combinations:

| User Says | Layout | Mode | Theme |
|-----------|--------|------|-------|
| "高密度信息大图" / "信息密集" | dense-grid | Swiss | 克莱因蓝 or 柠檬黄 |
| "对比分析" / "vs" | binary-comparison | Swiss | 安全橙 |
| "流程图" / "步骤" | flow-chart | Swiss | 克莱因蓝 |
| "时间线" / "演进" | timeline | Editorial | 沙丘 |
| "知识卡片" / "干货" | grid-cards | Editorial | 墨水经典 |
| "杂志风" / "排版" | hero-center | Editorial | 莫兰迪 or 墨水经典 |
| "纸墨风" / "Kami" / "雅致" | grid-cards | Editorial | 墨水经典 |
| "金句" / "引述" | single-focus | Editorial | 自动匹配 |
| "速查表" / "cheatsheet" | dense-grid | Swiss | 克莱因蓝 |
| "清单" / "红线" | vertical-list | Editorial | 墨水经典 |
| "森林" / "自然" | hero-center | Editorial | 森林墨 |
| "手工" / "牛皮纸" | grid-cards | Editorial | 牛皮纸 |
