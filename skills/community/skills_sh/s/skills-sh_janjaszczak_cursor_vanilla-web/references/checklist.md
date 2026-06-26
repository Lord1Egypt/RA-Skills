<!-- .cursor/skills/vanilla-web/references/checklist.md -->

# Vanilla Web – Done Checklist

## HTML
- Semantic elements used; no div-soup for buttons/inputs
- Forms have labels; interactive controls are keyboard reachable
- Focus visible (CSS) and focus order logical

## CSS
- No layout tied to fixed pixel widths unless explicitly required
- Uses variables for repeated values (spacing/colors) where sensible
- No unused selectors added

## JS (ESM)
- No global mutable variables introduced
- Modules have single responsibility
- Event handlers are small; heavy logic extracted to utilities
- Errors handled (try/catch around async boundaries where needed)

## Runtime
- Page loads without console errors
- Feature verified in browser (happy path + one failure path)
- Runbook updated (how to start/verify)

## Delivery quality
- Complete runnable files committed/produced
- Minimal verification steps included in the final response
