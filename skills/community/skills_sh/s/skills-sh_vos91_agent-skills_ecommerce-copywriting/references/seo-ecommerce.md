# E-commerce SEO Copywriting

Optimize every page for search without sacrificing conversion.

## Page-Level SEO Elements

### Title Tags

**Formula:**
`[Primary Keyword] - [Secondary Keyword/Modifier] | [Brand]`

**Character limit:** 50-60 characters (Google truncates at ~60)

**Examples by page type:**

| Page Type | Formula | Example |
|-----------|---------|---------|
| Product | [Product] - [Key Attribute] \| Brand | "Leather Weekender Bag - Carry-On Size \| BrandName" |
| Category | [Category] - Shop [Modifier] \| Brand | "Men's Running Shoes - Shop Cushioned & Lightweight \| BrandName" |
| Homepage | [Brand] - [Tagline/Value Prop] | "BrandName - Premium Leather Goods Since 2015" |
| Collection | [Collection Name] - [Product Type] \| Brand | "Winter Sale - 30% Off Outerwear \| BrandName" |

**Product title tag tips:**
- Include key attributes (size, color, material) if searched
- Put most important keyword first
- Don't stuff — one primary, one secondary max
- Include brand at end (unless brand IS the keyword)

### Meta Descriptions

**Formula:**
`[Benefit/Hook]. [Feature/Proof]. [CTA]. [Trust signal].`

**Character limit:** 150-160 characters

**Examples:**

**Product:**
```
Travel in style without checking bags. Fits overhead bins on all major airlines. 
Shop now — free returns for 30 days.
```

**Category:**
```
Find your perfect running shoe. Cushioned, lightweight, and trail-ready options. 
Free shipping over €50. Shop the collection.
```

**Homepage:**
```
Premium leather goods crafted to last a lifetime. Bags, wallets, and accessories 
made in Italy. Free shipping & 2-year warranty.
```

**Tips:**
- Include primary keyword naturally
- Add a call-to-action ("Shop now", "Discover", "Browse")
- Mention unique value props (free shipping, warranty, etc.)
- Don't duplicate across pages

### H1 Tags

One H1 per page. Should match search intent.

**Product page:** Product name + key variant
- "Leather Weekender Bag — Brown / Large"

**Category page:** Category name + modifier (optional)
- "Men's Running Shoes"
- "Waterproof Hiking Boots for Every Trail"

**Homepage:** Primary value proposition
- "Premium Leather Goods Crafted to Last"

---

## Product Page SEO

### URL Structure

**Pattern:** `/category/product-name`

**Examples:**
- ✅ `/bags/leather-weekender-bag`
- ✅ `/running-shoes/mens-ultra-boost`
- ❌ `/product?id=12345`
- ❌ `/bags/leather-weekender-bag-brown-large-2024-edition`

**Tips:**
- Use hyphens, not underscores
- Keep URLs short and descriptive
- Include primary keyword
- Avoid parameters when possible
- Don't include variant info in URL (use canonical)

### Product Description SEO

**Keyword placement:**
1. First 100 words — include primary keyword naturally
2. Throughout body — use variations and synonyms
3. Subheadings — use secondary keywords
4. Alt text — describe images with keywords

**Avoid:**
- Keyword stuffing (unnatural repetition)
- Duplicate descriptions across variants
- Manufacturer descriptions (duplicate content)

**Example keyword-optimized opening:**
```
This leather weekender bag is built for travelers who refuse to check luggage. 
At 45L capacity, it fits overhead bins on all major airlines while holding 
a weekend's worth of clothes, your laptop, and essentials.
```

### Structured Data (Schema Markup)

Essential for product pages:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Leather Weekender Bag",
  "description": "Premium full-grain leather travel bag...",
  "image": "https://example.com/images/weekender-bag.jpg",
  "brand": {
    "@type": "Brand",
    "name": "BrandName"
  },
  "offers": {
    "@type": "Offer",
    "price": "249.00",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/bags/leather-weekender-bag"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

**Benefits:**
- Rich snippets in search results
- Price, availability, ratings shown
- Higher click-through rate

---

## Category Page SEO

Category pages often have more ranking potential than individual products.

### Category Description Placement

**Above products (intro):** 50-100 words
```
Shop our collection of men's running shoes. From cushioned everyday trainers 
to lightweight racing flats, find the perfect shoe for your stride.
```

**Below products (full description):** 200-400 words
- More detailed category information
- Links to subcategories
- Buying guide content
- FAQs

### Internal Linking

Category pages should link to:
- Subcategories
- Featured/bestselling products
- Related categories
- Buying guides

### Faceted Navigation SEO

Filters create URL parameters that can cause issues:
- Duplicate content
- Crawl budget waste
- Diluted page authority

**Solutions:**
- Canonical tags pointing to main category URL
- Noindex on filtered pages
- Robots.txt blocking parameters
- Use JavaScript for filtering (no URL change)

---

## Bulk Product SEO

### Meta Description Templates

Create templates per category:

**Fashion:**
```
Shop the [Product Name] in [Color]. [Key feature]. [Material] for lasting 
comfort. [Trust signal: Free shipping/returns].
```

**Electronics:**
```
[Product Name] — [Primary benefit]. [Key spec]. [Compatibility info]. 
[Trust signal]. Shop now.
```

**Food:**
```
[Product Name] from [Origin]. [Taste/quality descriptor]. [Certification if any]. 
[Trust signal]. Order today.
```

### Variation Pages

For products with multiple variants (size, color):

**Option 1: Single page with variants**
- One URL for all variants
- Canonical to self
- Best for similar variants (sizes)

**Option 2: Separate pages per variant**
- Unique content per page
- Canonical to main variant OR self
- Best for significantly different variants (colors with unique images)

**Avoid:**
- Duplicate descriptions across variant pages
- Thin content pages for every variant

---

## Technical SEO Checklist

### Crawlability
- [ ] XML sitemap includes all product pages
- [ ] Robots.txt allows crawling of important pages
- [ ] No orphan product pages (all linked from categories)
- [ ] Internal search results pages noindexed

### Indexability
- [ ] Canonical tags on all product pages
- [ ] Out-of-stock products handled (noindex or redirect)
- [ ] Pagination handled (rel=prev/next or infinite scroll)
- [ ] Hreflang for international stores

### Page Speed
- [ ] Images optimized and lazy-loaded
- [ ] Critical CSS inlined
- [ ] JavaScript deferred
- [ ] Core Web Vitals passing

### Mobile
- [ ] Mobile-friendly design
- [ ] Tap targets appropriately sized
- [ ] No horizontal scrolling
- [ ] Content not hidden behind interactions

---

## Common E-commerce SEO Mistakes

### 1. Duplicate Content
**Problem:** Same description across products/variants
**Fix:** Unique descriptions, canonical tags, noindex thin pages

### 2. Missing Product Schema
**Problem:** No rich snippets in search results
**Fix:** Implement Product schema with all required fields

### 3. Poor URL Structure
**Problem:** IDs, parameters, excessive folders
**Fix:** Clean URLs: `/category/product-name`

### 4. Thin Category Pages
**Problem:** Just a product grid, no text
**Fix:** Add intro description + expanded content below products

### 5. Ignoring Internal Linking
**Problem:** Products only linked from categories
**Fix:** Cross-link related products, use breadcrumbs, add "related products"

### 6. Not Handling Out-of-Stock
**Problem:** Indexed pages with no purchase option
**Fix:** Keep page if restocking, redirect if discontinued, show alternatives

### 7. Blocked Resources
**Problem:** CSS/JS blocked in robots.txt
**Fix:** Allow Googlebot to render pages fully

---

## SEO Content Opportunities

### Buying Guides
- "How to Choose the Right Running Shoe"
- "Leather Care Guide: Keep Your Bag Looking New"
- High-value content that links to products

### Comparison Pages
- "Trail Running Shoes vs. Road Running Shoes"
- Captures comparison keywords

### FAQ Pages
- Answer common questions
- Opportunity for FAQ schema

### User-Generated Content
- Reviews (unique content per product)
- Q&A sections
- Customer photos
