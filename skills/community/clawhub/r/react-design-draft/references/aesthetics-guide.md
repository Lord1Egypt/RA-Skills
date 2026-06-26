# Aesthetics Guide v3

23 visual styles + 11 palettes + anti-patterns. Inspired by Kami's restraint system, taste-skill's anti-slop philosophy, and baoyu-skills' multi-dimension approach.

## Phase 0: The Three Constraints (审美哲学层)

**All styles must obey these constraints. They are non-negotiable.**

Inspired by Kami's "ten invariants" and taste-skill's "anti-slop" philosophy. Style can vary, but constraints are constant.

### Constraint 1: 克制 (Restraint)

- Brand/accent color covers **≤ 5% of document surface area**
- Brand color is for: title left-bar, tags, CTA buttons, accent numbers only
- More than 5% brand color = ornament, not design
- **Single accent principle**: one chromatic color per design. No second chromatic color (exception: breaking-change badges must be registered as `--breaking-*` tokens)

### Constraint 2: 呼吸 (Breathing)

- Card spacing ≥ 2× content spacing (gap between cards must be visually larger than gap within cards)
- Section title margin-bottom ≥ 2× margin-above (anchor the title to its content)
- Whisper shadow only: `0 4pt 24pt rgba(0,0,0,0.05)`, never hard drop shadows
- Ring shadow for emphasis: `0 0 0 1pt var(--brand)`, not box-shadow with offset > 4px
- Border width: 0.5pt (not 1px), border-radius: 8pt minimum for cards

### Constraint 3: 温度 (Warmth)

- **All grays must have warm undertone** (R ≈ G > B in RGB). No cool blue-grays.
- Forbidden: `#94A3B8`, `#CBD5E1`, `#E2E8F0`, `#F1F5F9`, `#F8FAFC` (these are cool blue-grays)
- Required warm gray scale:
  ```css
  --near-black: #141413;   /* warm olive undertone, not pure black */
  --dark-warm:  #3d3d3a;   /* secondary text */
  --olive:      #504e49;   /* subtext, descriptions */
  --stone:      #6b6a64;   /* tertiary, dates, metadata */
  --border:     #e8e6dc;   /* warm border */
  --parchment:  #f5f4ed;   /* warm cream background, never pure white */
  --ivory:      #faf9f5;   /* card background */
  ```
- **Never** use `#FFFFFF` as page background. Use `--parchment` or `--ivory`.
- **Never** use `#000000` as text color. Use `--near-black`.

### Serif Weight Lock

- Serif headings: weight 500 only. **Forbidden**: weight 600/700/900 on serif fonts
- Serif body: weight 400 only
- Rationale: synthetic bold on serif destroys the font's natural elegance

### The Larger, The Lighter (越大越轻)

**Core principle**: Large text should be lighter; small text should be heavier. This is the single most impactful typography rule for achieving "premium" feel.

| Role | Size (640px canvas) | Weight | Tracking | Rationale |
|------|---------------------|--------|----------|-----------|
| Display/Hero | 56-72px | 200-400 | +0.04em | Light weight at large size = elegance, not shouting |
| Section title | 36-48px | 400-500 | +0.03em | Medium weight anchors the hierarchy |
| Body | 14-18px | 400-500 | normal | Standard reading weight |
| Captions/meta | 10-12px | 500-650 | +0.1-0.22em | Small text needs heavier weight + wider tracking for readability |

**Hard rules**:
- A 56px+ title at weight 600+ instantly downgrades design from "premium" to "generic landing page"
- Chinese display text: weight 500 max (serif) or 300-400 (sans)
- Numbers in data cards: weight 200-400 at large size, 500-600 at small size
- **Exception**: brand name / logo text can use 700+ regardless of size

**Why it works**: The human eye perceives light-weight large text as confident and refined, while heavy-weight large text reads as aggressive and cheap. Think Monocle vs. a spam email.

**Why it works** (design decision rationale):
- Light-weight large text reads as confident and refined — like Monocle, The New Yorker, or A Book Apart
- Heavy-weight large text reads as aggressive and cheap — like spam email or discount flyers
- This principle has been validated by 100 years of magazine and poster design
- The specific weight ranges (200-400 for display, 500-650 for meta) are calibrated for screen rendering at 640px canvas width

### CJK Letter-Spacing

- Chinese body text with serif: `letter-spacing: 0.3pt` (compensate for density)
- Chinese display text (24px+): `letter-spacing: 0.2-1pt` (optical breathing)
- English body: `letter-spacing: 0`
- Small labels (< 10pt): `+0.2 to +0.5pt`

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

## Phase 0.5: Dual Style System (Editorial vs Swiss)

Inspired by guizang-ppt-skill's two-stance design philosophy. The two systems are **visual stances, not content categories** — any topic can be rendered in either mode. Pick by editorial intent ("feature story" vs "release note"), not by topic lookup.

### Mode A: Editorial Magazine (杂志社论风)

Good fits: humanistic, cultural, narrative, reflective content — but also workplace essays, AI think-pieces, product retrospectives, anything wanting a slow magazine-feature pace.

Visual anchors:
- **Serif/Songti display title** + quiet sans body text
- **Warm paper background** (#f5f4ed / #f1efea), deep ink text, restrained color
- **Atmosphere layer**: subtle paper grain, ink wash, or gradient atmosphere (not flat beige)
- **Magazine structure**: columns, pull-quotes, marginalia, ledger rows, large photo wells
- **Large but purposeful whitespace**
- **Fine rules** (0.5pt), editorial contrast, documentary photography

Palettes: warm, elegant, earth, kami-parchment, morandi-journal, or any Brand DNA palette
Font presets: 古典书卷, 瘦金风骨, 纸墨书卷(Kami), 官方权威

### Mode B: Swiss International (瑞士国际主义风)

Good fits: tech products, data reports, engineering, design, annual summaries — anything wanting an engineered, quantified, decisive feel.

Visual anchors:
- **Full sans-serif** (Inter / Noto Sans SC), no serif anywhere
- **Light paper background** (#fafaf8) + near-black text (#0a0a0a)
- **Grid/dot matrix background** (CSS pattern, not WebGL)
- **One high-saturation accent only**: IKB Blue / Lemon Yellow / Lemon Green / Safety Orange
- **Strict left-aligned grid**, hairline rules, no center alignment (except special covers)
- **Card-fill matrices**, KPI towers, h-bar charts, numbered statements

Palettes: Swiss-specific (see below)
Font presets: 现代简约 only (Inter + Noto Sans SC)

### Swiss Accent Palettes (4 options, pick one)

| Accent | Hex | accent-on | Vibe | Best For |
|--------|-----|-----------|------|----------|
| **IKB Blue** (克莱因蓝) | #002FA7 | #ffffff | Academic, rational, classic Swiss | AI/tech/design, default choice |
| **Lemon Yellow** (柠檬黄) | #FFD500 | #0a0a0a | Active, vibrant, IKEA-like | Youth, retail, consumer |
| **Lemon Green** (柠檬绿) | #C5E803 | #0a0a0a | Future, emerging, Off-White vibe | Eco, Gen-Z, new tech |
| **Safety Orange** (安全橙) | #FF6B35 | #ffffff | Industrial, urgent, Saul Bass | Industrial, automotive, warnings |

**Hard rules for Swiss mode**:
- One accent only per design set. No mixing blue + yellow + green + orange
- No gradients. Pure color blocks, hairline rules, grid modules only
- No serif fonts loaded. No `font-family: serif` or `Noto Serif SC`
- No rounded corners on accent blocks. Sharp edges only
- Headings sit on top-left content axis, not center

### Swiss Gray Scale (cross-accent unified)

```css
--swiss-paper: #fafaf8;    /* warm white, not pure white */
--swiss-grey-1: #f0f0ee;   /* light grey block bg */
--swiss-grey-2: #d4d4d2;   /* mid grey, dividers/borders */
--swiss-grey-3: #737373;   /* dark grey, secondary text */
--swiss-ink: #0a0a0a;      /* near-black, not pure black */
```

This gray scale is color-calibrated "premium gray" that doesn't compete with any accent. **Do not** replace with pure white (#fff) or pure black (#000).

### Style Identity Test

Before delivering, verify each illustration passes its identity test:

**Swiss identity test** (ALL four must hold):
1. Every large display title (≥48px) has font-weight ≤ 400
2. No serif family loaded in the document. No element uses `font-family: serif`
3. Section separators are hairline rules (1-2px) or grid gutters, not card borders + drop shadows
4. Exactly one accent palette in use. No mixed accents across illustrations

**Editorial identity test** (ALL three must hold):
1. Background has at least one atmosphere layer beyond flat fill (grain, gradient, wash)
2. Display title uses serif-zh family (Noto Serif SC / 汇文明朝体 / TsangerJinKai02)
3. Contains at least one: large photo well, serif pull-quote, marginalia column, or ledger with magazine row hierarchy

If a design fails its identity test, it is "generic" — fix it or switch mode honestly.

## Phase 1: Choose Style (23 options)

### Professional & Clean

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 1 | **minimal** | Extreme whitespace, 2 colors, geometric sans | 1 font, 16px+ body, 48px+ headings, no borders |
| 2 | **corporate-memphis** | Flat geometric shapes, limited palette, clean | Rounded rects, solid fills, 2-3 colors, no gradients |
| 3 | **technical-schematic** | Blueprint lines, monospace labels, precision | Thin borders, mono font for labels, grid bg, blue/dark |
| 4 | **ui-wireframe** | Gray-scale, component outlines, functional | Gray palette, dashed borders, placeholder blocks |

### Editorial & Magazine

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 5 | **bold-editorial** | Huge type, tight leading, high contrast | 72px+ hero text, black/white + 1 accent, minimal decoration |
| 6 | **editorial-infographic** | Data-rich, structured, magazine layout | Multi-column, pull-quotes, stat callouts, ruled lines |
| 7 | **aged-academia** | Serif fonts, aged paper, scholarly | Serif display, warm cream bg, subtle texture, footnotes |

### Hand-crafted & Artistic

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 8 | **craft-handmade** | Textured paper, stamp-like elements, warm | Warm bg, slight rotation on cards, hand-drawn borders via SVG |
| 9 | **hand-drawn-edu** | Sketch lines, notebook feel, educational | Dashed borders, pencil-like SVG icons, lined-paper bg |
| 10 | **storybook-watercolor** | Soft washes, dreamy, narrative | Pastel gradients, soft shadows, rounded organic shapes |
| 11 | **chalkboard** | Dark bg, chalk-like text, classroom | Dark green/gray bg, white text with slight opacity variation |
| 12 | **sketch-notes** | Doodle style, arrows, boxes, informal | SVG arrows, hand-drawn dividers, rotated sticky notes |

### Digital & Tech

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 13 | **cyberpunk-neon** | Dark bg, neon glows, futuristic | Dark bg, text-shadow glow effects, neon accent borders |
| 14 | **pixel-art** | Blocky, 8-bit aesthetic, retro gaming | Pixel font, block borders, no border-radius, grid-based |
| 15 | **retro-pop-grid** | Bold color blocks, grid layout, 60s-70s pop | Thick borders, primary colors, geometric patterns |

### Playful & Character

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 16 | **claymation** | 3D clay look, rounded, soft shadows | Large border-radius, soft multi-layer shadows, pastel |
| 17 | **kawaii** | Cute, pastel, rounded, emoji-like | Extra rounded (16px+), pastel palette, cute SVG icons |
| 18 | **origami** | Paper fold effects, geometric, precise | Diagonal CSS gradients for fold effect, sharp edges, white |
| 19 | **lego-brick** | Blocky, interlocking, primary colors | No border-radius, thick borders, bright primary colors |
| 20 | **pop-laboratory** | Scientific but fun, beakers, bubbles | Circular elements, gradient bubbles, lab-equipment SVGs |

### Elegant & Refined

| # | Style | Key Traits | CSS Implementation |
|---|-------|-----------|-------------------|
| 21 | **morandi-journal** | Muted sophisticated tones, artistic | Morandi color palette, serif + sans mix, generous spacing |
| 22 | **ikea-manual** | Clean pictorial instructions, minimal text | Icon-heavy, step numbers, thin lines, no decoration |
| 23 | **kami-editorial** | Warm parchment, ink-blue accent, serif hierarchy, restrained | Parchment bg #f5f4ed, ink-blue #1B365D only accent, serif 400/500 only, no bold, whisper shadows, en-dash bullets |

## Phase 2: Typography Rules

### Font Strategy: Local-First, Web-Fallback

Design drafts are primarily for **local preview + screenshot export**, not web deployment. Therefore:

1. **Prioritize local fonts** — better CJK rendering, no subset missing chars, instant load
2. **Web fonts as fallback** — only when local font unavailable or deployment needed
3. **CSS `font-family` stack** — local first, web fallback, generic last

```css
/* Example: local 汇文明朝体 → web Noto Serif SC → generic serif */
--font-display: '汇文明朝体', 'Noto Serif SC', serif;
```

### Font Pairing System (6 Presets)

Each preset = 1 display + 1 body + 1 mono. Choose based on style.

| Preset | Display (标题) | Body (正文) | Mono (代码) | Vibe | Best With |
|--------|---------------|------------|------------|------|-----------|
| **古典书卷** | 汇文明朝体 | 楷体-GB2312 | Ubuntu Mono | 文化感、书卷气 | aged-academia, editorial-infographic, craft-handmade |
| **瘦金风骨** | 宋徽宗瘦金体 | 汇文明朝体 | Ubuntu Mono | 极致个性、锋利 | bold-editorial, morandi-journal, brutalist-raw |
| **官方权威** | 方正小标宋 | Noto Sans SC | Ubuntu Mono | 正式、商务 | corporate-memphis, minimal, technical-schematic |
| **现代简约** | Source Han Serif SC Heavy | Noto Sans SC | Ubuntu Mono | 干净、现代 | minimal, editorial-infographic, ui-wireframe |
| **手写教育** | 楷体-GB2312 | Noto Sans SC | Ubuntu Mono | 温和、亲切 | hand-drawn-edu, chalkboard, sketch-notes |
| **创意趣味** | 不坑盒子 | Noto Sans SC | Ubuntu Mono | 个性、张扬 | kawaii, pop-laboratory, retro-pop-grid |
| **纸墨书卷(Kami)** | 仓耳今楷02(TsangerJinKai02) | Noto Sans SC | JetBrains Mono | 克制、雅致、纸感 | kami-editorial, aged-academia, editorial-infographic, morandi-journal |

### Style → Font Preset Mapping

| Style | Font Preset | CSS Variables |
|-------|-----------|---------------|
| minimal | 现代简约 | `--font-display: 'Source Han Serif SC Heavy', 'Noto Serif SC', serif; --font-body: 'Noto Sans SC', sans-serif` |
| bold-editorial | 瘦金风骨 | `--font-display: '宋徽宗瘦金体', 'Noto Serif SC', serif; --font-body: '汇文明朝体', 'Noto Serif SC', serif` |
| editorial-infographic | 古典书卷 | `--font-display: '汇文明朝体', 'Noto Serif SC', serif; --font-body: 'Noto Sans SC', sans-serif` |
| technical-schematic | 现代简约 | `--font-display: 'Source Han Serif SC Heavy', serif; --font-body: 'Noto Sans SC', sans-serif` |
| hand-drawn-edu | 手写教育 | `--font-display: '楷体-GB2312', 'KaiTi', serif; --font-body: 'Noto Sans SC', sans-serif` |
| craft-handmade | 古典书卷 | `--font-display: '汇文明朝体', 'Noto Serif SC', serif; --font-body: '楷体-GB2312', serif` |
| aged-academia | 古典书卷 | `--font-display: '汇文明朝体', 'Noto Serif SC', serif; --font-body: '楷体-GB2312', serif` |
| morandi-journal | 瘦金风骨 | `--font-display: '宋徽宗瘦金体', 'Noto Serif SC', serif; --font-body: '汇文明朝体', serif` |
| cyberpunk-neon | 现代简约 | `--font-display: 'Source Han Serif SC Heavy', serif; --font-body: 'Noto Sans SC', sans-serif` |
| chalkboard | 手写教育 | `--font-display: '楷体-GB2312', serif; --font-body: 'Noto Sans SC', sans-serif` |
| corporate-memphis | 官方权威 | `--font-display: '方正小标宋', 'SimSun', serif; --font-body: 'Noto Sans SC', sans-serif` |
| kawaii | 创意趣味 | `--font-display: '不坑盒子', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| brutalist-raw | 瘦金风骨 | `--font-display: '宋徽宗瘦金体', serif; --font-body: 'Noto Sans SC', sans-serif` |
| storybook-watercolor | 手写教育 | `--font-display: '楷体-GB2312', serif; --font-body: 'Noto Sans SC', sans-serif` |
| retro-pop-grid | 创意趣味 | `--font-display: '不坑盒子', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| kami-editorial | 纸墨书卷(Kami) | `--font-display: 'TsangerJinKai02', 'Source Han Serif SC', serif; --font-body: 'Noto Sans SC', sans-serif` |
| ui-wireframe | 现代简约 | `--font-display: 'Source Han Serif SC Heavy', serif; --font-body: 'Noto Sans SC', sans-serif` |
| sketch-notes | 手写教育 | `--font-display: '楷体-GB2312', serif; --font-body: 'Noto Sans SC', sans-serif` |
| pixel-art | 现代简约 | `--font-display: 'Noto Sans SC', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| claymation | 创意趣味 | `--font-display: '不坑盒子', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| origami | 现代简约 | `--font-display: 'Source Han Serif SC Heavy', serif; --font-body: 'Noto Sans SC', sans-serif` |
| lego-brick | 现代简约 | `--font-display: 'Noto Sans SC', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| pop-laboratory | 创意趣味 | `--font-display: '不坑盒子', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |
| ikea-manual | 现代简约 | `--font-display: 'Noto Sans SC', sans-serif; --font-body: 'Noto Sans SC', sans-serif` |

### Local Font Registry

These fonts are installed on the user's machine and available for design drafts:

| Font Name | CSS Name | File | Category |
|-----------|---------|------|----------|
| 汇文明朝体 | `'汇文明朝体'` | `汇文明朝体GBKv1.001.ttf` | Serif/明朝 — elegant, scholarly |
| 宋徽宗瘦金体 | `'宋徽宗瘦金体'` | `宋徽宗瘦金体.ttf` | Calligraphy — extreme thin strokes, imperial |
| 方正小标宋 | `'方正小标宋简体'` | `方正小标宋简体.TTF` | Song — official, authoritative |
| 楷体 | `'楷体-GB2312'` | `楷体-GB2312.ttf` | Kai — handwritten, warm |
| 仿宋 | `'仿宋－GB2312'` | `仿宋－GB2312.ttf` | Fang — classical, formal |
| 黑体 | `'SimHei'` | `simhei.ttf` | Hei — bold, modern |
| 不坑盒子 | `'不坑盒子'` | `不坑盒子.ttf` | Creative — playful, unique |
| Noto Sans SC | `'Noto Sans SC'` | System | Sans — clean, universal |
| Source Han Serif SC Heavy | `'Source Han Serif SC Heavy'` | System | Serif — elegant, powerful |
| Ubuntu Mono | `'Ubuntu Mono'` | `UbuntuMono[wght].ttf` | Mono — code, data |
| TsangerJinKai02 | `'TsangerJinKai02'` | User installed | Kai/Serif — elegant, restrained, Kami default Chinese font |

### Multi-Language Font Stacks

When content contains Japanese or Korean text, use these font stacks:

```css
/* Japanese */
--font-display-ja: 'YuMincho', 'Yu Mincho', 'Hiragino Mincho ProN', 'Noto Serif CJK JP', 'Source Han Serif JP', 'TsangerJinKai02', Georgia, serif;
--font-body-ja: 'Noto Sans CJK JP', 'Source Han Sans JP', 'Hiragino Sans', sans-serif;

/* Korean */
--font-display-ko: 'Source Han Serif K', 'Source Han Serif KR', 'Noto Serif KR', 'Apple SD Gothic Neo', AppleMyungjo, Charter, Georgia, serif;
--font-body-ko: 'Noto Sans KR', 'Source Han Sans KR', 'Apple SD Gothic Neo', sans-serif;
```

### Slide Scaling Formula

When generating slides or presentation-mode design drafts:

| Property | Print/Screen | Slide | Reason |
|----------|-------------|-------|--------|
| Title size | 30-34pt | 48-64pt | Projection needs larger text |
| Inner padding | N/A | 72-80px top, 80px sides | <72px top feels cramped |
| Eyebrow tracking | 0.5-1pt | 3px max | Print tracking spreads on screen |
| Display tracking | 0 to -0.2pt | -0.5pt | Tighten large titles to prevent letter gaps |
| Header gap | 8-14pt | 36px+ | <36px rule looks like underline |
| Title line-height | 1.1-1.3 | 1.3 minimum | CJK chars collide at slide scale <1.3 |
| Macro spacing | base | ×1.6 | Section gaps, margins |
| Micro spacing | base | ×0.5 | Label-to-value, badge padding |

### Font Size Scale

Modular scale (ratio 1.25): 12 → 14 → 16 → 20 → 24 → 32 → 48

**CJK-specific adjustments**:
- CJK titles: use 1.1x the English size (CJK chars are visually smaller at same px)
- CJK body: minimum 14px (12px CJK is unreadable)
- CJK line-height: 1.7-1.8 (CJK needs more leading than Latin's 1.5)

## Phase 3: Color Rules

### 11 Palette Schemes + Brand DNA Palettes

Each palette defines: bg-primary, bg-secondary, bg-card, text-primary, text-secondary, text-muted, accent-1 through accent-4, border.

| Palette | bg-primary | text-primary | Accents |
|---------|-----------|-------------|---------|
| **warm** | #FAF8F5 | #2D2418 | #E8913A, #D4583A, #5B8C5A, #3D7EA6 |
| **elegant** | #F8F7F4 | #1A1A2E | #2D4A7A, #C9A84C, #6B5B8D, #3A6B5E |
| **cool** | #F5F7FA | #1E293B | #3B82F6, #06B6D4, #6366F1, #8B5CF6 |
| **dark** | #0F172A | #E2E8F0 | #22D3EE, #A78BFA, #F472B6, #34D399 |
| **earth** | #F5F0E8 | #3D3529 | #8B6F47, #5B7B5E, #C17F59, #6B8FA3 |
| **vivid** | #FFFFFF | #111827 | #EF4444, #F59E0B, #10B981, #3B82F6 |
| **pastel** | #FDF4FF | #374151 | #C084FC, #F9A8D4, #93C5FD, #86EFAC |
| **mono** | #FAFAFA | #18181B | #71717A, #A1A1AA |
| **retro** | #F5E6D3 | #4A3728 | #C17F3E, #8B4513, #6B8E6B, #B85C38 |
| **duotone** | #0A0A0A | #FAFAFA | #FF6B35 |
| **macaron** | #FFF5F5 | #4A4A4A | #FFB5C2, #B5DEFF, #C5E8B0, #E8C5FF |
| **kami-parchment** | #F5F4ED | #141413 | #1B365D (ink-blue, sole accent) |

#### Kami Full Token System (when style = kami-editorial)

When using kami-editorial, the full token system below replaces the simplified 3-variable kami-parchment:

```css
:root {
  /* Brand */
  --kami-brand: #1B365D;
  --kami-brand-light: #2D5A8A;

  /* Surfaces */
  --kami-parchment: #f5f4ed;
  --kami-ivory: #faf9f5;
  --kami-warm-sand: #e8e6dc;
  --kami-dark-surface: #30302e;
  --kami-deep-dark: #141413;

  /* Text */
  --kami-near-black: #141413;
  --kami-dark-warm: #3d3d3a;
  --kami-olive: #504e49;
  --kami-stone: #6b6a64;

  /* Borders */
  --kami-border: #e8e6dc;
  --kami-border-soft: #e5e3d8;

  /* Brand derivatives */
  --kami-brand-tint: #EEF2F7;
  --kami-tag-bg: #E4ECF5;

  /* Semantic warm (only approved exception) */
  --kami-breaking-bg: #f0e0d8;
  --kami-breaking-fg: #8b4513;
}
```

**Application rules**: When kami-editorial is selected, ALL kami tokens above must be used. Do not mix with generic palette variables.

#### Brand DNA Palettes (auto-applied when content source detected)

| Palette | bg-primary | text-primary | Accents | Font Override | Traits |
|---------|-----------|-------------|---------|---------------|--------|
| **economist-red** | #FDFCFA | #1D1D1B | #E3120B (sole accent), grays: #333/#666/#999 | 方正小标宋(display) + 汇文明朝体(serif-body) | Thick rules, no radius, mobile-first |
| **wechat-green** | #FFFFFF | #333333 | #07C160 (sole accent) | Noto Sans SC | Rounded 8px, loose spacing, 578px |
| **peoples-red-gold** | #FFF9F0 | #1D1D1B | #DE2910, #FFDE00 | 方正小标宋 + 仿宋 | Formal, symmetrical |
| **xhs-red** | #FFF5F5 | #333333 | #FF2442, #FFB5C2 | Noto Sans SC | Card waterfall, photo-heavy |
| **zhihu-blue** | #FFFFFF | #1A1A1A | #0066FF | Noto Sans SC | Clean, long-form |

### Color Application Rules

- **60-30-10 rule**: 60% background, 30% card/section, 10% accent highlights
- **Never > 4 accent colors** in one design
- **Dark text on light bg**: never pure #000
- **Light text on dark bg**: never pure #FFF
- **Accents must pass WCAG AA** contrast

### Aesthetic Guardrails (保护美学比给自由更重要)

Inspired by guizang's philosophy: "Color matching mistakes instantly destroy aesthetics — protecting beauty matters more than giving freedom."

**Palette Lock Rule**: When using Swiss mode, only the 4 Swiss Accent Palettes are allowed. When using Editorial mode, only the warm/elegant/earth/kami/morandi palettes are allowed. Do not accept arbitrary hex values from users — recommend from presets instead.

**Single Accent Principle (Swiss)**: One chromatic accent per design set. No mixing IKB Blue + Lemon Yellow in the same article's illustrations.

**No Cross-Mode Mixing**: Do not use Swiss gray scale in Editorial mode, or Editorial warm grays in Swiss mode. Each mode has its own calibrated color system.

**When user insists on custom color**: Allow it only if they provide a brand hex code with explicit brand context (e.g., "our brand color is #E3120B"). Register it as `--brand-accent` and apply single-accent rules.

**Why restriction works** (design decision rationale):
- Color matching mistakes instantly destroy aesthetics — a wrong accent color can make an entire design set look amateur
- 10 curated palettes have been validated across hundreds of real-world magazine and poster designs
- "Freedom to choose any color" = "freedom to make ugly things" — this is why professional design tools ship with preset palettes
- The Swiss single-accent rule comes from 70+ years of Swiss International Typographic Style practice — mixing multiple bright colors violates the style's DNA

## Phase 4: Layout & Composition

- ✅ Asymmetric over symmetric when content allows
- ✅ Overlapping elements for depth
- ✅ Diagonal flow for visual energy
- ✅ Generous negative space OR controlled density (never in-between)
- ❌ Never center everything
- ❌ Never identical spacing everywhere

## Phase 5: Motion & Interaction

- **Page load**: staggered reveal (50-100ms delay between items)
- **Hover**: subtle lift + shadow increase
- **Scroll**: IntersectionObserver for reveals
- **Duration**: 150ms / 250ms / 350ms
- ❌ Never `transition: all`
- ❌ Never animate `width`/`height`

## Phase 6: Anti-Patterns (Absolute Bans)

### Kami Ten Invariants (when style = kami-editorial)

When using kami-editorial style, these 10 rules are absolute — think before overriding:

1. Page background parchment `#f5f4ed`, **never pure white**
2. Single accent: ink-blue `#1B365D`, **no second chromatic color**
3. All grays warm-toned (yellow-brown undertone), **no cool blue-grays**
4. Chinese: serif headlines, sans body. Sans only for UI labels/meta
5. Serif weight locked at 400/500, **no synthetic bold (600/700)**
6. Line-heights: tight headlines 1.1-1.3, dense body 1.4-1.45, reading body 1.5-1.55
7. Chinese body letter-spacing: 0.3pt for comfortable reading
8. Tag backgrounds must be **solid hex**, never rgba
9. Depth via ring shadow or whisper shadow, **never hard drop shadows**
10. **No italic** in print/PDF templates

### General Anti-Patterns (all styles)

### Typography Bans
- Inter / Roboto / Arial as primary font
- system-ui as font choice
- All text same weight
- Center-aligned body text at width > 600px

### Color Bans
- Purple gradient on white background
- Blue-purple gradient hero
- Evenly distributed rainbow colors
- Pure white (#FFF) background
- Pure black (#000) text
- > 4 accent colors

### Layout Bans
- Nested rounded cards (card in card in card)
- Identical card grid with no variation
- Excessive box-shadow (> 2 layers)
- Border + background + shadow on same element
- Full-width everything
- Hero section with gradient + centered text

### Component Bans
- Icon + emoji + badge on same line
- Circular avatar in every card
- Progress bar for everything
- Tooltip on every element

### Image-Text Conflict Bans (图片-文字冲突防护)

When an illustration places text on top of a photo (full-bleed cover, large image well, hero background):

1. **Quiet zone test**: Photo must have a low-detail, low-contrast area where text will sit. If no quiet zone exists, use a framed-photo layout instead of full-bleed.

2. **Subject mapping**: Before placing title, identify where the photo's subject/focal point sits. Place text only in documented safe zones. Record subject position as a CSS comment: `/* subject: center-top, safe zone: bottom 40% */`.

3. **object-position discipline**: Set `object-position` inline on every `<img>` based on subject location. Default `center` is a fallback, not a recommendation.
   - Face/portrait: `center 30%`
   - Mid-body: `center 62%`
   - Sky-heavy landscape: `center 70%`
   - Foreground gear: `center 25%`

4. **Thumbnail test**: Downscale rendered image to 360px wide. If title is not legible, move title, swap photo, or add localized image-toned tint around title area only.

5. **No full-canvas falloffs**: Do not default to full-image dark overlays. If a tint is needed, apply it only around the text area, matching the image's own color temperature.

## Phase 7: Quality Checklist

- [ ] One clear style chosen and consistently executed
- [ ] Fonts: 1 display + 1 body + 1 mono (none are Inter/Roboto/Arial)
- [ ] Colors: off-white bg, near-black text, 2-4 meaningful accents
- [ ] No purple gradient on white
- [ ] No nested rounded cards
- [ ] Spacing follows 4px scale
- [ ] Typography hierarchy: ≥ 3 distinct levels
- [ ] Layout serves content
- [ ] Every visual element carries information
- [ ] Design would be memorable
