# Extraction Methods

## Process

1. `web_fetch` to get HTML
2. Extract styles: CSS variables(--var) > `<style>` selectors > inline style > Tailwind class inference > @font-face > manifest.json/design tokens
3. Cannot extract directly (hover colors, etc.) → infer from industry conventions
4. All colors unified to HEX

## Inference Rules

- hover color: darken primary by 10-15% / CSS variable `-hover` suffix
- active color: darken primary by 15-20%
- text color scale: decrease opacity from darkest (0.9→0.7→0.5→0.3)
- border color: text color at low opacity (0.1-0.15)

## Notes

- Cannot extract precisely → mark `estimated` + inference basis
- Font stack ordered by priority
- Only output visible components, do not fabricate
- Interaction animation timing → `out of scope`
- SPA/heavy JS rendering → note limitation, analyze based on available content
