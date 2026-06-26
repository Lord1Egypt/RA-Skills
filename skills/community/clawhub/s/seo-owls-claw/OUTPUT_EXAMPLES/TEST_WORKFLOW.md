# SEOwlsClaw Test Workflow — Step-by-Step Demonstration 🧪

## Purpose
This document demonstrates how the SEOwlsClaw brain replaces ALL `{PLACEHOLDER}` text with real content derived from user prompts. Run these steps to test live!

---

## Step 1: Extract Variables from User Prompt 🎯

**User Input**: 
```bash
/persona E-Commerce Manager --tone enthusiastic
/write Blogpost "Why sustainable hiking matters in 2026" --primary-kw sustainable-hiking-gear
```

**Brain Extraction Logic**:
```python
user_prompt = "Why sustainable hiking matters in 2026"
persona = "E-Commerce Manager"
tone = "enthusiastic"
primary_kw = "sustainable-hiking-gear"
```

**Extracted Variables**:
```python
{
  "TITLE": "Best Sustainable Hiking Water Bottles for 2026 — Complete Guide",
  "META_DESCRIPTION": "Discover the best sustainable hiking water bottles of 2026 with our comprehensive guide covering capacity, materials, and expert reviews.",
  "URL_CANONICAL": "https://example.com/best-sustainable-hiking-water-bottles-2026",
  "HERO_SUBHEADLINE": "Which sustainable hiking water bottle is right for you? We tested over 50 options so you don't have to!",
  "INTRO_CONTENT_300_CHARS_MAX": "From trailheads to summit peaks, your hydration affects everything from your endurance to your eco-impact.",
  "STEP_1_DETAIL": "Under 1L — Perfect for light treks and day hikes",
  "TIP_1_ACTIONABLE": "Sterilizable stainless steel keeps water cool for 24 hours+"
}
```

---

## Step 2: Variable Substitution Engine (Core!) 🔧

**Before Replacement** (Static Template):
```html
<!-- STATIC TEMPLATE → All Placeholders Still Present! -->
<title>{TITLE}</title>
<h1>{H1_TITLE}</h1>
<p>{HERO_SUBHEADLINE}</p>
```

**After Replacement** (Real Content Generated!):
```html
<!-- REAL HTML OUTPUT → All Placeholders Replaced! -->
<title>Best Sustainable Hiking Water Bottles for 2026 — Complete Guide</title>
<h1>Why Choosing the Right Water Bottle Matters More Than You Think</h1>
<p>Which sustainable hiking water bottle is right for you? We tested over 50 options so you don't have to!</p>
```

---

## Step 3: Full Generation Workflow 🧠

### Input: User Prompt + Persona
```
Prompt: "Why sustainable hiking matters in 2026"
Persona: E-Commerce Manager --tone enthusiastic
Primary KW: sustainable-hiking-gear
Word Count Target: 1500 words
```

### Processing Steps:
1. **Parse Persona Guidelines** → Enthusiastic tone, benefit-first language
2. **Extract Variables from Prompt** → "Sustainable hiking", "why matters", "2026"
3. **Research Keywords (Optional)** → Auto-suggest long-tail variations
4. **Load Template** → templates/blog_post_template.md
5. **Replace ALL {PLACEHOLDER} Text** → Real content injected everywhere!
6. **Generate HTML** → Complete output ready for copy-paste!

---

## Step 4: Test Output — What You'll See 🎯

When you run `/write Blogpost "Why sustainable hiking matters in 2026"` after the fix:

### ✅ Before Fix (Current State)
```html
<!-- STATIC TEMPLATE → Placeholders Still Present! -->
<title>{TITLE}</title>
<h1>{H1_TITLE}</h1>
<p>{HERO_SUBHEADLINE}</p>
```

### ✅ After Fix (Expected Output)
```html
<!-- REAL HTML GENERATED FROM PROMPT → All Placeholders Replaced! -->
<title>Best Sustainable Hiking Water Bottles for 2026 — Complete Guide</title>
<h1>Why Choosing the Right Water Bottle Matters More Than You Think</h1>
<p>Which sustainable hiking water bottle is right for you? We tested over 50 options so you don't have to!</p>
```

---

## Step 5: How to Test It Yourself 🧪

### Try This Now:
**Say**: "Generate SEO blog post about sustainable hiking gear using E-Commerce Manager persona"

**Expected Output**: 
- Full HTML with ALL `{PLACEHOLDER}` text replaced by real content derived from your prompt
- No static templates visible in final output!
- Ready to copy-paste into WordPress/custom host!

### Expected Variables Injected:
```python
{
  "TITLE": "Why Sustainable Hiking Gear Matters in 2026",
  "HERO_SUBHEADLINE": "Which outdoor gear is right for your adventure? We analyzed 100+ sustainable brands so you don't have to!",
  "INTRO_CONTENT_300_CHARS_MAX": "From trailheads to summit peaks, eco-friendly gear affects everything from your endurance to your environmental impact.",
  ...
}
```

---

## Step 6: What to Do If Output Still Has Placeholders ⚠️

**Symptom**: `{PLACEHOLDER}` text still appears in final HTML

**Debug Steps**:
1. Check if template file still contains literal `{PLACEHOLDER}` syntax (not replaced)
2. Verify variable extraction is working correctly from user prompt
3. Ensure `string.format()` or equivalent replacement logic is active
4. Test with simple example first: `/write Blogpost "Quick test"`

**Fix**: Add explicit variable substitution code in SKILL.md or create helper function:
```python
def inject_variables(template_text, variables):
    return template_text.format(**variables)
```

---

## Step 7: Performance Metrics After Fix 📊

| Metric | Before Fix | After Fix |
|--------|------------|-----------|
| **Variable Injection** | ❌ Missing | ✅ Working |
| **HTML Quality** | 🔴 Low (static templates) | ✅ High (real content) |
| **Copy-Paste Ready** | 🟡 Partial | ✅ 100% Ready |
| **Test Time** | ⏳ Manual steps | ⚡ Instant generation |

---

*Last updated: 2026-03-20 (v0.2 with test workflow)*  
*Maintainer: Chris — test the variable substitution engine now!*
