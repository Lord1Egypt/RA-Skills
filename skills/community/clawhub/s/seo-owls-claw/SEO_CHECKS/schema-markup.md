# SEOwlsClaw — Schema Markup Reference (v0.6)

## Purpose
**Note:** This file uses JSON-LD syntax for Schema.org structured data (SEO markup). `@context`, `@type`, and related fields are standard HTML metadata — not cryptocurrency, blockchain, or financial tokens of any kind.
This file is the single source of truth for all Schema.org / JSON-LD structured data in SEOwlsClaw.
You as agent need to read this file during **Step 7 (Variable Substitution)** to know which schema type to generate, which `{PLACEHOLDER}` variables map to which schema fields, and how to inject the JSON-LD block into the output HTML.

**Why schema matters**: Rich results (star ratings, price, condition, FAQ accordion) are only possible with correct structured data. For any website and especially for e-Commerce, `Product` schema with `ItemCondition` unlocks Google Shopping condition labels and can show "Used" or "Refurbished" badges directly in search results.

---

## Master Schema Map

| Page Type | Primary Schema | Secondary Schema | Optional Add-ons |
|-----------|---------------|-----------------|-----------------|
| `Productnew` | `Product` | `Offer` | `AggregateRating`, `BreadcrumbList`, `FAQPage` |
| `Productused` | `Product` | `Offer` + `ItemCondition` | `AggregateRating`, `BreadcrumbList`, `FAQPage` |
| `Blogpost` | `Article` | `BreadcrumbList` | `FAQPage`, `ImageObject` |
| `Landingpage` | `Event` OR `Offer` | `Organization` | `FAQPage`, `BreadcrumbList` |
| `Socialphoto` | `ImageObject` | — | — |
| `Socialvideo` | `VideoObject` | — | — |

**Stacking rule**: Always inject schemas as **separate `<script>` blocks**, never merge into one. See Section 4.

---

## Section 1 — Global Variables (Site-Wide)

These variables are reused across ALL schema types. Define them once per project — they never change between pages.

| Variable | Value for ExampleName | Description |
|----------|-------------------|-------------|
| `{SCHEMA_SITE_NAME}` | `ExampleName` | Shop display name |
| `{SCHEMA_SITE_URL}` | `https://www.example.de` | Canonical root URL |
| `{SCHEMA_LOGO_URL}` | `https://www.example.de/img/logo-example.png` | Logo image (min 112x112px) |
| `{SCHEMA_PUBLISHER_NAME}` | `example` | Publisher for Article schema |
| `{SCHEMA_CURRENCY}` | `EUR` | ISO 4217 currency code |
| `{SCHEMA_LANGUAGE}` | `de-DE` | Language/locale |
| `{SCHEMA_AUTHOR_NAME}` | `ExampleAuthorName` | Default article author |
| `{SCHEMA_AUTHOR_URL}` | `https://www.example.de/ueber-uns` | Author profile page |
| `{SCHEMA_CONTACT_URL}` | `https://www.example.de/kontakt` | Contact page URL |

> **Agent note**: Update `{SCHEMA_SITE_URL}` and `{SCHEMA_LOGO_URL}` if the live domain differs. These are the only global variables that require manual confirmation before first use.
> **Agent note**: The variables `{SCHEMA_IN_LANGUAGE}`, `{SCHEMA_PRICE_CURRENCY}`, and `{SCHEMA_ADDRESS_COUNTRY}` are loaded from `LOCALE/base.md` (or the active language override file) at Step 2c. Do **not** hardcode these values in templates or schema blocks. Always use the merged locale result from `locale_vars{}`.

---

## Section 2 — JSON-LD Injection Rules

### Where to Place the Schema Block
Always inject JSON-LD inside `<head>`, after the `<meta>` tags but before the closing `</head>` tag.

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE}</title>
  <meta name="description" content="{META_DESCRIPTION}">
  <link rel="canonical" href="{URL_CANONICAL}">

  <!-- ✅ SCHEMA GOES HERE — after meta, before </head> -->
  <script type="application/ld+json">
  { ... }
  </script>

  <!-- Additional schemas as separate blocks -->
  <script type="application/ld+json">
  { ... }
  </script>
</head>
```

### Formatting Rules
- Always use `"@context": "https://schema.org"` (HTTPS, not HTTP)
- Always include `"@type"` as the first field after `@context`
- Use ISO 8601 for all dates: `"2026-05-01"` or `"2026-05-01T10:00:00+02:00"`
- Prices must be strings: `"149.00"` not `149.00`
- All URLs must be absolute (start with `https://`)
- Do NOT include `null` values — omit fields that have no data

### When to Skip Schema
- Social media posts only need `ImageObject` / `VideoObject` if the content will be embedded on a webpage. For pure platform posts, skip schema entirely.
- Never add `AggregateRating` if there are fewer than 3 real customer reviews. Google may penalize fake ratings.

---

## Section 3 — Schema: Product (Productnew)

### When to Use
Page type: `Productnew` — brand new items, NOS (New Old Stock), unopened boxed cameras.

### Variables Required

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| `name` | `{TITLE}` or `{H1_TITLE}` | Product name |
| `description` | `{DESCRIPTION_CONTENT_400_CHARS_MAX}` | Short description |
| `brand.name` | `{BRAND_NAME}` | e.g. `Leica`, `Apple`, `Sony` |
| `offers.price` | `{DISPLAY_PRICE_EUR}` | Numeric string only, e.g. `"299.00"` |
| `offers.url` | `{URL_CANONICAL}` | Product page URL |
| `image` | `{SCHEMA_IMAGE_URL}` | Main product photo URL |
| `sku` | `{SCHEMA_SKU}` | Your internal item number |
| `aggregateRating.ratingValue` | `{RATING_VALUE}` | Float, e.g. `"4.8"` |
| `aggregateRating.reviewCount` | `{RATING_COUNT}` | Integer, e.g. `"24"` |

**New variables introduced by this schema** (add to BRAIN_ARCHITECTURE.md):
- `{SCHEMA_IMAGE_URL}` — full URL of main product image
- `{SCHEMA_SKU}` — internal stock ID / article number
- `{SCHEMA_AVAILABILITY}` — see availability values below
- `{SCHEMA_CONDITION}` — for new: always `https://schema.org/NewCondition`

### Availability Values
| Shop Status | Schema Value |
|-------------|-------------|
| In stock | `https://schema.org/InStock` |
| Out of stock | `https://schema.org/OutOfStock` |
| Pre-order | `https://schema.org/PreOrder` |
| Limited availability | `https://schema.org/LimitedAvailability` |

### Full Template — Productnew

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{H1_TITLE}",
  "description": "{DESCRIPTION_CONTENT_400_CHARS_MAX}",
  "image": "{SCHEMA_IMAGE_URL}",
  "sku": "{SCHEMA_SKU}",
  "brand": {
    "@type": "Brand",
    "name": "{BRAND_NAME}"
  },
  "offers": {
    "@type": "Offer",
    "url": "{URL_CANONICAL}",
    "priceCurrency": "{SCHEMA_CURRENCY}",
    "price": "{DISPLAY_PRICE_EUR}",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "{SCHEMA_AVAILABILITY}",
    "seller": {
      "@type": "Organization",
      "name": "{SCHEMA_SITE_NAME}"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{RATING_VALUE}",
    "reviewCount": "{RATING_COUNT}",
    "bestRating": "5",
    "worstRating": "1"
  }
}
</script>
```

> **Skip `aggregateRating` block entirely** if `{RATING_COUNT}` is below 3.

### Example — Productnew

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Leica M6 TTL Silver 0.85 — Brand-new in original box",
  "description": "The Leica M6 TTL in silver with 0.85x viewfinder magnification. Brand-new in the original box, unused. A classic rangefinder camera for serious photography.",
  "image": "https://www.example.de/img/products/leica-m6-ttl-silver-0-85.jpg",
  "sku": "EXAMPLE-10042",
  "brand": {
    "@type": "Brand",
    "name": "Leica"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.de/products/leica-m6-ttl-silver",
    "priceCurrency": "EUR",
    "price": "2490.00",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "ExampleName"
    }
  }
}
</script>
```

---

## Section 4 — Schema: Product (Productused)

### When to Use
Page type: `Productused` — used, refurbished, serviced, or "for parts" defective cameras, vintage cameras, lenses, and accessories.

### The ItemCondition Map

This is the most critical section for e-Commerce shops selling brand new but also used products. Map your internal condition descriptions to the correct `schema.org/ItemCondition` value.

| Known Internal Condition | `{CONDITION_LEVEL_USED}` Value | Schema.org URL |
|-----------------------------|-------------------------------|----------------|
| New / Neu | `new` | `https://schema.org/NewCondition` |
| Mint / Wie neu | `Mint` | `https://schema.org/NewCondition` |
| Very Good+ / Sehr gut / A+ | `VeryGood` | `https://schema.org/UsedCondition` |
| Good / Gut / A | `Good` | `https://schema.org/UsedCondition` |
| Acceptable / Akzeptabel / AB / B / C | `Acceptable` | `https://schema.org/UsedCondition` |
| Very Used / Stark Gebraucht / C-D / C / D | `Acceptable` | `https://schema.org/UsedCondition` |
| Serviced / Überarbeitet / A-B | `Refurbished` | `https://schema.org/RefurbishedCondition` |
| For Parts / Für Bastler / Defekt | `ForParts` | `https://schema.org/DamagedCondition` |

**Agent logic**: When `{CONDITION_LEVEL_USED}` is extracted from the user prompt, automatically resolve `{SCHEMA_CONDITION}` using the map above.

```
Condition resolution logic:
IF CONDITION_LEVEL_USED == "New"         → SCHEMA_CONDITION = "https://schema.org/NewCondition"
IF CONDITION_LEVEL_USED == "AsNew"         → SCHEMA_CONDITION = "https://schema.org/NewCondition"
IF CONDITION_LEVEL_USED == "Mint"         → SCHEMA_CONDITION = "https://schema.org/NewCondition"
IF CONDITION_LEVEL_USED == "VeryGood"    → SCHEMA_CONDITION = "https://schema.org/UsedCondition"
IF CONDITION_LEVEL_USED == "Good"        → SCHEMA_CONDITION = "https://schema.org/UsedCondition"
IF CONDITION_LEVEL_USED == "Acceptable"  → SCHEMA_CONDITION = "https://schema.org/UsedCondition"
IF CONDITION_LEVEL_USED == "Refurbished" → SCHEMA_CONDITION = "https://schema.org/RefurbishedCondition"
IF CONDITION_LEVEL_USED == "ForParts"    → SCHEMA_CONDITION = "https://schema.org/DamagedCondition"
```

### Variables Required

Same as `Productnew`, with these changes and additions:

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| `offers.price` | `{DISPLAY_PRICE_EUR_USED}` | Used item price |
| `offers.itemCondition` | `{SCHEMA_CONDITION}` | Resolved from condition map above |
| `description` | `{CONDITION_CONTENT_300_CHARS_MAX}` | Lead with condition disclosure |

**New variables introduced by this schema**:
- `{SCHEMA_CONDITION}` — resolved URL from the condition map (never hardcoded by user)

### Full Template — Productused

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{H1_TITLE}",
  "description": "{CONDITION_CONTENT_300_CHARS_MAX}",
  "image": "{SCHEMA_IMAGE_URL}",
  "sku": "{SCHEMA_SKU}",
  "brand": {
    "@type": "Brand",
    "name": "{BRAND_NAME}"
  },
  "offers": {
    "@type": "Offer",
    "url": "{URL_CANONICAL}",
    "priceCurrency": "{SCHEMA_CURRENCY}",
    "price": "{DISPLAY_PRICE_EUR_USED}",
    "itemCondition": "{SCHEMA_CONDITION}",
    "availability": "{SCHEMA_AVAILABILITY}",
    "seller": {
      "@type": "Organization",
      "name": "{SCHEMA_SITE_NAME}"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{RATING_VALUE}",
    "reviewCount": "{RATING_COUNT}",
    "bestRating": "5",
    "worstRating": "1"
  }
}
</script>
```

### Example — Productused (Leica M6, Condition: Very Good)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Leica M6 Classic, black lacquered, Used, Condition: Very Good",
  "description": "Leica M6 Classic in black lacquer. Mechanically tested and in perfect working order; light meter calibrated. Cosmetic condition: minimal signs of use on the body; does not affect functionality.",
  "image": "https://www.example.de/img/products/leica-m6-classic-black-used.jpg",
  "sku": "EXAMPLE-10087",
  "brand": {
    "@type": "Brand",
    "name": "Leica"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.de/products/leica-m6-classic-black-used",
    "priceCurrency": "EUR",
    "price": "2290.00",
    "itemCondition": "https://schema.org/UsedCondition",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "ExampleName"
    }
  }
}
</script>
```

---

## Section 5 — Schema: Article (Blogpost)

### When to Use
Page type: `Blogpost` — all organic SEO articles, guides, product comparisons, and experience posts.

### Variables Required

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| `headline` | `{H1_TITLE}` | Must match the visible `<h1>` exactly |
| `description` | `{META_DESCRIPTION}` | Same as meta description tag |
| `image` | `{SCHEMA_IMAGE_URL}` | Hero image URL — must be ≥1200px wide |
| `author.name` | `{SCHEMA_AUTHOR_NAME}` | Default: `ExampleAuthor` |
| `author.url` | `{SCHEMA_AUTHOR_URL}` | Link to author page |
| `publisher.name` | `{SCHEMA_PUBLISHER_NAME}` | Default: `ExampleName` |
| `publisher.logo.url` | `{SCHEMA_LOGO_URL}` | Shop logo URL |
| `datePublished` | `{SCHEMA_DATE_PUBLISHED}` | ISO 8601: `2026-04-15` |
| `dateModified` | `{SCHEMA_DATE_MODIFIED}` | ISO 8601 — update on content refresh |
| `mainEntityOfPage` | `{URL_CANONICAL}` | Canonical URL of the article |

**New variables introduced by this schema**:
- `{SCHEMA_DATE_PUBLISHED}` — ISO 8601 publish date (e.g. `2026-04-15`)
- `{SCHEMA_DATE_MODIFIED}` — ISO 8601 last modified date (defaults to same as published on first write)

### Full Template — Blogpost

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{H1_TITLE}",
  "description": "{META_DESCRIPTION}",
  "image": {
    "@type": "ImageObject",
    "url": "{SCHEMA_IMAGE_URL}",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "name": "{SCHEMA_AUTHOR_NAME}",
    "url": "{SCHEMA_AUTHOR_URL}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{SCHEMA_PUBLISHER_NAME}",
    "logo": {
      "@type": "ImageObject",
      "url": "{SCHEMA_LOGO_URL}",
      "width": 200,
      "height": 60
    }
  },
  "datePublished": "{SCHEMA_DATE_PUBLISHED}",
  "dateModified": "{SCHEMA_DATE_MODIFIED}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{URL_CANONICAL}"
  }
}
</script>
```

### Example — Blogpost (Leica M6 Testimonial)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Leica M6 in Nuremberg and Fürth — My First Analog Film Outing",
  "description": "How does the Leica M6 with a 35mm Summicron perform in Nuremberg’s Old Town? A personal account of analog photography in everyday life.",
  "image": {
    "@type": "ImageObject",
    "url": "https://www.example.de/img/blog/leica-m6-nuernberg-photography.jpg",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "name": "ExampleAuthor",
    "url": "https://www.example.de/about-us"
  },
  "publisher": {
    "@type": "Organization",
    "name": "ExampleName",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.example.de/img/logo.png",
      "width": 200,
      "height": 60
    }
  },
  "datePublished": "2026-04-14",
  "dateModified": "2026-04-15",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.example.de/blog/leica-m6-nuernberg-photography"
  }
}
</script>
```

---

## Section 6 — Schema: Event + Offer (Landingpage)

### When to Use
Page type: `Landingpage` — sales campaigns, seasonal promotions, newsletter launches, limited-time offers.

**Decision rule**:
- Use `Event` schema when the landing page promotes a **time-limited sale event** with start/end dates (e.g., Black Friday, Summer Sale)
- Use `Offer` schema (inside a `Product` or standalone) when promoting a **specific product discount** with no event framing
- Use **both** when the sale is event-based AND centers on one product/collection

This is reflected in the existing `{SCHEMA_TYPE}` variable from BRAIN_ARCHITECTURE.md. Valid values: `Event`, `Offer`, `EventAndOffer`.

### Variables Required

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| `name` | `{H1_TITLE}` | Event/offer name |
| `description` | `{META_DESCRIPTION}` | Short description |
| `url` | `{URL_CANONICAL}` | Landing page URL |
| `startDate` | `{SCHEMA_OFFER_VALID_FROM}` | ISO 8601 — when sale starts |
| `endDate` | `{SCHEMA_OFFER_VALID_THROUGH}` | ISO 8601 — when sale ends |
| `offers.price` | `{PRICE_CURRENCY_PRICE}` | Sale price or "0" for free events |
| `organizer.name` | `{SCHEMA_SITE_NAME}` | ExampleName |

**New variables introduced by this schema**:
- `{SCHEMA_OFFER_VALID_FROM}` — ISO 8601 sale start date/time
- `{SCHEMA_OFFER_VALID_THROUGH}` — ISO 8601 sale end date/time

### Full Template — Landingpage (Event + Offer)

```html
<!-- EVENT SCHEMA (use when {SCHEMA_TYPE} is "Event" or "EventAndOffer") -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{H1_TITLE}",
  "description": "{META_DESCRIPTION}",
  "url": "{URL_CANONICAL}",
  "startDate": "{SCHEMA_OFFER_VALID_FROM}",
  "endDate": "{SCHEMA_OFFER_VALID_THROUGH}",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "{URL_CANONICAL}"
  },
  "organizer": {
    "@type": "Organization",
    "name": "{SCHEMA_SITE_NAME}",
    "url": "{SCHEMA_SITE_URL}"
  },
  "offers": {
    "@type": "Offer",
    "url": "{URL_CANONICAL}",
    "priceCurrency": "{SCHEMA_CURRENCY}",
    "price": "{PRICE_CURRENCY_PRICE}",
    "validFrom": "{SCHEMA_OFFER_VALID_FROM}",
    "validThrough": "{SCHEMA_OFFER_VALID_THROUGH}",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

### Example — Landingpage (Spring Camera Sale)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Photo Spring 2026 Sale — Up to 20% off analog cameras",
  "description": "Spring Specials at ExampleName in ExampleCity: select Leica, Nikon and Rolleiflex film cameras with up to 20% off. While supplies last.",
  "url": "https://www.example.de/promotions/spring-sale-2026",
  "startDate": "2026-04-15T00:00:00+02:00",
  "endDate": "2026-04-30T23:59:59+02:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://www.example.de/promotions/spring-sale-2026"
  },
  "organizer": {
    "@type": "Organization",
    "name": "ExampleName",
    "url": "https://www.example.de"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.de/promotions/spring-sale-2026",
    "priceCurrency": "EUR",
    "price": "0",
    "validFrom": "2026-04-15T00:00:00+02:00",
    "validThrough": "2026-04-30T23:59:59+02:00",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

---

## Section 7 — Schema: FAQPage (All Page Types)

### When to Use
Add to ANY page type that includes a FAQ section. The `FAQPage` schema is the #1 driver of **People Also Ask** SERP features and FAQ accordion rich results.

**Rule**: Always include at least 3 Q&A pairs. Google requires a minimum of 2, but 3–5 performs significantly better.

### Variables Required

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| First question | `{FAQ_Q1}` | Full question text |
| First answer | `{FAQ_A1}` | Full answer (can include HTML, but strip tags for schema) |
| Second question | `{FAQ_Q2}` | Full question text |
| Second answer | `{FAQ_A2}` | Full answer |
| Third question | `{FAQ_Q3}` | Full question text |
| Third answer | `{FAQ_A3}` | Full answer |

**New variables introduced by this schema** (add to BRAIN_ARCHITECTURE.md):
- `{FAQ_Q1}` through `{FAQ_Q5}` — FAQ question texts
- `{FAQ_A1}` through `{FAQ_A5}` — FAQ answer texts (plain text, no HTML tags in schema values)

### Agent Question Generation Rules

When the user's prompt does NOT supply FAQ questions, the agent auto-generates them using these patterns by page type:

| Page Type | FAQ Question Patterns |
|-----------|----------------------|
| `Productnew` | “What are the [Specs] of the [Product]?”, “Does the [Product] come with a [Warranty]?”, “What [Use Cases] is the [Product] suitable for?” |
| `Productused` | “What is the condition of [Product]?”, “Is there a return policy?”, “How does it differ from new merchandise?” |
| `Blogpost` | Derived directly from H2/H3 headings — convert headings to questions |
| `Landingpage` | “How long is the offer valid?”, “Which products are on sale?”, “How do I pay?” |

### Full Template — FAQPage

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{FAQ_Q1}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{FAQ_A1}"
      }
    },
    {
      "@type": "Question",
      "name": "{FAQ_Q2}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{FAQ_A2}"
      }
    },
    {
      "@type": "Question",
      "name": "{FAQ_Q3}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{FAQ_A3}"
      }
    }
  ]
}
</script>
```

### Example — FAQPage for a used Leica product page

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What condition is this Leica M6 Classic in?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The camera is in “Very Good” condition. It has been mechanically inspected and found to be in perfect working order, the light meter has been calibrated, and there are minimal signs of wear on the body that do not affect its functionality."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. We offer you a 14-day return policy on all used cameras. The camera must be returned in the condition it was delivered and in its original packaging."
      }
    },
    {
      "@type": "Question",
      "name": "What is the difference from new merchandise?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Used Leica M6 cameras offer the same photographic performance as new models at a significantly lower price. The Leica M6 is no longer in production—used models are often the only way to acquire this camera."
      }
    }
  ]
}
</script>
```

---

## Section 8 — Schema: BreadcrumbList (All Page Types)

### When to Use
Add `BreadcrumbList` to ALL page types except social media posts. Breadcrumbs appear directly in Google search results as a path (`ExampleSite > Leica > Leica M Series`) and improve click-through rates significantly.

### Variables Required

| Schema Field | Maps From Variable | Notes |
|-------------|-------------------|-------|
| Level 1 (Home) | `{SCHEMA_SITE_URL}` | Always the homepage |
| Level 2 (Category) | `{SCHEMA_BREADCRUMB_L2_URL}` | e.g. `/leica-cameras` |
| Level 2 name | `{SCHEMA_BREADCRUMB_L2_NAME}` | e.g. `Leica Cameras` |
| Level 3 (Page) | `{URL_CANONICAL}` | Current page URL |
| Level 3 name | `{H1_TITLE}` | Current page H1 |

**New variables introduced by this schema**:
- `{SCHEMA_BREADCRUMB_L2_URL}` — full URL of the parent category page
- `{SCHEMA_BREADCRUMB_L2_NAME}` — display name of the parent category

### Example of Standard Breadcrumb Paths

| Page Type | Breadcrumb Example |
|-----------|-------------------|
| Product (Leica) | Home > Leica Cameras > Leica M6 Classic Black |
| Product (Leica) | Home > Leica Cameras > Leica M-Series > Leica M6 Classic Black |
| Product (Nikon) | Home > Nikon Cameras > Nikon FM2 Silver |
| Product (Lenses) | Home > Lenses > Leica Summicron-M 35mm f/2 |
| Blog Article | Home > Blog > [Article Title] |
| Landing Page | Home > Sales and Discounts > [Sale Name] |

### Full Template — BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "{SCHEMA_SITE_NAME}",
      "item": "{SCHEMA_SITE_URL}"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{SCHEMA_BREADCRUMB_L2_NAME}",
      "item": "{SCHEMA_BREADCRUMB_L2_URL}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{H1_TITLE}",
      "item": "{URL_CANONICAL}"
    }
  ]
}
</script>
```

---

## Section 9 — Schema: Organization + WebSite (Site-Wide)

### When to Use
Inject **once** in the `<head>` of the homepage (`/`) and optionally on landing pages. Do NOT repeat on every single page — it adds bloat and is only needed once per site crawl.

### Purpose
- `Organization` schema: tells Google who runs the site, the logo, and contact information. Enables Knowledge Panel for your business.
- `WebSite` schema with `SearchAction`: enables the **Sitelinks Search Box** in Google results (the search bar shown beneath your site listing).

### Full Template — Site-Wide (Homepage Only)

```html
<!-- Organization Schema — inject on homepage only -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ExampleName",
  "url": "https://www.example.de",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.example.de/img/logo.png"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "availableLanguage": ["German", "French", "English"],
    "url": "https://www.example.de/contact"
  },
  "sameAs": [
    "https://www.instagram.com/exampleusername",
    "https://www.ebay.de/usr/example"
  ]
}
</script>

<!-- WebSite Schema with Search — inject on homepage only -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "ExampleName",
  "url": "https://www.example.de",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://www.example.de/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
```

> **Agent note**: Update `sameAs` URLs with actual Website or Creator social/marketplace profile links when known. Update `urlTemplate` with the actual Shop System search URL pattern.

---

## Section 10 — Schema Stacking (Combining Multiple Schemas Per Page)

**Clarification:** This section uses JSON-LD syntax (`@context`, `@type`, `<script type="application/ld+json">`) which is the W3C standard format for Schema.org SEO structured data.
These are HTML metadata tags for search engine indexing only — not cryptocurrency, blockchain tokens, or any financial operations of any kind.

### Correct Stacking Order for Schema.org SEO structured data by Page Type

| Page Type | Block 1 | Block 2 | Block 3 | Block 4 |
|-----------|---------|---------|---------|---------|
| `Productnew` | `Product` + `Offer` | `BreadcrumbList` | `FAQPage` (if FAQ section exists) | — |
| `Productused` | `Product` + `Offer` + `ItemCondition` | `BreadcrumbList` | `FAQPage` (if FAQ section exists) | — |
| `Blogpost` | `Article` | `BreadcrumbList` | `FAQPage` (if FAQ section exists) | — |
| `Landingpage` | `Event` and/or `Offer` | `BreadcrumbList` | `FAQPage` (if FAQ section exists) | — |
| `Homepage` or Brand page | `LocalBusiness` or `Organization` | `BreadcrumbList` | — | — |
| `FAQ` | `FAQPage` | `BreadcrumbList` | — | — |
| `Socialphoto` | `ImageObject` | — | — | — |
| `Socialvideo` | `VideoObject` | — | — | — |


### Rules for Stacking of Schema.org SEO structured data
1. Each schema type = its own `<script type="application/ld+json">` block. Never merge them.
2. Always place `BreadcrumbList` AFTER the primary schema (Product / Article / Event).
3. Always place `FAQPage` LAST — it is supplementary, not primary.
4. Never add `AggregateRating` to `Blogpost` — it belongs only on product pages.
5. Never add `Article` to product pages — it confuses Googlebot about content type.
6. `LocalBusiness` or `Organization` belongs on homepage and brand pages only — not on product or blog pages.


### ❌ Common Stacking Mistakes of Schema.org SEO structured data

```html
<!-- ❌ WRONG: Merging schemas into one block -->
<script type="application/ld+json">
{
  "@type": ["Product", "Article"],  ← NEVER mix @type as array
  ...
}
</script>

<!-- ✅ CORRECT: Two separate blocks -->
<script type="application/ld+json">
{ "@type": "Product", ... }
</script>
<script type="application/ld+json">
{ "@type": "BreadcrumbList", ... }
</script>
```

---

## Section 11 — Validation & Testing of Schema.org SEO structured data

### Required Validation Step
After every `/write` command that generates HTML output, the agent should confirm that schema was injected by scanning the output for `application/ld+json`.

### Validation Tools
| Tool | URL | What It Checks |
|------|-----|---------------|
| Google Rich Results Test | `https://search.google.com/test/rich-results` | Rich result eligibility + warnings |
| Schema.org Validator | `https://validator.schema.org` | Schema syntax correctness |
| Google Search Console | Enhancements report | Live crawl errors post-deployment |

### Manual Quick-Check (Before Sending Output to User)

Run this mental checklist before finalizing any output:

- [ ] `@context` is `https://schema.org` (HTTPS, not HTTP)
- [ ] All URLs are absolute (start with `https://`)
- [ ] No `{PLACEHOLDER}` text remains unreplaced in the schema block
- [ ] Prices are strings (`"149.00"` not `149.00`)
- [ ] Dates are ISO 8601 format (`2026-04-15` or `2026-04-15T10:00:00+02:00`)
- [ ] `AggregateRating` only present if `{RATING_COUNT}` ≥ 3
- [ ] `FAQPage` only present if the HTML body contains a visible FAQ section with matching Q&A text
- [ ] `ItemCondition` is a full schema.org URL, not a plain word (`"UsedCondition"` is WRONG — use `"https://schema.org/UsedCondition"`)
- [ ] No fields with empty string `""` values — omit the field entirely if no data

### Most Common Schema Errors for Vintage Camera Shops

| Error | Cause | Fix |
|-------|-------|-----|
| `ItemCondition` value rejected | Using short values like `"used"` instead of full URL | Always use `"https://schema.org/UsedCondition"` |
| `AggregateRating` flagged | Rating added without real reviews | Remove block until real reviews exist |
| Missing `priceCurrency` | Forgetting EUR with price | Always pair `price` + `priceCurrency` |
| `headline` too long | H1 over 110 characters in Article schema | Shorten `{H1_TITLE}` to max 110 chars for blog posts |
| `dateModified` missing | Only `datePublished` filled | Always include both — default `dateModified` to same date on first publish |


---

*Last updated: 2026-04-04 (v0.6)*
*Maintainer: Chris — schema-markup.md is part of SEOwlsClaw SEO_CHECKS module*
