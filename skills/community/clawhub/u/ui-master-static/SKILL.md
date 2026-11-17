---
name: ui-master-static
description: "Use this skill whenever the user wants to build a production-grade UI with native/vanilla CSS — no Tailwind, no CSS-in-JS, no utility framework. Triggers include: plain Vite + HTML/CSS projects, static sites, simple landing pages, or any project explicitly avoiding a CSS framework; requests for a header, navbar, dashboard shell, or landing layout built with 'plain CSS' or 'native CSS'; requests for modern visual effects (glassmorphism, gradients, scroll animations, parallax, 3D transforms, micro-interactions, CSS Houdini); or establishing a CSS architecture (custom properties as design tokens, BEM naming, file organization) for a project without a component framework. Do NOT use this skill for Tailwind CSS or shadcn/ui projects — use the ui-master skill instead. Do NOT use for CSS-in-JS (styled-components, emotion) or CSS Modules-first projects unless the user explicitly wants the BEM/vanilla approach applied there too."
---

# UI Master Static — Production-Grade UI with Native CSS + BEM

Approach this the way a senior CSS engineer approaches a framework-free build: every advantage a utility framework gives you — consistency, theming, no dead code — has to come from discipline instead of tooling. That means a real token system in `:root` custom properties, a naming convention (BEM) that keeps specificity flat and predictable, and a deliberate architecture so the CSS doesn't rot into a pile of one-off overrides by the tenth page.

This skill is deliberately thorough — treat it as a reference library, not a script to run top to bottom. Read the reference file that matches what you're building; don't load everything for a one-off tweak.

## When this applies vs. `ui-master`

Use **this** skill for: plain Vite scaffolds, static HTML/CSS sites, projects that explicitly reject a utility framework, or any brief that says "native CSS," "vanilla CSS," or "no Tailwind." Use **`ui-master`** instead for Tailwind v4 + shadcn/ui projects. The two skills share the same production-quality bar (tokens, accessibility, real states) but differ entirely in mechanism — don't mix utility classes into a project this skill is styling.

## Step 0 — Confirm scope

Infer from the repo if present: is there already a `styles/` or `css/` folder with an existing architecture? If so, match its conventions rather than imposing a new one wholesale — introduce BEM/tokens incrementally if the existing code doesn't use them, rather than rewriting everything unasked. For a greenfield project, set up the full architecture from `references/css-architecture-bem.md` from the start.

## Step 1 — Architecture and tokens

Before writing a single component's CSS, read `references/css-architecture-bem.md`. It covers:

- The design token system: every color, spacing, radius, shadow, and type value declared once as a custom property in `:root`, never a literal value inside a component rule
- BEM naming (`block__element--modifier`) and why it keeps specificity flat (one class, one specificity level — no cascade fights)
- File organization for a framework-free project (tokens → base/reset → layout → components → utilities), and the import order that keeps the cascade predictable
- The two-stage custom-property pattern for a runtime light/dark theme toggle (same underlying mechanism as Tailwind v4's `@theme inline`, just without the build step)

Get this right first — it's the difference between a CSS codebase that stays maintainable past page three and one that needs `!important` by page five.

## Step 2 — Layout patterns

Read `references/layout-patterns.md` for structural patterns: sticky/blurred headers with mobile navigation, dashboard shells (sidebar + topbar) built with CSS Grid template areas, responsive card grids with container queries (`@container`, no plugin needed in native CSS either — it's a browser feature), and landing-page hero/section rhythm. Adapt the worked examples in `examples/header.html` + `examples/header.css` and `examples/dashboard.html` + `examples/dashboard.css` rather than starting from a blank file.

## Step 3 — Modern effects

Read `references/modern-effects.md` for the full effects catalogue: glassmorphism, layered/mesh gradients, elevation shadow scales, scroll-driven animations (native `animation-timeline: scroll()`, no JS/library needed), parallax, hover/focus micro-interactions, 3D transforms and perspective, complex multi-stage `@keyframes`, and CSS Houdini (`@property` for animatable custom properties — excellent support — and the Paint API, which is Chromium-first and needs a progressive-enhancement fallback). `examples/effects-showcase.html` + `examples/effects-showcase.css` demonstrate each technique in isolation so you can lift the specific one needed rather than reverse-engineering a combined demo.

**Restraint still applies.** Reference `frontend-design` skill's guidance: spend boldness in one place per screen. A header with a glass blur AND a gradient mesh AND a 3D tilt AND a scroll-triggered reveal all at once reads as a tech demo, not a product. Pick the one effect that serves this specific brief's signature moment; keep the rest of the page quiet and disciplined.

## Step 4 — Verify before calling it done

Read `references/accessibility-performance-checklist.md`. Native CSS has no framework to catch mistakes for you — the checklist matters more here, not less. Pay particular attention to:

- Every effect in Step 3 has a `prefers-reduced-motion` fallback (scroll animations, parallax, and 3D transforms are the most common offenders)
- Houdini Paint API effects have a plain-CSS fallback for non-Chromium browsers (`@supports`)
- Specificity stayed flat — if you needed `!important` anywhere, the BEM structure broke down somewhere and should be fixed at the source, not patched over

## Common failure modes to avoid

- **Specificity creep**: nested selectors like `.card .card__title.active` instead of a single BEM class like `.card__title--active` — the moment two classes combine to override a third, the architecture has started to fail.
- **Literal values in component CSS**: `padding: 23px` or `color: #3a86ff` inside a component block instead of a token — makes theming and consistency impossible to enforce later.
- **Effects with no fallback**: `animation-timeline: scroll()` or Paint API used with no `@supports` fallback, silently breaking the experience on unsupported browsers instead of degrading gracefully.
- **One CSS file that keeps growing**: no separation between tokens, layout, and components — every new page becomes harder to place correctly.
- **Reduced-motion ignored**: parallax and scroll-linked animation are exactly the effects most likely to cause discomfort for motion-sensitive users, and exactly the ones most often shipped without the media query guard.
