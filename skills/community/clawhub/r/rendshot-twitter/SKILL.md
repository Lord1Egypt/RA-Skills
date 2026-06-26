---
name: twitter
description: "Create high-performing Twitter/X content images — post images, thread headers, link preview cards, and profile banners. Use when the user mentions: 'Twitter', 'X', 'tweet image', 'Twitter card', 'X post', 'tweet graphic', 'thread header', or wants to create visual content for Twitter/X. Combines platform algorithm knowledge, visual design best practices, and Rendshot image generation."
---

# Twitter/X Content Image Generator

Create post images, thread headers, and link preview cards optimized for Twitter/X's algorithm and visual standards.

## Workflow

### Step 1: Understand the Content Goal

Ask (if not provided):
- What type? (single image post / thread header / link preview card / poll graphic)
- What niche? (tech, business, creator, news, meme)
- Goal? (engagement, clicks, followers, brand)

### Step 2: Apply Algorithm-Aware Decisions

Read [references/algorithm.md](references/algorithm.md) for:
- Image post vs text-only performance differences
- Thread optimization strategies
- Engagement patterns by content type
- Avoid suppression triggers

### Step 3: Apply Visual Style

Read [references/design-style.md](references/design-style.md) for:
- Style selection by niche
- Color palette and typography rules
- Layout patterns per format
- Dark mode considerations (most Twitter users use dark mode)

### Step 4: Generate with Rendshot

**Post Image (1200x675):**
```
generate_image({
  prompt: "Twitter post image for a tech announcement, dark theme, bold white title 'We just shipped v2.0', subtle gradient background, modern sans-serif, minimal and impactful",
  platform: "twitter_post",
  locale: "en"
})
```

**Link Preview Card (1200x628):**
```
generate_image({
  prompt: "Twitter card for a blog post about React performance, dark blue tech aesthetic, title 'React Renders Explained', code snippet preview, clean layout",
  platform: "twitter_card",
  locale: "en"
})
```

**Thread Header:**
```
generate_image({
  prompt: "Twitter thread header image, 'How I Built a SaaS in 30 Days', numbered badge '1/12', dark background with cyan accent, bold modern font",
  platform: "twitter_post"
})
```

**Using templates:**
```
list_templates({ platform: "twitter_card", q: "blog post" })
get_template({ template_id: "tpl_xxx" })
generate_image({ template_id: "tpl_xxx", variables: { ... } })
```

### Step 5: Save for Brand Consistency

```
create_template({
  name: "Product Launch Tweet",
  html: "<returned html>",
  variables: [...],
  platform: "twitter_post",
  tags: ["launch", "product", "announcement"]
})
```

## Format Quick Reference

| Format | Platform preset | Size | Use case |
|--------|----------------|------|----------|
| Post image | `twitter_post` | 1200x675 | Image tweets, thread headers |
| Link card | `twitter_card` | 1200x628 | Blog/article OG images for link previews |

## Key Principles

- **Dark mode first**: ~80% of Twitter users use dark mode. Design for dark backgrounds.
- **Bold and scannable**: Users scroll fast. Large text, high contrast, minimal elements.
- **One message per image**: Don't cram multiple ideas. One clear takeaway.
- **Text-to-visual ratio**: Twitter favors images with less text overlay. Keep it punchy.

## References

- [Algorithm and engagement optimization](references/algorithm.md) — ranking signals, image vs text performance, thread strategy
- [Visual design guide](references/design-style.md) — dark mode design, niche aesthetics, typography
- [Recommended templates](references/templates.md) — curated templates by content type
