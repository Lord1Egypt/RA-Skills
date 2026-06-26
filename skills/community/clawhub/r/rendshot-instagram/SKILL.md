---
name: instagram
description: "Create high-performing Instagram content images — feed posts, stories, reels covers, and carousels. Use when the user mentions: 'Instagram', 'IG', 'IG post', 'Instagram story', 'reels cover', 'Instagram carousel', 'feed post', or wants to create visual content for Instagram. Combines platform algorithm knowledge, visual design best practices, and Rendshot image generation."
---

# Instagram Content Image Generator

Create feed posts, stories, reels covers, and carousel graphics optimized for Instagram's algorithm and visual standards.

## Workflow

### Step 1: Understand the Content Goal

Ask (if not provided):
- What format? (feed post / story / reels cover / carousel)
- What niche? (e.g., food, fitness, fashion, tech, travel)
- What's the goal? (engagement, traffic, brand awareness, sales)
- Personal brand or business?

### Step 2: Apply Algorithm-Aware Decisions

Read [references/algorithm.md](references/algorithm.md) for:
- Format selection based on reach goals
- Caption and hook strategies that boost ranking
- Hashtag and engagement optimization
- Avoid patterns that reduce distribution

### Step 3: Apply Visual Style

Read [references/design-style.md](references/design-style.md) for:
- Aesthetic selection by niche
- Color palette and typography rules
- Layout patterns per format
- Visual consistency for brand building

### Step 4: Generate with Rendshot

**Feed Post (1080x1080):**
```
generate_image({
  prompt: "Instagram feed post for a coffee brand, minimal aesthetic, large serif title 'The Art of Pour Over', warm brown palette, clean white background, product photo area at center",
  platform: "instagram_post",
  locale: "en"
})
```

**Story (1080x1920):**
```
generate_image({
  prompt: "Instagram story for a fitness coach, bold modern design, title 'CHEST DAY ROUTINE', neon accent on dark background, numbered list layout for 5 exercises",
  platform: "instagram_story",
  locale: "en"
})
```

**Carousel (multi-call):**
Generate each slide individually with consistent style:
```
// Slide 1 — Cover
generate_image({
  prompt: "Instagram carousel cover slide, '5 Python Tips You Need', modern tech aesthetic, dark theme with green accents, bold sans-serif",
  platform: "instagram_post"
})

// Slide 2-5 — Content slides (use create_template for consistency)
generate_image({
  template_id: "tpl_carousel_slide",
  variables: { slide_number: "1", tip_title: "F-Strings", code_snippet: "..." }
})
```

**Using templates:**
```
list_templates({ platform: "instagram_post", q: "product showcase" })
get_template({ template_id: "tpl_xxx" })
generate_image({ template_id: "tpl_xxx", variables: { ... } })
```

### Step 5: Save for Brand Consistency

```
create_template({
  name: "Coffee Brand IG Post",
  html: "<returned html>",
  variables: [...],
  platform: "instagram_post",
  tags: ["coffee", "minimal", "brand"]
})
```

## Format Quick Reference

| Format | Platform preset | Size | Use case |
|--------|----------------|------|----------|
| Feed post | `instagram_post` | 1080x1080 | Main feed content |
| Story | `instagram_story` | 1080x1920 | Stories, reels covers |
| Landscape | `twitter_post` | 1200x675 | IGTV covers, link previews (no IG-specific landscape preset; this cross-platform size works) |

## Carousel Best Practices

- Slide 1: Hook — bold title, curiosity gap, no text wall
- Slides 2-N: One idea per slide, consistent layout template
- Last slide: CTA ("Save this", "Follow for more", "Link in bio")
- Use `create_template` after first slide to lock the layout for remaining slides
- Optimal length: 5-10 slides (algorithm favors time-on-post)

## References

- [Algorithm and reach optimization](references/algorithm.md) — ranking signals, format strategy, hashtags
- [Visual design guide](references/design-style.md) — aesthetics by niche, color palettes, typography
- [Recommended templates](references/templates.md) — curated templates by format and niche
