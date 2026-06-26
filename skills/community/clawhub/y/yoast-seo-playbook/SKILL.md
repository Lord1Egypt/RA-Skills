---
name: yoast-seo-playbook
description: Yoast SEO operating playbook for WordPress delivery. Covers Yoast Free vs Yoast Premium capability boundaries, editor workflows, safe optimization QA, and when to use WordPress REST vs wp-admin for SEO tasks.
metadata: {"openclaw":{"emoji":"🔎"}}
---

# Yoast SEO Playbook (WordPress)

Use this skill when planning, reviewing, or executing SEO work on WordPress sites using Yoast.

Primary goals:
1. Keep recommendations truthful and implementable in the site's actual Yoast tier.
2. Produce editor-friendly SEO changes (titles, descriptions, schema context, readability).
3. Separate *content SEO operations* from *site design/system operations*.

## Read Order

1. [references/free-vs-premium-matrix.md](references/free-vs-premium-matrix.md)
2. [references/core-workflows.md](references/core-workflows.md)
3. [references/qa-checklist.md](references/qa-checklist.md)
4. [references/sources.md](references/sources.md)

## Operating Rules

- Confirm plugin state before proposing feature-dependent actions:
  - Is Yoast SEO active?
  - Is Yoast SEO Premium active/licensed?
- If Premium status is unknown, default to **Yoast Free-safe** guidance.
- Do not claim a feature is available unless confirmed by tier.
- Keep one clear H1 per page and logical H2/H3 hierarchy.
- Avoid fabricated SEO claims (rank guarantees, fake metrics, invented authority).
- For live content CRUD, pair with `wordpress-content-rest-api`.

## Capability Check (always first)

For any Yoast task:
1. Confirm Yoast active.
2. Confirm Free-only vs Premium.
3. Select workflow path using the matrix.
4. Mark Premium-only suggestions as optional when tier is uncertain.

## Rilvo Defaults

Unless the user states otherwise:
- Language: Italian-first (rilvo audience), with clean, direct copy.
- Style: practical, non-hype, credible.
- Prefer maintainable on-page SEO over hacks.
- Keep outputs editor-ready for WordPress/Yoast fields.

## Done Criteria

A Yoast SEO task is complete only when:
- Tier assumptions are explicit (Free vs Premium).
- Title + meta description are unique and intent-aligned.
- Heading/content structure is scannable and coherent.
- Internal link opportunities are identified (when relevant).
- Next action is clear (draft update, review, publish approval).