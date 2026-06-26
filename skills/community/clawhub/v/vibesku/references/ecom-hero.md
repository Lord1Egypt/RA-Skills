# Template: ecom-hero

**Purpose**: Generate a single professional product image — main photos, marketing banners, or vertical posters.

**When to use**: User needs ONE image for a specific placement (storefront hero, ad banner, social post, product main photo).

**Output type**: IMAGE | **Supports analysis**: Yes | **Cost**: 1K/2K = 1 credit, 4K = 2 credits

## Assets

| Role | Min | Max | Required |
|------|-----|-----|----------|
| PRODUCT (product images) | 1 | 10 | Yes |
| LOGO (brand logo) | 0 | 1 | No |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scenario` | string | `MAIN_IMAGE` | Image layout type (see below) |
| `style` | string | `auto` | Visual style (see below) |
| `customStyle` | string | — | Free-text style description (only when `style=custom`) |
| `aspectRatio` | string | `1:1` | Output aspect ratio (e.g. `1:1`, `16:9`, `3:4`, `9:16`) |
| `imageSize` | string | `2K` | Resolution: `1K`, `2K`, or `4K` (4K = 2 credits) |
| `layoutMode` | string | `auto` | Text layout: `auto`, `stacked`, `side-by-side`, `diagonal` |
| `primaryLang` | string | `en` | Primary text language code |
| `secondaryLang` | string | `none` | Secondary language (`none` for monolingual) |

## Scenario Options

Controls the overall image composition and layout.

| Scenario | Best For | Default Ratio | Description |
|----------|----------|---------------|-------------|
| `MAIN_IMAGE` | Product listings, storefronts | 1:1 | Product centered, clean background, maximum product visibility |
| `BANNER` | Homepage heroes, ad creatives | 16:9 | Horizontal layout with space for marketing text |
| `POSTER` | Social media, detail pages | 3:4 | Vertical format, prominent product with text overlay |

**When to use which scenario**:
- **MAIN_IMAGE**: Default choice. Product is the focus, no marketing text needed. E-commerce main photo, catalog image.
- **BANNER**: Need horizontal layout WITH text. Homepage hero, email header, Facebook ad, LinkedIn banner.
- **POSTER**: Need vertical layout WITH text. Instagram post, detail page top image, in-store display.

## Style Options

Controls the visual aesthetic, lighting, and mood of the generated image.

| Style | Visual Feel | Best For |
|-------|-------------|----------|
| `auto` | AI analyzes product and picks best style | When unsure — let AI decide |
| `studio` | Clean background, professional lighting | Electronics, watches, jewelry |
| `lifestyle` | Real-world context, warm tones | Food, home goods, apparel |
| `premium` | Dark theme, metallic accents, generous whitespace | Luxury items, high-end tech |
| `minimal` | Geometric, monochrome, clean | Modern accessories, stationery |
| `vibrant` | Bold colors, high energy | Kids products, sports, snacks |
| `tech` | Cool tones, glow effects, data viz | Gadgets, smart devices |
| `organic` | Earth tones, botanical elements | Health, organic, eco-friendly |
| `custom` | User-defined (requires `customStyle`) | Specific brand aesthetic |

**When to use `custom`**: When the user describes a specific visual direction that doesn't match any preset (e.g. "Scandinavian cafe aesthetic" or "Y2K retro gradient"). Pass the description as `customStyle`.

## Layout Mode

Controls how overlaid text is positioned relative to the product.

| Mode | Description | When to Use |
|------|-------------|-------------|
| `auto` | AI decides based on product shape and scenario | Default — works well in most cases |
| `stacked` | Text above or below product | Tall/vertical products |
| `side-by-side` | Text left or right of product | Wide/horizontal products |
| `diagonal` | Text along a diagonal axis | Dynamic, energetic compositions |

## Examples

```bash
# Product main photo (most common use case)
vibesku generate -t ecom-hero \
  -n "Wireless Headphones" -d "Premium ANC with 30h battery" \
  -b "AudioTech" -i product.jpg -l logo.png

# Marketing banner for homepage (16:9)
vibesku generate -t ecom-hero \
  -n "Summer Collection" -i hero-product.jpg \
  -o '{"scenario":"BANNER","style":"vibrant","aspectRatio":"16:9"}'

# Premium vertical poster (3:4, 4K)
vibesku generate -t ecom-hero \
  -n "Luxury Watch" -i watch.jpg \
  -o '{"scenario":"POSTER","style":"premium","aspectRatio":"3:4","imageSize":"4K"}'

# Bilingual banner (Chinese primary + English secondary)
vibesku generate -t ecom-hero \
  -n "智能音箱" -d "AI语音助手，360度环绕音效" -i speaker.jpg \
  -o '{"scenario":"BANNER","primaryLang":"zh","secondaryLang":"en"}'

# Custom brand style
vibesku generate -t ecom-hero \
  -n "Artisan Coffee" -i coffee.jpg \
  -o '{"style":"custom","customStyle":"Scandinavian cafe aesthetic, muted pastels, hand-drawn illustrations"}'

# Instagram Story ad (9:16 vertical)
vibesku generate -t ecom-hero \
  -n "Running Shoes" -i shoes.jpg \
  -o '{"scenario":"POSTER","style":"vibrant","aspectRatio":"9:16"}'

# Multiple product angles for better AI understanding
vibesku generate -t ecom-hero \
  -n "Ceramic Vase" -i front.jpg side.jpg top.jpg detail.jpg \
  -o '{"style":"minimal"}'
```

## Tips

- When user doesn't specify style, omit it — `auto` lets AI analyze the product and pick the best match
- For social media: `BANNER` + `16:9` (Facebook/LinkedIn), `POSTER` + `9:16` (Instagram Stories/TikTok), `MAIN_IMAGE` + `1:1` (Instagram feed)
- `imageSize: 4K` doubles the credit cost — only use when user explicitly needs high resolution or print-quality
- Multiple product images (via `-i`) help AI understand the product from different angles — the more angles, the more faithful the reproduction
- For bilingual output, set both `primaryLang` and `secondaryLang` — primary language is displayed more prominently
- Always include `-b` (brand name) and `-l` (logo) when user has brand assets — they get integrated into the layout
