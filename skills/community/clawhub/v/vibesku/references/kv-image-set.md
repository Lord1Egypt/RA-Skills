# Template: kv-image-set

**Purpose**: Generate a coordinated set of detail-page posters from a single product — each poster covers a different storytelling angle (hero shot, lifestyle, tech specs, user reviews, etc.).

**When to use**: User needs a COMPLETE visual set for a product detail page, campaign, or brand presentation. This is VibeSKU's signature "VisionKV™" capability.

**Output type**: IMAGE | **Supports analysis**: Yes | **Cost**: 1K/2K = 1 credit/scene, 4K = 2 credits/scene

## Assets

| Role | Min | Max | Required |
|------|-----|-----|----------|
| PRODUCT (product images) | 1 | 10 | Yes |
| LOGO (brand logo) | 0 | 1 | No |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scenes` | string[] | `["kv-hero"]` | **Scene IDs to generate** — each scene = 1 poster (see below) |
| `style` | string | `auto` | Visual style applied across all scenes (see below) |
| `customStyle` | string | — | Free-text style (only when `style=custom`) |
| `typography` | string | `auto` | Text rendering effect (see below) |
| `customTypography` | string | — | Free-text typography (only when `typography=custom`) |
| `aspectRatio` | string | `9:16` | Output ratio (typically vertical: `9:16` or `3:4`) |
| `imageSize` | string | `2K` | Resolution: `1K`, `2K`, or `4K` |
| `layoutMode` | string | `auto` | Text layout: `auto`, `stacked`, `side-by-side`, `diagonal` |
| `primaryLang` | string | `zh` | Primary text language (default Chinese for detail pages) |
| `secondaryLang` | string | `en` | Secondary language |

## Scene Options

Each scene generates ONE poster. Order in the array determines output order.

| Scene ID | Name | Description | Best For |
|----------|------|-------------|----------|
| `kv-hero` | Hero Visual | Main cover image, faithful product reproduction | Always include — the "cover" of the product |
| `lifestyle` | Lifestyle / Usage | Product in real-world usage context | Showing product in use, building desire |
| `tech-craft` | Tech / Craft | Manufacturing process or technology visualization | Products with notable tech or craftsmanship |
| `detail-01` | Close-up: Product Detail | Zoomed-in key product feature | Highlighting a standout physical feature |
| `detail-02` | Close-up: Material / Texture | Material and texture showcase | Premium materials, fabric, metal finish |
| `detail-03` | Close-up: Functional Detail | Feature demonstration | Buttons, ports, mechanisms, moving parts |
| `user-review` | User Testimonials | Customer experience and social proof | Building trust, review-driven purchases |
| `brand-story` | Brand Story | Brand narrative and design origin | Brand-centric campaigns, premium positioning |
| `specs-table` | Product Specifications | Technical spec table | Electronics, appliances, detailed products |
| `usage-guide` | Usage Guide | How-to instructions and important notes | Products requiring setup or care instructions |

### Recommended Scene Combinations

| Use Case | Scenes | Poster Count |
|----------|--------|-------------|
| **Quick product page** | `["kv-hero", "lifestyle", "detail-01"]` | 3 |
| **Standard detail page** | `["kv-hero", "lifestyle", "tech-craft", "detail-01", "specs-table"]` | 5 |
| **Full detail page** | `["kv-hero", "lifestyle", "tech-craft", "detail-01", "detail-02", "user-review", "specs-table"]` | 7 |
| **Brand campaign** | `["kv-hero", "brand-story", "lifestyle", "user-review"]` | 4 |
| **Tech product launch** | `["kv-hero", "tech-craft", "detail-01", "detail-03", "specs-table"]` | 5 |
| **Beauty / skincare** | `["kv-hero", "lifestyle", "detail-02", "usage-guide"]` | 4 |
| **Food / beverage** | `["kv-hero", "lifestyle", "detail-01", "brand-story"]` | 4 |

**How to choose scenes**:
- Always start with `kv-hero` — it's the visual anchor of the entire set
- Add `lifestyle` when the product benefits from being shown in-use
- Add `detail-01/02/03` when the product has notable physical features, materials, or mechanisms
- Add `specs-table` for products where buyers compare specifications
- Add `user-review` when social proof is important (competitive categories)
- Add `brand-story` for premium/artisan products where origin matters
- Add `usage-guide` when the product has non-obvious usage or care instructions

## Style Options

Style is applied consistently across ALL scenes in the set, ensuring visual coherence.

| Style | Visual Feel | Best For |
|-------|-------------|----------|
| `auto` | AI picks based on product analysis | Default — recommended for most cases |
| `magazine` | Editorial layout, generous whitespace, high-fashion feel | Fashion, beauty, lifestyle brands |
| `watercolor` | Warm gradients, hand-painted texture | Artisan products, tea, ceramics |
| `tech-future` | Cool tones, glow effects, data overlays | Electronics, smart devices, SaaS |
| `retro-film` | Film grain, warm tones, nostalgic | Vintage, food & drink, heritage brands |
| `nordic-minimal` | Geometric, monochrome, ultra-clean | Modern accessories, furniture |
| `cyberpunk` | Neon, dark theme, glow effects | Gaming, youth-oriented, bold products |
| `organic-nature` | Earth tones, botanical, eco-friendly | Health, organic, sustainable products |
| `custom` | User-defined (requires `customStyle`) | Specific brand aesthetic |

## Typography Options

Controls how text is rendered on all posters in the set.

| Typography | Effect | Best For |
|------------|--------|----------|
| `auto` | AI selects based on style | Default — works well in most cases |
| `editorial-grid` | Bold serif + grid alignment | Magazine style, editorial, fashion |
| `glassmorphism` | Glass card + translucent background | Modern tech, clean feel |
| `luxury-3d` | 3D emboss + metallic texture | Luxury, premium products |
| `artistic-hand` | Handwritten + brush strokes | Artisan, creative, organic brands |
| `neon-glow` | Bold sans-serif + neon outline | Cyberpunk, gaming, youth |
| `minimal-clean` | Thin lines + whitespace | Minimal, clean brands |
| `custom` | User-defined (requires `customTypography`) | Specific brand typography |

### Recommended Style + Typography Pairings

| Product Category | Style | Typography |
|-----------------|-------|------------|
| Consumer electronics | `tech-future` | `glassmorphism` |
| Luxury goods | `magazine` | `luxury-3d` |
| Artisan / handmade | `watercolor` | `artistic-hand` |
| Gaming / youth | `cyberpunk` | `neon-glow` |
| Eco / organic | `organic-nature` | `minimal-clean` |
| Fashion / beauty | `nordic-minimal` | `editorial-grid` |
| Food / heritage | `retro-film` | `editorial-grid` |

## Examples

```bash
# Standard 5-poster detail page for a tech product
vibesku generate -t kv-image-set \
  -n "智能手表" -d "健康监测，7天续航" -b "TechWear" \
  -i watch-front.jpg watch-side.jpg \
  -o '{
    "scenes": ["kv-hero", "lifestyle", "tech-craft", "detail-01", "specs-table"],
    "style": "tech-future",
    "typography": "glassmorphism"
  }'

# Quick 3-poster set with auto style
vibesku generate -t kv-image-set \
  -n "Organic Face Cream" -i cream.jpg \
  -o '{"scenes": ["kv-hero", "lifestyle", "detail-01"]}'

# Full brand campaign set for artisan product
vibesku generate -t kv-image-set \
  -n "手工陶瓷茶具" -d "景德镇匠人手作" -b "茶道" \
  -i teapot.jpg -l logo.png \
  -o '{
    "scenes": ["kv-hero", "brand-story", "lifestyle", "detail-02", "user-review", "usage-guide"],
    "style": "watercolor",
    "typography": "artistic-hand",
    "primaryLang": "zh",
    "secondaryLang": "en"
  }'

# Premium 4K output for print material
vibesku generate -t kv-image-set \
  -n "Luxury Handbag" -i bag.jpg \
  -o '{
    "scenes": ["kv-hero", "detail-01", "detail-02"],
    "style": "magazine",
    "typography": "luxury-3d",
    "imageSize": "4K",
    "aspectRatio": "3:4"
  }'

# Gaming product with cyberpunk aesthetic
vibesku generate -t kv-image-set \
  -n "RGB Gaming Keyboard" -d "Mechanical switches, per-key RGB, hot-swappable" \
  -i keyboard.jpg \
  -o '{
    "scenes": ["kv-hero", "tech-craft", "detail-01", "detail-03", "specs-table"],
    "style": "cyberpunk",
    "typography": "neon-glow"
  }'

# English-only horizontal layout for Shopify
vibesku generate -t kv-image-set \
  -n "Minimalist Desk Lamp" -i lamp.jpg \
  -o '{
    "scenes": ["kv-hero", "lifestyle", "detail-01"],
    "aspectRatio": "16:9",
    "primaryLang": "en",
    "secondaryLang": "none"
  }'
```

## Tips

- **Billing**: Each scene = 1 poster = 1 credit (2K) or 2 credits (4K). A 5-scene set at 2K costs 5 credits.
- **Scene order**: `kv-hero` should almost always be first — it establishes the visual identity for the set.
- **Coherence**: Style and typography are applied across ALL posters, so the set looks professionally coordinated.
- **Default language**: `zh` + `en` (bilingual) — designed for Chinese e-commerce detail pages. Change `primaryLang`/`secondaryLang` for other markets.
- **Aspect ratio**: Default `9:16` for vertical detail pages (Taobao, JD.com). Use `16:9` or `3:2` for Shopify/Amazon A+ horizontal layouts.
- **Style + Typography**: Use the recommended pairings table above for best results. When in doubt, use `auto` for both.
- **Product images**: More angles = better AI understanding = more faithful product reproduction across all scenes.
