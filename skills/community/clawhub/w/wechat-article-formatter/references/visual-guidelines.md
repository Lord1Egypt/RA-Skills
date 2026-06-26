# Visual & Formatting Guidelines

## Visual Quality Contract

- The generated WeChat HTML is not strictly restricted in its visual design. You are free to use diverse formatting, color blocks, and creative layouts as long as they comply with WeChat's HTML rendering capabilities.
- The primary goal is to ensure the content displays normally and attractively on mobile screens. All layouts must be mobile-friendly and strictly avoid causing horizontal scrolling.
- Keep styles durable for WeChat copy-paste. The final copied body must materialize all required styling inline inside `article#wechatArticle`.
- Do not rely on external CSS, external fonts, SVG-only decoration, canvas, or JavaScript-dependent rendering, as these are not supported in the final WeChat article body.

## WeChat Formatting Rules

- Map the source into styled HTML elements. Do not modify the wording, split paragraphs, or add paragraphs. Ensure proper markup wrappers are used for layout representation.
- Keep the original paragraph structure intact. Do not arbitrarily split paragraphs or inject lists, quotes, or separators unless they are explicitly present in the source text.
- Apply visual polish only to source-backed elements. Do not force numbered sections, author blocks, ending cards, or media templates just to make the article look richer.
- Favor article-friendly structure over dashboard or app-like composition.
- Keep the content readable after copy-paste into the WeChat editor.
- Prefer simple, durable HTML structure such as headings, paragraphs, lists, blockquotes, tables, figures, and images. **Do not use `div` elements for content block structuring or text layout (such as moduleLabel, eyebrow labels, summary titles, or alert cards)**. The WeChat rich text editor often strips or flattens `div` elements, destroying their inline styling. Instead, use `<section>` for layout containers (like summaries, alerts, quotes, or cards) and `<p>` for paragraphs, subtitles, and labels.
- Avoid interaction patterns that only work in a browser, such as tabs, accordions, live previews, filters, or copy buttons, inside the final copy-ready body.
- Long inline code, URLs, and identifiers should be wrapped safely if they appear in preview HTML.
- Keep the chosen theme consistent across headings, quotes, code blocks, links, separators, and tables.
- Do not style article headings with full-width bottom underlines. In particular, avoid `border-bottom`, `text-decoration: underline`, and underline-like horizontal rules on `h1` or `h2`; use weight, color, spacing, or a short inline marker instead.
- For generated long-form articles, place a compact `moduleLabel` immediately above each major H2 section when the article has a clear section sequence. Use a stable pattern such as `01 / 问题入口`, `02 / 核心事实`, `03 / 关键判断`, with 12px monospace text and the theme accent color. Do not put the sequence number inside the H2.
- Shape major H2 headings as two-part editorial headings when wording can be edited: one part identifies the subject, the other part states the judgment, tension, or payoff. Examples: `它讲潮汕，但没有停在潮汕`; `真正的入口，是“我家里也有这样的人”`. Keep them natural in Chinese and avoid stiff translations such as `抓住两件事`.
- Style structurally important moments as richer article modules when they are present in the source, such as a lead summary, key insight block, table, figure, or closing takeaway, using the elements defined in references/theme-presets.md.
- Keep module styling consistent with the selected theme direction from `references/theme-presets.md`; do not mix unrelated palettes or visual languages in one article.

## Default Warm Editorial Style

- When no theme is requested, use `warm-editorial` to create a warm column-like reading experience.
- Use warm neutrals for the article base, a single clay accent for labels or emphasis, and low-contrast cream surfaces for callouts, tables, quotes, and summaries.
- Prefer scan rhythm over decoration: compact monospace labels above major H2 sections, strong two-part H2 typography, 12-16px paragraph gaps, and light borders are the default tools.
- For quote-like emphasis, prefer a soft surface, serif text, and relaxed line height over heavy side bars.
- For table-like diagrams that already exist in the source, make the table copy-safe, readable, and mobile-safe with visible cells, wrapped text, and restrained accent cells.
- Use shallow red or green surfaces only when the source already communicates a warning, risk, success, example, rubric, or positive note.
