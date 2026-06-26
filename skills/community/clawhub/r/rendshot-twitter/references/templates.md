# Twitter/X Recommended Templates

Use `list_templates({ platform: "twitter_post" })` or `list_templates({ platform: "twitter_card" })` to browse all available templates.

## By Content Type

### Product Launch / Announcement
- Search: `list_templates({ platform: "twitter_post", q: "launch announcement" })`
- Variables: `title`, `subtitle`, `logo`, `bg_color`
- Style: Tech / Business

### Thread Header
- Search: `list_templates({ platform: "twitter_post", q: "thread header" })`
- Variables: `title`, `thread_count`, `topic_tag`
- Style: Creator / Bold

### Blog Link Card
- Search: `list_templates({ platform: "twitter_card", q: "blog article" })`
- Variables: `title`, `author`, `site_name`, `bg_image`
- Style: Clean / Editorial

### Data / Stat Visualization
- Search: `list_templates({ platform: "twitter_post", q: "data stat chart" })`
- Variables: `metric`, `value`, `context`, `source`
- Style: Data / Research

## Prompt Examples

### Tech Launch
```
generate_image({
  prompt: "Twitter post image for a product launch, dark background #0D1117, large bold white title 'v2.0 is live', green accent #3FB950, terminal-style code snippet showing the key feature, minimal and impactful",
  platform: "twitter_post",
  locale: "en"
})
```

### Thread Header
```
generate_image({
  prompt: "Twitter thread header, dark navy background, large bold text 'How I got 10K followers in 90 days', thread indicator '🧵 1/8' in top right, creator personal brand style, high contrast white text",
  platform: "twitter_post",
  locale: "en"
})
```

### Blog Card
```
generate_image({
  prompt: "Twitter link card for a technical blog post titled 'Understanding WebSockets', dark gradient background, code bracket decorations, clean sans-serif font, site logo bottom-right",
  platform: "twitter_card",
  locale: "en"
})
```

### Data Highlight
```
generate_image({
  prompt: "Twitter data visualization image, central large number '47%' in bold, subtitle 'of developers now use AI daily', minimal dark background, single blue accent color, source citation at bottom",
  platform: "twitter_post",
  locale: "en"
})
```
