# Content → Layout Mapping & Three-Dimension Combination System

Inspired by baoyu-skills' Type × Style × Palette approach, adapted for React design drafts.

## Three-Dimension System

Design drafts are determined by combining three independent dimensions:

```
Layout (信息结构) × Style (视觉风格) × Palette (配色方案)
```

Each dimension is chosen independently, then combined. This gives 21 × 22 × 11 = 5,086 possible combinations.

## Dimension 1: Layout (21 types)

### Basic Layouts (from v1)

| # | Layout | Content Type | When to Use |
|---|--------|-------------|-------------|
| 1 | **grid-cards** | Enumeration | 3-12 parallel items, equal weight |
| 2 | **split-comparison** | Comparison | 2-3 way comparison, pros/cons |
| 3 | **step-flow** | Process | 3-7 ordered steps with dependencies |
| 4 | **dashboard** | Data | Metrics, charts, KPIs |
| 5 | **tree-nested** | Hierarchy | Parent-child, org chart, component tree |
| 6 | **timeline** | Timeline | Chronological events, version history |

### Extended Layouts (v2, inspired by baoyu-infographic)

| # | Layout | Content Type | When to Use |
|---|--------|-------------|-------------|
| 7 | **bento-grid** | Mixed | Diverse content types in one view, each cell different size |
| 8 | **linear-progression** | Process | Linear journey with milestones, start→end narrative |
| 9 | **binary-comparison** | Comparison | Strict A vs B with shared criteria rows |
| 10 | **comparison-matrix** | Comparison | Multi-item × multi-criteria grid |
| 11 | **hierarchical-layers** | Hierarchy | Stacked layers (OSI model, tech stack) |
| 12 | **hub-spoke** | Enumeration | Central concept with radiating subtopics |
| 13 | **structural-breakdown** | Hierarchy | Exploded view, whole → parts decomposition |
| 14 | **iceberg** | Mixed | Visible vs hidden layers (surface/depth metaphor) |
| 15 | **bridge** | Process | Current state → bridge/actions → future state |
| 16 | **funnel** | Process | Narrowing stages (sales funnel, filtering pipeline) |
| 17 | **isometric-map** | Hierarchy | 3D-ish system architecture, data flow |
| 18 | **periodic-table** | Enumeration | Categorized items in grid with group labels |
| 19 | **comic-strip** | Process | Sequential narrative with panels |
| 20 | **story-mountain** | Process | Setup → rising action → climax → resolution |
| 21 | **circular-flow** | Process | Cyclical process, no start/end (waterfall, CI/CD) |
| 22 | **dense-modules** | Mixed | Maximum information density, modular blocks |
| 23 | **winding-roadmap** | Process | Long roadmap with turns, strategic plan |
| 24 | **venn-diagram** | Comparison | Overlapping sets, shared characteristics |
| 25 | **jigsaw** | Mixed | Interlocking pieces that form a whole |

### Layout Selection Logic

```
1. Identify content type from user input
2. Count key units → determine density
3. Select primary layout from table above
4. If mixed content → primary layout + embedded secondary layouts
5. Apply density adjustment (see Density → Layout Adjustment below)
```

### Density → Layout Adjustment

| Density | Spacing | Card Size | Columns | Font Scale |
|---------|---------|-----------|---------|------------|
| Low (<5 items) | 24-32px gap | Large (360px+) | 1-2 | 1.0x |
| Medium (5-10) | 16-24px gap | Medium (280px) | 2-3 | 0.95x |
| High (>10) | 12-16px gap | Compact (220px) | 3-4 | 0.9x |

### Layout × Content Type Quick Reference

| Content Type | Recommended Layouts (in priority order) |
|-------------|----------------------------------------|
| Enumeration | grid-cards, hub-spoke, periodic-table, bento-grid |
| Comparison | split-comparison, binary-comparison, comparison-matrix, venn-diagram |
| Process | step-flow, linear-progression, funnel, circular-flow, comic-strip, story-mountain |
| Data | dashboard, bento-grid, dense-modules |
| Hierarchy | tree-nested, hierarchical-layers, structural-breakdown, isometric-map |
| Timeline | timeline, winding-roadmap, linear-progression |
| Mixed | bento-grid, dense-modules, iceberg, jigsaw |

## Dimension 2: Style (22 types)

See [`references/aesthetics-guide.md`](aesthetics-guide.md) for the complete style catalog with visual descriptions.

## Dimension 3: Palette (11 schemes)

| # | Palette | Colors | Best With |
|---|---------|--------|-----------|
| 1 | **warm** | Cream bg, amber/orange accents | Education, lifestyle |
| 2 | **elegant** | Off-white bg, navy/gold accents | Business, premium |
| 3 | **cool** | Light gray bg, blue/cyan accents | Technology, SaaS |
| 4 | **dark** | Dark bg, light text, neon accents | Developer tools, gaming |
| 5 | **earth** | Sand/olive bg, terracotta/green accents | Nature, sustainability |
| 6 | **vivid** | White bg, saturated multi-color | Infographics, children |
| 7 | **pastel** | Soft bg, muted accents | Health, wellness |
| 8 | **mono** | Grayscale only | Editorial, brutalist |
| 9 | **retro** | Aged paper bg, faded warm tones | Nostalgia, history |
| 10 | **duotone** | Two-color only (bg + accent) | Bold statements, posters |
| 11 | **macaron** | Soft pink/lavender/mint | Lifestyle, cute |

## Keyword Shortcuts

Certain user phrases auto-map to specific Layout × Style × Palette combinations:

| User Says | Layout | Style | Palette |
|-----------|--------|-------|---------|
| "高密度信息大图" / "信息密集" | dense-modules | morandi-journal or retro-pop-grid | warm or vivid |
| "对比分析" / "vs" | binary-comparison | bold-graphic | duotone |
| "流程图" / "步骤" | step-flow | technical-schematic | cool |
| "架构图" / "系统设计" | isometric-map or tree-nested | technical-schematic | dark or cool |
| "时间线" / "演进" | timeline | aged-academia or retro-pop-grid | retro |
| "仪表盘" / "数据面板" | dashboard | ui-wireframe or corporate-memphis | cool or dark |
| "知识卡片" / "学习笔记" | grid-cards | hand-drawn-edu or storybook-watercolor | warm |
| "杂志风" / "排版" | bento-grid | bold-editorial or editorial-infographic | mono or elegant |
| "信息图" / "可视化" | bento-grid or dense-modules | craft-handmade or pop-laboratory | vivid |
| "PPT" / "演示" | grid-cards or step-flow | corporate-memphis or bold-graphic | cool or elegant |
| "纸墨风" / "Kami" / "雅致" / "财报" | grid-cards or bento-grid | kami-editorial | kami-parchment |

## Content Source Brand DNA Matching

When content originates from a recognizable brand/media, auto-detect and apply its visual DNA. This overrides the default three-dimension auto-selection.

### Detection Logic

```
1. Check URL source domain (if provided)
2. Check content for brand keywords / masthead / byline
3. If brand matched → apply brand DNA preset (highest priority)
4. If no brand detected → fall back to three-dimension auto-selection
```

### Brand DNA Registry

| Brand | Detection Signals | Palette Override | Font Override | Layout Traits |
|-------|------------------|-----------------|---------------|---------------|
| **The Economist** | economist.com, "The Economist", "经济学人" | eco-red #E3120B + black/white/gray | 方正小标宋(display) + 汇文明朝体(serif-body) | Thick rules, no radius, mobile-first 640px |
| **WeChat / 微信公众号** | mp.weixin.qq.com, "公众号", "微信" | WeChat green #07C160 + white | Noto Sans SC | Rounded cards, loose spacing, 578px content width |
| **Apple** | apple.com, "Apple", "苹果" | Pure white + black | SF Pro / PingFang SC | Large whitespace, centered, hero image |
| **36Kr** | 36kr.com, "36氪" | 36Kr blue + dark | Source Han Sans | Dense, compact, tech-news layout |
| **People's Daily / 人民日报** | people.com.cn, "人民日报" | Red #DE2910 + gold #FFDE00 | 方正小标宋 + 仿宋 | Formal, symmetrical, official |
| **Xiaohongshu / 小红书** | xiaohongshu.com, "小红书" | XHS red #FF2442 + warm bg | Noto Sans SC | Card waterfall, lifestyle, photo-heavy |
| **Zhihu / 知乎** | zhihu.com, "知乎" | Zhihu blue #0066FF + white | Noto Sans SC | Q&A layout, long-form, clean |
| **GitHub** | github.com, "GitHub" | Dark bg + green accent | Monospace-heavy | Code blocks, repo stats, markdown |
| **Notion** | notion.so, "Notion" | Off-white + minimal | System UI | Block-based, clean, toggle lists |
| **Kami / 纸墨** | tw93/kami, "Kami", "纸墨风" | kami-parchment #F5F4ED + ink-blue #1B365D | TsangerJinKai02 | Kami Ten Invariants apply |
| **ByteDance / 字节跳动** | bytedance.com, "字节跳动", "抖音", "今日头条" | 字节蓝 #325AB4 + 白/浅灰 | Noto Sans SC | 紧凑卡片、数据密集、信息流风格 |
| **少数派 / sspai** | sspai.com, "少数派" | sspai-red #D93A31 + 白/暖灰 | Noto Sans SC | 长文排版、留白舒适、编辑风 |
| **极客时间** | time.geekbang.org, "极客时间", "极客邦" | 极客蓝 #3564D9 + 深色 | Noto Sans SC | 知识卡片、步骤清晰、课程风 |

### Brand DNA Application Rules

1. **Brand DNA has highest priority** — overrides keyword shortcuts and auto-selection
2. **Only override the dimensions that brand defines** — if brand only defines palette, keep auto-selected layout and style
3. **Always inform user** in Step 2 Confirm & Advise: "Detected content from [Brand], applied [Brand] visual DNA"
4. **User can still override** with `--layout / --style / --palette` flags
5. **Mobile-first for social media sources** — WeChat/Xiaohongshu content defaults to 640px max-width

## Mixed Content Strategy

When content contains multiple types:

1. **Identify dominant type** (by item count or emphasis)
2. **Primary layout** = dominant type's recommended layout
3. **Embed secondary layouts** as subsections within primary
4. **Example**: 7 enumeration points + 1 comparison → grid-cards where one card contains an embedded binary-comparison
5. **For complex mixed content**, prefer bento-grid or dense-modules as they handle diversity natively
