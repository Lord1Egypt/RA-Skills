# Output Template

Output file: `{domain}_design.md` (e.g. `stripe.com_design.md`)

## YAML Template

```yaml
---
version: alpha
name: {brand name}
description: {1-3 sentence visual style description}
colors:
  primary: "#XXX"        # CTA/brand color
  primary-active: "#XXX" # hover/active
  ink: "#XXX"            # darkest text
  body: "#XXX"           # body text
  body-strong: "#XXX"    # emphasized text
  muted: "#XXX"          # secondary text
  muted-soft: "#XXX"     # weakest text
  hairline: "#XXX"       # standard border
  hairline-soft: "#XXX"  # weak border
  hairline-strong: "#XXX"# emphasized border
  canvas: "#XXX"         # page background
  canvas-soft: "#XXX"    # soft background
  surface-card: "#XXX"   # card background
  surface-strong: "#XXX" # emphasized surface
  on-primary: "#XXX"     # text on primary
  semantic-error: "#XXX" # error color
  semantic-success: "#XXX" # success color
typography:
  display-mega: {fontFamily,fontSize,fontWeight,lineHeight,letterSpacing}
  display-lg: same / display-md: same / body-md: same
  body-sm: same / caption: same / code: same
  button: same / nav-link: same
rounded:
  none:0 sm:{px} md:{px} lg:{px} xl:{px} pill:{px}
spacing:
  xs:{px} sm:{px} base:{px} lg:{px} xl:{px} xxl:{px} section:{px}
components:
  top-nav: {bg,textColor,height}
  button-primary: {bg,textColor,rounded,padding,height}
  button-secondary: same
  hero-band/feature-card/code-block/text-input/footer: same format
---
```

## Field Reference

**colors**: All HEX. Must extract primary/ink/body/muted four-level text color scale. semantic-error/semantic-success only when visible on page.

**typography**: 5 properties per level `{fontFamily, fontSize(px), fontWeight, lineHeight, letterSpacing(px)}`. Font stack ordered by priority.

**rounded/spacing**: All px values. rounded.none fixed at 0px.

**components**: Only output components actually visible on the page.
