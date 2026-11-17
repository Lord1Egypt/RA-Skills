# SEOwlsClaw — SEO Checks Reference (v0.9.2)

## Purpose
This file (`SEO_CHECKS/seo-checks-reference.md`) covers the **universal audit workflow** that
applies to all page types — Search Intent confirmation, structured-data validation, and the
scoring pipeline. The rule *values* it checks against (E-E-A-T signals, on-page SEO thresholds,
common traps, FAQ requirements, quality principles, natural language rules) live in
`SEO_RULES/universal.md`.
For page-type-specific thresholds, required elements, and audit scoring, load the companion file:
> `SEO_CHECKS/page-type-specific-checks.md` — Detailed checks per page type (Productnew, Productused, Blogpost, Landingpage, FAQ, Socialphoto, Socialvideo), rule values in `SEO_RULES/<type>.md`

| File | Scope | When to Load |
|------|-------|--------------|
| `SEO_CHECKS/seo-checks-reference.md` | Universal audit workflow — all page types | Step 6, always |
| `SEO_CHECKS/page-type-specific-checks.md` | Per-type thresholds, hard fails, schema rules | Step 6, after universal checks |
| `SEO_CHECKS/seo-output-quality-checklist.md` | Pre-output quality gate | Step 6.5, before final output |
| `SEO_CHECKS/search_intent.md` | SERP lookup + intent scoring | Step 0, before everything |
| `SEO_CHECKS/schema-markup.md` | Schema.org rules + variable definitions | Step 5–6 for /writehtml |

**Load order in Step 6 from BRAIN_ARCHITECTURE.md file:**
> First run `seo-checks-reference.md` (universal audit mechanics, checked against `SEO_RULES/universal.md`)
> After universal checks pass, load `page-type-specific-checks.md` and run
> the checks for the active page type against `SEO_RULES/<type>.md`. Hard fails in that file
> block output the same way as universal hard fails. (type-specific hard fails + warnings)
> Finally walk through `seo-output-quality-checklist.md` → and only after ALL the quality checks have passed proceed to Step 6.5 from BRAIN_ARCHITECTURE.md file

---

## Related Files in SEO_CHECKS/

| File | What It Adds |
|------|-------------|
| `page-type-specific-checks.md` | Audit scoring (HARD FAIL/WARNING) per page type — rule values in SEO_RULES/<type>.md — runs after this file in Step 6 from BRAIN_ARCHITECTURE.md file |
| `seo-output-quality-checklist.md` | Final quality gate before output is delivered — Step 6.5 from BRAIN_ARCHITECTURE.md file |
| `search_intent.md` | SERP lookup and intent detection — Step 0, before any checks run |
| `schema-markup.md` | Full schema variable definitions and stacking rules — referenced during Step 5 of Variable Substitution from BRAIN_ARCHITECTURE.md file |

---

## Step 1: Search Intent Detection 🔍

### Query Intent Analysis
Before generating content, the SEOwlsClaw brain analyzes your prompt to determine search intent type:

```python
# Intent Detection Logic
def detect_search_intent(user_prompt):
    """Analyze prompt for Informational/Transactional/Commercial intent"""
    
    informational_keywords = [
        "how to", "what is", "why buy", "guide", "tutorial", 
        "explanation", "meaning of", "definition", "overview"
    ]
    
    transactional_keywords = [
        "buy", "purchase", "price", "cheap", "sale", "discount",
        "review", "comparison", "best", "top rated"
    ]
    
    commercial_keywords = [
        "vs", "compare", "alternatives", "similar to", 
        "which is better", "recommendations for"
    ]
    
    prompt_lower = user_prompt.lower()
    
    if any(kw in prompt_lower for kw in informational_keywords):
        return "Informational"
    elif any(kw in prompt_lower for kw in transactional_keywords):
        return "Transactional"
    elif any(kw in prompt_lower for kw in commercial_keywords):
        return "Commercial"
    
    # Default to Informational if unclear
    return "Informational"
```

### Intent Mapping → Content Format
| Intent Type | Recommended Format | Hierarchy Pattern | Template Used |
|----------|-----|---|---|
| **Informational** | Blog Post + Guide | H1: Question, H2: Main sections, H3: Examples | `TEMPLATES/blog_post_template.md` |
| **Transactional** | Product Page | H1: Product name, H2: Features, H3: Specs | `TEMPLATES/product_new_template.md` or `product_used_template.md` |
| **Commercial** | Comparison Guide | H1: "Best X for Y", H2: Option A vs B, H3: Pros/Cons | Custom comparison template |

### Example: Leica M6 Prompt
```python
user_prompt = "I tried the Leica M6 in Fürth and Nürnberg... Summilux 50mm f1.4"

# Detection Result:
intent = "Informational" (personal experience + educational value)
recommended_format = Blog Post
template_used = TEMPLATES/blog_post_template.md
```

---

## Step 2: Expanded SEO Checks by Category 🧩

All rule values for this step — E-E-A-T Signals, On-Page SEO Requirements, Common SEO Traps,
FAQ Section Requirements, Quality Over Quantity Principles, and Natural Language Integration —
are defined in `SEO_RULES/universal.md`. Load it and check the generated content against every
table in it before proceeding to Step 3.

---

## Step 3: Structured Data Validation (Schema Markup Checks) ✅ Critical

### JSON-LD Schema Types Required per Page Type
| Page Type | Schema Type | Required Fields | Auto-Validate Check |
|-------|----|----|----|
| **Blog Post** | `Article` | headline, description, datePublished, author | Verify all fields present + format correct |
| **Product New** | `Product` | name, description, brand, offers (priceCurrency/price) | Check price in correct currency format |
| **Product Used** | `Product` + `ConditionSpecification` | All Product fields + condition field | Validate condition level values (Used - Excellent, etc.) |
| **Landing Page** | `Event` or `Organization` | startDate, endDate, offers (for events) OR description/areaServed (org) | Detect intent → inject correct schema type |

### Schema Validation Rules
```python
# Auto-validate JSON-LD before output generation
def validate_jsonld(schema_string):
    """Check for syntax errors + completeness issues"""
    
    validation_checks = {
        "syntax_valid": True,  # Try parsing as JSON
        "required_fields_present": len(required_fields) == total_fields,
        "no_extra_spaces": schema_string.count('"') % 2 == 0,
        "valid_type_detected": schema_type in ["Product", "Article", "Event"]
    }
    
    # Fail fast if validation fails
    if not all(validation_checks.values()):
        return False, [f"Validation failed: {missing}")
    
    return True, []
```

---

## Step 4: SEOwlsClaw Workflow with New Checks 🔄

### Complete Validation Pipeline
```python
def complete_seo_workflow(user_prompt):
    """Full pipeline from intent detection to validation"""
    
    # 1. Detect Search Intent
    intent = detect_search_intent(user_prompt)  # ← NEW FUNCTION in v0.8
    
    # 2. Select Template & Generate Content
    template = get_template_by_intent(intent)
    html_output = generate_content(template, user_prompt)
    
    # 3. Validate E-E-A-T Signals
    eeat_check = check_eeat_signals(html_output)
    
    # 4. Verify On-Page SEO Requirements
    onpage_check = check_onpage_seo(html_output)
    
    # 5. Avoid Common Traps
    trap_checks = check_common_traps(html_output)
    
    # 6. Validate FAQ Section (if applicable)
    faq_check = validate_faq_section(html_output)
    
    # 7. Enforce Quality Over Quantity
    quality_check = check_quality_over_quantity(html_output)
    
    # 8. Check Natural Language Integration
    language_check = check_natural_language(html_output)
    
    # 9. Validate Schema Markup
    schema_validation = validate_jsonld(schema_string)
    
    return {
        "html_content": html_output,
        "intent_detected": intent,
        "all_checks_passed": all([
            eeat_check["passed"],
            onpage_check["passed"],
            trap_checks["no_traps_found"],
            faq_check["valid_if_applicable"],
            quality_check["meets_standards"],
            language_check["natural_language_detected"],
            schema_validation["all_valid"]
        ]),
        "recommendations": [issue for issue in all_issues] if any([
            not eeat_check["passed"],
            trap_checks["no_traps_found"],
            not quality_check["meets_standards"],
            not schema_validation["all_valid"]
        ]) else None
    }
```

---

*Last updated: 24-08-2026 (v0.9.2)*
*Adds: trimmed Step 2 to audit-workflow mechanics only — E-E-A-T, on-page SEO, traps, FAQ, quality,
and natural-language rule values now live in SEO_RULES/universal.md*
*Maintainer: Chris — implementing search intent detection + expanded SEO checks!*
