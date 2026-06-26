# Product Descriptions Deep-Dive

Templates and patterns for every product type.

## Universal Structure

Every product description follows this skeleton:

```
[HOOK] — Stop the scroll (1 sentence)
[BENEFIT BRIDGE] — Connect to customer need (1-2 sentences)
[PROOF] — Why they should believe you (specs, materials, process)
[IMAGINE] — Paint ownership picture (sensory language)
[CTA CONTEXT] — Reason to act now
```

## Templates by Category

### Fashion & Apparel

**Template:**
```
[Hook about how it makes you feel/look]

[Fit & style description — who it's for, when to wear it]

[Material story — what it's made of and why that matters]

Key details:
• Fit: [Relaxed/Slim/Regular] — [size guidance]
• Material: [Fabric composition]
• Care: [Washing instructions]
• Made in: [Origin if relevant]

[Optional: Styling suggestion]
```

**Example — T-Shirt:**
```
The shirt you'll reach for every morning.

Designed for the guy who wants to look put-together without trying too hard. 
The relaxed fit sits just right — not baggy, not tight. Works with jeans, 
chinos, or your favorite shorts.

Made from 100% organic cotton that actually gets softer with each wash. 
No pilling, no fading, no regrets.

Key details:
• Fit: Relaxed — size up if you prefer oversized
• Material: 180gsm organic cotton, pre-shrunk
• Care: Machine wash cold, tumble dry low
• Made in: Portugal

Style tip: Tuck the front, leave the back — instant effortless cool.
```

### Electronics & Tech

**Template:**
```
[Problem/solution hook]

[Primary benefit — what it does for you]

[How it works — simplified tech explanation]

Specs:
• [Key spec 1]: [Value] — [Why it matters]
• [Key spec 2]: [Value] — [Why it matters]
• [Key spec 3]: [Value] — [Why it matters]

What's in the box:
• [Item 1]
• [Item 2]

Compatibility: [Devices/systems it works with]
```

**Example — Wireless Earbuds:**
```
Finally, earbuds that don't die mid-commute.

8 hours of playback on a single charge, plus 32 more from the case. 
That's a full week of commutes, workouts, and calls without hunting for a charger.

Active noise cancellation adapts to your environment — full isolation 
on the train, transparency mode when you need to hear your coffee order.

Specs:
• Battery: 8hrs playback, 40hrs total with case — outlasts your longest day
• ANC: Adaptive with transparency mode — your audio, your way
• Drivers: 11mm custom — rich bass without muddy mids
• Water resistance: IPX4 — sweat and rain won't stop you

What's in the box:
• Earbuds + charging case
• 3 ear tip sizes (S/M/L)
• USB-C cable
• Quick start guide

Works with: iOS 14+, Android 8+, Windows, Mac
```

### Food & Beverages

**Template:**
```
[Sensory hook — taste, aroma, experience]

[Story — origin, maker, process]

[Tasting notes or serving suggestion]

Details:
• [Size/quantity]
• [Ingredients highlights]
• [Dietary info: Vegan/GF/Organic/etc.]
• [Storage/shelf life]
```

**Example — Coffee:**
```
Wake up to chocolate and citrus in every cup.

Single-origin beans from a family farm in Ethiopia's Yirgacheffe region. 
Grown at 2,000m altitude where cool nights develop complex flavors.

Medium roast brings out notes of dark chocolate, orange zest, and a 
honey-like sweetness. Best as pour-over or Aeropress — but honestly, 
it makes a damn good espresso too.

Details:
• 250g whole bean (grind fresh for best results)
• Roasted within 7 days of shipping
• Organic, fair trade certified
• Best within 4 weeks of roast date
```

### Home & Furniture

**Template:**
```
[Lifestyle hook — how it transforms a space]

[Design story — inspiration, aesthetic]

[Practical details — dimensions, materials, durability]

Specifications:
• Dimensions: [L x W x H]
• Materials: [Primary materials]
• Weight capacity: [If applicable]
• Assembly: [Required/not required, time estimate]
• Care: [Cleaning/maintenance]
```

### Beauty & Skincare

**Template:**
```
[Result-focused hook]

[Who it's for — skin type, concern]

[How to use — ritual, routine placement]

Key ingredients:
• [Ingredient 1]: [What it does]
• [Ingredient 2]: [What it does]

Details:
• Size: [ml/oz]
• Skin types: [Oily/Dry/All/Sensitive]
• Free from: [Parabens/Sulfates/etc. if relevant]
• Scent: [Description or "fragrance-free"]
```

### B2B / Professional Products

**Template:**
```
[Business outcome hook — ROI, efficiency, problem solved]

[Use case description — who uses it, when, how]

[Proof points — case studies, metrics, certifications]

Specifications:
• [Technical specs relevant to procurement]
• [Compliance/certifications]
• [Integration/compatibility]

Includes:
• [What's included in purchase]
• [Support/warranty info]
```

## Bulk Description System

When writing 50+ descriptions, use a modular system:

### Step 1: Create Category Templates
Define the structure for each product category (see templates above).

### Step 2: Build Variation Banks

**Opening hooks (rotate to avoid repetition):**
```
Fashion:
- "The [item] you'll wear on repeat."
- "Effortlessly [adjective] from [occasion] to [occasion]."
- "Finally, a [item] that [solves common problem]."
- "Meet your new everyday [item]."
- "Designed for [lifestyle/activity] without sacrificing style."

Electronics:
- "Stop [pain point]. Start [benefit]."
- "[Benefit] without the [common tradeoff]."
- "Built for [user type] who demand [quality]."
- "The [product] that keeps up with [lifestyle]."

Food:
- "Taste [origin/region] in every bite."
- "For [moment/occasion] that deserve better than [inferior option]."
- "When only [quality descriptor] will do."
```

### Step 3: Define Attribute Patterns

For each attribute type, create benefit-focused phrasings:

**Materials:**
- Cotton → "Breathable comfort that lasts"
- Leather → "Ages beautifully with every wear"
- Recycled polyester → "Sustainability without compromising performance"

**Features:**
- Waterproof → "Rain or shine, you're covered"
- Wireless → "No cables, no limits"
- Adjustable → "Your fit, your way"

### Step 4: Batch Process

1. Export product data (CSV/JSON)
2. Apply templates programmatically
3. Human review for quality and brand voice
4. Optimize top 20% manually (bestsellers, high-margin items)

## Length Guidelines

| Product Type | Ideal Length | When to Go Longer |
|--------------|--------------|-------------------|
| Basic commodity | 50-100 words | Never |
| Standard product | 100-200 words | Complex features |
| Premium/luxury | 200-400 words | Story-driven brands |
| Technical/B2B | 200-500 words | Complex specs |
| High-consideration | 300-600 words | Expensive items |

## Common Mistakes

### ❌ Starting with the brand name
"BrandX's Premium Widget is made with..."
**Fix:** Start with customer benefit, not brand ego.

### ❌ Listing features without benefits
"Features: Bluetooth 5.0, 40mm drivers, 300mAh battery"
**Fix:** Each spec needs a "which means..." translation.

### ❌ Generic superlatives
"The best quality materials"
**Fix:** Be specific: "Full-grain leather from Italian tanneries"

### ❌ Wall of text
Long paragraphs without structure.
**Fix:** Use bullets, headers, bold key phrases.

### ❌ Forgetting mobile
Descriptions that look fine on desktop but break on phone.
**Fix:** Test on mobile, keep paragraphs to 2-3 lines.

### ❌ Missing the CTA context
Description ends without reason to buy now.
**Fix:** Add urgency, scarcity, or next-step clarity.
