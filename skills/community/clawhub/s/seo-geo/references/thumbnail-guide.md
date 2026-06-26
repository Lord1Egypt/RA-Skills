# Blog Thumbnail Generation

How to create effective blog thumbnails for SaaS content. Thumbnails are not decoration — they are a direct lever on click-through rate across social sharing, SERP rich results, and content aggregators.

## Thumbnail Psychology

Thumbnails drive approximately 50% of CTR on social platforms and SERP rich results. When a user sees a list of results or a social feed, the thumbnail is processed before the title text. A strong thumbnail earns the click; a weak one gets scrolled past regardless of content quality.

Key principles:
- **Pattern interrupt.** The thumbnail must stand out from adjacent content in the feed. If every competitor uses blue backgrounds, use orange.
- **Instant comprehension.** A viewer should understand what the content is about within 0.5 seconds of seeing the thumbnail.
- **Emotional trigger.** Curiosity, comparison, urgency, or clarity — the thumbnail should provoke one of these.
- **Brand recognition.** Consistent style across thumbnails builds recognition over time. Viewers start clicking because they recognize your visual pattern.

## Dimensions

| Use Case             | Dimensions   | Aspect Ratio |
|----------------------|--------------|--------------|
| Blog hero / YouTube  | 1280 x 720   | 16:9         |
| Open Graph (social)  | 1200 x 630   | ~1.91:1      |
| Twitter card         | 1200 x 628   | ~1.91:1      |
| LinkedIn share       | 1200 x 627   | ~1.91:1      |

**Standard practice:** Design at 1280x720 for the blog. Export a second version at 1200x630 for Open Graph meta tags. If you can only maintain one size, use 1200x630 — it works acceptably everywhere.

## Text Rules

Text on thumbnails must be treated differently than text on a webpage. It will be viewed at drastically different sizes depending on context.

- **Maximum 3-4 words.** Anything longer will not be readable at small sizes. "SaaS Pricing Guide" works. "The Complete Guide to SaaS Pricing Strategy for B2B Companies" does not.
- **High contrast.** White text on dark backgrounds or dark text on light backgrounds. Never place text on busy or medium-toned areas without a solid or semi-transparent backing.
- **Readable at 50x50px.** Test your thumbnail by scaling it down to the size it appears in a mobile feed. If you cannot read the text, increase the font size or reduce the word count.
- **Bold, sans-serif fonts.** Inter, Montserrat, or similar. Avoid thin weights, serif fonts, or script fonts — they break down at small sizes.
- **No full sentences.** Thumbnails use fragments, numbers, or single keywords. Think billboard, not paragraph.

## Color Psychology Basics

Use color intentionally based on the emotional response you want to trigger.

| Color  | Association           | Best For                                          |
|--------|-----------------------|---------------------------------------------------|
| Red    | Urgency, importance   | "Mistakes to Avoid," warnings, competitor battles  |
| Blue   | Trust, professionalism| Product guides, enterprise content, security topics|
| Green  | Growth, success       | Results, ROI content, case studies                 |
| Yellow | Attention, energy     | Listicles, tips, attention-grabbing announcements  |
| Orange | Action, enthusiasm    | CTAs, tutorials, "how to" content                  |
| Purple | Premium, innovation   | Advanced guides, thought leadership                |
| Black  | Authority, elegance   | Executive-level content, premium comparisons       |
| White  | Clarity, simplicity   | Minimalist designs, clean product screenshots      |

**Brand consistency note:** Pick 2-3 colors that align with your brand and rotate among them. Do not use a different color scheme for every thumbnail.

## Template Types

### Competitor VS

Split-screen design. Your product on one side, competitor on the other, "VS" in the center.

- **Layout:** Vertical split. Left side = your brand color, right side = competitor brand color. "VS" centered in a circle or bold text.
- **Elements:** Both logos (or product screenshots). Your side should be subtly more prominent (slightly larger, brighter, or positioned on the left where eyes land first).
- **Text:** "[Your Product] vs [Competitor]" or just "VS" if the logos are recognizable.
- **Color:** Use each brand's actual colors for their respective halves.

### Review

Product screenshot with a rating or verdict overlay.

- **Layout:** Product screenshot or UI as the background (slightly dimmed). Rating or verdict overlaid in a bold badge.
- **Elements:** Star rating, score (e.g., "8.5/10"), or a one-word verdict ("Best for Teams," "Worth It?").
- **Text:** Product name + verdict. Keep to 2-3 words max beyond the product name.
- **Color:** Green for positive reviews, yellow/orange for mixed, red for critical.

### Guide / Tutorial

Icon or illustration paired with title text on a clean background.

- **Layout:** Left-aligned icon or simple illustration. Title text on the right (or centered below).
- **Elements:** A relevant icon (gear for settings, chart for analytics, lock for security). Minimal — no product screenshots or complex illustrations.
- **Text:** The guide topic in 2-4 words. "API Setup Guide" or "SSO in 5 Min."
- **Color:** Brand primary color as background. White or light text.

### Listicle

Large number as the focal point with a topic indicator.

- **Layout:** The number takes up 40-60% of the thumbnail area. Topic icon or keyword beside or below it.
- **Elements:** Bold number ("7," "15," "21"). Optional: small icons representing the list items.
- **Text:** The number + topic. "7 Pricing Pages" or "12 Onboarding Flows."
- **Color:** High-contrast. The number should pop — consider a contrasting color for the number against the background.

## Tools for Generation

### Ideogram v3 Turbo via Replicate CLI

Best for generating custom illustrations and stylized thumbnails quickly.

```bash
replicate run ideogram-ai/ideogram-v3-turbo \
  --input prompt="[your prompt]" \
  --input aspect_ratio="16:9" \
  --input style_type="[style]"
```

**Style mapping by template type:**

| Template Type   | Ideogram Style          | Prompt Notes                                           |
|-----------------|-------------------------|--------------------------------------------------------|
| Competitor VS   | Flat Art                | "Split screen comparison, [Brand A] vs [Brand B], clean minimal design, bold VS text in center" |
| Review          | Flat Art                | "Product review card, rating badge, clean UI screenshot background" |
| Guide/Tutorial  | Magazine Editorial      | "Clean editorial layout, [topic] icon, professional SaaS blog header" |
| Listicle        | Flat Art                | "Bold number [N], [topic] icons, vibrant background, blog thumbnail" |

**Tips for AI-generated thumbnails:**
- Always specify "no text" or "minimal text" in the prompt — AI-generated text is unreliable. Add text manually afterward.
- Include "16:9 aspect ratio, blog thumbnail, high contrast" in every prompt.
- Generate 3-4 variations and pick the strongest.
- Post-process in a design tool to add your own text and branding.

### Canva (Manual Option)

- Use Canva's "Blog Banner" or "YouTube Thumbnail" templates as starting points.
- Upload your brand kit (colors, fonts, logos) for consistency.
- Maintain a set of 4-5 templates matching the types above. Duplicate and modify for each new article.
- Export as WebP for web use.

### Figma / Framer (Design Tool Option)

- Create a thumbnail component library with variants for each template type.
- Use auto-layout for consistent spacing.
- Share the library with your team so anyone can generate on-brand thumbnails.
- Figma plugins like "TinyImage" can export directly to compressed WebP.

## Naming Convention

```
{article-slug}-thumbnail.webp
```

Examples:
- `saas-pricing-guide-thumbnail.webp`
- `hubspot-vs-salesforce-thumbnail.webp`
- `7-onboarding-mistakes-thumbnail.webp`
- `plg-strategy-review-thumbnail.webp`

Keep slugs lowercase, hyphen-separated, matching the article URL slug. This makes it easy to associate thumbnails with their content programmatically.

## Compression

- **Format:** WebP. It provides 25-35% better compression than JPEG at equivalent quality and supports transparency.
- **Target size:** Under 200KB. Most thumbnails should land between 80-150KB.
- **Quality setting:** 80-85% quality in WebP is the sweet spot — visually indistinguishable from 100% at thumbnail sizes.
- **Fallback:** If your CMS does not support WebP, use JPEG at 85% quality. Avoid PNG for photographic thumbnails (file sizes are too large).

**Compression commands:**

```bash
# Convert and compress with cwebp
cwebp -q 82 input.png -o output.webp

# Batch convert all PNGs in a directory
for f in *.png; do cwebp -q 82 "$f" -o "${f%.png}.webp"; done
```

## Pre-Publish Checklist

Run through this before publishing any thumbnail.

- [ ] **Readable at small size?** Scale to 50x50px and confirm text is legible.
- [ ] **Brand-consistent?** Uses your established color palette and font.
- [ ] **Text contrast OK?** Text passes WCAG AA contrast ratio against its background.
- [ ] **No clutter?** Maximum 3 visual elements (text, icon/logo, background). If it feels busy, remove something.
- [ ] **Correct dimensions?** 1280x720 for blog, 1200x630 for OG tag.
- [ ] **Under 200KB?** Check file size after WebP compression.
- [ ] **Matches content?** The thumbnail accurately represents what the article covers. Clickbait thumbnails hurt long-term trust.
- [ ] **Named correctly?** Follows `{slug}-thumbnail.webp` convention.
- [ ] **Alt text prepared?** Have a descriptive alt text ready for the image tag.
