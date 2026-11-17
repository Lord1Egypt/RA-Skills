---
name: generating-lanthome-seo-blogs
description: Use when creating English SEO blog content for Lanthome from a lanthomeskincare.com product URL, including Markdown articles, blog-editor HTML fragments, SEO metadata, internal links, and cover images.
---

# Generating Lanthome SEO Blogs

## Overview

Create a complete Lanthome B2B skincare SEO package from one product page. Keep every claim traceable to the source page and deliver files that are ready for editorial review.

## Content Direction Rotation (8-direction cycle)

To avoid repetitive content, each blog rotates through 8 content directions. Determine which direction to use by counting the number of articles already generated (from blog-generation-history.json used_product_urls length) and applying modulo 8:

| Index | Direction | Title Formula | Core Content Focus |
|---|---|---|---|
| 0 | Selection Decision | Should You Launch [Product]? Market Size & Margin Analysis | Market size, profit margin, competition, entry barriers |
| 1 | Ingredient Science | [Ingredient] in Skincare: What Brands Need to Know | Ingredient mechanism, regulation limits, concentration, compatibility |
| 2 | Supplier Comparison | How to Evaluate [Product] Manufacturers: 7-Point Checklist | Evaluation dimensions (certs, MOQ, sampling, lead time, stability, comms, compliance) |
| 3 | Formulation Deep-Dive | [Product] Formulation Guide: Actives, pH & Stability | Active selection logic, pH range, preservative system, stability testing |
| 4 | Packaging & Compliance | [Product] Packaging & Labeling: EU/US/FDA Requirements | Label regulations, packaging materials, shipping restrictions, eco-packaging |
| 5 | Cost & Pricing | [Product] OEM Cost Breakdown: MOQ, Unit Price & Margin | Cost structure (ingredients + packaging + labor + certification + logistics), MOQ pricing tiers |
| 6 | Trend & Seasonal | 2026 Skincare Trends: What to Source for [Product Category] | K-beauty trends, seasonal positioning, social media data |
| 7 | Launch Playbook | From Concept to Shelf: Launching a [Product] in 90 Days | Timeline: selection → sampling → revision → production → QC → logistics → launch |

Each direction produces structurally distinct content — different H2 sections, different tables, different FAQ questions. Do NOT use the same H2 structure across directions.

## Workflow

1. Validate that the source is a `lanthomeskincare.com` product URL and inspect the live page.
2. Extract supported product facts and existing online product image URLs.
3. Read blog-generation-history.json to count used_product_urls length. Calculate `direction_index = length % 8`. Use the matching direction from the rotation table above.
4. Choose a buyer-oriented OEM/private-label primary keyword matching the selected direction. Ensure the primary keyword does NOT overlap with other articles' primary keywords.
5. Read `references/output-spec.md` completely, then draft the metadata and English article following these rules:
   - SEO Title: 50–65 characters, follow the title formula from the selected direction.
   - Meta Description: 140–160 characters with benefit + CTA.
   - SEO Keywords: 3–5 phrases, no keyword overlap across articles.
   - Breadcrumb: `Home > Blog > Article Topic` (no repetition).
   - Introduction: 2–4 sentences stating reader's problem and key conclusion upfront.
   - Table of Contents after introduction with clickable anchor links to each H2.
   - Short paragraphs (2–4 sentences), lists, and tables.
   - At least 2–3 product-specific details (anti-template requirement).
   - Conservative efficacy language (no "cures", "heals", "clinically proven").
   - 2–5 authoritative sources cited for ingredient/regulation content.
   - At least 5 internal links with descriptive anchor text.
   - Author info block before CTA button.
   - H2 sections MUST match the selected direction's content focus, NOT the generic "Market → Formula → Packaging → QC → Launch" structure.
6. Build the editor-ready fragment from `assets/blog-fragment-template.html` — include TOC, author block, and CTA button.
7. Use the `imagegen` skill to create the landscape PNG cover. **The cover must include the article headline text** (SEO title or H1) overlaid on the image.
7. Run every completion check in the reference before reporting the files.

## Inputs

- Require one Lanthome product URL.
- Accept an optional primary keyword, article angle, or additional internal links.
- If the page is inaccessible, request product-page content or an export instead of guessing.

## Output Files

Create a unique slug-based directory containing:

- `<slug>.md`
- `<slug>-blog-editor.html`
- `<slug>-cover.png`

The article body must exceed 2,000 English words. Include the author `lanthomes-elian`, related links matching the product's category (product + relevant category + About Us + Contact Us), SEO metadata, custom URL, and breadcrumb.

## Source and Safety Rules

Use only facts supported by the live product page. Use cosmetic, buyer-oriented language. Do not invent medical efficacy, certifications, regulatory status, test results, quantities, lead times, ingredients, or manufacturing capabilities.

## Completion

Return the three file paths and a short validation summary. Generate files only: do not access UEESHOP, fill publishing forms, save drafts, or publish.

## UEESHOP Blog Editor Injection (for automation tasks)

The UEESHOP blog editor uses **TinyMCE in iframe mode** (`Content_ifr`). Setting `textarea.value` does NOT persist — TinyMCE reads from its own internal model on save. The source code modal approach also fails because the modal's OK button click times out.

**Correct injection method — use TinyMCE API + triggerSave:**

```js
(function(){
  var html = `...FULL HTML BODY...`;
  var ed = tinymce.get('Content');
  if (!ed) ed = tinymce.activeEditor;
  if (!ed) return 'No TinyMCE editor found';
  ed.setContent(html);
  ed.save();
  tinymce.triggerSave();
  var ta = document.getElementById('Content');
  return 'Content set. TinyMCE=' + ed.getContent().length + ' | Textarea=' + (ta ? ta.value.length : 'no ta');
})()
```

**CRITICAL:** `ed.setContent()` alone does NOT persist on form submit. TinyMCE keeps content in its own iframe model and does NOT auto-sync to the hidden textarea. MUST call `ed.save()` AND `tinymce.triggerSave()` after `setContent`.

**MANDATORY verification — run a SECOND console call after injection:**
```js
(function(){
  var ed = tinymce.get('Content');
  var len = ed ? ed.getContent().length : 0;
  if (len < 500) return 'WARNING: Content length = ' + len + ' — retry injection!';
  return 'VERIFIED: Content length = ' + len;
})()
```
If content < 500 chars: retry injection. Do NOT save until verified.

**Post-save verification — reopen the draft and confirm content persisted:**
```js
(function(){
  var ed = tinymce.get('Content');
  var len = ed ? ed.getContent().length : 0;
  return len > 500 ? 'PERSISTED: ' + len + ' chars' : 'EMPTY: body not saved!';
})()
```
If EMPTY after save: content was lost during save — re-inject and re-save.

**Do NOT use:** `textarea.value` alone, source code modal, or `setContent` without `triggerSave`.

**TinyMCE editor IDs on this page:** `Content` (main body), `MobileDescription` (mobile description). Always target `Content` for the article body.

**SEO Keywords:** Do NOT fill the SEO keywords field in the UEESHOP form. Keywords are generated for the .md metadata only.
