# Theme Presets

## Purpose

Use these preset ids when the user wants an optional article color style for WeChat formatting.
This file is the local source of truth for preset ids, display names, and fallback behavior used by this repository.

## Fallback Behavior

- Fallback preset id: `warm-editorial`
- The preset display name `紫色高亮（Default）` is a regular preset name in this catalog, not the fallback preset.

## Available Presets

| Preset ID | Display Name | Visual Direction |
| --- | --- | --- |
| `warm-editorial` | 暖调专栏（Editorial） | Warm editorial column style with grounded neutral text, clay accents, cream information surfaces, strong scan rhythm, and copy-safe diagrams for long-form reading. |
| `light-simple` | 极简黑白（Simple） | Modern monochrome editorial style with strong spacing, crisp rules, restrained gray surfaces, and typography-led hierarchy. |
| `tech-blue` | 科技蓝（Theme1） | Clean technology article style with blue accents, pale information surfaces, numbered headings, and precise insight blocks. |
| `indigo-card` | 靛青卡片（Theme2） | Soft indigo card-based editorial style with lavender surfaces, compact rounded modules, and calm contrast. |
| `swiss-grid` | 瑞士网格（Swiss Grid） | Swiss magazine style with strict spacing, black rules, red accents, grid-like heading treatments, and high contrast modules. |
| `purple-highlight` | 紫色高亮（Default） | Polished highlight style with purple accents, soft callouts, emphatic pull quotes, and luminous summary sections. |
| `warm-nature` | 自然森系（Warm Nature） | Warm knowledge article style with green accents, organic muted surfaces, gentle quote blocks, and grounded section rhythm. |
| `vitality-orange` | 活力橙（Vitality） | Energetic creator/business article style with orange accents, warm highlight bands, bold takeaways, and lively but controlled hierarchy. |
| `wechat-pure-glass` | 原生微光（Pure Glass） | Native WeChat-friendly style with green accents, light translucent-feeling cards expressed as inline-safe surfaces, and approachable business readability. |
| `modern-cobalt` | 现代钴蓝（Cobalt） | Premium cobalt editorial style with deep blue accents, soft blue surfaces, strong numbered headings, and polished analytical modules. |
| `deep-space` | 深空探索（Space） | Dark editorial style with luminous blue accents, low-glare surfaces, clear contrast, and immersive science or technology emphasis. |

## Component Expectations

Each preset must be expressed through component-level inline styles, not just color substitutions.
When an element exists in the article, apply a deliberate treatment for it:

- `article`: max width, readable padding, foreground color, font family, and line height.
- `hero`: distinct top area with eyebrow, title, and deck styling.
- `eyebrow` and `moduleLabel`: compact monospace labels for column names, section counters, or module names when those labels already exist in the source.
- `h2`: visible theme treatment such as accent rule, number badge, tinted strip, or typographic contrast.
- `h3`: compact secondary heading with clear spacing and no oversized display treatment.
- `p`: comfortable paragraph rhythm with explicit margin, font size, color, and line height.
- `blockquote`: pull-quote or insight-block treatment with accent, padding, surface, and text color.
- `callout`: lightweight information module for source callouts, warnings, examples, or notes that already exist in the source.
- `summary`: compact takeaway module with different background or border treatment from normal sections.
- `strong` and `a`: theme-consistent emphasis colors and safe inline styles.
- `ul`, `ol`, and `li`: explicit spacing and marker color when lists appear.
- `hr`: styled divider when separators are used.
- `figure`, `img`, and `figcaption`: full-width image treatment, safe border radius, caption color, and spacing when images appear.
- `table`, `th`, and `td`: readable inline-styled table treatment when tables appear.
- `code` and `pre`: safe wrapping, readable contrast, and theme-consistent surface when code appears.

## Fixed Color Tokens

Most existing values are synchronized from the source theme constants in `D:\code\wechatgo\src\lib\wechatTheme.ts`.
`warm-editorial` is maintained locally as the default WeChat article preset.
Use these colors as fixed design tokens for each preset.
Do not infer new theme colors from the preset name when a matching token exists.

| Preset ID | Source Constant | Text | Heading | Accent | Muted | Surface | Border | Quote Surface | Code Surface | Code Text | Table Header | Table Border |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `warm-editorial` | `WECHAT_WARM_EDITORIAL` | `#3d3d3a` | `#141413` | `#b85c3e` | `#8a8175` | `#faf7f0` | `#ded7ca` | `#f0eee6` | `#f0eee6` | `#b04a3f` | `#fbfaf6` | `#d1cfc5` |
| `light-simple` | `WECHAT_LIGHT_SIMPLE_THEME` | `#2c3e50` | `#000000` | `#000000` | `#666` | `#f9fafb` | `#e5e7eb` | `transparent` | `#f3f4f6` | `#e11d48` | `#f9fafb` | `#e5e7eb` |
| `tech-blue` | `WECHAT_LIGHT_THEME1` | `#333333` | `#1772b4` | `#1772b4` | `#666` | `#eff6ff` | `#b3cdf2` | `#f7f9fc` | `#f6f8fa` | `#24292e` | `#eff6ff` | `#b3cdf2` |
| `indigo-card` | `WECHAT_LIGHT_THEME2` | `#374151` | `#4338ca` | `#4f46e5` | `#6b7280` | `#e0e7ff` | `#c7d2fe` | `#f9fafb` | `#f8fafc` | `#334155` | `#e0e7ff` | `#c7d2fe` |
| `swiss-grid` | `WECHAT_SWISS_GRID` | `#1a1a1a` | `#000000` | `#000000` | `#666` | `#f8f8f8` | `#1a1a1a` | `transparent` | `#f8f8f8` | `#333` | `#f8f8f8` | `#1a1a1a` |
| `purple-highlight` | `WECHAT_LIGHT_THEME` | `#1f2937` | `#111827` | `#7c3aed` | `#6b7280` | `#fbfbfe` | `#c4b5fd` | `#fbfbfe` | `#ffffff` | `#581c87` | `#f5f3ff` | `#c4b5fd` |
| `warm-nature` | `WECHAT_WARM_NATURE` | `#44403c` | `#3f6212` | `#84cc16` | `#78716c` | `#ecfccb` | `#d9f99d` | `#fafaf9` | `#fdf6e3` | `#657b83` | `#ecfccb` | `#d9f99d` |
| `vitality-orange` | `WECHAT_VITALITY_ORANGE` | `#292524` | `#c2410c` | `#f97316` | `#431407` | `#fff7ed` | `#fdba74` | `#fff7ed` | `#fff7ed` | `#431407` | `#fff7ed` | `#fdba74` |
| `wechat-pure-glass` | `WECHAT_PURE_GLASS` | `#1f2937` | `#07c160` | `#07c160` | `#374151` | `#f2fbf6` | `#d1d5db` | `#f2fbf6` | `#f2fbf6` | `#064e3b` | `#f9fafb` | `#d1d5db` |
| `modern-cobalt` | `WECHAT_MODERN_COBALT` | `#1f2937` | `#1e40af` | `#1e40af` | `#64748b` | `#eff6ff` | `#e2e8f0` | `transparent` | `#f8fafc` | `#334155` | `#f8fafc` | `#e2e8f0` |
| `deep-space` | `WECHAT_DEEP_SPACE` | `#0f172a` | `#7c3aed` | `#06b6d4` | `#475569` | `#f8fafc` | `#7c3aed` | `#0b0c15` | `#f8fafc` | `#0f172a` | `#1e1b4b` | `#7c3aed` |

## Scene Color Defaults

Use these optional semantic colors for scenario-specific modules when the injected theme JSON does not provide them.
These defaults keep warning, positive, and summary blocks aligned with each preset instead of falling back to the warm editorial colors.

| Preset ID | Summary Surface | Summary Text | Warning Surface | Warning Text | Warning Border | Positive Surface | Positive Text | Positive Border |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `warm-editorial` | `#faf7f0` | `#3d3d3a` | `#f6e8e4` | `#7a2f29` | `#d97757` | `#f1f5ec` | `#5f7748` | `#cbd6bd` |
| `light-simple` | `#f9fafb` | `#2c3e50` | `#fff1f2` | `#e11d48` | `#fecdd3` | `#f0fdf4` | `#166534` | `#bbf7d0` |
| `tech-blue` | `#eff6ff` | `#1e3a8a` | `#fff1f0` | `#cf222e` | `#fecaca` | `#ecfdf5` | `#047857` | `#a7f3d0` |
| `indigo-card` | `#e0e7ff` | `#4338ca` | `#fff1f2` | `#be123c` | `#fecdd3` | `#eff6ff` | `#2563eb` | `#bfdbfe` |
| `swiss-grid` | `#f8f8f8` | `#000000` | `#fff1f1` | `#b91c1c` | `#000000` | `#f1f1f1` | `#1a1a1a` | `#1a1a1a` |
| `purple-highlight` | `#f5f3ff` | `#581c87` | `#fff1f2` | `#be123c` | `#fecdd3` | `#f3e8ff` | `#6b21a8` | `#c4b5fd` |
| `warm-nature` | `#ecfccb` | `#3f6212` | `#fdf6e3` | `#78350f` | `#fde68a` | `#f5f5f4` | `#4d7c0f` | `#d9f99d` |
| `vitality-orange` | `#fff7ed` | `#c2410c` | `#ffedd5` | `#431407` | `#fdba74` | `#fff7ed` | `#db2777` | `#fed7aa` |
| `wechat-pure-glass` | `#f2fbf6` | `#064e3b` | `#fff7ed` | `#c2410c` | `#fed7aa` | `#f2fbf6` | `#065f32` | `#07c160` |
| `modern-cobalt` | `#eff6ff` | `#1e40af` | `#fff1f2` | `#be123c` | `#fecdd3` | `#f1f5f9` | `#2563eb` | `#93c5fd` |
| `deep-space` | `#1e1b4b` | `#e9d5ff` | `#f3e8ff` | `#581c87` | `#7c3aed` | `#e2e8f0` | `#0f172a` | `#06b6d4` |

## Full Theme Palettes

When a semantic token above does not cover a specific component, use only colors from the matching full palette below before introducing any new color.

| Preset ID | Full Palette |
| --- | --- |
| `warm-editorial` | `#3d3d3a`, `#141413`, `#b85c3e`, `#d97757`, `#8a8175`, `#6f6c64`, `#faf7f0`, `#fbfaf6`, `#f0eee6`, `#ded7ca`, `#d1cfc5`, `#ffffff`, `#f6e8e4`, `#7a2f29`, `#f1f5ec`, `#5f7748`, `#cbd6bd`, `#b04a3f` |
| `light-simple` | `#2c3e50`, `#eaeaea`, `#000000`, `#333333`, `#666`, `#000`, `#333`, `#f3f4f6`, `#e11d48`, `#f9fafb`, `#e5e7eb`, `#374151`, `#1a1a1a` |
| `tech-blue` | `#333333`, `#1772b4`, `#eff6ff`, `#1e3a8a`, `#666`, `#f7f9fc`, `#b3cdf2`, `#555555`, `#fff1f0`, `#cf222e`, `#f6f8fa`, `#d0d7de`, `#24292e` |
| `indigo-card` | `#374151`, `#e0e7ff`, `#111827`, `#4338ca`, `#4f46e5`, `#6b7280`, `#f9fafb`, `#4b5563`, `#f3f4f6`, `#eff6ff`, `#2563eb`, `#f8fafc`, `#e2e8f0`, `#334155`, `#c7d2fe` |
| `swiss-grid` | `#1a1a1a`, `#333`, `#e5e5e5`, `#000`, `#666`, `#999`, `#333333`, `#f1f1f1`, `#f8f8f8`, `#eee`, `#000000` |
| `purple-highlight` | `#1f2937`, `#111827`, `#5b21b6`, `#6b7280`, `#7c3aed`, `#374151`, `#fbfbfe`, `#8b5cf6`, `#555`, `#f3e8ff`, `#6b21a8`, `#ffffff`, `#e9d5ff`, `#581c87`, `#c4b5fd`, `#f5f3ff` |
| `warm-nature` | `#44403c`, `#3f6212`, `#d9f99d`, `#1a2e05`, `#ecfccb`, `#84cc16`, `#1c1917`, `#fde68a`, `#78716c`, `#4d7c0f`, `#fafaf9`, `#57534e`, `#e7e5e4`, `#f5f5f4`, `#78350f`, `#fdf6e3`, `#eee8d5`, `#657b83` |
| `vitality-orange` | `#292524`, `#fff7ed`, `#f97316`, `#fed7aa`, `#db2777`, `#c2410c`, `#ea580c`, `#ffedd5`, `#431407`, `#fff`, `#fdba74` |
| `wechat-pure-glass` | `#1f2937`, `#374151`, `#f2fbf6`, `#111827`, `#07c160`, `#000`, `#065f32`, `#1c1c1e`, `#064e3b`, `#d1d5db`, `#f9fafb` |
| `modern-cobalt` | `#1f2937`, `#374151`, `#111827`, `#1e40af`, `#eff6ff`, `#2563eb`, `#93c5fd`, `#64748b`, `#f1f5f9`, `#0f172a`, `#f8fafc`, `#e2e8f0`, `#334155`, `#1e293b` |
| `deep-space` | `#0f172a`, `#334155`, `#cbd5e1`, `#3b0764`, `#7c3aed`, `#06b6d4`, `#475569`, `#d8b4fe`, `#0b0c15`, `#e2e8f0`, `#1e293b`, `#f3e8ff`, `#581c87`, `#f8fafc`, `#1e1b4b`, `#e9d5ff` |

## Fixed Typography Tokens

These typography tokens combine common WeChat Official Account layout guidance with the source values already used in `D:\code\wechatgo\src\lib\wechatTheme.ts`.
Use these sizes as fixed defaults for generated article HTML.
Do not infer new font sizes from the preset name.

Research basis:

- Common WeChat layout guidance places body text around `14px` to `16px`, with `15px` as a broadly compatible default.
- H2 or small section headings commonly sit around `16px` to `18px`; large titles commonly sit around `18px` to `22px`, while designed article hero titles may go up to `24px` to `28px`.
- Notes, sources, captions, and auxiliary text commonly sit around `10px` to `14px`.
- Comfortable article line height is commonly `1.5` to `2`; use `1.75` as the default long-reading rhythm.

| Token | Fixed Value | Use |
| --- | --- | --- |
| `articleBase` | `15px` | Root article text and normal body paragraphs. |
| `articleBaseLong` | `16px` | Optional long-read body/list text when the theme source already uses 16px list paragraphs or when readability matters more than density. |
| `heroEyebrow` | `13px` | Short category, source, or kicker above h1. |
| `heroTitle` | `24px` | Default h1/hero title size. |
| `heroTitleLarge` | `26px` | Strong editorial h1 size used by several source themes. |
| `heroTitleMax` | `28px` | Maximum h1 size; use only for short hero titles. |
| `heroDek` | `16px` | Subtitle, deck, or intro below h1. |
| `sectionTitle` | `18px` | Default h2 size. |
| `sectionTitleCompact` | `17px` | Compact h2 size for card-like or pill-like themes. |
| `sectionTitleLarge` | `20px` | Strong h2 size for Swiss/grid or space-style themes. |
| `sectionTitleMax` | `22px` | Maximum h2 size; use only when matching the source theme. |
| `minorHeading` | `16px` | Default h3 size. |
| `minorHeadingLarge` | `17px` | Slightly stronger h3 size. |
| `quote` | `15px` | Blockquote, insight block, or pull quote body. |
| `list` | `15px` | Default list item or pseudo-list paragraph text. |
| `listReadable` | `16px` | Long-read list text for themes that already use 16px list paragraphs. |
| `table` | `14px` | Table body and header text. |
| `inlineCode` | `14px` | Default inline code text. |
| `inlineCodeCompact` | `13px` | Compact inline code text when the source theme uses it. |
| `codeBlock` | `13px` | Code block text. |
| `caption` | `13px` | Image caption, figure note, or source line. |
| `captionLarge` | `14px` | Image caption when stronger credibility labeling is needed. |
| `note` | `12px` | Footnote, metadata, legal note, or auxiliary source text. |
| `dividerText` | `12px` | Text inside separators or compact section labels. |

Warm editorial defaults:

- Use `16px` body text when the article is a long read or when the source paragraphs are dense.
- Use `20px` for strong H2 headings in `warm-editorial`; this keeps section titles prominent while staying within mobile WeChat reading norms.
- Use `12px` monospace labels for eyebrows, section counters, module labels, and table/module captions when such labels already exist.

Use these line-height defaults unless a theme source value below is more specific:

| Token | Fixed Value | Use |
| --- | --- | --- |
| `headingLineHeightTight` | `1.2` | H1 and compact display headings. |
| `headingLineHeight` | `1.3` | H2 and H3 headings. |
| `bodyLineHeight` | `1.7` | Default paragraph rhythm. |
| `bodyLineHeightLoose` | `1.75` | Long-read paragraph rhythm. |
| `listLineHeight` | `1.75` | Default list rhythm. |
| `codeLineHeight` | `1.6` | Code blocks and tables. |

## Theme Typography Snapshot

These values come from the matching source constants in `D:\code\wechatgo\src\lib\wechatTheme.ts`.
When generating a named preset, prefer the row below over the common defaults.

| Preset ID | Base | Line Height | H1 | H2 | H3 | Quote | List | Inline Code | Code Block | Table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `warm-editorial` | `16px` | `1.8` | `24px` | `20px` | `16px` | `18px / 1.75` | `16px / 1.8` | `14px` | `13px / 1.65` | `14px / 1.65` |
| `light-simple` | `15px` | `1.7` | `26px` | `22px` | `18px` | `15px` | `15px / 1.8` | `14px` | `13px / 1.7` | `14px / 1.6` |
| `tech-blue` | `15px` | `1.7` | `22px` | `18px` | `17px` | `15px` | `15px / 1.75` | `14px` | `13px / 1.6` | `14px / 1.6` |
| `indigo-card` | `15px` | `1.7` | `24px` | `17px` | `16px` | `15px` | `15px / 1.75` | `13px` | `13px / 1.6` | `14px / 1.6` |
| `swiss-grid` | `15px` | `1.7` | `26px` | `20px` | `16px` | `15px` | `15px / 1.8` | `13px` | `13px / 1.6` | `14px / 1.6` |
| `purple-highlight` | `15px` | `1.6` | `24px` | `18px` | `16px` | `15px` | `15px / 1.75` | `13px` | `13px / 1.6` | `14px / 1.6` |
| `warm-nature` | `15px` | `1.7` | `26px` | `18px` | `17px` | `15px / 1.7` | `16px / 1.9` | `14px` | `13px / 1.6` | `14px / 1.6` |
| `vitality-orange` | `15px` | `1.75` | `26px` | `18px` | `17px` | `15px` | `16px / 1.85` | `14px` | `13px / 1.6` | `14px / 1.6` |
| `wechat-pure-glass` | `15px` | `1.7` | `26px` | `17px` | `17px` | `15px` | `16px / 1.8` | `14px` | `13px / 1.6` | `14px / 1.6` |
| `modern-cobalt` | `15px` | `1.75` | `26px` | `18px` | `17px` | `15px` | `16px / 1.8` | `14px` | `13px / 1.6` | `14px / 1.6` |
| `deep-space` | `15px` | `1.75` | `28px` | `20px` | `17px` | `15px / 1.7` | `16px / 1.9` | `14px` | `13px / 1.6` | `14px / 1.6` |

## Modern Style Rules

- Prefer a finished editorial article feel over plain document formatting.
- Use one accent color family plus neutral supporting surfaces for each preset.
- Add hierarchy through spacing, rules, surfaces, and heading treatments before adding more colors.
- For the default `warm-editorial` preset, prefer warm neutral backgrounds, clay accent labels, 12px monospace module labels, bold H2 typography, and lightweight copy-safe table diagrams when the source already contains diagram-like tabular content.
- For `warm-editorial`, use shallow semantic surfaces only when source content already calls for them: warning or risk notes may use `#f6e8e4` with `#7a2f29`; positive examples or rubric notes may use `#f1f5ec` with `#5f7748`.
- Keep long-read and information-dense presets left aligned for faster scanning. Center H1/H2 and their compact labels only in visual-led presets where headings are usually short: `purple-highlight`, `modern-cobalt`, and `deep-space`.
- Keep corners at `8px` or less unless the source theme already requires a softer article card.
- Keep decorative effects copy-paste friendly: use borders, backgrounds, padding, and inline text styling instead of external CSS or runtime effects.
- Avoid overusing large cards. Reserve card-like surfaces for summary, quote, comparison, or key insight sections.
- Avoid heavy gradients, floating decorative blobs, complex shadows, and browser-only layout tricks inside `article#wechatArticle`.

## Usage Rules

- If the user provides a preset id, use it directly.
- If the user provides a preset display name, map it to the matching preset id.
- If the user only asks for “换个配色” and does not specify one, use `warm-editorial` to match the current source fallback, or recommend another preset from this list when the task explicitly asks for suggestions.
- Keep the output self-contained and compatible with `article#wechatArticle`.
- Full preview HTML should expose every preset in this table through a theme switcher and initialize to `warm-editorial` unless a different valid preset is requested.
- Do not generate a preset by changing only the `article`, `h1`, `h2`, and `p` colors. The preset must also cover the component expectations above when those elements appear.
- Use the fixed color tokens and full palettes above as the source of truth for all preset colors.
- Use the fixed typography tokens and theme typography snapshot above as the source of truth for all preset font sizes and line heights.
