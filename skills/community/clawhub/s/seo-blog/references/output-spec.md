# Lanthome SEO Blog Output Specification

## Source Rules

Inspect the live Lanthome product page before drafting. Record only facts, ingredients, positioning, customization statements, packaging details, and image URLs visible on that page. When a fact is unclear, omit it or describe it as a buyer question.

Use cosmetic-care language such as moisture support, barrier support, daily care, comfort, formulation evaluation, sourcing, and brand positioning. Do not state or imply that a cosmetic diagnoses, treats, cures, or prevents disease. Do not invent certifications, clinical evidence, test results, regulatory approvals, minimum order quantities, lead times, formulas, ingredients, or factory capabilities.

### Efficacy Language Rules

When discussing ingredients or product effects — especially for eczema, anti-aging, SPF, clinical, healing, skin repair, inflammation, or dermatologist-tested topics — do NOT write ingredient potential as confirmed product efficacy.

**Use conservative phrasing:**
- may help support
- is commonly used for
- is designed to
- can be customized for
- subject to formulation and testing

**Never use:**
- cures, heals, clinically proven, guaranteed results, eliminates wrinkles, treats eczema

### Authority Sources

When the article covers ingredients, regulations, or medical-adjacent topics, cite 2–5 relevant authoritative sources inline or as references:
- FDA (US Food and Drug Administration)
- European Commission (cosmetic regulations)
- American Academy of Dermatology (AAD)
- PubMed (peer-reviewed studies)
- CIR (Cosmetic Ingredient Review)
- COSMOS (organic/natural cosmetic standard)
- ISO (International Organization for Standardization)

Link to the official source page, not to secondary articles.

## Output Directory and Files

Create a new directory named from the article slug. Do not overwrite an earlier article. Produce:

1. `<slug>.md` with metadata followed by the complete article.
2. `<slug>-blog-editor.html` containing an editor-ready HTML fragment.
3. `<slug>-cover.png` containing a landscape cover image.

## Metadata Contract

Put these fields at the start of the Markdown file and in the HTML comment block:

- `SEO Title`: natural English, primary keyword included, **50–65 characters**. Follow title formulas: "Private Label + Product + Manufacturer Guide" / "How to Choose a + Product + Manufacturer" / "OEM + Product + Formulation Guide".
- `Meta Description`: clear benefit and search intent, **140–160 characters**, include a call-to-action or benefit.
- `SEO Keywords`: **3–5** focused comma-separated phrases, primary keyword first. Avoid keyword overlap across articles — each article should target a distinct primary keyword.
- `Custom URL`: `https://lanthomeskincare.com/blog/<short-slug>` — keep the slug **3–5 words max**, lowercase hyphenated. Example: `balm-stick-format-comparison`, NOT `private-label-foot-nourishing-balm-stick-organic-christmas-formula-guide`.
- `Breadcrumb`: `Home > Blog > <Short Topic>` — the topic part should be **3–5 words**, concise and descriptive. Example: `Balm Stick Format Comparison`, NOT the full product name or full article title.
- `Author`: `lanthomes-elian`.

## Article Contract

- Write more than 2,000 English words in the article body; metadata and link descriptions do not count.
- Use exactly one descriptive `h1` and a logical `h2`/`h3` hierarchy. Do NOT repeat the blog title as an H1 inside the body.
- **Add a Table of Contents** at the top of the article (after introduction, before first H2) with clickable anchor links to each H2 section.
- **Article introduction (first 2–4 sentences)**: briefly state the reader's problem and the article's key conclusion upfront.
- Match commercial search intent: private label, OEM/ODM, sourcing, formulation evaluation, quality control, packaging, positioning, or brand development.
- Explain product claims conservatively (see Efficacy Language Rules above).
- Use short paragraphs (2–4 sentences each), practical lists, and clear transitions. Avoid consecutive large text blocks.
- Use tables for product specs, comparison data, and customization options.
- Link naturally to the reference product within the article.
- **Anti-template requirement**: each article must include at least 2–3 product-specific details that differ from other articles — real formula characteristics, product specs, MOQ ranges, sampling process, lead times, packaging options, formula adjustment scope, or QC processes. Do not simply repeat the same generic structure (market → formula → packaging → QC → launch) across all articles.

### Internal Links Requirement

Every article must include body-text links to:
- The reference product page
- A relevant product category page (matching the product's category per the Category → URL mapping table)
- The About Us page and Contact Us page

Plus the 4 Related Links at the end (product + category + About Us + Contact Us). Use descriptive anchor text, NOT generic text ("click here", "read more").

### Author Info Block

End every article with this author block (before CTA button, before Related Links):

```
About the Author

This article was prepared by the Lanthome skincare manufacturing team, with experience in private label formulation, packaging development, quality control, and international OEM/ODM projects.
```

## HTML Fragment Contract

Start from `assets/blog-fragment-template.html` and replace every placeholder.

- Omit `doctype`, `html`, `head`, and `body` wrappers.
- Omit scripts, stylesheets, structured-data blocks, event handlers, and `javascript:` URLs.
- Use editor-safe semantic elements and inline styles only.
- Do NOT include product images in the article body. The article is text-only.
- Include a **Table of Contents** after the introduction, using anchor links to H2 sections.
- Include a styled CTA button (`{{BUTTON_TEXT}}`) linking to the reference product URL (`{{PRODUCT_URL}}`) between the article body and the Related Links section.
- Include the **Author Info block** before the CTA button.
- Do NOT include an `h1` in the HTML body — the blog title is rendered by the CMS title field. Start with the introduction paragraph directly.
- Use `h2` for major sections and `h3` for subsections.
- End with the `Related Links` section below.
- Use short paragraphs (2–4 sentences), lists, and tables for readability.

## Related Links

Links must be **relevant to the product** — no unrelated products or categories.

### Category → URL mapping

Determine the product's category from the source page breadcrumb, then match:

| Product Category | Collection URL |
|---|---|
| Skin Care Set | https://lanthomeskincare.com/collections/skin-care-set |
| Sunscreen | https://lanthomeskincare.com/collections/sunscreen |
| Face Care | https://lanthomeskincare.com/collections/skin-care |
| Serum | https://lanthomeskincare.com/collections/serum-1 |
| Eye Care | https://lanthomeskincare.com/collections/eye-care |
| Body Care | https://lanthomeskincare.com/collections/serum |
| Foot Care | https://lanthomeskincare.com/collections/foot-care |
| Hand Care | https://lanthomeskincare.com/collections/hand-care |

### Required links (4 total, in order)

1. **Reference product** — the product the blog is about, with a one-sentence description.
2. **Product category** — the matching collection link, with descriptive anchor text (e.g., "Foot Care collection", "Face Care products").
3. **About Us** — `https://lanthomeskincare.com/pages/about-us`
4. **Contact Us** — `https://lanthomeskincare.com/pages/contact-us`

Example for a Foot Care product:

```markdown
[Private Label Foot Nourishing Balm Stick](https://lanthomeskincare.com/products/...)- Organic foot balm stick for seasonal foot care — OEM customization available.
[Foot Care collection](https://lanthomeskincare.com/collections/foot-care)- Browse private label foot care products including balm sticks, moisturizers and seasonal options.
[About Us](https://lanthomeskincare.com/pages/about-us)- Learn more about Lanthome's manufacturing capabilities and OEM/ODM services.
[Contact Us](https://lanthomeskincare.com/pages/contact-us)- Reach the Lanthome team to discuss your private label project.
```

For HTML, use one unordered list. Each item must contain one anchor followed by `- ` and its description. Do NOT include unrelated products or categories.

## Cover Image Contract

Use the `imagegen` skill to create a landscape PNG suitable for a B2B skincare blog. Use a premium, clean skincare aesthetic, soft neutral colors, and product-category cues. **The cover must display the article headline (SEO title or H1) as on-image text.** Do not add certification seals, medical symbols, before-and-after claims, unsupported product packaging, or unrelated logos.

## Completion Checks

Confirm all of the following before delivery:

- The three output files exist in a unique slug directory.
- The English article body exceeds 2,000 words.
- The SEO Title is 50–65 characters. The Meta Description is 140–160 characters.
- Keywords are 3–5 phrases, primary keyword first, with no overlap with other articles' primary keywords.
- Breadcrumb topic is 3–5 words (e.g., `Balm Stick Format Comparison`), not a full product name or article title.
- Custom URL slug is 3–5 words, lowercase hyphenated.
- Keywords, custom URL, breadcrumb, and author are present.
- The HTML is a fragment with NO `h1` (title is rendered by CMS), no product images, and no forbidden wrappers or scripts.
- A **Table of Contents** with anchor links is present after the introduction.
- An **Author Info block** is present before the CTA button.
- The article introduction gives a brief conclusion upfront (2–4 sentences).
- Paragraphs are 2–4 sentences each; lists and tables are used where appropriate.
- At least 2–3 product-specific details are included (anti-template requirement).
- At least 5 internal links are present (1 product, 1 category, 2 blog/page, 1 contact) with descriptive anchor text.
- Efficacy language is conservative (no "cures", "heals", "clinically proven").
- 2–5 authoritative sources are cited for ingredient/regulation/medical-adjacent content.
- 4 relevant links are present (product + matching category + About Us + Contact Us) with descriptive anchor text. No unrelated products or categories.
- The cover is a landscape PNG and follows the visual restrictions.
- Every factual or performance statement is supported by the source page or clearly framed as buyer guidance.

## Error Handling

- If the product page cannot be accessed, request its text or an exported page.
- If the page provides no usable online product image, report that constraint and do not invent a URL.
- If the user requests an unsupported claim, replace it with neutral cosmetic-care or sourcing language.
- If image generation is unavailable, finish the Markdown and HTML, report the missing cover, and do not create a fake image file.
