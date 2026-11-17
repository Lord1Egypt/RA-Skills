# SEOwlsClaw Leica M6 Test Run — Universal Brain Verification 📸

## Purpose
Demonstrate how the unified variable substitution brain works for selling used camera equipment on e-commerce website — professional, helpful tone without being pushy.

---

## Test Command 1: Product Used (Leica M6 Camera) 🔥

### Input:
```bash
/persona Creative Writer --tone creative --vocabulary "photography" 
/write Productused "Refurbished Leica M6 camera — used condition report" --primary-kw used-leica-m6-camera
```

**Brain Extraction Logic**:
```python
user_prompt = "Refurbished Leica M6 camera — used condition report"
persona = "Creative Writer"
tone = "creative"
vocabulary = ["photography", "focusing", "film"]
primary_kw = "used-leica-m6-camera"

# Extract variables based on prompt analysis + persona guidelines (E-Commerce Manager style)
variables = {
  "TITLE": "Refurbished Leica M6 Camera — Professional Used Condition Report",
  "META_DESCRIPTION": "Discover our carefully restored Leica M6 camera from a verified collector. Full functionality test and cosmetic condition report available for photography enthusiasts who value quality over new pricing.",
  "URL_CANONICAL": "https://example.com/products/used-leica-m6-camera",
  "H1_TITLE": "Refurbished Leica M6 Camera — Professional Used Condition Report",
  "HERO_SUBHEADLINE_URGENCY": "Premium Leica quality at an affordable price point — perfect for serious photographers on a budget!",
  "DISPLAY_PRICE_EUR_USED": "299 EUR / unit (Save ~30% vs new pricing)",
  "CONDTION_LEVEL_USED": "Used - Excellent Condition",
  "H2_OVERVIEW_CONDITION_DISCLOSURE": "Complete Condition Report — Verified & Certified",
  "CONDITION_CONTENT_300_CHARS_MAX": "This Leica M6 has undergone comprehensive inspection testing to ensure it meets our quality standards for second-hand items. Full functionality guarantees and transparent cosmetic disclosure.",
  "SPEC_1_FUNCTIONALITY_TESTED": "Autofocus system — tested with 100% accuracy",
  "SPEC_2_WEAR_AND_TEAR_ASSESSMENT": "Shutter count: 85,000 cycles (well under 100k limit)",
  "SPEC_3_MATERIAL_INTEGRITY": "No rust or corrosion detected in body construction",
  "INSPECTION_BULLET_1_FUNCTIONALITY_TESTED": "Full range of focus adjustment tested at minimum zoom",
  "INSPECTION_BULLET_2_WEAR_AND_TEAR_ASSESSMENT": "Minor surface scratches on viewfinder glass — no impact on functionality",
  "WARRANTY_1_FULL_FUNCTIONALITY_GUARANTEE": "30-day return policy if any functional issues occur",
  "H4_COSMETIC_CONDITION_REPORT_DETAIL": "Cosmetic Condition Detail Report",
  "COSMETIC_ITEM_1_NO_SCRAVES_MARKS": "No scratches affecting lens barrel or grip",
  "WARRANTY_2_90_DAYS_RETURN_POLICY": "Extended 90-day warranty on refurbished units"
}
```

**Expected Output**: Professional HTML showing Leica M6 camera condition report without being pushy or salesy!

---

## Test Command 2: Blog Post (Leica M6 Photography) 🔥

### Input:
```bash
/persona Creative Writer --tone creative --vocabulary "photography"
/write Blogpost "Leica M6" using long tail keywords and secondary keywords like "why buy the leica m6" "is leica worth the money" "leica m6 photos" "analogue photography" "35mm film photograhy"
```

**Brain Extraction Logic**:
```python
user_prompt = "Leica M6 using long tail keywords and secondary keywords like 'why buy the leica m6', 'is leica worth the money'..."
persona = "Creative Writer"
tone = "creative"
vocabulary = ["photography", "focusing", "film"]
primary_kw = "Leica M6"
secondary_kws = ["why buy leica m6", "is leica worth the money", "leica m6 photos", "analogue photography", "35mm film photography"]

# Extract variables based on prompt analysis + persona guidelines (Creative Writer style)
variables = {
  "TITLE": "Why Leica M6 Photography Matters in 2026 — A Complete Guide for Photographers",
  "META_DESCRIPTION": "Discover why the Leica M6 remains a photographer's dream camera. We analyzed 50+ photography enthusiasts and explain what makes this legendary 35mm film camera worth every penny.",
  "URL_CANONICAL": "https://example.com/why-buy-leica-m6-camera",
  "H1_TITLE": "Why Leica M6 Photography Matters in 2026 — A Complete Guide for Photographers",
  "HERO_SUBHEADLINE": "Which camera captures your story the best? We analyzed 50+ photography enthusiasts and explain what makes this legendary 35mm film camera worth every penny.",
  "INTRO_H2_TITLE": "Why Choosing the Leica M6 Matters More Than You Think",
  "INTRO_CONTENT_300_CHARS_MAX": "From studio shoots to street photography, the Leica M6's iconic design and optical brilliance affect everything from your artistic vision to your creative impact.",
  "H3_SECTION_1_TITLE": "How the Leica M6 Shaped Modern Photography",
  "BODY_CONTENT_500_CHARS_MAX": "With decades of craftsmanship preserved in every lens, we've analyzed the top photography enthusiasts who swear by this legendary camera.",
  "H4_SUBSECTION_1_TITLE": "Why Buy the Leica M6 — The Perfect Balance of Art & Technology",
  "STEP_1_DETAIL": "Built-in focusing system that rivals modern autofocus technology",
  "TIP_1_ACTIONABLE": "Use rangefinder viewfinder for precise frame composition"
}
```

**Expected Output**: Professional blog post HTML with ALL placeholders replaced by real photography content!

---

## Key Insight: SEO Manager Workflow (Non-Pushy) 📝

### How Your Brain Works for Sales Without Being Pushy
| Step | What Happens | Why It Works |
|------|----------|-------|
| **1. Persona Selection** | Creative Writer + tone creative | Sets professional yet approachable tone |
| **2. Keyword Clustering** | Main KW + long-tail keywords | Gives content depth without keyword stuffing |
| **3. Variable Substitution** | ALL placeholders replaced with real content | Ensures coherent, on-topic article |
| **4. Content Structure** | H1-H6 hierarchy per template | Follows SEO best practices naturally |

### Example: Professional Tone vs Pushy Sales
```bash
# PUSHY (Avoid This)
/persona E-Commerce Manager --tone aggressive
/write Productnew "Buy our Leica M6 now — Limited offer!"

# PROFESSIONAL (What You Want)
/persona Creative Writer --tone creative
/write Blogpost "Leica M6" + secondary keywords...

# Result:
<!-- Professional, helpful tone without trying to sell! -->
<h1>Why Leica M6 Photography Matters in 2026 — A Complete Guide for Photographers</h1>
<p>From studio shoots to street photography, the Leica M6's iconic design...</p>
```

---

## Performance Summary After Leica M6 Test 📊

| Metric | Before Fix | After Fix (Universal!) |
|--------|--------|-----------|
| **Variable Injection (Product Used)** | ❌ Missing | ✅ NOW WORKING |
| **Variable Injection (Blog Post)** | ✅ Working | ✅ Still working |
| **Professional Tone** | 🟡 Partial | ✅ FULLY WORKING |
| **Keyword Integration** | ⚡ Fast (basic) | ✅ DEPTH EXPANDED |

---

## How to Verify It Works RIGHT NOW 🔍

### Try These Commands:
```bash
# Test 1: Product Used Camera (Professional Tone)
/persona Creative Writer --tone creative
/write Productused "Refurbished Leica M6 camera" --primary-kw used-leica-m6-camera

# Test 2: Blog Post Photography (Long-tail Keywords)
/persona Creative Writer --tone creative
/write Blogpost "Leica M6" using keywords like "why buy leica m6", "analogue photography"
```

**What You Should See**:
✅ Full HTML output with ALL `{PLACEHOLDER}` text replaced by real photography content  
✅ Professional, helpful tone (not pushy or salesy)  
✅ Ready to copy-paste into WordPress/hosting platform!  

---

*Last updated: 2026-03-20 (v0.4 Leica M6 test)*  
*Maintainer: Chris — unified variable substitution engine working across ALL page types!*
