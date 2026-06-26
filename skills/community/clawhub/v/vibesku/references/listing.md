# Template: listing

**Purpose**: Generate SEO-optimized product listing copy — titles, bullet points, and descriptions tailored to specific e-commerce marketplaces.

**When to use**: User needs text content for product listings on e-commerce platforms, or general product descriptions.

**Output type**: TEXT | **Supports analysis**: No | **Cost**: 1 credit per generation

## Assets

| Role | Min | Max | Required |
|------|-----|-----|----------|
| PRODUCT (product images) | 0 | 10 | No (but improves quality) |
| LOGO (brand logo) | 0 | 1 | No |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `templateName` | string | `GENERIC` | Target marketplace format (see below) |
| `language` | string | `English` | Output language (e.g. `English`, `Chinese`, `Japanese`) |

## Template Name Options

| Template Name | Platform | Output Format | When to Use |
|---------------|----------|---------------|-------------|
| `AMAZON_LISTING` | Amazon | Title (≤200 chars) + 5 bullet points + product description | Selling on Amazon (any marketplace) |
| `TAOBAO_DETAIL` | Taobao / Tmall | Title + selling points + detailed description (Chinese commerce style) | Selling on Taobao, Tmall, or Chinese platforms |
| `SHOPIFY_DESC` | Shopify | Title + key benefits + product description (DTC brand voice) | DTC stores, independent Shopify sites |
| `GENERIC` | Any platform | Title + bullet points + description (general e-commerce) | Multi-platform, general use, or unsure |

### Platform-Specific Guidance

**AMAZON_LISTING**:
- Title follows Amazon's keyword-rich format (brand + product + key features)
- 5 bullet points focus on benefits, not just features
- Description is HTML-compatible for A+ Content
- Best paired with `language: "English"` for US/UK/DE marketplaces

**TAOBAO_DETAIL**:
- Title uses Chinese e-commerce keyword patterns
- Selling points use emotional + factual hybrid style
- Description is longer and more narrative (Chinese buyers read more)
- Best paired with `language: "Chinese"`

**SHOPIFY_DESC**:
- Title is concise and brand-forward
- Benefits focus on lifestyle value, not specifications
- Description uses storytelling and brand voice
- Best paired with `language: "English"` for DTC brands

**GENERIC**:
- Balanced format that works across platforms
- Use when listing on multiple platforms simultaneously
- Use when the target platform doesn't match the other three

## Brief Fields

The quality of generated copy depends heavily on what you provide:

| Field | CLI Flag | Impact | Guidance |
|-------|----------|--------|----------|
| `productName` | `-n` | High | Include brand name + product type + key differentiator |
| `productDetails` | `-d` | **Critical** | Include: materials, dimensions, key specs, unique selling points, target audience |
| `brandName` | `-b` | Medium | Brand name for consistent mention in copy |

**The more detail in `-d`, the better the output.** Include:
- Key specifications (size, weight, capacity, battery life, etc.)
- Materials and construction
- Unique selling points vs competitors
- Target audience / use cases
- Certifications or awards

## Examples

```bash
# Amazon listing in English
vibesku generate -t listing \
  -n "Wireless Noise-Cancelling Headphones" \
  -d "40mm drivers, ANC, 30h battery, Bluetooth 5.3, foldable design, USB-C charging, 280g, memory foam ear cushions" \
  -b "AudioTech" \
  -o '{"templateName":"AMAZON_LISTING","language":"English"}'

# Taobao listing in Chinese
vibesku generate -t listing \
  -n "无线降噪耳机" \
  -d "40mm驱动单元，主动降噪，30小时续航，蓝牙5.3，折叠设计，USB-C充电，280g，记忆海绵耳垫" \
  -b "AudioTech" \
  -o '{"templateName":"TAOBAO_DETAIL","language":"Chinese"}'

# Shopify DTC brand description
vibesku generate -t listing \
  -n "Artisan Soy Candle" \
  -d "Hand-poured, 100% natural soy wax, 50h burn time, cotton wick, essential oils, recyclable glass jar, 8oz" \
  -o '{"templateName":"SHOPIFY_DESC","language":"English"}'

# Generic multi-platform listing
vibesku generate -t listing \
  -n "Smart Water Bottle" \
  -d "Temperature display, vacuum insulated, 500ml, 304 stainless steel, keeps hot 12h/cold 24h, BPA-free" \
  -o '{"templateName":"GENERIC","language":"English"}'

# With product images (improves copy accuracy)
vibesku generate -t listing \
  -n "Ergonomic Office Chair" \
  -d "Mesh back, adjustable lumbar support, 4D armrests, 135° recline, supports up to 300lbs" \
  -i chair-front.jpg chair-side.jpg chair-detail.jpg \
  -o '{"templateName":"AMAZON_LISTING","language":"English"}'

# Japanese marketplace listing
vibesku generate -t listing \
  -n "抹茶パウダー" \
  -d "京都宇治産、有機JAS認証、石臼挽き、30g、茶道・ラテ両用" \
  -o '{"templateName":"GENERIC","language":"Japanese"}'
```

## Tips

- **`-d` is the most important input** — the richer the product details, the better the generated copy. Include specs, materials, unique features, and target audience.
- **Product images are optional but valuable** — when provided (`-i`), AI can describe visual details (color, texture, design) that you might forget to mention in `-d`.
- **This template does NOT support analysis** — unlike image templates, it does not auto-analyze uploaded photos. It relies on your text brief.
- **Cost is fixed at 1 credit** per generation regardless of output length.
- **Language affects writing style**, not just translation — `AMAZON_LISTING` + `English` produces Amazon US-style copy, while `TAOBAO_DETAIL` + `Chinese` produces native Chinese commerce writing.
- **Multi-language strategy**: Generate separate listings for each marketplace rather than translating one. Each template name is optimized for its platform's buyer expectations.
