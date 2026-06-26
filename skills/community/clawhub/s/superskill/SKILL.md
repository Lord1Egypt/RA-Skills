---
name: clawdbot-superskill
description: >-
  ClawdBot's complete production skill set. Contains three merged capabilities:
  (1) The FurrBudd WordPress article builder — full CSS theme, HTML component
  templates, SVG icon library, 7 WordPress compatibility rules, and pre-delivery
  checklist for generating affiliate product review articles on furrbudd.com.
  (2) Editorial affiliate UX strategy — competitive intelligence from The Spruce
  Pets, NYT Wirecutter, and Dog Food Advisor for content architecture and
  editorial decision-making. (3) AI Money Mastery website builder — complete
  React/Vite/Tailwind source code scaffold with luxury UI components for
  AI-monetization landing pages. ClawdBot should activate this skill when the
  user mentions FurrBudd, product reviews, WordPress articles, affiliate
  content, editorial strategy, AI Money Mastery, or React website builds.
---

# ClawdBot Super Skill

> ClawdBot's unified knowledge base. Three production systems in one file — from WordPress affiliate articles to editorial strategy to React website scaffolding.

---

# SKILL 1: FURRBUDD ARTICLE BUILDER

## Overview

ClawdBot generates self-contained HTML blocks (CSS + HTML, no JS frameworks) pasted into the WordPress **Code Editor** at [furrbudd.com](https://furrbudd.com). Each article is a single file: a `<link>` tag, one `<style>` block, and one `<div class="fb-article">` wrapper.

The WordPress theme at furrbudd.com aggressively overrides SVG sizes, backgrounds, fonts, and colors. Every compatibility rule below exists because of a real rendering failure on the live site. ClawdBot must follow them exactly.

---

### Part 1: WordPress Compatibility Rules

These are non-negotiable. Violating any will break rendering on the live site.

#### Rule 1: Font Loading — `<link>`, Never `@import`

WordPress strips `@import` inside `<style>` tags. The article must start with:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Oswald:wght@400;600;700&display=swap">
<style>
/* all CSS here */
</style>
<div class="fb-article">
  <!-- all HTML here -->
</div>
```

#### Rule 2: SVG Icons — Triple Protection Required

The WP theme applies `svg { width: 100% }` which blows icons to full container width. Every `<svg>` needs ALL THREE layers:

**Layer 1 — CSS reset with `!important` and WP wrapper selectors** (included in the stylesheet below).

**Layer 2 — HTML `width`/`height` attributes:**
```html
<svg class="ico" width="18" height="18" viewBox="0 0 24 24" ...>
```

**Layer 3 — Inline `style` with `!important`:**
```html
<svg class="ico" width="18" height="18"
  style="width:1.1em!important;height:1.1em!important;max-width:1.1em!important;max-height:1.1em!important;display:inline-block!important;vertical-align:-0.15em!important;overflow:visible!important"
  viewBox="0 0 24 24" ...>
```

All three layers must be present on every SVG. Never skip a layer.

#### Rule 3: Dark-Background Sections — Inline Styles with Hardcoded Colors

The WP theme overrides CSS `background` on divs. Any dark-background section (`.callout`, `.final-verdict`) MUST have:
- `background-color` and `background` set in an inline `style` attribute
- Hardcoded hex values (NOT CSS variables)
- `!important` on background properties
- Inline `style` with hardcoded `color` on EVERY child text element

#### Rule 4: Text Properties — Always `!important`

The WP theme overrides `font-size`, `line-height`, `color`, and `font-family`. Every text-bearing CSS rule needs `!important` on those four properties.

#### Rule 5: CSS Variables vs Hardcoded Values

- Use CSS variables in the stylesheet for general properties
- Use hardcoded hex for `background` on dark sections
- Use hardcoded hex for `color` on text inside dark sections
- Always define variables in the `.fb-article` root selector

#### Rule 6: Hyperlinks — Triple Protection (Same as SVGs)

The WP theme strips `text-decoration: underline` from links. Every `<a>` tag (except `.btn-primary` buttons) needs ALL THREE layers:

**Layer 1 — CSS reset with `!important` and WP wrapper selectors** (included in the stylesheet):
```css
.fb-article a,
.entry-content .fb-article a,
body .entry-content .fb-article a {
  color: #0f2b4a !important;
  text-decoration: underline !important;
  text-decoration-color: #d4a843 !important;
  text-underline-offset: 3px !important;
  text-decoration-thickness: 2px !important;
  text-decoration-style: solid !important;
}
```

**Layer 2 — Inline `style` on every body-text `<a>` tag:**
```html
<a href="AFFILIATE_LINK" target="_blank" rel="noopener nofollow sponsored"
  style="color:#0f2b4a!important;text-decoration:underline!important;text-decoration-color:#d4a843!important;text-underline-offset:3px!important;text-decoration-thickness:2px!important">
  link text
</a>
```

**Layer 3 — Dark-section links** get gold-light color instead:
```html
<a href="AFFILIATE_LINK" target="_blank" rel="noopener nofollow sponsored"
  style="color:#e8c46a!important;text-decoration:underline!important;text-decoration-color:#d4a843!important;text-underline-offset:3px!important;text-decoration-thickness:2px!important">
  link text
</a>
```

**Exception:** `.btn-primary` buttons get `text-decoration: none !important` — never underline CTA buttons.

#### Rule 7: Article Width — 1100px Centered

The WP theme's single-post container is set to 1100px. Every article's `.fb-article` root selector must include:

```css
.fb-article {
  max-width: 1100px;
  margin: 0 auto;
  /* ...rest of variables and properties... */
}
```

---

### Part 2: Complete CSS Stylesheet

ClawdBot must copy this entire `<style>` block into every new article. Only product-specific content changes between articles — the CSS stays identical.

```css
.fb-article {
  max-width: 1100px;
  margin: 0 auto;
  --fb-navy: #0f2b4a;
  --fb-navy-dark: #0a1e33;
  --fb-teal: #0d7377;
  --fb-gold: #d4a843;
  --fb-gold-light: #e8c46a;
  --fb-white: #ffffff;
  --fb-off-white: #f5f5f5;
  --fb-light-gray: #e8e8e8;
  --fb-mid-gray: #888888;
  --fb-dark-gray: #333333;
  --fb-text: #333333;
  --fb-text-light: #666666;
  --fb-shadow: 0 4px 15px rgba(0,0,0,0.1);
  --fb-shadow-lg: 0 8px 30px rgba(0,0,0,0.15);
  --fb-transition: all 0.3s ease;
  font-family: 'Open Sans', sans-serif;
  color: var(--fb-text);
  line-height: 1.6;
}

/* GLOBAL SVG RESET */
.fb-article svg,
.fb-article svg[viewBox],
.fb-article svg.ico,
.entry-content .fb-article svg,
.entry-content .fb-article svg.ico,
.entry-content .fb-article svg[viewBox],
.post-content .fb-article svg,
.wp-block-group .fb-article svg,
body .entry-content svg.ico,
body .entry-content svg[viewBox] {
  width: 1.1em !important;
  height: 1.1em !important;
  max-width: 1.1em !important;
  max-height: 1.1em !important;
  min-width: 0 !important;
  min-height: 0 !important;
  display: inline-block !important;
  vertical-align: -0.15em !important;
  overflow: visible !important;
  flex-shrink: 0 !important;
}
.fb-article .ico-check { color: var(--fb-teal) !important; }
.fb-article .ico-warn { color: #b07a2a !important; }
.fb-article .art-tag svg,
.fb-article .verdict-title svg { width: 1em !important; height: 1em !important; max-width: 1em !important; max-height: 1em !important; }
.fb-article .pc-item svg,
.fb-article .who-item svg { width: 1em !important; height: 1em !important; max-width: 1em !important; max-height: 1em !important; margin-top: 2px; }
.fb-article .faq-q svg { width: 1.2em !important; height: 1.2em !important; max-width: 1.2em !important; max-height: 1.2em !important; }

/* ROPE BORDER */
.fb-article .rope-border {
  width: 100%;
  height: 10px;
  background: linear-gradient(to right, #8B6914, #C4982B, #D4A843, #C4982B, #8B6914, #C4982B, #D4A843, #C4982B, #8B6914, #C4982B, #D4A843);
  background-size: 60px 10px;
  margin-bottom: 40px;
}

/* EYEBROW TAGS */
.fb-article .eyebrow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 32px;
}
.fb-article .art-tag {
  font-family: 'Oswald', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  padding: 5px 14px;
  border-radius: 4px;
}
.fb-article .tag-cat { background: var(--fb-teal); color: #fff; }
.fb-article .tag-pick { background: var(--fb-gold); color: var(--fb-navy); }
.fb-article .art-meta {
  color: var(--fb-mid-gray);
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 36px;
}

/* VERDICT BOX */
.fb-article .verdict-box {
  background: var(--fb-off-white);
  border: 2px solid var(--fb-light-gray);
  border-radius: 12px;
  padding: 30px;
  margin: 0 0 32px;
  box-shadow: var(--fb-shadow);
}
.fb-article .verdict-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--fb-navy);
  letter-spacing: 0.5px;
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid var(--fb-gold);
}
.fb-article .verdict-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 24px;
  margin-bottom: 20px;
}
.fb-article .verdict-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.9rem !important;
  line-height: 1.5 !important;
  color: var(--fb-text) !important;
  font-family: 'Open Sans', sans-serif !important;
  margin: 0;
}
.fb-article .verdict-rating {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 18px;
  border-top: 1px solid var(--fb-light-gray);
  flex-wrap: wrap;
}
.fb-article .stars { color: var(--fb-gold); font-size: 22px; letter-spacing: 2px; }
.fb-article .rating-num {
  font-family: 'Oswald', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--fb-navy);
}
.fb-article .rating-meta { font-size: 0.85rem !important; color: var(--fb-mid-gray) !important; font-family: 'Open Sans', sans-serif !important; }

/* CTA */
.fb-article .cta-wrap { text-align: center; margin: 32px 0; }
.fb-article .btn-primary {
  display: inline-block;
  background-color: var(--fb-gold);
  color: var(--fb-navy) !important;
  font-family: 'Oswald', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 14px 40px;
  border-radius: 30px;
  letter-spacing: 1px;
  transition: var(--fb-transition);
  box-shadow: 0 4px 15px rgba(212,168,67,0.4);
  text-decoration: none !important;
}
.fb-article .btn-primary:hover {
  background-color: var(--fb-gold-light);
  transform: translateY(-2px);
}
.fb-article .cta-note { font-size: 0.8rem !important; color: var(--fb-mid-gray) !important; margin: 8px 0 0; font-family: 'Open Sans', sans-serif !important; }

/* HEADINGS */
.fb-article h2 {
  font-family: 'Oswald', sans-serif !important;
  font-size: 1.7rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  color: var(--fb-navy) !important;
  letter-spacing: 0.5px;
  margin: 44px 0 16px !important;
  padding-bottom: 10px !important;
  border-bottom: 3px solid var(--fb-teal) !important;
  display: flex;
  align-items: center;
  gap: 10px;
}
.fb-article h2::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 26px;
  background: var(--fb-gold);
  border-radius: 3px;
  flex-shrink: 0;
}
.fb-article h3 {
  font-family: 'Oswald', sans-serif !important;
  font-size: 1.15rem !important;
  font-weight: 600 !important;
  color: var(--fb-navy) !important;
  margin: 28px 0 10px !important;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.fb-article p {
  font-size: 1rem !important;
  line-height: 1.8 !important;
  color: var(--fb-text) !important;
  margin-bottom: 18px !important;
  font-family: 'Open Sans', sans-serif !important;
}
.fb-article strong { font-weight: 600; color: var(--fb-navy); }

/* HYPERLINK STYLE — hardened for WP (Rule 6) */
.fb-article a,
.entry-content .fb-article a,
.post-content .fb-article a,
.wp-block-group .fb-article a,
body .entry-content .fb-article a {
  color: #0f2b4a !important;
  text-decoration: underline !important;
  text-decoration-color: #d4a843 !important;
  text-underline-offset: 3px !important;
  text-decoration-thickness: 2px !important;
  text-decoration-style: solid !important;
  transition: var(--fb-transition);
}
.fb-article a:hover,
.entry-content .fb-article a:hover,
body .entry-content .fb-article a:hover {
  color: #0d7377 !important;
  text-decoration-color: #e8c46a !important;
}
.fb-article .btn-primary,
.entry-content .fb-article .btn-primary,
body .entry-content .fb-article .btn-primary {
  text-decoration: none !important;
}

/* STAR RATING (CSS mask, not SVG) */
.fb-article .star-bar {
  display: inline-flex;
  gap: 2px;
}
.fb-article .star-icon {
  width: 22px;
  height: 22px;
  background: var(--fb-gold);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z'/%3E%3C/svg%3E") center/contain no-repeat;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z'/%3E%3C/svg%3E") center/contain no-repeat;
}
.fb-article .star-icon.empty { background: var(--fb-light-gray); }
.fb-article .star-icon.partial { background: linear-gradient(to right, var(--fb-gold) 60%, var(--fb-light-gray) 60%); }

/* ACCORDION FAQ */
.fb-article .faq-item { cursor: pointer; }
.fb-article .faq-q { display: flex; justify-content: space-between; align-items: center; }
.fb-article .faq-chevron {
  font-style: normal;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
  color: var(--fb-teal);
  flex-shrink: 0;
  margin-left: 12px;
}
.fb-article .faq-item.open .faq-chevron { transform: rotate(180deg); }
.fb-article .faq-a {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.35s ease, margin 0.35s ease;
  margin: 0;
}
.fb-article .faq-item.open .faq-a {
  max-height: 300px;
  margin-top: 10px;
}

/* STAT PILLS */
.fb-article .stat-row { display: flex; flex-wrap: wrap; gap: 12px; margin: 24px 0; }
.fb-article .stat-pill {
  background: var(--fb-white);
  border: 2px solid var(--fb-light-gray);
  border-radius: 12px;
  padding: 14px 20px;
  text-align: center;
  min-width: 100px;
  transition: var(--fb-transition);
}
.fb-article .stat-pill:hover { border-color: var(--fb-teal); box-shadow: var(--fb-shadow); }
.fb-article .stat-num {
  font-family: 'Oswald', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--fb-teal);
  display: block;
  line-height: 1;
  margin-bottom: 4px;
}
.fb-article .stat-lbl {
  font-family: 'Oswald', sans-serif;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--fb-mid-gray);
}

/* INGREDIENT BOX */
.fb-article .ingredient-box {
  background: #f0f9f9;
  border: 2px solid rgba(13,115,119,0.2);
  border-left: 5px solid var(--fb-teal);
  border-radius: 8px;
  padding: 20px 24px;
  margin: 20px 0;
  font-size: 0.95rem;
  line-height: 2;
  color: var(--fb-dark-gray);
}
.fb-article .ingredient-box strong { color: var(--fb-teal); font-weight: 700; }

/* PROS / CONS */
.fb-article .pc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 28px 0; }
.fb-article .pc-box { border-radius: 12px; padding: 22px 24px; box-shadow: var(--fb-shadow); }
.fb-article .pc-box.pros { background: #f0f9f4; border: 2px solid #a8d5b5; }
.fb-article .pc-box.cons { background: #fff8f0; border: 2px solid #f0d5a8; }
.fb-article .pc-label {
  font-family: 'Oswald', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid currentColor;
}
.fb-article .pc-box.pros .pc-label { color: var(--fb-teal); }
.fb-article .pc-box.cons .pc-label { color: #b07a2a; }
.fb-article .pc-item { font-size: 0.88rem !important; line-height: 1.5 !important; margin-bottom: 9px; display: flex; gap: 8px; align-items: flex-start; color: var(--fb-text) !important; font-family: 'Open Sans', sans-serif !important; }

/* CALLOUT (dark background — needs inline style too) */
.fb-article .callout {
  background-color: #0f2b4a !important;
  background: linear-gradient(135deg, #0a1e33 0%, #0f2b4a 100%) !important;
  border-radius: 12px !important;
  padding: 28px 32px !important;
  margin: 32px 0;
  position: relative;
  overflow: hidden;
}
.fb-article .callout::before {
  content: '\201C';
  position: absolute;
  top: -10px; left: 16px;
  font-family: 'Oswald', sans-serif;
  font-size: 8rem;
  color: rgba(212,168,67,0.15);
  line-height: 1;
}
.fb-article .callout p {
  color: rgba(255,255,255,0.9) !important;
  font-size: 1.05rem;
  font-style: italic;
  line-height: 1.7;
  margin-bottom: 0 !important;
  position: relative;
  z-index: 1;
}
.fb-article .callout cite {
  display: block;
  margin-top: 10px;
  color: #d4a843 !important;
  font-family: 'Oswald', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-style: normal;
  position: relative;
  z-index: 1;
}

/* WHO BOXES */
.fb-article .who-box { border-radius: 12px; padding: 24px 26px; margin: 16px 0; box-shadow: var(--fb-shadow); }
.fb-article .who-box.good { background: #f0f9f4; border: 2px solid #a8d5b5; }
.fb-article .who-box.skip { background: #fff8f0; border: 2px solid #f0d5a8; }
.fb-article .who-box h3 { margin: 0 0 14px !important; font-size: 1rem !important; text-transform: uppercase; }
.fb-article .who-box.good h3 { color: var(--fb-teal) !important; }
.fb-article .who-box.skip h3 { color: #b07a2a !important; }
.fb-article .who-item { font-size: 0.9rem !important; margin-bottom: 9px; display: flex; gap: 10px; align-items: flex-start; line-height: 1.5 !important; color: var(--fb-text) !important; font-family: 'Open Sans', sans-serif !important; }

/* PRICE TABLE */
.fb-article .price-table { width: 100%; border-collapse: collapse; margin: 20px 0; border-radius: 12px; overflow: hidden; box-shadow: var(--fb-shadow); font-size: 0.95rem; }
.fb-article .price-table th { background: var(--fb-navy); color: var(--fb-white); text-align: left; padding: 12px 16px; font-family: 'Oswald', sans-serif; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }
.fb-article .price-table td { padding: 12px 16px; border-bottom: 1px solid var(--fb-light-gray); font-family: 'Open Sans', sans-serif !important; color: var(--fb-text) !important; font-size: 0.95rem !important; }
.fb-article .price-table tr:nth-child(even) td { background: var(--fb-off-white); }
.fb-article .price-table .best-row td { font-weight: 700; color: var(--fb-teal); background: #e8f5f5; }

/* FAQ */
.fb-article .faq-item { border: 2px solid var(--fb-light-gray); border-radius: 8px; padding: 20px 24px; margin-bottom: 12px; transition: var(--fb-transition); }
.fb-article .faq-item:hover { border-color: var(--fb-teal); box-shadow: var(--fb-shadow); }
.fb-article .faq-q { font-family: 'Oswald', sans-serif; font-size: 1rem; font-weight: 700; color: var(--fb-navy); text-transform: uppercase; letter-spacing: 0.3px; margin: 0 0 10px; }
.fb-article .faq-a { font-size: 0.92rem !important; color: var(--fb-text-light) !important; line-height: 1.75 !important; margin: 0; font-family: 'Open Sans', sans-serif !important; }

/* FINAL VERDICT (dark background — needs inline style too) */
.fb-article .final-verdict {
  background-color: #0f2b4a !important;
  background: linear-gradient(135deg, #0a1e33 0%, #0f2b4a 50%, #1a3d5c 100%) !important;
  border-radius: 12px !important;
  padding: 36px 38px !important;
  margin-top: 48px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15) !important;
}
.fb-article .fv-header { display: flex; align-items: center; gap: 24px; margin-bottom: 20px; flex-wrap: wrap; }
.fb-article .fv-score { font-family: 'Oswald', sans-serif; font-size: 4rem; font-weight: 700; color: #d4a843 !important; line-height: 1; }
.fb-article .fv-score-max { font-size: 1.5rem !important; color: rgba(255,255,255,0.35) !important; }
.fb-article .fv-label { font-family: 'Oswald', sans-serif; font-size: 0.72rem !important; color: rgba(255,255,255,0.45) !important; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }
.fb-article .fv-title h2 {
  color: #fff !important;
  font-size: 1.6rem !important;
  margin: 0 0 4px !important;
  padding: 0 !important;
  border: none !important;
}
.fb-article .fv-title h2::before { display: none !important; }
.fb-article .fv-title p { color: #e8c46a !important; font-size: 0.85rem !important; font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 !important; }
.fb-article .fv-divider { border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 20px 0; }
.fb-article .body-text { color: rgba(255,255,255,0.8) !important; font-size: 0.95rem !important; line-height: 1.8 !important; margin-bottom: 14px !important; font-family: 'Open Sans', sans-serif !important; }

/* DIVIDER */
.fb-article .divider { border: none; border-top: 1px solid var(--fb-light-gray); margin: 40px 0; }

/* AFFILIATE NOTE */
.fb-article .affiliate-note {
  background: var(--fb-off-white);
  border: 1px solid var(--fb-light-gray);
  border-radius: 8px;
  padding: 16px 20px;
  font-size: 0.82rem;
  color: var(--fb-mid-gray);
  line-height: 1.6;
  margin-top: 48px;
  font-style: italic;
}

/* RESPONSIVE */
@media (max-width: 640px) {
  .fb-article .verdict-grid { grid-template-columns: 1fr; }
  .fb-article .pc-grid { grid-template-columns: 1fr; }
  .fb-article h2 { font-size: 1.3rem !important; }
}
```

---

### Part 3: SVG Icon Library

Every SVG must include `class="ico" width="18" height="18"` plus the full inline `style` string. The inline style is abbreviated as `ICO_STYLE` — ClawdBot must always expand it to:

```
style="width:1.1em!important;height:1.1em!important;max-width:1.1em!important;max-height:1.1em!important;display:inline-block!important;vertical-align:-0.15em!important;overflow:visible!important"
```

#### Checkmark (teal, for pros/positives)
```html
<svg class="ico ico-check" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
```

#### Warning triangle (amber, for cons/cautions)
```html
<svg class="ico ico-warn" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#b07a2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
```

#### Paw print (filled, for who-box items)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><ellipse cx="8" cy="7" rx="2.5" ry="3"/><ellipse cx="16" cy="7" rx="2.5" ry="3"/><ellipse cx="4.5" cy="13" rx="2" ry="2.5"/><ellipse cx="19.5" cy="13" rx="2" ry="2.5"/><path d="M12 20c-3 0-5-2-6-4s0-4 2-4.5c1.5-.4 2.5.5 4 .5s2.5-.9 4-.5c2 .5 3 2.5 2 4.5s-3 4-6 4z"/></svg>
```

#### Paw outline (for category tag, puppy FAQ)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5.172C10 3.782 8.423 2.679 6.5 3c-2.823.47-4.113 6.006-4 7 .137 1.217 1.5 2 2.5 2s2-.5 3-1.5c.5-.5 1-1 1.5-1s1 .5 1.5 1c1 1 2 1.5 3 1.5s2.363-.783 2.5-2c.113-.994-1.177-6.53-4-7C10.577 2.679 10 3.782 10 5.172z"/><path d="M12 17c-2 0-4-1-4-3s2-4 4-4 4 2 4 4-2 3-4 3z"/><circle cx="8.5" cy="12.5" r=".5" fill="currentColor"/><circle cx="15.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 17v4"/></svg>
```

#### Star (filled, for badge tag)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
```

#### Lightning bolt (for quick verdict title)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
```

#### Calendar (for date in meta)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
```

#### Pen (for author in meta)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
```

#### Clock (for read time in meta)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2"/><path d="M10 2h4"/></svg>
```

#### Leaf (for natural/organic pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21c3-6 10-9 16-10C20 5 14 3 8 5c-4 1.33-5 5-4 8l-1 8"/><path d="M8 13c3-2 7-3 11-3"/></svg>
```

#### Crosshair/target (for probiotic/science pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1" fill="currentColor"/><line x1="12" y1="2" x2="12" y2="7"/><line x1="12" y1="17" x2="12" y2="22"/><line x1="2" y1="12" x2="7" y2="12"/><line x1="17" y1="12" x2="22" y2="12"/></svg>
```

#### Trend down (for weight/glycemic pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>
```

#### Flag (for sourcing pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
```

#### Flask/beaker (for no-recall pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 100-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 01-2-2V6h6v4a2 2 0 01-2 2z"/><path d="M12 6V3a1 1 0 00-1-1H9a1 1 0 00-1 1v3"/></svg>
```

#### Sparkle (for coat/results pros)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.5 5.5L19 9l-5.5 1.5L12 16l-1.5-5.5L5 9l5.5-1.5L12 2z"/><path d="M19 14l1 3 3 1-3 1-1 3-1-3-3-1 3-1 1-3z" opacity=".6"/></svg>
```

#### Dollar sign (for price cons)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#b07a2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
```

#### Plant/wheat (for grain cons)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22l10-10"/><path d="M16 8l-4 4"/><path d="M12 12c1-2 3-4 6-4 0 3-2 5-4 6"/><path d="M8 16c1-2 3-4 6-4 0 3-2 5-4 6"/><path d="M16 4c1-2 3-2 5 0 0 3-2 4-4 4"/><path d="M12 8c1-2 3-2 5 0 0 3-2 4-4 4"/></svg>
```

#### Bar chart (for carb cons)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
```

#### Refresh/cycle (for transition cons)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>
```

#### Shopping cart (for availability cons)
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
```

#### Chevron down (for FAQ accordion)
Use the text character `▼` inside `<i class="faq-chevron">▼</i>` (not an SVG).

---

### Part 4: HTML Component Templates

ClawdBot uses the exact HTML below for each component section. Replace bracketed `[PLACEHOLDER]` values with product-specific content. `AFFILIATE_URL` is the single affiliate link the user provides per article.

#### 4.1 Rope Border
```html
<div class="rope-border"></div>
```

#### 4.2 Eyebrow Tags
```html
<div class="eyebrow">
  <span class="art-tag tag-cat">[PAWN_OUTLINE_SVG] [Category Name] Reviews</span>
  <span class="art-tag tag-pick">[STAR_SVG] [Badge Text, e.g. "Amazon Overall Pick"]</span>
</div>
```

#### 4.3 Article Meta
```html
<div class="art-meta">
  <span>[CALENDAR_SVG] [Month Year]</span>
  <span>·</span>
  <span>[PEN_SVG] FurrBudd Editorial Team</span>
  <span>·</span>
  <span>[CLOCK_SVG] [X] min read</span>
</div>
```

#### 4.4 Quick Verdict Box
```html
<div class="verdict-box">
  <div class="verdict-title">[LIGHTNING_SVG] Quick Verdict</div>
  <div class="verdict-grid">
    <div class="verdict-item"><span>[CHECKMARK_SVG]</span><span>[Pro point]</span></div>
    <div class="verdict-item"><span>[CHECKMARK_SVG]</span><span>[Pro point]</span></div>
    <div class="verdict-item"><span>[WARNING_SVG]</span><span>[Con point]</span></div>
    <div class="verdict-item"><span>[WARNING_SVG]</span><span>[Con point]</span></div>
  </div>
  <div class="verdict-rating">
    <span class="star-bar" role="img" aria-label="[X] out of 5 stars">
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon partial"></span>
    </span>
    <span class="rating-num">[X.X]</span>
    <span class="rating-meta">out of 5 &nbsp;·&nbsp; [N] Amazon reviews &nbsp;·&nbsp; [N]+ sold last month</span>
  </div>
</div>
```

#### 4.5 Primary CTA
```html
<div class="cta-wrap">
  <a class="btn-primary" href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">Check Price on Amazon →</a>
  <p class="cta-note">[Available sizes / shipping info]</p>
</div>
```

#### 4.6 Divider
```html
<hr class="divider" />
```

#### 4.7 Body Sections
```html
<h2>[Section Title]</h2>
<p>[Body paragraph with <a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored"><strong>anchor text</strong></a> links woven in naturally.]</p>
<h3>[Subheading]</h3>
<p>[Sub-section paragraph.]</p>
```

#### 4.8 Ingredient Box (optional, for food products)
```html
<div class="ingredient-box">
  <strong>[Key Ingredient 1]</strong> · <strong>[Key Ingredient 2]</strong> · Regular Ingredient · <strong>[Key Ingredient 3]</strong> · Regular Ingredient
</div>
```

#### 4.9 Callout Quote (DARK BACKGROUND — inline styles mandatory)
```html
<div class="callout" style="background-color:#0f2b4a!important;background:linear-gradient(135deg,#0a1e33 0%,#0f2b4a 100%)!important;border-radius:12px!important;padding:28px 32px!important;position:relative;overflow:hidden">
  <p style="color:rgba(255,255,255,0.9)!important;font-style:italic!important;line-height:1.7!important;position:relative;z-index:1">[Quote text]</p>
  <cite style="color:#d4a843!important;display:block!important;position:relative;z-index:1">— [Attribution]</cite>
</div>
```

#### 4.10 Stat Pills
```html
<div class="stat-row">
  <div class="stat-pill"><span class="stat-num">[Value]</span><span class="stat-lbl">[Label]</span></div>
  <div class="stat-pill"><span class="stat-num">[Value]</span><span class="stat-lbl">[Label]</span></div>
</div>
```

#### 4.11 Pros & Cons Grid
```html
<div class="pc-grid">
  <div class="pc-box pros">
    <div class="pc-label">[CHECKMARK_SVG] What We Love</div>
    <div class="pc-item"><span>[THEMED_ICON_SVG]</span><span>[Pro point]</span></div>
  </div>
  <div class="pc-box cons">
    <div class="pc-label">[WARNING_SVG] Worth Knowing</div>
    <div class="pc-item"><span>[THEMED_ICON_SVG]</span><span>[Con point]</span></div>
  </div>
</div>
```

#### 4.12 Price Table
```html
<table class="price-table">
  <tr><th>Size</th><th>Amazon Price</th><th>Cost Per [Unit]</th></tr>
  <tr><td>[Size]</td><td>$[Price]</td><td>$[X] / [unit]</td></tr>
  <tr class="best-row"><td><a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored"><strong>[Size] ← Best Value — Buy Now</strong></a></td><td><strong>$[Price]</strong></td><td><strong>$[X] / [unit]</strong></td></tr>
</table>
```

#### 4.13 Who-Is-It-For Boxes
```html
<div class="who-box good">
  <h3>[CHECKMARK_SVG] Great Fit If Your Dog…</h3>
  <div class="who-item"><span>[PAWN_FILLED_SVG]</span><span>[Good-fit scenario]</span></div>
</div>
<div class="who-box skip">
  <h3>[WARNING_SVG] Less Ideal If Your Dog…</h3>
  <div class="who-item"><span>[WARNING_SVG]</span><span>[Less-ideal scenario]</span></div>
</div>
```

#### 4.14 FAQ Accordion
```html
<div class="faq-item" onclick="this.classList.toggle('open')">
  <div class="faq-q"><span>[THEMED_ICON_SVG] [Question text]</span><i class="faq-chevron">▼</i></div>
  <p class="faq-a">[Answer text]</p>
</div>
```

#### 4.15 Final Verdict (DARK BACKGROUND — inline styles mandatory)
```html
<div class="final-verdict" style="background-color:#0f2b4a!important;background:linear-gradient(135deg,#0a1e33 0%,#0f2b4a 50%,#1a3d5c 100%)!important;border-radius:12px!important;padding:36px 38px!important">
  <div class="fv-header">
    <div>
      <div class="fv-score" style="color:#d4a843!important;font-family:'Oswald',sans-serif!important;font-size:4rem!important;font-weight:700!important">[X.X]<span class="fv-score-max" style="color:rgba(255,255,255,0.35)!important;font-size:1.5rem!important">/10</span></div>
      <div class="fv-label" style="color:rgba(255,255,255,0.45)!important;font-family:'Oswald',sans-serif!important;font-size:0.72rem!important">FurrBudd Rating</div>
    </div>
    <div class="fv-title">
      <h2 style="color:#ffffff!important;font-size:1.6rem!important;margin:0 0 4px!important;padding:0!important;border:none!important">Final Verdict</h2>
      <p style="color:#e8c46a!important;font-size:0.85rem!important;font-family:'Oswald',sans-serif!important;text-transform:uppercase!important;margin:0!important">Editor's Choice — [Product Category]</p>
    </div>
  </div>
  <hr class="fv-divider" style="border:none!important;border-top:1px solid rgba(255,255,255,0.15)!important;margin:20px 0!important" />
  <p class="body-text" style="color:rgba(255,255,255,0.8)!important;font-size:0.95rem!important;line-height:1.8!important;font-family:'Open Sans',sans-serif!important">[Verdict paragraph with <a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored" style="color: var(--fb-gold-light);">affiliate link</a>.]</p>
  <div class="cta-wrap" style="text-align:left; margin-bottom:0;">
    <a class="btn-primary" href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">Shop [Product] on Amazon →</a>
  </div>
</div>
```

#### 4.16 Affiliate Disclosure
```html
<div class="affiliate-note">
  <strong>Disclosure:</strong> FurrBudd participates in the Amazon Services LLC Associates Program. If you purchase through our links, we may earn a small commission at no extra cost to you. This does not influence our editorial opinions or recommendations. Thank you for supporting FurrBudd!
</div>
```

---

### Part 5: Affiliate Links

The user provides one affiliate URL per article. ClawdBot must place it on:
- Every CTA button (`<a class="btn-primary" href="AFFILIATE_URL" ...>`)
- Contextual text links in body paragraphs (on product names, key phrases)
- Price table "Best Value" row
- Final Verdict CTA and body links

Every affiliate link must include:
```html
<a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">
```

Links inside `.final-verdict` dark sections also need `style="color: var(--fb-gold-light);"`.

---

### Part 6: Article Section Order

ClawdBot must follow this exact order inside `<div class="fb-article">`:

| # | Section | Class | Dark BG? |
|---|---------|-------|----------|
| 1 | Rope border | `.rope-border` | No |
| 2 | Eyebrow tags | `.eyebrow` > `.art-tag` | No |
| 3 | Article meta | `.art-meta` | No |
| 4 | Quick Verdict | `.verdict-box` | No |
| 5 | Primary CTA | `.cta-wrap` > `.btn-primary` | No |
| 6 | Divider | `.divider` | No |
| 7 | Body sections | `h2` + `p` + `h3` | No |
| 8 | Callout quote | `.callout` | **YES — inline style** |
| 9 | More body | `h2` + `p` | No |
| 10 | Stat pills | `.stat-row` > `.stat-pill` | No |
| 11 | Pros & Cons | `.pc-grid` | No |
| 12 | Price table | `.price-table` | No |
| 13 | Who-is-it-for | `.who-box` | No |
| 14 | Reviews + callout | `h2` + `.callout` | **Callout = YES** |
| 15 | FAQ accordion | `.faq-item` | No |
| 16 | Final Verdict | `.final-verdict` | **YES — inline style** |
| 17 | Disclosure | `.affiliate-note` | No |

---

### Part 7: Color Palette & Typography

#### Colors

| Variable | Hex | Usage |
|----------|-----|-------|
| `--fb-navy` | `#0f2b4a` | Headings, strong text, dark backgrounds |
| `--fb-navy-dark` | `#0a1e33` | Gradient start on dark sections |
| `--fb-teal` | `#0d7377` | Check icons, h2 borders, accents |
| `--fb-gold` | `#d4a843` | CTA buttons, stars, decorative borders, citations |
| `--fb-gold-light` | `#e8c46a` | Hover states, subtitle text in dark sections |
| `--fb-text` | `#333333` | Body text |
| `--fb-text-light` | `#666666` | FAQ answers, secondary text |
| `--fb-mid-gray` | `#888888` | Meta text, captions |
| `--fb-off-white` | `#f5f5f5` | Light box backgrounds |
| `--fb-light-gray` | `#e8e8e8` | Borders, dividers |

#### Typography

| Element | Font | Weight | Size | Case |
|---------|------|--------|------|------|
| h2 headings | Oswald | 700 | 1.7rem | Uppercase |
| h3 subheadings | Oswald | 600 | 1.15rem | Uppercase |
| Body paragraphs | Open Sans | 400 | 1rem | Normal |
| Eyebrow tags | Oswald | 700 | 0.72rem | Uppercase |
| CTA buttons | Oswald | 700 | 1rem | Uppercase |
| Stat numbers | Oswald | 700 | 1.6rem | Normal |
| Stat labels | Oswald | — | 0.68rem | Uppercase |

---

### Part 8: FurrBudd Pre-Delivery Checklist

Before ClawdBot delivers any new article, verify every item:

- [ ] File starts with `<link rel="stylesheet">` for Google Fonts (NOT `@import`)
- [ ] All CSS inside a single `<style>` block between `<link>` and `<div class="fb-article">`
- [ ] CSS is identical to the stylesheet in Part 2
- [ ] Every `<svg>` has all three protections: CSS reset, `width="18" height="18"` attrs, inline `style` with `!important`
- [ ] All text CSS rules use `!important` on font-size, line-height, color, font-family
- [ ] Both `.callout` divs have inline `style` with hardcoded hex background
- [ ] `.final-verdict` div has inline `style` with hardcoded hex background
- [ ] Every text element inside dark sections has inline `style` with hardcoded `color`
- [ ] All affiliate links use `target="_blank" rel="noopener nofollow sponsored"`
- [ ] Affiliate disclosure present at bottom
- [ ] FAQ items use `onclick="this.classList.toggle('open')"`
- [ ] Star rating uses CSS `mask` on `<span class="star-icon">` (NOT SVG)
- [ ] `@media (max-width: 640px)` collapses verdict-grid and pc-grid to 1 column
- [ ] Article section order matches Part 6 exactly
- [ ] User's affiliate URL is placed on all CTA buttons, text links, price table, and final verdict

---

# SKILL 2: EDITORIAL AFFILIATE UX STRATEGY

Competitive intelligence for ClawdBot to apply when planning site architecture, writing article content, and making editorial decisions for FurrBudd.

---

### Part 9: Competitive Landscape

#### Sites Analyzed

1. **The Spruce Pets** (thesprucepets.com) — Magazine-style editorial
2. **NYT Wirecutter — Pets** (nytimes.com/wirecutter/pets/) — Newspaper-style testing authority
3. **Dog Food Advisor** (dogfoodadvisor.com) — Expert blog / resource hub

#### The Core Pattern

All three follow the same conversion funnel:

```
Trust → Education → Recommendation → Affiliate Click
```

Never:

```
Product → Price → Buy
```

The product is never the hero — **the expert opinion is**. Products appear only within the context of editorial judgment, testing methodology, and expert verification. ClawdBot must always frame FurrBudd content this way.

---

### Part 10: Homepage & Navigation Principles

#### Homepage Must-Haves

1. **Lead with editorial, not product listings** — zero commerce above the fold
2. **Quantified credibility banner** — "X Products Reviewed" model builds instant trust
3. **Expert team section on homepage** — named credentials
4. **Methodology preview** — brief "how we evaluate" before deep-dive page
5. **Recall/safety utility content** — recall alerts drive email signup and position the brand as protective

#### Navigation Architecture

- **Pet-type first** (Dogs, Cats, etc.), NOT product-category first
- Deep taxonomies: by breed, by condition, by life stage, by ingredient
- "Best [Product]" lists as primary navigation targets
- Recalls/safety as a first-class nav item

---

### Part 11: Review Article Content Strategy

#### Article Title Patterns (Proven Formats)

- "The [N] Best [Product], Tested and Reviewed"
- "The [N] Best [Product] of [Year]"
- "[Product Name] Review [Year]: Is It Worth It?"
- "Best [Product] for [Specific Need] — Expert Picks"

#### Article Structure (Editorial Best Practices)

Every review ClawdBot generates should include:

1. **"Top Picks" summary at top** — scannable before the deep dive
2. **Category labels** — "Best Overall", "Best Budget", "Best for [Specific Need]"
3. **Pros/Cons structure** — every product must have documented negatives
4. **Testing methodology section** — "How We Evaluated" builds legitimacy
5. **Author + expert attribution** — byline with credentials
6. **Spec tables** — structured product data for comparison
7. **"Why Trust Us" section** — methodology summary
8. **"Who This Is For" framing** — frame the reader's need before selling

#### Content Differentiators That Build Trust

| Element | How ClawdBot Implements |
|---------|------------------------|
| Honest negatives | Always include 3+ genuine cons per product. Use "Worth Knowing" framing. |
| Testing provenance | State how the product was evaluated. If label-based, acknowledge it honestly. |
| Expert attribution | Use "FurrBudd Editorial Team" byline; add veterinary review when available. |
| Independence declaration | Affiliate disclosure on every article. State "we are not paid by brands." |
| Freshness signals | Include publish/update dates. Monthly date stamps on "Best Of" lists. |

---

### Part 12: CTA Language Rules

#### Words ClawdBot Must NEVER Use
- "Buy Now"
- "Add to Cart"
- "Shop" (except in Final Verdict CTA: "Shop [Product] on Amazon")
- "Purchase"

#### Approved CTA Phrases

| Phrase | Context |
|--------|---------|
| "Check Price on Amazon" | Primary CTA button |
| "View on Amazon" | Secondary/inline links |
| "$[Price] at Amazon" | Price-anchored links |
| "[Size] — Best Value" | Price table highlight row |
| "Shop [Product] on Amazon" | Final Verdict CTA only |

---

### Part 13: Affiliate Link Handling

#### Link Placement Rules (ClawdBot must follow)

1. Primary CTA button (after verdict box)
2. 2-3 contextual text links in body paragraphs (on product name, key benefit phrases)
3. Price table "Best Value" row
4. Final Verdict CTA and body links
5. Never more than one CTA button visible without substantial content between them

---

### Part 14: Trust Signal Priority

Ranked by impact — ClawdBot should maintain active signals and plan for roadmap items:

| Priority | Signal | Status |
|----------|--------|--------|
| 1 | Affiliate disclosure on every article | **Active** |
| 2 | Honest negatives (Pros/Cons) for every product | **Active** |
| 3 | Author bylines with "FurrBudd Editorial Team" | **Active** |
| 4 | Publish/update dates on every article | **Active** |
| 5 | Transparent rating methodology page | Roadmap |
| 6 | Named expert review board with credentials | Roadmap |
| 7 | "How We Evaluated" section in every review | Roadmap |
| 8 | Monthly date stamps on "Best Of" lists | Roadmap |
| 9 | User review/community features | Future |
| 10 | Academic/scientific source citations | Future |

---

### Part 15: Brand Voice Guidelines

ClawdBot must write FurrBudd content with these rules:

- Write in third-person editorial ("FurrBudd recommends...") or inclusive first-person plural ("we found...")
- Never use aggressive sales language
- Acknowledge limitations and trade-offs honestly
- Frame recommendations around the dog's needs, not the product's features
- Use data points and specifics over vague praise
- Make the site feel like a magazine, not a storefront

---

### Part 16: SEO Content Guidelines

#### Target Word Count

- Single product reviews: 1,500+ words
- "Best Of" roundup lists: 2,500+ words
- Informational/educational posts: 1,000+ words

#### Keyword Placement

- Primary keyword in H1 title
- Primary keyword in first 100 words
- Secondary keywords in H2 and H3 headings
- Natural keyword density throughout body
- Primary keyword in meta description and URL slug

#### Internal Linking Strategy

- Every article links to 2-3 related FurrBudd articles
- "Best Of" lists link to individual product reviews
- Individual reviews link back to relevant "Best Of" lists

---

### Part 17: Editorial Pre-Delivery Checklist

ClawdBot verifies these alongside the technical checklist (Part 8):

- [ ] Article is 1,500+ words for single product reviews
- [ ] Title follows proven format patterns (Part 11)
- [ ] At least 3 genuine cons listed — no "puff piece" reviews
- [ ] CTA language uses only approved phrases (Part 12)
- [ ] Affiliate links placed in all 4 required positions (Part 13)
- [ ] Author byline and date present
- [ ] Content reads as editorial recommendation, not sales copy
- [ ] No "Buy Now", "Add to Cart", or "Shop" language (except Final Verdict CTA)
- [ ] Product evaluated from the dog's perspective, not just features
- [ ] Primary keyword in title, first 100 words, and at least 2 H2s
- [ ] FAQ section includes 5+ questions with natural keyword usage

---

# SKILL 3: AI MONEY MASTERY WEBSITE BUILDER

Originally created by Manus AI. ClawdBot uses this scaffold when the user requests AI-monetization landing pages or React website builds.

**Live reference:** https://bcdluqyt.manussite.space

---

### Part 18: Project Setup

```bash
npx create-react-app ai-money-website
cd ai-money-website

npm install @radix-ui/react-slot @radix-ui/react-separator lucide-react class-variance-authority clsx tailwind-merge framer-motion
npm install -D tailwindcss @tailwindcss/vite tw-animate-css
```

---

### Part 19: File Structure

```
ai-money-website/
├── public/
├── src/
│   ├── assets/          # Images
│   ├── components/
│   │   └── ui/         # UI components
│   ├── App.jsx         # Main application
│   ├── App.css         # Luxury styling
│   ├── index.css       # Global styles
│   └── main.jsx        # Entry point
├── index.html          # SEO-optimized HTML
├── package.json        # Dependencies
└── vite.config.js      # Vite configuration
```

---

### Part 20: index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Money Mastery - 25+ Proven Ways to Make Money Online with Artificial Intelligence</title>
    <meta name="description" content="Discover 25+ proven strategies to make money online with AI. From AI content creation to automated businesses, learn how to generate income using artificial intelligence tools and technologies." />
    <meta name="keywords" content="make money with AI, artificial intelligence business, AI monetization, online income AI, AI side hustle, generative AI profit, AI automation business, machine learning income" />
    <meta name="author" content="AI Money Mastery" />
    <meta name="robots" content="index, follow" />
    <meta property="og:title" content="AI Money Mastery - 25+ Proven Ways to Make Money Online with AI" />
    <meta property="og:description" content="Discover proven strategies to generate income using artificial intelligence. Learn from industry experts and start your AI-powered business today." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://ai-money-mastery.com" />
    <meta property="og:image" content="/src/assets/ai_business_hero.webp" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="AI Money Mastery - Make Money Online with AI" />
    <meta name="twitter:description" content="25+ proven ways to generate income using artificial intelligence" />
    <meta name="twitter:image" content="/src/assets/ai_business_hero.webp" />
    <link rel="canonical" href="https://ai-money-mastery.com" />
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "AI Money Mastery",
      "description": "Learn proven strategies to make money online with artificial intelligence",
      "url": "https://ai-money-mastery.com",
      "author": { "@type": "Organization", "name": "AI Money Mastery" },
      "publisher": { "@type": "Organization", "name": "AI Money Mastery" }
    }
    </script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

### Part 21: Core Configuration Files

#### package.json

```json
{
  "name": "ai-money-website",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "@radix-ui/react-slot": "^1.2.2",
    "@radix-ui/react-separator": "^1.1.6",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "framer-motion": "^12.15.0",
    "lucide-react": "^0.510.0",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "tailwind-merge": "^3.3.0",
    "tailwindcss": "^4.1.7"
  },
  "devDependencies": {
    "@eslint/js": "^9.25.0",
    "@types/react": "^19.1.2",
    "@types/react-dom": "^19.1.2",
    "@vitejs/plugin-react": "^4.4.1",
    "@tailwindcss/vite": "^4.1.7",
    "eslint": "^9.25.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.19",
    "globals": "^16.0.0",
    "tw-animate-css": "^1.2.9",
    "vite": "^6.3.5"
  }
}
```

#### vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

#### src/main.jsx

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

---

### Part 22: Global Styles (src/index.css)

```css
@import "tailwindcss";
@import "tw-animate-css";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --card: 0 0% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 0 0% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

### Part 23: UI Components

#### src/lib/utils.js

```javascript
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
```

#### src/components/ui/button.jsx

```jsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
})
Button.displayName = "Button"

export { Button, buttonVariants }
```

#### src/components/ui/card.jsx

```jsx
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-xl border bg-card text-card-foreground shadow", className)} {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

#### src/components/ui/badge.jsx

```jsx
import * as React from "react"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive: "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({ className, variant, ...props }) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
```

#### src/components/ui/separator.jsx

```jsx
import * as React from "react"
import * as SeparatorPrimitive from "@radix-ui/react-separator"
import { cn } from "@/lib/utils"

const Separator = React.forwardRef(
  ({ className, orientation = "horizontal", decorative = true, ...props }, ref) => (
    <SeparatorPrimitive.Root
      ref={ref}
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-border",
        orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
        className
      )}
      {...props}
    />
  )
)
Separator.displayName = SeparatorPrimitive.Root.displayName

export { Separator }
```

---

### Part 24: Development Commands

```bash
npm install       # Install dependencies
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
```

---

### Part 25: Customization Guide

When ClawdBot builds or modifies the AI Money Mastery site:

1. **Content**: Edit the `aiMethods`, `marketStats`, and `successStories` arrays in App.jsx
2. **Styling**: Modify the luxury aesthetic in App.css
3. **SEO**: Update meta tags in index.html
4. **Images**: Replace images in src/assets/
5. **Colors**: Adjust CSS variables in index.css and App.css
6. **Sections**: Create new components and import in App.jsx
7. **Animations**: Use Framer Motion for custom animations

The site is fully responsive: Desktop (1200px+), Tablet (768-1199px), Mobile (320-767px).

---

*Built for ClawdBot. Three skills, one file. Battle-tested on furrbudd.com, informed by competitive analysis of the top pet editorial platforms, and scaffolded from a Manus AI React build.*
