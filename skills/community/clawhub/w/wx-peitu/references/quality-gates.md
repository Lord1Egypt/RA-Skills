# Quality Gates Reference

## Core Principle

**Density = Signal per Pixel**. High density means more useful information per unit of visual space, NOT more visual noise.

## Density Scoring

For each design draft, evaluate on these 5 dimensions (each 1-5 points):

### 1. Content Utilization Rate

| Score | Standard |
|-------|----------|
| 1 | < 30% of viewport carries information, rest is decoration |
| 2 | 30-50% content, significant empty decoration |
| 3 | 50-70% content, balanced whitespace |
| 4 | 70-85% content, purposeful whitespace only |
| 5 | > 85% content, every pixel serves a purpose |

### 2. Information Hierarchy Clarity

| Score | Standard |
|-------|----------|
| 1 | Flat structure, no visual distinction between levels |
| 2 | 2 levels distinguishable (title vs body) |
| 3 | 3 levels clear (title → subtitle → body) |
| 4 | 4+ levels with consistent scale system |
| 5 | 4+ levels + visual encoding (color/size/weight/position) maps to importance |

### 3. Data-Ink Ratio (Tufte)

| Score | Standard |
|-------|----------|
| 1 | > 60% of visual elements are non-informational (borders, backgrounds, decorations) |
| 2 | 40-60% non-informational ink |
| 3 | 25-40% non-informational ink |
| 4 | 10-25% non-informational ink |
| 5 | < 10% non-informational ink, every line/shade carries meaning |

### 4. Scanning Efficiency

| Score | Standard |
|-------|----------|
| 1 | User must read everything to find key info |
| 2 | Key info identifiable with effort |
| 3 | Key info findable within 3 seconds |
| 4 | Key info immediately visible, hierarchy guides eye naturally |
| 5 | F-pattern/Z-pattern optimized, key info in expected positions |

### 5. Whitespace Purposefulness

| Score | Standard |
|-------|----------|
| 1 | Random or excessive whitespace |
| 2 | Whitespace exists but inconsistent |
| 3 | Consistent spacing system (4/8px grid) |
| 4 | Whitespace creates clear grouping (proximity principle) |
| 5 | Whitespace is an active design element — creates rhythm, emphasis, and breathing |

## Minimum Quality Threshold

Two scoring systems are used depending on context:

| 模式 | 评分系统 | 维度 | 及格线 | 说明 |
|------|---------|------|--------|------|
| **Single illustration** | 5维25分 | Content Utilization / Information Hierarchy / Data-Ink Ratio / Scanning Efficiency / Whitespace Purposefulness | ≥ 16/25 | 单张独立设计稿 |
| **Multi per-illustration** | 3维15分 | 取5维中得分最高的3个维度 | ≥ 9/15 | 多图模式下的单张 |
| **Cover / back-cover** | 3维15分 | 同上 | ≥ 6/15 | 视觉冲击可覆盖密度 |

SKILL.md Rule 7 中的 `≥9/15` 指 Multi 模式下的3维评分。

If threshold not met, identify the weakest dimension and improve before outputting.

## Canvas Coverage Hard Rule

On 640px-wide canvases, content must cover ≥70% of canvas height. Any pure-whitespace band >20% of canvas height (>128px) needs a stated reason — hero-image breathing, single-sentence statement, or leading/trailing margins (combined ≤20%).

On 900×383 covers, photo + title + subtitle must cover ≥60% of canvas.

On 640×640 quote cards, the quote + attribution + at least one anchor (kicker/meta/hairline rule) must exist. A quote without anchors reads as "missing content", not "intentional whitespace".

**Do NOT use `flex: 1` or `justify-content: center` to push content to the vertical center.** Social cards are scrolled one at a time; under-filled cards read as "PowerPoint with a missing element."

Each recipe in `assets.md` carries a `Minimum density:` line. If your content doesn't reach that floor, **switch to a different recipe or shorten the canvas** — never just publish under-filled.

## Density Anti-Patterns (Red Lines)

These patterns indicate density has crossed into clutter. **Any one = reject and fix**:

| Anti-Pattern | Detection Rule |
|-------------|---------------|
| **Card nesting > 2 levels** | Card inside card inside card = visual noise |
| **> 3 font sizes in one card** | Indicates hierarchy failure |
| **> 4 colors used as accents** | Color coding loses meaning beyond 4 |
| **Horizontal scrolling required** | Content overflow = layout failure |
| **Text < 12px** | Readability threshold violated |
| **Line height < 1.4** | Cramped text = unreadable at high density |
| **> 2 box-shadow layers** | Depth illusion becomes noise |
| **Border + background + shadow on same element** | Triple emphasis = no emphasis |
| **Icon + emoji + badge on same line** | Visual overload |
| **Grid gap < 8px** | Elements merge visually |

## Extended Anti-Patterns (8 Categories, 48 Rules)

Inspired by Kami's anti-pattern system. These are quality gates, not suggestions.

### Category 1: Content Hollow (#1-5)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 1 | Adjective stacking without numbers | Write specific numbers: "3x faster" not "much faster" |
| 2 | Filler opening paragraphs | Delete, start directly with the point |
| 3 | Title restated as sentence | Body must add information the title doesn't carry |
| 4 | Vague time references ("recently", "lately") | Anchor to date/quarter: "Q4 2025" |
| 5 | Synonyms masking repetition | One claim, one evidence, move on |

### Category 2: Metric Fraud (#6-10)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 6 | Integer implying precision | Match source precision: "approximately 40%" not "40%" |
| 7 | Fake decimal precision | Round to source precision or state "approximately" |
| 8 | Metric-narrative disconnect | Text must match what the chart shows |
| 9 | Fabricated comparison baseline | Name the alternative and baseline method |
| 10 | Mixed time periods in comparison | Label each comparison window explicitly |

### Category 3: Structural Mimicry (#11-15)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 11 | Resume entries without results | Use Impact formula: Action + Scope + Measurable Result |
| 12 | Template slot filling | Name specific skills and application scenarios |
| 13 | Research report without differentiated insight | State what the market is getting wrong |
| 14 | One-pager without clear ask | Ask must be above the fold |
| 15 | Slide title is label not assertion | Use assertion-evidence pattern: "Revenue grew 3x" not "Revenue" |

### Category 4: Visual Excess (#16-19)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 16 | > 3 brand-color accents per page | One accent color is enough |
| 17 | Chart without insight title | Title must state the insight, not just the metric |
| 18 | Decorative chart restating text | Chart must add a dimension text doesn't convey |
| 19 | Icons/emoji as section markers | Use typographic hierarchy instead |

### Category 5: Source Missing (#20-23)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 20 | Unverified version numbers | Check official source before writing |
| 21 | "Latest" without date | Always attach a date |
| 22 | Competitive comparison without market data | Cite ranking source |
| 23 | Assumed availability | List actually verified platforms |

### Category 6: Tone Pollution (#24-29)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 24 | Chinese AI officialese (赋能/打造/拥抱/助力) | Say what it does, not what it "empowers" |
| 25 | English AI officialese (leverage/unlock/seamlessly) | Use human language |
| 26 | Caption restating flowchart | Give judgment beyond what the diagram shows |
| 27 | AI tone markers (dash stacking, meta-commentary) | Delete meta-comments, replace dashes with colons/periods |
| 28 | Sans font stack missing CJK fallback | Any element that might render CJK must include `var(--serif)` |
| 29 | Caption restating slide title | Caption must give information the title doesn't |

### Category 7: CJK & Layout Specific (#30-38)

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 30 | CJK/Latin number baseline drift | Use `font-variant-numeric: lining-nums tabular-nums` |
| 31 | Currency symbol scaling misaligned | Use `font-size: 0.74em; transform: translateY(0.015em)` |
| 32 | Tag background using rgba | Use solid hex only (WeasyPrint double-rect bug) |
| 33 | Hard drop shadows | Use ring shadow or whisper shadow |
| 34 | Pure white (#FFF) background | Use parchment #f5f4ed or off-white |
| 35 | Pure black (#000) text | Use near-black #141413 or #1D1D1B |
| 36 | Serif synthetic bold (600/700) | Lock serif at 400/500 only |
| 37 | Cool blue-gray tones | All grays must be warm-toned (yellow-brown undertone) |
| 38 | Italic in print/PDF templates | Italic only allowed in screen-only contexts |
| 38a | Flex centering on social card (using `flex:1` or `justify-content:center` to vertically center sparse content) | Fill the canvas with content, or switch to a smaller canvas/recipe |
| 38b | Under-filled 640px card with <70% content coverage | Add pull quote, evidence image, marginal column, or ledger rows |
| 38c | Cover title without photo background (纯色封面) | All covers must use photo background — hero pages must stop the scroll |
| 38d | Mixed Editorial/Swiss recipes in same set | Pick one mode for all body illustrations; only covers may differ |
| 38e | Same recipe 3+ times consecutively | Force layout diversity — switch recipe every 2 cards max |

### Category 8: AI Voice Decontamination (#39-48)

Inspired by md2wechat's humanize principle. These rules detect and remove AI-generated text patterns that feel inauthentic to human readers.

| # | Anti-Pattern | Fix |
|---|-------------|-----|
| 39 | Universal transition phrases ("值得注意的是"/"需要指出的是"/"值得一提的是") | Delete entirely; if the point matters, state it directly |
| 40 | Fake specificity ("多个"/"若干"/"一系列" without exact count) | Replace with exact number: "3个"/"5项" |
| 41 | Hollow emphasis ("至关重要"/"不可或缺"/"举足轻重") | Replace with specific evidence: "占营收62%" not "至关重要" |
| 42 | Parallel triple structure (3 consecutive identical sentence patterns) | Vary structure; use one short + one long + one question |
| 43 | Excessive humility ("仅供参考"/"个人浅见"/"不揣浅陋") | State the claim confidently; let evidence do the hedging |
| 44 | AI hedging ("在一定程度上"/"从某种意义上说") | Either commit to the claim or add a specific condition |
| 45 | Listicle padding (item that restates the intro) | Each list item must add a NEW dimension, not rephrase |
| 46 | Conclusion that merely summarizes | Conclusion must escalate: add a judgment or implication not stated before |
| 47 | Rhetorical question chain (>2 consecutive questions) | Replace with assertions; questions are for the reader, not the writer |
| 48 | "In today's world" / "在当今时代" opening | Start with the specific claim, not the era |

## Spacing System

Use a consistent spacing scale based on 4px:

```
4px  — micro (icon-to-label)
8px  — tight (badge-to-text)
12px — compact (list items)
16px — standard (card padding)
24px — comfortable (section gap)
32px — generous (major section)
48px — spacious (page sections)
64px — expansive (hero spacing)
```

**Rule**: Only use values from this scale. No arbitrary margins.

## Typography Scale

```
12px / 1.4 — caption, metadata, timestamps
14px / 1.5 — body text, descriptions
16px / 1.5 — large body, lead text
20px / 1.4 — subtitle, card titles
24px / 1.3 — section headings
32px / 1.2 — page headings
48px / 1.1 — hero titles
```

**Font weight mapping**:
- 400: body, descriptions
- 500: labels, badges
- 600: subtitles, card titles
- 700: headings
- 800: hero titles

## Grid System

- **Base unit**: 4px
- **Column count**: 12-column grid
- **Gutter**: 16px (compact) / 24px (standard) / 32px (spacious)
- **Max content width**: 1200px
- **Breakpoints**: 640px / 768px / 1024px / 1280px
