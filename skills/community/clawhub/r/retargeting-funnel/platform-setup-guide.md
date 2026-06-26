# Platform Setup Guide: Meta, Google, and TikTok Retargeting

Step-by-step configuration for retargeting pixels, events, product catalogs, and campaign structures across the three major advertising platforms.

## Meta (Facebook / Instagram)

### Pixel and Conversions API Setup

**Browser Pixel Installation:**

1. Go to Meta Events Manager > Data Sources > Add New Data Source > Web
2. Name your pixel and enter your website URL
3. Choose installation method:
   - **Shopify/WooCommerce:** Use the native integration (Settings > Sales Channels > Facebook & Instagram for Shopify)
   - **Manual:** Add the base pixel code to the `<head>` of every page
   - **Google Tag Manager:** Use the Meta Pixel template in GTM

**Required Event Configuration:**

```
Event: ViewContent
Trigger: Product detail page load
Parameters: content_ids, content_type, value, currency

Event: AddToCart
Trigger: Add-to-cart button click or AJAX cart update
Parameters: content_ids, content_type, value, currency

Event: InitiateCheckout
Trigger: Checkout page load or checkout button click
Parameters: content_ids, value, currency, num_items

Event: Purchase
Trigger: Order confirmation / thank-you page
Parameters: content_ids, value, currency, order_id
```

**Conversions API (CAPI):**
- Purpose: Server-side event tracking that supplements browser pixel data, compensating for ad blockers and iOS privacy restrictions
- Setup via: Shopify native CAPI integration, or server-side GTM with Meta's API endpoint
- Deduplication: Use `event_id` parameter on both browser pixel and CAPI events to prevent double-counting
- Target Event Match Quality score: 6.0+ (check in Events Manager > Data Sources > [Pixel] > Overview)

### Product Catalog Setup

1. Go to Commerce Manager > Catalogs > Create Catalog
2. Choose "Ecommerce" catalog type
3. Connect product feed:
   - **Shopify:** Automatic sync via Facebook & Instagram sales channel
   - **Manual feed:** Upload CSV/XML or provide a hosted feed URL
   - **Feed schedule:** Set to refresh every 4-6 hours for price/stock accuracy

**Feed quality checklist:**
- All products have unique `id` values matching ViewContent `content_ids`
- Images meet minimum 500x500px resolution
- Prices and availability are current (stale data causes ad disapprovals)
- Product titles are under 150 characters
- GTIN/MPN fields populated where applicable (improves matching)

### Campaign Structure for Retargeting

**Recommended campaign hierarchy:**

```
Campaign: [Brand] Retargeting - Top Funnel
  Objective: Traffic or Engagement
  Budget: CBO at campaign level
  Ad Set: S1 - Homepage Bouncers (30-day window)
    Audience: Custom Audience, exclusions applied
    Placements: Advantage+ (review weekly)
  Ad Set: S2 - Category Browsers (21-day window)
    Audience: Custom Audience, exclusions applied

Campaign: [Brand] Retargeting - Mid Funnel
  Objective: Sales (Advantage+ Catalog Sales)
  Budget: CBO at campaign level
  Ad Set: S3 - Product Viewers (14-day window)
    Audience: Custom Audience from ViewContent, exclusions applied
    Creative: Dynamic product ads from catalog

Campaign: [Brand] Retargeting - Bottom Funnel
  Objective: Sales (Advantage+ Catalog Sales)
  Budget: CBO at campaign level
  Ad Set: S4 - Cart Abandoners (7-day window)
    Audience: Custom Audience from AddToCart, exclusions applied
    Creative: Dynamic product ads with urgency overlay
  Ad Set: S5 - Checkout Abandoners (3-day window)
    Audience: Custom Audience from InitiateCheckout, exclusions applied
    Creative: Dynamic product ads with incentive overlay
```

**Key settings:**
- Attribution window: 7-day click, 1-day view (standard)
- Optimization: Purchase event for bottom funnel, Landing Page Views for top funnel
- Frequency cap: Set at ad set level using delivery optimization settings

## Google Ads

### Google Tag and Enhanced Conversions

**Google Tag Installation:**

1. Go to Google Ads > Tools & Settings > Conversions > New Conversion Action > Website
2. Install the Google tag (gtag.js) in the `<head>` of every page, or use GTM with the Google Ads Conversion Tracking tag

**Event configuration with gtag.js:**

```
// Product page view
gtag('event', 'view_item', {
  currency: 'USD',
  value: 29.99,
  items: [{ item_id: 'SKU123', item_name: 'Product Name' }]
});

// Add to cart
gtag('event', 'add_to_cart', {
  currency: 'USD',
  value: 29.99,
  items: [{ item_id: 'SKU123', item_name: 'Product Name', quantity: 1 }]
});

// Purchase
gtag('event', 'purchase', {
  transaction_id: 'ORDER-789',
  currency: 'USD',
  value: 59.98,
  items: [{ item_id: 'SKU123', quantity: 1 }, { item_id: 'SKU456', quantity: 1 }]
});
```

**Enhanced Conversions:**
1. Go to Tools & Settings > Conversions > Settings > Enhanced Conversions
2. Enable and choose implementation method (gtag.js, GTM, or API)
3. Pass hashed customer data (email, phone, address) with conversion events
4. This improves match rates by 5-15%, critical for retargeting audience accuracy

### Google Merchant Center and Product Feed

1. Create a Merchant Center account and link it to Google Ads
2. Upload product feed via:
   - Shopify: Google & YouTube sales channel (automatic sync)
   - Manual: Supplemental feed via Google Sheets, scheduled fetch URL, or direct upload
3. Feed must include: id, title, description, link, image_link, price, availability, brand, gtin

**Feed optimization:**
- Product titles should lead with the most searched terms
- Use `custom_label` fields (0-4) for segmenting products by margin, season, or promotion status
- Set `ads_redirect` to deep-link users back to the exact product page with UTM parameters

### Campaign Structure for Retargeting

**Performance Max (Bottom Funnel — S3, S4, S5):**

```
Campaign: [Brand] PMax Retargeting
  Goal: Sales
  Bid strategy: Target ROAS (start at current ROAS, tighten over 2 weeks)
  Audience signals:
    - Custom segment: Website visitors who added to cart (7 days)
    - Custom segment: Website visitors who viewed products (14 days)
  Asset groups:
    - Group 1: Cart/checkout abandoners (urgency-focused headlines and images)
    - Group 2: Product viewers (benefit-focused, ratings-included)
  Listing groups: All products (or filter by custom_label for high-margin items)
```

**Standard Display (Top Funnel — S1, S2):**

```
Campaign: [Brand] Display Retargeting - Awareness
  Goal: Website traffic
  Bid strategy: Maximize clicks (with CPC cap)
  Audiences:
    - Remarketing segment: All visitors, exclude product viewers and below
  Ads: Responsive display ads with brand lifestyle images
  Placements: Review and exclude low-quality placements weekly
```

**YouTube (Top Funnel — S1):**

```
Campaign: [Brand] YouTube Retargeting
  Goal: Brand awareness and reach
  Bid strategy: Target CPM
  Ad format: 15-second non-skippable bumper ads or 6-second bumpers
  Audiences: All site visitors (30 days), exclude purchasers
  Frequency cap: 3 per week per user
```

## TikTok Ads

### TikTok Pixel and Events API

**Pixel Installation:**

1. Go to TikTok Ads Manager > Assets > Events > Web Events > Set Up Web Events
2. Choose "TikTok Pixel" and select installation method:
   - **Shopify:** TikTok sales channel app (automatic)
   - **Manual:** Add pixel base code to `<head>`, then configure events
   - **GTM:** Use TikTok's GTM template

**Required events:**

```
ttq.track('ViewContent', {
  content_id: 'SKU123',
  content_type: 'product',
  value: 29.99,
  currency: 'USD'
});

ttq.track('AddToCart', {
  content_id: 'SKU123',
  content_type: 'product',
  value: 29.99,
  currency: 'USD'
});

ttq.track('InitiateCheckout', {
  value: 59.98,
  currency: 'USD'
});

ttq.track('CompletePayment', {
  content_id: 'SKU123',
  value: 59.98,
  currency: 'USD'
});
```

**Events API (Server-Side):**
- Supplement browser pixel for improved match rates
- Configure via TikTok's server-to-server integration or partner connectors
- Use the same `event_id` for deduplication between pixel and Events API

### TikTok Product Catalog

1. Go to Assets > Catalog > Create Catalog
2. Upload product feed via scheduled URL fetch or manual CSV
3. Feed requirements mirror Meta's format: id, title, description, availability, condition, price, link, image_link

### Campaign Structure for Retargeting

**Spark Ads for Top Funnel (S1, S2):**

```
Campaign: [Brand] TikTok Retargeting - Top Funnel
  Objective: Traffic
  Ad Group: S1+S2 Combined (minimum audience size consideration)
    Audience: Custom Audience from website traffic, exclude AddToCart+
    Placement: TikTok feed
    Bid: Lowest cost (auto-bid)
    Budget: Daily budget with scheduled delivery
  Ads: Spark Ads boosting organic creator content
    - Use brand's own TikTok posts or licensed creator UGC
    - Spark Ads outperform standard in-feed ads by 30-50% on engagement
```

**Collection Ads for Mid Funnel (S3):**

```
Campaign: [Brand] TikTok Retargeting - Mid Funnel
  Objective: Website conversions (ViewContent optimization)
  Ad Group: S3 - Product Viewers
    Audience: Custom Audience from ViewContent, exclude AddToCart+
  Ads: Collection Ads linking to instant gallery page
    - Hero video at top, product tiles below
    - Products pulled from catalog matching viewed categories
```

**Conversion Ads for Bottom Funnel (S4, S5):**

```
Campaign: [Brand] TikTok Retargeting - Bottom Funnel
  Objective: Website conversions (CompletePayment optimization)
  Ad Group: S4+S5 Combined
    Audience: Custom Audience from AddToCart, exclude CompletePayment
    Optimization: Value optimization (if sufficient conversion volume)
  Ads: Standard in-feed video ads
    - Show the carted product in use
    - Include price and urgency messaging in text overlay
    - CTA button: "Shop Now" linking directly to cart
```

## Cross-Platform Coordination

### Unified Audience Definitions

Maintain a master spreadsheet mapping each segment to its platform-specific audience ID:

| Segment | Meta Audience ID | Google Segment ID | TikTok Audience ID | Size | Last Updated |
|---|---|---|---|---|---|
| S1 | [ID] | [ID] | [ID] | [Size] | [Date] |
| S2 | [ID] | [ID] | [ID] | [Size] | [Date] |
| S3 | [ID] | [ID] | [ID] | [Size] | [Date] |
| S4 | [ID] | [ID] | [ID] | [Size] | [Date] |
| S5 | [ID] | [ID] | [ID] | [Size] | [Date] |

### Platform Role Assignment

Assign primary roles to avoid over-saturating users across platforms:

| Platform | Primary Role | Best Segments | Rationale |
|---|---|---|---|
| Meta | Full-funnel workhorse | S1-S5 | Largest retargeting reach, strongest DPA capabilities |
| Google | Intent capture and display reach | S3-S5 (PMax), S1 (Display/YouTube) | Search remarketing captures active shoppers; Display extends reach |
| TikTok | Social proof and discovery | S1-S3 | Strongest for video-first brand engagement; weaker for bottom-funnel conversion |

### Frequency Management Across Platforms

When running retargeting on multiple platforms, total frequency across all platforms matters:

- Target total cross-platform frequency: 8-12 impressions per day for bottom funnel, 4-6 for top funnel
- Use platform-level frequency caps that assume 40-60% audience overlap between Meta and Google
- Monitor reach vs. frequency reports weekly on each platform to detect over-saturation
- If a user is in your S4 segment on all three platforms, they could see 15+ ads per day without cross-platform caps — adjust individual platform caps accordingly
