# SEOwlsClaw — Do's & Don'ts per Page Type (v0.1)

## Purpose
This file defines the explicit rules for SEO quality checks applied after content generation. Use `/checks <url>` to run these against any generated page.

---

## 1. Landing Pages (Sale/Newsletter Campaigns)

### ✅ Do's
- **Title tag**: Include primary keyword + urgency ("20% off Sale", "Limited Offer")
- **Meta description**: Max 160 chars with CTA ("Shop now!")
- **H1 tag**: Must be descriptive + keyword-focused ("Exclusive Summer Sale: Electronics Discount")
- **Scarcity language**: Include "limited", "only X left", "starting today" phrases
- **CTA button**: High contrast, visible above fold with text "Shop Now" or "Get Deal"
- **Social proof**: Add testimonials + ratings section (H4/H5 headers)
- **Internal links**: Footer H6 links to FAQ + related product pages

### ❌ Don'ts
- **Title tag**: Do not exceed 60 chars (truncation hurts CTR)
- **Keyword stuffing**: Avoid repeating keywords in H2-H3 tags
- **Thin content**: Minimum 500 words required for conversion focus
- **Missing schema**: No JSON-LD Event/Offer markup = no rich snippets
- **CTA placement**: Do not bury CTA below fold (visibility reduces conversions)

---

## 2. Blog Posts (Organic SEO Articles)

### ✅ Do's
- **Title tag**: Question or "How to" format + primary keyword ("Best Hiking Water Bottles 2026")
- **Meta description**: Answer user intent in first 25 words
- **H1 tag**: Single descriptive title (no numbers unless article is listicle)
- **Subheadings**: Use H2 main sections, H3 subsections, H4 examples/steps
- **Word count target**: 1500+ words for competitive queries
- **Internal linking**: Related articles section with anchor-text links (H6 footer)
- **Schema markup**: Article schema + author + datePublished

### ❌ Don'ts
- **Title tag**: Do not include year unless query specifically mentions it ("2026 best...")
- **Keyword stuffing**: Avoid >2% keyword density in body text
- **Missing alt text**: Images without descriptive alt text = accessibility violation
- **Thin content**: <300 words fails Google's minimum threshold
- **No TOC (Table of Contents)**: Links improve navigation + dwell time metrics

---

## 3. Product New Pages

### ✅ Do's
- **Title tag**: Brand + product name + key feature ("EcoFriendly Water Bottle | Sustainable")
- **Meta description**: Benefit-driven ("Lifetime warranty, leak-proof design for your adventures")
- **H1 tag**: Descriptive title + keyword ("Brand Name Water Bottle: Sustainable Hiking Gear")
- **Technical specs**: dl/dl elements with dt/dd labels + unit measurements
- **Comparison table**: New version vs. previous model or competitor comparison
- **AggregateRating schema**: Star ratings with rating count for rich snippets
- **Internal links**: Related products + FAQ/tech support pages (H6 footer)

### ❌ Don'ts
- **Title tag**: Do not use generic "Buy Now" titles
- **Keyword stuffing**: Avoid repeating product features in H2-H3 tags
- **Missing condition field**: For new products, specify "Pristine/New Condition" in schema
- **No warranty/guarantee section**: Trust signals required for conversion
- **Hidden specs**: Do not bury technical details in image-only alt text

---

## 4. Product Used Pages

### ✅ Do's
- **Title tag**: Brand + product name + "Used/Refurbished" keyword ("EcoWater Bottle | Used Condition")
- **Meta description**: Value proposition vs. new pricing ("Save 30% on tested refurbished items")
- **H1 tag**: Descriptive title with condition clarity ("Brand Name Water Bottle — Certified Refurbished")
- **Condition report**: Detailed H3/H4 sections (cosmetic wear, functionality test)
- **Inspection bullets**: List of functional/structural tests performed
- **Warranty/guarantee section**: Return policy + 30-day guarantee bullet points
- **Schema markup**: ConditionSpecification field in JSON-LD

### ❌ Don'ts
- **Title tag**: Do not use "Brand New" language for used products (trust violation)
- **Keyword stuffing**: Avoid repeating "used/second-hand" excessively
- **Missing condition disclosure**: No transparency = no trust signal
- **No value proposition**: Must show savings vs. new pricing explicitly
- **Hidden specs**: Do not hide functionality test results in body text

---

## 5. Social Photo Posts

### ✅ Do's
- **Title tag**: Short, keyword-rich ("Sustainable Water Bottle | EcoFriendly Gear")
- **Meta description**: Alt text < 120 chars describing visual + product name
- **Alt text element**: Image alt attribute present (critical for accessibility + image SEO)
- **Hashtags**: Platform-specific (#brand, #hashtag_primary, #hashtag_trend)
- **Link integration**: Descriptive anchor text linking to product page
- **Visual SEO**: Alt text matches image content description

### ❌ Don'ts
- **Missing alt text**: Critical accessibility violation + missed image traffic
- **Keyword stuffing in hashtags**: >5 hashtags reduces engagement + spam signal
- **Generic title tags**: "Cool Product Photo" fails search intent
- **No brand mention**: Do not omit brand name from description/tagline
- **Hidden CTA link**: Anchor text must be descriptive ("Shop Brand Name now")

---

## 6. Social Video Posts (YouTube/TikTok)

### ✅ Do's
- **Title tag**: Optimized for search + YouTube algorithm ("Best Hiking Water Bottles 2026 | Review")
- **Meta description**: First 200 chars must include primary keyword + hook
- **VideoObject schema**: thumbnailUrl + contentUrl + uploadDate elements present
- **Transcript timestamps**: Accessibility + search indexing benefits
- **Alt text/video description**: Voiceover alt text < 100 chars describing key scenes
- **Internal linking**: Link to product page with descriptive anchor

### ❌ Don'ts
- **Generic title tags**: "Video Review" fails search intent
- **Missing thumbnail in schema**: Critical for YouTube optimization
- **Keyword stuffing in description**: >2% density = spam signal
- **No clear CTA link**: Do not bury link in video description (requires click)
- **Missing transcript alt text**: Accessibility violation + missed search indexing

---

## Quick Reference: Run `/checks` Against Generated Page

**Example Command**:
```bash
/checks https://yourdomain.com/summer-sale-landing
```

**Expected Output**:
```
SEOwlsClaw — SEO Checks Report (v0.1)
Date: 2026-03-20 | Type: Landingpage

✅ Title tag < 60 chars (passed)
✅ Meta description < 160 chars (passed)
✅ H1 tag exists + unique (passed)
✅ Canonical URL present (passed)
✅ Schema.org Event/Offer JSON-LD (passed)
✅ Alt text on images (passed)
❌ Keyword density > 2% (failed)

Issues Found: 1 | Pass Rate: 95%

Recommendation: Reduce keyword repetition in H2-H3 tags
```

---

*Last updated: 2026-03-20 (v0.1 initial build)*  
*Maintainer: Chris — explicit do/don't rules per page type for quality assurance*
