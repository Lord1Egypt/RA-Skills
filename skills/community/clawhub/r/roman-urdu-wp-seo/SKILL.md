---
name: roman-urdu-wp-seo
description: Optimize WordPress content for Roman Urdu/Hinglish search intent with keyword variants, blended meta tags, image alt-text guidance, and technical SEO checks for Pakistani and South Asian audiences.
metadata:
  triggers:
    - roman urdu seo
    - wordpress seo pakistan
    - hinglish keywords
    - urdu content optimization
    - desi audience seo
  version: 1.0.0
  homepage: https://github.com/byte-wave/roman-urdu-wp-seo
---

# Roman Urdu WordPress SEO Optimizer

## Overview

Use this skill to optimize WordPress posts and pages for audiences who search in English, Roman Urdu, or a natural mix of both. Keep the **English keyword core** discoverable while adding authentic South Asian phrasing to keyword ideas, metadata, headings, image alt-text, and search-intent analysis.

This skill is designed around practical WordPress publishing experience from **Byte Wave, Lahore, Pakistan**. It supports editorial SEO; it does not replace search-console data, keyword-volume tools, editorial judgment, or a final human review by a native speaker.

## Workflow Decision Tree

1. **Confirm the platform.** Apply this workflow when the target is WordPress or a WordPress-compatible SEO workflow. If the request is for Shopify, Webflow, a static site, or generic SEO without WordPress context, do not activate this skill unless the user explicitly asks for a WordPress adaptation.
2. **Check the audience.** Determine whether the intended readers are in Pakistan, India, or another South Asian market where Roman Urdu/Hinglish searches are plausible. Ask one concise clarifying question if the audience is unknown.
3. **Classify the request.**
   - For keyword research, read `references/roman-urdu-keyword-patterns.md` and use `scripts/keyword_expander.py`.
   - For metadata, use `scripts/meta_tag_generator.py` and then edit for accuracy, brand voice, and SERP fit.
   - For a full post audit, read `references/wordpress-seo-checklist.md`.
   - For wording, localization, or code-mixing decisions, read `references/code-mixing-guide.md`.
4. **Run the optimization workflow** below and clearly label assumptions.
5. **Return an implementation-ready result** with keyword variants, title, meta description, slug recommendation, headings, alt-text suggestions, internal-link ideas, schema guidance, and a QA checklist.

## Full Optimization Workflow

### 1. Establish search intent and audience

Record the topic, primary English keyword, location, language preference, reader sophistication, and desired action. Decide whether Roman Urdu belongs in the search layer. Use it when it reflects how the audience actually searches; do not add it merely because the site is based in South Asia.

Separate informational, commercial-investigation, transactional, and navigational intent. Preserve the user's actual intent when adding Roman Urdu variants. For example, `best mobile under 30000` and `30 hazar ke andar best mobile` can represent the same commercial investigation, while `mobile kaise reset karein` is a how-to query.

### 2. Expand the English keyword

Start with the English keyword supplied by the user or extracted from the post. Generate **two to three** useful Roman Urdu or mixed variants. Include, where natural:

- A direct transliteration, such as `ghar se online earning` → `ghar baithe online paisa kamana`.
- A common desi phrasing, such as `best laptop for students` → `students ke liye best laptop`.
- A local modifier, such as `in Pakistan`, `Lahore`, `under 30000`, `2026`, or `with PTA approval`, only when it matches the brief.

Use `scripts/keyword_expander.py` for a deterministic first pass. Treat its output as suggestions, not as measured search volume. Remove awkward, ambiguous, repetitive, or culturally unnatural variants.

### 3. Produce blended metadata

Keep the primary English keyword or its exact close variant near the beginning of the title where possible. Add one concise Roman Urdu/Hinglish phrase that clarifies the reader benefit. Keep the title readable; never concatenate variants as a keyword list.

Write a meta description that explains the value of the page and uses one natural mixed-language phrase. Avoid unsupported claims, excessive punctuation, fake urgency, and keyword stuffing. Use `scripts/meta_tag_generator.py` for draft generation, then manually edit the result.

Recommended output fields:

| Field | Requirement |
| --- | --- |
| SEO title | English keyword core plus a natural Roman Urdu/Hinglish benefit; target roughly 50–60 characters when practical. |
| Meta description | Clear benefit and one mixed-language phrase; target roughly 140–160 characters when practical. |
| Slug | Short, lowercase, hyphenated, and stable; prefer the English keyword core unless the site's established convention says otherwise. |
| Focus keyword | One primary English keyword; list Roman Urdu variants separately as supporting terms. |
| Search intent | State the intent and audience rather than guessing volume. |

Character targets are editorial heuristics, not guarantees of how Google will display a snippet. Never truncate a meaningful word solely to hit a target.

### 4. Audit WordPress implementation

Apply `references/wordpress-seo-checklist.md` to inspect the permalink, indexability, canonical, XML sitemap, robots directives, headings, internal links, images, schema, performance, and mobile presentation. Check compatibility with **Yoast SEO** and **Rank Math** without assuming both plugins are installed. Mention where the editor must verify a setting in the active plugin.

For every important image, suggest descriptive alt-text. Use Roman Urdu in alt-text only when it accurately describes the image and is useful to the intended audience; never use alt-text as a keyword dump. Do not put important text only inside images.

### 5. Refine content without forcing translation

Use `references/code-mixing-guide.md` to judge natural placement, register, spelling variants, and code-switching. Make headings and body copy clear for the actual reader. Keep the original language of the article unless the user explicitly asks for a full translation.

**Do not forcibly translate English content into Roman Urdu.** By default, use Roman Urdu/Hinglish only for SEO metadata, keyword suggestions, example headings, alt-text suggestions, and short localization notes. Translate the full article only when the user explicitly requests it.

Avoid stereotypes, fake local claims, and invented search data. Flag terms that may have multiple meanings. Ask before making sensitive cultural, medical, legal, financial, or safety claims.

### 6. Deliver the result

Return the following sections in order:

1. Audience and search-intent assessment.
2. Primary keyword and two to three approved Roman Urdu/Hinglish variants, with rejected variants noted only when helpful.
3. SEO title and meta description, including character counts when generated by the bundled script.
4. Suggested slug, focus-keyword setup, headings, internal links, and image alt-text.
5. WordPress technical findings, including Yoast/Rank Math notes, canonical, sitemap, schema, and indexability.
6. A pre-publish QA checklist and any assumptions or items requiring the user's confirmation.

## Bundled Resources

Read only the reference needed for the current task so the workflow remains focused.

- `references/roman-urdu-keyword-patterns.md`: Load for transliteration conventions, common modifiers, and the table of 20+ reusable keyword patterns.
- `references/wordpress-seo-checklist.md`: Load for WordPress-specific metadata, permalink, schema, sitemap, performance, and plugin checks.
- `references/code-mixing-guide.md`: Load for register, spelling, English-word retention, and natural Roman Urdu/Hinglish usage.
- `scripts/keyword_expander.py`: Run with an English keyword to generate deterministic supporting variants. It uses only the Python standard library and has no credentials or network dependency.
- `scripts/meta_tag_generator.py`: Run with a keyword, topic, and optional audience/benefit to draft a blended title and description. Review every draft before publishing.
- `examples/sample-optimized-post.md`: Use as an end-to-end reference for a realistic WordPress post about budget smartphones in Pakistan.

## Script Usage

Run scripts from the skill directory or provide their path from another working directory:

```bash
python scripts/keyword_expander.py "best mobile under 30000" --location Pakistan
python scripts/meta_tag_generator.py \
  --keyword "best mobile under 30000" \
  --topic "budget smartphones" \
  --audience "Pakistan ke buyers" \
  --benefit "30 hazar ke andar sahi phone choose karein"
```

Use `--json` on either script when structured output is more convenient. The scripts are offline utilities. They do not fetch keyword volume, scrape Google, call an API, or publish to WordPress.

## Activation Tests

### Activate for these requests

1. “Meri WordPress post `best mobile under 30000` ko Pakistan audience ke liye Roman Urdu SEO mein optimize karo.”
2. “WordPress ke liye `online earning ideas` ke 3 Hinglish keyword variants do.”
3. “Yoast SEO meta title aur description banao for a Lahore-focused Urdu-English blog.”
4. “Meri WordPress recipe post ke liye Roman Urdu search intent aur image alt-text check karo.”
5. “Rank Math ke sath Pakistani audience ke liye `ghar baithe paisa kamayein` content audit karo.”
6. “Desi audience ke liye WordPress slug, schema, sitemap, aur mixed-language metadata suggest karo.”

### Do not activate for these requests

1. “Give me generic English SEO keywords for a SaaS landing page.”
2. “Optimize my Shopify product page for English-speaking customers.”
3. “Translate this entire article into Urdu,” when no SEO or WordPress task is requested.
4. “Write a pure-English technical SEO audit for a custom static site.”
5. “Create a YouTube SEO strategy for a US audience.”
6. “Fix this WordPress PHP bug,” when no SEO, keyword, metadata, or search-intent work is involved.

## Functional Test Procedure

Use the supplied sample post as a representative end-to-end test:

1. Read `examples/sample-optimized-post.md` and identify the primary keyword and audience.
2. Run `scripts/keyword_expander.py` for `best mobile under 30000` with `--location Pakistan`.
3. Run `scripts/meta_tag_generator.py` with the sample's topic, audience, and benefit.
4. Compare the generated variants and metadata against the sample's approved output. Confirm that the English core remains present, the phrasing is natural, and the length warnings are visible when applicable.
5. Apply `references/wordpress-seo-checklist.md` to the sample's permalink, headings, alt-text, schema, canonical, sitemap, and plugin notes.
6. Confirm that the workflow recommends metadata and keyword localization without rewriting the English body into Roman Urdu.

## Quality and Security Rules

Do not include API keys, passwords, cookies, tokens, personal data, or hardcoded local paths in this skill or its scripts. Keep scripts portable, deterministic, and dependency-free unless a future version explicitly documents a dependency. Do not claim search volume or rankings without a cited data source. Do not publish or mutate a WordPress site unless the user explicitly authorizes the action and the required authenticated integration is available.

ClawHub skills are distributed under the platform's automatic MIT-0 terms. Do not add separate license terms, pricing, paywall metadata, or attribution requirements to this skill.
