# Analysis Dimensions

## 1. Design Style

Judgment dimensions: brand color tone (warm/cool/neutral/pure white/dark) → visual language (skeuomorphic/flat/neumorphic/minimalist/editorial/magazine/tech) → brand color strategy (monochrome/dual/multi-color) → depth expression (shadow layers/border lines) → typographic tone (weight strategy/letter-spacing) → UI texture (border-radius/boundaries/cards)

Output 3-5 sentences into the `description` field.

## 2. Color System

Extract: primary brand color (CTA) → primary hover state (hover/active) → text color scale (ink>body>muted>muted-soft) → border color scale (hairline>hairline-soft>hairline-strong) → page background (canvas>canvas-soft>surface-card>surface-strong) → semantic colors (error/success, when visible) → special colors (timeline/tags)

Source: CSS variables > `<style>` selectors > inline style > Tailwind class inference. Unify to HEX.

## 3. Typography

Hierarchy: display-mega(H1/Hero) > display-lg/md/sm > title-md/sm > body-md/sm > caption > code > button > nav-link

Record per level: fontFamily, fontSize(px), fontWeight, lineHeight, letterSpacing(px)

## 4. Spacing & Border Radius

Border radius: border-radius of buttons/cards/inputs/badges
Spacing: paragraph spacing/grid spacing/section spacing + content area padding

## 5. Component Styles

Only extract visible components: top-nav(bg/text/height) | button-primary(bg/text/rounded/padding/height) | button-secondary(same) | feature-card(bg/rounded/padding) | pricing-card(if present) | text-input(if present) | code-block(bg/font/rounded/padding) | footer(bg/text/padding) | badge/pill(bg/rounded/text)

## 6. Design Guidelines

- **Do**: color boundaries/font strategy/spacing rules
- **Don't**: prohibitions (no secondary brand color/no pure white background, etc.)
- **Breakpoints**: responsive breakpoints and layout changes (if inferable)
