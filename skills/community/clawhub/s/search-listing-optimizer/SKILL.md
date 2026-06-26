---
name: search-listing-optimizer
description: Optimize ecommerce product listings for Amazon A9, Taobao/1688 search, JD search, TikTok Shop discovery, Xiaohongshu SEO, and Shopify storefront search using keyword density frameworks, attribute-completeness checklists, and conversion-trap detection. Use when sellers need a listing audit, keyword refresh, or conversion improvement brief without live search analytics or platform API access.
---

# Search Listing Optimizer

## Overview

Use this skill to audit a product listing and generate an optimization brief covering keyword targeting, attribute completeness, image metadata, and conversion-trap detection. It applies built-in search-ranking heuristics and best-practice libraries to surface actionable improvements.

This MVP is heuristic. It does **not** connect to live search analytics, A9 algorithms, or platform seller portals. It relies on the user's provided listing notes and product context.

## Trigger

Use this skill when the user wants to:
- audit an Amazon, Taobao, JD, TikTok Shop, Xiaohongshu, or Shopify listing for search visibility
- identify missing keywords, weak attributes, or conversion traps in existing copy
- rebuild a listing keyword strategy for a new product or category entry
- compare listing quality across multiple marketplaces
- generate a before-and-after optimization brief for a product team

### Example prompts

- "Audit our Amazon skincare listing for A9 visibility"
- "Help me optimize our Taobao product listing for crowd-collapse ranking"
- "What's wrong with our JD listing that gets traffic but no conversions?"
- "Create an optimization brief for our new TikTok Shop product"

## Workflow

1. Capture the platform, product context, and optimization goal.
2. Apply keyword-density and search-intent frameworks for the target platform.
3. Assess attribute completeness across key fields.
4. Detect common conversion traps (pricing, images, reviews, description).
5. Return a markdown optimization brief with prioritized action items.

## Inputs

The user can provide any mix of:
- platform: Amazon, Taobao, 1688, JD, TikTok Shop, Xiaohongshu, Shopify, general
- product category: category name, subcategory, price range
- current listing notes: title, bullet points, description, keywords, images, reviews
- optimization goal: visibility boost, conversion improvement, new listing, relaunch
- competitor context: competitor ASINs, titles, or keyword strategies (optional)

## Outputs

Return a markdown brief with:
- platform search algorithm summary (how ranking works on that platform)
- keyword opportunity map (search volume intent × competition)
- listing attribute scorecard (title, bullets, description, backend keywords, images)
- conversion-trap detection (pricing, trust signals, review depth, description clarity)
- prioritized action list with expected impact
- template for revised title, bullets, or description

## Safety

- No live search analytics, ad console, or seller portal access.
- Optimization recommendations are directional; actual ranking depends on platform algorithms.
- Do not claim guaranteed ranking improvements or sales lift.
- Pricing and promotional decisions remain with the operator.

## Best-fit Scenarios

- sellers preparing new listings or refreshing existing ones for better visibility
- teams managing multiple marketplace accounts needing a consistent audit framework
- brands expanding to new platforms and needing a listing best-practice brief

## Not Ideal For

- real-time rank tracking, automated listing updates, or live ad campaign management
- products in highly regulated categories with strict claim restrictions
- very early-stage products with no sales history or review data

## Acceptance Criteria

- Return markdown text.
- Include attribute scorecard, keyword opportunity map, and prioritized action list.
- Make ranking assumptions explicit.
- Keep the brief practical for marketplace sellers and listing specialists.
