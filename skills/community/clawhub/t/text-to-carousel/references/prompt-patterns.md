# Carousel Prompt Patterns

## Design Style Presets

### Dark Luxury (recommended for health/premium brands)
```
STYLE: Ultra-premium dark editorial. Like Aesop, Tom Ford, or luxury skincare brand.
Background: Deep dark emerald (#0a2420) with subtle floating gold bokeh particles.
Translucent bamboo/leaf silhouettes layered in background.
Moody, dark, premium luxury feel.
```

### Clean Medical (for infographic/data slides)
```
STYLE: Modern luxury medical editorial. Clean but sophisticated.
Background: Off-white (#f7f5f2) with subtle texture.
Teal (#008080) accent elements.
Professional, trustworthy, clean layout.
```

### Warm Testimonial (for social proof slides)
```
STYLE: Luxury brand social proof. Warm and trustworthy.
Background: Warm golden cream (#fff8ee) gradient.
Gold accent bar at top.
White cards with colored left borders.
```

## Slide Type Templates

### Cover Slide
```
Create a stunning 1024x1024 luxury Instagram carousel cover for [BRAND].
- "BRAND_NAME" in small elegant gold serif at top center
- Main title: [TITLE] in LARGE white serif
- Thin gold horizontal line separator
- Subtitle: [SUBTITLE] in medium gold
- Tag pills with gold borders: [TAG1] | [TAG2] | [TAG3]
- "01 / [TOTAL]" bottom right
CRITICAL: The Chinese characters must be exactly: [EXACT_TEXT]
```

### Infographic Slide
```
Create a 1024x1024 premium infographic Instagram slide.
- Header: [HEADER] in dark teal, large bold
- [N] cards in [LAYOUT] grid, white with [COLOR] left border:
  Card 1: [TEXT]
  Card 2: [TEXT]
- Highlighted box: [KEY_MESSAGE]
- Button: [CTA_TEXT]
CRITICAL: All Chinese text must be exactly as written above.
```

### Comparison Slide
```
Create a 1024x1024 premium comparison infographic.
- Three comparison cards stacked vertically:
  Card 1 (RED): [NAME] | [DETAIL] | red progress bar [PCT]% | ✕
  Card 2 (AMBER): [NAME] | [DETAIL] | amber bar [PCT]% | !
  Card 3 (GREEN): [NAME] | [DETAIL] | green bar [PCT]% | ✓
- Traffic light color coding.
- Conclusion: [KEY_MESSAGE]
```

### Product CTA Slide
```
Create a 1024x1024 premium product CTA Instagram slide.
- Dark emerald gradient with golden bokeh
- Header: [CTA_TITLE] in gold, [SUBTITLE] in white
- CENTER: The attached product image
- Selling points in gold: [POINT1], [POINT2], ...
- Gold CTA button: [CTA_TEXT]
```

## Chinese Text Tips

- Always include "CRITICAL: The Chinese characters must be exactly: [TEXT]" at end of prompt
- For important text, spell out character by character if needed
- gemini-3-pro-image-preview handles Chinese well; gemini-2.5-flash-image does NOT
- Verify output with vision model before delivery

## Common Carousel Structures

### Health/Wellness (6 slides)
1. Cover — Hook + brand
2. Problem — Why this matters
3. Solution — How product solves it
4. Details — Key features/ingredients
5. Social Proof — Testimonials/results
6. CTA — Product + buy now

### Educational (5 slides)
1. Cover — Topic + hook
2-4. Content — Key points (one per slide)
5. CTA — Follow/share/visit

### Product Launch (4 slides)
1. Cover — Product name + hero shot
2. Features — Key selling points
3. Social Proof — Reviews/testimonials
4. CTA — Buy now + link
