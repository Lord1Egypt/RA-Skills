# Instagram Recommended Templates

Use `list_templates({ platform: "instagram_post" })` to browse all available templates. Below are curated recommendations by format and niche.

## By Format

### Feed Post (1080x1080)
- Search: `list_templates({ platform: "instagram_post" })`

#### Quote / Text Post
- Search: `list_templates({ platform: "instagram_post", q: "quote text" })`
- Variables: `quote_text`, `author`, `bg_color`, `accent_color`
- Style: Clean Minimal or Bold & Graphic

#### Product Showcase
- Search: `list_templates({ platform: "instagram_post", q: "product showcase" })`
- Variables: `title`, `product_image`, `price`, `cta_text`
- Style: Warm Editorial or Clean Minimal

#### Tip / Value Post
- Search: `list_templates({ platform: "instagram_post", q: "tip value" })`
- Variables: `title`, `tip_text`, `number`, `category_icon`
- Style: Clean Minimal or Playful

### Story (1080x1920)
- Search: `list_templates({ platform: "instagram_story" })`

#### Announcement
- Variables: `title`, `body_text`, `date`, `bg_image`
- Style: Bold & Graphic or Warm Editorial

#### Poll / Question
- Variables: `question`, `option_a`, `option_b`, `bg_color`
- Style: Playful or Clean Minimal

### Carousel Slide
- Search: `list_templates({ platform: "instagram_post", q: "carousel slide" })`
- Variables: `slide_number`, `title`, `body_text`, `accent_color`
- Style: Consistent with slide 1

## Prompt Examples by Niche

### Food
```
generate_image({
  prompt: "Instagram feed post for an artisan bakery, warm editorial style, serif title 'Sourdough Sundays', cream and terracotta palette, centered bread photo area with flour dust texture background",
  platform: "instagram_post",
  locale: "en"
})
```

### Fitness
```
generate_image({
  prompt: "Instagram story for a gym workout routine, bold dark design with neon green accents, title 'PUSH DAY', numbered list of 6 exercises with rep counts, modern sans-serif font",
  platform: "instagram_story",
  locale: "en"
})
```

### Tech / SaaS
```
generate_image({
  prompt: "Instagram carousel cover for Python tips, dark theme with cyan code accents, title '7 Python One-Liners', monospace font for code, clean minimal layout, slide indicator dots at bottom",
  platform: "instagram_post",
  locale: "en"
})
```

### Fashion
```
generate_image({
  prompt: "Instagram feed post for an outfit of the day, black and blush minimal design, title 'OOTD', full-body photo placeholder area centered, small style tags at bottom, editorial serif font",
  platform: "instagram_post",
  locale: "en"
})
```

### Travel
```
generate_image({
  prompt: "Instagram carousel cover for a travel guide, ocean blue and sand palette, title 'BALI ON A BUDGET', subtitle '7 Days Under $500', photo collage area, adventure sans-serif font",
  platform: "instagram_post",
  locale: "en"
})
```

### Business / Coaching
```
generate_image({
  prompt: "Instagram carousel cover for business tips, navy and yellow palette, title '5 Pricing Mistakes', bold modern sans-serif, clean minimal style with geometric accent shapes",
  platform: "instagram_post",
  locale: "en"
})
```
