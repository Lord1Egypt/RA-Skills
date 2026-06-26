# Xiaohongshu Visual Design Guide

## Cover Style Categories

### 1. Magazine Style (杂志风) — Best for: 种草, 测评, 穿搭
- Clean editorial layout with clear hierarchy
- Large title text with serif or stylized font
- Structured grid, generous whitespace
- Muted or cohesive color palette
- Professional product photography feel
- **When to use**: Premium products, brand reviews, outfit lookbooks

### 2. Handwritten Feel (手写感) — Best for: 日常分享, 教程, 美食
- Hand-drawn elements, brush stroke accents
- Casual, approachable tone
- Warm color palette (cream, peach, soft green)
- Sticker/doodle decorations (moderate)
- **When to use**: Personal stories, cooking tutorials, lifestyle tips

### 3. Clean Minimal (干净利落) — Best for: 数码, 职场, 知识类
- Strong typographic hierarchy, no clutter
- 1-2 accent colors max
- Bold sans-serif titles
- Geometric layout with clear sections
- Flat illustration or icon-based
- **When to use**: Tech reviews, productivity tips, career advice

### 4. Impact Contrast (对比冲击) — Best for: before/after, 对比, 攻略
- Split layout (left/right or top/bottom)
- High contrast colors
- Large bold text with emphasis markers
- Visual comparison structure
- Arrow or "VS" elements
- **When to use**: Transformations, product comparisons, budget vs premium

### 5. Warm Lifestyle (温暖生活) — Best for: 家居, 母婴, 旅行
- Soft photography with natural light feel
- Warm earth tones (terracotta, sage, cream)
- Gentle gradient overlays
- Rounded shapes, organic layouts
- **When to use**: Home decor, parenting, travel diaries

## Color Palettes by Category

### 美妆护肤
- Primary: Soft pink `#F5C6C6`, Rose gold `#C9A7A7`
- Accent: Berry `#8B3A62`, Coral `#E88D72`
- Background: Cream `#FFF8F5`

### 美食烘焙
- Primary: Warm brown `#8B6F47`, Honey `#D4A54A`
- Accent: Forest `#5B7553`, Terracotta `#C17652`
- Background: Parchment `#FBF3EB`

### 家居生活
- Primary: Sage `#9CAF88`, Sand `#C9B99A`
- Accent: Terracotta `#C17652`, Olive `#6B7B3A`
- Background: Warm white `#FAF7F2`

### 数码科技
- Primary: Deep blue `#2B4C7E`, Graphite `#3D3D3D`
- Accent: Electric blue `#4A90D9`, Green `#4CAF50`
- Background: Cool gray `#F5F5F7`

### 穿搭时尚
- Primary: Black `#1A1A1A`, Off-white `#F5F0E8`
- Accent: Gold `#C9A44A`, Red `#C13B3B`
- Background: Light beige `#FAF5EE`

### 旅行出行
- Primary: Sky blue `#7EB8D4`, Sand `#D4C5A9`
- Accent: Sunset orange `#E88D52`, Forest `#4A7C59`
- Background: Cloud white `#F8FAFB`

## Typography Rules

### Title (标题)
- Size: 40-60px (relative to 1080px width)
- Weight: Bold or Extra-bold
- Max 2 lines (10-15 Chinese characters per line)
- Position: Top 1/3 or center, never bottom edge
- Contrast: Must be readable on any background (use text shadow or background blur)

### Subtitle (副标题)
- Size: 24-32px
- Weight: Regular or Medium
- 1 line, supporting information
- Slightly lower contrast than title

### Body Text on Cover
- Avoid more than 3 text elements total on a cover
- Keep text in the safe zone (avoid edges by 60px margin)
- Text-to-image ratio: aim for 30% text, 70% visual

### Font Recommendations
- Chinese serif: 思源宋体 (Noto Serif SC), 方正楷体
- Chinese sans: 思源黑体 (Noto Sans SC), PingFang SC, 阿里巴巴普惠体
- Chinese handwritten: 站酷快乐体, 庞门正道标题体
- Accent/English: Playfair Display, DM Serif, Poppins

## Layout Patterns

### Standard Cover (1080x1440, 3:4)
```
┌──────────────────────┐
│     Top margin 80px  │
│  ┌────────────────┐  │
│  │  TITLE AREA    │  │  ← Top 1/3: Title + subtitle
│  │  Subtitle      │  │
│  └────────────────┘  │
│                      │
│  ┌────────────────┐  │
│  │                │  │  ← Middle: Key visual / product
│  │  VISUAL AREA   │  │
│  │                │  │
│  └────────────────┘  │
│                      │
│  ┌────────────────┐  │
│  │  CTA / Tag     │  │  ← Bottom: Call to action or tag
│  └────────────────┘  │
│     Bottom margin    │
└──────────────────────┘
```

### Wide Format (1080x810, 4:3)
```
┌──────────────────────────────┐
│  TITLE          │  VISUAL    │  ← Left text + right visual
│  Subtitle       │  AREA      │    OR
│  Tag/CTA        │            │  ← Full bleed with text overlay
└──────────────────────────────┘
```

## Design Anti-Patterns

Avoid these common mistakes:

1. **Text wall** — Too much text on cover, nothing stands out
2. **Neon overload** — Excessive bright colors competing for attention
3. **Tiny text** — Text unreadable in feed thumbnail (preview is ~300px wide)
4. **No focal point** — Everything equally weighted, eye has nowhere to land
5. **Stock photo feel** — Generic imagery without personality
6. **Border abuse** — Thick colored borders around the entire image (feels spammy)
7. **Mismatched tone** — Serious topic with playful design, or vice versa
