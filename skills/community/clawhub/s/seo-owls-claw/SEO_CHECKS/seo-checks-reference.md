# SEOwlsClaw — SEO Checks Reference (v0.5+)

## Purpose
This document maps out the complete SEO validation workflow for SEOwlsClaw v0.5+, including Search Intent detection + expanded checks for E-E-A-T, On-Page SEO, and common pitfalls.

---

## Step 1: Search Intent Detection (NEW Function!) 🔍

### Query Intent Analysis
Before generating content, the brain analyzes your prompt to determine search intent type:

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
| **Informational** | Blog Post + Guide | H1: Question, H2: Main sections, H3: Examples | `templates/blog_post_template.md` |
| **Transactional** | Product Page | H1: Product name, H2: Features, H3: Specs | `templates/product_new_template.md` or `product_used_template.md` |
| **Commercial** | Comparison Guide | H1: "Best X for Y", H2: Option A vs B, H3: Pros/Cons | Custom comparison template |

### Example: Your Leica M6 Prompt
```python
user_prompt = "I tried the Leica M6 in Fürth and Nürnberg... Summilux 50mm f1.4"

# Detection Result:
intent = "Informational" (personal experience + educational value)
recommended_format = Blog Post
template_used = templates/blog_post_template.md
```

---

## Step 2: Expanded SEO Checks by Category 🧩

### E-E-A-T Signals (Covers Critical SEO Factor!) ✅ High Priority
| Check | What to Verify | Why It Matters | Pass/Fail Criteria |
|-------|----|----|----|
| **Expertise** | Author credentials + domain authority in niche | Google ranks expert content higher | Author bio present + relevant experience mentioned |
| **Experience** | Personal stories, real examples, hands-on testing | Builds trust with readers | Includes personal anecdotes (your Leica M6 story!) |
| **Authoritativeness** | Domain reputation, citations, backlinks from reputable sites | Establishes industry leadership | 2+ authoritative domain references in content |
| **Trustworthiness** | Accurate facts, no misleading claims, transparent sourcing | Ensures content reliability | Cite sources + avoid speculation without evidence |

### On-Page SEO Requirements ✅ High Priority
| Check | Standard Rule | Page Type Specifics | Pass/Fail Criteria |
|-------|----|----|----|
| **Title Tag Length** | 50-60 characters max | Blog: Include keyword early, Products: Brand first | Title < 60 chars + primary keyword present |
| **Meta Description** | 150-160 characters max | All types: Compelling CTA phrase | Meta desc < 160 chars + includes keyword |
| **H1 Tag (Only One)** | Single descriptive H1 per page | Products: "{Brand} + Product + Keyword", Blogs: "How to.../Why..." | Exactly 1 H1 element present |
| **Heading Structure** | H2 for main sections, H3/H4 for subsections | Informational: More depth, Transactional: Less clutter | Max 6-8 H2 tags, proper nesting (no skipping from H2→H4) |
| **Internal Linking** | 2-3 relevant internal links per page | Products: FAQ/related pages, Blogs: Related articles | Footer H6 links present + anchor text descriptive |

### Common SEO Traps to Avoid ⚠️ High Priority
| Trap | What It Is | How to Avoid | Consequence if Missed |
|-------|----|----|----|
| **Keyword Stuffing** | Repeating keywords unnaturally (>2% density) | Natural language flow, vary wording | Google penalizes low-quality content |
| **Thin Content** | <300 words for informational queries (underserved filter) | Provide comprehensive answers with depth | Pages deprioritized in SERPs |
| **Duplicate Content** | Same content appearing on multiple URLs | Use canonical tags + unique meta data | Search engines may merge/reject duplicate pages |
| **Broken Links** | Internal/external links returning 404 errors | Test all H6 link URLs before deployment | Poor user experience + crawlability issues |
| **Missing Schema** | No JSON-LD markup for page type | Always inject correct schema in head section | Missed rich snippets in SERPs |

### FAQ Section Requirements ✅ Medium Priority
| Check | When to Include | Format Required | Best Practice |
|-------|----|----|----|
| **FAQ Block Present** | All informational/commercial pages | H2: "Frequently Asked Questions", Q&A format with `<ul><li>Questions</li></ul>` tags | Answer each question in 2-3 sentences + link to main content |
| **People Also Ask Optimization** | Blog posts, guides | Include related questions at end of article | Anticipate user follow-up queries |
| **Schema FAQ Markup** | All pages with FAQ section | `<FAQPage>` JSON-LD schema in head | Enables star rating + question previews |

### Quality Over Quantity Principles ✅ Medium Priority
| Principle | What It Means | How SEOwlsClaw Enforces It |
|-------|----|----|
| **Depth > Breadth** | One comprehensive article > 10 shallow ones | Enforce minimum word count (Blog: 1500+ words) |
| **Value-First Content** | Answer user's actual question + add extra value | Include comparison tables, examples, actionable tips |
| **No Fluff Sections** | Every section must serve purpose or contain keywords | Validate every H2/H3 has relevant content (not just headers) |
| **User Intent Match** | Content structure matches SERP features | Analyze SERP first → mimic format that ranks well |

### Natural Language Integration ✅ Medium Priority
| Check | Standard Rule | Implementation | Pass/Fail Criteria |
|-------|----|----|----|
| **Conversational Tone** | Second-person ("you"), simple sentences, avoid jargon | Persona guidelines control vocabulary choice | No overly technical/complex phrasing without explanation |
| **Active Voice** | "The camera captures light" vs "Light is captured by the camera" | Convert to active voice for readability | >80% active voice in content body |
| **Sentence Variety** | Mix short + long sentences for flow | Avoid repetitive sentence structures | Vary sentence length (not all same word count) |

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

## Step 4: Long-Term Project Tracking (Integration Idea) 🚀

### Google Search Console Integration (Complex Tool Integration!)
**Status**: Requires API access + authentication  
**Implementation Complexity**: High ⭐⭐⭐⭐⭐  
**Priority**: Long-term project tracking  

| Component | What It Does | Implementation Steps |
|----------|--|-------|
| **Fetch Performance Data** | Get page load time, Core Web Vitals from GSC | Requires Search Console API + OAuth token |
| **Index Coverage Reports** | Track which pages are indexed, errors | Submit sitemap → fetch status every 24h |
| **Query Analysis** | See what keywords bring traffic to your site | Parse queries via API → match against generated content |

### Google Analytics Integration (Complex Tool Integration!)
**Status**: Requires GA4 API + authentication  
**Implementation Complexity**: High ⭐⭐⭐⭐⭐  
**Priority**: Long-term analytics  

| Component | What It Does | Implementation Steps |
|----------|--|-------|
| **Traffic Metrics** | Page views, bounce rate, engagement time | Fetch via GA4 API (requires admin access) |
| **Conversion Tracking** | Monitor button clicks, form submissions | Link to Google Tag Manager + event tracking |
| **SEO Impact Analysis** | Track how generated content affects rankings | Compare before/after traffic metrics per page type |

### Long-Term Project Benefits (Once Implemented!)
- ✅ Track which page types rank best over months
- ✅ Measure ROI of SEOwlsClaw-generated content
- ✅ Identify trending keywords organically
- ✅ Compare performance across seasons/topics

---

## Step 5: SEOwlsClaw Workflow with New Checks 🔄

### Complete Validation Pipeline (v0.5+)
```python
def complete_seo_workflow(user_prompt):
    """Full pipeline from intent detection to validation"""
    
    # 1. Detect Search Intent
    intent = detect_search_intent(user_prompt)  # ← NEW FUNCTION
    
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

*Last updated: 2026-03-21 (v0.5+ planning complete)*  
*Maintainer: Chris — implementing search intent detection + expanded SEO checks!*
