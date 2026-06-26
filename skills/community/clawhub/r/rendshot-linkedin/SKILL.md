---
name: linkedin
description: "Create high-performing LinkedIn content images — feed posts, article covers, carousel documents, and company page graphics. Use when the user mentions: 'LinkedIn', 'LinkedIn post', 'LinkedIn carousel', 'LinkedIn article', 'professional post', or wants to create visual content for LinkedIn. Combines platform algorithm knowledge, B2B visual design best practices, and Rendshot image generation."
---

# LinkedIn Content Image Generator

Create feed posts, article covers, and carousel graphics optimized for LinkedIn's algorithm and professional visual standards.

## Workflow

### Step 1: Understand the Content Goal

Ask (if not provided):
- What type? (feed post / article cover / carousel / company update)
- What industry? (tech, finance, consulting, HR, marketing)
- Goal? (thought leadership, lead gen, hiring, brand awareness)
- Personal profile or company page?

### Step 2: Apply Algorithm-Aware Decisions

Read [references/algorithm.md](references/algorithm.md) for:
- Content type ranking by reach
- Dwell time and engagement signals
- Posting strategy for B2B audiences
- Avoid suppression patterns

### Step 3: Apply Visual Style

Read [references/design-style.md](references/design-style.md) for:
- Professional aesthetic standards
- Color palette by industry
- Typography for credibility
- Carousel slide design patterns

### Step 4: Generate with Rendshot

**Feed Post (1200x627):**
```
generate_image({
  prompt: "LinkedIn feed post for a SaaS startup, professional clean design, title 'We Raised $5M Series A', navy and white palette, company logo area top-left, key metrics grid below title",
  platform: "linkedin_post",
  locale: "en"
})
```

**Carousel (multi-slide, 1200x627 each):**
```
// Slide 1 — Cover
generate_image({
  prompt: "LinkedIn carousel cover, '5 Lessons from Scaling to 100 Employees', professional dark blue gradient, large bold title, author photo area bottom-left",
  platform: "linkedin_post"
})

// Subsequent slides — use template for consistency
generate_image({
  template_id: "tpl_linkedin_slide",
  variables: { slide_number: "1", lesson_title: "Hire slow, fire fast", body: "..." }
})
```

**Using templates:**
```
list_templates({ platform: "linkedin_post", q: "professional" })
get_template({ template_id: "tpl_xxx" })
generate_image({ template_id: "tpl_xxx", variables: { ... } })
```

### Step 5: Save for Brand Consistency

```
create_template({
  name: "Company Announcement",
  html: "<returned html>",
  variables: [...],
  platform: "linkedin_post",
  tags: ["announcement", "corporate", "professional"]
})
```

## Format Quick Reference

| Format | Platform preset | Size | Use case |
|--------|----------------|------|----------|
| Feed post | `linkedin_post` | 1200x627 | Images, carousels, announcements |

## Key Principles

- **Professional first**: No memes, no casual design. Clean, credible, corporate-appropriate.
- **Carousel is king**: LinkedIn carousels (PDF documents) get 3-5x more reach than single images.
- **Value-dense**: LinkedIn users expect insights, data, and actionable takeaways.
- **Author credibility**: Include author name/photo/title — personal branding drives engagement.

## References

- [Algorithm and reach optimization](references/algorithm.md) — ranking signals, content types, posting strategy
- [Visual design guide](references/design-style.md) — professional aesthetics, industry palettes, carousel patterns
- [Recommended templates](references/templates.md) — curated templates by content type
