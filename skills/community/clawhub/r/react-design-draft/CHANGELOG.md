# Changelog

All notable changes to this project will be documented in this file.

## [5.3.0] - 2026-06-10

### Added — guizang Methodology Absorption (5 blind spots fixed)

Inspired by op7418's methodology article: "做杂志，不做网页" / "限制不是阻碍，是底线" / "Skill 是一个产品"

- **Category Detection**: Silent pre-Q1 content category identification (10 categories: 深度观察/科技产品/人文文化/职场干货/旅行生活/读书笔记/人物访谈/数据研究/观点评论/教程指南). Each category maps to default Mode + Palette + Key Visual Trait. User's explicit Q1 answer overrides detection.
- **Screenshot Styling**: Device frame components (macOS window / iOS device / Browser chrome), material backgrounds (格纸/点阵/暖白/深色), mode-specific shadow & radius rules, screenshot priority chain
- **Out of Scope declaration**: 6 explicit boundaries — full article typesetting, video, pure image editing, fan content, hard-sell advertising, tutorials >15 cards. "A skill that claims to do everything usually does nothing well."
- **Adaptive Font Size Rules**: Title length → size/weight/line-clamp mapping (Short ≤6 chars → 56-72px/200-400; Extended 25+ → 22-28px/500/3 lines). Dynamic adjustment: never overflow, minimum readable sizes, number emphasis, CJK line-break, line-height scaling. Includes React utility function `getTitleStyle()`.
- **Design Decision "Why" Explanations**: Added rationale to "The Larger, The Lighter" (100 years of magazine design validation) and "Aesthetic Guardrails" (70+ years of Swiss Typographic Style practice, 10 curated palettes validated across hundreds of designs)

### Changed
- Version bumped from 5.2.0 to 5.3.0
- multi-illustration.md Step C: added Category Detection before Q1
- image-sources.md: added Screenshot Styling section
- react-output-spec.md: added Adaptive Font Size Rules section
- aesthetics-guide.md: added "Why it works" / "Why restriction works" rationale blocks
- SKILL.md: added Out of Scope section before Mode Detection

## [5.2.0] - 2026-06-10

### Added — guizang-skill Absorption (6 elements) + Image Sources

- **"The Larger, The Lighter" typography rule**: Large text (56px+) uses weight 200-400, small text (10-12px) uses weight 500-650. A 56px+ title at weight 600+ = instant downgrade to "generic landing page"
- **Dual Style System (Editorial vs Swiss)**: Two complete visual stances — Editorial Magazine (serif + warm paper + atmosphere) vs Swiss International (sans + gray-white + one high-saturation accent). Pick by editorial intent, not content type
  - 4 Swiss Accent Palettes: IKB Blue / Lemon Yellow / Lemon Green / Safety Orange
  - Swiss Gray Scale: 5-step calibrated premium gray (#fafaf8 → #0a0a0a)
  - Style Identity Test: 4-rule Swiss test + 3-rule Editorial test — must pass before delivery
- **Aesthetic Guardrails**: "Protect beauty over freedom" — Swiss mode limited to 4 accent palettes (no custom hex), Editorial mode limited to warm palettes, no cross-mode color mixing
- **Visual Rhythm Planning**: hero/dark/light/accent theme classes across illustrations. Hard rules: no 3+ consecutive same theme, 6+ illustrations must have ≥1 hero + ≥1 dark + ≥1 light
- **Swiss Gray Scale**: Cross-accent unified premium gray system (warm white #fafaf8, not pure white #fff)
- **Image-Text Conflict Protection**: Quiet zone test, subject mapping, object-position discipline, thumbnail test, no full-canvas falloffs
- **Image Sources**: Free stock library integration — Pexels (general), Unsplash (editorial), Wallhaven (cinematic). Mode-based priority, user images first
  - New reference file: `references/image-sources.md`

### Changed
- Version bumped from 5.1.0 to 5.2.0
- SKILL.md Rules expanded from 21 to 27
- aesthetics-guide.md: added Phase 0.5 (Dual Style System), The Larger The Lighter rule, Aesthetic Guardrails, Image-Text Conflict Bans
- multi-illustration.md Step C: Q1 answers now map to Editorial/Swiss modes; added Visual Rhythm Planning section
- Step C Answer→Style Mapping: added Mode column (Editorial/Swiss)

## [5.1.0] - 2026-06-09

### Added — md2wechat-skill Absorption (6 elements)

- **4-Purpose Decision Framework**: Each illustration now tagged with purpose (attention/readability/memorability/conversion), driving silent design parameter adjustments
  - Step A extraction table: added `Purpose` column for all 20 extract types
  - Step B: added Purpose-Based Design Adjustments table (token overrides per purpose)
- **11 new illustration type templates**: verdict-card, audience-fit-card, myth-fact-card, manifesto-card, bridge-card, callout-card, definition-card, cases-card, notice-card, series-card, subscribe-card
  - Emoji mapping table expanded from 13 to 24 entries
- **AI Voice Decontamination (Category 8)**: 10 new anti-patterns (#39-48) for detecting and removing AI-generated text patterns
  - Universal transitions, fake specificity, hollow emphasis, parallel triple, excessive humility, AI hedging, listicle padding, summary-only conclusions, rhetorical question chains, "in today's world" openings
- **Content Readiness Check**: Pre-matching structural check in Step 1 — verifies content has visualizable units before proceeding
- **3 new Brand DNA entries**: ByteDance/字节跳动, 少数派/sspai, 极客时间
- **Uniqueness Constraint**: Anti-pattern for type overuse + per-type max count table (cover:1, verdict:1, quote:2, etc.)

### Changed
- Version bumped from 5.0.0 to 5.1.0
- SKILL.md Step 1: added Content Readiness Check as step 1, renumbered subsequent steps
- SKILL.md Step 1.6: added AI voice decontamination reference
- density-standards.md: expanded from 38 to 48 anti-pattern rules
- content-layout-mapping.md: Brand DNA Registry expanded from 10 to 13 brands
- multi-illustration.md: Step A table expanded from 10 to 20 extract types
- multi-illustration.md: Anti-Patterns expanded from 7 to 8 entries

## [5.0.0] - 2026-06-09

### Added — Persona Layer (人设层)
- **配图大师人设**: "你的工作不是让用户理解设计术语，而是把模糊的'好看'翻译成精确的设计参数"
- **Master Mode**: "大师推荐"/"你定"/"直接来" 一键跳过所有确认点，全自动化生成
- **3-question style customization**: 用3个简单问题（调性→印象→配色）替代23种风格×12种配色选择
- **Emoji + description mapping**: 13种内部类型翻译为用户可理解的 emoji + 一句话描述
- **User-friendly Step B output**: 配图方案用自然语言展示，密度评分内部计算不暴露
- **Usage Guide (Step E)**: 文章章节→配图位置映射 + 快速修改指令，替代技术文档

### Added — Aesthetics Philosophy Layer (审美哲学层)
- **The Three Constraints (三大约束)**: 克制(Restraint) + 呼吸(Breathing) + 温度(Warmth)
  - 克制: 品牌色≤5%面积，单色原则
  - 呼吸: whisper shadow，0.5pt边框，8pt圆角
  - 温度: 暖灰色系，禁冷蓝灰，禁纯白背景
- **Warm gray scale**: 7级暖灰色替代冷蓝灰色（#141413→#3d3d3a→#504e49→#6b6a64→#e8e6dc→#f5f4ed→#faf9f5）
- **Serif weight lock**: 衬线体锁定500，禁止700/900
- **CJK letter-spacing**: 中文衬线正文0.3pt，标题0.2-1pt
- **Anti-Slop 8 red lines**: 禁止连续同布局/纯白背景/冷蓝灰/衬线粗体/硬投影/rgba标签等

### Changed
- Version bumped from 4.2.0 to 5.0.0
- SKILL.md: Mode Detection 增加 Master Mode 入口
- SKILL.md: Step 2 从技术参数展示改为3问题降维
- SKILL.md: Rules 从15条扩展到19条，增加审美哲学层规则
- multi-illustration.md: Step B 从技术方案改为人话版+大师建议
- multi-illustration.md: Step C 从风格参数改为3问题定制
- multi-illustration.md: Step E 从配图地图改为使用指南
- aesthetics-guide.md: 增加 Phase 0 审美哲学层（三大约束+8条红线）

## [4.2.0] - 2026-06-09

### Added
- **3 knowledge card sub-types**: rule-card, checklist-card, cheatsheet-card
  - rule-card: numbered rules + violation consequence (e.g., "三条铁律")
  - checklist-card: items + severity markers (e.g., "7条安全红线")
  - cheatsheet-card: name + example pairs, ultra-compact (e.g., "B1-B6访谈规则")
- **3 logic visualization sub-types**: logic-chain, process-pipeline, version-timeline
  - logic-chain: causal reasoning (A导致B导致C)
  - process-pipeline: phase-based pipeline with input/output (Phase 0→1→2)
  - version-timeline: iteration history (v1→v2→v3)
- **Cover/back-cover density gate exemption**: threshold lowered to ≥6/15 (vs ≥9/15 for other types)
  - Rationale: cover/back-cover value is brand identity, not information density

### Changed
- Version bumped from 4.1.0 to 4.2.0
- multi-illustration.md: logic-chain template expanded into 3 distinct types with selection guide
- multi-illustration.md: quote-card section expanded with 4 sub-type templates + selection guide

## [4.1.0] - 2026-06-09

### Added
- **Multi-Illustration Mode**: Generate multiple illustrations for a single article
  - Step A: Article parsing (extract thesis, data, logic chains, quotes, comparisons)
  - Step B: Illustration plan + density scoring (3-dimension 15-point gate, ≥9/15 to generate)
  - Step C: Style unification confirmation (shared design-tokens.css across all illustrations)
  - Step D: Batch generation (shared tokens + per-illustration data/components)
  - Step E: Illustration map (article section ↔ illustration mapping)
  - Two mandatory confirmation points: content plan + style plan
  - Content drives quantity, not templates
  - Every illustration independently passes density gate
- **5 new illustration templates**: cover, back-cover, quote-card, section-divider, logic-chain
- **WeChat public account size specs**: 封面 900×383, 正文 640px, 金句 640×640
- **Multi-illustration anti-patterns**: forced quantity, filler illustrations, style drift, duplicate info
- Mode detection: "多图"/"配图"/"全套"/"文章配图" triggers Multi-Illustration Mode
- Rules #14 and #15 added for multi-illustration content-driven quantity and density gate

### Changed
- Version bumped from 4.0.0 to 4.1.0
- SKILL.md restructured: Mode Detection section + Single Draft Mode + Multi-Illustration Mode
- Rule #3 updated: density threshold now differentiates single mode (≥16/25) vs multi mode (≥9/15)

## [4.0.0] - 2026-06-08

### Added
- **Chart system** (P0): 14 chart types with auto-selection decision tree + CSS/SVG implementation specs
  - bar-chart, horizontal-bar-chart, line-chart, donut-chart, quadrant-chart
  - flow-chart, swimlane-chart, state-machine, tree-chart, layered-diagram
  - venn-diagram, candlestick-chart, waterfall-chart, treemap
- **Brand Profile system** (P0): Four-layer brand configuration with priority resolution
  - Layer 1: Explicit prompts (highest)
  - Layer 2: Brand DNA auto-detection
  - Layer 3: User brand profile (`~/.config/react-design-draft/brand.md`)
  - Layer 4: Three-dimension auto-selection (lowest)
  - Project style scanning (CSS/tailwind/tokens extraction)
- **Kami Full Token System** (P1): 20+ CSS variables replacing simplified 3-variable kami-parchment
  - Brand: --kami-brand, --kami-brand-light
  - Surfaces: --kami-parchment, --kami-ivory, --kami-warm-sand, --kami-dark-surface, --kami-deep-dark
  - Text: --kami-near-black, --kami-dark-warm, --kami-olive, --kami-stone
  - Borders: --kami-border, --kami-border-soft
  - Derivatives: --kami-brand-tint, --kami-tag-bg, --kami-breaking-bg, --kami-breaking-fg
- **Extended Anti-Patterns** (P1): 7 categories, 38 rules (up from 10 red lines)
  - Content Hollow (#1-5), Metric Fraud (#6-10), Structural Mimicry (#11-15)
  - Visual Excess (#16-19), Source Missing (#20-23), Tone Pollution (#24-29)
  - CJK & Layout Specific (#30-38)
- **Writing quality gate** (P1): Assertion-evidence, Impact formula, data-over-adjectives, no-AI-officialese
- **Document type presets** (P2): 9 Kami-inspired templates
  - one-pager-doc, long-doc, letter, portfolio, resume, equity-report, changelog, landing-page, slides
- **Multi-language font stacks** (P2): Japanese (YuMincho) and Korean (Source Han Serif K)
- **Slide scaling formula** (P2): Macro ×1.6, Micro ×0.5, with 7 property-specific rules
- Step 0: Brand Profile added to execution flow
- SKILL.md Rules expanded from 10 to 13 (added #11 Brand profile, #12 Chart auto-selection, #13 Writing quality gate)

### Changed
- Version bumped from 3.0.0 to 4.0.0
- Execution flow: 4 steps → 5 steps (added Step 0: Brand Profile)
- Step 1 now includes chart needs detection and content quality pre-check
- Step 2 Confirm & Advise now includes chart type recommendation
- Step 3 now references chart-system.md

## [3.0.0] - 2026-06-08

### Added
- Three-dimension combination system: Layout × Style × Palette (5,086 combinations)
- 25 layout patterns covering enumeration, comparison, process, data, hierarchy, timeline, and mixed content
- 23 visual styles across 6 categories (Professional, Editorial, Hand-crafted, Digital, Playful, Elegant)
- 12 color palettes including kami-parchment
- 7 font presets with local-first CJK font strategy
- 11 local font registry entries (汇文明朝体, 宋徽宗瘦金体, 仓耳今楷02, etc.)
- 29 quick presets with keyword trigger mapping
- 5-dimension density scoring system (25-point scale, ≥16 threshold)
- 10 density anti-pattern red lines
- Kami Ten Invariants for kami-editorial style
- Pre-generation consultation (Step 2: Confirm & Advise)
- Post-generation edit guide (Step 4: mandatory)
- Component granularity rules (≤80 lines, 5 extraction triggers)
- Interactive edit matrix (13 user intents → file → action)
- Agent platform edit workflow comparison (React vs image design drafts)
- React 4-piece output specification (design-tokens.css / data.js / components/*.jsx / App.jsx)

### Changed
- Font strategy from Web-first to Local-first, Web-fallback
- Step 2 upgraded from "Confirm" to "Confirm & Advise" with adaptation advice
- Step 4 added as mandatory Post-Generation Guide

### Fixed
- SKILL.md frontmatter: added version, category, metadata.requires_api_key
- Description trimmed to ≤150 characters
- Style → Font mapping completed for all 23 styles (was missing 8)
