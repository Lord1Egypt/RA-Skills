# Notion database schema for a UI inspiration library

Use a single Notion database as the long-term UI inspiration library. Keep the first version lean and optimized for retrieval, not exhaustive taxonomy.

## Recommended properties

For concrete property mapping and creation order, also read `notion-mapping-spec.md`.

- **Name** (title)
- **Image** (files)
- **Platform** (select)
- **Page Type** (multi_select)
- **Style Tags** (multi_select)
- **Component Tags** (multi_select)
- **Use Case** (multi_select)
- **Highlights** (rich_text)
- **Summary** (rich_text)
- **Reference Value** (select)
- **Source** (rich_text)
- **Captured At** (date)

## Retrieval-oriented tagging advice

Optimize for future search. Prefer tags that help answer:
- show me B2B dashboards with dense tables,
- find dark AI product inspirations,
- find strong onboarding references,
- find list/detail patterns for web tools.

Avoid overly subjective tags unless they are stable and reusable.

## First-version constraints

For the MVP:
- use a controlled vocabulary where possible,
- keep each multi-select field compact,
- keep titles concise,
- keep summaries short,
- avoid over-specific categories when uncertain.
